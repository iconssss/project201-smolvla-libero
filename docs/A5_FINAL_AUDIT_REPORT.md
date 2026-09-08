# A5 Final Audit Report

**Verdict: PASS** — 2026-09-08（用户授权的 PuTTY 终态审计）。

## Scope and frozen protocol

- Checkpoint: `outputs/A4_100k_final/checkpoints/100000/pretrained_model`
- Four suites: Spatial, Object, Goal, LIBERO-10/Long；task 0–9，每 task 10 个固定 init-state episodes。
- Seed 0、hard reset、relative control、native LIBERO success predicate、2 cameras、8D state、7D action。
- Common closed-loop override: `--policy.n_action_steps=1`。
- W1 serial: `eval.batch_size=1`、`eval.use_async_envs=false`、`env.max_parallel_tasks=1`、GPU0、offline、EGL。

## Result

| Scope | Episodes | Success rate |
| --- | ---: | ---: |
| Spatial | 100 | 82.0% |
| Object | 100 | 78.0% |
| Goal | 100 | 80.0% |
| LIBERO-10 / Long | 100 | 46.0% |
| **Overall** | **400** | **71.5% (286/400)** |

Evaluator-reported pure rollout time: 25,604.024 s (7 h 06 m 44 s), or 64.010 s/episode.

## Integrity checks

- `eval_info.json` is present and parseable; it contains 40 task records, four group aggregates, and one overall aggregate.
- Each suite covers task IDs 0–9; each of the 40 task directories contains 10 videos: 400 MP4s total.
- The final log contains `End of eval`; the final error scan found 0 matches for OOM, NaN/Inf, Traceback, processor/data/contract errors, or checkpoint/safetensors corruption.
- Frozen command/config snapshots and their launch SHA256 manifest are present; both snapshot hashes verify.
- Output directory is 29 MiB and log is 23 MiB at final audit; 229 GiB persistent disk remained free.

## Artifacts

- Output/results: `/root/shared-nvme/201-smolvla-libero/outputs/A5_primary_400ep`
- Machine-readable aggregate and per-task result: `outputs/A5_primary_400ep/eval_info.json`
- Videos: `outputs/A5_primary_400ep/videos/`
- Log: `/root/shared-nvme/201-smolvla-libero/logs/A5_primary_400ep.log`
- Frozen launch evidence: `environment/A5_primary_command_snapshot.txt`, `environment/A5_primary_evaluator_config_snapshot.json`, `environment/A5_primary_launch_sha256.txt`

## Interpretation boundary

This is a single-seed, fixed-init-state, closed-loop LIBERO endpoint result under the frozen W1/common-horizon protocol. It supports an auditable reproduction result only; it does not establish SOTA, universal improvement, real-robot performance, or a multi-seed statistical conclusion.

