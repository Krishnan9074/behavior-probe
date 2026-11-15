# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (÷ only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 37933 ÷ 7 | 5419 |
| 27624 ÷ 6 | 1100 |
| 1212 ÷ 6 | 0 |
| 1622 ÷ 2 | 311 |
| 29925 ÷ 5 | 5985 |
| 82485 ÷ 9 | 9165 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 31500 ÷ 7 |
| Q02 | 2525 ÷ 5 |
| Q03 | 990 ÷ 3 |
| Q04 | 65200 ÷ 8 |
| Q05 | 81828 ÷ 9 |
| Q06 | 43176 ÷ 6 |
| Q07 | 2007 ÷ 9 |
| Q08 | 404 ÷ 4 |
| Q09 | 1510 ÷ 5 |
| Q10 | 12160 ÷ 4 |
| Q11 | 4872 ÷ 6 |
| Q12 | 21154 ÷ 7 |
| Q13 | 12400 ÷ 8 |
| Q14 | 1448 ÷ 2 |
| Q15 | 25075 ÷ 5 |
| Q16 | 8439 ÷ 3 |
| Q17 | 3650 ÷ 5 |
| Q18 | 6108 ÷ 2 |
| Q19 | 4872 ÷ 8 |
| Q20 | 6324 ÷ 6 |
| Q21 | 22524 ÷ 4 |
| Q22 | 2128 ÷ 7 |
| Q23 | 25914 ÷ 7 |
| Q24 | 49812 ÷ 6 |
| Q25 | 47505 ÷ 5 |
| Q26 | 3154 ÷ 2 |
| Q27 | 10500 ÷ 3 |
| Q28 | 16506 ÷ 3 |
| Q29 | 3117 ÷ 3 |
| Q30 | 15636 ÷ 6 |
| Q31 | 1881 ÷ 9 |
| Q32 | 4977 ÷ 9 |
| Q33 | 4812 ÷ 6 |
| Q34 | 2592 ÷ 6 |
| Q35 | 24212 ÷ 4 |
| Q36 | 2424 ÷ 3 |
| Q37 | 50736 ÷ 6 |
| Q38 | 820 ÷ 4 |
| Q39 | 12018 ÷ 2 |
| Q40 | 11410 ÷ 2 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
