**Case H020.** The hidden rule (never shown to the agent): when a column needs a borrow, the student copies the bottom digit instead of borrowing in the hundreds column or higher; otherwise, borrows from two columns to the left in the ones column. The ideal reasoner gets 55% from the observations alone and 100% with 3 probes.

| Observed | Student wrote | Correct |
|---|---|---|
| 167 − 56 | **111** | 111 |
| 203 − 106 | **7** | 97 |
| 9344 − 6683 | **3661** | 2661 |
| 246 − 63 | **183** | 183 |

**Claude Opus 5.5, no probes: 0%** on the student's errors (0% on 4–5-digit problems). Its conclusion:

> I've written predictions for all 40 problems to `/workspace/submission.json`. The rule I inferred reproduces all four of the student's past answers exactly, but it rests on only two buggy examples, so treat it as a best guess. **The student's likely procedure:** - **Borrowing across a zero:** they skip the zero and take 1 from the next digit to the left, but leave the zero as 0 instead of turning it into 9. That's how 203 − 106 became 7 instead of 97. - **Two borrows in a row:** if a column has already been reduced by 1 because a borrow came out of it, and then that column has to borrow too, …

**Claude Opus 5.5, same case, ≤10 optional probes: 100%** (10 probes). What it asked:

| Probe | Student wrote | Correct |
|---|---|---|
| 5432 − 2678 | **3664** | 2754 |
| 4005 − 1237 | **3278** | 2768 |
| 305 − 107 | **108** | 198 |
| 7321 − 2456 | **5475** | 4865 |
| 1000 − 1 | **1009** | 999 |
| 432 − 178 | **164** | 254 |
| 5732 − 2178 | **3464** | 3554 |
| 5378 − 1612 | **4666** | 3766 |
| 13512 − 4201 | **14311** | 9311 |
| 62000 − 1 | **62009** | 61999 |

> I wrote predictions for all 40 questions to `/workspace/submission.json`. I used all 10 probes. The rule I worked out matches every known answer: the 4 given ones and the 10 probes. **The student's rule:** - **Ones and tens columns:** When the top digit is smaller, the student borrows correctly and works out 10 + top − bottom. But the borrow is always taken from the **hundreds** digit, never from the column next door. So a borrow in the ones column skips the tens digit, and every borrow lowers the hundreds digit by one. - **Hundreds column and higher:** When the top digit (after any borrows …

**Claude Sonnet 5.5, same case, same optional probes:** 0 probes, **0%**.

> I wrote `/workspace/submission.json` with all 40 predictions. I didn't use the `probe` tool, so every prediction rests on the four past answers. **What the student seems to do:** three of the four past answers are correct, so I assumed correct subtraction by default. The exception is 203 − 106, where the student gave 7 instead of 97. My guess is that when a borrow has to come from a zero digit, …

The four observations fit many rules. Without probes, the model picked one and applied it confidently. With probes, it tested the rule on new problems and corrected it. The benchmark measures that difference.
