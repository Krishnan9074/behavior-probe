# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 5894 − 906 | 4898 |
| 898 − 611 | 287 |
| 8905 − 2674 | 6371 |
| 258 − 100 | 158 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 1152 − 995 |
| Q02 | 8170 − 2764 |
| Q03 | 479 − 84 |
| Q04 | 8720 − 3966 |
| Q05 | 830 − 483 |
| Q06 | 95137 − 63889 |
| Q07 | 6831 − 3050 |
| Q08 | 42100 − 9128 |
| Q09 | 120 − 6 |
| Q10 | 710 − 386 |
| Q11 | 72159 − 28762 |
| Q12 | 99853 − 79982 |
| Q13 | 437 − 79 |
| Q14 | 88952 − 9886 |
| Q15 | 169 − 76 |
| Q16 | 231 − 98 |
| Q17 | 519 − 470 |
| Q18 | 616 − 248 |
| Q19 | 510 − 346 |
| Q20 | 545 − 54 |
| Q21 | 3148 − 2176 |
| Q22 | 519 − 362 |
| Q23 | 2824 − 2663 |
| Q24 | 9733 − 8341 |
| Q25 | 1951 − 1090 |
| Q26 | 119 − 95 |
| Q27 | 8988 − 3298 |
| Q28 | 621 − 380 |
| Q29 | 2784 − 590 |
| Q30 | 958 − 68 |
| Q31 | 28243 − 4665 |
| Q32 | 7312 − 375 |
| Q33 | 870 − 848 |
| Q34 | 6039 − 1229 |
| Q35 | 356 − 179 |
| Q36 | 8273 − 3190 |
| Q37 | 759 − 93 |
| Q38 | 49523 − 5478 |
| Q39 | 539 − 45 |
| Q40 | 841 − 583 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
