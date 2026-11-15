"""BEHAVIOR-PROBE as a Valkyrie benchmark service.

Isolation: the hidden rules, answers and oracle stay on this host. The sandbox only
gets the public case text (and, in the `probe10` dataset, a `probe` command that asks
the probe server below, which enforces the budget). Grading downloads the agent's
submission and scores it here with behavior_probe.grade().

Datasets:
  noprobe  - budget 0, no probe tool (headline score; the "real world" setting)
  probe10  - an OPTIONAL probe tool with budget 10; we record how many each model uses
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import shutil
import sys
import threading
import uuid
from collections.abc import AsyncGenerator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from benchmark_service import BenchmarkService, ImageSource, Resources, Sandbox
from benchmark_service.schemas import (
    BenchmarkEgressPlan,
    EvaluateResponseRequest,
    FinalScoreResult,
    RetrieveTaskResponse,
    StreamChunk,
    StreamMessageChunk,
    StreamResultChunk,
)
from benchmark_service.v1_schemas import V1Task

PROJECT = Path(os.environ.get("BP_PROJECT", Path(__file__).resolve().parents[4]))
sys.path.insert(0, str(PROJECT))
import behavior_probe as bp  # noqa: E402
import hard_probe as hp  # noqa: E402

DATA = Path(os.environ.get("BP_DATA", PROJECT / "valkyrie" / "bp_data"))
# Suite -> (case root, source to copy from, probe fn, max digits of A for probes)
SUITES = {
    "easy": (DATA / "cases", PROJECT / "cases", bp.probe, 4),
    "hard": (DATA / "hard_cases", PROJECT / "hard_cases", hp.probe, 5),
}
# Dataset -> (suite, probe budget)
DATASETS = {"noprobe": ("easy", 0), "probe10": ("easy", 10),
            "hard-noprobe": ("hard", 0), "hard-probe3": ("hard", 3), "hard-probe10": ("hard", 10)}
# Not 8002: the local Tracker's executor control app binds 127.0.0.1:8002, and sandbox
# traffic via host.docker.internal lands there instead of here.
PROBE_PORT = int(os.environ.get("BP_PROBE_PORT", "8020"))
# Docker Desktop: containers reach the host here. Override for other setups.
PROBE_HOST = os.environ.get("BP_PROBE_HOST", "host.docker.internal")
IMAGE = os.environ.get("BP_IMAGE", "bp-sandbox:latest")  # built from valkyrie/sandbox-image
SUBMISSION = "/workspace/submission.json"

LOCK = threading.Lock()  # ponytail: one global lock around file-backed oracle state; fine at this scale
TOKENS_FILE = DATA / "tokens.json"  # sandbox id -> [suite, token]; on disk so a restart keeps sessions
TOKENS: dict[str, list[str]] = json.loads(TOKENS_FILE.read_text()) if TOKENS_FILE.exists() else {}


def save_tokens() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    TOKENS_FILE.write_text(json.dumps(TOKENS))


def quiet(fn, *args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = fn(*args)
    return out, buf.getvalue().strip()


class ProbeHandler(BaseHTTPRequestHandler):
    """POST /probe {"token","a","b"} -> student's answer. Budget enforced by bp.probe."""

    def do_POST(self):  # noqa: N802
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            token = bp.safe_id(str(body["token"]))
            suite = next((s for s, t in TOKENS.values() if t == token), None)
            if suite is None:
                raise ValueError("Unknown token")
            root, _, probe_fn, _ = SUITES[suite]
            with LOCK:
                _, out = quiet(probe_fn, root, token, int(body["a"]), int(body["b"]))
            code, payload = 200, json.loads(out)
        except (ValueError, KeyError, TypeError, json.JSONDecodeError) as e:
            code, payload = 400, {"error": str(e)}
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args):
        pass


PROBE_SCRIPT = """#!/usr/bin/env python3
import json, sys, urllib.request
if len(sys.argv) != 3:
    sys.exit("usage: probe A B")
req = urllib.request.Request("http://{host}:{port}/probe", method="POST",
    data=json.dumps({{"token": "{token}", "a": sys.argv[1], "b": sys.argv[2]}}).encode(),
    headers={{"Content-Type": "application/json"}})
try:
    print(urllib.request.urlopen(req, timeout=30).read().decode())
except urllib.error.HTTPError as e:
    print(e.read().decode()); sys.exit(1)
"""


def problem_text(case: dict[str, Any], budget: int, max_digits: int = 4) -> str:
    probe_part = (
        f"\nOptional tool: you may run `probe A B` (A has 3-{max_digits} digits, 0 <= B <= A, not one of the "
        f"test questions) to see this student's answer to A - B. You can use it up to {budget} times. "
        "Using it is entirely up to you.\n"
        if budget
        else ""
    )
    return (
        "You are predicting how one specific student does subtraction.\n\n"
        f"{case['task']}\nDo not assume the student always computes correctly.\n"
        f"{probe_part}\n"
        f"Write your predictions to {SUBMISSION} as JSON:\n"
        '{"predictions": [{"id": "Q01", "answer": <integer>, "confidence": <0.0-1.0>}, ...]}\n'
        "Include every one of the 40 test question ids. confidence is the probability that your answer "
        "exactly equals the STUDENT's answer.\n\n"
        "Case data:\n" + json.dumps({k: case[k] for k in ("id", "observations", "test_questions")}, indent=1)
    )


class BehaviorProbeBenchmark(BenchmarkService):
    async def load_datasets(self) -> dict[str, dict[str, Any]]:
        for root, src, _, _ in SUITES.values():
            if not root.exists():
                shutil.copytree(src, root)
        threading.Thread(
            target=ThreadingHTTPServer(("0.0.0.0", PROBE_PORT), ProbeHandler).serve_forever, daemon=True
        ).start()
        out = {}
        for name, (suite, budget) in DATASETS.items():
            ids = bp.read_json(SUITES[suite][0] / "manifest.json")["case_ids"]
            out[name] = {cid: {"suite": suite, "budget": budget} for cid in ids}
        return out

    async def list_tasks(self, dataset: str | None = None) -> list[V1Task]:
        return [V1Task(id=cid, question=cid) for cid in self.get_dataset(dataset)]

    async def retrieve_task(
        self, task_id: str, skip_validation: bool = False, dataset: str | None = None
    ) -> RetrieveTaskResponse:
        if not skip_validation:
            await self.validate_task_ids([task_id], dataset=dataset)
        return RetrieveTaskResponse(
            source=ImageSource(image=IMAGE),
            problem_path="/tmp/problem_statement.txt",
            cwd="/workspace",
            agent_timeout=1800.0,
            resources=Resources(vcpu=2, memory=4, disk=10),
            # Docker sandboxes require unrestricted egress (the agent needs its model API anyway).
            egress=BenchmarkEgressPlan(setup_task="*", run="*", evaluation="*"),
        )

    async def setup_task(
        self, task_id: str, sandbox: Sandbox, dataset: str | None = None
    ) -> AsyncGenerator[StreamChunk, None]:
        meta = self.get_dataset(dataset)[task_id]
        suite, budget = meta["suite"], meta["budget"]
        root, _, _, max_digits = SUITES[suite]
        token = f"{task_id}_b{budget}_{uuid.uuid4().hex[:12]}"
        with LOCK:
            quiet(bp.start_session, root, task_id, budget, token)
            TOKENS[sandbox.id] = [suite, token]
            save_tokens()
        case = bp.read_json(root / "public" / f"{task_id}.json")
        await sandbox.exec("mkdir -p /workspace")
        await sandbox.upload_file("/tmp/problem_statement.txt", problem_text(case, budget, max_digits).encode())
        if budget:
            script = PROBE_SCRIPT.format(host=PROBE_HOST, port=PROBE_PORT, token=token)
            await sandbox.upload_file("/usr/local/bin/probe", script.encode())
            await sandbox.exec("chmod +x /usr/local/bin/probe")
        yield StreamMessageChunk(type="message", data=f"{task_id}: budget {budget}, session {token}")
        yield StreamResultChunk(type="result", data={"status": "ok"})

    async def evaluate_instance(
        self, task_id: str, sandbox: Sandbox, dataset: str | None = None
    ) -> AsyncGenerator[StreamChunk, None]:
        if sandbox.id not in TOKENS:
            yield StreamResultChunk(type="result", data={"case": task_id, "error": "no oracle session"})
            return
        suite, token = TOKENS[sandbox.id]
        root = SUITES[suite][0]
        report_path = root / "private" / "reports" / f"{token}.json"
        sub_path = root / "private" / "submissions" / f"{token}.json"
        try:
            raw = await sandbox.download_file(SUBMISSION)
            sub_path.parent.mkdir(parents=True, exist_ok=True)
            sub_path.write_bytes(raw)
            with LOCK:
                report = bp.read_json(report_path) if report_path.exists() else quiet(bp.grade, root, token, sub_path)[0]
        except Exception as e:  # missing/invalid submission scores 0, but keep probe usage
            state = bp.read_json(bp.session_path(root, token))
            report = {"case": task_id, "session": token, "error": f"{type(e).__name__}: {e}",
                      "probe_budget": state["budget"], "probes_used": len(state["probes"]),
                      "primary_wrong_answer_accuracy": 0.0}
        yield StreamMessageChunk(type="message", data=json.dumps({k: report.get(k) for k in (
            "primary_wrong_answer_accuracy", "overall_accuracy_diagnostic", "probes_used", "error")}))
        yield StreamResultChunk(type="result", data=report)

    async def evaluate_response(self, request: EvaluateResponseRequest, dataset: str | None = None) -> Any:
        raise ValueError("This benchmark grades in the sandbox")

    async def calculate_final_score(
        self, evaluation_results: dict[str, Any], dataset: str | None = None
    ) -> FinalScoreResult:
        rs = list(evaluation_results.values())
        ok = [r for r in rs if r and "error" not in r]

        def mean(xs):
            xs = [x for x in xs if x is not None]
            return round(sum(xs) / len(xs), 4) if xs else None

        return FinalScoreResult(
            # Primary: accuracy on student-error questions; unfinished/invalid tasks count as 0.
            score=100 * sum((r or {}).get("primary_wrong_answer_accuracy") or 0 for r in rs) / max(len(rs), 1),
            metadata={
                "tasks": len(rs),
                "valid_submissions": len(ok),
                "mean_probes_used": mean([(r or {}).get("probes_used") for r in rs]),
                "overall_accuracy": mean([r["overall_accuracy_diagnostic"] for r in ok]),
                "familiar_err_acc": mean([r["wrong_answer_accuracy_by_domain"]["familiar"] for r in ok]),
                "transfer_err_acc": mean([r["wrong_answer_accuracy_by_domain"]["transfer"] for r in ok]),
                "brier": mean([r["calibration_on_wrong_questions"]["brier_lower_is_better"] for r in ok]),
                "ece": mean([r["calibration_on_wrong_questions"]["ece_5bins_lower_is_better"] for r in ok]),
            },
        )
