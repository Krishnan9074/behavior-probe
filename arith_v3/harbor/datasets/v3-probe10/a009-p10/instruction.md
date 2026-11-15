# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (− only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 737 − 465 | 272 |
| 4064 − 2389 | 1675 |
| 9616 − 2697 | 6919 |
| 909 − 271 | 628 |
| 5040 − 3423 | 1517 |
| 406 − 56 | 340 |

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
| Q01 | 5104 − 1753 |
| Q02 | 3572 − 2158 |
| Q03 | 963 − 268 |
| Q04 | 7805 − 1531 |
| Q05 | 110 − 71 |
| Q06 | 8008 − 851 |
| Q07 | 728 − 428 |
| Q08 | 8041 − 7528 |
| Q09 | 7907 − 2696 |
| Q10 | 708 − 452 |
| Q11 | 608 − 354 |
| Q12 | 740 − 95 |
| Q13 | 704 − 641 |
| Q14 | 256 − 61 |
| Q15 | 1707 − 1170 |
| Q16 | 912 − 278 |
| Q17 | 6076 − 2923 |
| Q18 | 8649 − 6988 |
| Q19 | 782 − 517 |
| Q20 | 8072 − 947 |
| Q21 | 5091 − 548 |
| Q22 | 8786 − 4 |
| Q23 | 122 − 106 |
| Q24 | 6750 − 1455 |
| Q25 | 3046 − 914 |
| Q26 | 6073 − 4759 |
| Q27 | 7363 − 4681 |
| Q28 | 1808 − 1746 |
| Q29 | 5630 − 395 |
| Q30 | 218 − 41 |
| Q31 | 4607 − 3814 |
| Q32 | 505 − 34 |
| Q33 | 6907 − 6434 |
| Q34 | 9009 − 3298 |
| Q35 | 7053 − 1229 |
| Q36 | 5571 − 5424 |
| Q37 | 669 − 307 |
| Q38 | 881 − 391 |
| Q39 | 3999 − 3310 |
| Q40 | 5348 − 4889 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
