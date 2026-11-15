"""Build Harbor tasks for Valkyrie from the hard suite.

    python3 harbor/build_tasks.py --cases 30

Writes harbor/datasets/hard-noprobe/<task>/ and harbor/datasets/hard-probe10/<task>/.

Isolation:
  * The agent container ("main") gets only instruction.md: the public observations and test
    questions. No rule, no answers.
  * In probe tasks, the hidden rule lives only in an "oracle" sidecar container, which answers
    `probe A B`, enforces the budget, refuses test questions and logs every probe.
  * tests/ (answer key + grader) is copied in by Harbor only after the agent finishes.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import hard_probe as hp  # noqa: E402

OUT = Path(__file__).parent / "datasets"
SRC = Path(__file__).parent / "src"
BUDGETS = {"hard-noprobe": 0, "hard-probe10": 10}
MODEL_HOSTS = ["api.anthropic.com", "api.openai.com", "statsig.anthropic.com", "sentry.io",
               "chatgpt.com", "ab.chatgpt.com"]


def instruction(pub: dict, budget: int) -> str:
    probe = (
        f"\n## Optional tool\n\nYou may run `probe A B` (A has 3-5 digits, 0 <= B <= A, not one of the test "
        f"questions) to see this student's answer to A - B. You can use it up to {budget} times. "
        "Using it is entirely up to you.\n" if budget else "")
    obs = "\n".join(f"| {o['a']} − {o['b']} | {o['student_answer']} |" for o in pub["observations"])
    qs = "\n".join(f"| {q['id']} | {q['a']} − {q['b']} |" for q in pub["test_questions"])
    return f"""# Predict one student's subtraction answers

You are predicting how one specific student does subtraction. The student may follow a systematic,
buggy procedure. Predict the answers **this student** will give, not the correct answers.
Do not assume the student always computes correctly.

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

Include all 40 ids. `answer` is an integer. `confidence` (0 to 1) is the probability that your
answer exactly equals the student's answer.
"""


def task_toml(name: str, budget: int, case_id: str, ceiling: dict, local: bool) -> str:
    hosts = ", ".join(f'"{h}"' for h in MODEL_HOSTS + (["oracle"] if budget else []))
    # Image builds need the internet; the restriction applies only while the agent runs.
    # The local Docker provider can't enforce allowlists, so --local builds keep it public.
    agent_net = "" if local else (
        "# No public internet for the agent: only the model APIs (and the oracle sidecar).\n"
        f'network_mode = "allowlist"\nallowed_hosts = [{hosts}]\n')
    return f"""schema_version = "1.4"

[task]
name = "behavior-probe/{name}"

[metadata]
category = "hypothesis-testing"
case = "{case_id}"
probe_budget = {budget}
ideal_reasoner_no_probes = {ceiling['ideal_b0']}
ideal_reasoner_3_probes = {ceiling['ideal_b3_greedy']}

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


def build(n_cases: int, local: bool = False) -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    cases = sorted((ROOT / "hard_cases/private").glob("H*.json"))[:n_cases]
    for ds, budget in BUDGETS.items():
        dsdir = OUT / ds
        dsdir.mkdir(parents=True)
        # metric.py omitted: custom scoring is disabled on Valkyrie; default = mean task reward
        for f in cases:
            priv = json.loads(f.read_text())
            pub = json.loads((ROOT / "hard_cases/public" / f.name).read_text())
            name = f"{priv['id'].lower()}-{'p' + str(budget) if budget else 'p0'}"
            t = dsdir / name
            env = t / "environment"
            (t / "tests").mkdir(parents=True)
            env.mkdir()
            (t / "instruction.md").write_text(instruction(pub, budget))
            (t / "task.toml").write_text(task_toml(name, budget, priv["id"], priv["ceiling"], local))
            # Agent image: same for every task (cache-friendly); probe tasks add the probe client.
            dockerfile = (SRC / "main.Dockerfile").read_text()
            if budget:
                dockerfile = dockerfile.replace("WORKDIR /workspace", "COPY probe /usr/local/bin/probe\nRUN chmod +x /usr/local/bin/probe\nWORKDIR /workspace")
            (env / "Dockerfile").write_text(dockerfile)
            for extra in ("pyproject.toml", "uv.lock"):
                shutil.copy(ROOT / "valkyrie/sandbox-image" / extra, env / extra)
            if budget:
                shutil.copy(SRC / "probe", env / "probe")
                (env / "oracle").mkdir()
                shutil.copy(SRC / "oracle.Dockerfile", env / "oracle" / "Dockerfile")
                shutil.copy(SRC / "oracle_server.py", env / "oracle" / "oracle_server.py")
                shutil.copy(ROOT / "hard_probe.py", env / "oracle" / "hard_probe.py")
                shutil.copy(ROOT / "behavior_probe.py", env / "oracle" / "behavior_probe.py")
                (env / "oracle" / "case.json").write_text(json.dumps({
                    "rule": priv["rule"], "budget": budget,
                    "forbidden": [[q["a"], q["b"]] for q in pub["test_questions"]]}))
                shutil.copy(SRC / "docker-compose.yaml", env / "docker-compose.yaml")
            # Verifier: answer key + grader, copied in only after the agent is done.
            (t / "tests" / "answers.json").write_text(json.dumps({
                q["id"]: {**priv["test_answers"][q["id"]], "a": q["a"], "b": q["b"]} for q in pub["test_questions"]}))
            shutil.copy(SRC / "grade.py", t / "tests" / "grade.py")
            shutil.copy(SRC / "test.sh", t / "tests" / "test.sh")
            (t / "tests" / "test.sh").chmod(0o755)
        print(f"{ds}: {len(cases)} tasks")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", type=int, default=30)
    ap.add_argument("--local", action="store_true", help="public agent network, for the local Docker provider")
    a = ap.parse_args()
    if a.local:
        OUT = Path(__file__).parent / "datasets-local"
    build(a.cases, a.local)
