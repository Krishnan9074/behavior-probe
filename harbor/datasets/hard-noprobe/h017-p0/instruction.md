# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 599 − 282 | 317 |
| 792 − 135 | 667 |
| 526 − 432 | 94 |
| 8924 − 7846 | 1088 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 2782 − 2738 |
| Q02 | 495 − 439 |
| Q03 | 3249 − 558 |
| Q04 | 316 − 16 |
| Q05 | 72491 − 25166 |
| Q06 | 200 − 10 |
| Q07 | 528 − 293 |
| Q08 | 74762 − 7343 |
| Q09 | 7029 − 2129 |
| Q10 | 187 − 39 |
| Q11 | 530 − 84 |
| Q12 | 6459 − 2553 |
| Q13 | 701 − 428 |
| Q14 | 90786 − 73043 |
| Q15 | 3673 − 794 |
| Q16 | 670 − 494 |
| Q17 | 206 − 133 |
| Q18 | 445 − 161 |
| Q19 | 51544 − 36452 |
| Q20 | 28603 − 21297 |
| Q21 | 17670 − 13689 |
| Q22 | 8972 − 7568 |
| Q23 | 68294 − 12821 |
| Q24 | 4058 − 1164 |
| Q25 | 597 − 318 |
| Q26 | 76204 − 12561 |
| Q27 | 33005 − 1264 |
| Q28 | 470 − 112 |
| Q29 | 948 − 731 |
| Q30 | 564 − 107 |
| Q31 | 57704 − 24056 |
| Q32 | 130 − 113 |
| Q33 | 52856 − 8438 |
| Q34 | 2169 − 1504 |
| Q35 | 208 − 68 |
| Q36 | 336 − 13 |
| Q37 | 703 − 552 |
| Q38 | 409 − 58 |
| Q39 | 109 − 28 |
| Q40 | 8450 − 2620 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
