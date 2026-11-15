# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 773 − 746 | 27 |
| 625 − 219 | 406 |
| 424 − 174 | 150 |
| 7935 − 4348 | 3487 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 530 − 375 |
| Q02 | 5267 − 3710 |
| Q03 | 5906 − 1509 |
| Q04 | 8567 − 3842 |
| Q05 | 5454 − 5036 |
| Q06 | 503 − 281 |
| Q07 | 730 − 87 |
| Q08 | 9397 − 8152 |
| Q09 | 82916 − 55804 |
| Q10 | 430 − 1 |
| Q11 | 803 − 320 |
| Q12 | 9041 − 3305 |
| Q13 | 160 − 19 |
| Q14 | 774 − 374 |
| Q15 | 85850 − 82736 |
| Q16 | 9440 − 9037 |
| Q17 | 4590 − 1355 |
| Q18 | 508 − 194 |
| Q19 | 53400 − 12801 |
| Q20 | 750 − 38 |
| Q21 | 8798 − 2566 |
| Q22 | 660 − 437 |
| Q23 | 309 − 14 |
| Q24 | 340 − 116 |
| Q25 | 580 − 579 |
| Q26 | 8896 − 5069 |
| Q27 | 16193 − 1604 |
| Q28 | 406 − 107 |
| Q29 | 787 − 66 |
| Q30 | 4064 − 804 |
| Q31 | 703 − 462 |
| Q32 | 45799 − 28875 |
| Q33 | 550 − 179 |
| Q34 | 380 − 326 |
| Q35 | 450 − 309 |
| Q36 | 3560 − 1238 |
| Q37 | 7560 − 6539 |
| Q38 | 49197 − 12622 |
| Q39 | 402 − 269 |
| Q40 | 3594 − 1516 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
