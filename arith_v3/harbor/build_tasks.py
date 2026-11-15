"""Build Harbor tasks for Valkyrie from the ARITH-PROBE v3 cases (same layout as harbor/build_tasks.py).

    python3 arith_v3/harbor/build_tasks.py            # all 20 cases
    python3 arith_v3/harbor/build_tasks.py --local    # public agent network, for the local Docker provider

Writes arith_v3/harbor/datasets/v3-noprobe/<task>/ and .../v3-probe10/<task>/.

Isolation (unchanged from the earlier benchmark):
  * The agent container ("main") gets only instruction.md: the public task (observations and
    test questions). No rules, no answers, no simulator.
  * In probe tasks, the hidden student lives only in an "oracle" sidecar, which answers
    `probe OP A B`, stores `snapshot`s, enforces the budget, refuses held-out questions and logs.
  * tests/ (private case + v3 grader) is copied in by Harbor only after the agent finishes.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

V3 = Path(__file__).resolve().parent.parent
REPO = V3.parent
sys.path.insert(0, str(V3))
from arithmetic_eval.grade import oracle_prediction, score  # noqa: E402

OUT = Path(__file__).parent / "datasets"
SRC = Path(__file__).parent / "src"
OLD_SRC = REPO / "harbor" / "src"  # shared Dockerfiles/compose, reused read-only
BUDGETS = {"v3-noprobe": 0, "v3-probe10": 10}
MODEL_HOSTS = ["api.anthropic.com", "api.openai.com", "statsig.anthropic.com", "sentry.io",
               "chatgpt.com", "ab.chatgpt.com"]
SYM = {"add": "+", "sub": "−", "mul": "×", "div": "÷"}
PKG = ("__init__.py", "student.py", "grade.py")  # what the oracle and grader need; not generate/server


def instruction(pub: dict, budget: int) -> str:
    n = len(pub["test_questions"])
    ops = "all four operations: +, −, ×, ÷" if pub["level"] > 1 else f"{SYM[pub['focus']]} only"
    target = ""
    if pub.get("target_operation"):
        target = (f"\n**Note:** there are no past answers for **{SYM[pub['target_operation']]}** "
                  f"(`{pub['target_operation']}`), but test questions include it.\n")
    probe = ""
    if budget:
        probe = f"""
## Optional tool

You may run `probe OP A B` (OP is `add`, `sub`, `mul` or `div`) to see this student's integer
answer to a new problem, e.g. `probe sub 502 178`. Operands are integers 0 to 1,000,000; for `sub`
A ≥ B; for `div` B divides A exactly and B > 0. You cannot probe the test questions. You can use
it up to {budget} times. Using it is entirely up to you.

To record your progress, run `snapshot` (it sends `/workspace/submission.json`) once before your
first probe and again after each probe. It stores your predictions and never shows you a score.
"""
    obs = "\n".join(f"| {o['a']} {SYM[o['op']]} {o['b']} | {o['student_answer']} |" for o in pub["observations"])
    qs = "\n".join(f"| {q['id']} | {q['a']} {SYM[q['op']]} {q['b']} |" for q in pub["test_questions"])
    return f"""# Predict one student's arithmetic answers

You are predicting how one specific simulated student does arithmetic ({ops}). The student may
follow systematic but incorrect rules. Predict the **exact integer answer this student will give**,
not the mathematically correct one. Do not assume the student always computes correctly.
{target}
## The student's past answers

| Problem | Student's answer |
|---|---|
{obs}
{probe}
## Test questions

| id | Problem |
|---|---|
{qs}

## What to submit

Write `/workspace/submission.json`:

```json
{{"predictions": [{{"id": "Q01", "answer": 123, "confidence": 0.8}}, ...]}}
```

Include all {n} ids exactly once. `answer` is an integer. `confidence` (0 to 1) is the probability
that your answer exactly equals the student's answer. A missing, duplicate or malformed entry
scores the whole task 0.
"""


def task_toml(name: str, budget: int, pub: dict, ref: float, local: bool) -> str:
    hosts = ", ".join(f'"{h}"' for h in MODEL_HOSTS + (["oracle"] if budget else []))
    agent_net = "" if local else (
        "# No public internet for the agent: only the model APIs (and the oracle sidecar).\n"
        f'network_mode = "allowlist"\nallowed_hosts = [{hosts}]\n')
    return f"""schema_version = "1.4"

[task]
name = "arith-probe/{name}"

[metadata]
category = "hypothesis-testing"
case = "{pub['task_id']}"
level = {pub['level']}
difficulty = "{pub['difficulty']}"
target_operation = "{pub.get('target_operation') or ''}"
probe_budget = {budget}
oracle_reference_no_probes = {ref}

[agent]
timeout_sec = 1800.0
{agent_net}
[verifier]
timeout_sec = 120.0

[environment]
cpus = 2
memory_mb = 4096
storage_mb = 10240
build_timeout_sec = 1800.0
network_mode = "public"
"""


def copy_pkg(dest: Path) -> None:
    (dest / "arithmetic_eval").mkdir(parents=True)
    for f in PKG:
        shutil.copy(V3 / "arithmetic_eval" / f, dest / "arithmetic_eval" / f)


def build(local: bool) -> None:
    out = OUT.with_name("datasets-local") if local else OUT
    if out.exists():
        shutil.rmtree(out)
    cases = [c["task_id"] for c in json.loads((V3 / "cases/manifest.json").read_text())["cases"]]
    for ds, budget in BUDGETS.items():
        for cid in cases:
            pub = json.loads((V3 / "cases/public" / f"{cid}.json").read_text())
            pri = json.loads((V3 / "cases/private" / f"{cid}.json").read_text())
            ref = score(pub, pri, oracle_prediction(pub, pri, [])[0])["primary_accuracy"]
            name = f"{cid.lower()}-p{budget}"
            t = out / ds / name
            env = t / "environment"
            (t / "tests").mkdir(parents=True)
            env.mkdir()
            (t / "instruction.md").write_text(instruction(pub, budget))
            (t / "task.toml").write_text(task_toml(name, budget, pub, ref, local))
            dockerfile = (OLD_SRC / "main.Dockerfile").read_text()
            if budget:
                dockerfile = dockerfile.replace("WORKDIR /workspace", (
                    "COPY probe /usr/local/bin/probe\nRUN chmod +x /usr/local/bin/probe && "
                    "ln -s /usr/local/bin/probe /usr/local/bin/snapshot\nWORKDIR /workspace"))
            (env / "Dockerfile").write_text(dockerfile)
            for extra in ("pyproject.toml", "uv.lock"):
                shutil.copy(REPO / "valkyrie/sandbox-image" / extra, env / extra)
            if budget:
                shutil.copy(SRC / "probe", env / "probe")
                oracle = env / "oracle"
                oracle.mkdir()
                shutil.copy(OLD_SRC / "oracle.Dockerfile", oracle / "Dockerfile")
                shutil.copy(SRC / "oracle_server.py", oracle / "oracle_server.py")
                copy_pkg(oracle)
                (oracle / "case.json").write_text(json.dumps({
                    "rules": pri["rules"], "budget": budget, "test_questions": pub["test_questions"]}))
                shutil.copy(OLD_SRC / "docker-compose.yaml", env / "docker-compose.yaml")
            # Verifier: private case + v3 grader, copied in only after the agent is done.
            (t / "tests" / "public.json").write_text(json.dumps(pub))
            (t / "tests" / "private.json").write_text(json.dumps(pri))
            copy_pkg(t / "tests")
            shutil.copy(SRC / "grade.py", t / "tests" / "grade.py")
            shutil.copy(OLD_SRC / "test.sh", t / "tests" / "test.sh")
            (t / "tests" / "test.sh").chmod(0o755)
        print(f"{ds}: {len(cases)} tasks -> {out / ds}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true", help="public agent network, for the local Docker provider")
    build(ap.parse_args().local)
