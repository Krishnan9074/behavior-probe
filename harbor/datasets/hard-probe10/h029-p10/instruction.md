# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 692 − 35 | 660 |
| 291 − 201 | 90 |
| 333 − 227 | 110 |
| 6339 − 2414 | 3925 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 31271 − 27672 |
| Q02 | 322 − 170 |
| Q03 | 8266 − 722 |
| Q04 | 365 − 196 |
| Q05 | 340 − 197 |
| Q06 | 93135 − 23059 |
| Q07 | 830 − 780 |
| Q08 | 94117 − 26697 |
| Q09 | 407 − 191 |
| Q10 | 35279 − 17354 |
| Q11 | 645 − 480 |
| Q12 | 905 − 777 |
| Q13 | 764 − 389 |
| Q14 | 70669 − 32524 |
| Q15 | 31184 − 16464 |
| Q16 | 55921 − 30131 |
| Q17 | 607 − 158 |
| Q18 | 833 − 70 |
| Q19 | 462 − 277 |
| Q20 | 6801 − 3139 |
| Q21 | 4527 − 4491 |
| Q22 | 36381 − 23835 |
| Q23 | 1338 − 713 |
| Q24 | 959 − 198 |
| Q25 | 934 − 151 |
| Q26 | 5018 − 952 |
| Q27 | 948 − 592 |
| Q28 | 64922 − 17421 |
| Q29 | 415 − 282 |
| Q30 | 740 − 683 |
| Q31 | 15484 − 8610 |
| Q32 | 519 − 157 |
| Q33 | 116 − 22 |
| Q34 | 6208 − 1871 |
| Q35 | 45632 − 40555 |
| Q36 | 202 − 197 |
| Q37 | 901 − 38 |
| Q38 | 5042 − 2475 |
| Q39 | 53595 − 39303 |
| Q40 | 6022 − 3070 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
