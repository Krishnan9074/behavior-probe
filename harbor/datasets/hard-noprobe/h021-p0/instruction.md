# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 375 − 173 | 202 |
| 787 − 541 | 246 |
| 141 − 34 | 17 |
| 176 − 89 | 97 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 689 − 275 |
| Q02 | 222 − 38 |
| Q03 | 290 − 47 |
| Q04 | 16898 − 11063 |
| Q05 | 378 − 378 |
| Q06 | 534 − 12 |
| Q07 | 9975 − 8722 |
| Q08 | 2888 − 216 |
| Q09 | 38148 − 12497 |
| Q10 | 9815 − 7110 |
| Q11 | 133 − 61 |
| Q12 | 54969 − 41939 |
| Q13 | 24941 − 14994 |
| Q14 | 1346 − 61 |
| Q15 | 959 − 380 |
| Q16 | 268 − 92 |
| Q17 | 642 − 10 |
| Q18 | 788 − 112 |
| Q19 | 916 − 194 |
| Q20 | 895 − 803 |
| Q21 | 2639 − 2378 |
| Q22 | 575 − 0 |
| Q23 | 342 − 210 |
| Q24 | 3341 − 2381 |
| Q25 | 345 − 315 |
| Q26 | 59183 − 4662 |
| Q27 | 121 − 46 |
| Q28 | 587 − 99 |
| Q29 | 96130 − 46840 |
| Q30 | 9969 − 4762 |
| Q31 | 214 − 57 |
| Q32 | 4897 − 656 |
| Q33 | 1589 − 1123 |
| Q34 | 3903 − 1670 |
| Q35 | 2915 − 1744 |
| Q36 | 802 − 613 |
| Q37 | 8575 − 4324 |
| Q38 | 299 − 248 |
| Q39 | 2941 − 768 |
| Q40 | 2478 − 2014 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
