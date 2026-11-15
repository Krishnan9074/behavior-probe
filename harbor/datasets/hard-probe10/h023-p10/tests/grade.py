"""Harbor verifier for one BEHAVIOR-PROBE task. Copied into /tests only after the agent finishes.

reward = accuracy on the questions where the student errs (the benchmark's primary metric).
Also writes overall accuracy, 3-digit vs 4-5-digit error accuracy, Brier score and probes used.
"""
import json
import urllib.request
from pathlib import Path

OUT = Path("/logs/verifier")
OUT.mkdir(parents=True, exist_ok=True)
answers = json.loads(Path("/tests/answers.json").read_text())


def probes_used():
    try:
        log = json.loads(urllib.request.urlopen("http://oracle:8000/log", timeout=10).read())
        return log["probes"]
    except Exception:
        return []  # no-probe tasks have no oracle


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


probes = probes_used()
result = {"reward": 0.0, "valid": 0, "probes_used": len(probes)}
try:
    raw = json.loads(Path("/workspace/submission.json").read_text())
    preds = {}
    for p in raw["predictions"]:
        if p["id"] in preds or p["id"] not in answers:
            raise ValueError(f"unknown or duplicate id {p['id']}")
        if type(p["answer"]) is not int or not (0 <= float(p["confidence"]) <= 1):
            raise ValueError(f"bad answer/confidence for {p['id']}")
        preds[p["id"]] = (p["answer"], float(p["confidence"]))
    if set(preds) != set(answers):
        raise ValueError(f"{len(answers) - len(preds)} predictions missing")
    rows = [{"ok": int(preds[q][0] == a["answer"]), "conf": preds[q][1], **a} for q, a in answers.items()]
    wrong = [r for r in rows if r["student_is_wrong"]]
    result.update({
        "reward": mean([r["ok"] for r in wrong]),
        "valid": 1,
        "overall_accuracy": mean([r["ok"] for r in rows]),
        "correct_answer_accuracy": mean([r["ok"] for r in rows if not r["student_is_wrong"]]),
        "familiar_error_accuracy": mean([r["ok"] for r in wrong if r["domain"] == "familiar"]),
        "transfer_error_accuracy": mean([r["ok"] for r in wrong if r["domain"] == "transfer"]),
        "brier": mean([(r["conf"] - r["ok"]) ** 2 for r in wrong]),
    })
    detail = {"probes": probes, "per_question": [{"id": q, "student": a["answer"], "predicted": preds[q][0],
                                                   "confidence": preds[q][1], "student_is_wrong": a["student_is_wrong"]}
                                                  for q, a in answers.items()]}
except Exception as e:  # missing or malformed submission scores 0
    detail = {"probes": probes, "error": f"{type(e).__name__}: {e}"}

(OUT / "reward.json").write_text(json.dumps(result))
(OUT / "detail.json").write_text(json.dumps(detail))
print(json.dumps(result))
