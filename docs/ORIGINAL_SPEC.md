# BEHAVIOR-PROBE — Virtual Student Benchmark MVP

This package uses **no LLM to impersonate students**. A deterministic Python
column-subtraction simulator produces reproducible task instances.

## Important distinction

This is an **offline benchmark generator, trusted oracle, and grader prototype**.
It is **not yet integrated with Valkyrie**. In a proper Agent benchmark, the
Agent sandbox must receive **only** `cases/public/Sxxx.json` and a limited
query tool. It must **never** see `behavior_probe.py`, `cases/private/`, hidden
answers, or the underlying rules. Run `start`, `probe`, and `grade` on a trusted
service, not from an agent-visible filesystem.

## Start with Python 3.10+ (no third-party dependencies)

```bash
python3 behavior_probe.py generate --root cases --n 20 --seed 20261114
python3 behavior_probe.py start --root cases --case S001 --budget 3 --session demo3
python3 behavior_probe.py probe --root cases --session demo3 --a 502 --b 178
```

Generated structure:

```
cases/
  manifest.json
  public/S001.json ... S020.json  # observation pairs + hidden test questions, no answers
  private/S001.json ... S020.json # hidden procedural rule + ground truth answers
  private/sessions/                # query budgets, questions, closed status
  private/reports/                 # grader outputs
```

To check the grader, score a **deliberately weak** arithmetic baseline:

```bash
python3 behavior_probe.py baseline --root cases --case S001 --out baseline.json
python3 behavior_probe.py start --root cases --case S001 --budget 0 --session baseline0
python3 behavior_probe.py grade --root cases --session baseline0 --submission baseline.json
```

After graded 0/3/10 sessions, export curve data using:

```bash
python3 behavior_probe.py summarize --root cases --out probe_curve.csv
```

`baseline.json` shows the expected submission schema:

```json
{
  "predictions": [
    {"id": "Q01", "answer": 123, "confidence": 0.85}
  ]
}
```

Include **all 40** IDs from `public/S001.json`. `answer` is an **integer**;
`confidence` is a probability from **0** to **1** that this exact answer
matches the *student's*, not the arithmetic correct, answer.

## Three benchmark metrics

1. **Primary: accuracy only on questions where the simulated student errs**.
   The agent does **not** know which evaluation questions are error cases.
   The remaining correct-answer cases are reported separately, not used as
   the primary score. Evaluations have equal wrong/right counts.
2. **Query efficiency:** number of probes used; compare the prediction
   accuracy under budgets **0, 3, and 10**, with separately initialized
   sessions and otherwise equal conditions. Do not reward asking zero
   questions while being inaccurate.
3. **Uncertainty / calibration:** each prediction carries confidence. On
   the error subset, report Brier score (lower better), five-bin expected
   calibration error, the accuracy and coverage of predictions with
   confidence >= 0.8, and the accuracy of lower-confidence predictions.

For 0/3/10 comparisons, use exactly the **same cases and evaluation
questions**, new session IDs, the same agent/model, and independent trials.
Never let the agent directly probe a held-out test question; the oracle
rejects these exact pairs.

## Error mechanisms

The simulator has several right-to-left column subtraction bugs, with
conditional triggers:
- subtract smaller digit from larger without borrowing;
- borrow ten but forget to decrement the neighboring column;
- write zero in a column where borrowing is required;
- fail to propagate a borrow through a zero.

For the first three, the mistake can occur at every borrow, only at the ones
position, only at the tens position, or if the next higher column is zero.
These mechanisms are **synthetic teaching hypotheses**, not a validated
sample of real students. Correct responses alone are intentionally not
enough to score highly. The test set includes 3-digit familiar and 4-digit
transfer problems, each split evenly between student-correct and
student-incorrect cases.

## Limitations / benchmark-design checks

- A deterministic answer given a rule is unique. A **hidden rule is not
  necessarily uniquely identifiable** from a short history. Score behavioral
  prediction rather than exact hidden labels.
- Probe budgets must be enforced in the evaluator (not by prompting the
  agent). The script persists usage per session for local testing.
- This CLI is a trusted-side proof of concept, not a production-safe remote
  endpoint. For Valkyrie, implement an authenticated query endpoint or a
  controlled agent tool with per-run budget accounting.
- The generator intentionally balances error/correct answers in hidden
  tests for metric stability. This makes a **curated diagnostic distribution**,
  not an estimate of real-world student error rates.
- Calibration needs enough examples per bin; 20 error cases per student are
  small. Aggregate across independent students and seeds for reliable curves.
- Do not claim that prediction on synthetic subtraction mistakes generalizes
  to real learners without external validation.
