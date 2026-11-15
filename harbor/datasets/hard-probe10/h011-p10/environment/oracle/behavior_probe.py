#!/usr/bin/env python3
"""BEHAVIOR-PROBE: deterministic student-simulator benchmark prototype.

Python standard library only. This is a trusted-side generator/oracle/grader.
Never mount this script, private/, or reference answers in the evaluated agent's sandbox.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

BUGS = ("smaller_from_larger", "forget_decrement", "write_zero", "zero_bridge")
SCOPES = ("any", "ones_only", "tens_only", "next_digit_zero")
BUDGETS = (0, 3, 10)


@dataclass(frozen=True)
class StudentRule:
    bug: str
    scope: str = "any"


def student_answer(a: int, b: int, rule: StudentRule) -> int:
    """Simulate right-to-left column subtraction with one systematic procedural bug.

    All tasks use non-negative subtraction (a>=b). The returned answer is not a
    random wrong number: it is the output of a deterministic digit algorithm.
    """
    if not (isinstance(a, int) and isinstance(b, int) and a >= b >= 0):
        raise ValueError("Require integers with a >= b >= 0")
    if rule.bug not in BUGS or rule.scope not in SCOPES:
        raise ValueError("Unknown virtual student rule")

    length = max(len(str(a)), len(str(b)))
    x, y = a, b
    borrow = 0
    result = 0
    place = 1

    for col in range(length):
        upper, lower = x % 10, y % 10
        x //= 10
        y //= 10

        # The zero-bridge mistake: a student fails to propagate an incoming
        # borrow through a zero in a higher column.
        if rule.bug == "zero_bridge" and borrow and upper == 0 and col > 0:
            borrow = 0

        diff = upper - borrow - lower
        if diff < 0:
            applies = (
                rule.scope == "any"
                or (rule.scope == "ones_only" and col == 0)
                or (rule.scope == "tens_only" and col == 1)
                or (rule.scope == "next_digit_zero" and x % 10 == 0 and col + 1 < length)
            )
            if applies and rule.bug == "smaller_from_larger":
                # Flip the smaller/larger digits rather than borrowing.
                digit = abs(upper - lower)
                borrow = 0
            elif applies and rule.bug == "forget_decrement":
                # Borrow 10 but forget to decrement the next column.
                digit = diff + 10
                borrow = 0
            elif applies and rule.bug == "write_zero":
                # Write 0 in the problematic column instead of borrowing.
                digit = 0
                borrow = 0
            else:
                digit = diff + 10
                borrow = 1
        else:
            digit = diff
            borrow = 0
        if not 0 <= digit <= 9:
            raise AssertionError("Digit out of range")
        result += digit * place
        place *= 10
    return result


def choose_item(rng: random.Random, digits: int, want_wrong: bool, rule: StudentRule,
                used: set[tuple[int, int]]) -> dict[str, int]:
    low, high = 10 ** (digits - 1), 10**digits - 1
    for _ in range(250_000):
        a = rng.randint(low, high)
        b = rng.randint(0, a)
        if (a, b) in used:
            continue
        got = student_answer(a, b, rule)
        if (got != a - b) == want_wrong:
            used.add((a, b))
            return {"a": a, "b": b, "student_answer": got}
    raise RuntimeError(f"Could not sample enough examples: {rule}, digits={digits}, wrong={want_wrong}")


def make_case(rng: random.Random, cid: str, rule: StudentRule, n_initial: int = 6) -> tuple[dict[str, Any], dict[str, Any]]:
    used: set[tuple[int, int]] = set()
    observed = [choose_item(rng, 3, True, rule, used) for _ in range(2)]
    observed += [choose_item(rng, 3, False, rule, used) for _ in range(n_initial - 2)]
    rng.shuffle(observed)

    # 40 hidden questions, half 3-digit and half 4-digit; each split has
    # 10 genuine student errors and 10 correct answers. No overlaps.
    hidden_items: list[dict[str, Any]] = []
    for digits, domain in ((3, "familiar"), (4, "transfer")):
        for wrong in (True, False):
            for _ in range(10):
                item = choose_item(rng, digits, wrong, rule, used)
                hidden_items.append({**item, "domain": domain, "student_is_wrong": wrong})
    rng.shuffle(hidden_items)
    public_questions: list[dict[str, Any]] = []
    answers: dict[str, dict[str, Any]] = {}
    for i, item in enumerate(hidden_items, 1):
        qid = f"Q{i:02d}"
        public_questions.append({"id": qid, "a": item["a"], "b": item["b"]})
        answers[qid] = {
            "answer": item["student_answer"],
            "student_is_wrong": item["student_is_wrong"],
            "domain": item["domain"],
        }

    public = {
        "id": cid,
        "task": "Infer this individual student's subtraction behavior from observed answers. "
                "Predict the answers the student, not a calculator, will give on new questions.",
        "instructions": "You may request up to your session's probe budget. Submit an integer answer "
                        "and a confidence from 0.0 to 1.0 for every test question. "
                        "Do not assume the student always computes correctly.",
        "observations": [{"a": x["a"], "b": x["b"], "student_answer": x["student_answer"]} for x in observed],
        "test_questions": public_questions,
    }
    private = {
        "id": cid,
        "rule": {"bug": rule.bug, "scope": rule.scope},
        "test_answers": answers,
    }
    return public, private


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def generate(root: Path, seed: int, n: int) -> None:
    if n < 1:
        raise ValueError("Number of cases must be positive")
    root.mkdir(parents=True, exist_ok=True)
    specs = [StudentRule(bug, scope) for bug in BUGS[:3] for scope in SCOPES]
    specs += [StudentRule("zero_bridge", "any")]
    random.Random(seed).shuffle(specs)
    cases = []
    for i in range(n):
        cid = f"S{i+1:03d}"
        # Keep the rule selection varied; all generation is seeded/reproducible.
        spec = specs[i % len(specs)]
        rng = random.Random(seed + 1009 * (i + 1))
        public, private = make_case(rng, cid, spec)
        write_json(root / "public" / f"{cid}.json", public)
        write_json(root / "private" / f"{cid}.json", private)
        cases.append(cid)
    write_json(root / "manifest.json", {"seed": seed, "case_ids": cases,
                                        "allowed_probe_budgets": list(BUDGETS)})
    print(f"Generated {len(cases)} cases at {root.resolve()}")
    print("Give evaluated agents ONLY files in public/; keep private/ and this script trusted-side.")


def safe_id(v: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,64}", v):
        raise ValueError("ID may contain only A-Z, a-z, 0-9, underscore and hyphen")
    return v


def session_path(root: Path, session: str) -> Path:
    return root / "private" / "sessions" / f"{safe_id(session)}.json"


def start_session(root: Path, case: str, budget: int, session: str) -> None:
    safe_id(case)
    if budget not in BUDGETS:
        raise ValueError(f"Supported budgets: {BUDGETS}")
    if not (root / "public" / f"{case}.json").exists():
        raise ValueError("Unknown case")
    state_path = session_path(root, session)
    if state_path.exists():
        raise ValueError("Session ID already exists; choose a fresh ID")
    state = {"case": case, "budget": budget, "probes": [], "graded": False}
    write_json(state_path, state)
    print(json.dumps({"session": session, "case": case, "remaining": budget}))


def probe(root: Path, session: str, a: int, b: int) -> None:
    path = session_path(root, session)
    state = read_json(path)
    if state["graded"]:
        raise ValueError("Session already graded")
    if len(state["probes"]) >= state["budget"]:
        raise ValueError("No probes remaining")
    if not (100 <= a <= 9999 and 0 <= b <= a):
        raise ValueError("Probe must use 3- or 4-digit a, with 0 <= b <= a")
    case = state["case"]
    public = read_json(root / "public" / f"{case}.json")
    forbidden = {(q["a"], q["b"]) for q in public["test_questions"]}
    if (a, b) in forbidden:
        raise ValueError("Cannot directly probe a held-out evaluation question")
    private = read_json(root / "private" / f"{case}.json")
    rule = StudentRule(**private["rule"])
    answer = student_answer(a, b, rule)
    state["probes"].append({"a": a, "b": b, "student_answer": answer})
    write_json(path, state)
    print(json.dumps({"a": a, "b": b, "student_answer": answer,
                      "remaining": state["budget"] - len(state["probes"])}))


def _mean(xs: list[float]) -> float | None:
    return round(sum(xs) / len(xs), 4) if xs else None


def grade(root: Path, session: str, submission_file: Path) -> dict[str, Any]:
    state_file = session_path(root, session)
    state = read_json(state_file)
    if state["graded"]:
        raise ValueError("Session already graded")
    pub = read_json(root / "public" / f"{state['case']}.json")
    priv = read_json(root / "private" / f"{state['case']}.json")
    submission = read_json(submission_file)
    raw = submission.get("predictions")
    if not isinstance(raw, list):
        raise ValueError("Expected a JSON object with a predictions list")
    questions = {q["id"]: q for q in pub["test_questions"]}
    predictions: dict[str, dict[str, Any]] = {}
    for p in raw:
        if not isinstance(p, dict) or p.get("id") not in questions or p["id"] in predictions:
            raise ValueError("Unknown or duplicated prediction ID")
        answer, confidence = p.get("answer"), p.get("confidence")
        if type(answer) is not int or type(confidence) not in (float, int) or not 0 <= confidence <= 1:
            raise ValueError("Each prediction needs an integer answer and confidence in [0,1]")
        predictions[p["id"]] = {"answer": answer, "confidence": float(confidence)}
    if set(predictions) != set(questions):
        raise ValueError("A prediction is required for EVERY test question")

    records = []
    for qid, gt in priv["test_answers"].items():
        p = predictions[qid]
        records.append({"id": qid, "correct": int(p["answer"] == gt["answer"]),
                        "confidence": p["confidence"], "student_is_wrong": gt["student_is_wrong"],
                        "domain": gt["domain"]})

    wrong = [r for r in records if r["student_is_wrong"]]
    right = [r for r in records if not r["student_is_wrong"]]
    high = [r for r in wrong if r["confidence"] >= 0.8]
    low = [r for r in wrong if r["confidence"] < 0.8]

    # Brier score on held-out student-error problems: lower is better.
    brier = _mean([(r["confidence"] - r["correct"]) ** 2 for r in wrong])
    # ECE on the same problems, five fixed confidence bins.
    ece = 0.0
    for i in range(5):
        bucket = [r for r in wrong if (i / 5 <= r["confidence"] < (i+1) / 5) or
                  (i == 4 and r["confidence"] == 1)]
        if bucket:
            ece += len(bucket) / len(wrong) * abs(
                sum(r["confidence"] for r in bucket) / len(bucket) -
                sum(r["correct"] for r in bucket) / len(bucket))

    result = {
        "case": state["case"], "session": session, "probe_budget": state["budget"],
        "probes_used": len(state["probes"]),
        "primary_wrong_answer_accuracy": _mean([r["correct"] for r in wrong]),
        "wrong_answer_test_n": len(wrong),
        "overall_accuracy_diagnostic": _mean([r["correct"] for r in records]),
        "correct_answer_accuracy_diagnostic": _mean([r["correct"] for r in right]),
        "wrong_answer_accuracy_by_domain": {d: _mean([r["correct"] for r in wrong if r["domain"] == d])
                                           for d in ("familiar", "transfer")},
        "calibration_on_wrong_questions": {
            "brier_lower_is_better": brier,
            "ece_5bins_lower_is_better": round(ece, 4),
            "high_confidence_coverage": round(len(high) / len(wrong), 4),
            "accuracy_when_high_confidence": _mean([r["correct"] for r in high]),
            "accuracy_when_low_confidence": _mean([r["correct"] for r in low]),
            "high_confidence_error_rate": _mean([1-r["correct"] for r in high]),
        }
    }
    write_json(root / "private" / "reports" / f"{safe_id(session)}.json", result)
    state["graded"] = True
    write_json(state_file, state)
    return result


def baseline(root: Path, case: str, dest: Path) -> None:
    pub = read_json(root / "public" / f"{safe_id(case)}.json")
    # Deliberately weak baseline: assume student always computes correctly.
    submission = {"predictions": [
        {"id": q["id"], "answer": q["a"] - q["b"], "confidence": 0.95}
        for q in pub["test_questions"]]}
    write_json(dest, submission)
    print(f"Wrote intentionally weak correct-arithmetic baseline to {dest}")



def summarize(root: Path, output: Path) -> list[dict[str, Any]]:
    """Aggregate completed run reports into data for the 0/3/10 probe curve."""
    buckets: dict[int, list[dict[str, Any]]] = {b: [] for b in BUDGETS}
    for path in sorted((root / "private" / "reports").glob("*.json")):
        report = read_json(path)
        if report["probe_budget"] in buckets:
            buckets[report["probe_budget"]].append(report)
    rows = []
    for budget, reports in buckets.items():
        if not reports:
            continue
        rows.append({
            "probe_budget": budget,
            "runs": len(reports),
            "unique_cases": len({r["case"] for r in reports}),
            "mean_probes_used": _mean([r["probes_used"] for r in reports]),
            "mean_wrong_answer_accuracy": _mean([r["primary_wrong_answer_accuracy"] for r in reports]),
            "mean_brier": _mean([r["calibration_on_wrong_questions"]["brier_lower_is_better"]
                                 for r in reports]),
        })
    if rows:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps(rows, indent=2))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("generate", help="Create public + hidden benchmark datasets")
    p.add_argument("--root", default="cases")
    p.add_argument("--seed", type=int, default=20261114)
    p.add_argument("--n", type=int, default=20)
    p = sub.add_parser("start", help="Start a 0/3/10-probe evaluation session")
    p.add_argument("--root", default="cases")
    p.add_argument("--case", required=True)
    p.add_argument("--budget", type=int, choices=BUDGETS, required=True)
    p.add_argument("--session", required=True)
    p = sub.add_parser("probe", help="Trusted evaluator: answer one agent-selected problem")
    p.add_argument("--root", default="cases")
    p.add_argument("--session", required=True)
    p.add_argument("--a", type=int, required=True)
    p.add_argument("--b", type=int, required=True)
    p = sub.add_parser("grade", help="Evaluate all held-out predictions")
    p.add_argument("--root", default="cases")
    p.add_argument("--session", required=True)
    p.add_argument("--submission", type=Path, required=True)
    p = sub.add_parser("baseline", help="Create a deliberately weak baseline submission")
    p.add_argument("--root", default="cases")
    p.add_argument("--case", required=True)
    p.add_argument("--out", type=Path, default=Path("baseline_submission.json"))
    p = sub.add_parser("summarize", help="Export 0/3/10 accuracy-curve data to CSV")
    p.add_argument("--root", default="cases")
    p.add_argument("--out", type=Path, default=Path("probe_curve.csv"))
    args = parser.parse_args()
    root = Path(getattr(args, "root", "cases"))
    if args.command == "generate":
        generate(root, args.seed, args.n)
    elif args.command == "start":
        start_session(root, args.case, args.budget, args.session)
    elif args.command == "probe":
        probe(root, args.session, args.a, args.b)
    elif args.command == "grade":
        print(json.dumps(grade(root, args.session, args.submission), indent=2))
    elif args.command == "baseline":
        baseline(root, args.case, args.out)
    elif args.command == "summarize":
        summarize(root, args.out)


if __name__ == "__main__":
    main()
