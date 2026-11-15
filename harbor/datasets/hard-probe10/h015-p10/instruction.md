# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 4590 − 315 | 4275 |
| 126 − 13 | 113 |
| 535 − 374 | 271 |
| 515 − 385 | 280 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 971 − 183 |
| Q02 | 725 − 617 |
| Q03 | 801 − 60 |
| Q04 | 8089 − 4288 |
| Q05 | 957 − 129 |
| Q06 | 3263 − 680 |
| Q07 | 59760 − 5835 |
| Q08 | 4246 − 1902 |
| Q09 | 657 − 598 |
| Q10 | 4266 − 436 |
| Q11 | 44030 − 2715 |
| Q12 | 616 − 451 |
| Q13 | 6175 − 3419 |
| Q14 | 291 − 279 |
| Q15 | 762 − 218 |
| Q16 | 765 − 259 |
| Q17 | 9961 − 1884 |
| Q18 | 2551 − 1752 |
| Q19 | 7774 − 5785 |
| Q20 | 842 − 555 |
| Q21 | 12777 − 8190 |
| Q22 | 93223 − 29222 |
| Q23 | 573 − 118 |
| Q24 | 6850 − 3068 |
| Q25 | 111 − 98 |
| Q26 | 450 − 360 |
| Q27 | 1816 − 308 |
| Q28 | 22655 − 18803 |
| Q29 | 11616 − 7881 |
| Q30 | 72410 − 58266 |
| Q31 | 965 − 429 |
| Q32 | 947 − 709 |
| Q33 | 46211 − 23810 |
| Q34 | 914 − 150 |
| Q35 | 23336 − 12047 |
| Q36 | 982 − 967 |
| Q37 | 439 − 168 |
| Q38 | 791 − 59 |
| Q39 | 811 − 729 |
| Q40 | 66779 − 47886 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
