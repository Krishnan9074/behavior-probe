# ARITH-PROBE v3 — Interactive Arithmetic Behavioral Inference

**A runnable, literature-informed, deterministic AI-agent benchmark prototype.**

This repository is a **trusted-side local pilot**, not a deployed Valkyrie
`BenchmarkService`. It supports Python 3.10+ using **only the standard library**.
There is no LLM student and no LLM judge.

## Downloads / separation of responsibilities

- **Full repository (benchmark owner ONLY)** includes simulator source, generated
  `cases/private/` hidden answers, generator, scoring, authenticated local API,
  an oracle reference, research taxonomy, tests, and sample task handoff.
- **Public task ZIP (agent ONLY)** includes `task.json` and `agent_prompt.txt`.
  Never give the full repository to a tested agent. Do not run the trusted
  simulator or any `cases/private/` files in an agent's sandbox.

## What is being tested?

The agent receives a few arithmetic problems and the answers given by an
unknown, rule-governed virtual student. It must predict exactly what that
student will answer on unseen questions, **not what the right mathematical
answer would be**. A query-budgeted probe interface lets the agent choose
additional arithmetic expressions and observe the student's answer.

The model is **not** asked to name or classify an educational error label.
Labels generate behavior privately, and can be used for offline stratification.

### Three levels

| Level | Name | Student and initial evidence | Held-out tests |
|---|---|---|---|
| 1 | Single-Operation Inference | Easy: one rule, 6 observations; Hard: two interacting rules, 4 intentionally ambiguous observations | 40 test expressions, 20 wrong / 20 right |
| 2 | Mixed-Operation Inference | One hidden rule per operation, 2 observations per operation (8 total), **shared** probe budget | 80 test expressions, 10 wrong + 10 right per operation |
| 3 | Cross-Operation Behavioral Inference | One **truly shared** digit-interpretation rule in all operations. Four initial observations in **three** operations; none from the specified target operation | 80 tests, 10 wrong + 10 right per operation; separately report transfer accuracy before target-operation probes |

Level 3 currently operationalizes **only** Wallace Type 4 (zero/one handling),
using two synthetic variants (`zero_as_one`, `one_as_zero`) and triggers.
It does not yet model all forms of shared cognitive behavior across operations.

The 20 included cases comprise **12 Level 1, 4 Level 2, and 4 Level 3** tasks.
Re-generation supports more cases. Each case has exact arithmetic outputs
and a fixed, reproducible random seed.

### Research-inspired error taxonomy

See [`RULES.md`](RULES.md): 12 selected **numbered** Wallace (1984) types
(W01, W02, W04, W06, W08, W09, W10, W11, W12, W13, W15, W16), plus
**EXTRA_SFL**, which Wallace additionally reports outside the original
17-item numbered list. All 13 categories are represented in the included
20-task dataset. There may be multiple executable rules under a label, and
one rule may have multiple trigger conditions. **No empirical claim is made
that the simulator reproduces actual student response frequencies.**

## 1. Run locally (Mac / Windows / Linux)

Unzip, then open a terminal in the project directory:

```bash
python3 --version
python3 -m unittest discover -s tests -v
python3 tools/validate_cases.py
```

Browse the public task only:

```bash
python3 benchmark.py show --case A002
```

Find specific tasks by level in `cases/manifest.json` (manifest is owner-side
metadata; the individual public task does **not** reveal hidden rules).

Regenerate the full dataset under a **new root** to avoid overwriting pilots:

```bash
python3 benchmark.py generate --root cases_new --seed 20261115 \
  --easy-per-op 2 --level2 4 --level3-per-op 1
```

## 2. Zero-probe model pilot

1. Send the agent **only** `examples/agent_level2_A001_public_only.zip` or
   `examples/agent_level3_A002_public_only.zip` (or export a different
   public task). The ZIP has `task.json` and `agent_prompt.txt` only.
2. Ask it for exactly the JSON predictions specified in the task, including
   a confidence probability in `[0, 1]` for every question.
3. Save the answer as `gpt_A002.json`, etc. All test questions must be present.
4. On the **benchmark owner's** machine, create a zero-probe session and grade:

```bash
python3 benchmark.py start --case A002 --budget 0 --session gpt_A002
python3 benchmark.py grade --session gpt_A002 --submission gpt_A002.json
```

The full file must never enter the evaluated agent's sandbox.

## 3. Interactive pilot and exact observed K100

On the **owner side**, create a session and give the agent access to the
mediated probe API or relay arithmetic probes manually:

```bash
python3 benchmark.py start --case A002 --budget 3 --session fable3
```

To measure an accuracy curve, the agent must submit an updated prediction file
**at k=0, and after every probe**. The submit endpoint saves snapshots, but
**does not reveal hidden test scores**:

```bash
python3 benchmark.py submit --session fable3 --submission pred_at_0.json
python3 benchmark.py probe --session fable3 --op sub --a 502 --b 178
python3 benchmark.py submit --session fable3 --submission pred_at_1.json
# ... repeat until the agent finishes ...
python3 benchmark.py grade --session fable3
```

The probe is a **structured arithmetic query**, never a natural-language
question: e.g. `{ "op":"mul", "a":234, "b":16 }` or `502 - 178`.
The student replies with a **single integer**. Exact held-out test expressions
cannot be probed. For division, the original expression must divide exactly;
zero divisors are rejected. Other operations allow zero operands.

Each model should get an independent, clean session. Never feed the agent
hidden test correctness or grader results during an interactive run.

### Optional local HTTP API

The agent may call a tool-mediated endpoint if its harness has network access.
**Never expose this server on a public interface; bind to 127.0.0.1 only.**

```bash
python3 benchmark.py serve --host 127.0.0.1 --port 8787
```

`start` returns a per-session `api_token`. Supply it via a harness secret or
Bearer authentication, not as benchmark content. Endpoints:

- `GET /task?session=fable3` — public task, used/remaining budget.
- `POST /probe?session=fable3` with `{"op":"sub","a":502,"b":178}`.
- `POST /snapshot?session=fable3` with the submission JSON.

All endpoints require `Authorization: Bearer <session token>`.
Snapshots do not disclose any hidden score. Note that the HTTP server is a
**local testing utility**, not a production-hardened network service.

If using Fable/Claude Code/Codex in a **different sandbox**, forward only the
public task + a narrowly scoped probe tool; do **not** let it read the owner
machine's full project files.

## 4. Exact scoring

**Headline score (per task):** among the 20 (Level 1) or 40 (Level 2/3)
held-out expressions that the student actually gets wrong, how often did the
agent predict the **exact integer student response**?

Additional metrics:

- **Total accuracy**: same exact-match metric across all 40/80 test expressions.
- **Per-operation error accuracy**: exact-match percentage on wrong-answer
  expressions, separately for `add`, `sub`, `mul`, and `div`.
- **Macro error accuracy**: mean of the per-operation error accuracies for
  operations in that task. For Levels 2/3 the test sets are balanced (10 wrong
  problems in each operation), so micro and macro coincide on each task.
- **Probe curve**: error-case accuracy at every **submitted** probe count `k`.
- **K100_error_observed**: first saved snapshot with all error cases correct.
  **K100_all_observed**: first with **all test answers** correct (strict).
  `K95_error_observed`: first with at least 95% error-case accuracy.
  If never achieved, these values are `null`, not `budget+1`.
- **Confidence calibration**: confidence is the agent's subjective probability
  that the predicted **student answer** is an exact match. The grader computes
  Brier score (`mean((confidence - correct_indicator)^2)`), five-bin expected
  calibration error (ECE), and error rate/coverage for confidence >= 0.90.
  Metrics are reported on all test questions **and** wrong-answer questions.
  Brier and ECE are lower-is-better; Brier is not a pure calibration metric.
- **Cross-operation transfer (L3)**: target-operation wrong-answer accuracy
  **only if no probe of that target operation has yet been made**. Otherwise
  transfer-only accuracy is `null` and `transfer_contaminated=true`.
- **Oracle reference**: uniform voting among all compatible models in the
  declared finite hypothesis family. It separates underdetermined evidence
  from some failures to use evidence. **It is not a universal score upper bound,
  theoretical minimal-query oracle, nor an empirical prior over children.**

**Malformed, omitted, duplicate-ID, non-integer, or out-of-range-confidence
submissions score 0** on that snapshot. No partial credit. A snapshot is
valid only if all questions are answered.

### Example JSON submission

```json
{
  "predictions": [
    {"id": "Q01", "answer": 339, "confidence": 0.92},
    {"id": "Q02", "answer": 101, "confidence": 0.65}
  ]
}
```

The actual submission must contain **all** IDs from `task.json`; this two-row
fragment shows the schema only.

## 5. Reports, oracle and public-only handoff

```bash
python3 benchmark.py baseline --case A002 --out examples/math_A002.json
python3 benchmark.py start --case A002 --budget 0 --session oracle_check
python3 benchmark.py oracle --session oracle_check
python3 benchmark.py summarize --out probe_curve.csv
python3 benchmark.py export --case A002 --out public_only_A002.zip
```

`cases/private/reports/*.json` contains score timelines and K100. `summarize`
exports a CSV for drawing an actual accuracy–probe curve.

## 6. Scientific / evaluation caveats

1. Wallace (1984) compiled **17 types across four operations**, drawing on
   earlier research; they are broad diagnostic categories, not 17 ready-made
   computational programs. The paper also reports smaller-from-larger as an
   additional, unnumbered error type. See `RULES.md`.
2. The simulated error mechanisms and trigger combinations are explicitly
   **engineering operationalizations**; we have no empirical validation that
   their prevalence or combination matches real students.
3. Balancing tests to exactly half wrong answers is a deliberate scoring
   decision, **not** a population statistic. The held-out questions may be
   adversarially discriminative among models consistent with the observations.
4. When changing the rule pool, regenerate all cases and re-run all baseline
   agents. Historical Fable results on an earlier version are **not directly
   comparable** to v3 scores.
5. K100 is **the earliest observed perfect snapshot**, not a proof that the
   agent could not have succeeded with fewer queries. The hidden test set is
   finite; a perfect score is not a proof of exact rule recovery.
6. Cross-operation transfer is currently a narrow **synthetic** proof of
   concept for shared zero/one misinterpretation, not a validated model of
   cognitive generalization.
7. **Not yet a deployed Valkyrie benchmark service.** Integrating an isolated
   interactive tool endpoint into the relevant harness is still required for
   fully automated, secure agent runs.

## Citation / provenance

Wallace, Catherine C. (1984). *A Comparison of Computational Error Patterns
for Grades 3, 5 and 8.* University of North Florida master's thesis.
https://digitalcommons.unf.edu/etd/59/

For the original arithmetic bug modeling tradition, see Brown & Burton
(1978), referenced within the thesis. We **do not** claim direct validation
by either study of our exact Python simulator.
