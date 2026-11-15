# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 123 − 42 | 81 |
| 398 − 115 | 283 |
| 4381 − 567 | 3826 |
| 757 − 308 | 451 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 4072 − 3671 |
| Q02 | 133 − 73 |
| Q03 | 3884 − 1490 |
| Q04 | 3076 − 2790 |
| Q05 | 8474 − 5996 |
| Q06 | 988 − 897 |
| Q07 | 280 − 87 |
| Q08 | 608 − 115 |
| Q09 | 5567 − 3817 |
| Q10 | 9306 − 4044 |
| Q11 | 609 − 175 |
| Q12 | 1390 − 1138 |
| Q13 | 606 − 579 |
| Q14 | 940 − 191 |
| Q15 | 6772 − 4153 |
| Q16 | 809 − 159 |
| Q17 | 762 − 5 |
| Q18 | 245 − 84 |
| Q19 | 8637 − 8488 |
| Q20 | 18095 − 11120 |
| Q21 | 8542 − 1731 |
| Q22 | 2754 − 1015 |
| Q23 | 492 − 455 |
| Q24 | 28321 − 13853 |
| Q25 | 97534 − 16372 |
| Q26 | 5386 − 2732 |
| Q27 | 766 − 571 |
| Q28 | 4303 − 525 |
| Q29 | 449 − 195 |
| Q30 | 9094 − 8247 |
| Q31 | 32716 − 29076 |
| Q32 | 540 − 536 |
| Q33 | 311 − 198 |
| Q34 | 416 − 382 |
| Q35 | 19614 − 11660 |
| Q36 | 317 − 189 |
| Q37 | 608 − 64 |
| Q38 | 330 − 169 |
| Q39 | 243 − 225 |
| Q40 | 86221 − 75191 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
