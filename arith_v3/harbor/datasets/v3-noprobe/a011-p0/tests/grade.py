"""Harbor verifier for one ARITH-PROBE v3 task. Copied into /tests only after the agent finishes.

Scores with the unmodified v3 grader (arithmetic_eval/grade.py):
reward = exact-match accuracy on the held-out questions the student gets wrong.
The final /workspace/submission.json is graded; snapshots saved with `snapshot` give the
probe curve and observed K100 / K95, exactly as `benchmark.py grade` computes them.
"""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, "/tests")
from arithmetic_eval.grade import score  # noqa: E402

OUT = Path("/logs/verifier")
OUT.mkdir(parents=True, exist_ok=True)
public = json.loads(Path("/tests/public.json").read_text())
private = json.loads(Path("/tests/private.json").read_text())

try:
    log = json.loads(urllib.request.urlopen("http://oracle:8000/log", timeout=10).read())
except Exception:
    log = {"probes": [], "snapshots": []}  # no-probe tasks have no oracle
probes = log["probes"]

try:
    final = json.loads(Path("/workspace/submission.json").read_text())
except Exception as e:
    final = {"error": f"{type(e).__name__}: {e}"}  # scores 0 as malformed

snaps = log["snapshots"] + [{"after_probes": len(probes), "submission": final}]
timeline = [{"snapshot": i + 1, "after_probes": s["after_probes"],
             **score(public, private, s["submission"], probes[:s["after_probes"]])}
            for i, s in enumerate(snaps)]
last = timeline[-1]


def first(pred):
    return min((r["after_probes"] for r in timeline if r["valid"] and pred(r)), default=None)


cal = last["calibration_error_cases"] or {}
result = {
    "reward": last["primary_accuracy"],
    "valid": int(last["valid"]),
    "overall_accuracy": last["overall_accuracy"],
    "macro_error_accuracy": last["macro_error_accuracy"],
    "transfer_error_accuracy": last["transfer_error_accuracy"],
    "transfer_contaminated": last["transfer_contaminated"],
    "brier_error_cases": cal.get("brier"),
    "ece_error_cases": cal.get("ece_5_bins"),
    "probes_used": len(probes),
    "snapshots": len(snaps),
    "k100_error_observed": first(lambda r: r["primary_accuracy"] == 1.0),
    "k100_all_observed": first(lambda r: r["overall_accuracy"] == 1.0),
    "k95_error_observed": first(lambda r: r["primary_accuracy"] >= .95),
    **{f"{op}_error_accuracy": row["accuracy_error"] for op, row in last["per_operation"].items()},
}
detail = {"case": private["task_id"], "level": private["level"], "difficulty": private["family"],
          "probes": probes, "timeline": timeline,
          "per_question": [{**q, "student": private["test_answers"][q["id"]]["answer"],
                            "student_is_wrong": private["test_answers"][q["id"]]["is_error"],
                            "predicted": next((p.get("answer") for p in final.get("predictions", [])
                                               if isinstance(p, dict) and p.get("id") == q["id"]), None)
                            if isinstance(final, dict) and isinstance(final.get("predictions"), list) else None}
                           for q in public["test_questions"]]}

# reward.json holds numbers only (as in the earlier benchmark); null metrics are left out
result = {k: int(v) if isinstance(v, bool) else v for k, v in result.items() if v is not None}
(OUT / "reward.json").write_text(json.dumps(result))
(OUT / "detail.json").write_text(json.dumps(detail))
print(json.dumps(result))
