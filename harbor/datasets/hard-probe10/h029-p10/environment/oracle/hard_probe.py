#!/usr/bin/env python3
"""HARD-PROBE: a harder BEHAVIOR-PROBE variant (same case/grade format).

What makes it hard:
  1. Students combine TWO interacting bug components (bug x trigger condition), drawn
     from 6 bugs x 8 conditions, so ~2.3k possible students instead of 13 textbook bugs.
  2. Only 4 observations, chosen so many different students fit them.
  3. Test questions are chosen where the students that fit the observations disagree.
  4. Transfer questions go up to 5 digits.
Validity: each case records the ideal reasoner's ceiling (uniform prior over the
hypothesis space, majority answer) with 0 probes and with 3 greedy info-gain probes,
so a low agent score means the agent failed, not that the task is impossible.

Grading reuses behavior_probe.grade (it only reads the case JSON).
    python3 hard_probe.py generate --root hard_cases --n 20 --seed 7
    python3 hard_probe.py probe --root hard_cases --session X --a 5023 --b 1786
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import Counter
from pathlib import Path

import behavior_probe as bp

BUGS = ("smaller_from_larger", "forget_decrement", "write_zero", "borrow_skip", "double_decrement", "write_bottom")
CONDS = ("any", "ones", "tens", "high", "next_zero", "incoming", "big_bottom", "top_zero")
TARGET = 0.55  # ideal reasoner's 0-probe ceiling we aim each case at


def fires(cond: str, col: int, t: int, b: int, dec: int, next_top: int | None) -> bool:
    return {
        "any": True, "ones": col == 0, "tens": col == 1, "high": col >= 2,
        "next_zero": next_top == 0, "incoming": dec > 0, "big_bottom": b >= 7, "top_zero": t == 0,
    }[cond]


def simulate(a: int, b: int, comps) -> int:
    return run(a, b, comps)[0]


def natural(a: int, b: int, comps) -> bool:
    """False if the procedure leaves a digit outside 0-9 or borrows past the leftmost
    column, i.e. a step no real student could write down. Cases avoid such items."""
    return run(a, b, comps)[1]


def run(a: int, b: int, comps) -> tuple[int, bool]:
    """Right-to-left column subtraction; in a column that needs a borrow, the first
    component whose condition fires decides what the student does."""
    top = [int(c) for c in str(a)[::-1]]
    n, carry, result, ok = len(top), [0] * (len(top) + 2), 0, True
    for col in range(n):
        t, bv, dec = top[col], (b // 10**col) % 10, carry[col]
        t_eff = t - dec
        if t_eff >= bv:
            digit = t_eff - bv
        else:
            nxt = top[col + 1] if col + 1 < n else None
            bug = next((bug for bug, cond in comps if fires(cond, col, t, bv, dec, nxt)), None)
            digit = t_eff + 10 - bv
            if bug is None:
                carry[col + 1] += 1
            elif bug == "smaller_from_larger":
                digit = abs(t - bv)
            elif bug == "write_zero":
                digit = 0
            elif bug == "write_bottom":
                digit = bv
            elif bug == "borrow_skip":
                carry[col + 2] += 1
            elif bug == "double_decrement":
                carry[col + 1] += 2
            # forget_decrement: borrow 10, decrement nothing
        ok = ok and 0 <= digit <= 9
        result += (digit % 10) * 10**col  # only reachable for unnatural items, which cases exclude
    return result, ok and not any(carry[n:])


HYPS = [((c,),) for c in itertools.product(BUGS, CONDS)]
HYPS = [h[0] for h in HYPS] + [p for p in itertools.permutations(itertools.product(BUGS, CONDS), 2)]


def rand_item(rng: random.Random, digits: int) -> tuple[int, int]:
    a = rng.randint(10 ** (digits - 1), 10**digits - 1)
    return a, rng.randint(0, a)


def make_case(rng: random.Random, cid: str):
    all_obs = list({rand_item(rng, rng.choice((3, 3, 4))) for _ in range(160)})
    all_test = list({rand_item(rng, d) for d in (3,) * 250 + (4,) * 150 + (5,) * 100} - set(all_obs))
    # Student: two components that both change answers on the pool.
    while True:
        student = rng.choice(HYPS[len(BUGS) * len(CONDS):])
        # Keep only problems this student can work without an impossible step.
        obs_pool = [it for it in all_obs if natural(*it, student)]
        test_pool = [it for it in all_test if natural(*it, student)]
        pool = obs_pool + test_pool
        ans = [simulate(a, b, student) for a, b in pool]
        if all(ans != [simulate(a, b, (c,)) for a, b in pool] for c in student) and \
                sum(x != a - b for x, (a, b) in zip(ans, pool)) > 0.25 * len(pool):
            break
    truth = dict(zip(pool, ans))
    table = {h: [simulate(a, b, h) for a, b in pool] for h in HYPS}
    idx = {item: i for i, item in enumerate(pool)}

    def consistent(items):
        return [h for h in HYPS if all(table[h][idx[it]] == truth[it] for it in items)]

    def vote(items_cons, it):
        return Counter(table[h][idx[it]] for h in items_cons).most_common(1)[0][0]

    def select_tests(cons):
        # 10 error + 10 correct items per domain, only where consistent students disagree.
        hidden = []
        for domain, digs in (("familiar", (3,)), ("transfer", (4, 5))):
            cand = [it for it in test_pool if len(str(it[0])) in digs]
            for wrong in (True, False):
                group = [it for it in cand if (truth[it] != it[0] - it[1]) == wrong]
                contested = [it for it in group if any(table[h][idx[it]] != truth[it] for h in cons)]
                pick = rng.sample(contested, min(10, len(contested)))
                pick += rng.sample([it for it in group if it not in pick], 10 - len(pick))
                hidden += [{"a": a, "b": b, "student_answer": truth[(a, b)], "domain": domain,
                            "student_is_wrong": wrong} for a, b in pick]
        rng.shuffle(hidden)
        return hidden

    def ceiling(cons, hidden):
        err_items = [(h["a"], h["b"]) for h in hidden if h["student_is_wrong"]]
        return sum(vote(cons, it) == truth[it] for it in err_items) / len(err_items)

    # Observations: 4 items (>=2 student errors); keep the set whose ideal 0-probe
    # ceiling is closest to TARGET, so the case is hard but not hopeless.
    errs = [it for it in obs_pool if truth[it] != it[0] - it[1]]
    rights = [it for it in obs_pool if truth[it] == it[0] - it[1]]
    best = None
    for _ in range(60):
        obs = rng.sample(errs, 2) + rng.sample(rights, 2)
        cons = consistent(obs)
        hidden = select_tests(cons)
        c0 = ceiling(cons, hidden)
        if best is None or abs(c0 - TARGET) < abs(best[3] - TARGET):
            best = (obs, cons, hidden, c0)
    obs, cons, hidden, ceil0 = best
    rng.shuffle(obs)
    err_items = [(h["a"], h["b"]) for h in hidden if h["student_is_wrong"]]
    c3, forbidden = list(cons), {(h["a"], h["b"]) for h in hidden}
    for _ in range(3):  # greedy probe: item whose answers split the consistent set most evenly
        probe_it = min((it for it in pool if it not in forbidden),
                       key=lambda it: max(Counter(table[h][idx[it]] for h in c3).values()))
        c3 = [h for h in c3 if table[h][idx[probe_it]] == truth[probe_it]]
    ceil3 = sum(vote(c3, it) == truth[it] for it in err_items) / len(err_items)

    qs = [{"id": f"Q{i:02d}", "a": h["a"], "b": h["b"]} for i, h in enumerate(hidden, 1)]
    public = {
        "id": cid,
        "task": "Infer this individual student's subtraction behavior from observed answers. "
                "Predict the answers the student, not a calculator, will give on new questions.",
        "instructions": "Submit an integer answer and a confidence from 0.0 to 1.0 for every test question. "
                        "Do not assume the student always computes correctly.",
        "observations": [{"a": a, "b": b, "student_answer": truth[(a, b)]} for a, b in obs],
        "test_questions": qs,
    }
    private = {
        "id": cid, "rule": {"components": [list(c) for c in student]},
        "test_answers": {q["id"]: {"answer": h["student_answer"], "student_is_wrong": h["student_is_wrong"],
                                   "domain": h["domain"]} for q, h in zip(qs, hidden)},
        "ceiling": {"consistent_hypotheses": len(cons), "ideal_b0": round(ceil0, 3),
                    "ideal_b3_greedy": round(ceil3, 3)},
    }
    return public, private


def make_case_retry(rng: random.Random, cid: str):
    """Some students leave too few natural problems to fill the pools; draw again from
    the same stream (deterministic, and cases that succeed first time are unchanged)."""
    for _ in range(20):
        try:
            return make_case(rng, cid)
        except ValueError:
            continue
    raise RuntimeError(f"{cid}: could not build a case")


def generate(root: Path, seed: int, n: int) -> None:
    ids = []
    for i in range(n):
        cid = f"H{i + 1:03d}"
        pub, priv = make_case_retry(random.Random(seed * 1000 + i), cid)
        bp.write_json(root / "public" / f"{cid}.json", pub)
        bp.write_json(root / "private" / f"{cid}.json", priv)
        ids.append(cid)
        print(cid, priv["rule"]["components"], priv["ceiling"], flush=True)
    bp.write_json(root / "manifest.json", {"seed": seed, "case_ids": ids, "allowed_probe_budgets": list(bp.BUDGETS)})


def probe(root: Path, session: str, a: int, b: int) -> dict:
    """Same contract as behavior_probe.probe, with the hard simulator."""
    path = bp.session_path(root, session)
    state = bp.read_json(path)
    if state["graded"]:
        raise ValueError("Session already graded")
    if len(state["probes"]) >= state["budget"]:
        raise ValueError("No probes remaining")
    if not (100 <= a <= 99999 and 0 <= b <= a):
        raise ValueError("Probe must use 3- to 5-digit a, with 0 <= b <= a")
    public = bp.read_json(root / "public" / f"{state['case']}.json")
    if (a, b) in {(q["a"], q["b"]) for q in public["test_questions"]}:
        raise ValueError("Cannot directly probe a held-out evaluation question")
    comps = [tuple(c) for c in bp.read_json(root / "private" / f"{state['case']}.json")["rule"]["components"]]
    answer = simulate(a, b, comps)
    state["probes"].append({"a": a, "b": b, "student_answer": answer})
    bp.write_json(path, state)
    out = {"a": a, "b": b, "student_answer": answer, "remaining": state["budget"] - len(state["probes"])}
    print(json.dumps(out))
    return out


def self_check() -> None:
    """The single-component simulator must match behavior_probe's textbook bugs."""
    rng = random.Random(0)
    mapping = {"any": "any", "ones": "ones_only", "tens": "tens_only", "next_zero": "next_digit_zero"}
    for _ in range(3000):
        a, b = rand_item(rng, rng.choice((3, 4)))
        for bug in BUGS[:3]:
            for cond, scope in mapping.items():
                assert simulate(a, b, ((bug, cond),)) == bp.student_answer(a, b, bp.StudentRule(bug, scope)), (a, b, bug, cond)
        assert simulate(a, b, ()) == a - b
    print("self-check ok:", len(HYPS), "hypotheses")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate"); g.add_argument("--root", default="hard_cases"); g.add_argument("--n", type=int, default=20); g.add_argument("--seed", type=int, default=7)
    p = sub.add_parser("probe"); p.add_argument("--root", default="hard_cases"); p.add_argument("--session", required=True); p.add_argument("--a", type=int, required=True); p.add_argument("--b", type=int, required=True)
    sub.add_parser("check")
    args = ap.parse_args()
    if args.cmd == "generate":
        generate(Path(args.root), args.seed, args.n)
    elif args.cmd == "probe":
        probe(Path(args.root), args.session, args.a, args.b)
    else:
        self_check()
