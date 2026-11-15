"""Results for the hosted ARITH-PROBE v3 runs (arith_v3/harbor/runs_hosted.tsv).

    python3 arith_v3/harbor/analyze_hosted.py

Same method as harbor/analyze_hosted.py (case-level bootstrap CIs, paired model comparisons),
plus v3's breakdowns: per level, per operation, Level-3 transfer, K100. Writes:
  arith_v3/results/hosted/final.json       per (model, condition) metrics, paired diffs, oracle reference
  arith_v3/results/hosted/results-*.json   raw Valkyrie results
  arith_v3/docs/img/*.svg                  charts
"""
import json
import os
import random
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

V3 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(V3))
from arithmetic_eval.grade import oracle_prediction, score  # noqa: E402

RES = V3 / "results" / "hosted"
IMG = V3 / "docs" / "img"
RES.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)
ENV = {k: v for k, v in os.environ.items() if k != "VALKYRIE_URL"}
B = 10_000
NAMES = {"claude-opus-5-5": "Claude Opus 5.5", "claude-fable-5-2": "Claude Fable 5.2",
         "claude-sonnet-5-5": "Claude Sonnet 5.5", "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol"}
COND = {"v3-noprobe": "No probes", "v3-probe10": "≤10 optional probes"}
OPS = ("add", "sub", "mul", "div")


def load(cid):
    return [json.loads((V3 / f"cases/{s}/{cid}.json").read_text()) for s in ("public", "private")]


def group(cid):
    pub, _ = load(cid)
    return {"L1_easy": "L1 easy", "L1_hard": "L1 hard"}.get(pub["difficulty"][:7], f"L{pub['level']}")


def results(rid):
    f = RES / f"results-{rid}.json"
    if not f.exists():
        subprocess.run(["valkyrie", "run", "results", rid, "--path", str(f)], env=ENV, check=True, capture_output=True)
    return json.loads(f.read_text())


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def boot(xs, rng):
    if not xs:
        return [None, None]
    n = len(xs)
    ms = sorted(sum(xs[rng.randrange(n)] for _ in range(n)) / n for _ in range(B))
    return [ms[int(0.025 * B)], ms[int(0.975 * B)]]


CASES = [c["task_id"] for c in json.loads((V3 / "cases/manifest.json").read_text())["cases"]]
GROUPS = {c: group(c) for c in CASES}
ORACLE = {c: score(*load(c), oracle_prediction(*load(c), [])[0])["primary_accuracy"] for c in CASES}

cells = defaultdict(dict)  # (model, cond) -> case -> rewards (None = errored, scored 0)
run_ids = []
for line in (Path(__file__).parent / "runs_hosted.tsv").read_text().splitlines():
    if not line.strip():
        continue
    model, ds, rid = line.split("\t")
    model, cond = model.split("/")[-1], ds.split("/")[1].split("@")[0]
    run_ids.append({"model": model, "condition": cond, "run_id": rid})
    d = results(rid)
    for c in CASES:
        cells[(model, cond)][c] = None
    for task, ev in (d.get("evaluation_results") or {}).items():
        rw = (ev or {}).get("rewards") if isinstance(ev, dict) else None
        cells[(model, cond)][task.split("-")[0].upper()] = rw

rng = random.Random(0)
R = lambda r: (r or {}).get("reward") or 0.0  # noqa: E731
out = {"cells": [], "pairs": [], "runs": run_ids, "bootstrap_resamples": B,
       "oracle_reference": {"no_probes": mean(ORACLE.values()),
                            "by_group": {g: mean([ORACLE[c] for c in CASES if GROUPS[c] == g]) for g in sorted(set(GROUPS.values()))},
                            "per_case": ORACLE}}
for (model, cond), reps in sorted(cells.items()):
    err = [R(reps[c]) for c in CASES]
    ok = [r for r in reps.values() if r and r.get("valid")]
    base = cells.get((model, "v3-noprobe"), {}) if cond != "v3-noprobe" else {}
    l3 = [c for c in CASES if GROUPS[c] == "L3"]
    out["cells"].append({
        "model": model, "condition": cond, "n": len(CASES), "valid": len(ok),
        "errored": sum(1 for r in reps.values() if r is None),
        "err_acc": mean(err), "ci95": boot(err, rng),
        "by_group": {g: mean([R(reps[c]) for c in CASES if GROUPS[c] == g]) for g in sorted(set(GROUPS.values()))},
        "by_op": {op: mean([r.get(f"{op}_error_accuracy") for r in ok]) for op in OPS},
        "overall": mean([r["overall_accuracy"] for r in ok]),
        "macro": mean([r.get("macro_error_accuracy") for r in ok]),
        "brier": mean([r.get("brier_error_cases") for r in ok]),
        "ece": mean([r.get("ece_error_cases") for r in ok]),
        # transfer is only defined before the target op is probed (v3 rule); count what stayed clean
        "l3_transfer": mean([(reps[c] or {}).get("transfer_error_accuracy") for c in l3]),
        "l3_transfer_clean": sum(1 for c in l3 if reps[c] and "transfer_error_accuracy" in reps[c]),
        "probes_mean": mean([(reps[c] or {}).get("probes_used", 0) for c in CASES]),
        "cases_probed": sum(1 for c in CASES if (reps[c] or {}).get("probes_used", 0) > 0),
        "k100_reached": sum(1 for r in ok if "k100_error_observed" in r),
        "k100_mean": mean([r.get("k100_error_observed") for r in ok]),
        "snapshots_mean": mean([r.get("snapshots") for r in ok]),
        "gain_vs_noprobe": mean([R(reps[c]) - R(base[c]) for c in CASES]) if base else None,
        "per_case": {c: R(reps[c]) for c in CASES},
    })
models = sorted({m for m, _ in cells})
for cond in COND:
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            ra, rb = cells.get((a, cond)), cells.get((b, cond))
            if not ra or not rb:
                continue
            d = [R(ra[c]) - R(rb[c]) for c in CASES]
            lo, hi = boot(d, rng)
            out["pairs"].append({"condition": cond, "a": a, "b": b, "n": len(CASES), "diff": mean(d),
                                 "ci95": [lo, hi], "significant": lo > 0 or hi < 0})
(RES / "final.json").write_text(json.dumps(out, indent=1))

# ---- SVG charts (no dependencies), same style as docs/img in the earlier benchmark ----
C = {"v3-noprobe": "#8A9A93", "v3-probe10": "#3E8E8F", "ideal": "#E4572E", "ink": "#17241F", "grid": "#E3E8E5"}
get = lambda m, c: next((x for x in out["cells"] if x["model"] == m and x["condition"] == c), None)  # noqa: E731
# charts show only models whose runs completed (errored tasks are infra failures, e.g. API quota)
complete = [m for m in models if all((get(m, c) or {"errored": 1})["errored"] == 0 for c in COND)]
order = sorted(complete, key=lambda m: -((get(m, "v3-probe10") or {}).get("err_acc") or 0))
SERIES = [("v3-noprobe", "No probes", C["v3-noprobe"]), ("v3-probe10", "≤10 optional probes", C["v3-probe10"])]


def bars(fname, title, groups, value, ci=None, ref=None, W=760):
    H, L, T, Bm = 380, 60, 50, 60
    pw, ph = W - L - 20, H - T - Bm
    gw = pw / len(groups)
    bw = (gw - 24) / len(SERIES)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="{L}" y="26" font-size="16" font-weight="700" fill="{C["ink"]}">{title}</text>']
    for v in range(0, 101, 25):
        y = T + ph - v / 100 * ph
        s.append(f'<line x1="{L}" y1="{y}" x2="{W - 20}" y2="{y}" stroke="{C["grid"]}"/>')
        s.append(f'<text x="{L - 8}" y="{y + 4}" font-size="11" fill="#6b6b66" text-anchor="end">{v}%</text>')
    for i, (gkey, glabel) in enumerate(groups):
        x0 = L + i * gw + 12
        for j, (cond, label, color) in enumerate(SERIES):
            v = value(gkey, cond)
            if v is None:
                continue
            x, y = x0 + j * bw, T + ph - v * ph
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw - 4:.1f}" height="{ph - (y - T):.1f}" rx="3" fill="{color}"><title>{glabel} · {label}: {100 * v:.1f}%</title></rect>')
            top = y
            if ci:
                lo, hi = ci(gkey, cond)
                xc = x + (bw - 4) / 2
                s.append(f'<line x1="{xc:.1f}" y1="{T + ph - lo * ph:.1f}" x2="{xc:.1f}" y2="{T + ph - hi * ph:.1f}" stroke="{C["ink"]}" stroke-width="1.2"/>')
                top = min(y, T + ph - hi * ph)
            s.append(f'<text x="{x + (bw - 4) / 2:.1f}" y="{top - 6:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="{C["ink"]}">{100 * v:.0f}</text>')
        if ref:
            r = ref(gkey)
            if r is not None:
                y = T + ph - r * ph
                s.append(f'<line x1="{x0 - 4:.1f}" y1="{y:.1f}" x2="{x0 + gw - 20:.1f}" y2="{y:.1f}" stroke="{C["ideal"]}" stroke-dasharray="5 4" stroke-width="1.5"/>')
        s.append(f'<text x="{x0 + (gw - 24) / 2:.1f}" y="{T + ph + 20}" font-size="12" text-anchor="middle" fill="{C["ink"]}">{glabel}</text>')
    lx = L
    for cond, label, color in SERIES:
        s.append(f'<rect x="{lx}" y="{H - 22}" width="12" height="12" rx="2" fill="{color}"/><text x="{lx + 17}" y="{H - 12}" font-size="12" fill="{C["ink"]}">{label}</text>')
        lx += 190
    if ref:
        s.append(f'<line x1="{lx}" y1="{H - 16}" x2="{lx + 20}" y2="{H - 16}" stroke="{C["ideal"]}" stroke-dasharray="5 4" stroke-width="1.5"/><text x="{lx + 26}" y="{H - 12}" font-size="12" fill="{C["ideal"]}">oracle reference, no probes</text>')
    elif ci:
        s.append(f'<text x="{W - 20}" y="{H - 12}" font-size="10" text-anchor="end" fill="#6b6b66">whiskers: 95% bootstrap CI over cases</text>')
    s.append("</svg>")
    (IMG / fname).write_text("\n".join(s))


OR = out["oracle_reference"]
bars("v3_accuracy.svg", f"ARITH-PROBE v3: accuracy on the student's errors (n={len(CASES)} cases)",
     [(m, NAMES.get(m, m).replace("Claude ", "")) for m in order],
     lambda m, c: (get(m, c) or {}).get("err_acc"), ci=lambda m, c: get(m, c)["ci95"],
     ref=lambda m: OR["no_probes"])
GL = sorted(OR["by_group"])
bars("v3_by_level.svg", "By level, mean of all models (accuracy on the student's errors)",
     [(g, g) for g in GL],
     lambda g, c: mean([x["by_group"][g] for x in out["cells"] if x["condition"] == c and x["model"] in complete]),
     ref=lambda g: OR["by_group"][g])

for c in sorted(out["cells"], key=lambda c: (c["condition"], -(c["err_acc"] or 0))):
    print(f"{c['model']:18} {c['condition']:11} err={100 * c['err_acc']:5.1f} "
          f"CI=[{100 * c['ci95'][0]:4.1f},{100 * c['ci95'][1]:4.1f}] "
          + " ".join(f"{g}={100 * v:5.1f}" for g, v in c["by_group"].items())
          + f" probes={c['probes_mean']:.1f} valid={c['valid']} err'd={c['errored']}")
print("oracle reference", {k: round(v, 3) for k, v in OR["by_group"].items()}, round(OR["no_probes"], 3),
      "| significant pairs:", sum(p["significant"] for p in out["pairs"]), "/", len(out["pairs"]))
