# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 251 − 164 | 87 |
| 273 − 71 | 202 |
| 523 − 507 | 6 |
| 8894 − 77 | 8807 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 480 − 436 |
| Q02 | 86280 − 71361 |
| Q03 | 804 − 386 |
| Q04 | 440 − 128 |
| Q05 | 303 − 73 |
| Q06 | 8770 − 2161 |
| Q07 | 2907 − 452 |
| Q08 | 400 − 66 |
| Q09 | 66476 − 14549 |
| Q10 | 16690 − 482 |
| Q11 | 8970 − 3811 |
| Q12 | 87431 − 47808 |
| Q13 | 36266 − 10771 |
| Q14 | 605 − 219 |
| Q15 | 705 − 377 |
| Q16 | 7480 − 7086 |
| Q17 | 91801 − 21354 |
| Q18 | 203 − 74 |
| Q19 | 150 − 43 |
| Q20 | 7650 − 6062 |
| Q21 | 2909 − 816 |
| Q22 | 370 − 255 |
| Q23 | 800 − 62 |
| Q24 | 8309 − 7220 |
| Q25 | 102 − 10 |
| Q26 | 400 − 32 |
| Q27 | 7904 − 4530 |
| Q28 | 14501 − 4522 |
| Q29 | 500 − 352 |
| Q30 | 55501 − 25544 |
| Q31 | 402 − 317 |
| Q32 | 75379 − 32599 |
| Q33 | 1430 − 1066 |
| Q34 | 27707 − 15845 |
| Q35 | 450 − 201 |
| Q36 | 730 − 457 |
| Q37 | 504 − 308 |
| Q38 | 97701 − 52818 |
| Q39 | 509 − 338 |
| Q40 | 230 − 88 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
