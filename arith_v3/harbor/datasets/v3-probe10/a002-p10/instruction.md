# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic (all four operations: +, −, ×, ÷). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.

**Note:** there are no past answers for **÷** (`div`), but test questions include it.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 4207 × 2 | 8414 |
| 964 × 91 | 86760 |
| 4624 − 3690 | 934 |
| 450 + 8 | 458 |

## Optional tool

You may run `probe OP A B` (OP is `add`, `sub`, `mul` or `div`) to see this student's integer
answer to a new problem, e.g. `probe sub 502 178`. Operands are integers 0 to 1,000,000; for `sub`
A ≥ B; for `div` B divides A exactly and B > 0. You cannot probe the test questions. You can use
it up to 10 times. Using it is entirely up to you.

To record your progress, run `snapshot` (it sends `/workspace/submission.json`) once before your
first probe and again after each probe. It stores your predictions and never shows you a score.

## Test questions

| id | Problem |
|---|---|
| Q01 | 688 − 14 |
| Q02 | 304806 ÷ 6 |
| Q03 | 415 × 24 |
| Q04 | 873 + 6 |
| Q05 | 11892 ÷ 4 |
| Q06 | 89600 − 84215 |
| Q07 | 6684 − 5656 |
| Q08 | 22148 − 3155 |
| Q09 | 32490 ÷ 6 |
| Q10 | 3185 × 4 |
| Q11 | 6773 − 3026 |
| Q12 | 5111 − 4625 |
| Q13 | 1215 ÷ 3 |
| Q14 | 44807 ÷ 7 |
| Q15 | 226404 ÷ 4 |
| Q16 | 34446 − 6943 |
| Q17 | 516 × 8 |
| Q18 | 6586 × 9 |
| Q19 | 324 + 479 |
| Q20 | 19644 + 63024 |
| Q21 | 278469 ÷ 3 |
| Q22 | 609 × 44 |
| Q23 | 70363 + 71042 |
| Q24 | 4573 × 3 |
| Q25 | 23686 + 4889 |
| Q26 | 541917 ÷ 9 |
| Q27 | 608797 ÷ 7 |
| Q28 | 12382 − 9956 |
| Q29 | 93786 − 80523 |
| Q30 | 91590 + 94145 |
| Q31 | 4685 × 49 |
| Q32 | 38482 + 62828 |
| Q33 | 46200 ÷ 7 |
| Q34 | 813 − 134 |
| Q35 | 677 − 295 |
| Q36 | 100 × 6 |
| Q37 | 62319 + 92563 |
| Q38 | 808 × 9 |
| Q39 | 5750 + 4109 |
| Q40 | 167 × 28 |
| Q41 | 78980 + 77289 |
| Q42 | 185574 ÷ 6 |
| Q43 | 9566 − 7338 |
| Q44 | 814 − 19 |
| Q45 | 98160 + 7 |
| Q46 | 375228 ÷ 7 |
| Q47 | 71501 + 98022 |
| Q48 | 37894 + 69835 |
| Q49 | 2303 − 2246 |
| Q50 | 912 × 6 |
| Q51 | 27977 + 5 |
| Q52 | 437 − 189 |
| Q53 | 212716 ÷ 4 |
| Q54 | 11436 ÷ 6 |
| Q55 | 802 + 962 |
| Q56 | 1876 + 946 |
| Q57 | 92 × 80 |
| Q58 | 1558 × 8 |
| Q59 | 7397 − 546 |
| Q60 | 18981 ÷ 9 |
| Q61 | 493 − 18 |
| Q62 | 4235 × 6 |
| Q63 | 42274 − 20159 |
| Q64 | 67 × 42 |
| Q65 | 648 ÷ 6 |
| Q66 | 85463 − 17024 |
| Q67 | 6164 − 4659 |
| Q68 | 52 × 80 |
| Q69 | 14 × 5 |
| Q70 | 1423 × 7 |
| Q71 | 8206 ÷ 2 |
| Q72 | 9344 + 9082 |
| Q73 | 13015 ÷ 5 |
| Q74 | 16 × 25 |
| Q75 | 134 + 8 |
| Q76 | 530 + 5 |
| Q77 | 68591 + 12443 |
| Q78 | 616048 ÷ 8 |
| Q79 | 7262 × 4 |
| Q80 | 104098 ÷ 2 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 80 ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
