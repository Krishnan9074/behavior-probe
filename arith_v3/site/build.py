#!/usr/bin/env python3
"""Build the v3 Behavior-Probe leaderboard: template.html + slim stats -> public/index.html.

Reads ../results/hosted/final.json (from harbor/analyze_hosted.py) and the raw Valkyrie results.
Publishes only aggregate and per-task scores and one task's public inputs: no hidden rules,
answer keys or trajectories.
    python3 arith_v3/site/build.py

Live at https://behavior-probe.vercel.app (Vercel project "behavior-probe"): this page is served
at / and the earlier Behavior-Probe leaderboard (site/public/index.html) at /v1/. To deploy, put
public/index.html at the root of a folder, site/public/index.html at v1/index.html, copy
site/public/.vercel into it, and run `npx vercel deploy --prod` from that folder.
"""
import json
from pathlib import Path
from statistics import mean, pstdev

HERE = Path(__file__).parent
V3 = HERE.parent
F = json.loads((V3 / "results/hosted/final.json").read_text())
MANIFEST = json.loads((V3 / "cases/manifest.json").read_text())["cases"]

NAMES = {"claude-sonnet-5-5": ("Claude Sonnet 5.5", "Anthropic"), "claude-opus-5-5": ("Claude Opus 5.5", "Anthropic"),
         "claude-fable-5-2": ("Claude Fable 5.2", "Anthropic"), "gpt-6-astra": ("GPT-6 Astra", "OpenAI"),
         "gpt-6.1-sol": ("GPT-6.1 Sol", "OpenAI")}
HARNESS = {"anthropic": "Claude Code", "gpt": "Codex CLI"}
GROUP = {"L1 easy": "easy", "L1 hard": "hard", "L2": "l2", "L3": "l3"}


def r4(v):
    return None if v is None else round(v, 4)


runs = []
for cell in F["cells"]:
    rid = next(r["run_id"] for r in F["runs"] if r["model"] == cell["model"] and r["condition"] == cell["condition"])
    ev = json.loads((V3 / f"results/hosted/results-{rid}.json").read_text())["evaluation_results"]
    by_case = {t.split("-")[0].upper(): v for t, v in ev.items()}
    scores = list(cell["per_case"].values())
    secs = [(v.get("task_breakdown") or {}).get("agent_run_duration") for v in by_case.values()]
    rw = lambda c: (by_case.get(c) or {}).get("rewards") or {}  # noqa: E731
    runs.append({
        "model": cell["model"], "setting": cell["condition"],
        "harness": HARNESS["gpt" if cell["model"].startswith("gpt") else "anthropic"],
        "acc": r4(cell["err_acc"]), "se": r4(pstdev(scores) / (len(scores) - 1) ** 0.5),
        "lo": r4(cell["ci95"][0]), "hi": r4(cell["ci95"][1]),
        **{GROUP[g]: r4(v) for g, v in cell["by_group"].items()},
        "overall": r4(cell["overall"]), "brier": r4(cell["brier"]), "ece": r4(cell["ece"]),
        "probes": r4(cell["probes_mean"]), "probed": cell["cases_probed"], "k100": cell["k100_reached"],
        "valid": cell["valid"], "n": cell["n"], "gain": r4(cell["gain_vs_noprobe"]),
        "secs": r4(mean([s for s in secs if s is not None])),
        # per task: [error-Q acc, probes, rejected, all-question acc, Brier, agent secs, K100 reached]
        # (the page recomputes every column from these for the level toggle)
        "tasks": {c: [round(cell["per_case"][c], 3), int(rw(c).get("probes_used", 0)), not rw(c).get("valid"),
                      r4(rw(c).get("overall_accuracy")), r4(rw(c).get("brier_error_cases")),
                      r4(((by_case.get(c) or {}).get("task_breakdown") or {}).get("agent_run_duration")),
                      "k100_error_observed" in rw(c)] for c in cell["per_case"]},
    })

O = F["oracle_reference"]
cases = [{"id": c["task_id"],
          "group": GROUP[{"L1_easy": "L1 easy", "L1_hard": "L1 hard"}.get(c["difficulty"][:7], f"L{c['level']}")],
          "op": c["focus"] if c["level"] == 1 else None, "target": c["target_operation"]} for c in MANIFEST]
pub = json.loads((V3 / "cases/public/A002.json").read_text())  # public inputs only
slim = {
    "updated": "November 15, 2026",
    "models": {k: {"name": n, "lab": lab} for k, (n, lab) in NAMES.items()},
    "runs": runs,
    "cases": cases,
    "oracle": {"all": r4(O["no_probes"]), **{GROUP[g]: r4(v) for g, v in O["by_group"].items()},
               "tasks": {c: r4(v) for c, v in O["per_case"].items()}},
    "pairs": [{k: (r4(v) if isinstance(v, float) else v) for k, v in p.items() if k != "n"} for p in F["pairs"]],
    "example": {"id": pub["task_id"], "target": pub["target_operation"], "observations": pub["observations"],
                "questions": [{k: q[k] for k in ("op", "a", "b")} for q in pub["test_questions"][:3]]},
}
out = HERE / "public/index.html"
out.parent.mkdir(exist_ok=True)
out.write_text((HERE / "template.html").read_text().replace(
    "/*DATA*/", "window.BP = " + json.dumps(slim, separators=(",", ":")).replace("</", "<\\/") + ";"))
print("wrote", out, out.stat().st_size, "bytes")
for r in runs:
    print(f"{r['model']:18} {r['setting']:11} acc {r['acc']:.3f} ±{r['se']:.3f} secs {r['secs']:.0f} probes {r['probes']} valid {r['valid']}")
