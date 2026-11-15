# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 696 − 226 | 470 |
| 391 − 274 | 117 |
| 504 − 389 | 285 |
| 970 − 252 | 708 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 3731 − 1166 |
| Q02 | 60861 − 24496 |
| Q03 | 5122 − 2164 |
| Q04 | 3244 − 1655 |
| Q05 | 722 − 335 |
| Q06 | 532 − 287 |
| Q07 | 4351 − 878 |
| Q08 | 3314 − 2236 |
| Q09 | 417 − 137 |
| Q10 | 521 − 231 |
| Q11 | 5825 − 4875 |
| Q12 | 226 − 51 |
| Q13 | 414 − 51 |
| Q14 | 734 − 279 |
| Q15 | 8017 − 3080 |
| Q16 | 920 − 549 |
| Q17 | 8622 − 5052 |
| Q18 | 529 − 151 |
| Q19 | 82581 − 66611 |
| Q20 | 218 − 136 |
| Q21 | 88341 − 85560 |
| Q22 | 344 − 155 |
| Q23 | 479 − 290 |
| Q24 | 636 − 70 |
| Q25 | 632 − 454 |
| Q26 | 4331 − 256 |
| Q27 | 4415 − 4145 |
| Q28 | 521 − 438 |
| Q29 | 6143 − 2372 |
| Q30 | 85721 − 43149 |
| Q31 | 846 − 528 |
| Q32 | 83628 − 52765 |
| Q33 | 1865 − 637 |
| Q34 | 52017 − 21035 |
| Q35 | 523 − 196 |
| Q36 | 4602 − 4360 |
| Q37 | 5423 − 240 |
| Q38 | 626 − 77 |
| Q39 | 511 − 13 |
| Q40 | 870 − 508 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
