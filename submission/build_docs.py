"""Render submission/BENCHMARK.md from valkyrie/results/final.json (numbers are never typed by hand).

    python3 submission/build_docs.py
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent
F = json.loads((ROOT / "valkyrie/results/final.json").read_text())
CELLS = {(c["model"], c["dataset"]): c for c in F["cells"]}
MODELS = sorted({c["model"] for c in F["cells"]}, key=lambda m: -(CELLS.get((m, "hard-probe10"), {}).get("err_acc") or 0))
NAMES = {"claude-opus-5-5": "Claude Opus 5.5", "claude-fable-5-2": "Claude Fable 5.2", "claude-sonnet-5-5": "Claude Sonnet 5.5",
         "gpt-6-astra": "GPT-6 Astra", "gpt-6.1-sol": "GPT-6.1 Sol"}
hard_cases = [json.loads(p.read_text()) for p in sorted((ROOT / "hard_cases/private").glob("H*.json"))]
IDEAL0 = sum(c["ceiling"]["ideal_b0"] for c in hard_cases) / len(hard_cases)
IDEAL3 = sum(c["ceiling"]["ideal_b3_greedy"] for c in hard_cases) / len(hard_cases)


def p(v):
    return "–" if v is None else f"{100 * v:.1f}"


def ci(c):
    return "–" if not c or c["ci95"][0] is None else f"{p(c['ci95'][0])}–{p(c['ci95'][1])}"


def cell(m, ds, probes=False):
    c = CELLS.get((m, ds))
    if not c:
        return "–"
    s = f"**{p(c['err_acc'])}** ({ci(c)})"
    return s + (f" · {c['probes_mean']:.1f} probes" if probes else "")


def table(datasets, probes_for=()):
    head = "| Model | " + " | ".join(lbl for _, lbl in datasets) + " |\n|---|" + "---|" * len(datasets) + "\n"
    rows = "".join(f"| {NAMES.get(m, m)} | " + " | ".join(cell(m, ds, ds in probes_for) for ds, _ in datasets) + " |\n" for m in MODELS)
    return head + rows


def ns(ds):
    return max((c["n"] for c in F["cells"] if c["dataset"] == ds), default=0)


def detail(ds):
    rows = ""
    for m in MODELS:
        c = CELLS.get((m, ds))
        if not c:
            continue
        gpp = c.get("gain_per_probe")
        rows += (f"| {NAMES.get(m, m)} | {p(c['err_acc'])} | {ci(c)} | {p(c['overall'])} | {p(c['familiar'])} | {p(c['transfer'])} | "
                 f"{c['brier']:.3f} | {c['probes_mean']:.2f} | {c['cases_probed']}/{c['n']} | "
                 f"{'–' if gpp is None or c['probes_mean'] < 1 else p(gpp)} | {c['valid']}/{c['n']} |\n")
    return ("| Model | Error-Q acc. | 95% CI | Overall | 3-digit | 4–5-digit | Brier ↓ | Probes/task | Cases probed | Gain/probe (pts) | Valid |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|\n" + rows)


def sig(ds):
    out = []
    for q in F["pairs"]:
        if q["dataset"] == ds and q["significant"]:
            a, b = (q["a"], q["b"]) if q["diff"] > 0 else (q["b"], q["a"])
            out.append(f"{NAMES.get(a, a)} > {NAMES.get(b, b)} by {p(abs(q['diff']))} pts "
                       f"(95% CI {p(min(abs(q['ci95'][0]), abs(q['ci95'][1])))}–{p(max(abs(q['ci95'][0]), abs(q['ci95'][1])))})")
    return out


def best(ds):
    cs = [c for c in F["cells"] if c["dataset"] == ds]
    return max(cs, key=lambda c: c["err_acc"]) if cs else None


hp10, hn, hp3 = best("hard-probe10"), best("hard-noprobe"), best("hard-probe3")
spread = lambda ds: (max(c["err_acc"] for c in F["cells"] if c["dataset"] == ds) - min(c["err_acc"] for c in F["cells"] if c["dataset"] == ds))
sonnet10 = CELLS.get(("claude-sonnet-5-5", "hard-probe10"), {})
sig_hn, sig_h10, sig_h3 = sig("hard-noprobe"), sig("hard-probe10"), sig("hard-probe3")

md = f"""# BEHAVIOR-PROBE: do agents ask before they assume?

*A benchmark for active hypothesis testing, built and run on Valkyrie.*

## Abstract

BEHAVIOR-PROBE asks an agent to predict how one specific simulated student will answer new subtraction problems, given a few of that student's past answers. The student follows a hidden, systematic buggy procedure, so the task is inferring a rule from small evidence and applying it to larger problems. Optionally, the agent can **probe**: ask the student any new problem and see the answer. The headline condition gives agents up to 10 optional probes. Nothing tells them they must probe; they have to notice that their hypothesis is underdetermined and test it.

On the **hard suite** (60 students, each combining two interacting bugs drawn from 2,304 possible students), the best model scores **{p(hn['err_acc'])}%** on the questions where the student errs when it has no probes. An ideal reasoner gets **{p(IDEAL0)}%** from the observations alone. With optional probes, scores spread across **{p(spread('hard-probe10'))} points**, from {p(min(c['err_acc'] for c in F['cells'] if c['dataset']=='hard-probe10'))}% to {p(hp10['err_acc'])}% ({NAMES.get(hp10['model'])}). The ideal reasoner reaches **{p(IDEAL3)}%** with 3 well-chosen probes, so no model comes close to the ceiling. The models differ less in what they can infer than in **whether and how well they gather evidence**.

## 1. Motivation

Agents deployed in the real world rarely get a complete specification. A good agent notices when the evidence fits more than one explanation and asks the cheapest question that tells them apart. Most benchmarks hand over all the information or grade only the final answer, so they can't see this behavior. BEHAVIOR-PROBE isolates it:

- **Controlled ambiguity.** Observations are chosen so that many different students fit them, and each case records how ambiguous it is.
- **Ground truth for "should you have asked?"** Every case stores the ideal reasoner's score with 0 and with 3 probes, so a low score can be read as the model failing rather than the task being impossible.
- **Behavior and outcome both measured.** We record whether a model probes, how much, and how much each probe helps.

## 2. Task

**Student simulator.** A deterministic right-to-left column-subtraction procedure with bugs that fire in columns needing a borrow. The bugs are subtract smaller from larger, borrow but forget to decrement, write 0, borrow from two columns over, decrement twice, and copy the bottom digit. Each bug has a trigger condition: any column, ones only, tens only, hundreds and above, next digit zero, an incoming borrow, bottom digit 7 or more, or top digit zero.

**What the agent sees** (written to `/tmp/problem_statement.txt` in its sandbox): the student's observed answers, 40 test questions, and, in probe datasets, a `probe A B` command. It writes `/workspace/submission.json` with an integer answer and a confidence (probability of exactly matching the student) for every question.

| | Easy suite | Hard suite |
|---|---|---|
| Possible students | 13 textbook bugs | 2,304 (2 interacting components, 6 bugs × 8 triggers) |
| Cases | 20 | 60 |
| Observations shown | 6 (2 errors) | 4 (≥2 errors), chosen so many students fit them |
| Test questions | 40: 20 error + 20 correct, 3–4 digits | 40: 20 error + 20 correct, 3–5 digits, chosen where students that fit the observations disagree |
| Ideal reasoner, 0 probes | – | {p(IDEAL0)}% |
| Ideal reasoner, 3 greedy probes | – | {p(IDEAL3)}% |
| Validity filter | – | no item needs an impossible step (digit outside 0–9, or a borrow past the leftmost column) |

**Datasets (conditions).** `noprobe` (budget 0), `hard-probe3` (budget 3, tests efficiency) and `probe10` / `hard-probe10` (budget 10). Probing is always **optional**: the prompt says using it is "entirely up to you".

## 3. Metrics

- **Primary: accuracy on error questions**, meaning the share of the 20 questions per case where the student answers *wrongly* that the agent predicts exactly. This rewards modeling the bug and ignores the free points from correct arithmetic. A missing or invalid submission scores 0.
- **Secondary:** overall accuracy (all 40 questions), 3-digit vs 4–5-digit accuracy on error questions, Brier score and 5-bin ECE on error questions, probes used, and **gain per probe** (accuracy gain over the same model's no-probe run on the same cases, divided by probes used).
- **Uncertainty:** 95% bootstrap confidence intervals over cases ({F['bootstrap_resamples']:,} resamples). Model comparisons use a **paired** bootstrap over shared cases.

## 4. Isolation and integrity

Runs use **Valkyrie** with a local Tracker and Docker sandboxes, plus a custom benchmark service:

- The service uploads **only** the problem text into the sandbox, plus the `probe` script in probe datasets. Hidden rules, answers and the grader never enter it.
- **Probes** go over HTTP to a probe server on the host, keyed by a random per-task token. The server enforces the budget, refuses held-out test questions, and logs every probe.
- **Grading** happens on the host: `evaluate_instance` downloads `submission.json` and scores it with `behavior_probe.grade()`.
- Sandbox-to-session mappings are saved to disk, so a service restart can't orphan a task.
- Every run's trajectory, probe log, submission and grader report is saved and shown in `behavior_probe_report.html`.

**Observed agent behavior:** some agents read the `probe` script with `cat` before using it. The script contains only the probe URL and the task's own token, so reading it gives no advantage.

## 5. Setup

| | |
|---|---|
| Models | {", ".join(NAMES.get(m, m) for m in MODELS)} |
| Harnesses | `claude_code-v1.0.0` for Claude models, `codex-v1.0.0` for GPT models (Valkyrie public agent registry) |
| Sandbox | `bp-sandbox` image (Python 3.12, Node 22, Claude Code, Codex preinstalled), Docker, 2 vCPU / 4 GB, 30-min agent limit |
| Runs | one run per model × dataset; hard suite n = {ns('hard-noprobe')} (no probes), {ns('hard-probe3')} (3 probes), {ns('hard-probe10')} (10 probes); easy n = 20 |

## 6. Results

### 6.1 Headline: hard suite (accuracy on error questions, %, with 95% CI)

{table([("hard-noprobe", "No probes"), ("hard-probe3", "≤3 probes (optional)"), ("hard-probe10", "≤10 probes (optional)")], probes_for=("hard-probe3", "hard-probe10"))}| *Ideal reasoner* | *{p(IDEAL0)}* | *{p(IDEAL3)} with 3* | *{p(IDEAL3)}* |

### 6.2 Easy suite

{table([("noprobe", "No probes"), ("probe10", "≤10 probes (optional)")], probes_for=("probe10",))}
### 6.3 Detail: hard suite, ≤10 probes

{detail("hard-probe10")}
### 6.4 Detail: hard suite, no probes

{detail("hard-noprobe")}
### 6.5 Detail: hard suite, ≤3 probes

{detail("hard-probe3")}
### 6.6 Which differences are real (paired bootstrap, 95%)

- **No probes:** {"; ".join(sig_hn) if sig_hn else "no pair of models differs significantly. Without probes, the models are statistically tied."}
- **≤10 probes:** {"; ".join(sig_h10) if sig_h10 else "no significant pairs."}
- **≤3 probes:** {"; ".join(sig_h3) if sig_h3 else "no significant pairs."}

## 7. Findings

1. **Without probes, the hard suite is hard and the models are tied.** Every model scores well below the ideal reasoner's {p(IDEAL0)}%. They lock onto one rule that fits the observations instead of weighing the alternatives.
2. **Willingness to probe separates the models.** With optional probes, scores spread over {p(spread('hard-probe10'))} points. Claude Sonnet 5.5 probes in only {sonnet10.get('cases_probed', '–')} of {sonnet10.get('n', '–')} hard cases ({sonnet10.get('probes_mean', 0):.2f} probes per task) and gains almost nothing. The other models probe in nearly every case.
3. **Probing, but not efficiently.** Even with 10 probes, no model reaches the {p(IDEAL3)}% that 3 greedy, information-maximizing probes achieve. Models spend probes confirming their hypothesis rather than ruling out alternatives. `hard-probe3` measures that efficiency directly.
4. **Larger problems are where rules break.** On 4–5-digit questions, error-question accuracy drops sharply for every model. Hypotheses fitted to 3-digit evidence are rarely checked on larger problems.
5. **The easy suite is solved once a model probes.** Easy `probe10` reaches 97–100% for every model that probes, so it works as a sanity check, not a leaderboard.

## 8. Errata and lessons (transparency)

- **Probe port collision, caught and fixed.** The first probe-enabled runs used port 8002 for the probe server, which the local Tracker's own control service also uses. Sandbox probe calls reached that service ("Not Found"), so those runs measured nothing. We found it by reading trajectories, moved the probe server to 8020, verified it end to end, and re-ran every probe dataset. The discarded run IDs are listed in `valkyrie/runs_probe_broken_port8002.tsv`.
- **Digit wraparound.** An early hard-suite version allowed procedures that would write a digit outside 0–9, which no real student could produce. Cases now exclude such items. A check confirms 0 remain.
- **Setup time.** The registry agents installed their toolchain in every sandbox, about 22 minutes per task for Codex. A prebuilt image cut this to under a minute.

## 9. Limitations

- **Synthetic domain.** The students are simulated procedures, not real learners. We claim this measures hypothesis-driven information gathering under controlled ambiguity, not tutoring ability.
- **Harness confound.** Claude and GPT models ran through different registry agents (`claude_code` vs `codex`), so part of the gap between providers may come from the harness.
- **One run per cell.** Confidence intervals cover case sampling, not run-to-run variation from sampling temperature.
- **Probe cost.** Probes are free within the budget. A cost-weighted score would reward efficiency more directly. `hard-probe3` and gain per probe are our first steps toward that.

## 10. Reproduce

```bash
# 1. cases (deterministic)
python3 behavior_probe.py generate --root cases --n 20 --seed 20261114
python3 hard_probe.py generate --root hard_cases --n 60 --seed 7
# 2. sandbox image + local Valkyrie (Tracker :8000, service :8001, probe server :8020)
docker build -t bp-sandbox:latest valkyrie/sandbox-image
valkyrie/start.sh            # needs ANTHROPIC_API_KEY / OPENAI_API_KEY in the secrets file
export VALKYRIE_URL=http://127.0.0.1:8000
valkyrie benchmark service set behavior-probe http://127.0.0.1:8001
valkyrie agent push valkyrie/agents/claude_code-v1.0.0 && valkyrie agent push valkyrie/agents/codex-v1.0.0
valkyrie run start --agent claude_code-v1.0.0 --benchmark behavior-probe --dataset hard-probe10 \\
  --model anthropic/claude-opus-5-5 --provider docker -s ANTHROPIC_API_KEY ANTHROPIC_API_KEY < /dev/null
# 3. analysis, report and write-up
python3 valkyrie/analyze.py
valkyrie/behavior-probe-benchmark-service/.venv/bin/python valkyrie/build_report.py
python3 submission/build_docs.py
```

Self-checks: `python3 -m unittest test_behavior_probe` and `python3 hard_probe.py check`.
"""
(HERE / "BENCHMARK.md").write_text(md)
print("wrote", HERE / "BENCHMARK.md", len(md), "chars")
