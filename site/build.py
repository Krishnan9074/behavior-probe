#!/usr/bin/env python3
"""Build the public leaderboard: site/template.html + slim stats -> site/public/index.html.

Reads ../valkyrie/report/data.js (written by valkyrie/build_report.py). Publishes only
aggregate and per-task scores: no hidden rules, answer keys, prompts or trajectories.
    python3 site/build.py
"""
import json
from pathlib import Path
from statistics import mean, pstdev

HERE = Path(__file__).parent
s = (HERE.parent / "valkyrie/report/data.js").read_text()
D = json.loads(s[s.index("{"):s.rindex("}") + 1])

NAMES = {"claude-sonnet-5-5": ("Claude Sonnet 5.5", "Anthropic"), "claude-opus-5-5": ("Claude Opus 5.5", "Anthropic"),
         "claude-fable-5-2": ("Claude Fable 5.2", "Anthropic"), "gpt-6-astra": ("GPT-6 Astra", "OpenAI"),
         "gpt-6.1-sol": ("GPT-6.1 Sol", "OpenAI")}
HARNESS = {"claude_code-v1.0.0": "Claude Code", "codex-v1.0.0": "Codex CLI"}


def avg(xs):
    xs = [x for x in xs if x is not None]
    return round(mean(xs), 4) if xs else None


runs = []
for r in D["runs"]:
    reps = [t.get("report") or {} for t in r["tasks"]]
    ok = [x for x in reps if x and not x.get("error")]
    scores = [x.get("primary_wrong_answer_accuracy") or 0 for x in reps]  # rejected/missing count as 0
    runs.append({
        "model": r["model"], "setting": r["dataset"], "harness": HARNESS.get(r["agent"], r["agent"]),
        "acc": avg(scores), "se": round(pstdev(scores) / (len(scores) - 1) ** 0.5, 4),  # SE of the mean over tasks
        "short": avg([x["wrong_answer_accuracy_by_domain"]["familiar"] for x in ok]),
        "long": avg([x["wrong_answer_accuracy_by_domain"]["transfer"] for x in ok]),
        "overall": avg([x["overall_accuracy_diagnostic"] for x in ok]),
        "brier": avg([x["calibration_on_wrong_questions"]["brier_lower_is_better"] for x in ok]),
        "probes": avg([x.get("probes_used") for x in reps]), "valid": len(ok), "n": len(reps),
        "cost": avg([(t.get("metrics") or {}).get("cost") for t in r["tasks"]]),
        "secs": avg([(t.get("metrics") or {}).get("wall_clock_duration") for t in r["tasks"]]),
        "tasks": {t["case"]: [round((t.get("report") or {}).get("primary_wrong_answer_accuracy") or 0, 2),
                              (t.get("report") or {}).get("probes_used") or 0,
                              bool((t.get("report") or {}).get("error"))] for t in r["tasks"]},
    })

hard = {k: c for k, c in D["cases"].items() if c["suite"] == "hard"}
slim = {
    "updated": "November 14, 2026",
    "models": {k: {"name": n, "lab": lab} for k, (n, lab) in NAMES.items()},
    "runs": runs,
    "cases": {"easy": [k for k, c in D["cases"].items() if c["suite"] == "easy"], "hard": list(hard)},
    "ideal": {"b0": avg([c["ceiling"]["ideal_b0"] for c in hard.values()]),
              "b3": avg([c["ceiling"]["ideal_b3_greedy"] for c in hard.values()]),
              "tasks": {k: c["ceiling"]["ideal_b0"] for k, c in hard.items()}},
    # Public inputs of one task (these four lines are in the agent's prompt); no answers to test questions.
    "example": {"id": "H001", "observations": D["cases"]["H001"]["observations"],
                "questions": [{"id": q["id"], "a": q["a"], "b": q["b"]} for q in D["cases"]["H001"]["questions"][:3]]},
}
out = HERE / "public/index.html"
out.write_text((HERE / "template.html").read_text().replace("/*DATA*/", "window.BP = " + json.dumps(slim, separators=(",", ":")).replace("</", "<\\/") + ";"))
print("wrote", out, out.stat().st_size, "bytes")
for r in runs:
    print(f"{r['model']:18} {r['setting']:13} acc {r['acc']:.3f} ±{r['se']:.3f} cost {r['cost']} secs {r['secs']} probes {r['probes']} valid {r['valid']}")
