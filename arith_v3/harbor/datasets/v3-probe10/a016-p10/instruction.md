# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (÷ only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 4008 ÷ 2 | 24 |
| 420 ÷ 4 | 15 |
| 5425 ÷ 7 | 775 |
| 23898 ÷ 3 | 7966 |

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
| Q01 | 141215 ÷ 5 |
| Q02 | 154514 ÷ 2 |
| Q03 | 1618 ÷ 2 |
| Q04 | 14115 ÷ 3 |
| Q05 | 117416 ÷ 2 |
| Q06 | 7412 ÷ 4 |
| Q07 | 27111 ÷ 3 |
| Q08 | 162612 ÷ 2 |
| Q09 | 16513 ÷ 7 |
| Q10 | 40215 ÷ 7 |
| Q11 | 1719 ÷ 9 |
| Q12 | 95115 ÷ 5 |
| Q13 | 1818 ÷ 6 |
| Q14 | 1617 ÷ 7 |
| Q15 | 15021 ÷ 3 |
| Q16 | 13212 ÷ 4 |
| Q17 | 514 ÷ 2 |
| Q18 | 14416 ÷ 4 |
| Q19 | 21615 ÷ 5 |
| Q20 | 4116 ÷ 4 |
| Q21 | 77310 ÷ 9 |
| Q22 | 159612 ÷ 4 |
| Q23 | 641816 ÷ 7 |
| Q24 | 195310 ÷ 5 |
| Q25 | 495711 ÷ 9 |
| Q26 | 1318 ÷ 2 |
| Q27 | 2112 ÷ 6 |
| Q28 | 1715 ÷ 5 |
| Q29 | 140410 ÷ 5 |
| Q30 | 1416 ÷ 2 |
| Q31 | 143919 ÷ 3 |
| Q32 | 412281 ÷ 9 |
| Q33 | 1414 ÷ 2 |
| Q34 | 128511 ÷ 3 |
| Q35 | 2112 ÷ 8 |
| Q36 | 141714 ÷ 9 |
| Q37 | 71514 ÷ 9 |
| Q38 | 50110 ÷ 5 |
| Q39 | 374115 ÷ 5 |
| Q40 | 347112 ÷ 8 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
