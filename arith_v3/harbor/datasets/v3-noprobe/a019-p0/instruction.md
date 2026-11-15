# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (+ only). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 333 + 434 | 767 |
| 4517 + 4 | 4511 |
| 548 + 982 | 420 |
| 5303 + 4456 | 9759 |
| 441 + 306 | 747 |
| 337 + 303 | 630 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 9090 + 415 |
| Q02 | 382 + 610 |
| Q03 | 544 + 545 |
| Q04 | 5892 + 6202 |
| Q05 | 600 + 142 |
| Q06 | 9200 + 5613 |
| Q07 | 6981 + 6895 |
| Q08 | 4802 + 9482 |
| Q09 | 851 + 2 |
| Q10 | 435 + 560 |
| Q11 | 104 + 324 |
| Q12 | 3486 + 9960 |
| Q13 | 7745 + 1 |
| Q14 | 2911 + 3027 |
| Q15 | 4876 + 4372 |
| Q16 | 836 + 735 |
| Q17 | 4098 + 8184 |
| Q18 | 3628 + 842 |
| Q19 | 732 + 99 |
| Q20 | 8467 + 7172 |
| Q21 | 2232 + 1 |
| Q22 | 874 + 4 |
| Q23 | 1520 + 2 |
| Q24 | 8806 + 4166 |
| Q25 | 6977 + 4050 |
| Q26 | 179 + 923 |
| Q27 | 511 + 592 |
| Q28 | 1613 + 1 |
| Q29 | 664 + 2 |
| Q30 | 7261 + 1631 |
| Q31 | 2123 + 2 |
| Q32 | 882 + 2 |
| Q33 | 4170 + 4 |
| Q34 | 7592 + 5806 |
| Q35 | 5034 + 339 |
| Q36 | 8767 + 8465 |
| Q37 | 3104 + 2203 |
| Q38 | 3050 + 1 |
| Q39 | 7194 + 5 |
| Q40 | 632 + 7 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
