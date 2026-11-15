# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

**Note:** there are no past answers for **−** (`sub`), but test questions include it.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 544 × 42 | 22848 |
| 48510 ÷ 5 | 9700 |
| 94804 + 60770 | 155574 |
| 73458 ÷ 7 | 10494 |

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
| Q01 | 258282 ÷ 9 |
| Q02 | 36265 + 16628 |
| Q03 | 68994 + 37297 |
| Q04 | 962 + 6 |
| Q05 | 90815 + 1 |
| Q06 | 711 × 77 |
| Q07 | 21 × 12 |
| Q08 | 695072 ÷ 8 |
| Q09 | 3549 × 3 |
| Q10 | 2103 + 4130 |
| Q11 | 8096 − 6378 |
| Q12 | 85 × 48 |
| Q13 | 97 × 3 |
| Q14 | 33 × 7 |
| Q15 | 87 × 41 |
| Q16 | 3606 ÷ 6 |
| Q17 | 49850 + 1 |
| Q18 | 736 + 64 |
| Q19 | 7574 + 5470 |
| Q20 | 856 − 550 |
| Q21 | 3240 ÷ 8 |
| Q22 | 379 × 5 |
| Q23 | 96878 − 77638 |
| Q24 | 78825 − 40504 |
| Q25 | 3691 × 82 |
| Q26 | 1105 × 4 |
| Q27 | 8199 − 5456 |
| Q28 | 340 − 226 |
| Q29 | 20858 + 38341 |
| Q30 | 831 − 252 |
| Q31 | 82086 + 4036 |
| Q32 | 68585 + 97966 |
| Q33 | 3907 − 3498 |
| Q34 | 1072 × 3 |
| Q35 | 12615 ÷ 3 |
| Q36 | 1540 ÷ 5 |
| Q37 | 180291 ÷ 3 |
| Q38 | 1428 ÷ 7 |
| Q39 | 539 + 549 |
| Q40 | 12985 ÷ 7 |
| Q41 | 2523 − 1736 |
| Q42 | 568 − 196 |
| Q43 | 1672 ÷ 8 |
| Q44 | 49525 ÷ 5 |
| Q45 | 471 − 162 |
| Q46 | 6527 + 3682 |
| Q47 | 1649 + 6618 |
| Q48 | 71243 − 36326 |
| Q49 | 629 × 9 |
| Q50 | 327 − 244 |
| Q51 | 4667 − 928 |
| Q52 | 290808 ÷ 4 |
| Q53 | 472 × 6 |
| Q54 | 1488 × 61 |
| Q55 | 17472 ÷ 2 |
| Q56 | 66798 + 19539 |
| Q57 | 30056 ÷ 8 |
| Q58 | 753 × 9 |
| Q59 | 1612 ÷ 2 |
| Q60 | 18842 + 8 |
| Q61 | 8491 − 3612 |
| Q62 | 72 × 46 |
| Q63 | 1336 × 23 |
| Q64 | 262 × 76 |
| Q65 | 9238 × 11 |
| Q66 | 807561 ÷ 9 |
| Q67 | 601 − 558 |
| Q68 | 435 + 411 |
| Q69 | 276 + 117 |
| Q70 | 3627 ÷ 9 |
| Q71 | 2238 − 671 |
| Q72 | 7278 + 9549 |
| Q73 | 5705 − 2965 |
| Q74 | 1461 × 23 |
| Q75 | 188525 ÷ 5 |
| Q76 | 55392 − 37794 |
| Q77 | 358 − 201 |
| Q78 | 72883 + 4 |
| Q79 | 279705 ÷ 3 |
| Q80 | 465237 ÷ 9 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
