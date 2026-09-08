# A5 Static Preparation

环境语义应复用 A2：四个 LIBERO suite、task 0–9、每 task 10 个固定 init-state episode、hard reset、relative control、256×256、batch=1 和 native success predicate。两路相机语义为 agentview 与 wrist；A4 的 `camera1`/`camera2` 仅是训练期 feature-key rename。状态为 8D、动作 7D（[-1, 1]）、control frequency 为 20 Hz；四个 suite 的 horizon 分别为 280 / 280 / 300 / 520。

每个 checkpoint 使用自己的 native processor，不强制统一 processor。

## 已批准 protocol

Anchor 的 `chunk_size=50, n_action_steps=1`，而 A4 final 是 `chunk_size=50, n_action_steps=50`。冻结 evaluator 每个环境 step 仅调用一次 `policy.select_action()`，SmolVLA 会按 `n_action_steps` 管理动作队列。总控已批准 A5 common closed-loop protocol：两者均通过 evaluator CLI 使用 `--policy.n_action_steps=1`。这不修改 checkpoint、source、processor、dataset 或 revision。

仅完成 scheduling 准备：未来可在不改变 task、init state、seed、timeout、success 或 episode semantics 的前提下，对 vector-env concurrency 1 / 2 / 4 / 8 做执行层 microbenchmark。尚未固定并发度，也未启动 A5。

## Horizon smoke（2026-09-07）

冻结 A4 100K checkpoint 在 `libero_spatial/task0` 的 5 个固定 init-state episodes 上完成受限 protocol smoke。`--policy.n_action_steps=<n>` 被 `EvalPipelineConfig` 正确解析并进入 runtime。native50 的动作队列在连续两步后为 `49 → 48`；override1 每步后为 `0`，故下一步会重新生成 chunk。

| 设置 | 纯 rollout | 每 episode | 成功 | 峰值显存 |
| --- | ---: | ---: | ---: | ---: |
| native50 | 39.54 s | 7.91 s | 4/5 | 1974 MiB |
| override1 | 187.84 s | 37.57 s | 4/5 | 1974 MiB |

两组在该极小样本上同为 4/5，不构成性能结论。primary anchor-vs-A4 comparator 已冻结为 common `n_action_steps=1`，因为它匹配 anchor native closed-loop horizon。完整证据：远端 `environment/A5_HORIZON_ANALYSIS.md`。

## Scheduling benchmark（2026-09-07）

在 common horizon、相同 `libero_spatial/task0`、5 个请求 episode 下，W1（batch=1、同步）是唯一保持请求/输出 episode 数一致的配置：183.37 秒纯 eval、5 个视频、4/5 success。W2 与 W4 虽然要求 5 episodes，却分别输出 6 / 8 个视频且成功序列变为 3/5，因此不是纯调度加速，不可用于正式 A5。

正式 A5 推荐保持 A2 对齐的 `eval.batch_size=1`、`eval.use_async_envs=false`、`env.max_parallel_tasks=1`。详见远端 `environment/A5_PARALLEL_SCHEDULING_BENCHMARK.md`。

## Final preflight（2026-09-07）

正式 A5 command 的缩小范围版本（四个 suite、task0、每 suite 一个 fixed-init episode）以相同 common horizon/W1 语义完成：exit code 0、4 个 nonempty 视频、`eval_info.json`、无 OOM/NaN/Inf/Traceback/processor/data/contract error。纯 eval 为 299.25 秒（74.81 秒/episode），wall time 为 325 秒；GPU 峰值 2122 MiB。该 4 episode run 仅验证执行链路，不能作为 A5 benchmark 得分。

由四 suite preflight 外推，400 episodes 纯 rollout 约 8.31 小时；正式运行建议预留 9–10 小时。远端证据：`environment/A5_FINAL_PREFLIGHT_AUDIT.md`。

## Optimization decision（2026-09-07）

已授权的 40-episode instrumentation profiling 在运行约 4 分 41 秒后按 owner 指令安全终止；保留 `logs/A5_profile_40ep.log` 和已有输出。终止发生在 active rollout 内，故 wrapper 尚未来得及写出结构化逐 episode metrics JSON；不得把缺失的细分计时补造为测量结果。

决定为 **STOP optimization**，正式 A5 保持冻结的 W1：`n_action_steps=1`、`eval.batch_size=1`、`eval.use_async_envs=false`、`env.max_parallel_tasks=1`。final preflight 的平均 GPU 利用率为 13.98%、峰值 21%、峰值显存 2122 MiB，符合 serial closed-loop 中 CPU/EGL 仿真、观察处理和每环境步 policy inference 共同主导的特征；这些 GPU 数值不是逐类时间占比。视频文件仅 34–161 KiB，且 preflight 的 wall-minus-pure-eval 为 25.75 秒（包含进程、模型、环境初始化和视频），没有证据表明 video/render/IO 是值得改变执行策略的瓶颈。

W2/W4 scheduling benchmark 分别为 5 个请求 episode 生成 6/8 个视频并改变 success sequence，因而不保持 episode semantics，不能作为 A5 加速方案。唯一可审计的执行配置仍是 W1。400 episode 纯 rollout 估计约 8.31 小时，建议预留 9–10 小时；未启动正式 A5。
