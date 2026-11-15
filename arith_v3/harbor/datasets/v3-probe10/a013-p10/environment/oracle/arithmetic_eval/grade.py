"""Deterministic exact-match, per-operation, calibration and oracle scoring."""
from __future__ import annotations

from collections import Counter, defaultdict

from .student import OPS, answer, correct, rule_configurations, shared_rule_configurations


def parse_predictions(submission: object, questions: list[dict]) -> tuple[dict, str | None]:
    if not isinstance(submission, dict) or not isinstance(submission.get("predictions"), list):
        return {}, "Submission must have a predictions array"
    entries = submission["predictions"]
    ids = {q["id"] for q in questions}
    if len(entries) != len(ids):
        return {}, f"Expected {len(ids)} predictions; got {len(entries)}"
    parsed = {}
    for entry in entries:
        if not isinstance(entry, dict): return {}, "Each prediction must be an object"
        ident, ans, confidence = entry.get("id"), entry.get("answer"), entry.get("confidence")
        if ident not in ids or ident in parsed: return {}, "Unknown or duplicate question ID"
        if type(ans) is not int: return {}, f"Integer answer required for {ident}"
        if type(confidence) not in (float, int) or not 0 <= confidence <= 1:
            return {}, f"Confidence must be between 0 and 1 for {ident}"
        parsed[ident] = {"answer": ans, "confidence": float(confidence)}
    if set(parsed) != ids: return {}, "Missing test questions"
    return parsed, None


def calibration(outcomes: list[tuple[int, float]]) -> dict | None:
    if not outcomes: return None
    n = len(outcomes)
    brier = sum((c - y) ** 2 for y, c in outcomes) / n
    buckets = [[] for _ in range(5)]
    for y, conf in outcomes:
        buckets[min(4, int(5 * conf))].append((y, conf))
    ece = sum(len(bucket) / n * abs(sum(c for _, c in bucket) / len(bucket)
                                         - sum(y for y, _ in bucket) / len(bucket))
              for bucket in buckets if bucket)
    high = [(y, c) for y, c in outcomes if c >= .9]
    return {"brier": round(brier, 6), "ece_5_bins": round(ece, 6),
            "high_confidence_threshold": 0.9,
            "high_confidence_error_rate": round(sum(not y for y, _ in high) / len(high), 6) if high else None,
            "high_confidence_coverage": round(len(high) / n, 6),
            "n": n}


def score(public: dict, private: dict, submission: object,
          probe_log: list[dict] | None = None) -> dict:
    parsed, parse_error = parse_predictions(submission, public["test_questions"])
    if parse_error:
        return {"valid": False, "error": parse_error, "primary_accuracy": 0.0,
                "overall_accuracy": 0.0, "macro_error_accuracy": 0.0,
                "error_correct": 0, "all_correct": 0,
                "n_error": sum(x["is_error"] for x in private["test_answers"].values()),
                "n_all": len(public["test_questions"]), "per_operation": {},
                "calibration_error_cases": None, "calibration_all": None,
                "transfer_error_accuracy": None, "transfer_contaminated": None}
    all_pairs, error_pairs = [], []
    per_op = defaultdict(lambda: {"n_all": 0, "n_error": 0, "all_correct": 0, "error_correct": 0})
    for q in public["test_questions"]:
        expected = private["test_answers"][q["id"]]
        p = parsed[q["id"]]
        ok = int(p["answer"] == expected["answer"])
        all_pairs.append((ok, p["confidence"]))
        row = per_op[q["op"]]
        row["n_all"] += 1
        row["all_correct"] += ok
        if expected["is_error"]:
            row["n_error"] += 1
            row["error_correct"] += ok
            error_pairs.append((ok, p["confidence"]))
    for row in per_op.values():
        row["accuracy_all"] = round(row["all_correct"] / row["n_all"], 6)
        row["accuracy_error"] = round(row["error_correct"] / row["n_error"], 6) if row["n_error"] else None
    eligible = [row["accuracy_error"] for row in per_op.values() if row["accuracy_error"] is not None]
    nerror = len(error_pairs)
    target = private.get("target_operation")
    direct = bool(target and any(p["op"] == target for p in (probe_log or [])))
    return {"valid": True, "error": None,
            "primary_accuracy": round(sum(y for y, _ in error_pairs) / nerror, 6) if nerror else 0.0,
            "overall_accuracy": round(sum(y for y, _ in all_pairs) / len(all_pairs), 6),
            "macro_error_accuracy": round(sum(eligible) / len(eligible), 6) if eligible else None,
            "n_error": nerror, "n_all": len(all_pairs),
            "error_correct": sum(y for y, _ in error_pairs),
            "all_correct": sum(y for y, _ in all_pairs),
            "per_operation": dict(sorted(per_op.items())),
            "calibration_error_cases": calibration(error_pairs),
            "calibration_all": calibration(all_pairs),
            "transfer_target_operation": target,
            "transfer_contaminated": direct if target else None,
            "transfer_error_accuracy": (per_op[target]["accuracy_error"]
                                        if target and not direct else None),
            "transfer_note": ("Target-operation direct probe already used; transfer-only score suppressed"
                              if direct else None)}


def oracle_prediction(public: dict, private: dict, probe_log: list[dict]):
    """Uniform compatible-model majority vote under the DECLARED hypothesis family.

    This is a finite-candidate baseline, not a provable upper bound or an
    absolute minimum-probes oracle. Ties use smallest numeric output.
    """
    level = private["level"]
    observations = [{"op": x["op"], "a": x["a"], "b": x["b"], "y": x["student_answer"]}
                    for x in public["observations"] + probe_log]
    compatible = {}
    if level == 3:
        cs = [[shared] for shared in shared_rule_configurations()]
        matched = [cfg for cfg in cs if all(answer(x["op"], x["a"], x["b"], cfg) == x["y"]
                                            for x in observations)]
        if not matched: raise AssertionError("Shared candidate family does not explain evidence")
        compatible = {op: matched for op in OPS}
    else:
        focus = public["focus"] if level == 1 else None
        cfg_count = 2 if public["difficulty"].startswith("L1_hard") else 1
        for op in OPS:
            if focus and op != focus:
                compatible[op] = [[]]
                continue
            observations_op = [x for x in observations if x["op"] == op]
            matched = [cfg for cfg in rule_configurations(op, cfg_count)
                       if all(answer(op, x["a"], x["b"], cfg) == x["y"] for x in observations_op)]
            if not matched: raise AssertionError(f"No matching hypotheses for {op}")
            compatible[op] = matched
    predictions = []
    for q in public["test_questions"]:
        candidates = compatible[q["op"]]
        frequency = Counter(answer(q["op"], q["a"], q["b"], cfg) for cfg in candidates)
        maximum = max(frequency.values())
        chosen = min(y for y, n in frequency.items() if n == maximum)
        predictions.append({"id": q["id"], "answer": chosen,
                            "confidence": round(maximum / len(candidates), 8)})
    return {"predictions": predictions}, {op: len(c) for op, c in compatible.items()}


def math_baseline(public: dict) -> dict:
    return {"predictions": [{"id": q["id"], "answer": correct(q["op"], q["a"], q["b"]),
                             "confidence": 1.0} for q in public["test_questions"]]}
