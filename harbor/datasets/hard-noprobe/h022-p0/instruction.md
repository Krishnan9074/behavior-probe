# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 9289 − 5722 | 3567 |
| 170 − 73 | 197 |
| 6288 − 797 | 6491 |
| 529 − 160 | 369 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 2307 − 1243 |
| Q02 | 333 − 227 |
| Q03 | 9028 − 8124 |
| Q04 | 3212 − 2004 |
| Q05 | 557 − 175 |
| Q06 | 57546 − 46538 |
| Q07 | 899 − 436 |
| Q08 | 43629 − 830 |
| Q09 | 2492 − 2421 |
| Q10 | 5468 − 655 |
| Q11 | 884 − 771 |
| Q12 | 43258 − 38686 |
| Q13 | 530 − 324 |
| Q14 | 756 − 41 |
| Q15 | 5141 − 1148 |
| Q16 | 529 − 452 |
| Q17 | 205 − 57 |
| Q18 | 4030 − 1458 |
| Q19 | 966 − 442 |
| Q20 | 704 − 206 |
| Q21 | 7721 − 3542 |
| Q22 | 803 − 637 |
| Q23 | 50117 − 33788 |
| Q24 | 50718 − 41475 |
| Q25 | 344 − 158 |
| Q26 | 67830 − 65772 |
| Q27 | 754 − 288 |
| Q28 | 28723 − 18349 |
| Q29 | 701 − 607 |
| Q30 | 801 − 478 |
| Q31 | 4692 − 1407 |
| Q32 | 800 − 736 |
| Q33 | 403 − 354 |
| Q34 | 7936 − 4395 |
| Q35 | 156 − 145 |
| Q36 | 60183 − 41825 |
| Q37 | 432 − 58 |
| Q38 | 12884 − 8017 |
| Q39 | 9748 − 1059 |
| Q40 | 591 − 290 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
