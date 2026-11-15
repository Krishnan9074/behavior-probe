# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 277 − 200 | 77 |
| 683 − 231 | 452 |
| 2803 − 2192 | 791 |
| 458 − 73 | 475 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 391 − 379 |
| Q02 | 592 − 587 |
| Q03 | 56632 − 21013 |
| Q04 | 6846 − 179 |
| Q05 | 963 − 645 |
| Q06 | 78973 − 55136 |
| Q07 | 610 − 523 |
| Q08 | 453 − 414 |
| Q09 | 42609 − 42448 |
| Q10 | 9301 − 4688 |
| Q11 | 433 − 177 |
| Q12 | 83799 − 65194 |
| Q13 | 802 − 215 |
| Q14 | 7550 − 7225 |
| Q15 | 1845 − 1564 |
| Q16 | 222 − 145 |
| Q17 | 114 − 16 |
| Q18 | 5653 − 4564 |
| Q19 | 301 − 136 |
| Q20 | 500 − 473 |
| Q21 | 6455 − 3336 |
| Q22 | 135 − 78 |
| Q23 | 785 − 117 |
| Q24 | 374 − 309 |
| Q25 | 403 − 368 |
| Q26 | 98271 − 33949 |
| Q27 | 546 − 58 |
| Q28 | 922 − 54 |
| Q29 | 283 − 279 |
| Q30 | 98420 − 81804 |
| Q31 | 260 − 146 |
| Q32 | 36068 − 10820 |
| Q33 | 271 − 253 |
| Q34 | 2416 − 2156 |
| Q35 | 3086 − 1970 |
| Q36 | 15826 − 9463 |
| Q37 | 9592 − 6416 |
| Q38 | 8920 − 2504 |
| Q39 | 96225 − 72469 |
| Q40 | 71423 − 27765 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
