#!/usr/bin/env python3
"""Run an isolated LLM agent against BEHAVIOR-PROBE cases (trusted side).

The agent is `claude -p` with ALL tools disabled, user settings/hooks/MCP off,
launched from an empty temp dir. It sees only the public case text and the probe
answers this script relays. Budgets are enforced by behavior_probe.probe().

    cp -R cases runs            # fresh root so reports don't mix with other runs
    python3 agent_eval.py --root runs --cases S001 --budgets 3          # smoke test
    python3 agent_eval.py --root runs --budgets 0 3 10 --workers 6      # full run
"""
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import behavior_probe as bp

SYSTEM = "You are being evaluated on predicting a simulated student's behavior. Follow the reply protocol exactly."

PROTOCOL = """Here is the case (JSON):

{case}

You have a probe budget of {budget}. A probe asks the student one new subtraction
problem a - b (a has 3 or 4 digits, 0 <= b <= a, and it must not be one of the
test questions) and returns the student's answer.

Reply protocol - every reply must be exactly ONE of:
  PROBE <a> <b>
      (one probe per reply; only while you have probes left)
  SUBMIT
  {{"predictions": [{{"id": "Q01", "answer": <int>, "confidence": <0..1>}}, ...]}}
      (all 40 test question IDs; confidence = probability your answer equals
      the STUDENT's answer)

Probes remaining: {budget}."""

SUBMIT_RE = re.compile(r"SUBMIT\s*(\{.*\})", re.S)
PROBE_RE = re.compile(r"^\s*PROBE\s+(\d+)\s+(\d+)\s*$", re.M)


def ask(prompt: str, session: str | None, model: str, cwd: str) -> tuple[str, str, float]:
    cmd = ["claude", "-p", prompt, "--model", model, "--output-format", "json",
           "--tools", "", "--setting-sources", "", "--strict-mcp-config",
           "--system-prompt", SYSTEM]
    if session:
        cmd += ["--resume", session]
    # Drop a parent Claude session's proxy/auth wiring; keep the rest (e.g. CLAUDE_CONFIG_DIR).
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("CLAUDE_CODE_", "CLAUDE_AGENT_SDK", "CLAUDECODE", "CLAUDE_PID"))
           and k != "ANTHROPIC_BASE_URL"}
    out = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=1800)
    try:
        d = json.loads(out.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"claude CLI failed: {out.stderr.strip() or out.stdout[:300]}")
    if d.get("is_error"):
        raise RuntimeError(f"claude CLI error: {d.get('result')}")
    return d["result"], d["session_id"], d.get("total_cost_usd") or 0.0


def quiet(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*a)
    return buf.getvalue().strip()


def run_one(root: Path, case: str, budget: int, model: str, tag: str) -> dict:
    sess = f"{case}_b{budget}_{tag}"
    quiet(bp.start_session, root, case, budget, sess)
    pub = bp.read_json(root / "public" / f"{case}.json")
    msg = PROTOCOL.format(case=json.dumps(pub, indent=1), budget=budget)
    transcript, cid, cost = [], None, 0.0
    sub_path = root / "private" / "submissions" / f"{sess}.json"
    sub_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as empty:
        # ponytail: fixed turn cap; raise if agents legitimately need more retries
        for _ in range(budget + 4):
            reply, cid, c = ask(msg, cid, model, empty)
            cost += c
            transcript += [{"to_agent": msg}, {"from_agent": reply}]
            m_sub, m_probe = SUBMIT_RE.search(reply), PROBE_RE.search(reply)
            if m_sub:
                try:
                    sub_path.write_text(m_sub.group(1))
                    report = bp.grade(root, sess, sub_path)
                    report["cost_usd"] = round(cost, 4)
                    bp.write_json(root / "private" / "transcripts" / f"{sess}.json", transcript)
                    return report
                except (ValueError, json.JSONDecodeError) as e:
                    msg = f"Submission rejected: {e}. Reply with a corrected SUBMIT."
            elif m_probe:
                try:
                    res = json.loads(quiet(bp.probe, root, sess, int(m_probe[1]), int(m_probe[2])))
                    msg = (f"{res['a']} - {res['b']}: student answered {res['student_answer']}. "
                           f"Probes remaining: {res['remaining']}.")
                except ValueError as e:
                    msg = f"Probe rejected: {e}. Reply with PROBE or SUBMIT."
            else:
                msg = "Reply must be exactly `PROBE <a> <b>` or `SUBMIT` + JSON."
    bp.write_json(root / "private" / "transcripts" / f"{sess}.json", transcript)
    raise RuntimeError(f"{sess}: no valid submission within turn limit")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, required=True)
    ap.add_argument("--cases", nargs="*", help="default: all in manifest")
    ap.add_argument("--budgets", type=int, nargs="+", default=[0, 3, 10])
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--tag", default="t1", help="trial label; new tag = new independent sessions")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    cases = args.cases or bp.read_json(args.root / "manifest.json")["case_ids"]
    jobs = [(c, b) for c in cases for b in args.budgets]
    with ThreadPoolExecutor(args.workers) as ex:
        futs = {ex.submit(run_one, args.root, c, b, args.model, args.tag): (c, b) for c, b in jobs}
        for f in as_completed(futs):
            c, b = futs[f]
            try:
                r = f.result()
                print(f"{c} b={b}: err-acc={r['primary_wrong_answer_accuracy']} "
                      f"overall={r['overall_accuracy_diagnostic']} probes={r['probes_used']} "
                      f"brier={r['calibration_on_wrong_questions']['brier_lower_is_better']} ${r['cost_usd']}",
                      flush=True)
            except Exception as e:  # keep the batch going; failures are listed
                print(f"{c} b={b}: FAILED {e}", flush=True)
    bp.summarize(args.root, args.root / "probe_curve.csv")


if __name__ == "__main__":
    main()
