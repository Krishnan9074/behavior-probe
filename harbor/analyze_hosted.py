"""Results for the hosted Valkyrie runs (harbor/runs_hosted.tsv).

    python3 harbor/analyze_hosted.py

Pulls each run's per-task rewards, then writes:
  results/hosted/final.json      per (model, condition): mean, bootstrap 95% CI, metrics, paired diffs
  results/hosted/results-*.json  raw Valkyrie results
  docs/img/*.svg                 charts for the README
"""
import json
import os
import random
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results" / "hosted"
IMG = ROOT / "docs" / "img"
RES.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)
ENV = {k: v for k, v in os.environ.items() if k != "VALKYRIE_URL"}
B = 10_000
NAMES = {"claude-opus-5-5": "Opus 5.5", "claude-fable-5-2": "Fable 5.2", "claude-sonnet-5-5": "Sonnet 5.5",
         "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol"}
COND = {"hard-noprobe": "No probes", "hard-probe10": "≤10 optional probes"}


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


def case_of(task_id):
    return task_id.split("-")[0].upper()


cells = defaultdict(dict)  # (model, cond) -> case -> rewards
run_ids = []
for line in (Path(__file__).parent / "runs_hosted.tsv").read_text().splitlines():
    if not line.strip():
        continue
    model, ds, rid = line.split("\t")
    model, cond = model.split("/")[-1], ds.split("/")[1].split("@")[0]
    run_ids.append({"model": model, "condition": cond, "run_id": rid})
    d = results(rid)
    for task, ev in (d.get("evaluation_results") or {}).items():
        rw = (ev or {}).get("rewards") if isinstance(ev, dict) else None
        cells[(model, cond)][case_of(task)] = rw  # None = task errored (scored 0)

rng = random.Random(0)
out = {"cells": [], "pairs": [], "runs": run_ids, "bootstrap_resamples": B}
for (model, cond), reps in sorted(cells.items()):
    cases = sorted(reps)
    err = [(r or {}).get("reward") or 0.0 for r in (reps[c] for c in cases)]
    ok = [r for r in reps.values() if r and r.get("valid")]
    base = cells.get((model, "hard-noprobe"), {}) if cond != "hard-noprobe" else {}
    shared = [c for c in cases if c in base]
    gain = mean([((reps[c] or {}).get("reward") or 0) - ((base[c] or {}).get("reward") or 0) for c in shared]) if shared else None
    out["cells"].append({
        "model": model, "condition": cond, "n": len(cases), "valid": len(ok),
        "err_acc": mean(err), "ci95": boot(err, rng),
        "overall": mean([r["overall_accuracy"] for r in ok]),
        "familiar": mean([r["familiar_error_accuracy"] for r in ok]),
        "transfer": mean([r["transfer_error_accuracy"] for r in ok]),
        "brier": mean([r["brier"] for r in ok]),
        "probes_mean": mean([(reps[c] or {}).get("probes_used", 0) for c in cases]),
        "cases_probed": sum(1 for c in cases if (reps[c] or {}).get("probes_used", 0) > 0),
        "gain_vs_noprobe": gain,
    })
models = sorted({m for m, _ in cells})
for cond in COND:
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            ra, rb = cells.get((a, cond), {}), cells.get((b, cond), {})
            sh = sorted(set(ra) & set(rb))
            if len(sh) < 5:
                continue
            d = [((ra[c] or {}).get("reward") or 0) - ((rb[c] or {}).get("reward") or 0) for c in sh]
            lo, hi = boot(d, rng)
            out["pairs"].append({"condition": cond, "a": a, "b": b, "n": len(sh), "diff": mean(d), "ci95": [lo, hi],
                                 "significant": lo > 0 or hi < 0})
# ideal reasoner on the same cases
used = sorted({c for reps in cells.values() for c in reps})
ceil = [json.loads((ROOT / "hard_cases/private" / f"{c}.json").read_text())["ceiling"] for c in used]
out["ideal"] = {"no_probes": mean([c["ideal_b0"] for c in ceil]), "three_probes": mean([c["ideal_b3_greedy"] for c in ceil]), "cases": used}
(RES / "final.json").write_text(json.dumps(out, indent=1))

# ---- SVG charts (no dependencies) ----
C = {"hard-noprobe": "#8A9A93", "hard-probe10": "#3E8E8F", "ideal": "#E4572E", "ink": "#17241F", "grid": "#E3E8E5"}
get = lambda m, c: next((x for x in out["cells"] if x["model"] == m and x["condition"] == c), None)
order = sorted(models, key=lambda m: -((get(m, "hard-probe10") or {}).get("err_acc") or 0))


def bar_chart(fname, title, series, ideal_lines=()):
    W, H, L, T, Bm = 760, 380, 60, 50, 60
    pw, ph = W - L - 20, H - T - Bm
    g = len(order)
    gw = pw / g
    bw = (gw - 24) / len(series)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<text x="{L}" y="26" font-size="16" font-weight="700" fill="{C["ink"]}">{title}</text>']
    for v in range(0, 101, 25):
        y = T + ph - v / 100 * ph
        s.append(f'<line x1="{L}" y1="{y}" x2="{W - 20}" y2="{y}" stroke="{C["grid"]}"/>')
        s.append(f'<text x="{L - 8}" y="{y + 4}" font-size="11" fill="#6b6b66" text-anchor="end">{v}%</text>')
    for i, m in enumerate(order):
        x0 = L + i * gw + 12
        for j, (cond, label, color) in enumerate(series):
            c = get(m, cond)
            if not c:
                continue
            v, (lo, hi) = 100 * c["err_acc"], c["ci95"]
            x = x0 + j * bw
            y = T + ph - v / 100 * ph
            s.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw - 4:.1f}" height="{ph - (y - T):.1f}" rx="3" fill="{color}"><title>{NAMES.get(m, m)} · {label}: {v:.1f}%</title></rect>')
            if lo is not None:
                ylo, yhi, xc = T + ph - 100 * lo / 100 * ph, T + ph - 100 * hi / 100 * ph, x + (bw - 4) / 2
                s.append(f'<line x1="{xc:.1f}" y1="{ylo:.1f}" x2="{xc:.1f}" y2="{yhi:.1f}" stroke="{C["ink"]}" stroke-width="1.2"/>')
            ylab = min(y, T + ph - (hi or 0) * ph) - 6
            s.append(f'<text x="{x + (bw - 4) / 2:.1f}" y="{ylab:.1f}" font-size="11" font-weight="700" text-anchor="middle" fill="{C["ink"]}">{v:.0f}</text>')
        s.append(f'<text x="{x0 + (gw - 24) / 2:.1f}" y="{T + ph + 20}" font-size="12" text-anchor="middle" fill="{C["ink"]}">{NAMES.get(m, m)}</text>')
    for v, label in ideal_lines:
        y = T + ph - v * ph
        s.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W - 20}" y2="{y:.1f}" stroke="{C["ideal"]}" stroke-dasharray="5 4" stroke-width="1.5"/>')
        s.append(f'<text x="{L + 4}" y="{y - 5:.1f}" font-size="11" text-anchor="start" fill="{C["ideal"]}">{label}</text>')
    lx = L
    for cond, label, color in series:
        s.append(f'<rect x="{lx}" y="{H - 22}" width="12" height="12" rx="2" fill="{color}"/><text x="{lx + 17}" y="{H - 12}" font-size="12" fill="{C["ink"]}">{label}</text>')
        lx += 190
    s.append(f'<text x="{W - 20}" y="{H - 12}" font-size="10" text-anchor="end" fill="#6b6b66">whiskers: 95% bootstrap CI over cases</text>')
    s.append("</svg>")
    (IMG / fname).write_text("\n".join(s))


I = out["ideal"]
bar_chart("hard_accuracy.svg", "Accuracy on the student's errors (hard suite, n=%d cases)" % len(used),
          [("hard-noprobe", "No probes", C["hard-noprobe"]), ("hard-probe10", "≤10 optional probes", C["hard-probe10"])],
          [(I["no_probes"], f"ideal reasoner, no probes ({100 * I['no_probes']:.0f}%)"), (I["three_probes"], f"ideal reasoner, 3 probes ({100 * I['three_probes']:.0f}%)")])

# probes vs gain
W, H = 760, 300
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Helvetica,Arial,sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>',
     f'<text x="20" y="26" font-size="16" font-weight="700" fill="{C["ink"]}">Who chooses to probe, and what it buys (≤10 optional probes)</text>']
for i, m in enumerate(order):
    c = get(m, "hard-probe10")
    if not c:
        continue
    y = 60 + i * 44
    s.append(f'<text x="20" y="{y + 16}" font-size="13" fill="{C["ink"]}">{NAMES.get(m, m)}</text>')
    w = c["probes_mean"] / 10 * 300
    s.append(f'<rect x="140" y="{y}" width="{w:.1f}" height="22" rx="3" fill="{C["hard-probe10"]}"/><text x="{146 + w:.1f}" y="{y + 16}" font-size="12" fill="{C["ink"]}">{c["probes_mean"]:.1f} probes/task</text>')
    gn = c.get("gain_vs_noprobe")
    if gn is not None:
        s.append(f'<text x="560" y="{y + 16}" font-size="13" fill="{C["ideal"] if gn > 0.15 else "#6b6b66"}">{"+" if gn >= 0 else ""}{100 * gn:.0f} pts vs no probes</text>')
s.append("</svg>")
(IMG / "probes.svg").write_text("\n".join(s))

for c in sorted(out["cells"], key=lambda c: (c["condition"], -(c["err_acc"] or 0))):
    print(f"{c['model']:18} {c['condition']:13} n={c['n']:2} err={100 * c['err_acc']:5.1f} "
          f"CI=[{100 * (c['ci95'][0] or 0):4.1f},{100 * (c['ci95'][1] or 0):4.1f}] probes={c['probes_mean']:.1f} valid={c['valid']}")
print("ideal", I["no_probes"], I["three_probes"], "| significant pairs:", sum(p["significant"] for p in out["pairs"]), "/", len(out["pairs"]))
