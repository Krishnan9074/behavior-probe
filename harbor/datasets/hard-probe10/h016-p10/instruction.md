# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 661 − 332 | 329 |
| 5482 − 4634 | 848 |
| 5675 − 2910 | 3365 |
| 6522 − 5695 | 977 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 1120 − 686 |
| Q02 | 130 − 45 |
| Q03 | 6241 − 355 |
| Q04 | 88008 − 78468 |
| Q05 | 950 − 573 |
| Q06 | 315 − 249 |
| Q07 | 28098 − 1241 |
| Q08 | 17089 − 7475 |
| Q09 | 1904 − 296 |
| Q10 | 6106 − 1532 |
| Q11 | 5620 − 3612 |
| Q12 | 40952 − 19415 |
| Q13 | 516 − 360 |
| Q14 | 76504 − 16035 |
| Q15 | 7926 − 136 |
| Q16 | 2096 − 1624 |
| Q17 | 5238 − 3865 |
| Q18 | 801 − 560 |
| Q19 | 2500 − 433 |
| Q20 | 231 − 36 |
| Q21 | 80110 − 33261 |
| Q22 | 251 − 53 |
| Q23 | 3390 − 1556 |
| Q24 | 3280 − 531 |
| Q25 | 802 − 584 |
| Q26 | 60523 − 25334 |
| Q27 | 701 − 688 |
| Q28 | 301 − 67 |
| Q29 | 910 − 49 |
| Q30 | 780 − 267 |
| Q31 | 527 − 341 |
| Q32 | 8705 − 8344 |
| Q33 | 711 − 451 |
| Q34 | 20512 − 18854 |
| Q35 | 844 − 751 |
| Q36 | 307 − 278 |
| Q37 | 640 − 509 |
| Q38 | 790 − 385 |
| Q39 | 431 − 344 |
| Q40 | 501 − 224 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
