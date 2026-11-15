"""Write docs/FAILURE_EXAMPLE.md from the hosted runs: the case where probing changed a model's
score the most, with its no-probe hypothesis, its probes, and a non-probing model on the same case.

    python3 harbor/failure_example.py
"""
import io
import json
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
F = json.loads((ROOT / "results/hosted/final.json").read_text())
ENV = {k: v for k, v in os.environ.items() if k != "VALKYRIE_URL"}
NAMES = {"claude-opus-5-5": "Claude Opus 5.5", "claude-fable-5-2": "Claude Fable 5.2", "claude-sonnet-5-5": "Claude Sonnet 5.5",
         "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol"}
BUG = {"smaller_from_larger": "subtracts the smaller digit from the larger instead of borrowing",
       "forget_decrement": "borrows 10 but forgets to reduce the next column",
       "write_zero": "writes 0 instead of borrowing", "borrow_skip": "borrows from two columns to the left",
       "double_decrement": "reduces the next column by 2 instead of 1", "write_bottom": "copies the bottom digit instead of borrowing"}
WHEN = {"any": "in any column", "ones": "in the ones column", "tens": "in the tens column", "high": "in the hundreds column or higher",
        "next_zero": "when the next top digit is 0", "incoming": "when the column was already borrowed from",
        "big_bottom": "when the bottom digit is 7 or more", "top_zero": "when the top digit is 0"}


def rewards(rid):
    d = json.loads((ROOT / "results/hosted" / f"results-{rid}.json").read_text())
    return {t.split("-")[0].upper(): (e or {}).get("rewards") for t, e in (d.get("evaluation_results") or {}).items()}


runs = {(r["model"], r["condition"]): r["run_id"] for r in F["runs"]}
R = {k: rewards(v) for k, v in runs.items()}
best = None
for (m, cond), rid in runs.items():
    if cond != "hard-probe10" or (m, "hard-noprobe") not in R:
        continue
    for case, rw in R[(m, cond)].items():
        base = R[(m, "hard-noprobe")].get(case)
        if rw and base and rw.get("probes_used", 0) > 0:
            gain = rw["reward"] - base["reward"]
            if best is None or gain > best[0]:
                best = (gain, m, case)
gain, model, case = best
# a model on the same case that probed least
others = [(R[(m, "hard-probe10")].get(case) or {}, m) for (m, c) in runs if c == "hard-probe10" and m != model]
low = min(others, key=lambda x: (x[0].get("probes_used", 99), x[0].get("reward", 1)))


def agent_output(rid, task):
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["valkyrie", "run", "output", rid, f"{task}/agent_output.tar.gz", "-o", tmp + "/o"],
                       env=ENV, check=True, capture_output=True)
        f = next(Path(tmp).rglob("agent_output.tar.gz"))
        with tarfile.open(f) as t:
            names = t.getnames()
            rd = lambda n: t.extractfile(n).read().decode(errors="replace") if n in names else ""
            return rd("logs/final_message.txt").strip(), rd("logs/trajectory.jsonl")


def probes_from(traj):
    out = []
    for m in re.finditer(r'\\"a\\": (\d+), \\"b\\": (\d+), \\"student_answer\\": (\d+)', traj):
        t = tuple(int(x) for x in m.groups())
        if t not in out:
            out.append(t)
    if not out:
        for m in re.finditer(r'"a": (\d+), "b": (\d+), "student_answer": (\d+)', traj):
            t = tuple(int(x) for x in m.groups())
            if t not in out:
                out.append(t)
    return out


def clip(s, n=600):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n].rsplit(" ", 1)[0] + " …"


low_case = f"{case.lower()}-p10"
no_msg, _ = agent_output(runs[(model, "hard-noprobe")], f"{case.lower()}-p0")
yes_msg, yes_traj = agent_output(runs[(model, "hard-probe10")], low_case)
low_msg, _ = agent_output(runs[(low[1], "hard-probe10")], low_case)
probes = probes_from(yes_traj)
priv = json.loads((ROOT / "hard_cases/private" / f"{case}.json").read_text())
pub = json.loads((ROOT / "hard_cases/public" / f"{case}.json").read_text())
rule = "; otherwise, ".join(f"{BUG[b]} {WHEN[w]}" for b, w in priv["rule"]["components"])
base = R[(model, "hard-noprobe")][case]
yes = R[(model, "hard-probe10")][case]

md = f"""**Case {case}.** The hidden rule (never shown to the agent): when a column needs a borrow, the student {rule}. The ideal reasoner gets {100 * priv['ceiling']['ideal_b0']:.0f}% from the observations alone and {100 * priv['ceiling']['ideal_b3_greedy']:.0f}% with 3 probes.

| Observed | Student wrote | Correct |
|---|---|---|
""" + "".join(f"| {o['a']} − {o['b']} | **{o['student_answer']}** | {o['a'] - o['b']} |\n" for o in pub["observations"]) + f"""
**{NAMES[model]}, no probes: {100 * base['reward']:.0f}%** on the student's errors ({100 * base['transfer_error_accuracy']:.0f}% on 4–5-digit problems). Its conclusion:

> {clip(no_msg)}

**{NAMES[model]}, same case, ≤10 optional probes: {100 * yes['reward']:.0f}%** ({yes['probes_used']:.0f} probes). What it asked:

| Probe | Student wrote | Correct |
|---|---|---|
""" + "".join(f"| {a} − {b} | **{s}** | {a - b} |\n" for a, b, s in probes[:10]) + f"""
> {clip(yes_msg)}

**{NAMES[low[1]]}, same case, same optional probes:** {low[0].get('probes_used', 0):.0f} probes, **{100 * low[0].get('reward', 0):.0f}%**.

> {clip(low_msg, 400)}

The four observations fit many rules. Without probes, the model picked one and applied it confidently. With probes, it tested the rule on new problems and corrected it. The benchmark measures that difference.
"""
(ROOT / "docs" / "FAILURE_EXAMPLE.md").write_text(md)
print(f"case {case}: {model} {base['reward']:.2f} -> {yes['reward']:.2f}; low = {low[1]} {low[0].get('reward')}; {len(probes)} probes parsed")
(ROOT / "docs" / "failure_example.json").write_text(json.dumps({
    "case": case, "model": model, "model_name": NAMES[model], "no_probe": base["reward"], "with_probes": yes["reward"],
    "probes_used": yes["probes_used"], "low_model": NAMES[low[1]], "low_probes": low[0].get("probes_used", 0),
    "low_reward": low[0].get("reward", 0), "rule": rule, "observations": pub["observations"],
    "probes": [list(x) for x in probes[:10]]}))
