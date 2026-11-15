# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (÷ only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 808 ÷ 2 | 44 |
| 12096 ÷ 6 | 216 |
| 37756 ÷ 4 | 9439 |
| 57704 ÷ 8 | 7213 |
| 2712 ÷ 3 | 94 |
| 2880 ÷ 9 | 320 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 6839 ÷ 7 |
| Q02 | 40570 ÷ 5 |
| Q03 | 418 ÷ 2 |
| Q04 | 534 ÷ 2 |
| Q05 | 600 ÷ 2 |
| Q06 | 47346 ÷ 6 |
| Q07 | 36252 ÷ 4 |
| Q08 | 29632 ÷ 4 |
| Q09 | 58383 ÷ 9 |
| Q10 | 7299 ÷ 9 |
| Q11 | 7232 ÷ 8 |
| Q12 | 28930 ÷ 5 |
| Q13 | 5490 ÷ 6 |
| Q14 | 2905 ÷ 5 |
| Q15 | 894 ÷ 3 |
| Q16 | 66825 ÷ 9 |
| Q17 | 1708 ÷ 2 |
| Q18 | 545 ÷ 5 |
| Q19 | 18068 ÷ 4 |
| Q20 | 18735 ÷ 5 |
| Q21 | 2535 ÷ 5 |
| Q22 | 5442 ÷ 6 |
| Q23 | 7458 ÷ 3 |
| Q24 | 1220 ÷ 4 |
| Q25 | 15010 ÷ 2 |
| Q26 | 1078 ÷ 2 |
| Q27 | 610 ÷ 2 |
| Q28 | 54378 ÷ 6 |
| Q29 | 4728 ÷ 4 |
| Q30 | 12232 ÷ 4 |
| Q31 | 4040 ÷ 8 |
| Q32 | 1600 ÷ 4 |
| Q33 | 1608 ÷ 8 |
| Q34 | 6280 ÷ 8 |
| Q35 | 36186 ÷ 6 |
| Q36 | 20056 ÷ 8 |
| Q37 | 17790 ÷ 5 |
| Q38 | 3688 ÷ 4 |
| Q39 | 12068 ÷ 2 |
| Q40 | 8096 ÷ 4 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
