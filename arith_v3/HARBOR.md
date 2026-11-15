# ARITH-PROBE v3 on Valkyrie (Harbor + Modal)

`arith_v3/` is the v3 benchmark copied unchanged from `arithmetic_behavior_benchmark_v3/`
(simulator, 20 cases, grader, tests). `arith_v3/harbor/` packages it as Harbor tasks, set up the
same way as the earlier `behavior-probe` runs. Nothing outside `arith_v3/` was changed, and the
earlier results are untouched.

## Datasets

| Valkyrie dataset | Probe budget | Tasks |
|---|---|---|
| `arith-probe/v3-noprobe` | 0 | 20 (12 Level 1, 4 Level 2, 4 Level 3) |
| `arith-probe/v3-probe10` | 10 (optional) | same 20 |

```
arith_v3/harbor/datasets/v3-probe10/a002-p10/
├── instruction.md            # public task only: past answers + 80 test questions
├── task.toml                 # same limits/allowlist as before; metadata has level, target op, oracle reference
├── environment/
│   ├── Dockerfile            # same agent image as before + `probe` / `snapshot`
│   ├── docker-compose.yaml   # main + oracle sidecar (unchanged)
│   └── oracle/               # hidden rules + v3 student.py; the only place they exist during the run
└── tests/                    # public.json, private.json, v3 grader; copied in after the agent finishes
```

- **Probe:** `probe OP A B` (e.g. `probe mul 234 16`). Same checks as v3's `server.py`: budget,
  operand range, `a >= b` for sub, exact division, no held-out questions.
- **Snapshots:** `snapshot` sends `/workspace/submission.json` to the oracle with the current probe
  count, so the verifier can compute v3's probe curve and observed K100/K95. It never returns a score.
- **Reward:** v3 `grade.score()` on the final submission: exact-match accuracy on the questions the
  student gets wrong. `reward.json` also has overall, macro and per-operation error accuracy,
  Level-3 transfer accuracy (left out once the target operation has been probed), Brier, ECE, probes,
  K100/K95. `detail.json` has the full snapshot timeline and per-question answers.
- **Oracle reference** (`oracle_reference_no_probes` in each `task.toml`): v3's uniform majority-vote
  baseline from the given observations alone. It is not an upper bound.

## Run it

```bash
python3 arith_v3/harbor/build_tasks.py           # rebuild tasks from arith_v3/cases
valkyrie dataset push arith-probe/v3-noprobe arith_v3/harbor/datasets/v3-noprobe --tag v3
valkyrie dataset push arith-probe/v3-probe10 arith_v3/harbor/datasets/v3-probe10 --tag v3
valkyrie run start --agent claude_code-bp --dataset arith-probe/v3-probe10@v3 \
  --model anthropic/claude-opus-5-5 --provider modal -s ANTHROPIC_API_KEY <your-anthropic-secret> --concurrency 5
```

Agents (`valkyrie/agents/claude_code-bp`, `codex-v1.0.0`) and the Modal connection
(`harbor/connect_modal.sh`, `"runtime": "vm"` for the sidecar) are the same as before.
Self-checks: `cd arith_v3 && python3 -m unittest discover -s tests && python3 tools/validate_cases.py`.
