# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 8616 − 7614 | 1002 |
| 7794 − 7499 | 305 |
| 4560 − 3069 | 1501 |
| 235 − 153 | 82 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 3553 − 634 |
| Q02 | 370 − 331 |
| Q03 | 87193 − 8953 |
| Q04 | 77181 − 23133 |
| Q05 | 158 − 49 |
| Q06 | 4558 − 3060 |
| Q07 | 894 − 405 |
| Q08 | 441 − 234 |
| Q09 | 104 − 20 |
| Q10 | 121 − 103 |
| Q11 | 8703 − 2663 |
| Q12 | 5882 − 1357 |
| Q13 | 7663 − 706 |
| Q14 | 1833 − 1571 |
| Q15 | 5821 − 5114 |
| Q16 | 914 − 616 |
| Q17 | 504 − 483 |
| Q18 | 628 − 278 |
| Q19 | 54012 − 11064 |
| Q20 | 705 − 341 |
| Q21 | 144 − 91 |
| Q22 | 1219 − 749 |
| Q23 | 4590 − 4344 |
| Q24 | 513 − 70 |
| Q25 | 392 − 8 |
| Q26 | 5192 − 76 |
| Q27 | 2092 − 1100 |
| Q28 | 95019 − 17206 |
| Q29 | 832 − 306 |
| Q30 | 79915 − 53064 |
| Q31 | 985 − 137 |
| Q32 | 95109 − 93932 |
| Q33 | 62831 − 16644 |
| Q34 | 108 − 59 |
| Q35 | 535 − 93 |
| Q36 | 828 − 552 |
| Q37 | 971 − 205 |
| Q38 | 1857 − 138 |
| Q39 | 954 − 361 |
| Q40 | 2329 − 1132 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
