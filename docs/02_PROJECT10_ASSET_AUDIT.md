# Project10 Asset Audit

**Source inspected:** `D:\600-Robot\300-Project\901-Project10` at commit `072cd4bb9cbf7336284253a56d6c75162adf63df` (2026-08-31). It remains untouched. Its working tree was clean at audit time.

## Historical factual reconstruction

| Question | Evidence-based answer |
|---|---|
| LeRobot | v0.6.0 (repository says pinned, but no vendored commit manifest exists); superseded by 201's v0.6.1 lock |
| model | `lerobot/smolvla_base`, snapshot `c83c316...`; 450M; native feature regeneration from dataset metadata |
| data | `lerobot/libero`, snapshot `a1aaac...`; 1,693 episodes / 273,465 frames |
| data/model contract | 2×256 images, 8D state, 7D action, language max 48; action delta timestamps 0..49/10 |
| train configuration | bf16 claimed in docs; DDP 4 ranks, per-GPU 16, global 64, seed 42, 4 workers/rank, AdamW |
| LR/scheduler | literal `LR=1e-5`; no scheduler is instantiated in M1/M2/M3/M6 |
| accumulation | none (global batch arose from 4×16) |
| checkpoint | `policy.save_pretrained`, `optimizer.pt`, JSON metadata; later processor artifacts added manually/re-saved |
| processor/normalizer | custom overrides using `ds.meta.stats` and mean-std map; m4 repaired missing serialized normalizer files |
| evaluator | official `lerobot.scripts.lerobot_eval.main` invoked by wrapper; `.pruned_init` states 0–9; seed 1000 |
| action execution | chunks length 50; historical test executes 50/10/5, but this is not a current conclusion |
| RNG | M7-R monkeypatches `VLAFlowMatching.sample_noise`, but wrapper seeds per task rather than explicitly per init state |
| EGL | multi-worker rendering failed because node exposed one EGL device; historical workaround combined CUDA visibility with `MUJOCO_EGL_DEVICE_ID=0` |

## `m4_fix_stats.py`

It reconstructs preprocess/postprocess pipelines from dataset stats and saves them into a 5K checkpoint. It was needed because earlier `save_pretrained` output did not carry expected normalizer artifact files. This fixes a real historical integrity failure, but its hard-coded old paths and hand-built overrides make it **reference only**. Current official checkpoint save/reload must be tested instead.

## Classification

| Classification | Assets | Decision |
|---|---|---|
| KEEP / COPY | None at bootstrap | Current official CLI is sufficient; copying no code avoids inherited contracts. |
| REFERENCE ONLY | README, RESULTS, INTERVIEW_GUIDE; `m1_ddp_smoke.py`, `m2_*`, `m3_train.py`, `m6_train.py`, `m4_latency.py`, `m4_aggregate.py`, `m5_*`, `m7r_*`, `m8_figures.py`; compact result JSON/CSV | historical evidence / design inspiration only; do not import or execute as 201 entrypoints. |
| RETIRE | 4-GPU DDP scripts/assumptions; fixed `/root/shared-nvme/project10-vla` paths; `1e-5` unscheduled LR; copying base processor artifacts; conclusion that the compatible released checkpoint is impossible | violates single-card, current-stack, or contract-evidence requirements. |
| UNKNOWN | exact M0 source artifact (not retained), exact LeRobot commit, exact installation lock/pip freeze, raw videos/eval CLI arguments, full m4 evaluator driver | cannot be elevated to evidence without artifacts. |

## Reuse-risk inventory

All `src/*.py` scripts contain hard-coded remote paths. Training scripts import DDP/NCCL and hard-code `world_size=4` logic. `m5_prepare_base.py` creates a symbolic link to model weights; incompatible with the self-contained-artifact standard. `m7r_eval.py` monkeypatches a library method, so it cannot establish baseline parity. `m8_figures.py` hard-codes historical values and paths. No file is copied into 201.

## Lessons retained as requirements, not code

1. Canary a released compatible checkpoint before training.
2. Test every checkpoint by independent reload with its own processor/normalizer.
3. Preserve paired init-state/seed evidence only after the official evaluator is anchored.
4. Treat EGL placement and video generation as gates, not post-hoc polish.
5. Never infer online success from loss alone.
