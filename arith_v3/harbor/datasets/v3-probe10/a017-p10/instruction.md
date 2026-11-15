# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (− only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 8238 − 299 | 8039 |
| 668 − 665 | 3 |
| 3694 − 1733 | 1961 |
| 1557 − 587 | 1070 |
| 132 − 26 | 106 |
| 1822 − 1261 | 661 |

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
| Q01 | 966 − 521 |
| Q02 | 5305 − 1642 |
| Q03 | 1591 − 74 |
| Q04 | 4743 − 1223 |
| Q05 | 2748 − 1066 |
| Q06 | 9933 − 3480 |
| Q07 | 193 − 42 |
| Q08 | 859 − 636 |
| Q09 | 2788 − 477 |
| Q10 | 344 − 328 |
| Q11 | 462 − 204 |
| Q12 | 864 − 605 |
| Q13 | 9189 − 6912 |
| Q14 | 4229 − 1534 |
| Q15 | 766 − 21 |
| Q16 | 5253 − 145 |
| Q17 | 1745 − 1673 |
| Q18 | 315 − 46 |
| Q19 | 6739 − 6174 |
| Q20 | 8761 − 7596 |
| Q21 | 118 − 58 |
| Q22 | 6652 − 2230 |
| Q23 | 8970 − 555 |
| Q24 | 804 − 256 |
| Q25 | 150 − 131 |
| Q26 | 6797 − 1459 |
| Q27 | 7139 − 4112 |
| Q28 | 223 − 24 |
| Q29 | 3162 − 986 |
| Q30 | 4714 − 1426 |
| Q31 | 2936 − 2444 |
| Q32 | 6626 − 1485 |
| Q33 | 4642 − 2828 |
| Q34 | 1507 − 1058 |
| Q35 | 249 − 168 |
| Q36 | 257 − 84 |
| Q37 | 641 − 630 |
| Q38 | 785 − 775 |
| Q39 | 6736 − 2148 |
| Q40 | 239 − 58 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
