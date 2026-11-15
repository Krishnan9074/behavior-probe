# Selected Wallace error categories and executable rule mapping

**Source:** Catherine C. Wallace (1984), *A Comparison of Computational Error
Patterns for Grades 3, 5 and 8*, literature review, printed pp. 17–20
(PDF pages 18–21); additional 'smaller-from-larger' category in analysis,
printed pp. 27–32. Original PDF: https://digitalcommons.unf.edu/etd/59/

Wallace discusses **17 numbered types spanning all four operations**. The
selected subset comprises **12 numbered types plus 1 supplementary type**.
The numbers are provenance identifiers, **not** labels agents must predict.

| Label | Wallace error type / interpretation | Executable rule(s) in this project | Operations |
|---|---|---|---|
| W01 | 1. Multiplying vertically | `multiply_vertically` | mul |
| W02 | 2. Adding columns without place value or regrouping | `add_no_regroup` | add |
| W04 | 4. Difficulty with zero or one | `zero_as_one`, `one_as_zero` | add, sub, mul, div |
| W06 | 6. Borrowing when not needed | `borrow_unnecessarily` | sub |
| W08 | 8. Not allowing for having borrowed | `forget_decrement` | sub |
| W09 | 9. Failing to borrow, giving zero | `write_zero` | sub |
| W10 | 10. Failing to add carried number | `drop_carry` | add |
| W11 | 11. Carrying the wrong number | `wrong_carry_amount` | mul |
| W12 | 12. Misplacing columns in multiplication | `partial_products_unshifted` | mul |
| W13 | 13. Omitting zero in quotient | `omit_zero_quotient` | div |
| W15 | 15. Adding single-digit addend to both digits | `single_digit_repeated` | add |
| W16 | 16. Dividing divisor into each digit without partial products | `digitwise_no_remainder` | div |
| EXTRA_SFL | Supplemental: subtracting smaller digit from larger regardless of position | `smaller_from_larger` | sub |

Excluded for now: numbered types 3, 5, 7, 14 and 17. These either overlap with
selected patterns, require more detailed algorithmic or written-layout
semantics, or are lower priority for the current benchmark. They were **not
silently reclassified as included**.

## Three levels of representation

A hidden student is generated from:

```text
Research literature category
  -> our precisely specified executable Python algorithm
     -> a condition (trigger) and/or composition with another bug
        -> an individual simulated student's responses
```

For example:

```json
{"paper_label": "W08", "executable_rule": "forget_decrement", "trigger": "ones_only"}
```

This example is a **metadata illustration**, not an actual field in the
agent-visible test; `paper_label` lives implicitly in the trusted rule
catalog. Agent submissions contain **predicted numeric answers and confidence
only**, never label names.

### Trigger choices

- `any`, `ones_only`, `tens_only`, `next_digit_zero` for most column-local rules.
- `any`, `dividend_has_zero`, `divisor_even` for division rules.
- `any`, `ones_only`, `tens_only` for the two shared input interpretation rules.
- Invalid/no-effect trigger combinations are omitted from the hypothesis
  generator (e.g., whole-answer `add_no_regroup` only has `any`).

### Composition semantics

- Input interpretation (`zero_as_one`/`one_as_zero`) is applied to operands
  **before** the operation-specific arithmetic procedure.
- At most **one** shared interpretation rule may be selected in a student.
- Two different procedural rules may be combined where supported, with the
  evaluator executing the precise deterministic rules in `student.py`.
- Generator rejects 'two-rule' students if sampled inputs show that one of
  the rules is effectively inert in the combination.
- Level 3 applies the **same exact interpretation function and trigger**
  across four operations. Its target operation has no initial observations.

## Important research-validity boundary

These are operationalizations of categories in a literature review, **not**
faithful reconstructions of individual students recorded in 1984. For
instance, W04 is a broad category; treating every `0` as `1` is **our chosen
synthetic deterministic implementation**, not a directly documented typical
student prevalence. Similarly, W16 has been simplified to a fully defined
integer-only per-digit division algorithm. Some raw category names describe
written intermediate work; our single-integer outputs intentionally abstract
away the written procedure.

The project evaluates **black-box behavioral inference over synthetic rules**.
No result should be interpreted as evidence about how an AI predicts real
children or identifies psychological causes.
