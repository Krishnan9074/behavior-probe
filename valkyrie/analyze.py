"""Final statistics: merge runs per (model, dataset), bootstrap 95% CIs over cases,
probe efficiency, and paired model comparisons. Writes results/final.json.

    python3 analyze.py
"""
import json
import os
import random
import subprocess
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
RES = HERE / "results"
RES.mkdir(exist_ok=True)
env = {**os.environ, "VALKYRIE_URL": "http://127.0.0.1:8000"}
B = 10_000


def results(rid):
    f = RES / f"results-{rid}.json"
    if not f.exists():
        subprocess.run(["valkyrie", "run", "results", rid], cwd=RES, env=env, check=True, capture_output=True)
    return json.loads(f.read_text())


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def boot_ci(xs, rng):
    n = len(xs)
    if not n:
        return None, None
    ms = sorted(sum(xs[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return ms[int(0.025 * B)], ms[int(0.975 * B)]


# (model, dataset) -> case -> report (later runs overwrite earlier ones for the same case)
cells = defaultdict(dict)
agents = {}
for line in (HERE / "runs.tsv").read_text().splitlines():
    if not line.strip():
        continue
    model, ds, rid = line.split("\t")
    model = model.split("/")[-1]
    d = results(rid)
    agents[model] = d["benchmark_arguments"]["contract"]["name"]
    for case, rep in (d.get("evaluation_results") or {}).items():
        if rep is not None:
            cells[(model, ds)][case] = rep

rng = random.Random(0)
out = {"cells": [], "pairs": [], "agents": agents, "bootstrap_resamples": B}
for (model, ds), reps in sorted(cells.items()):
    cases = sorted(reps)
    err = [reps[c].get("primary_wrong_answer_accuracy") or 0.0 for c in cases]  # invalid submission = 0
    ok = [reps[c] for c in cases if "error" not in reps[c]]
    lo, hi = boot_ci(err, rng)
    cell = {
        "model": model, "dataset": ds, "n": len(cases), "valid": len(ok),
        "err_acc": mean(err), "ci95": [lo, hi],
        "overall": mean([r["overall_accuracy_diagnostic"] for r in ok]),
        "familiar": mean([r["wrong_answer_accuracy_by_domain"]["familiar"] for r in ok]),
        "transfer": mean([r["wrong_answer_accuracy_by_domain"]["transfer"] for r in ok]),
        "brier": mean([r["calibration_on_wrong_questions"]["brier_lower_is_better"] for r in ok]),
        "ece": mean([r["calibration_on_wrong_questions"]["ece_5bins_lower_is_better"] for r in ok]),
        "probes_mean": mean([reps[c].get("probes_used", 0) for c in cases]),
        "cases_probed": sum(1 for c in cases if reps[c].get("probes_used", 0) > 0),
        "perfect": sum(1 for x in err if x == 1.0),
    }
    base = cells.get((model, ds.replace("probe10", "noprobe").replace("probe3", "noprobe")))
    if base is not cells.get((model, ds)) and base:
        shared = [c for c in cases if c in base]
        gain = mean([(reps[c].get("primary_wrong_answer_accuracy") or 0) - (base[c].get("primary_wrong_answer_accuracy") or 0) for c in shared])
        probes = mean([reps[c].get("probes_used", 0) for c in shared])
        cell["gain_vs_noprobe"] = gain
        cell["gain_per_probe"] = gain / probes if probes else None
    out["cells"].append(cell)

# Paired bootstrap of model differences on the same dataset and the same cases.
models = sorted({m for m, _ in cells})
for ds in sorted({d for _, d in cells}):
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            ra, rb = cells.get((a, ds), {}), cells.get((b, ds), {})
            shared = sorted(set(ra) & set(rb))
            if len(shared) < 5:
                continue
            diffs = [(ra[c].get("primary_wrong_answer_accuracy") or 0) - (rb[c].get("primary_wrong_answer_accuracy") or 0) for c in shared]
            lo, hi = boot_ci(diffs, rng)
            out["pairs"].append({"dataset": ds, "a": a, "b": b, "n": len(shared), "diff": mean(diffs),
                                 "ci95": [lo, hi], "significant": lo > 0 or hi < 0})

(RES / "final.json").write_text(json.dumps(out, indent=1))
fmt = lambda v: "-" if v is None else f"{100 * v:5.1f}"
print(f"{'model':18} {'dataset':13} {'n':>3} {'err%':>6} {'95% CI':>13} {'probes':>6} {'gain/pr':>7} {'brier':>6}")
for c in sorted(out["cells"], key=lambda c: (c["dataset"], -(c["err_acc"] or 0))):
    gpp = c.get("gain_per_probe")
    print(f"{c['model']:18} {c['dataset']:13} {c['n']:>3} {fmt(c['err_acc']):>6} [{fmt(c['ci95'][0])},{fmt(c['ci95'][1])}] "
          f"{c['probes_mean']:6.2f} {('-' if gpp is None else f'{100*gpp:5.1f}'):>7} {c['brier'] or 0:6.3f}")
sig = [p for p in out["pairs"] if p["significant"]]
print(f"\n{len(sig)}/{len(out['pairs'])} model pairs differ significantly (paired bootstrap, 95%).")
