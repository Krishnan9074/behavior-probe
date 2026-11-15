# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 448 − 23 | 425 |
| 96 × 22 | 2002 |
| 502 + 592 | 1094 |
| 6018 + 5792 | 11800 |
| 201 × 56 | 11256 |
| 362635 ÷ 7 | 51805 |
| 9720 − 1851 | 7870 |
| 3861 ÷ 9 | 428 |

## Test questions

| id | Problem |
|---|---|
| Q01 | 1611 + 7494 |
| Q02 | 711 ÷ 3 |
| Q03 | 398 + 2 |
| Q04 | 105256 ÷ 8 |
| Q05 | 849 × 10 |
| Q06 | 63 × 5 |
| Q07 | 608 + 839 |
| Q08 | 82034 + 77449 |
| Q09 | 97 × 7 |
| Q10 | 38 × 55 |
| Q11 | 2091 − 253 |
| Q12 | 152031 ÷ 3 |
| Q13 | 16131 ÷ 3 |
| Q14 | 16961 ÷ 7 |
| Q15 | 350 − 307 |
| Q16 | 798 + 836 |
| Q17 | 2926 + 295 |
| Q18 | 190211 ÷ 7 |
| Q19 | 1289 + 8576 |
| Q20 | 2121 ÷ 3 |
| Q21 | 301 − 115 |
| Q22 | 26031 − 5524 |
| Q23 | 2352 × 4 |
| Q24 | 12070 − 10896 |
| Q25 | 6237 × 6 |
| Q26 | 1635 ÷ 5 |
| Q27 | 22559 + 6 |
| Q28 | 95160 − 47045 |
| Q29 | 371 + 709 |
| Q30 | 928 + 8 |
| Q31 | 14231 ÷ 7 |
| Q32 | 37 × 73 |
| Q33 | 32 × 31 |
| Q34 | 51791 − 16013 |
| Q35 | 1231 × 91 |
| Q36 | 9970 − 4058 |
| Q37 | 432 × 4 |
| Q38 | 941 × 29 |
| Q39 | 9890 − 3707 |
| Q40 | 19002 ÷ 2 |
| Q41 | 4101 − 3356 |
| Q42 | 100 − 55 |
| Q43 | 6314 ÷ 7 |
| Q44 | 816 + 431 |
| Q45 | 192468 ÷ 4 |
| Q46 | 83049 + 10176 |
| Q47 | 1021 − 677 |
| Q48 | 9511 − 1044 |
| Q49 | 1887 ÷ 3 |
| Q50 | 6038 + 1827 |
| Q51 | 935 × 5 |
| Q52 | 1326 ÷ 6 |
| Q53 | 16540 − 10707 |
| Q54 | 6923 × 53 |
| Q55 | 46 × 5 |
| Q56 | 3892 × 52 |
| Q57 | 22302 + 64408 |
| Q58 | 51820 − 37306 |
| Q59 | 7112 × 12 |
| Q60 | 648 + 152 |
| Q61 | 61628 + 35302 |
| Q62 | 40635 + 7 |
| Q63 | 21161 ÷ 7 |
| Q64 | 7075 + 1408 |
| Q65 | 3005 + 5878 |
| Q66 | 5391 − 4034 |
| Q67 | 6533 × 84 |
| Q68 | 16227 ÷ 9 |
| Q69 | 5093 × 2 |
| Q70 | 263 × 10 |
| Q71 | 60001 − 46775 |
| Q72 | 44112 ÷ 6 |
| Q73 | 158406 ÷ 6 |
| Q74 | 98620 − 80692 |
| Q75 | 9080 − 2553 |
| Q76 | 61 × 61 |
| Q77 | 4112 + 845 |
| Q78 | 71981 ÷ 7 |
| Q79 | 514521 ÷ 9 |
| Q80 | 12031 − 7115 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
