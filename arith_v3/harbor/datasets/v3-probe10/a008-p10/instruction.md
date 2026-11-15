# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

**Note:** there are no past answers for **×** (`mul`), but test questions include it.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 3312 ÷ 4 | 825 |
| 333 − 232 | 101 |
| 630 ÷ 6 | 105 |
| 263 + 526 | 789 |

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
| Q01 | 873 × 28 |
| Q02 | 231 × 69 |
| Q03 | 10470 ÷ 5 |
| Q04 | 9631 − 7917 |
| Q05 | 1920 + 8253 |
| Q06 | 47196 − 19510 |
| Q07 | 403 + 9 |
| Q08 | 626 − 384 |
| Q09 | 112614 ÷ 3 |
| Q10 | 73689 + 68325 |
| Q11 | 946 − 355 |
| Q12 | 8127 ÷ 9 |
| Q13 | 4136 × 53 |
| Q14 | 89634 − 64193 |
| Q15 | 1402 × 49 |
| Q16 | 1129 + 936 |
| Q17 | 756 − 66 |
| Q18 | 55489 + 39531 |
| Q19 | 4134 + 2011 |
| Q20 | 211 × 51 |
| Q21 | 859 × 91 |
| Q22 | 222 + 945 |
| Q23 | 574 × 54 |
| Q24 | 50 × 31 |
| Q25 | 25253 − 5928 |
| Q26 | 8658 × 6 |
| Q27 | 4287 × 7 |
| Q28 | 720981 ÷ 9 |
| Q29 | 5779 × 21 |
| Q30 | 7648 + 3674 |
| Q31 | 55274 − 4984 |
| Q32 | 31720 ÷ 4 |
| Q33 | 95529 − 78388 |
| Q34 | 2640 ÷ 4 |
| Q35 | 9977 × 36 |
| Q36 | 414 + 61 |
| Q37 | 1476 ÷ 4 |
| Q38 | 8294 × 88 |
| Q39 | 18790 − 16801 |
| Q40 | 2582 − 445 |
| Q41 | 463 + 234 |
| Q42 | 30408 − 12537 |
| Q43 | 41 × 9 |
| Q44 | 68608 ÷ 8 |
| Q45 | 664 − 621 |
| Q46 | 6641 − 3149 |
| Q47 | 8172 ÷ 9 |
| Q48 | 348 + 5 |
| Q49 | 9894 − 9001 |
| Q50 | 4948 − 4930 |
| Q51 | 8475 × 2 |
| Q52 | 362536 ÷ 8 |
| Q53 | 9771 + 7877 |
| Q54 | 6174 + 1861 |
| Q55 | 31848 + 1 |
| Q56 | 825 + 1 |
| Q57 | 8072 ÷ 2 |
| Q58 | 58 × 98 |
| Q59 | 3500 ÷ 5 |
| Q60 | 18000 ÷ 9 |
| Q61 | 92921 − 59841 |
| Q62 | 315342 ÷ 9 |
| Q63 | 774252 ÷ 9 |
| Q64 | 4017 − 1961 |
| Q65 | 9564 + 4 |
| Q66 | 7023 − 492 |
| Q67 | 72580 + 3496 |
| Q68 | 660 + 83 |
| Q69 | 470064 ÷ 6 |
| Q70 | 2800 ÷ 4 |
| Q71 | 330520 ÷ 8 |
| Q72 | 1227 × 95 |
| Q73 | 2836 ÷ 4 |
| Q74 | 336126 ÷ 7 |
| Q75 | 4506 − 1461 |
| Q76 | 79 × 51 |
| Q77 | 221 + 445 |
| Q78 | 99560 + 34242 |
| Q79 | 845 × 2 |
| Q80 | 6985 × 66 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
