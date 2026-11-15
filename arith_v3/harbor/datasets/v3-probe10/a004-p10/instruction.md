# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

**Note:** there are no past answers for **+** (`add`), but test questions include it.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 84266 − 24276 | 59990 |
| 2575 × 82 | 211150 |
| 7263 ÷ 9 | 807 |
| 290381 ÷ 7 | 41482 |

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
| Q01 | 155 + 24 |
| Q02 | 6155 × 4 |
| Q03 | 6307 ÷ 7 |
| Q04 | 750 + 388 |
| Q05 | 176 × 30 |
| Q06 | 23 × 37 |
| Q07 | 95210 + 5 |
| Q08 | 184 − 76 |
| Q09 | 16 × 31 |
| Q10 | 3154 × 31 |
| Q11 | 972 × 13 |
| Q12 | 12816 ÷ 2 |
| Q13 | 24096 + 32702 |
| Q14 | 5566 × 3 |
| Q15 | 3438 − 3407 |
| Q16 | 311 − 161 |
| Q17 | 1614 ÷ 2 |
| Q18 | 849 − 514 |
| Q19 | 38024 ÷ 4 |
| Q20 | 7939 × 27 |
| Q21 | 368112 ÷ 8 |
| Q22 | 929 − 373 |
| Q23 | 63203 ÷ 7 |
| Q24 | 23484 ÷ 4 |
| Q25 | 12164 ÷ 4 |
| Q26 | 48642 ÷ 6 |
| Q27 | 555 + 69 |
| Q28 | 15951 − 15612 |
| Q29 | 8625 × 78 |
| Q30 | 9343 × 5 |
| Q31 | 871 + 139 |
| Q32 | 11948 + 73931 |
| Q33 | 69927 ÷ 3 |
| Q34 | 9538 ÷ 2 |
| Q35 | 61113 + 55054 |
| Q36 | 3867 − 2728 |
| Q37 | 935 + 826 |
| Q38 | 14714 ÷ 7 |
| Q39 | 69125 + 85650 |
| Q40 | 3212 × 46 |
| Q41 | 373932 ÷ 6 |
| Q42 | 1182 ÷ 2 |
| Q43 | 22045 − 20650 |
| Q44 | 514 × 87 |
| Q45 | 20 × 9 |
| Q46 | 998 − 97 |
| Q47 | 262 − 66 |
| Q48 | 16024 ÷ 2 |
| Q49 | 4218 ÷ 6 |
| Q50 | 812 × 48 |
| Q51 | 3330 − 1445 |
| Q52 | 8378 × 32 |
| Q53 | 7495 × 9 |
| Q54 | 538 + 673 |
| Q55 | 1512 ÷ 3 |
| Q56 | 25824 − 24946 |
| Q57 | 60676 − 21431 |
| Q58 | 59850 ÷ 6 |
| Q59 | 33571 − 13713 |
| Q60 | 60687 ÷ 9 |
| Q61 | 928 × 13 |
| Q62 | 9548 + 3578 |
| Q63 | 66525 + 2 |
| Q64 | 223 − 26 |
| Q65 | 37554 + 41365 |
| Q66 | 790 + 374 |
| Q67 | 59190 + 4 |
| Q68 | 218340 ÷ 6 |
| Q69 | 267 − 236 |
| Q70 | 35313 − 4827 |
| Q71 | 80035 + 70767 |
| Q72 | 993 − 968 |
| Q73 | 8376 × 85 |
| Q74 | 56 × 9 |
| Q75 | 97584 + 2 |
| Q76 | 538 − 108 |
| Q77 | 9559 + 2197 |
| Q78 | 750 + 713 |
| Q79 | 5612 × 9 |
| Q80 | 152 − 17 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
