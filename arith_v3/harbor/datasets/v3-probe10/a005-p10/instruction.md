# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (× only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 303 × 10 | 3030 |
| 346 × 28 | 8478 |
| 36 × 35 | 1050 |
| 23 × 22 | 506 |
| 22 × 2 | 44 |
| 98 × 95 | 8100 |

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
| Q01 | 852 × 4 |
| Q02 | 12 × 2 |
| Q03 | 10 × 9 |
| Q04 | 99 × 8 |
| Q05 | 10 × 65 |
| Q06 | 88 × 43 |
| Q07 | 177 × 2 |
| Q08 | 905 × 7 |
| Q09 | 193 × 6 |
| Q10 | 77 × 82 |
| Q11 | 34 × 2 |
| Q12 | 678 × 6 |
| Q13 | 770 × 94 |
| Q14 | 75 × 4 |
| Q15 | 23 × 31 |
| Q16 | 10 × 43 |
| Q17 | 448 × 34 |
| Q18 | 11 × 97 |
| Q19 | 15 × 10 |
| Q20 | 19 × 31 |
| Q21 | 424 × 11 |
| Q22 | 112 × 2 |
| Q23 | 11 × 8 |
| Q24 | 20 × 4 |
| Q25 | 117 × 83 |
| Q26 | 13 × 2 |
| Q27 | 59 × 13 |
| Q28 | 12 × 3 |
| Q29 | 100 × 42 |
| Q30 | 404 × 20 |
| Q31 | 727 × 8 |
| Q32 | 30 × 2 |
| Q33 | 55 × 85 |
| Q34 | 80 × 9 |
| Q35 | 497 × 11 |
| Q36 | 915 × 11 |
| Q37 | 941 × 9 |
| Q38 | 391 × 50 |
| Q39 | 27 × 10 |
| Q40 | 723 × 9 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
