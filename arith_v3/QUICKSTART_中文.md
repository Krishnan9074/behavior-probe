# ARITH-PROBE v3：中文快速上手

这是可以在本地运行的四则运算 Virtual Student / Black-Box Behavioral
Inference Benchmark。虚拟学生和评分器是确定性的 Python 程序，无须 LLM Judge。
**注意：目前是本地 Pilot 版本，还不是已部署的 Valkyrie BenchmarkService。**

## 与第一版相比，更新了什么？

- 规则库按 Wallace（1984）论文筛选出 **12 个编号错误类别**，加上论文另外
  报告的 `smaller_from_larger`，总共 **13 个来源类别**。具体算法、触发条件
  是我们自行形式化的实现，并未得到真实学生行为数据验证。
- **Level 1** 单一运算推断，有 Easy 和双错误 Hard。
- **Level 2** 同一学生在加减乘除各有一个隐藏规则，四种运算共用 Probe 预算。
- **Level 3** 同一错误机制影响四则运算，某个目标运算的初始历史题为零，测量
  跨运算迁移。现版仅实现 Type 4 的共享零/一处理变体。
- 保留 Agent 通过 **算式** 而不是文字提问的接口。
- Grader 提供 **Error-Case Accuracy、Per-Operation / Macro Accuracy、
  Accuracy–Probe Curve、K100_error、K100_all、K95、Brier、ECE 和 Level 3 Transfer Accuracy**。
- 增加候选规则的 **Oracle Majority-Vote Reference**，但它不是最优分数上限。

## 1. 本地测试

解压完整 ZIP，Terminal 进入项目目录后执行：

```bash
python3 -m unittest discover -s tests -v
python3 tools/validate_cases.py
```

默认已经附带 **20 个任务**，入口 `benchmark.py`。

## 2. 让 Fable / GPT 跑一次 0 Probe

- Level 2 公开测试：`examples/agent_level2_A001_public_only.zip`
- Level 3 公开测试：`examples/agent_level3_A002_public_only.zip`

**只把公开 ZIP 给被测 Agent，绝对不要给整个项目 ZIP。**

Agent 根据 `task.json`、`agent_prompt.txt` 生成包含全部 80 道题预测的 JSON，
例如保存为 `fable_A001.json`。

```bash
python3 benchmark.py start --case A001 --budget 0 --session fable_A001
python3 benchmark.py grade --session fable_A001 --submission fable_A001.json
```

## 3. 有 Probe 的测试

```bash
python3 benchmark.py start --case A001 --budget 3 --session fable3
python3 benchmark.py submit --session fable3 --submission pred_0.json
python3 benchmark.py probe --session fable3 --op sub --a 502 --b 178
python3 benchmark.py submit --session fable3 --submission pred_1.json
python3 benchmark.py grade --session fable3
```

要得到准确的 **观测 K100**，Agent 应该在第 0 次，以及**每次提问之后**都提交完整预测快照。
`submit` 只保存预测，不会把测试分数告诉 Agent；`grade` 结束后才放出分数。

## 4. 保持学术依据与 Benchmark 测量的平衡

文献类别用于决定值得模拟的错误；具体规则用于生成确定性 Ground Truth；
Benchmark 用隐藏题预测、主动提问效率与信心校准进行评价。
**我们不让 Agent 猜 Label，也不宣称已经模拟真实儿童的认知过程。**

详细代码说明见 `README.md`；标签到算法的对应见 `RULES.md`。
