# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 23527 ÷ 7 | 3361 |
| 34396 + 67263 | 101659 |
| 409 − 360 | 39 |
| 6573 − 3976 | 2597 |
| 561 × 11 | 6171 |
| 64216 ÷ 2 | 32103 |
| 52307 + 1 | 52318 |
| 81 × 33 | 1573 |

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
| Q01 | 133 − 84 |
| Q02 | 953 × 77 |
| Q03 | 33054 + 4 |
| Q04 | 30604 + 22139 |
| Q05 | 6002 + 3243 |
| Q06 | 90264 + 7 |
| Q07 | 620 + 5 |
| Q08 | 12008 ÷ 8 |
| Q09 | 6446 − 6062 |
| Q10 | 246 − 10 |
| Q11 | 133986 ÷ 6 |
| Q12 | 45029 + 6 |
| Q13 | 31 × 12 |
| Q14 | 2771 + 2009 |
| Q15 | 99 × 10 |
| Q16 | 1830 + 4 |
| Q17 | 100 × 7 |
| Q18 | 24 × 21 |
| Q19 | 45197 − 44583 |
| Q20 | 76199 + 35009 |
| Q21 | 617 × 46 |
| Q22 | 2580 ÷ 6 |
| Q23 | 864 ÷ 8 |
| Q24 | 1872 ÷ 8 |
| Q25 | 9046 + 2 |
| Q26 | 8684 ÷ 4 |
| Q27 | 176790 ÷ 2 |
| Q28 | 5204 − 3977 |
| Q29 | 26539 + 20105 |
| Q30 | 568 × 42 |
| Q31 | 39530 + 4 |
| Q32 | 8160 + 5 |
| Q33 | 684 + 600 |
| Q34 | 874 ÷ 2 |
| Q35 | 271736 ÷ 8 |
| Q36 | 454 × 89 |
| Q37 | 912 − 669 |
| Q38 | 10764 + 86202 |
| Q39 | 75 × 10 |
| Q40 | 9128 − 8911 |
| Q41 | 12 × 3 |
| Q42 | 552 − 257 |
| Q43 | 5376 ÷ 6 |
| Q44 | 6175 − 1288 |
| Q45 | 27600 ÷ 6 |
| Q46 | 6219 × 5 |
| Q47 | 6456 ÷ 6 |
| Q48 | 2436 ÷ 6 |
| Q49 | 1194 ÷ 2 |
| Q50 | 363224 ÷ 8 |
| Q51 | 1661 − 481 |
| Q52 | 30579 − 12606 |
| Q53 | 93353 − 25368 |
| Q54 | 519 × 3 |
| Q55 | 1100 + 1614 |
| Q56 | 95532 − 24371 |
| Q57 | 16152 ÷ 8 |
| Q58 | 8187 × 36 |
| Q59 | 3680 ÷ 4 |
| Q60 | 9372 × 29 |
| Q61 | 922 − 338 |
| Q62 | 90978 + 79707 |
| Q63 | 90390 − 3308 |
| Q64 | 1560 ÷ 4 |
| Q65 | 223 × 32 |
| Q66 | 87799 − 87182 |
| Q67 | 179442 ÷ 6 |
| Q68 | 87062 + 1 |
| Q69 | 10 × 33 |
| Q70 | 81669 − 69079 |
| Q71 | 7669 × 69 |
| Q72 | 10898 ÷ 2 |
| Q73 | 2300 + 3707 |
| Q74 | 310 − 53 |
| Q75 | 634 − 255 |
| Q76 | 8989 × 9 |
| Q77 | 11 × 14 |
| Q78 | 93 × 11 |
| Q79 | 2102 − 86 |
| Q80 | 3091 + 6 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
