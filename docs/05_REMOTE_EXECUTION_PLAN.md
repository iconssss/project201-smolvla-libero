# Remote Execution Plan (do not execute until explicitly authorized)

Remote root: `/root/shared-nvme/201-smolvla-libero`. All commands below are templates, never credentials. Every GPU command prefixes `CUDA_VISIBLE_DEVICES=0`; no `torchrun` or multi-GPU launcher.

| Phase | Prepared action | Pass / stop | Outputs / backup |
|---|---|---|---|
| R0 connect + audit | interactive `plink.exe` connection; capture `uname`, disk, `nvidia-smi`, driver, CUDA, RAM | pass: one 4090 24GB and durable free space; stop if different | `environment/system_manifest.txt`; copy local |
| R1 bootstrap | checkout locked v0.6.1 commit, install selected extras in `env/`, set `MUJOCO_GL=egl`; record `pip freeze`, commits and CLI help | pass: exact lock verifies; stop on version/API mismatch | install log and verification addendum |
| R2 acquire | set project-local HF cache; fetch only locked base, released anchor, dataset revisions | pass: hashes, free-space reserve, decode one sample; stop on mismatch/disk | download manifest, `du`, SHA files |
| R3 A1 canary | `lerobot-eval` with one selected task, batch 1, 3 episodes, init states, hard reset, video | pass: all canary contract gates; stop before training otherwise | eval JSON, videos, command log |
| R4 A2 anchor | official four-suite command, 10/task, batch 1, max parallel tasks 1 | pass: credible released-anchor behavior; stop for implausibly low SR | raw JSON/CSV, selected videos, summary |
| R5 A3 smoke | 4→8→16 physical batch; 32 only with clear batch-16 headroom | pass: finite/stable evidence; no physical-64 probe | memory/throughput table |
| R6 confirmation | verify pins and write command/config; resolve the documented v0.6.1 effective-batch gate by owner amendment | pass: approved exact accumulation mechanism; stop if absent | frozen run config + amendment |
| R7 100K | prohibited until R6 passes; then launch single process, health check once, and stop monitoring | pass: finite metrics/checkpoints/reload; stop on integrity failure | logs, checkpoints, hashes, backup manifest |
| R8 evaluation | predeclared checkpoint coverage, then endpoint 400×seed0 and conditional seeds 1/2 | pass: all raw + aggregate evidence preserved | result JSON/CSV, figures, videos, report |

## Command skeletons

```bash
export CUDA_VISIBLE_DEVICES=0 MUJOCO_GL=egl HF_HOME=/root/shared-nvme/201-smolvla-libero/cache/hf
lerobot-eval --policy.path=PINNED_RELEASED_MODEL --env.type=libero \
  --env.task=libero_spatial --env.task_ids='[0]' --eval.batch_size=1 \
  --eval.n_episodes=3 --env.init_states=true --env.hard_reset=true \
  --env.control_mode=relative --env.max_parallel_tasks=1 --seed=0

lerobot-train --policy.type=smolvla --policy.load_vlm_weights=true \
  --policy.push_to_hub=false --dataset.repo_id=lerobot/libero --dataset.revision=PIN \
  --dataset.video_backend=torchcodec --output_dir=OUTPUT --steps=100000 --batch_size=PHYSICAL_BATCH
```

`--accelerator.gradient_accumulation.steps` is **not** included: it is absent from locked v0.6.1 source. Do not replace it with a guessed alias. R6 needs owner-approved resolution before this training skeleton is executable. For every long job report only PID, log path, one health check, and recovery command, then wait for user reactivation.
