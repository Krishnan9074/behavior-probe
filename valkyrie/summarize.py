"""Download each run's results (runs.tsv) and print a model x dataset table."""
import json
import os
import subprocess
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "results"
OUT.mkdir(exist_ok=True)
env = {**os.environ, "VALKYRIE_URL": "http://127.0.0.1:8000"}


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


import sys
only = sys.argv[1] if len(sys.argv) > 1 else ""  # e.g. "anthropic" to summarize a subset

rows = []
for line in (HERE / "runs.tsv").read_text().split("\n"):
    if not line.strip() or only not in line:
        continue
    model, ds, rid = line.split("\t")
    f = OUT / f"results-{rid}.json"
    if not f.exists():
        subprocess.run(["valkyrie", "run", "results", rid], cwd=OUT, env=env, check=True, capture_output=True)
    d = json.loads(f.read_text())
    res = d.get("evaluation_results") or {}
    ok = [r for r in res.values() if r and "error" not in r]
    probes = [r.get("probes_used") for r in res.values() if r]
    rows.append({
        "model": model.split("/")[-1], "dataset": ds,
        "score": (d.get("final_evaluation") or {}).get("final_score"),
        "graded": f"{len(ok)}/{len(res)}",
        "familiar": mean([r["wrong_answer_accuracy_by_domain"]["familiar"] for r in ok]),
        "transfer": mean([r["wrong_answer_accuracy_by_domain"]["transfer"] for r in ok]),
        "overall": mean([r["overall_accuracy_diagnostic"] for r in ok]),
        "brier": mean([r["calibration_on_wrong_questions"]["brier_lower_is_better"] for r in ok]),
        "probes_mean": mean(probes),
        "probes_total": sum(p or 0 for p in probes),
        "cases_probed": sum(1 for p in probes if p),
        "agent_s": (d.get("average_task_breakdown") or {}).get("agent_run_duration"),
    })

fmt = lambda v: "-" if v is None else (f"{v:.3f}" if isinstance(v, float) else str(v))
cols = list(rows[0])
print("\t".join(cols))
for r in sorted(rows, key=lambda r: (r["dataset"], -(r["score"] or 0))):
    print("\t".join(fmt(r[c]) for c in cols))
(OUT / "summary.json").write_text(json.dumps(rows, indent=2))
