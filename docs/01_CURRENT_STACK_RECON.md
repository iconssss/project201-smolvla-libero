# Current Stack Reconnaissance

**Research date:** 2026-09-06; amended before any GPU result. All required immutable source revisions are now frozen in `../environment/stack_lock.json`. Hub `main` is never used as a final pin.

## Authoritative sources

- [Official LeRobot LIBERO documentation](https://huggingface.co/docs/lerobot/en/libero): integration, commands, data schemas, 100K recipe, and evaluation protocol.
- [Official SmolVLA documentation](https://huggingface.co/docs/lerobot/en/smolvla): model installation and base-model workflow.
- [Current released compatible checkpoint configuration](https://huggingface.co/HuggingFaceVLA/smolvla_libero/blob/main/config.json): exact policy contract and optimizer defaults.
- [LeRobot v0.6.1 PyPI provenance](https://pypi.org/project/lerobot/0.6.1/): published 2026-08-03; signed source provenance maps tag `v0.6.1` to commit `7e241bd630a3719a56157a497ce5d08f244784f1`.
- [LeRobot v0.6.1 exact source](https://github.com/huggingface/lerobot/blob/7e241bd630a3719a56157a497ce5d08f244784f1/src/lerobot/configs/train.py): training config and CLI-backed schema.
- [LIBERO upstream repository](https://github.com/Lifelong-Robot-Learning/LIBERO): upstream benchmark; it has no formal GitHub releases.

## Selected baseline and pin policy

| Component | Selected source | Pin status |
|---|---|---|
| LeRobot | `huggingface/lerobot` v0.6.1 | tag and commit `7e241bd630a3719a56157a497ce5d08f244784f1` |
| LIBERO integration | LeRobot `.[libero]` extra plus upstream `Lifelong-Robot-Learning/LIBERO` | upstream commit `8f1084e3132a39270c3a13ebe37270a43ece2a01` |
| Training dataset | `lerobot/libero` (recommended official video dataset) | Hub commit `a1aaacb7f6cd6ee5fb43120f673cebb0cfea7dd4` |
| Released evaluator anchor | `HuggingFaceVLA/smolvla_libero` | Hub commit `6721902bc4d61e50a3bfdb11dfb4cb626f05d102` |
| Base initialization | `lerobot/smolvla_base` | Hub commit `4d2f2b37fa245361ef1efe6d91ce96b8bd4af511` |

R1 only verifies this lock after checkout/install; it must not substitute, resolve, or advance any pin.

## LeRobot v0.6.1 / LIBERO / PolicyProcessorPipeline compatibility

No explicit compatibility blocker was found for v0.6.1, LIBERO, SmolVLA, or PolicyProcessorPipeline:

- v0.6.1's published package exposes the `libero` and `smolvla` extras, while current official LIBERO documentation specifies the integration and `lerobot-eval` path.
- The selected released checkpoint's immutable commit is explicitly **“Migrate policy to PolicyProcessorPipeline system”** and bundles the pre/postprocessor JSON plus normalizer/unnormalizer state artifacts.
- v0.6.1's exact `TrainPipelineConfig` loads pre-trained policy configuration and persists the full train configuration/checkpoint path; this matches the pipeline-era checkpoint layout.

This is a static source/metadata compatibility determination. A1 remains the runtime contract gate.

## LeRobot / LIBERO interface

Official LIBERO support is Linux-only; set `MUJOCO_GL=egl` for headless servers. Install with `pip install -e ".[libero]"` after the selected LeRobot checkout. Official evaluation command:

```bash
lerobot-eval --policy.path=POLICY --env.type=libero \
  --env.task=libero_spatial,libero_object,libero_goal,libero_10 \
  --eval.batch_size=1 --eval.n_episodes=10 --env.max_parallel_tasks=1
```

Use `--env.control_mode=relative`; the action contract is relative delta end-effector control. Use `--env.init_states=true` and hard reset for benchmark reproduction. Soft reset is faster but official docs warn it is not bit-identical after settling steps. `batch_size=1` / `max_parallel_tasks=1` is deliberately conservative for single-GPU EGL and paired comparison reliability.

## Standard benchmark

Four primary suites are 10 tasks each: `libero_spatial`, `libero_object`, `libero_goal`, `libero_10` (Long). Official recommendation: 10 episodes/task = 400 per seed, then average three seeds because seed-to-seed variation can be a few percentage points. Success is the environment's native task success predicate; never infer success from episode length or reward proxy.

## Dataset contract

`lerobot/libero` is the recommended official option: 1,693 episodes, 273,465 frames, 40 tasks, LeRobot v3.0 format, two 256×256 RGB views, 8-D state, and 7-D action. It uses MP4 and requires a video backend (`torchcodec` preferred by current docs; PyAV is an alternate historical path); listed download size is 1.9 GB. The equivalent `HuggingFaceVLA/libero` PNG/parquet variant is 69.9 GB and is not selected unless R1 shows video decoding is unavailable.

Observation keys: `observation.images.image` (agent view), `observation.images.image2` (wrist), and `observation.state` (8D: eef position, axis-angle orientation, gripper qpos). Action is continuous `Box(-1,1,(7,))`: 6D eef delta + 1D gripper. Visual feature names and the normalizer's feature names must exactly agree.

## SmolVLA and released checkpoint contract

`lerobot/smolvla_base` is the 450M-base starting point. The selected evaluator anchor is **`HuggingFaceVLA/smolvla_libero`**, not Project10's legacy `lerobot/smolvla_libero` contract. Its published configuration verifies:

| Item | Released compatible configuration |
|---|---|
| inputs | two 3×256×256 images + 8D state + language |
| output | 7D action |
| normalization | visual identity; state/action mean-std |
| chunk / execution | `chunk_size=50`; `n_action_steps=1` |
| language | max 48 tokens |
| flow | 10 denoising steps |
| optimizer defaults | AdamW-style config; LR `1e-4`, betas `(0.9,0.95)`, eps `1e-8`, weight decay `1e-10`, grad clip 10 |
| scheduler defaults | warmup 1000; decay steps 30000; final/decay LR `2.5e-6` |
| trainable policy config | freeze vision encoder; train expert only; train state projection |
| image processing | resize-with-padding to 512×512 in the policy config |

Do not override `n_action_steps` or flow settings in A1/A2. Load the checkpoint's bundled processor and normalization artifacts; inspect and hash them. For own training, use the current library's official trainer and retain its processor output rather than reconstructing it from dataset stats.

## Official primary training recipe

Current official LIBERO documentation specifies:

```bash
lerobot-train --policy.type=smolvla --policy.load_vlm_weights=true \
  --policy.push_to_hub=false --dataset.repo_id=lerobot/libero \
  --dataset.video_backend=torchcodec --output_dir=OUTPUT --steps=100000 --batch_size=64
```

The released compatible checkpoint config supplies the detailed policy optimizer/scheduler values above, resolving Project10's `1e-5` discrepancy in favor of **`1e-4`**. Full policy fine-tuning is **not** assumed: current checkpoint config freezes the vision encoder and trains action expert/state projection.

### Gradient-accumulation audit (v0.6.1 exact source)

The v0.6.1 `TrainPipelineConfig` schema contains `batch_size` but no gradient-accumulation field, and its exact source has no `gradient_accumulation` / `accelerator` configuration. Therefore neither `--accelerator.gradient_accumulation.steps` (documented on moving `main`) nor any guessed alias is valid for this frozen v0.6.1 baseline. The `main` documentation's syntax must not be backported by assumption.

This creates a **formal A4 gate**: A3 may smoke physical batch 4→8→16 (and 32 only with demonstrable VRAM margin), but A4 cannot claim effective batch 64 via official v0.6.1 accumulation until the owner explicitly chooses a compatible, separately audited solution. No custom loop or version change is authorized by this project revision.

## Project10 legacy versus selected current stack

| Topic | Project10 | Current selected baseline |
|---|---|---|
| LeRobot | v0.6.0, custom scripts, 4×4090 DDP | v0.6.1 at `7e241bd`, official CLI first, one 4090 |
| released checkpoint conclusion | legacy `lerobot/smolvla_libero` judged 3 cams/6D | `HuggingFaceVLA/smolvla_libero` verified 2 cams/8D/7D; must canary |
| dataset | `lerobot/libero`, old snapshot hash | same recommended repo but a newly captured immutable revision |
| LR | hand-coded `1e-5` | released config `1e-4` |
| execution | custom/receding chunks, historical tests 50/10/5 | released contract `n_action_steps=1`; no pre-training alteration |
| processors | manually rebuilt/copy-fixed after save issue | official serialized processor must be preserved/reload-tested |
| evaluation | custom wrappers and monkeypatch RNG | official `lerobot-eval` anchor first; paired harness only after parity |

## Known constraints / unresolved items

- Current docs explicitly recommend 400 episodes and three seeds, but do not publish a SmolVLA-LIBERO result table. The released anchor is an operational anchor, not an unverified claimed target number.
- Exact Hub and upstream Git revisions cannot be responsibly inferred from mutable `main`; R0/R1 record them before acquisition.
- A1 validates EGL, MuJoCo, camera keys, processor, normalizer, action semantics, success capture, and video before any training.
