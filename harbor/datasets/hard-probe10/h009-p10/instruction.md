# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 770 − 98 | 772 |
| 267 − 68 | 299 |
| 4073 − 1668 | 2405 |
| 7529 − 2010 | 5519 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 782 − 149 |
| Q02 | 31181 − 29614 |
| Q03 | 6033 − 5149 |
| Q04 | 351 − 202 |
| Q05 | 66097 − 57676 |
| Q06 | 202 − 175 |
| Q07 | 71791 − 2986 |
| Q08 | 648 − 521 |
| Q09 | 959 − 568 |
| Q10 | 89768 − 86887 |
| Q11 | 53010 − 9710 |
| Q12 | 102 − 43 |
| Q13 | 259 − 198 |
| Q14 | 817 − 723 |
| Q15 | 65297 − 59594 |
| Q16 | 133 − 72 |
| Q17 | 884 − 534 |
| Q18 | 51302 − 14382 |
| Q19 | 92368 − 17920 |
| Q20 | 795 − 280 |
| Q21 | 6203 − 3557 |
| Q22 | 5904 − 2183 |
| Q23 | 66351 − 49726 |
| Q24 | 833 − 512 |
| Q25 | 915 − 275 |
| Q26 | 29659 − 7162 |
| Q27 | 732 − 512 |
| Q28 | 8927 − 3442 |
| Q29 | 63155 − 36305 |
| Q30 | 80195 − 42224 |
| Q31 | 642 − 26 |
| Q32 | 151 − 124 |
| Q33 | 41498 − 38905 |
| Q34 | 86011 − 49117 |
| Q35 | 1813 − 253 |
| Q36 | 519 − 346 |
| Q37 | 649 − 322 |
| Q38 | 909 − 851 |
| Q39 | 54195 − 14831 |
| Q40 | 248 − 82 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
