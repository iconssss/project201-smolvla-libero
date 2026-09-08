# A4 Finalize Audit

- A5 primary checkpoint 已冻结为 `/root/shared-nvme/201-smolvla-libero/outputs/A4_100k_final/checkpoints/100000/pretrained_model`；20K、40K、60K、80K 仅保留为训练历史。
- `training_step.json`：step=100000、batch=64、gradient accumulation=1、world size=1。checkpoint 包含模型、config、processor、tokenizer、optimizer、scheduler 与 RNG 状态。
- 离线 reload smoke PASS：在本地 tokenizer overlay、LIBERO metadata 和 `--policy.input_features=null` 条件下，严格加载为 0 missing / 0 unexpected / 0 shape mismatch；真实 batch contract 为 2 cameras / 8D state / 7D action。
- 参数审计：450,046,176 总参数中 99,880,992（155 tensors）可训练；350,165,184（345 tensors）冻结。86,433,024 个 vision-encoder 参数全部冻结。
- 训练定义已由最终 config 与运行时参数审计证实：完整 pretrained-policy 初始化后的 partial-parameter fine-tuning；不是 VLM-only，也不是全参数训练。
- SHA256 清单及原始 reload/参数审计证据位于远端 `environment/A4_100k_final_100000_SHA256SUMS.txt`、`a4_final_reload_smoke.json`、`a4_trainable_parameter_audit.json`。
- `INVALID_PRECONTRACT_RUN`（约 70 microsteps）持续排除，禁止 resume 或 evaluation。
