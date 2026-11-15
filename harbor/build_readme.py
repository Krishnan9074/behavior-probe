"""Render README.md from results/hosted/final.json. Every number is computed, never typed.

    python3 harbor/build_readme.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
F = json.loads((ROOT / "results/hosted/final.json").read_text())
NAMES = {"claude-opus-5-5": "Claude Opus 5.5", "claude-fable-5-2": "Claude Fable 5.2", "claude-sonnet-5-5": "Claude Sonnet 5.5",
         "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol"}
HARNESS = {"claude": "Claude Code (`claude_code-bp`)", "gpt": "Codex (`codex-v1.0.0`)"}
get = lambda m, c: next((x for x in F["cells"] if x["model"] == m and x["condition"] == c), None)
MODELS = sorted({c["model"] for c in F["cells"]}, key=lambda m: -((get(m, "hard-probe10") or {}).get("err_acc") or 0))
I = F["ideal"]
N = len(I["cases"])
p = lambda v: "–" if v is None else f"{100 * v:.1f}"
ci = lambda c: "–" if not c or c["ci95"][0] is None else f"{p(c['ci95'][0])}–{p(c['ci95'][1])}"
OVERVIEW_FILE = ROOT / "docs" / "OVERVIEW.md"  # the human-written paragraph lives here


def headline_table():
    rows = ["| Model | Harness | No probes | ≤10 optional probes | Gain | Probes / task | Cases probed |",
            "|---|---|---|---|---|---|---|"]
    for m in MODELS:
        a, b = get(m, "hard-noprobe"), get(m, "hard-probe10")
        gain = (b or {}).get("gain_vs_noprobe")
        rows.append(f"| {NAMES.get(m, m)} | {HARNESS['claude' if m.startswith('claude') else 'gpt']} | "
                    f"**{p((a or {}).get('err_acc'))}** ({ci(a)}) | **{p((b or {}).get('err_acc'))}** ({ci(b)}) | "
                    f"{'–' if gain is None else ('+' if gain >= 0 else '') + p(gain)} | "
                    f"{'–' if not b else format(b['probes_mean'], '.1f')} | "
                    f"{'–' if not b else str(b['cases_probed']) + '/' + str(b['n'])} |")
    rows.append(f"| *Ideal reasoner* | – | *{p(I['no_probes'])}* | *{p(I['three_probes'])} (with 3 probes)* | | | |")
    return "\n".join(rows)


def detail_table(cond):
    rows = ["| Model | Error-question acc. | 95% CI | All 40 questions | 3-digit | 4–5-digit | Brier ↓ | Valid |",
            "|---|---|---|---|---|---|---|---|"]
    for m in MODELS:
        c = get(m, cond)
        if c:
            rows.append(f"| {NAMES.get(m, m)} | {p(c['err_acc'])} | {ci(c)} | {p(c['overall'])} | {p(c['familiar'])} | "
                        f"{p(c['transfer'])} | {c['brier']:.3f} | {c['valid']}/{c['n']} |")
    return "\n".join(rows)


def sig(cond):
    out = []
    for q in F["pairs"]:
        if q["condition"] == cond and q["significant"]:
            a, b = (q["a"], q["b"]) if q["diff"] > 0 else (q["b"], q["a"])
            lo, hi = sorted([abs(q["ci95"][0]), abs(q["ci95"][1])])
            out.append(f"{NAMES.get(a, a)} > {NAMES.get(b, b)} by {p(abs(q['diff']))} pts (95% CI {p(lo)}–{p(hi)})")
    return out


def runs_table():
    rows = ["| Model | Condition | Valkyrie run ID |", "|---|---|---|"]
    for r in F["runs"]:
        rows.append(f"| {NAMES.get(r['model'], r['model'])} | `{r['condition']}` | `{r['run_id']}` |")
    return "\n".join(rows)


overview = OVERVIEW_FILE.read_text().strip() if OVERVIEW_FILE.exists() else (
    "> **TODO (human-written, required by the hackathon):** replace this block with a one-paragraph overview "
    "of the benchmark written by you, in `docs/OVERVIEW.md`, then rerun `python3 harbor/build_readme.py`.")
example = (ROOT / "docs" / "FAILURE_EXAMPLE.md").read_text().strip() if (ROOT / "docs" / "FAILURE_EXAMPLE.md").exists() else "_Added after the runs finish._"
noprobe = [get(m, "hard-noprobe")["err_acc"] for m in MODELS if get(m, "hard-noprobe")]
probe = [get(m, "hard-probe10")["err_acc"] for m in MODELS if get(m, "hard-probe10")]
sig_n, sig_p = sig("hard-noprobe"), sig("hard-probe10")
P10 = [get(m, "hard-probe10") for m in MODELS if get(m, "hard-probe10")]
NP = [get(m, "hard-noprobe") for m in MODELS if get(m, "hard-noprobe")]
top = max(P10, key=lambda c: c["err_acc"])
heavy = [c for c in P10 if c is not top and c["probes_mean"] >= 8]  # probe nearly as much as the top model
light = min(P10, key=lambda c: c["probes_mean"])
gap_rows = [c for c in P10 if c["familiar"] - c["transfer"] >= 0.1]


def rng(cs, k, scale=100, fmt="{:.0f}"):
    v = [scale * c[k] for c in cs]
    return (fmt.format(min(v)) + "–" + fmt.format(max(v))) if len(v) > 1 else fmt.format(v[0])


f3 = (f"**How a model probes matters, not just how many times.** {NAMES[top['model']]} used {top['probes_mean']:.1f} probes per task and reached "
      f"{p(top['err_acc'])}%. " + (f"{', '.join(NAMES[c['model']] for c in heavy)} used almost as many ({rng(heavy, 'probes_mean', 1, '{:.1f}')}) "
      f"but reached only {rng(heavy, 'err_acc')}%. " if heavy else "") +
      f"{NAMES[light['model']]} probed in {light['cases_probed']} of {light['n']} cases ({light['probes_mean']:.1f} per task) and gained "
      f"{p(light.get('gain_vs_noprobe'))} points. No model reaches the ideal reasoner's {p(I['three_probes'])}% with 3 probes.")
f4 = (f"**Bigger problems are where fitted rules break.** Without probes, every model scores {rng(NP, 'familiar')}% on 3-digit error "
      f"questions but only {rng(NP, 'transfer')}% on 4–5-digit ones. " +
      (f"With probes, {NAMES[top['model']]} closes the gap ({p(top['familiar'])}% vs {p(top['transfer'])}%); "
       if top not in gap_rows else "") +
      (f"{', '.join(NAMES[c['model']] for c in gap_rows)} still drop {rng(gap_rows, 'familiar', 100) and ''}"
       f"{min(100 * (c['familiar'] - c['transfer']) for c in gap_rows):.0f}–{max(100 * (c['familiar'] - c['transfer']) for c in gap_rows):.0f} points."
       if gap_rows else ""))

md = f"""# BEHAVIOR-PROBE: do agents ask before they assume?

{overview}

![Accuracy on the student's errors](docs/img/hard_accuracy.svg)

## How it works

Each task is one **simulated student** who subtracts with a hidden, systematic bug. The agent gets:

- **4 of the student's past answers**, chosen so that many different bugs fit them;
- **40 new problems** (3 to 5 digits), chosen where those candidate bugs disagree;
- in the probe condition, an optional **`probe A B`** command that shows the student's answer to any new problem (up to 10 times; the prompt says using it is "entirely up to you").

It writes `/workspace/submission.json`: an integer answer and a confidence for each problem. **The score is accuracy on the 20 problems where the student gets it wrong**, so getting the arithmetic right earns nothing; the agent has to model the bug.

| | |
|---|---|
| Possible students | 2,304: two interacting components, each one of 6 bugs (subtract smaller from larger, borrow without decrementing, write 0, borrow from two columns over, decrement twice, copy the bottom digit) × 8 triggers (any column, ones, tens, hundreds+, next digit 0, incoming borrow, bottom digit ≥ 7, top digit 0) |
| Ambiguity, by design | the 4 observations are chosen so that many students fit them; test questions are where those students disagree |
| Solvable, by construction | each case records an **ideal reasoner** (uniform prior over all 2,304 students, majority vote): **{p(I['no_probes'])}%** from the observations alone, **{p(I['three_probes'])}%** after 3 well-chosen probes |
| Validity | no problem requires a step a real student couldn't write (a digit outside 0–9, or a borrow past the leftmost column) |
| Cases in this release | {N} hard students × 2 conditions (`hard-noprobe`, `hard-probe10`) |

## What it found

{headline_table()}

Accuracy on the student-error questions, %, with 95% bootstrap CIs over {N} cases. "Gain" is the change versus the same model with no probes, on the same cases.

![Probe use](docs/img/probes.svg)

1. **Without probes, every model is below the ideal reasoner's {p(I['no_probes'])}%** ({p(min(noprobe))}–{p(max(noprobe))}%). With only 4 observations, models commit to one rule that fits and stop. {"Significant differences: " + "; ".join(sig_n) + "." if sig_n else "No pair of models differs significantly."}
2. **With optional probes, the spread is {p(max(probe) - min(probe))} points** ({p(min(probe))}–{p(max(probe))}%). {"Significant differences: " + "; ".join(sig_p) + "." if sig_p else ""}
3. {f3}
4. {f4}

### A concrete failure

{example}

### Detail

**No probes**

{detail_table("hard-noprobe")}

**≤10 optional probes**

{detail_table("hard-probe10")}

## How it's built (Valkyrie + Harbor)

Every task is a [Harbor](https://docs.harborframework.com/tasks/overview) task, pushed to Valkyrie as `behavior-probe/hard-noprobe` and `behavior-probe/hard-probe10` and run on Modal.

```
harbor/datasets/hard-probe10/h001-p10/
├── instruction.md            # the student's 4 answers + 40 questions (public)
├── task.toml                 # limits; agent network = model APIs + oracle only
├── environment/
│   ├── Dockerfile            # agent image (Claude Code, Codex preinstalled) + `probe` client
│   ├── docker-compose.yaml   # main + oracle sidecar
│   └── oracle/               # the ONLY place the hidden rule exists during the run
└── tests/                    # answer key + grader, copied in after the agent finishes
```

- **The agent never sees the answer.** The hidden rule lives in an `oracle` sidecar container. It answers `probe A B`, enforces the budget of 10, refuses the 40 test questions and logs every probe. The answer key arrives in `tests/` only after the agent is done.
- **No public internet for the agent.** During the run it can reach only the model APIs and the oracle.
- **Rich reward.** `tests/grade.py` writes `reward.json` with the reward (error-question accuracy) plus overall accuracy, 3-digit and 4–5-digit accuracy, Brier score and probes used.
- **Harnesses.** We use the two harnesses Valkyrie provides out of the box: Claude Code for Claude models, Codex for GPT models. Each is its provider's own agent, so every model runs in the setup it was built for. The task needs only a shell, file writes and the `probe` command, so neither harness has a tool advantage. The trade-off is that harness and model are confounded across providers (see Limitations).

## Run it

```bash
uv tool install valkyrie-cli && valkyrie login
valkyrie org use <your-org>
python3 harbor/build_tasks.py --cases 30            # build the Harbor tasks from hard_cases/
valkyrie dataset push behavior-probe/hard-noprobe harbor/datasets/hard-noprobe --tag v2
valkyrie dataset push behavior-probe/hard-probe10 harbor/datasets/hard-probe10 --tag v2
valkyrie agent push valkyrie/agents/claude_code-bp && valkyrie agent push valkyrie/agents/codex-v1.0.0
valkyrie run start --agent claude_code-bp --dataset behavior-probe/hard-probe10@v2 \\
  --model anthropic/claude-opus-5-5 --provider modal -s ANTHROPIC_API_KEY <your-anthropic-secret> --concurrency 5
python3 harbor/analyze_hosted.py && python3 harbor/build_readme.py   # results, charts, this README
```

Modal needs `"runtime": "vm"` in its Valkyrie credentials for the sidecar (`harbor/connect_modal.sh` sets this up from `~/.modal.toml`). Cases are deterministic: `python3 hard_probe.py generate --root hard_cases --n 60 --seed 7`. Self-checks: `python3 hard_probe.py check` and `python3 -m unittest test_behavior_probe`.

### Runs (traces)

{runs_table()}

`valkyrie run fetch <id>` or `valkyrie tui` shows every task's log, the agent's full trajectory, its probes and the grader's output.

## Limitations

- **Synthetic students.** This measures hypothesis testing under controlled ambiguity, not tutoring real learners.
- **Harness confound.** Claude models ran on Claude Code and GPT models on Codex, so gaps between providers mix model and harness.
- **One run per cell, {N} cases.** The confidence intervals cover case sampling, not run-to-run variation.
- **Free probes.** Within the budget, probes cost nothing. A cost-weighted score would reward the most informative question more directly.

## Also in this repo

- `hard_probe.py` (hard suite generator and simulator) and `behavior_probe.py` (original easy suite and grader).
- `valkyrie/`: an earlier self-hosted Valkyrie version (custom benchmark service, local Docker). Its results include a 20-case easy suite and 60-case hard runs; see `submission/BENCHMARK.md`.
- `behavior_probe_report.html`: an interactive report of those earlier runs (inputs diff, every task, run comparison).
- `docs/ORIGINAL_SPEC.md`: the original benchmark spec.
"""
(ROOT / "README.md").write_text(md)
print("README.md written,", len(md), "chars")
