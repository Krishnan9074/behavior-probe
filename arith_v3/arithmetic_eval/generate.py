"""Seeded, balanced, hidden-ground-truth three-level task generator."""
from __future__ import annotations

import json
import random
from collections import Counter
from pathlib import Path
from typing import Any

from .student import (OPS, RULES, SELECTED_LABELS, SHARED_RULES,
                      answer, correct, rule_configurations, shared_rule_configurations)


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sample_problem(op: str, rng: random.Random, hard: bool = False) -> tuple[int, int]:
    if op == "add":
        width = rng.choice([3, 4, 5] if hard else [3, 4])
        a = rng.randrange(10 ** (width - 1), 10 ** width)
        b = rng.randrange(1, 10) if rng.random() < .22 else rng.randrange(10 ** (width - 2), 10 ** width)
        return a, b
    if op == "sub":
        width = rng.choice([3, 4, 5] if hard else [3, 4])
        a = rng.randrange(10 ** (width - 1), 10 ** width)
        return a, rng.randrange(1, a)
    if op == "mul":
        width = rng.choice([2, 3, 4] if hard else [2, 3])
        a = rng.randrange(10 ** (width - 1), 10 ** width)
        b = rng.randrange(2, 10) if rng.random() < .35 else rng.randrange(10, 100)
        return a, b
    if op == "div":
        divisor = rng.randrange(2, 10)
        width = rng.choice([3, 4, 5] if hard else [3, 4])
        quotient = rng.randrange(10 ** (width - 1), 10 ** width)
        if rng.random() < .45:
            qs = list(str(quotient))
            qs[rng.randrange(1, len(qs) - 1)] = "0"
            quotient = int("".join(qs))
        return quotient * divisor, divisor
    raise ValueError(op)


def pool_for(op: str, rules: list[dict], rng: random.Random, hard: bool,
             n: int = 1100) -> list[dict]:
    pool, seen = [], set()
    for _ in range(n * 7):
        if len(pool) >= n: break
        a, b = sample_problem(op, rng, hard)
        if (a, b) in seen: continue
        seen.add((a, b))
        y = answer(op, a, b, rules)
        pool.append({"op": op, "a": a, "b": b, "y": y, "is_error": y != correct(op, a, b)})
    return pool


def choose_viable(op: str, count: int, rng: random.Random,
                  hard: bool, need: int, preferred_names: list[str] | None = None) -> tuple[list[dict], list[dict]]:
    configs = rule_configurations(op, count)
    if preferred_names:
        target = set(preferred_names)
        configs = [cfg for cfg in configs if target <= {r["name"] for r in cfg}]
        if not configs: raise ValueError(f"No candidate contains {preferred_names} for {op}")
    rng.shuffle(configs)
    for cfg in configs[:min(130, len(configs))]:
        pool = pool_for(op, cfg, rng, hard, n=1300 if need >= 20 else 950)
        tally = Counter(p["is_error"] for p in pool)
        if tally[True] < need + 8 or tally[False] < need + 8: continue
        if count == 2:
            # Both bugs must have a measurable independent effect in combination.
            # Reject pairs where either constituent rule is inert.
            sample = pool[:350]
            eff_first = sum(p["y"] != answer(op, p["a"], p["b"], [cfg[1]]) for p in sample)
            eff_second = sum(p["y"] != answer(op, p["a"], p["b"], [cfg[0]]) for p in sample)
            if min(eff_first, eff_second) < 6: continue
        return cfg, pool
    raise RuntimeError(f"No sufficiently active configuration for {op}/{count}")


def sample_balanced(pool: list[dict], n_each: int, rng: random.Random,
                    excluded: set[tuple] | None = None) -> list[dict]:
    excluded = excluded or set()
    wrong = [p for p in pool if p["is_error"] and (p["op"], p["a"], p["b"]) not in excluded]
    right = [p for p in pool if not p["is_error"] and (p["op"], p["a"], p["b"]) not in excluded]
    if len(wrong) < n_each or len(right) < n_each:
        raise RuntimeError("Insufficient correct/incorrect candidates")
    result = rng.sample(wrong, n_each) + rng.sample(right, n_each)
    rng.shuffle(result)
    return result


def candidate_compatible(op: str, cfg: list[dict], observations: list[dict]) -> bool:
    return all(answer(op, x["a"], x["b"], cfg) == x["y"] for x in observations if x["op"] == op)


def ambiguous_history(op: str, pool: list[dict], cfg_count: int, rng: random.Random,
                      *, history_count: int = 4, min_candidates: int = 2) -> tuple[list[dict], list[list[dict]]]:
    all_cfgs = rule_configurations(op, cfg_count)
    wrong = [p for p in pool if p["is_error"]]
    right = [p for p in pool if not p["is_error"]]
    best_obs, best_models = [], []
    for _ in range(90):
        obs = rng.sample(wrong, history_count // 2) + rng.sample(right, history_count - history_count // 2)
        matches = [c for c in all_cfgs if candidate_compatible(op, c, obs)]
        if len(matches) > len(best_models):
            best_obs, best_models = obs, matches
        if len(matches) >= max(5, min_candidates): break
    if not best_obs: raise RuntimeError("No history found")
    rng.shuffle(best_obs)
    return best_obs, best_models


def cross_history(pools: dict[str, list[dict]], target: str, rng: random.Random):
    """Choose 1 wrong + 3 right observations on non-target operations.

    A residual hypothesis set >=2 is required. This is an intentionally
    evidence-scarce experiment; the ideal reasoner cannot be expected to get
    100% without gathering more information.
    """
    shared = shared_rule_configurations()
    source = [op for op in OPS if op != target]
    best_history, best_models = [], []
    for _ in range(100):
        wrong_op = rng.choice(source)
        obs = [rng.choice([p for p in pools[wrong_op] if p["is_error"]])]
        for op in source:
            obs.append(rng.choice([p for p in pools[op] if not p["is_error"]]))
        matching = [c for c in shared if all(answer(p["op"], p["a"], p["b"], [c]) == p["y"] for p in obs)]
        if len(matching) > len(best_models):
            best_history, best_models = obs, matching
        if len(matching) >= 2: break
    if len(best_models) < 2:
        # No possible ambiguity for this draw. Prefer an explicit error to silently
        # advertising a hypothesis-distinction task that is already identified.
        raise RuntimeError("Could not construct ambiguous cross-operation observations")
    rng.shuffle(best_history)
    return best_history, [[c] for c in best_models]


def discriminative_test(pool: list[dict], candidates: list[list[dict]],
                        history: list[dict], rng: random.Random, n_each: int) -> list[dict]:
    excluded = {(p["op"], p["a"], p["b"]) for p in history}
    if len(candidates) < 2:
        return sample_balanced(pool, n_each, rng, excluded)
    sampled = rng.sample(candidates, min(40, len(candidates)))
    ranked = {True: [], False: []}
    for p in pool:
        if (p["op"], p["a"], p["b"]) in excluded: continue
        outcomes = Counter(answer(p["op"], p["a"], p["b"], c) for c in sampled)
        disagreement = 1 - sum((n / len(sampled)) ** 2 for n in outcomes.values())
        ranked[p["is_error"]].append((disagreement, rng.random(), p))
    result = []
    for flag in (True, False):
        ranked[flag].sort(key=lambda x: (x[0], x[1]), reverse=True)
        if len(ranked[flag]) < n_each: raise RuntimeError("Insufficient discriminative candidates")
        result += [p for _, _, p in ranked[flag][:n_each]]
    rng.shuffle(result)
    return result


def create_case(cid: str, family: str, rng: random.Random,
                preferred_names: list[str] | None = None) -> tuple[dict, dict, dict]:
    rules = {op: [] for op in OPS}
    history, test = [], []
    target_operation = None
    if family.startswith("L1_"):
        _, mode, op = family.split("_")
        count = 2 if mode == "hard" else 1
        cfg, pool = choose_viable(op, count, rng, count == 2, 20, preferred_names)
        rules[op] = cfg
        if count == 2:
            history, compatible = ambiguous_history(op, pool, 2, rng)
            test = discriminative_test(pool, compatible, history, rng, 20)
        else:
            history = sample_balanced(pool, 3, rng)
            test = sample_balanced(pool, 20, rng, {(p["op"], p["a"], p["b"]) for p in history})
    elif family == "L2_mixed":
        pools, compatible_by_op = {}, {}
        for op in OPS:
            cfg, pools[op] = choose_viable(op, 1, rng, True, 10)
            rules[op] = cfg
            h, candidates = ambiguous_history(op, pools[op], 1, rng, history_count=2)
            history += h
            compatible_by_op[op] = candidates
        for op in OPS:
            test += discriminative_test(pools[op], compatible_by_op[op], history, rng, 10)
    elif family.startswith("L3_cross_"):
        target_operation = family[len("L3_cross_"):]
        if target_operation not in OPS: raise ValueError("Bad L3 target")
        # One genuinely shared, executable input interpretation rule (W04)
        # applies unchanged to all four arithmetic operations. No local bugs.
        # The target operation receives ZERO direct observations.
        configs = shared_rule_configurations()
        rng.shuffle(configs)
        made = False
        for shared in configs:
            curr_rules = {op: [shared.copy()] for op in OPS}
            pools = {op: pool_for(op, curr_rules[op], rng, True, n=1500) for op in OPS}
            if any(sum(p["is_error"] for p in pools[op]) < 12 or
                   sum(not p["is_error"] for p in pools[op]) < 12 for op in OPS):
                continue
            try:
                h, compatible = cross_history(pools, target_operation, rng)
            except RuntimeError:
                continue
            history = h
            rules = curr_rules
            excluded = {(p["op"], p["a"], p["b"]) for p in history}
            for op in OPS:
                test += discriminative_test(pools[op], compatible, history, rng, 10)
            made = True
            break
        if not made: raise RuntimeError(f"No viable L3 transfer student for target {target_operation}")
    else:
        raise ValueError(family)

    rng.shuffle(history)
    rng.shuffle(test)
    pub_observations = [{"op": p["op"], "a": p["a"], "b": p["b"], "student_answer": p["y"]}
                        for p in history]
    pub_questions = [{"id": f"Q{i+1:02}", "op": p["op"], "a": p["a"], "b": p["b"]}
                     for i, p in enumerate(test)]
    level = int(family[1])
    public = {
        "task_id": cid,
        "level": level,
        "difficulty": family,
        "focus": family.split("_")[-1] if level == 1 else "all_four_operations",
        "target_operation": target_operation,
        "probe_budget_max": 10,
        "instructions": ("Predict the EXACT integer answers this virtual student would give to all hidden test questions. "
                         "You can ask arithmetic probes when your session permits; responses are integers, not explanations. "
                         "Return one integer answer and confidence probability [0,1] per question. "
                         "Historical observations are intentionally limited. Do not assume the mathematically correct answer."),
        "observations": pub_observations,
        "test_questions": pub_questions,
        "submission_schema": {"predictions": [{"id": "Q01", "answer": 123, "confidence": 0.75}]},
    }
    if level == 3:
        public["transfer_protocol"] = ("No initial observations for target_operation. "
            "Transfer accuracy is measured before any direct probes of that operation; "
            "after such a probe it is reported as contaminated by direct evidence.")
    private = {
        "task_id": cid, "family": family, "level": level, "rules": rules,
        "target_operation": target_operation,
        "test_answers": {q["id"]: {"answer": p["y"], "is_error": p["is_error"],
                                     "mathematically_correct": correct(p["op"], p["a"], p["b"])}
                         for q, p in zip(pub_questions, test)}
    }
    entry = {"task_id": cid, "level": level, "difficulty": family,
             "focus": public["focus"], "target_operation": target_operation,
             "n_history": len(history), "n_test": len(test),
             "n_error_test": sum(p["is_error"] for p in test)}
    return public, private, entry


def generate(root: Path, seed: int = 20261115, easy_per_op: int = 2,
             l2_count: int = 4, l3_per_op: int = 1) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    rng = random.Random(seed)
    families = ([f"L1_easy_{op}" for op in OPS] * easy_per_op
                + [f"L1_hard_{op}" for op in OPS]
                + ["L2_mixed"] * l2_count
                + [f"L3_cross_{op}" for op in OPS] * l3_per_op)
    rng.shuffle(families)
    # Deterministically guarantee each selected literature category is represented
    # in the shipped task set (not merely advertised in the rule catalog).
    easy_plan = {
        "add": ["add_no_regroup", "drop_carry"],
        "sub": ["borrow_unnecessarily", "forget_decrement"],
        "mul": ["wrong_carry_amount", "multiply_vertically"],
        "div": ["omit_zero_quotient", "digitwise_no_remainder"],
    }
    hard_plan = {
        "add": ["single_digit_repeated", "zero_as_one"],
        "sub": ["write_zero", "smaller_from_larger"],
        "mul": ["partial_products_unshifted", "zero_as_one"],
        "div": None,
    }
    easy_seen = {op: 0 for op in OPS}
    manifest = []
    for i, family in enumerate(families, 1):
        cid = f"A{i:03}"
        preferred = None
        if family.startswith("L1_easy"):
            op = family.rsplit("_", 1)[1]
            index = easy_seen[op]
            easy_seen[op] += 1
            if index < len(easy_plan[op]): preferred = [easy_plan[op][index]]
        elif family.startswith("L1_hard"):
            preferred = hard_plan[family.rsplit("_", 1)[1]]
        pub, pri, entry = create_case(cid, family, rng, preferred)
        write_json(root / "public" / f"{cid}.json", pub)
        write_json(root / "private" / f"{cid}.json", pri)
        manifest.append(entry)
    actually_used = {RULES[op][r["name"]][0]
                     for x in manifest
                     for op, rs in read_json(root / "private" / f"{x['task_id']}.json")["rules"].items()
                     for r in rs}
    if easy_per_op >= 2 and not set(SELECTED_LABELS) <= actually_used:
        raise AssertionError(f"Missing selected categories in generated tasks: {set(SELECTED_LABELS)-actually_used}")
    summary = {"seed": seed, "n_cases": len(manifest),
               "labels_represented_in_tasks": sorted(actually_used),
               "label_taxonomy": "12 numbered Wallace categories + 1 Wallace supplemental category",
               "selected_labels": list(SELECTED_LABELS),
               "split": "public = agent-visible; private = trusted evaluation only",
               "cases": manifest}
    write_json(root / "manifest.json", summary)
    return summary
