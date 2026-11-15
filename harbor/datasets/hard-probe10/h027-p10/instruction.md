# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 4859 − 334 | 4525 |
| 2953 − 113 | 2840 |
| 6703 − 4572 | 1231 |
| 320 − 14 | 216 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 363 − 322 |
| Q02 | 82249 − 45204 |
| Q03 | 682 − 102 |
| Q04 | 8174 − 799 |
| Q05 | 9152 − 2112 |
| Q06 | 3798 − 2642 |
| Q07 | 49248 − 19969 |
| Q08 | 931 − 425 |
| Q09 | 694 − 631 |
| Q10 | 486 − 130 |
| Q11 | 8585 − 4552 |
| Q12 | 9844 − 5017 |
| Q13 | 507 − 307 |
| Q14 | 299 − 223 |
| Q15 | 21110 − 16116 |
| Q16 | 1458 − 1156 |
| Q17 | 491 − 187 |
| Q18 | 59978 − 41962 |
| Q19 | 707 − 209 |
| Q20 | 5884 − 1701 |
| Q21 | 883 − 757 |
| Q22 | 74945 − 2923 |
| Q23 | 569 − 132 |
| Q24 | 27899 − 23349 |
| Q25 | 386 − 14 |
| Q26 | 281 − 33 |
| Q27 | 411 − 408 |
| Q28 | 715 − 7 |
| Q29 | 421 − 0 |
| Q30 | 81541 − 598 |
| Q31 | 99619 − 67393 |
| Q32 | 87577 − 34345 |
| Q33 | 846 − 327 |
| Q34 | 281 − 2 |
| Q35 | 67074 − 36756 |
| Q36 | 979 − 500 |
| Q37 | 422 − 228 |
| Q38 | 14813 − 11908 |
| Q39 | 81350 − 34179 |
| Q40 | 4798 − 3756 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
