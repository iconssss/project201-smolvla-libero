# Flagship A — SmolVLA × LIBERO

Single-RTX-4090, current-stack reproduction project: fine-tune SmolVLA base on the 40-task LIBERO dataset and evaluate in closed loop on Spatial, Object, Goal, and Long.

Status: **PRE-GPU MODIFY — immutable stack is locked; the v0.6.1 gradient-accumulation gate is blocked. No training, model/dataset download, remote connection, or GPU execution has occurred in this repository.**

The primary objective is a credible portfolio-quality VLA positive result, not a research ablation. The released checkpoint must first validate the evaluator before any training starts.

Read in order:

1. `docs/00_PROJECT_CHARTER.md`
2. `docs/01_CURRENT_STACK_RECON.md`
3. `docs/02_PROJECT10_ASSET_AUDIT.md`
4. `docs/04_PRIMARY_PROTOCOL_DRAFT.md`
5. `docs/05_REMOTE_EXECUTION_PLAN.md`
6. `docs/07_RESOURCE_BUDGET.md`

Large data, checkpoints, videos, caches, and credentials are intentionally ignored by Git. See `checkpoints/` for the artifact manifest convention.
