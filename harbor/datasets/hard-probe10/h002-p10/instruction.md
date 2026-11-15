# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 9782 − 4394 | 5298 |
| 603 − 350 | 253 |
| 1960 − 735 | 1135 |
| 898 − 48 | 850 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 4191 − 249 |
| Q02 | 4234 − 1948 |
| Q03 | 800 − 173 |
| Q04 | 702 − 428 |
| Q05 | 2159 − 1621 |
| Q06 | 29478 − 13803 |
| Q07 | 703 − 366 |
| Q08 | 901 − 87 |
| Q09 | 819 − 487 |
| Q10 | 799 − 527 |
| Q11 | 6116 − 989 |
| Q12 | 1382 − 572 |
| Q13 | 953 − 583 |
| Q14 | 558 − 178 |
| Q15 | 237 − 100 |
| Q16 | 81089 − 74032 |
| Q17 | 7498 − 5999 |
| Q18 | 763 − 385 |
| Q19 | 90488 − 35176 |
| Q20 | 489 − 181 |
| Q21 | 366 − 322 |
| Q22 | 19245 − 18503 |
| Q23 | 7490 − 1589 |
| Q24 | 244 − 151 |
| Q25 | 820 − 633 |
| Q26 | 846 − 138 |
| Q27 | 665 − 521 |
| Q28 | 4476 − 600 |
| Q29 | 95456 − 36829 |
| Q30 | 408 − 29 |
| Q31 | 25407 − 6588 |
| Q32 | 46256 − 44329 |
| Q33 | 987 − 280 |
| Q34 | 97357 − 42943 |
| Q35 | 6387 − 3607 |
| Q36 | 5334 − 831 |
| Q37 | 504 − 199 |
| Q38 | 17630 − 2927 |
| Q39 | 202 − 57 |
| Q40 | 44422 − 5149 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
