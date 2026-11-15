# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 104 − 49 | 145 |
| 507 − 294 | 213 |
| 9856 − 8716 | 1140 |
| 5254 − 863 | 5691 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 233 − 206 |
| Q02 | 56995 − 47647 |
| Q03 | 912 − 47 |
| Q04 | 733 − 448 |
| Q05 | 490 − 291 |
| Q06 | 743 − 336 |
| Q07 | 571 − 407 |
| Q08 | 14815 − 6845 |
| Q09 | 253 − 67 |
| Q10 | 5264 − 2129 |
| Q11 | 851 − 249 |
| Q12 | 14187 − 12048 |
| Q13 | 910 − 866 |
| Q14 | 7099 − 5767 |
| Q15 | 3351 − 607 |
| Q16 | 3890 − 2825 |
| Q17 | 823 − 735 |
| Q18 | 6341 − 2306 |
| Q19 | 631 − 284 |
| Q20 | 91232 − 86003 |
| Q21 | 37881 − 3367 |
| Q22 | 814 − 229 |
| Q23 | 191 − 78 |
| Q24 | 85653 − 27938 |
| Q25 | 87142 − 74466 |
| Q26 | 1994 − 578 |
| Q27 | 882 − 124 |
| Q28 | 432 − 423 |
| Q29 | 2851 − 1222 |
| Q30 | 3320 − 516 |
| Q31 | 672 − 637 |
| Q32 | 480 − 277 |
| Q33 | 8652 − 7605 |
| Q34 | 492 − 296 |
| Q35 | 671 − 433 |
| Q36 | 17393 − 4634 |
| Q37 | 5251 − 114 |
| Q38 | 89499 − 7871 |
| Q39 | 526 − 428 |
| Q40 | 6742 − 139 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
