# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 4210 − 3909 | 1310 |
| 4244 − 2809 | 2440 |
| 846 − 606 | 240 |
| 616 − 515 | 101 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 4144 − 3285 |
| Q02 | 6205 − 2757 |
| Q03 | 4799 − 3491 |
| Q04 | 367 − 120 |
| Q05 | 450 − 173 |
| Q06 | 104 − 97 |
| Q07 | 9492 − 6843 |
| Q08 | 695 − 301 |
| Q09 | 887 − 156 |
| Q10 | 57299 − 32127 |
| Q11 | 411 − 173 |
| Q12 | 47783 − 1280 |
| Q13 | 1297 − 162 |
| Q14 | 318 − 263 |
| Q15 | 467 − 166 |
| Q16 | 9694 − 7490 |
| Q17 | 4806 − 2793 |
| Q18 | 5448 − 2212 |
| Q19 | 1349 − 103 |
| Q20 | 42308 − 27635 |
| Q21 | 6899 − 5893 |
| Q22 | 710 − 204 |
| Q23 | 59930 − 25649 |
| Q24 | 649 − 221 |
| Q25 | 5671 − 4470 |
| Q26 | 483 − 71 |
| Q27 | 59396 − 22557 |
| Q28 | 191 − 85 |
| Q29 | 298 − 190 |
| Q30 | 306 − 69 |
| Q31 | 632 − 124 |
| Q32 | 6932 − 656 |
| Q33 | 30189 − 7581 |
| Q34 | 42736 − 42414 |
| Q35 | 861 − 203 |
| Q36 | 342 − 131 |
| Q37 | 785 − 53 |
| Q38 | 65383 − 21792 |
| Q39 | 652 − 423 |
| Q40 | 111 − 10 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
