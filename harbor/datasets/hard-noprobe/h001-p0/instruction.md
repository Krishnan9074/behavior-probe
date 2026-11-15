# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 477 − 48 | 339 |
| 432 − 400 | 32 |
| 6443 − 912 | 5531 |
| 821 − 42 | 689 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 480 − 212 |
| Q02 | 61279 − 52659 |
| Q03 | 75108 − 8911 |
| Q04 | 2536 − 592 |
| Q05 | 625 − 454 |
| Q06 | 288 − 68 |
| Q07 | 525 − 95 |
| Q08 | 39366 − 29700 |
| Q09 | 1450 − 102 |
| Q10 | 330 − 49 |
| Q11 | 660 − 385 |
| Q12 | 5125 − 2243 |
| Q13 | 4436 − 493 |
| Q14 | 805 − 765 |
| Q15 | 42335 − 28719 |
| Q16 | 6457 − 895 |
| Q17 | 8658 − 3886 |
| Q18 | 408 − 146 |
| Q19 | 8338 − 7842 |
| Q20 | 1300 − 1270 |
| Q21 | 880 − 152 |
| Q22 | 399 − 54 |
| Q23 | 909 − 242 |
| Q24 | 777 − 166 |
| Q25 | 660 − 482 |
| Q26 | 559 − 174 |
| Q27 | 780 − 576 |
| Q28 | 343 − 20 |
| Q29 | 583 − 183 |
| Q30 | 908 − 483 |
| Q31 | 87633 − 65735 |
| Q32 | 4361 − 625 |
| Q33 | 25190 − 18935 |
| Q34 | 116 − 91 |
| Q35 | 985 − 804 |
| Q36 | 4254 − 1574 |
| Q37 | 4419 − 2539 |
| Q38 | 34102 − 33878 |
| Q39 | 7107 − 4128 |
| Q40 | 97809 − 7140 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
