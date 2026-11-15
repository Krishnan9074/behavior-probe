"""Bundle every input and run artifact into report/data.js for report/index.html.

Run with the service venv (it imports the service's problem_text):
    behavior-probe-benchmark-service/.venv/bin/python build_report.py
"""
import glob
import json
import os
import subprocess
import tarfile
from pathlib import Path

HERE = Path(__file__).parent
PROJECT = HERE.parent
DATA = HERE / "bp_data"
OBJ = Path(glob.glob(str(HERE / "Valkyrie/.local/data/orgs/*/objects/benchmarks"))[0])
OUT = HERE / "report"
RES = HERE / "results"
env = {**os.environ, "VALKYRIE_URL": "http://127.0.0.1:8000"}
CLIP = 1500

import sys  # noqa: E402
sys.path.insert(0, str(HERE / "behavior-probe-benchmark-service/src"))
from behavior_probe_benchmark_service.benchmark_service import DATASETS, SUITES, problem_text  # noqa: E402

SUITE_DIR = {"easy": DATA / "cases", "hard": DATA / "hard_cases"}


def rj(p):
    return json.loads(Path(p).read_text())


def clip(s, n=CLIP):
    s = s if isinstance(s, str) else json.dumps(s)
    return s if len(s) <= n else s[:n] + f"… [+{len(s) - n} chars]"


def trajectory(events, agent):
    steps = []
    for e in events:
        if agent.startswith("claude"):
            if e.get("type") == "assistant":
                for b in e["message"].get("content", []):
                    if b.get("type") == "text" and b["text"].strip():
                        steps.append({"k": "assistant", "t": clip(b["text"])})
                    elif b.get("type") == "tool_use":
                        inp = b.get("input", {})
                        steps.append({"k": "tool", "t": clip(f"{b['name']}: " + (inp.get("command") or json.dumps(inp)))})
            elif e.get("type") == "user":
                for b in e["message"].get("content", []):
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        c = b.get("content")
                        if isinstance(c, list):
                            c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                        steps.append({"k": "result", "t": clip(c or "")})
        else:
            it = e.get("item") if e.get("type") == "item.completed" else None
            if not it:
                continue
            if it.get("type") == "agent_message":
                steps.append({"k": "assistant", "t": clip(it.get("text", ""))})
            elif it.get("type") == "reasoning" and it.get("text"):
                steps.append({"k": "reasoning", "t": clip(it["text"])})
            elif it.get("type") == "command_execution":
                steps.append({"k": "tool", "t": clip(it.get("command", ""))})
                steps.append({"k": "result", "t": clip(f"[exit {it.get('exit_code')}] " + (it.get("aggregated_output") or ""))})
    return steps


def agent_output(run_id, task):
    f = OBJ / run_id / task / "agent_output.tar.gz"
    if not f.exists():
        return {}
    out = {}
    with tarfile.open(f) as t:
        names = t.getnames()
        def read(n):
            return t.extractfile(n).read().decode(errors="replace") if n in names else None
        out["final_message"] = read("logs/final_message.txt")
        m = read("logs/metrics_total.json")
        out["metrics"] = json.loads(m) if m else {}
        traj = read("logs/trajectory.jsonl") or ""
        out["events"] = [json.loads(line) for line in traj.splitlines() if line.strip().startswith("{")]
    return out


def results(run_id):
    f = RES / f"results-{run_id}.json"
    if not f.exists():
        subprocess.run(["valkyrie", "run", "results", run_id], cwd=RES, env=env, check=True, capture_output=True)
    return rj(f)


cases = {}
for suite, d in SUITE_DIR.items():
    for f in sorted((d / "public").glob("*.json")):
        pub, priv = rj(f), rj(d / "private" / f.name)
        cases[pub["id"]] = {
            "suite": suite, "observations": pub["observations"],
            "questions": [{**q, **priv["test_answers"][q["id"]]} for q in pub["test_questions"]],
            "rule": priv["rule"], "ceiling": priv.get("ceiling"),
            # exact prompt per dataset, as setup_task writes it to /tmp/problem_statement.txt
            "statement": {ds: problem_text(pub, budget, SUITES[suite][3])
                          for ds, (s, budget) in DATASETS.items() if s == suite},
        }

runs = []
for line in (HERE / "runs.tsv").read_text().splitlines():
    if not line.strip():
        continue
    model, ds, rid = line.split("\t")
    d = results(rid)
    agent = d["benchmark_arguments"]["contract"]["name"]
    suite = DATASETS[ds][0]
    root = SUITE_DIR[suite]
    tasks = []
    for task, rep in sorted((d.get("evaluation_results") or {}).items()):
        if not rep:
            tasks.append({"case": task, "missing": True})
            continue
        tok = rep.get("session")
        sess = rj(root / "private" / "sessions" / f"{tok}.json") if tok else {}
        subf = root / "private" / "submissions" / f"{tok}.json"
        try:
            preds = {p["id"]: p for p in rj(subf)["predictions"]} if subf.exists() else {}
        except Exception:
            preds = {}
        ao = agent_output(rid, task)
        tasks.append({
            "case": task, "report": rep, "probes": sess.get("probes", []),
            "predictions": preds, "final_message": ao.get("final_message"),
            "metrics": ao.get("metrics", {}), "trajectory": trajectory(ao.get("events", []), agent),
        })
    fe = d.get("final_evaluation") or {}
    runs.append({"id": rid, "model": model.split("/")[-1], "agent": agent, "dataset": ds, "suite": suite,
                 "budget": DATASETS[ds][1], "score": fe.get("final_score"), "meta": fe.get("properties", {}),
                 "status": d.get("status"), "tasks": tasks})

# Inputs shown in the diff view: exactly what each sandbox received, plus the harness.
inputs = {}
for ds, (suite, budget) in DATASETS.items():
    cid = "S001" if suite == "easy" else "H001"
    pub = rj(SUITE_DIR[suite] / "public" / f"{cid}.json")
    inputs[f"Problem statement · {ds} ({cid})"] = problem_text(pub, budget, SUITES[suite][3])
inputs["Probe script (probe10 datasets)"] = (
    "#!/usr/bin/env python3\n# uploaded to /usr/local/bin/probe; posts {token,a,b} to the host probe server,\n"
    "# which enforces the budget and refuses test questions\n" +
    Path(HERE / "behavior-probe-benchmark-service/src/behavior_probe_benchmark_service/benchmark_service.py")
    .read_text().split('PROBE_SCRIPT = """')[1].split('"""')[0])
cc = (HERE / "agents/claude_code-v1.0.0/collect_outputs.py").read_text()
inputs["Harness · claude_code (Claude models)"] = (
    (HERE / "agents/claude_code-v1.0.0/contract.yaml").read_text() + "\n# command (prompt = problem statement on stdin):\n" +
    cc.split("def build_claude_command")[1].split("def stream_claude")[0])
cx = (HERE / "agents/codex-v1.0.0/collect_outputs.py").read_text()
i = cx.find('"exec"')
inputs["Harness · codex (OpenAI models)"] = (
    (HERE / "agents/codex-v1.0.0/contract.yaml").read_text() + "\n# command:\n" + cx[max(0, i - 200): i + 600])
SUB = ("You are the agent under evaluation in a benchmark. Your folder: <view>/{case}_b{b}_sub\n\n"
       "Task: case.json in your folder has observed subtraction answers from one simulated student (who may follow a "
       "systematic buggy procedure) and 40 test_questions. Predict the answer THIS STUDENT will give on each test question "
       "(not the arithmetically correct answer).\n\nProbes: {probes}\n\nRules (strict): read only case.json in your folder. "
       "Do not read, list, search or open any other file or folder{extra}. The only commands allowed are {cmds}`python3 -c` "
       "for your own arithmetic, which must not read any files.\n\nOutput: write submission.json in your folder as "
       '{{"predictions":[{{"id":"Q01","answer":<int>,"confidence":<0..1>}}, ...]}} covering all 40 ids. confidence = '
       "probability your answer exactly equals the student's answer. Then reply with one line: your hypothesis about the student's rule.")
inputs["Pilot subagent prompt · budget 0"] = SUB.format(case="S001", b=0, probes="you have no probes for this run.", extra="", cmds="")
inputs["Pilot subagent prompt · budget 3"] = SUB.format(
    case="S001", b=3, probes="you may query the student up to 3 times by running `<your folder>/probe A B` (A has 3 or 4 digits, "
    "0 <= B <= A, and A,B must not be a test question). It prints the student's answer to A - B. Rejected queries don't count. "
    "Choose probes that best distinguish your hypotheses.", extra=", including the probe script itself", cmds="the probe command and ")
inputs["README.md (benchmark spec)"] = (PROJECT / "README.md").read_text()
inputs["hard_probe.py (hard benchmark design)"] = (PROJECT / "hard_probe.py").read_text().split('"""')[1]

pilots = {"easy_subagent": {}, "hard_subagent_v0": {}}
for key, root, pat in (("easy_subagent", PROJECT / "runs", "*_sub.json"), ("hard_subagent_v0", PROJECT / "hard_cases_v0", "*_sub.json")):
    for f in glob.glob(str(root / "private" / "reports" / pat)):
        r = rj(f)
        pilots[key].setdefault(str(r["probe_budget"]), []).append(
            {"case": r["case"], "err": r["primary_wrong_answer_accuracy"], "overall": r["overall_accuracy_diagnostic"],
             "probes": r["probes_used"]})

broken = [ln.split("\t") for ln in (HERE / "runs_probe_broken_port8002.tsv").read_text().splitlines() if ln.strip()]
OUT.mkdir(exist_ok=True)
bundle = {"cases": cases, "runs": runs, "inputs": inputs, "pilots": pilots,
          "broken_runs": [{"model": m.split("/")[-1], "dataset": d, "id": i} for m, d, i in broken]}
(OUT / "data.js").write_text("window.BP_DATA = " + json.dumps(bundle, separators=(",", ":")) + ";\n")
print(f"{len(runs)} runs, {sum(len(r['tasks']) for r in runs)} tasks, {len(cases)} cases, "
      f"{(OUT / 'data.js').stat().st_size / 1e6:.1f} MB")

# Single self-contained file: inline the data into the template.
tpl = (OUT / "template.html").read_text()
final = HERE.parent / "behavior_probe_report.html"
final.write_text(tpl.replace("<script>/*DATA*/</script>", "<script>" + (OUT / "data.js").read_text().replace("</", "<\\/") + "</script>"))
print("wrote", final)
