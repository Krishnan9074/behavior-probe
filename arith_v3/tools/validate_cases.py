#!/usr/bin/env python3
"""Trusted-side checks for the bundled tasks; no third-party dependencies."""
import argparse
import json
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from arithmetic_eval.generate import read_json
from arithmetic_eval.grade import math_baseline, oracle_prediction, score
from arithmetic_eval.student import OPS, RULES, SELECTED_LABELS, answer, correct


def validate(root):
    manifest = read_json(root / "manifest.json")
    label_counts, levels = Counter(), Counter()
    seen = set()
    for entry in manifest["cases"]:
        cid = entry["task_id"]
        assert cid not in seen, f"duplicate case ID: {cid}"
        seen.add(cid)
        pub, pri = read_json(root / "public" / f"{cid}.json"), read_json(root / "private" / f"{cid}.json")
        assert pub["task_id"] == pri["task_id"] == cid
        assert "rules" not in pub and "test_answers" not in pub
        level = entry["level"]
        levels[level] += 1
        n = 40 if level == 1 else 80
        assert len(pub["test_questions"]) == n
        assert len(pri["test_answers"]) == n
        assert sum(v["is_error"] for v in pri["test_answers"].values()) == n // 2
        assert len({q["id"] for q in pub["test_questions"]}) == n
        observed = {(p["op"], p["a"], p["b"]) for p in pub["observations"]}
        hidden = {(p["op"], p["a"], p["b"]) for p in pub["test_questions"]}
        assert len(hidden) == n and not observed.intersection(hidden)
        for op, rules in pri["rules"].items():
            for rule in rules: label_counts[RULES[op][rule["name"]][0]] += 1
        if level >= 2:
            for op in OPS:
                rows = [q for q in pub["test_questions"] if q["op"] == op]
                assert len(rows) == 20
                assert sum(pri["test_answers"][q["id"]]["is_error"] for q in rows) == 10
        if level == 3:
            assert entry["target_operation"] not in {h["op"] for h in pub["observations"]}
            assert all(pri["rules"][op] == pri["rules"]["add"] for op in OPS)
        for q in pub["test_questions"]:
            rules = pri["rules"][q["op"]]
            expected = pri["test_answers"][q["id"]]
            assert answer(q["op"], q["a"], q["b"], rules) == expected["answer"]
            assert (expected["answer"] != correct(q["op"], q["a"], q["b"])) == expected["is_error"]
        naive = score(pub, pri, math_baseline(pub))
        assert naive["primary_accuracy"] == 0.0 and naive["overall_accuracy"] == .5
        pred, candidates = oracle_prediction(pub, pri, [])
        assert score(pub, pri, pred)["valid"]
        assert all(v >= 1 for v in candidates.values())
    if len(manifest["cases"]) >= 20:
        assert set(SELECTED_LABELS) <= set(label_counts), set(SELECTED_LABELS) - set(label_counts)
    print(json.dumps({"validated": True, "n_cases": len(seen), "level_counts": dict(levels),
                      "n_selected_labels": len(SELECTED_LABELS),
                      "labels_represented": sorted(label_counts)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="cases")
    args = parser.parse_args()
    validate(Path(args.root))
