# Status

- 文档同步：2026-09-08；来源：已完成 A4/A5 artifact、最终审计报告和本地静态分析。
- 当前阶段：FINAL PUBLIC ARCHIVE PREPARATION。R0/R1/R2、A1、A3、A2、R6、contract correction、A4、A4 FINALIZE、A5 PREPARATION 与 A5 FINAL EVALUATION 均已完成。
- A4：PASS。`A4_100k_final` 已完成 100,000 optimizer updates；`100000/pretrained_model` 是冻结的 primary checkpoint。严格离线 reload 与真实 LIBERO batch contract 均通过；训练采用 pretrained-policy initialization、partial-parameter fine-tuning，vision encoder 保持冻结。证据：`docs/A4_FINALIZE_AUDIT.md`。
- A5：PASS。冻结 A4 checkpoint 在 common `n_action_steps=1` / W1 serial protocol 下完成 4 suites × 10 tasks × 10 fixed-init episodes（400 episodes）。overall endpoint success 为 71.5%（286/400）：Spatial 82.0%、Object 78.0%、Goal 80.0%、LIBERO-10/Long 46.0%。结果、400 videos、日志和 command/config snapshots 已完成审计。证据：`docs/A5_FINAL_AUDIT_REPORT.md`。
- 解释边界：该结果是 single-seed、fixed-init-state、simulated closed-loop LIBERO endpoint observation；不作因果、multi-seed statistical 或 real-robot claim。A2 vs A5 仅作为 task-level descriptive endpoint comparison，见 `docs/A2_A5_DESCRIPTIVE_COMPARISON.md`。
- 当前维护范围：仅本地归档、文档和 GitHub 发布前审计；禁止启动新训练、evaluation、profiling 或任何 GPU 任务。
- 冻结约束：`environment/stack_lock.json`、`docs/04_PRIMARY_PROTOCOL_DRAFT.md`、`docs/AMENDMENTS.md` 继续有效；未改动任何 revision、checkpoint 或实验语义。
- 下一步：完成公开安全审计后，等待项目所有者审核并明确授权 commit/push。
