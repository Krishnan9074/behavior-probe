# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (+ only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 16755 + 51546 | 68301 |
| 5746 + 6 | 11752 |
| 777 + 4 | 1181 |
| 342 + 654 | 996 |

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
| Q01 | 9702 + 9640 |
| Q02 | 9203 + 6160 |
| Q03 | 64413 + 37130 |
| Q04 | 53800 + 60922 |
| Q05 | 2709 + 5110 |
| Q06 | 58600 + 89851 |
| Q07 | 49508 + 22940 |
| Q08 | 41001 + 71550 |
| Q09 | 601 + 940 |
| Q10 | 2901 + 6880 |
| Q11 | 39200 + 11085 |
| Q12 | 9210 + 9208 |
| Q13 | 75814 + 80191 |
| Q14 | 410 + 661 |
| Q15 | 761 + 210 |
| Q16 | 39200 + 87968 |
| Q17 | 210 + 167 |
| Q18 | 1811 + 309 |
| Q19 | 58715 + 11970 |
| Q20 | 51418 + 30231 |
| Q21 | 410 + 867 |
| Q22 | 21001 + 75081 |
| Q23 | 17110 + 6720 |
| Q24 | 6700 + 2314 |
| Q25 | 93580 + 38001 |
| Q26 | 90817 + 53660 |
| Q27 | 76711 + 90479 |
| Q28 | 607 + 880 |
| Q29 | 94612 + 2610 |
| Q30 | 3210 + 539 |
| Q31 | 9021 + 7114 |
| Q32 | 86000 + 76027 |
| Q33 | 8715 + 8650 |
| Q34 | 80204 + 1 |
| Q35 | 4018 + 6221 |
| Q36 | 5100 + 1161 |
| Q37 | 53770 + 20771 |
| Q38 | 70160 + 23612 |
| Q39 | 21215 + 64170 |
| Q40 | 92040 + 57751 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
