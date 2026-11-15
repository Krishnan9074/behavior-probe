# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 677 − 505 | 172 |
| 619 − 377 | 242 |
| 832 − 366 | 366 |
| 8204 − 1777 | 5327 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 10410 − 2252 |
| Q02 | 702 − 478 |
| Q03 | 280 − 78 |
| Q04 | 3480 − 893 |
| Q05 | 9909 − 875 |
| Q06 | 4548 − 2705 |
| Q07 | 3208 − 2063 |
| Q08 | 5909 − 3143 |
| Q09 | 72762 − 60542 |
| Q10 | 590 − 328 |
| Q11 | 70525 − 5484 |
| Q12 | 1182 − 605 |
| Q13 | 850 − 293 |
| Q14 | 705 − 595 |
| Q15 | 2880 − 307 |
| Q16 | 209 − 116 |
| Q17 | 34467 − 12914 |
| Q18 | 7913 − 4071 |
| Q19 | 2768 − 2028 |
| Q20 | 220 − 97 |
| Q21 | 810 − 635 |
| Q22 | 250 − 67 |
| Q23 | 59907 − 39374 |
| Q24 | 720 − 528 |
| Q25 | 92561 − 75190 |
| Q26 | 704 − 334 |
| Q27 | 830 − 227 |
| Q28 | 770 − 485 |
| Q29 | 47552 − 30310 |
| Q30 | 4344 − 2933 |
| Q31 | 409 − 28 |
| Q32 | 880 − 56 |
| Q33 | 480 − 197 |
| Q34 | 3083 − 653 |
| Q35 | 701 − 10 |
| Q36 | 860 − 606 |
| Q37 | 43881 − 29051 |
| Q38 | 230 − 86 |
| Q39 | 9870 − 2513 |
| Q40 | 620 − 446 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
