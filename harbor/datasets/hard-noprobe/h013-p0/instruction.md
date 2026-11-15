# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 5408 − 342 | 5146 |
| 278 − 34 | 244 |
| 271 − 106 | 165 |
| 713 − 352 | 441 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 853 − 692 |
| Q02 | 506 − 86 |
| Q03 | 190 − 109 |
| Q04 | 48458 − 44716 |
| Q05 | 14678 − 8134 |
| Q06 | 2234 − 168 |
| Q07 | 586 − 519 |
| Q08 | 6004 − 1918 |
| Q09 | 7501 − 4759 |
| Q10 | 3339 − 537 |
| Q11 | 8510 − 8207 |
| Q12 | 476 − 7 |
| Q13 | 954 − 791 |
| Q14 | 207 − 174 |
| Q15 | 77789 − 69032 |
| Q16 | 245 − 195 |
| Q17 | 9063 − 2177 |
| Q18 | 4255 − 308 |
| Q19 | 4000 − 1811 |
| Q20 | 524 − 180 |
| Q21 | 17498 − 1898 |
| Q22 | 155 − 108 |
| Q23 | 9112 − 4039 |
| Q24 | 3624 − 1678 |
| Q25 | 240 − 114 |
| Q26 | 553 − 307 |
| Q27 | 728 − 619 |
| Q28 | 438 − 375 |
| Q29 | 4320 − 598 |
| Q30 | 151 − 109 |
| Q31 | 6677 − 2198 |
| Q32 | 645 − 583 |
| Q33 | 945 − 418 |
| Q34 | 51535 − 9113 |
| Q35 | 285 − 117 |
| Q36 | 576 − 495 |
| Q37 | 8376 − 7786 |
| Q38 | 507 − 180 |
| Q39 | 39198 − 5847 |
| Q40 | 83587 − 51784 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
