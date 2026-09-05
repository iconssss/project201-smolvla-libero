# Remote Execution Plan (do not execute until explicitly authorized)

Remote root: `/root/shared-nvme/201-smolvla-libero`. All commands below are templates, never credentials. Every GPU command prefixes `CUDA_VISIBLE_DEVICES=0`; no `torchrun` or multi-GPU launcher.

| Phase | Prepared action | Pass / stop | Outputs / backup |
|---|---|---|---|
| R0 connect + audit | interactive `plink.exe` connection; capture `uname`, disk, `nvidia-smi`, driver, CUDA, RAM | pass: one 4090 24GB and durable free space; stop if different | `environment/system_manifest.txt`; copy local |
| R1 bootstrap | checkout primary LeRobot commit `3f2c29ef7e44b1ddccbcda3b6a63939e53639e9e`, install selected extras in `env/`, set `MUJOCO_GL=egl`; record `pip freeze`, commit and CLI help | pass: exact lock verifies; stop on version/API mismatch | install log and verification addendum |
| R2 acquire | set project-local HF cache; fetch only locked base, released anchor, dataset revisions | pass: hashes, free-space reserve, decode one sample; stop on mismatch/disk | download manifest, `du`, SHA files |
| R3 A1 canary | `lerobot-eval` with one selected task, batch 1, 3 episodes, init states, hard reset, video | pass: all canary contract gates; failure stops A3/A2/A4 | eval JSON, videos, command log |
| R4 A3 smoke | batch 8 first; 16 only with clear batch-8 headroom; 4 only after OOM; measure memory/throughput | pass: finite/stable evidence and selected divisor of 64; no batch-32/64 probe | memory/throughput table |
| R5 A2 anchor | official four-suite command, 10/task, batch 1, max parallel tasks 1 | pass: credible released-anchor behavior; stop for implausibly low SR | raw JSON/CSV, selected videos, summary |
| R6 freeze A4 | verify pins, selected `b`/`a`, local full-base snapshot path, and scaled microstep command/config | pass: immutable primary command; stop on mismatch | frozen run config |
| R7 100K updates | after R6, launch one process from full pinned base; health check once, then stop monitoring | pass: finite metrics/checkpoints/reload; stop on integrity failure | logs, checkpoints, hashes, backup manifest |
| R8 evaluation | predeclared checkpoint coverage, then endpoint 400×seed0 and conditional seeds 1/2 | pass: all raw + aggregate evidence preserved | result JSON/CSV, figures, videos, report |

## Command skeletons

```bash
export CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl HF_HOME=/root/shared-nvme/201-smolvla-libero/cache/hf
lerobot-eval --policy.path=PINNED_RELEASED_MODEL --env.type=libero \
  --env.task=libero_spatial --env.task_ids='[0]' --eval.batch_size=1 \
  --eval.n_episodes=3 --env.init_states=true --env.hard_reset=true \
  --env.control_mode=relative --env.max_parallel_tasks=1 --seed=0

lerobot-train --policy.path=LOCAL_PINNED_SMOLVLA_BASE_SNAPSHOT \
  --policy.push_to_hub=false --dataset.repo_id=lerobot/libero --dataset.revision=a1aaacb7f6cd6ee5fb43120f673cebb0cfea7dd4 \
  --dataset.video_backend=torchcodec --output_dir=OUTPUT --batch_size=B \
  --accelerator.gradient_accumulation.steps=A \
  --steps=$((100000 * A)) --policy.scheduler_warmup_steps=$((1000 * A)) \
  --policy.scheduler_decay_steps=$((30000 * A)) --save_freq=$((20000 * A))
```

The source checkout is the exact primary commit, not `main`; `v0.6.1` is fallback/reference only. `LOCAL_PINNED_SMOLVLA_BASE_SNAPSHOT` must resolve to Hub SHA `4d2f2b37fa245361ef1efe6d91ce96b8bd4af511`, so primary initialization is full pretrained-policy fine-tuning rather than generic `--policy.type=smolvla --policy.load_vlm_weights=true` VLM-only initialization. Let `A=64/B`, where R4 chooses `B=8` first, `16` only with clear headroom, or fallback `4` after OOM. The matching official source/docs define `steps` as microsteps and advance scheduler timing in that loop. R6 must preserve the scaled units shown above; it does not decide versions or alter the protocol. For every long job report only PID, log path, one health check, and recovery command, then wait for user reactivation.
