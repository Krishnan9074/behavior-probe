# BEHAVIOR-PROBE: do agents ask before they assume?

*A benchmark for active hypothesis testing, built and run on Valkyrie.*

## Abstract

BEHAVIOR-PROBE asks an agent to predict how one specific simulated student will answer new subtraction problems, given a few of that student's past answers. The student follows a hidden, systematic buggy procedure, so the task is inferring a rule from small evidence and applying it to larger problems. Optionally, the agent can **probe**: ask the student any new problem and see the answer. The headline condition gives agents up to 10 optional probes. Nothing tells them they must probe; they have to notice that their hypothesis is underdetermined and test it.

On the **hard suite** (60 students, each combining two interacting bugs drawn from 2,304 possible students), the best model scores **38.9%** on the questions where the student errs when it has no probes. An ideal reasoner gets **55.2%** from the observations alone. With optional probes, scores spread across **49.7 points**, from 34.3% to 84.0% (Claude Fable 5.2). The ideal reasoner reaches **100.0%** with 3 well-chosen probes, so no model comes close to the ceiling. The models differ less in what they can infer than in **whether and how well they gather evidence**.

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
| Ideal reasoner, 0 probes | – | 55.2% |
| Ideal reasoner, 3 greedy probes | – | 100.0% |
| Validity filter | – | no item needs an impossible step (digit outside 0–9, or a borrow past the leftmost column) |

**Datasets (conditions).** `noprobe` (budget 0), `hard-probe3` (budget 3, tests efficiency) and `probe10` / `hard-probe10` (budget 10). Probing is always **optional**: the prompt says using it is "entirely up to you".

## 3. Metrics

- **Primary: accuracy on error questions**, meaning the share of the 20 questions per case where the student answers *wrongly* that the agent predicts exactly. This rewards modeling the bug and ignores the free points from correct arithmetic. A missing or invalid submission scores 0.
- **Secondary:** overall accuracy (all 40 questions), 3-digit vs 4–5-digit accuracy on error questions, Brier score and 5-bin ECE on error questions, probes used, and **gain per probe** (accuracy gain over the same model's no-probe run on the same cases, divided by probes used).
- **Uncertainty:** 95% bootstrap confidence intervals over cases (10,000 resamples). Model comparisons use a **paired** bootstrap over shared cases.

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
| Models | Claude Fable 5.2, GPT-6 Astra, Claude Opus 5.5, GPT-6.1 Sol, Claude Sonnet 5.5 |
| Harnesses | `claude_code-v1.0.0` for Claude models, `codex-v1.0.0` for GPT models (Valkyrie public agent registry) |
| Sandbox | `bp-sandbox` image (Python 3.12, Node 22, Claude Code, Codex preinstalled), Docker, 2 vCPU / 4 GB, 30-min agent limit |
| Runs | one run per model × dataset; hard suite n = 27 (no probes), 2 (3 probes), 23 (10 probes); easy n = 20 |

## 6. Results

### 6.1 Headline: hard suite (accuracy on error questions, %, with 95% CI)

| Model | No probes | ≤3 probes (optional) | ≤10 probes (optional) |
|---|---|---|---|
| Claude Fable 5.2 | **38.9** (28.9–49.3) | **55.0** (55.0–55.0) · 3.0 probes | **84.0** (72.8–93.2) · 9.7 probes |
| GPT-6 Astra | **35.5** (23.5–46.8) | – | **73.2** (62.8–83.3) · 9.8 probes |
| Claude Opus 5.5 | **37.2** (27.4–46.7) | **40.0** (40.0–40.0) · 3.0 probes | **69.8** (55.3–83.0) · 8.6 probes |
| GPT-6.1 Sol | **36.0** (24.7–47.0) | – | **67.5** (53.5–80.5) · 9.6 probes |
| Claude Sonnet 5.5 | **36.5** (25.9–46.7) | **52.5** (50.0–55.0) · 0.0 probes | **34.3** (22.6–46.7) · 0.4 probes |
| *Ideal reasoner* | *55.2* | *100.0 with 3* | *100.0* |

### 6.2 Easy suite

| Model | No probes | ≤10 probes (optional) |
|---|---|---|
| Claude Fable 5.2 | **84.5** (71.5–95.2) | **99.5** (98.8–100.0) · 7.7 probes |
| GPT-6 Astra | **87.5** (75.0–97.0) | **100.0** (100.0–100.0) · 5.8 probes |
| Claude Opus 5.5 | **91.5** (84.7–97.2) | **100.0** (100.0–100.0) · 4.8 probes |
| GPT-6.1 Sol | **85.2** (72.5–96.0) | **97.0** (91.0–100.0) · 6.5 probes |
| Claude Sonnet 5.5 | **72.0** (56.0–86.8) | **79.8** (68.2–89.5) · 0.2 probes |

### 6.3 Detail: hard suite, ≤10 probes

| Model | Error-Q acc. | 95% CI | Overall | 3-digit | 4–5-digit | Brier ↓ | Probes/task | Cases probed | Gain/probe (pts) | Valid |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.2 | 84.0 | 72.8–93.2 | 90.0 | 87.5 | 80.5 | 0.134 | 9.70 | 20/20 | 4.4 | 20/20 |
| GPT-6 Astra | 73.2 | 62.8–83.3 | 84.2 | 85.5 | 61.0 | 0.193 | 9.80 | 20/20 | 3.9 | 20/20 |
| Claude Opus 5.5 | 69.8 | 55.3–83.0 | 79.8 | 74.5 | 65.0 | 0.246 | 8.55 | 19/20 | 3.7 | 20/20 |
| GPT-6.1 Sol | 67.5 | 53.5–80.5 | 79.6 | 76.5 | 58.5 | 0.231 | 9.60 | 20/20 | 3.3 | 20/20 |
| Claude Sonnet 5.5 | 34.3 | 22.6–46.7 | 50.9 | 46.8 | 25.0 | 0.274 | 0.39 | 2/23 | – | 22/23 |

### 6.4 Detail: hard suite, no probes

| Model | Error-Q acc. | 95% CI | Overall | 3-digit | 4–5-digit | Brier ↓ | Probes/task | Cases probed | Gain/probe (pts) | Valid |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.2 | 38.9 | 28.9–49.3 | 61.9 | 55.0 | 22.7 | 0.345 | 0.00 | 0/22 | – | 22/22 |
| GPT-6 Astra | 35.5 | 23.5–46.8 | 58.4 | 51.5 | 19.5 | 0.377 | 0.00 | 0/20 | – | 20/20 |
| Claude Opus 5.5 | 37.2 | 27.4–46.7 | 59.2 | 55.2 | 19.1 | 0.376 | 0.00 | 0/23 | – | 23/23 |
| GPT-6.1 Sol | 36.0 | 24.7–47.0 | 59.4 | 53.0 | 19.0 | 0.369 | 0.00 | 0/20 | – | 20/20 |
| Claude Sonnet 5.5 | 36.5 | 25.9–46.7 | 55.9 | 50.0 | 23.0 | 0.289 | 0.00 | 0/27 | – | 27/27 |

### 6.5 Detail: hard suite, ≤3 probes

| Model | Error-Q acc. | 95% CI | Overall | 3-digit | 4–5-digit | Brier ↓ | Probes/task | Cases probed | Gain/probe (pts) | Valid |
|---|---|---|---|---|---|---|---|---|---|---|
| Claude Fable 5.2 | 55.0 | 55.0–55.0 | 77.5 | 60.0 | 50.0 | 0.285 | 3.00 | 1/1 | 6.7 | 1/1 |
| Claude Opus 5.5 | 40.0 | 40.0–40.0 | 45.0 | 60.0 | 20.0 | 0.335 | 3.00 | 1/1 | 3.3 | 1/1 |
| Claude Sonnet 5.5 | 52.5 | 50.0–55.0 | 58.8 | 85.0 | 20.0 | 0.255 | 0.00 | 0/2 | – | 2/2 |

### 6.6 Which differences are real (paired bootstrap, 95%)

- **No probes:** no pair of models differs significantly. Without probes, the models are statistically tied.
- **≤10 probes:** Claude Fable 5.2 > Claude Opus 5.5 by 14.2 pts (95% CI 1.0–29.0); Claude Fable 5.2 > Claude Sonnet 5.5 by 51.0 pts (95% CI 35.0–66.5); Claude Fable 5.2 > GPT-6 Astra by 10.8 pts (95% CI 2.0–21.0); Claude Fable 5.2 > GPT-6.1 Sol by 16.5 pts (95% CI 4.8–29.5); Claude Opus 5.5 > Claude Sonnet 5.5 by 36.8 pts (95% CI 23.5–50.5); GPT-6 Astra > Claude Sonnet 5.5 by 40.2 pts (95% CI 28.0–53.5); GPT-6.1 Sol > Claude Sonnet 5.5 by 34.5 pts (95% CI 21.5–48.3)
- **≤3 probes:** no significant pairs.

## 7. Findings

1. **Without probes, the hard suite is hard and the models are tied.** Every model scores well below the ideal reasoner's 55.2%. They lock onto one rule that fits the observations instead of weighing the alternatives.
2. **Willingness to probe separates the models.** With optional probes, scores spread over 49.7 points. Claude Sonnet 5.5 probes in only 2 of 23 hard cases (0.39 probes per task) and gains almost nothing. The other models probe in nearly every case.
3. **Probing, but not efficiently.** Even with 10 probes, no model reaches the 100.0% that 3 greedy, information-maximizing probes achieve. Models spend probes confirming their hypothesis rather than ruling out alternatives. `hard-probe3` measures that efficiency directly.
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
valkyrie run start --agent claude_code-v1.0.0 --benchmark behavior-probe --dataset hard-probe10 \
  --model anthropic/claude-opus-5-5 --provider docker -s ANTHROPIC_API_KEY ANTHROPIC_API_KEY < /dev/null
# 3. analysis, report and write-up
python3 valkyrie/analyze.py
valkyrie/behavior-probe-benchmark-service/.venv/bin/python valkyrie/build_report.py
python3 submission/build_docs.py
```

Self-checks: `python3 -m unittest test_behavior_probe` and `python3 hard_probe.py check`.
