"""Bundle every v3 input and run artifact into one self-contained report page.

    python3 arith_v3/report/build_report.py      (after harbor/analyze_hosted.py)

Same layout as valkyrie/build_report.py -> behavior_probe_report.html. Reads the raw Valkyrie
results and agent outputs (trajectory, final message, metrics) in results/hosted/, downloading any
that are missing, and writes arith_v3/behavior_probe_v3_report.html. This is an internal report:
it includes hidden rules and answer keys.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
V3 = HERE.parent
REPO = V3.parent
sys.path.insert(0, str(V3))
from arithmetic_eval.grade import correct, oracle_prediction  # noqa: E402
from arithmetic_eval.student import RULES  # noqa: E402

RES = V3 / "results" / "hosted"
OUTS = RES / "outputs"
ENV = {k: v for k, v in os.environ.items() if k != "VALKYRIE_URL"}
CLIP = 1500
GROUP = {"L1_easy": "easy", "L1_hard": "hard"}


def rj(p):
    return json.loads(Path(p).read_text())


def clip(s, n=CLIP):
    s = s if isinstance(s, str) else json.dumps(s)
    return s if len(s) <= n else s[:n] + f"… [+{len(s) - n} chars]"


def trajectory(events, agent):
    """Readable steps from Claude Code stream-json or Codex exec events (as in valkyrie/build_report.py)."""
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


PROBE_RE = re.compile(r'\{"op": "(add|sub|mul|div)", "a": (\d+), "b": (\d+), "student_answer": (-?\d+), "used": (\d+)')


def probes_from(events):
    """The oracle's replies are JSON lines in the tool output; 'used' numbers them, so repeats are dropped."""
    seen = {}
    for m in PROBE_RE.finditer("\n".join(json.dumps(e) .replace('\\"', '"') for e in events)):
        op, a, b, y, used = m.groups()
        seen.setdefault(int(used), {"op": op, "a": int(a), "b": int(b), "student_answer": int(y)})
    return [seen[k] for k in sorted(seen)]


def logs(rid, task):
    d = OUTS / rid / task / "agent_output" / "logs"
    if not d.exists():
        subprocess.run(["valkyrie", "run", "outputs", rid, "--output-dir", str(OUTS / rid)], env=ENV, check=True,
                       capture_output=True)
    read = lambda n: (d / n).read_text(errors="replace") if (d / n).exists() else None  # noqa: E731
    traj = read("trajectory.jsonl") or ""
    return {"final_message": read("final_message.txt"), "metrics": json.loads(read("metrics_total.json") or "{}"),
            "events": [json.loads(x) for x in traj.splitlines() if x.strip().startswith("{")]}


def rule_text(rules):
    out = []
    for op, rs in rules.items():
        for r in rs:
            label, desc = RULES[op][r["name"]]
            out.append({"op": op, "name": r["name"], "trigger": r["trigger"], "label": label, "desc": desc})
    return out


# ---- cases: public inputs + hidden answers + oracle reference ----
manifest = rj(V3 / "cases/manifest.json")["cases"]
cases = {}
for e in manifest:
    cid = e["task_id"]
    pub, pri = rj(V3 / f"cases/public/{cid}.json"), rj(V3 / f"cases/private/{cid}.json")
    opred, compat = oracle_prediction(pub, pri, [])
    omap = {p["id"]: p for p in opred["predictions"]}
    cases[cid] = {
        "group": GROUP.get(e["difficulty"][:7], f"l{e['level']}"), "level": e["level"], "difficulty": e["difficulty"],
        "focus": pub["focus"], "target": pub["target_operation"],
        "observations": [{**o, "correct": correct(o["op"], o["a"], o["b"])} for o in pub["observations"]],
        "questions": [{**q, "answer": pri["test_answers"][q["id"]]["answer"],
                       "student_is_wrong": pri["test_answers"][q["id"]]["is_error"],
                       "correct": pri["test_answers"][q["id"]]["mathematically_correct"],
                       "oracle": omap[q["id"]]["answer"], "oracle_conf": omap[q["id"]]["confidence"]}
                      for q in pub["test_questions"]],
        "rules": rule_text(pri["rules"]), "compatible": compat,
        "statement": {ds: (V3 / f"harbor/datasets/{ds}/{cid.lower()}-p{b}/instruction.md").read_text()
                      for ds, b in (("v3-noprobe", 0), ("v3-probe10", 10))},
    }
final = rj(RES / "final.json")
for cid, v in final["oracle_reference"]["per_case"].items():
    cases[cid]["oracle_score"] = v

# ---- runs ----
runs = []
for line in (V3 / "harbor/runs_hosted.tsv").read_text().splitlines():
    if not line.strip():
        continue
    model, ds, rid = line.split("\t")
    d = rj(RES / f"results-{rid}.json")
    agent = d["benchmark_arguments"]["contract"]["name"]
    tasks = []
    for task, ev in sorted((d.get("evaluation_results") or {}).items()):
        lg = logs(rid, task)
        tasks.append({"case": task.split("-")[0].upper(), "rewards": (ev or {}).get("rewards"),
                      "secs": ((ev or {}).get("task_breakdown") or {}).get("agent_run_duration"),
                      "probes": probes_from(lg["events"]), "final_message": lg["final_message"],
                      "metrics": {k: lg["metrics"].get(k) for k in ("cost", "wall_clock_duration", "output_tokens",
                                                                     "input_tokens", "cache_read_input_tokens")},
                      "trajectory": trajectory(lg["events"], agent)})
    fe = d.get("final_evaluation") or {}
    runs.append({"id": rid, "model": model.split("/")[-1], "agent": agent, "dataset": ds.split("/")[1].split("@")[0],
                 "budget": 10 if "probe10" in ds else 0, "score": fe.get("final_score"), "status": d.get("status"),
                 "tasks": tasks})

# ---- inputs shown in the diff view: exactly what the sandbox and verifier received ----
T = V3 / "harbor/datasets"
inputs = {
    "instruction.md · v3-noprobe (A002, Level 3)": (T / "v3-noprobe/a002-p0/instruction.md").read_text(),
    "instruction.md · v3-probe10 (A002, Level 3)": (T / "v3-probe10/a002-p10/instruction.md").read_text(),
    "instruction.md · v3-noprobe (A005, Level 1 easy)": (T / "v3-noprobe/a005-p0/instruction.md").read_text(),
    "instruction.md · v3-noprobe (A007, Level 1 hard)": (T / "v3-noprobe/a007-p0/instruction.md").read_text(),
    "instruction.md · v3-noprobe (A001, Level 2)": (T / "v3-noprobe/a001-p0/instruction.md").read_text(),
    "task.toml · v3-noprobe": (T / "v3-noprobe/a002-p0/task.toml").read_text(),
    "task.toml · v3-probe10": (T / "v3-probe10/a002-p10/task.toml").read_text(),
    "Agent Dockerfile · v3-noprobe": (T / "v3-noprobe/a002-p0/environment/Dockerfile").read_text(),
    "Agent Dockerfile · v3-probe10": (T / "v3-probe10/a002-p10/environment/Dockerfile").read_text(),
    "probe / snapshot client (in the agent container)": (V3 / "harbor/src/probe").read_text(),
    "Oracle sidecar server": (V3 / "harbor/src/oracle_server.py").read_text(),
    "Verifier grade.py (copied in after the agent finishes)": (V3 / "harbor/src/grade.py").read_text(),
    "v3 agent prompt (original benchmark)": (V3 / "prompts/agent_prompt.txt").read_text(),
    "Harness · claude_code-bp (contract)": (REPO / "valkyrie/agents/claude_code-bp/contract.yaml").read_text(),
    "Harness · codex-v1.0.0 (contract)": (REPO / "valkyrie/agents/codex-v1.0.0/contract.yaml").read_text(),
    "RULES.md (error taxonomy)": (V3 / "RULES.md").read_text(),
    "Earlier benchmark instruction.md · hard-probe10 (H001)": (REPO / "harbor/datasets/hard-probe10/h001-p10/instruction.md").read_text(),
}

failed = [ln.split("\t") for ln in (V3 / "harbor/runs_gpt_quota_failed.tsv").read_text().splitlines() if ln.strip()]
bundle = {"cases": cases, "runs": runs, "inputs": inputs,
          "oracle": {k: final["oracle_reference"][k] for k in ("no_probes", "by_group")},
          "pairs": final["pairs"],
          "failed_runs": [{"model": m.split("/")[-1], "dataset": d.split("/")[1], "id": i} for m, d, i in failed]}
data = "window.BP_DATA = " + json.dumps(bundle, separators=(",", ":")).replace("</", "<\\/") + ";"
out = V3 / "behavior_probe_v3_report.html"
out.write_text((HERE / "template.html").read_text().replace("<script>/*DATA*/</script>", "<script>" + data + "</script>"))
print(f"{len(runs)} runs, {sum(len(r['tasks']) for r in runs)} tasks, {len(cases)} cases, "
      f"{sum(len(t['probes']) for r in runs for t in r['tasks'])} probes parsed -> {out} ({out.stat().st_size / 1e6:.1f} MB)")
