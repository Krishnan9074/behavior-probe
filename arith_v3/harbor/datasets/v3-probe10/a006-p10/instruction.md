# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (+ only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 2517 + 2 | 2519 |
| 801 + 574 | 1375 |
| 1736 + 3370 | 410106 |
| 4050 + 9491 | 134141 |
| 2936 + 4219 | 611415 |
| 670 + 5 | 675 |

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
| Q01 | 513 + 566 |
| Q02 | 597 + 587 |
| Q03 | 256 + 9 |
| Q04 | 152 + 946 |
| Q05 | 474 + 370 |
| Q06 | 3400 + 9588 |
| Q07 | 1111 + 7854 |
| Q08 | 165 + 711 |
| Q09 | 7774 + 224 |
| Q10 | 622 + 888 |
| Q11 | 355 + 483 |
| Q12 | 9589 + 9 |
| Q13 | 9902 + 7 |
| Q14 | 1503 + 5 |
| Q15 | 4130 + 6 |
| Q16 | 979 + 544 |
| Q17 | 5226 + 7222 |
| Q18 | 9510 + 1 |
| Q19 | 5921 + 6665 |
| Q20 | 6017 + 2423 |
| Q21 | 9987 + 7 |
| Q22 | 2688 + 1 |
| Q23 | 746 + 256 |
| Q24 | 6317 + 483 |
| Q25 | 481 + 191 |
| Q26 | 205 + 165 |
| Q27 | 252 + 767 |
| Q28 | 935 + 861 |
| Q29 | 846 + 361 |
| Q30 | 281 + 4 |
| Q31 | 4155 + 2 |
| Q32 | 287 + 74 |
| Q33 | 4621 + 7 |
| Q34 | 2674 + 9709 |
| Q35 | 445 + 2 |
| Q36 | 8022 + 4 |
| Q37 | 350 + 921 |
| Q38 | 817 + 770 |
| Q39 | 5146 + 5186 |
| Q40 | 7106 + 397 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
