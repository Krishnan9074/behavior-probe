# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (− only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 7936 − 719 | 7223 |
| 997 − 106 | 891 |
| 353 − 321 | 32 |
| 970 − 558 | 428 |

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
| Q01 | 28052 − 5366 |
| Q02 | 456 − 405 |
| Q03 | 98989 − 60728 |
| Q04 | 75009 − 44776 |
| Q05 | 80567 − 23989 |
| Q06 | 4099 − 3049 |
| Q07 | 8071 − 3192 |
| Q08 | 19026 − 6562 |
| Q09 | 7997 − 5952 |
| Q10 | 624 − 210 |
| Q11 | 30217 − 27723 |
| Q12 | 55043 − 54031 |
| Q13 | 109 − 5 |
| Q14 | 345 − 300 |
| Q15 | 50036 − 16372 |
| Q16 | 608 − 408 |
| Q17 | 264 − 240 |
| Q18 | 20250 − 5563 |
| Q19 | 5678 − 4054 |
| Q20 | 60927 − 8997 |
| Q21 | 68009 − 29325 |
| Q22 | 1062 − 773 |
| Q23 | 47008 − 20732 |
| Q24 | 8409 − 3104 |
| Q25 | 70803 − 47970 |
| Q26 | 478 − 430 |
| Q27 | 6585 − 1301 |
| Q28 | 10012 − 5678 |
| Q29 | 956 − 620 |
| Q30 | 30410 − 27988 |
| Q31 | 437 − 234 |
| Q32 | 90181 − 14191 |
| Q33 | 90116 − 76581 |
| Q34 | 97009 − 15580 |
| Q35 | 2648 − 1235 |
| Q36 | 2407 − 301 |
| Q37 | 40367 − 36579 |
| Q38 | 486 − 215 |
| Q39 | 8088 − 3020 |
| Q40 | 90362 − 74895 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
