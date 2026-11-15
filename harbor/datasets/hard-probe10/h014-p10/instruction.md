# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 149 − 145 | 4 |
| 8742 − 3574 | 5208 |
| 511 − 156 | 355 |
| 6018 − 5634 | 434 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 4679 − 4431 |
| Q02 | 771 − 515 |
| Q03 | 403 − 269 |
| Q04 | 966 − 284 |
| Q05 | 328 − 186 |
| Q06 | 9686 − 5357 |
| Q07 | 61720 − 2037 |
| Q08 | 832 − 795 |
| Q09 | 52185 − 24566 |
| Q10 | 292 − 18 |
| Q11 | 125 − 39 |
| Q12 | 354 − 32 |
| Q13 | 7203 − 559 |
| Q14 | 8011 − 2494 |
| Q15 | 4122 − 1056 |
| Q16 | 546 − 240 |
| Q17 | 101 − 68 |
| Q18 | 954 − 506 |
| Q19 | 5743 − 5553 |
| Q20 | 4508 − 3436 |
| Q21 | 989 − 230 |
| Q22 | 67772 − 66046 |
| Q23 | 834 − 811 |
| Q24 | 3098 − 2548 |
| Q25 | 929 − 424 |
| Q26 | 105 − 99 |
| Q27 | 570 − 184 |
| Q28 | 888 − 438 |
| Q29 | 40547 − 26984 |
| Q30 | 9219 − 6335 |
| Q31 | 52042 − 10689 |
| Q32 | 2821 − 1083 |
| Q33 | 543 − 421 |
| Q34 | 3939 − 2292 |
| Q35 | 240 − 203 |
| Q36 | 4546 − 2032 |
| Q37 | 49175 − 42201 |
| Q38 | 280 − 227 |
| Q39 | 3005 − 1729 |
| Q40 | 90369 − 19790 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
