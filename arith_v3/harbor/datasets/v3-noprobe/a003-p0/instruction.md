# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 546 + 8 | 1354 |
| 17 × 47 | 187 |
| 88830 − 42121 | 46710 |
| 16180 ÷ 2 | 3040 |
| 5898 − 274 | 5624 |
| 44829 ÷ 3 | 14943 |
| 613 × 7 | 4291 |
| 56616 + 83098 | 139714 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 77 × 71 |
| Q02 | 260181 ÷ 9 |
| Q03 | 869 + 4 |
| Q04 | 69 × 15 |
| Q05 | 7322 + 4 |
| Q06 | 1035 ÷ 5 |
| Q07 | 810819 ÷ 9 |
| Q08 | 93868 + 8 |
| Q09 | 121 + 9 |
| Q10 | 39309 + 4 |
| Q11 | 932 + 89 |
| Q12 | 311328 ÷ 8 |
| Q13 | 7223 × 58 |
| Q14 | 5800 − 1735 |
| Q15 | 2601 − 2338 |
| Q16 | 62741 − 55036 |
| Q17 | 7071 × 14 |
| Q18 | 4041 − 783 |
| Q19 | 136 × 96 |
| Q20 | 3616 ÷ 4 |
| Q21 | 39200 − 2418 |
| Q22 | 69585 + 39298 |
| Q23 | 249 × 57 |
| Q24 | 84 × 82 |
| Q25 | 32184 ÷ 4 |
| Q26 | 31 × 19 |
| Q27 | 16200 ÷ 9 |
| Q28 | 379612 ÷ 4 |
| Q29 | 553 × 52 |
| Q30 | 14505 ÷ 5 |
| Q31 | 77901 − 48188 |
| Q32 | 55361 + 9 |
| Q33 | 10 × 18 |
| Q34 | 64430 + 50707 |
| Q35 | 943 × 24 |
| Q36 | 892 + 956 |
| Q37 | 581 × 98 |
| Q38 | 240401 ÷ 7 |
| Q39 | 651 × 41 |
| Q40 | 5134 + 3120 |
| Q41 | 57 × 37 |
| Q42 | 72041 − 12214 |
| Q43 | 103 × 15 |
| Q44 | 501 − 192 |
| Q45 | 11856 ÷ 2 |
| Q46 | 2184 ÷ 8 |
| Q47 | 36 × 88 |
| Q48 | 44 × 63 |
| Q49 | 31314 + 94095 |
| Q50 | 152020 ÷ 5 |
| Q51 | 78780 + 16412 |
| Q52 | 4030 − 855 |
| Q53 | 99498 + 47743 |
| Q54 | 800 − 666 |
| Q55 | 5865 + 8870 |
| Q56 | 14556 ÷ 2 |
| Q57 | 1520 ÷ 5 |
| Q58 | 4900 − 3595 |
| Q59 | 560616 ÷ 7 |
| Q60 | 616 × 19 |
| Q61 | 26361 − 19202 |
| Q62 | 1257 + 8375 |
| Q63 | 500 − 365 |
| Q64 | 81 × 16 |
| Q65 | 3090 − 126 |
| Q66 | 15836 ÷ 2 |
| Q67 | 2060 − 1565 |
| Q68 | 81940 − 35049 |
| Q69 | 19928 + 2 |
| Q70 | 3021 − 2942 |
| Q71 | 54318 + 2 |
| Q72 | 9793 × 74 |
| Q73 | 21910 ÷ 5 |
| Q74 | 1374 ÷ 2 |
| Q75 | 25501 − 48 |
| Q76 | 18944 ÷ 2 |
| Q77 | 456 + 9 |
| Q78 | 10650 − 4858 |
| Q79 | 9675 + 8 |
| Q80 | 201 − 122 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
