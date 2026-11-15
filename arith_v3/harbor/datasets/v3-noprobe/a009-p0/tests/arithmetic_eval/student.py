"""Deterministic arithmetic behavior simulator. TRUSTED SIDE ONLY.

Wallace (1984), pp. 17-20 (printed), synthesizes error types from earlier
literature. The classifications provide provenance; the precise algorithms,
triggers and combinations are OUR engineering operationalizations. They have
not been validated as individual-level cognitive models or population rates.
"""
from __future__ import annotations
from itertools import combinations

OPS = ("add", "sub", "mul", "div")
OP_SYMBOL = {"add": "+", "sub": "-", "mul": "*", "div": "/"}

# Exactly the selected 12 Wallace-numbered categories + the independently
# reported 'smaller from larger' category (not one of the original 17).
SELECTED_LABELS = {
    "W01": "Multiplying vertically",
    "W02": "Adding columns without place value or regrouping",
    "W04": "Difficulty with zero or one",
    "W06": "Borrowing when not needed",
    "W08": "Not allowing for having borrowed",
    "W09": "Failing to borrow and giving zero",
    "W10": "Failing to add carried number",
    "W11": "Carrying the wrong number",
    "W12": "Misplacing columns in multiplication",
    "W13": "Omitting zero in quotient",
    "W15": "Adding single-digit addend to both columns",
    "W16": "Dividing into each digit without partial products",
    "EXTRA_SFL": "Subtracting smaller from larger regardless of position",
}

# label, operational definition. Per-rule triggers create many possible models.
RULES = {
    "add": {
        "add_no_regroup": ("W02", "Write each column sum in sequence, without carrying; e.g. 58+83 -> 1311."),
        "drop_carry": ("W10", "Discard outgoing carry in vertical addition."),
        "single_digit_repeated": ("W15", "When adding a one-digit number, apply it in each existing column."),
        "zero_as_one": ("W04", "Read selected written zero digits as one before calculating."),
        "one_as_zero": ("W04", "Read selected written one digits as zero before calculating."),
    },
    "sub": {
        "smaller_from_larger": ("EXTRA_SFL", "Subtract smaller column digit from larger rather than borrow."),
        "forget_decrement": ("W08", "Complete the borrow but fail to decrement the next column."),
        "write_zero": ("W09", "Write zero rather than borrow when top digit is too small."),
        "borrow_unnecessarily": ("W06", "Borrow from the next column even when unneeded."),
        "zero_as_one": ("W04", "Read selected written zero digits as one before calculating."),
        "one_as_zero": ("W04", "Read selected written one digits as zero before calculating."),
    },
    "mul": {
        "multiply_vertically": ("W01", "Treat aligned digits as independent products; simplified implementation."),
        "wrong_carry_amount": ("W11", "Reduce nonzero outgoing multiplication carry by one."),
        "partial_products_unshifted": ("W12", "Shift later multiplication partial products one column too little."),
        "zero_as_one": ("W04", "Read selected written zero digits as one before calculating."),
        "one_as_zero": ("W04", "Read selected written one digits as zero before calculating."),
    },
    "div": {
        "omit_zero_quotient": ("W13", "Delete internal zeros of a multi-digit quotient."),
        "digitwise_no_remainder": ("W16", "Divide each digit by divisor ignoring all remainders."),
        "zero_as_one": ("W04", "Read selected written zero digits as one before calculating."),
        "one_as_zero": ("W04", "Read selected written one digits as zero before calculating."),
    },
}

# Source-wide rules below are the same input-transform algorithm across +,-,*,/
SHARED_RULES = ("zero_as_one", "one_as_zero")
LOCAL_TRIGGERS = ("any", "ones_only", "tens_only", "next_digit_zero")
DIV_TRIGGERS = ("any", "dividend_has_zero", "divisor_even")
SHARED_TRIGGERS = ("any", "ones_only", "tens_only")


def allowed_triggers(op: str, name: str | None = None) -> tuple[str, ...]:
    if name in SHARED_RULES:
        return SHARED_TRIGGERS
    if name == "add_no_regroup":
        return ("any",)
    if name in {"single_digit_repeated", "partial_products_unshifted"}:
        return ("any", "tens_only", "next_digit_zero")
    return DIV_TRIGGERS if op == "div" else LOCAL_TRIGGERS


def digits(n: int, width: int) -> list[int]:
    return [(n // (10 ** i)) % 10 for i in range(width)]


def ints(ds: list[int]) -> int:
    return sum(int(d) * (10 ** i) for i, d in enumerate(ds))


def local_active(trigger: str, i: int, upper: int) -> bool:
    if trigger == "any": return True
    if trigger == "ones_only": return i == 0
    if trigger == "tens_only": return i == 1
    if trigger == "next_digit_zero": return upper == 0
    raise ValueError(trigger)


def div_active(trigger: str, a: int, b: int) -> bool:
    if trigger == "any": return True
    if trigger == "dividend_has_zero": return "0" in str(a)
    if trigger == "divisor_even": return b % 2 == 0
    raise ValueError(trigger)


def validate_rules(op: str, rules: list[dict]) -> None:
    if op not in OPS: raise ValueError("Unknown operation")
    names = set()
    for r in rules:
        if r["name"] not in RULES[op]: raise ValueError("Unknown error rule")
        if r["name"] in names: raise ValueError("Duplicate rule")
        if r["trigger"] not in allowed_triggers(op, r["name"]): raise ValueError("Invalid trigger")
        names.add(r["name"])
    if len([r for r in rules if r["name"] in SHARED_RULES]) > 1:
        raise ValueError("Conflicting input-interpretation rules")


def correct(op: str, a: int, b: int) -> int:
    if op == "add": return a + b
    if op == "sub": return a - b
    if op == "mul": return a * b
    if op == "div":
        if b <= 0 or a % b: raise ValueError("Only exact positive division")
        return a // b
    raise ValueError(op)


def _active(rules: list[dict], name: str, i: int, upper: int) -> bool:
    return any(r["name"] == name and local_active(r["trigger"], i, upper) for r in rules)


def _change_digits(n: int, name: str, trigger: str) -> int:
    ds = digits(n, len(str(n)))
    target, replacement = (0, 1) if name == "zero_as_one" else (1, 0)
    for i in range(len(ds)):
        upper = ds[i + 1] if i + 1 < len(ds) else 0
        if ds[i] == target and local_active(trigger, i, upper):
            ds[i] = replacement
    return ints(ds)


def _addition(a: int, b: int, rules: list[dict]) -> int:
    width = max(len(str(a)), len(str(b))) + 3
    da, db = digits(a, width), digits(b, width)
    # Independent column sums concatenated from most to least significant.
    if _active(rules, "add_no_regroup", 0, da[1]):
        sums = [da[i] + db[i] for i in reversed(range(max(len(str(a)), len(str(b)))))]
        return int("".join(map(str, sums)))
    out, carry = [], 0
    for i in range(width):
        upper = da[i + 1] if i + 1 < width else 0
        y = db[i]
        if b < 10 and i > 0 and i < len(str(a)) and _active(rules, "single_digit_repeated", i, upper):
            y = b
        raw = da[i] + y + carry
        out.append(raw % 10)
        carry = 0 if _active(rules, "drop_carry", i, upper) else raw // 10
    return ints(out)


def _subtraction(a: int, b: int, rules: list[dict]) -> int:
    width = max(len(str(a)), len(str(b))) + 3
    da, db = digits(a, width), digits(b, width)
    out, borrow = [], 0
    for i in range(width):
        upper = da[i + 1] if i + 1 < width else 0
        top, bottom = da[i] - borrow, db[i]
        if top < bottom:
            if _active(rules, "smaller_from_larger", i, upper):
                out.append(bottom - max(0, top))
                borrow = 0
            elif _active(rules, "write_zero", i, upper):
                out.append(0)
                borrow = 0
            else:
                out.append((top + 10 - bottom) % 10)
                borrow = 0 if _active(rules, "forget_decrement", i, upper) else 1
        else:
            out.append(top - bottom)
            borrow = int(top > 0 and i + 1 < len(str(a)) and _active(rules, "borrow_unnecessarily", i, upper))
    return ints(out)


def _multiplication(a: int, b: int, rules: list[dict]) -> int:
    da, db = digits(a, len(str(a))), digits(b, len(str(b)))
    if any(r["name"] == "multiply_vertically" and r["trigger"] == "any" for r in rules):
        return ints([(da[i] if i < len(da) else 0) * (db[i] if i < len(db) else 0) % 10
                     for i in range(max(len(da), len(db)))])
    total = 0
    for j, y in enumerate(db):
        carry, part = 0, []
        for i, x in enumerate(da):
            upper = da[i + 1] if i + 1 < len(da) else 0
            raw = x * (db[i] if i < len(db) else 0) if _active(rules, "multiply_vertically", i, upper) else x * y + carry
            part.append(raw % 10)
            carry = raw // 10
            if carry and _active(rules, "wrong_carry_amount", i, upper):
                carry -= 1
        if carry: part.append(carry)
        shift = j
        if j and _active(rules, "partial_products_unshifted", j, da[j+1] if j+1 < len(da) else 0):
            shift -= 1
        total += ints(part) * (10 ** shift)
    return total


def _division(a: int, b: int, rules: list[dict], orig_a: int, orig_b: int) -> int:
    active = {r["name"] for r in rules if r["name"] not in SHARED_RULES and div_active(r["trigger"], orig_a, orig_b)}
    q = a // b if b else 0
    if "digitwise_no_remainder" in active:
        q = int("".join(str(int(ch) // b) for ch in str(a))) if b else 0
    if "omit_zero_quotient" in active and len(str(q)) > 2:
        ds = str(q)
        q = int(ds[0] + ds[1:-1].replace("0", "") + ds[-1])
    return q


def answer(op: str, a: int, b: int, rules: list[dict]) -> int:
    if type(a) is not int or type(b) is not int: raise ValueError("Operands must be integers")
    if a < 0 or b < 0 or (op == "sub" and a < b) or (op == "div" and (b <= 0 or a % b)):
        raise ValueError("Outside positive-integer benchmark domain")
    validate_rules(op, rules)
    orig_a, orig_b = a, b
    for rule in rules:
        if rule["name"] in SHARED_RULES:
            a = _change_digits(a, rule["name"], rule["trigger"])
            b = _change_digits(b, rule["name"], rule["trigger"])
    procedural = [r for r in rules if r["name"] not in SHARED_RULES]
    if not procedural and not any(r["name"] in SHARED_RULES for r in rules):
        return correct(op, a, b)
    if op == "add": return _addition(a, b, procedural)
    if op == "sub": return _subtraction(a, b, procedural)
    if op == "mul": return _multiplication(a, b, procedural)
    if op == "div": return _division(a, b, procedural, orig_a, orig_b)
    raise ValueError(op)


def rule_configurations(op: str, count: int, *, include_shared: bool = True) -> list[list[dict]]:
    atoms = [{"name": n, "trigger": t} for n in RULES[op]
             if include_shared or n not in SHARED_RULES
             for t in allowed_triggers(op, n)]
    if count == 1: return [[a] for a in atoms]
    if count != 2: raise ValueError("Supported count is 1 or 2")
    return [[x, y] for x, y in combinations(atoms, 2)
            if x["name"] != y["name"] and not ({x["name"], y["name"]} <= set(SHARED_RULES))]


def shared_rule_configurations() -> list[dict]:
    return [{"name": n, "trigger": t} for n in SHARED_RULES for t in SHARED_TRIGGERS]
