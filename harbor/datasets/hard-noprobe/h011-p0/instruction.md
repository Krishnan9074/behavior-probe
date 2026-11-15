# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 7472 − 2949 | 5533 |
| 483 − 70 | 413 |
| 287 − 9 | 288 |
| 958 − 734 | 224 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 46110 − 11045 |
| Q02 | 10770 − 225 |
| Q03 | 88182 − 35558 |
| Q04 | 665 − 506 |
| Q05 | 8118 − 7387 |
| Q06 | 49354 − 12945 |
| Q07 | 482 − 126 |
| Q08 | 5721 − 5479 |
| Q09 | 2442 − 818 |
| Q10 | 400 − 151 |
| Q11 | 95842 − 35625 |
| Q12 | 826 − 469 |
| Q13 | 5189 − 4799 |
| Q14 | 9850 − 6665 |
| Q15 | 831 − 732 |
| Q16 | 610 − 472 |
| Q17 | 1707 − 211 |
| Q18 | 263 − 24 |
| Q19 | 515 − 98 |
| Q20 | 8881 − 7970 |
| Q21 | 647 − 479 |
| Q22 | 4203 − 4063 |
| Q23 | 460 − 77 |
| Q24 | 7943 − 1336 |
| Q25 | 335 − 282 |
| Q26 | 109 − 13 |
| Q27 | 3723 − 3686 |
| Q28 | 420 − 161 |
| Q29 | 313 − 47 |
| Q30 | 362 − 353 |
| Q31 | 67351 − 33212 |
| Q32 | 16658 − 791 |
| Q33 | 8708 − 6433 |
| Q34 | 540 − 163 |
| Q35 | 86020 − 35895 |
| Q36 | 604 − 520 |
| Q37 | 38629 − 25334 |
| Q38 | 144 − 90 |
| Q39 | 206 − 154 |
| Q40 | 656 − 496 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
