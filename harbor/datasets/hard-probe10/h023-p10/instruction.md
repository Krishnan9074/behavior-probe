# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 689 − 32 | 657 |
| 337 − 202 | 135 |
| 861 − 764 | 107 |
| 9052 − 3183 | 6079 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 75358 − 65763 |
| Q02 | 5243 − 455 |
| Q03 | 8328 − 450 |
| Q04 | 81598 − 45019 |
| Q05 | 267 − 188 |
| Q06 | 925 − 578 |
| Q07 | 640 − 354 |
| Q08 | 81048 − 45060 |
| Q09 | 78932 − 12473 |
| Q10 | 363 − 290 |
| Q11 | 708 − 558 |
| Q12 | 415 − 279 |
| Q13 | 550 − 257 |
| Q14 | 6903 − 4247 |
| Q15 | 869 − 95 |
| Q16 | 51782 − 5382 |
| Q17 | 323 − 143 |
| Q18 | 4334 − 2254 |
| Q19 | 927 − 776 |
| Q20 | 452 − 266 |
| Q21 | 3415 − 2645 |
| Q22 | 62437 − 20447 |
| Q23 | 25250 − 22481 |
| Q24 | 19259 − 17740 |
| Q25 | 9649 − 868 |
| Q26 | 1800 − 846 |
| Q27 | 937 − 845 |
| Q28 | 64407 − 23278 |
| Q29 | 234 − 81 |
| Q30 | 2590 − 2462 |
| Q31 | 8742 − 5158 |
| Q32 | 9677 − 3914 |
| Q33 | 526 − 236 |
| Q34 | 171 − 91 |
| Q35 | 111 − 28 |
| Q36 | 463 − 70 |
| Q37 | 53599 − 28406 |
| Q38 | 611 − 135 |
| Q39 | 939 − 444 |
| Q40 | 245 − 186 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
