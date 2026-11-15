#!/usr/bin/env python3
"""Arithmetic Behavior Benchmark: trusted-side local pilot CLI.

Do NOT put this script, arithmetic_eval/, or cases/private/ in an agent sandbox.
The probe API must be mediated by a trusted process in a production harness.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import secrets
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from arithmetic_eval.generate import generate, read_json, write_json
from arithmetic_eval.grade import math_baseline, oracle_prediction, score
from arithmetic_eval.student import OPS, RULES, answer, correct


def _session_path(root: Path, name: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", name):
        raise ValueError("Session name must be 1..80 ASCII alphanumeric, underscore, or dash")
    return root / "private" / "sessions" / f"{name}.json"


def _get_session(root: Path, name: str) -> tuple[Path, dict, dict, dict]:
    path = _session_path(root, name)
    if not path.exists():
        raise ValueError(f"Unknown session: {name}")
    session = read_json(path)
    case = session["case"]
    pub = read_json(root / "public" / f"{case}.json")
    pri = read_json(root / "private" / f"{case}.json")
    return path, session, pub, pri


def _print(obj: dict) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def cmd_generate(args) -> None:
    _print(generate(Path(args.root), seed=args.seed, easy_per_op=args.easy_per_op, l2_count=args.level2, l3_per_op=args.level3_per_op))


def cmd_show(args) -> None:
    _print(read_json(Path(args.root) / "public" / f"{args.case}.json"))


def cmd_start(args) -> None:
    root = Path(args.root)
    if not 0 <= args.budget <= 10:
        raise ValueError("Probe budget must be 0..10")
    if not (root / "private" / f"{args.case}.json").exists():
        raise ValueError(f"Unknown case {args.case}")
    path = _session_path(root, args.session)
    if path.exists() and not args.overwrite:
        raise ValueError("Session already exists; use --overwrite to reset explicitly")
    state = {"case": args.case, "budget": args.budget, "probes": [], "submissions": [],
             "closed": False, "api_token": secrets.token_urlsafe(24), "created_utc": datetime.now(timezone.utc).isoformat()}
    write_json(path, state)
    _print({"session": args.session, "case": args.case, "budget": args.budget,
            "remaining": args.budget, "api_token": state["api_token"],
            "task_file": str(root / 'public' / f'{args.case}.json')})


def cmd_probe(args) -> None:
    root = Path(args.root)
    path, state, pub, pri = _get_session(root, args.session)
    if state["closed"]:
        raise ValueError("Session is closed")
    if len(state["probes"]) >= state["budget"]:
        raise ValueError("Probe budget exhausted")
    op, a, b = args.op, args.a, args.b
    if op not in OPS or not 0 <= a <= 1000000 or not 0 <= b <= 1000000 or (op == "div" and b == 0):
        raise ValueError("Invalid operation or operands")
    if op == "sub" and a < b:
        raise ValueError("Subtraction requires a >= b")
    if op == "div" and a % b != 0:
        raise ValueError("Only exact-integer division questions are supported")
    held_out = {(q["op"], q["a"], q["b"]) for q in pub["test_questions"]}
    if (op, a, b) in held_out:
        raise ValueError("Cannot probe an exact held-out test problem")
    y = answer(op, a, b, pri["rules"][op])
    state["probes"].append({"op": op, "a": a, "b": b, "student_answer": y})
    write_json(path, state)
    _print({"op": op, "a": a, "b": b, "student_answer": y,
            "used": len(state["probes"]), "remaining": state["budget"] - len(state["probes"])})


def cmd_submit(args) -> None:
    root = Path(args.root)
    path, state, pub, pri = _get_session(root, args.session)
    if state["closed"]:
        raise ValueError("Session is closed")
    submission = read_json(Path(args.submission))
    # Intentionally do not reveal validation against hidden test answers.
    from arithmetic_eval.grade import parse_predictions
    _, schema_error = parse_predictions(submission, pub["test_questions"])
    if schema_error:
        # Preserve for a reproducible zero-scoring submission rather than silently fix it.
        print(f"WARNING: malformed submission will score 0: {schema_error}")
    state["submissions"].append({"after_probes": len(state["probes"]), "submission": submission})
    write_json(path, state)
    _print({"snapshot_saved": len(state["submissions"]), "after_probes": len(state["probes"]),
            "hidden_accuracy_revealed": False})


def cmd_grade(args) -> None:
    root = Path(args.root)
    path, state, pub, pri = _get_session(root, args.session)
    if args.submission:
        state["submissions"].append({"after_probes": len(state["probes"]),
                                      "submission": read_json(Path(args.submission))})
    if not state["submissions"]:
        raise ValueError("No predictions submitted; use submit or grade --submission")
    timeline = []
    for idx, snapshot in enumerate(state["submissions"]):
        results = score(pub, pri, snapshot["submission"], state["probes"][:snapshot["after_probes"]])
        timeline.append({"snapshot": idx + 1, "after_probes": snapshot["after_probes"], **results})
    perfect_error = [r["after_probes"] for r in timeline if r["valid"] and r["primary_accuracy"] == 1.0]
    perfect_all = [r["after_probes"] for r in timeline if r["valid"] and r["overall_accuracy"] == 1.0]
    report = {
        "case": state["case"], "session": args.session, "budget": state["budget"],
        "level": pri["level"], "difficulty": pri["family"],
        "hidden_labels": {op: sorted({RULES[op][r["name"]][0] for r in rr})
                          for op, rr in pri["rules"].items() if rr},
        "probes_used": len(state["probes"]), "snapshots": timeline,
        "last_snapshot": timeline[-1], "k100_error_observed": min(perfect_error) if perfect_error else None,
        "k100_all_observed": min(perfect_all) if perfect_all else None,
        "k95_error_observed": min((r["after_probes"] for r in timeline if r["valid"] and r["primary_accuracy"] >= .95), default=None),
        "k100_note": "Earliest observed submitted snapshot, not theoretical minimum. Submit once at k=0 and after every probe to measure the full curve.",
    }
    out = root / "private" / "reports" / f"{args.session}.json"
    write_json(out, report)
    state["closed"] = True
    write_json(path, state)
    _print(report)


def cmd_baseline(args) -> None:
    public = read_json(Path(args.root) / "public" / f"{args.case}.json")
    write_json(Path(args.out), math_baseline(public))
    _print({"written": args.out, "case": args.case})


def cmd_oracle(args) -> None:
    root = Path(args.root)
    _, state, pub, pri = _get_session(root, args.session)
    pred, survivors = oracle_prediction(pub, pri, state["probes"])
    result = {"session": args.session, "compatible_models": survivors, "oracle_score": score(pub, pri, pred, state["probes"]),
              "caveat": "Uniform majority-vote baseline over specified model family; not a universal upper bound"}
    if args.out:
        write_json(Path(args.out), pred)
        result["predictions_written"] = args.out
    _print(result)


def cmd_summarize(args) -> None:
    root = Path(args.root)
    reports = sorted((root / "private" / "reports").glob("*.json"))
    with Path(args.out).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["session", "case", "budget", "after_probes",
                                                 "level", "labels", "primary_accuracy", "overall_accuracy", "macro_error_accuracy", "transfer_error_accuracy", "brier_error_cases",
                                                 "k100_error_observed", "k100_all_observed"])
        writer.writeheader()
        for path in reports:
            rep = read_json(path)
            for snap in rep["snapshots"]:
                cal = snap.get("calibration_error_cases") or {}
                writer.writerow({"session": rep["session"], "case": rep["case"],
                                 "budget": rep["budget"], "after_probes": snap["after_probes"],
                                 "level": rep.get("level"),
                                 "labels": ";".join(sorted({name for ids in rep.get("hidden_labels", {}).values() for name in ids})),
                                 "primary_accuracy": snap["primary_accuracy"],
                                 "overall_accuracy": snap["overall_accuracy"],
                                 "macro_error_accuracy": snap.get("macro_error_accuracy"),
                                 "transfer_error_accuracy": snap.get("transfer_error_accuracy"),
                                 "brier_error_cases": cal.get("brier"),
                                 "k100_error_observed": rep["k100_error_observed"],
                                 "k100_all_observed": rep["k100_all_observed"]})
    _print({"reports": len(reports), "written": args.out})


def cmd_export(args) -> None:
    """Create a safe-to-share task handoff with NO simulator or answer key."""
    public_path = Path(args.root) / "public" / f"{args.case}.json"
    if not public_path.exists():
        raise ValueError(f"Unknown case {args.case}")
    prompt_path = Path(__file__).resolve().parent / "prompts" / "agent_prompt.txt"
    with zipfile.ZipFile(args.out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(public_path, arcname="task.json")
        z.write(prompt_path, arcname="agent_prompt.txt")
    _print({"agent_bundle": args.out, "contains": ["task.json", "agent_prompt.txt"],
            "private_files": 0})


def cmd_serve(args) -> None:
    from arithmetic_eval.server import serve
    serve(Path(args.root), args.host, args.port)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate", help="Generate public/private case files")
    gen.add_argument("--root", default="cases")
    gen.add_argument("--seed", type=int, default=20261115)
    gen.add_argument("--easy-per-op", type=int, default=2)
    gen.add_argument("--level2", type=int, default=4)
    gen.add_argument("--level3-per-op", type=int, default=1)
    gen.set_defaults(func=cmd_generate)
    show = sub.add_parser("show", help="Show agent-visible task only")
    show.add_argument("--root", default="cases")
    show.add_argument("--case", required=True)
    show.set_defaults(func=cmd_show)
    start = sub.add_parser("start", help="Initialize independent query-budget session")
    start.add_argument("--root", default="cases")
    start.add_argument("--case", required=True)
    start.add_argument("--budget", type=int, default=3)
    start.add_argument("--session", required=True)
    start.add_argument("--overwrite", action="store_true")
    start.set_defaults(func=cmd_start)
    probe = sub.add_parser("probe", help="Query student once (trusted side only)")
    probe.add_argument("--root", default="cases")
    probe.add_argument("--session", required=True)
    probe.add_argument("--op", choices=OPS, required=True)
    probe.add_argument("--a", type=int, required=True)
    probe.add_argument("--b", type=int, required=True)
    probe.set_defaults(func=cmd_probe)
    submit = sub.add_parser("submit", help="Store prediction snapshot; DOES NOT disclose score")
    submit.add_argument("--root", default="cases")
    submit.add_argument("--session", required=True)
    submit.add_argument("--submission", required=True)
    submit.set_defaults(func=cmd_submit)
    grade = sub.add_parser("grade", help="Close session and release grader report")
    grade.add_argument("--root", default="cases")
    grade.add_argument("--session", required=True)
    grade.add_argument("--submission", default=None)
    grade.set_defaults(func=cmd_grade)
    baseline = sub.add_parser("baseline", help="Create mathematically-correct baseline submission")
    baseline.add_argument("--root", default="cases")
    baseline.add_argument("--case", required=True)
    baseline.add_argument("--out", required=True)
    baseline.set_defaults(func=cmd_baseline)
    oracle = sub.add_parser("oracle", help="Trusted-side uniform compatible-model reasoner")
    oracle.add_argument("--root", default="cases")
    oracle.add_argument("--session", required=True)
    oracle.add_argument("--out", default=None)
    oracle.set_defaults(func=cmd_oracle)
    summ = sub.add_parser("summarize", help="Export score-vs-probe CSV from reports")
    summ.add_argument("--root", default="cases")
    summ.add_argument("--out", default="probe_curve.csv")
    summ.set_defaults(func=cmd_summarize)
    expo = sub.add_parser("export", help="Package public task and prompt only for sharing with agents")
    expo.add_argument("--root", default="cases")
    expo.add_argument("--case", required=True)
    expo.add_argument("--out", required=True)
    expo.set_defaults(func=cmd_export)
    server = sub.add_parser("serve", help="Serve authenticated agent probe/snapshot API (local pilot)")
    server.add_argument("--root", default="cases")
    server.add_argument("--host", default="127.0.0.1")
    server.add_argument("--port", type=int, default=8787)
    server.set_defaults(func=cmd_serve)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
