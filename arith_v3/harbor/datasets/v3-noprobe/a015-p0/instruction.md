# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (× only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 70 × 6 | 420 |
| 103 × 66 | 6798 |
| 966 × 6 | 5796 |
| 24 × 30 | 600 |
| 518 × 36 | 18888 |
| 994 × 10 | 9900 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 84 × 40 |
| Q02 | 940 × 23 |
| Q03 | 715 × 28 |
| Q04 | 808 × 35 |
| Q05 | 705 × 4 |
| Q06 | 230 × 6 |
| Q07 | 28 × 22 |
| Q08 | 371 × 5 |
| Q09 | 727 × 2 |
| Q10 | 50 × 10 |
| Q11 | 828 × 7 |
| Q12 | 71 × 18 |
| Q13 | 72 × 60 |
| Q14 | 524 × 61 |
| Q15 | 813 × 44 |
| Q16 | 560 × 8 |
| Q17 | 959 × 3 |
| Q18 | 881 × 22 |
| Q19 | 70 × 34 |
| Q20 | 54 × 10 |
| Q21 | 887 × 29 |
| Q22 | 138 × 5 |
| Q23 | 76 × 64 |
| Q24 | 98 × 98 |
| Q25 | 69 × 4 |
| Q26 | 382 × 2 |
| Q27 | 11 × 47 |
| Q28 | 20 × 69 |
| Q29 | 623 × 96 |
| Q30 | 344 × 10 |
| Q31 | 985 × 71 |
| Q32 | 595 × 89 |
| Q33 | 72 × 5 |
| Q34 | 471 × 67 |
| Q35 | 12 × 4 |
| Q36 | 94 × 83 |
| Q37 | 71 × 27 |
| Q38 | 11 × 56 |
| Q39 | 597 × 4 |
| Q40 | 347 × 24 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
