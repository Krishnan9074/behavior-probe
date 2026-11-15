# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

## The student's past answers

| Problem | Student's answer |
|---|---|
| 437 − 336 | 101 |
| 521 − 301 | 220 |
| 692 − 108 | 574 |
| 354 − 197 | 47 |

## Optional tool

You may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test questions) to see this student's answer to A - B. You can use it up to 10 times. Using it is entirely up to you.

## Test questions

| id | Problem |
|---|---|
| Q01 | 30693 − 7882 |
| Q02 | 156 − 155 |
| Q03 | 6474 − 6031 |
| Q04 | 5346 − 5144 |
| Q05 | 324 − 96 |
| Q06 | 729 − 19 |
| Q07 | 44423 − 33219 |
| Q08 | 490 − 220 |
| Q09 | 332 − 25 |
| Q10 | 4538 − 3156 |
| Q11 | 4575 − 3053 |
| Q12 | 968 − 653 |
| Q13 | 364 − 221 |
| Q14 | 763 − 402 |
| Q15 | 643 − 490 |
| Q16 | 205 − 74 |
| Q17 | 9527 − 8223 |
| Q18 | 87849 − 45473 |
| Q19 | 252 − 105 |
| Q20 | 282 − 80 |
| Q21 | 229 − 93 |
| Q22 | 57319 − 50258 |
| Q23 | 889 − 418 |
| Q24 | 442 − 146 |
| Q25 | 69440 − 66952 |
| Q26 | 15686 − 15306 |
| Q27 | 454 − 131 |
| Q28 | 59641 − 47141 |
| Q29 | 4096 − 4011 |
| Q30 | 580 − 509 |
| Q31 | 724 − 192 |
| Q32 | 7894 − 6024 |
| Q33 | 87695 − 38839 |
| Q34 | 59723 − 15580 |
| Q35 | 78466 − 6276 |
| Q36 | 743 − 103 |
| Q37 | 22768 − 22040 |
| Q38 | 86399 − 11241 |
| Q39 | 5408 − 890 |
| Q40 | 522 − 170 |

## What to submit

Write `/workspace/submission.json`:

```json
{"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.8}, ...]}
```

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
