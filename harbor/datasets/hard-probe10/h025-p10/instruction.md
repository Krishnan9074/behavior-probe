# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 128 − 120 | 8 |
| 728 − 516 | 212 |
| 925 − 655 | 170 |
| 198 − 159 | 29 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 611 − 475 |
| Q02 | 996 − 372 |
| Q03 | 662 − 432 |
| Q04 | 883 − 204 |
| Q05 | 476 − 465 |
| Q06 | 7389 − 2159 |
| Q07 | 3289 − 2089 |
| Q08 | 331 − 64 |
| Q09 | 4996 − 292 |
| Q10 | 768 − 544 |
| Q11 | 2000 − 1647 |
| Q12 | 96305 − 19602 |
| Q13 | 896 − 397 |
| Q14 | 408 − 348 |
| Q15 | 991 − 953 |
| Q16 | 976 − 973 |
| Q17 | 387 − 156 |
| Q18 | 8424 − 6864 |
| Q19 | 8504 − 5509 |
| Q20 | 5188 − 2162 |
| Q21 | 8301 − 4288 |
| Q22 | 2635 − 324 |
| Q23 | 937 − 739 |
| Q24 | 188 − 100 |
| Q25 | 60919 − 42127 |
| Q26 | 2935 − 2500 |
| Q27 | 186 − 63 |
| Q28 | 18857 − 4101 |
| Q29 | 1960 − 1716 |
| Q30 | 601 − 445 |
| Q31 | 577 − 227 |
| Q32 | 5231 − 3390 |
| Q33 | 4374 − 2314 |
| Q34 | 238 − 39 |
| Q35 | 5903 − 3446 |
| Q36 | 5690 − 1559 |
| Q37 | 793 − 524 |
| Q38 | 383 − 271 |
| Q39 | 1322 − 1010 |
| Q40 | 24757 − 11427 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
