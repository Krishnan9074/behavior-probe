# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (× only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 1922 × 42 | 11532 |
| 294 × 2 | 588 |
| 7481 × 7 | 52367 |
| 589 × 45 | 5301 |

## Optional tool

You may run `probe OP A B` (OP is `add`, `sub`, `mul` or `div`) to see this student's integer
answer to a new problem, e.g. `probe sub 502 178`. Operands are integers 0 to 1,000,000; for `sub`
A ≥ B; for `div` B divides A exactly and B > 0. You cannot probe the test questions. You can use
it up to 10 times. Using it is entirely up to you.

To record your progress, run `snapshot` (it sends `/workspace/submission.json`) once before your
first probe and again after each probe. It stores your predictions and never shows you a score.

## Test questions

| id | Problem |
|---|---|
| Q01 | 400 × 9 |
| Q02 | 5300 × 62 |
| Q03 | 5915 × 3 |
| Q04 | 16 × 7 |
| Q05 | 14 × 5 |
| Q06 | 900 × 3 |
| Q07 | 5700 × 5 |
| Q08 | 8411 × 5 |
| Q09 | 19 × 7 |
| Q10 | 213 × 2 |
| Q11 | 500 × 85 |
| Q12 | 4812 × 5 |
| Q13 | 7010 × 79 |
| Q14 | 5400 × 4 |
| Q15 | 612 × 9 |
| Q16 | 3805 × 70 |
| Q17 | 5200 × 5 |
| Q18 | 7800 × 32 |
| Q19 | 4300 × 4 |
| Q20 | 6200 × 14 |
| Q21 | 11 × 2 |
| Q22 | 9615 × 2 |
| Q23 | 6500 × 5 |
| Q24 | 6009 × 80 |
| Q25 | 2319 × 3 |
| Q26 | 901 × 90 |
| Q27 | 5415 × 7 |
| Q28 | 7400 × 30 |
| Q29 | 19 × 5 |
| Q30 | 711 × 4 |
| Q31 | 504 × 20 |
| Q32 | 3200 × 55 |
| Q33 | 215 × 5 |
| Q34 | 2700 × 75 |
| Q35 | 9919 × 9 |
| Q36 | 316 × 7 |
| Q37 | 13 × 2 |
| Q38 | 4513 × 3 |
| Q39 | 5600 × 7 |
| Q40 | 6912 × 7 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
