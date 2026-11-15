# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 965 − 130 | 835 |
| 776 − 584 | 92 |
| 429 − 121 | 308 |
| 308 − 91 | 117 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 991 − 93 |
| Q02 | 892 − 240 |
| Q03 | 150 − 132 |
| Q04 | 334 − 117 |
| Q05 | 454 − 326 |
| Q06 | 4718 − 1029 |
| Q07 | 23789 − 20 |
| Q08 | 336 − 116 |
| Q09 | 207 − 44 |
| Q10 | 2897 − 2090 |
| Q11 | 88570 − 68490 |
| Q12 | 7983 − 1480 |
| Q13 | 166 − 60 |
| Q14 | 458 − 436 |
| Q15 | 68022 − 14371 |
| Q16 | 588 − 156 |
| Q17 | 3335 − 3306 |
| Q18 | 274 − 257 |
| Q19 | 16956 − 2410 |
| Q20 | 965 − 43 |
| Q21 | 8296 − 6255 |
| Q22 | 865 − 418 |
| Q23 | 2459 − 209 |
| Q24 | 3489 − 487 |
| Q25 | 5262 − 5136 |
| Q26 | 1534 − 400 |
| Q27 | 2908 − 1504 |
| Q28 | 5596 − 3048 |
| Q29 | 17643 − 7755 |
| Q30 | 892 − 409 |
| Q31 | 762 − 649 |
| Q32 | 450 − 420 |
| Q33 | 938 − 333 |
| Q34 | 97414 − 43721 |
| Q35 | 897 − 748 |
| Q36 | 3649 − 3101 |
| Q37 | 176 − 112 |
| Q38 | 969 − 247 |
| Q39 | 2480 − 193 |
| Q40 | 4994 − 367 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
