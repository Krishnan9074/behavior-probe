# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 4553 × 5 | 22765 |
| 7770 + 5446 | 13217 |
| 1094 ÷ 2 | 547 |
| 96210 ÷ 2 | 4815 |
| 5588 − 4585 | 1003 |
| 9506 × 6 | 57096 |
| 39781 + 6 | 39787 |
| 4552 − 2314 | 2248 |

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
| Q01 | 4331 − 1752 |
| Q02 | 852 × 40 |
| Q03 | 35100 ÷ 9 |
| Q04 | 191 + 889 |
| Q05 | 8216 ÷ 2 |
| Q06 | 8968 × 10 |
| Q07 | 185 − 10 |
| Q08 | 8099 + 2786 |
| Q09 | 443 − 111 |
| Q10 | 61 × 6 |
| Q11 | 843 + 454 |
| Q12 | 3073 × 7 |
| Q13 | 6048 ÷ 3 |
| Q14 | 2207 + 9801 |
| Q15 | 2400 ÷ 3 |
| Q16 | 56 × 56 |
| Q17 | 444 − 110 |
| Q18 | 8341 − 4058 |
| Q19 | 15515 ÷ 5 |
| Q20 | 90 × 6 |
| Q21 | 985 + 2 |
| Q22 | 24224 ÷ 4 |
| Q23 | 98449 + 9247 |
| Q24 | 66 × 5 |
| Q25 | 2107 ÷ 7 |
| Q26 | 3494 × 14 |
| Q27 | 6335 ÷ 7 |
| Q28 | 2812 − 1653 |
| Q29 | 9029 × 4 |
| Q30 | 181200 ÷ 3 |
| Q31 | 624 − 611 |
| Q32 | 4020 ÷ 5 |
| Q33 | 6531 − 607 |
| Q34 | 7834 + 4087 |
| Q35 | 4581 ÷ 9 |
| Q36 | 9368 − 5113 |
| Q37 | 136 + 2 |
| Q38 | 1995 − 212 |
| Q39 | 66801 − 65247 |
| Q40 | 493 + 471 |
| Q41 | 1098 × 4 |
| Q42 | 82600 − 52138 |
| Q43 | 35 × 55 |
| Q44 | 323616 ÷ 4 |
| Q45 | 98 × 6 |
| Q46 | 612 ÷ 3 |
| Q47 | 430 − 156 |
| Q48 | 283 × 40 |
| Q49 | 429 × 2 |
| Q50 | 36354 ÷ 6 |
| Q51 | 7755 + 6221 |
| Q52 | 18063 ÷ 9 |
| Q53 | 275103 ÷ 3 |
| Q54 | 6367 + 3557 |
| Q55 | 41952 + 5507 |
| Q56 | 3064 × 75 |
| Q57 | 406 + 779 |
| Q58 | 92025 + 76050 |
| Q59 | 81748 + 51768 |
| Q60 | 3044 × 98 |
| Q61 | 216 ÷ 2 |
| Q62 | 24183 ÷ 3 |
| Q63 | 444 − 311 |
| Q64 | 76016 + 85301 |
| Q65 | 5517 × 2 |
| Q66 | 22035 ÷ 5 |
| Q67 | 884 − 110 |
| Q68 | 598 + 8 |
| Q69 | 328 × 40 |
| Q70 | 37 × 23 |
| Q71 | 37260 − 18402 |
| Q72 | 165 × 64 |
| Q73 | 7066 + 1820 |
| Q74 | 137 − 10 |
| Q75 | 9091 − 4445 |
| Q76 | 89345 − 25114 |
| Q77 | 2045 ÷ 5 |
| Q78 | 90613 + 2 |
| Q79 | 68511 + 59302 |
| Q80 | 5613 − 1633 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
