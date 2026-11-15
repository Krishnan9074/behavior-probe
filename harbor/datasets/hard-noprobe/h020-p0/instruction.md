# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 167 − 56 | 111 |
| 203 − 106 | 7 |
| 9344 − 6683 | 3661 |
| 246 − 63 | 183 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 27797 − 22722 |
| Q02 | 470 − 235 |
| Q03 | 281 − 218 |
| Q04 | 234 − 121 |
| Q05 | 557 − 500 |
| Q06 | 22648 − 20712 |
| Q07 | 499 − 52 |
| Q08 | 876 − 703 |
| Q09 | 8579 − 5108 |
| Q10 | 106 − 14 |
| Q11 | 7084 − 2034 |
| Q12 | 145 − 102 |
| Q13 | 6199 − 49 |
| Q14 | 9891 − 6836 |
| Q15 | 15773 − 122 |
| Q16 | 9493 − 9412 |
| Q17 | 232 − 33 |
| Q18 | 9682 − 3266 |
| Q19 | 947 − 290 |
| Q20 | 79226 − 40124 |
| Q21 | 6152 − 1724 |
| Q22 | 684 − 168 |
| Q23 | 9487 − 4204 |
| Q24 | 491 − 174 |
| Q25 | 641 − 393 |
| Q26 | 615 − 315 |
| Q27 | 350 − 93 |
| Q28 | 54855 − 53145 |
| Q29 | 2086 − 1506 |
| Q30 | 5249 − 2905 |
| Q31 | 567 − 377 |
| Q32 | 2099 − 1140 |
| Q33 | 890 − 251 |
| Q34 | 80987 − 12786 |
| Q35 | 243 − 28 |
| Q36 | 625 − 38 |
| Q37 | 3381 − 954 |
| Q38 | 769 − 53 |
| Q39 | 6052 − 2373 |
| Q40 | 1261 − 181 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
