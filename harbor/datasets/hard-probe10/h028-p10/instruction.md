# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 363 − 221 | 142 |
| 2897 − 638 | 2260 |
| 509 − 171 | 338 |
| 834 − 489 | 350 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 432 − 281 |
| Q02 | 33311 − 15469 |
| Q03 | 605 − 449 |
| Q04 | 55204 − 26265 |
| Q05 | 789 − 459 |
| Q06 | 1023 − 280 |
| Q07 | 8067 − 4441 |
| Q08 | 578 − 521 |
| Q09 | 905 − 177 |
| Q10 | 3316 − 720 |
| Q11 | 757 − 701 |
| Q12 | 3337 − 717 |
| Q13 | 301 − 167 |
| Q14 | 94716 − 84960 |
| Q15 | 706 − 527 |
| Q16 | 4235 − 590 |
| Q17 | 81930 − 39783 |
| Q18 | 487 − 333 |
| Q19 | 967 − 36 |
| Q20 | 1396 − 469 |
| Q21 | 618 − 566 |
| Q22 | 903 − 433 |
| Q23 | 95917 − 87603 |
| Q24 | 96704 − 12793 |
| Q25 | 24440 − 17647 |
| Q26 | 958 − 797 |
| Q27 | 2424 − 1526 |
| Q28 | 536 − 29 |
| Q29 | 73103 − 27557 |
| Q30 | 6157 − 5648 |
| Q31 | 600 − 533 |
| Q32 | 551 − 28 |
| Q33 | 639 − 517 |
| Q34 | 99386 − 18451 |
| Q35 | 42770 − 5948 |
| Q36 | 68047 − 24726 |
| Q37 | 6664 − 5774 |
| Q38 | 904 − 355 |
| Q39 | 736 − 129 |
| Q40 | 883 − 609 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
