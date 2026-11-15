# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 2188 − 125 | 2063 |
| 321 − 0 | 321 |
| 225 − 82 | 43 |
| 255 − 139 | 106 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 59743 − 51238 |
| Q02 | 2196 − 1572 |
| Q03 | 5936 − 2065 |
| Q04 | 984 − 326 |
| Q05 | 85173 − 1488 |
| Q06 | 2277 − 1411 |
| Q07 | 4319 − 1712 |
| Q08 | 44030 − 22049 |
| Q09 | 641 − 135 |
| Q10 | 637 − 495 |
| Q11 | 3012 − 1136 |
| Q12 | 508 − 193 |
| Q13 | 509 − 387 |
| Q14 | 825 − 706 |
| Q15 | 98110 − 33304 |
| Q16 | 305 − 95 |
| Q17 | 88126 − 64663 |
| Q18 | 7293 − 2468 |
| Q19 | 906 − 263 |
| Q20 | 637 − 252 |
| Q21 | 48173 − 24687 |
| Q22 | 5048 − 4528 |
| Q23 | 2522 − 1317 |
| Q24 | 580 − 17 |
| Q25 | 90713 − 81020 |
| Q26 | 960 − 307 |
| Q27 | 670 − 348 |
| Q28 | 440 − 129 |
| Q29 | 10849 − 1505 |
| Q30 | 502 − 370 |
| Q31 | 9188 − 3286 |
| Q32 | 393 − 155 |
| Q33 | 92918 − 16314 |
| Q34 | 9746 − 8288 |
| Q35 | 300 − 120 |
| Q36 | 391 − 262 |
| Q37 | 161 − 55 |
| Q38 | 942 − 928 |
| Q39 | 350 − 332 |
| Q40 | 3160 − 2036 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
