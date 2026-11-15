"""End-to-end local benchmark invariants (stdlib unittest)."""
import json
import random
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from arithmetic_eval.generate import generate, read_json, sample_problem, write_json
from arithmetic_eval.grade import math_baseline, oracle_prediction, score, parse_predictions
from arithmetic_eval.server import process
from arithmetic_eval.student import (OPS, RULES, SELECTED_LABELS, SHARED_RULES,
                                     answer, correct, rule_configurations, shared_rule_configurations)

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "benchmark.py"


class SimulatorTests(unittest.TestCase):
    def test_documented_selected_labels(self):
        expected = {"W01", "W02", "W04", "W06", "W08", "W09", "W10", "W11",
                    "W12", "W13", "W15", "W16", "EXTRA_SFL"}
        self.assertEqual(set(SELECTED_LABELS), expected)
        self.assertEqual({meta[0] for group in RULES.values() for meta in group.values()}, expected)

    def test_unmodified_math(self):
        for op, a, b in [("add", 765, 897), ("sub", 1001, 387),
                         ("mul", 157, 38), ("div", 8092, 4)]:
            self.assertEqual(answer(op, a, b, []), correct(op, a, b))

    def test_every_rule_changes_at_least_one_sample(self):
        for op in OPS:
            for rule in RULES[op]:
                rng = random.Random(25)
                cfg = [{"name": rule, "trigger": "any"}]
                changed = False
                for _ in range(600):
                    a, b = sample_problem(op, rng, True)
                    val1 = answer(op, a, b, cfg)
                    self.assertEqual(val1, answer(op, a, b, cfg))
                    if val1 != correct(op, a, b): changed = True; break
                self.assertTrue(changed, f"Rule never changes output: {op}/{rule}")

    def test_exact_research_example_and_triggers(self):
        # W02, column totals concatenated: 58+83 => 13|11 => 1311.
        self.assertEqual(answer("add", 58, 83, [{"name": "add_no_regroup", "trigger": "any"}]), 1311)
        # Inadmissible triggers are rejected, not included as inert hypothesis atoms.
        with self.assertRaises(ValueError):
            answer("add", 58, 83, [{"name": "add_no_regroup", "trigger": "ones_only"}])
        self.assertGreater(len(rule_configurations("sub", 2)), len(rule_configurations("sub", 1)))

    def test_shared_rule_executes_identically_across_operations(self):
        self.assertEqual(set(SHARED_RULES), {"zero_as_one", "one_as_zero"})
        cfg = shared_rule_configurations()[0]
        for op, a, b in [("add", 106, 72), ("sub", 506, 101),
                         ("mul", 305, 24), ("div", 1008, 7)]:
            if op == "div":
                a = 1008  # 1008 / 7 is exact.
            self.assertEqual(answer(op, a, b, [cfg]), answer(op, a, b, [cfg]))


class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "cases"
        cls.manifest = generate(cls.root, seed=20261115, easy_per_op=2, l2_count=2, l3_per_op=1)

    @classmethod
    def tearDownClass(cls): cls.tmp.cleanup()

    def cases(self):
        for e in self.manifest["cases"]:
            yield e, read_json(self.root / "public" / f"{e['task_id']}.json"), read_json(self.root / "private" / f"{e['task_id']}.json")

    def test_generated_case_structure_and_balance(self):
        self.assertEqual(set(self.manifest["labels_represented_in_tasks"]), set(SELECTED_LABELS))
        level_counts = {k: 0 for k in (1, 2, 3)}
        for e, pub, pri in self.cases():
            level_counts[e["level"]] += 1
            n = 40 if e["level"] == 1 else 80
            self.assertEqual(len(pub["test_questions"]), n)
            self.assertEqual(len(pri["test_answers"]), n)
            self.assertEqual(sum(x["is_error"] for x in pri["test_answers"].values()), n // 2)
            self.assertNotIn("test_answers", pub)
            self.assertNotIn("rules", pub)
            self.assertEqual(len({q["id"] for q in pub["test_questions"]}), n)
            history = {(x["op"], x["a"], x["b"]) for x in pub["observations"]}
            test = {(x["op"], x["a"], x["b"]) for x in pub["test_questions"]}
            self.assertFalse(history & test)
            if e["level"] > 1:
                for op in OPS:
                    self.assertEqual(sum(q["op"] == op for q in pub["test_questions"]), 20)
                    self.assertEqual(sum(q["op"] == op and pri["test_answers"][q["id"]]["is_error"]
                                         for q in pub["test_questions"]), 10)
            if e["level"] == 3:
                target = e["target_operation"]
                self.assertNotIn(target, {x["op"] for x in pub["observations"]})
                self.assertEqual(len(pub["observations"]), 4)
                self.assertEqual({r["name"] for rs in pri["rules"].values() for r in rs},
                                 {pri["rules"]["add"][0]["name"]})
                self.assertTrue(all(pri["rules"][op] == pri["rules"]["add"] for op in OPS))
        self.assertEqual(level_counts, {1: 12, 2: 2, 3: 4})

    def test_math_baseline_zero_and_perfect_score(self):
        for _, pub, pri in self.cases():
            baseline = score(pub, pri, math_baseline(pub))
            self.assertTrue(baseline["valid"])
            self.assertEqual(baseline["primary_accuracy"], 0.0)
            self.assertEqual(baseline["overall_accuracy"], .5)
            self.assertEqual(baseline["macro_error_accuracy"], 0.0)
            perfect = {"predictions": [{"id": q["id"], "answer": pri["test_answers"][q["id"]]["answer"],
                                        "confidence": 1.0} for q in pub["test_questions"]]}
            s = score(pub, pri, perfect)
            self.assertEqual(s["primary_accuracy"], 1.0)
            self.assertEqual(s["overall_accuracy"], 1.0)
            self.assertEqual(s["macro_error_accuracy"], 1.0)
            self.assertEqual(s["calibration_error_cases"]["brier"], 0.0)
            self.assertEqual(s["calibration_all"]["brier"], 0.0)
            if pri["level"] == 3:
                self.assertEqual(s["transfer_error_accuracy"], 1.0)
                self.assertEqual(s["transfer_contaminated"], False)
                self.assertIsNone(score(pub, pri, perfect, [{"op": pri["target_operation"]}])
                                  ["transfer_error_accuracy"])

    def test_invalid_omission_and_confidence_scores_zero(self):
        _, pub, pri = next(self.cases())
        pred = math_baseline(pub)
        pred["predictions"].pop()
        self.assertFalse(score(pub, pri, pred)["valid"])
        self.assertEqual(score(pub, pri, pred)["primary_accuracy"], 0.0)
        pred = math_baseline(pub)
        pred["predictions"][0]["confidence"] = 1.5
        self.assertFalse(score(pub, pri, pred)["valid"])
        pred = math_baseline(pub)
        pred["predictions"][0]["answer"] = True
        self.assertFalse(score(pub, pri, pred)["valid"])

    def test_oracle_family_reproduces_evidence(self):
        for _, pub, pri in self.cases():
            pred, survivors = oracle_prediction(pub, pri, [])
            self.assertTrue(score(pub, pri, pred)["valid"])
            self.assertTrue(all(n > 0 for n in survivors.values()))

    def test_local_server_probe_auth_boundary(self):
        e, pub, pri = next(self.cases())
        name = "unit-api"
        write_json(self.root / "private" / "sessions" / f"{name}.json",
                   {"case": e["task_id"], "budget": 1, "probes": [], "submissions": [],
                    "closed": False, "api_token": "unit_secret"})
        with self.assertRaises(PermissionError):
            process(self.root, name, "bad", "task")
        result = process(self.root, name, "unit_secret", "task")
        self.assertIn("observations", result["task"])
        self.assertNotIn("rules", result["task"])
        q = pub["test_questions"][0]
        with self.assertRaises(ValueError):
            process(self.root, name, "unit_secret", "probe", {"op": q["op"], "a": q["a"], "b": q["b"]})
        x = process(self.root, name, "unit_secret", "probe", {"op": "add", "a": 768, "b": 291})
        self.assertEqual(x["remaining"], 0)
        with self.assertRaises(ValueError):
            process(self.root, name, "unit_secret", "probe", {"op": "add", "a": 128, "b": 7})
        msg = process(self.root, name, "unit_secret", "snapshot", math_baseline(pub))
        self.assertFalse(msg["hidden_score_revealed"])

    def test_cli_snapshots_k100_and_export(self):
        e, pub, pri = next(self.cases())
        baseline_path = Path(self.tmp.name) / "pred.json"
        perfect_path = Path(self.tmp.name) / "perfect.json"
        write_json(baseline_path, math_baseline(pub))
        write_json(perfect_path, {"predictions": [{"id": q["id"],
              "answer": pri["test_answers"][q["id"]]["answer"], "confidence": 1.0}
              for q in pub["test_questions"]]})

        def call(*args, ok=True):
            p = subprocess.run([sys.executable, str(SCRIPT), *args, "--root", str(self.root)],
                               cwd=PROJECT, capture_output=True, text=True)
            self.assertEqual(p.returncode == 0, ok, p.stderr)
            return p

        call("start", "--case", e["task_id"], "--budget", "1", "--session", "unit-cli")
        call("submit", "--session", "unit-cli", "--submission", str(baseline_path))
        test = pub["test_questions"][0]
        call("probe", "--session", "unit-cli", "--op", test["op"],
             "--a", str(test["a"]), "--b", str(test["b"]), ok=False)
        call("probe", "--session", "unit-cli", "--op", "add", "--a", "826", "--b", "34")
        call("submit", "--session", "unit-cli", "--submission", str(perfect_path))
        report = json.loads(call("grade", "--session", "unit-cli").stdout)
        self.assertEqual([s["after_probes"] for s in report["snapshots"]], [0, 1])
        self.assertEqual(report["k100_error_observed"], 1)
        self.assertEqual(report["k100_all_observed"], 1)
        outzip = Path(self.tmp.name) / "public.zip"
        call("export", "--case", e["task_id"], "--out", str(outzip))
        with zipfile.ZipFile(outzip) as z:
            self.assertEqual(set(z.namelist()), {"task.json", "agent_prompt.txt"})
            self.assertNotIn("rules", z.read("task.json").decode())


if __name__ == "__main__":
    unittest.main()
