# Primary Protocol Draft

**Status:** Draft frozen for PRE-GPU execution ordering. Exact immutable revisions are locked in `environment/stack_lock.json`; R1 only verifies them. Any later change requires `AMENDMENTS.md`.

## PRIMARY

### A0 — reconnaissance (complete)

Current-stack and historical-asset audits are complete. Gate: this document and remote plan committed locally.

### A1 — released-checkpoint canary

Load pinned `HuggingFaceVLA/smolvla_libero` with its bundled processors. First run: one task × three official fixed init states, `batch=1`, hard resets, relative control, video enabled. Then Spatial tasks 2 and Long tasks 2, three episodes each. Record reset/action/success/video evidence.

**Pass:** render, state/image keys, processor/normalizer, finite actions, termination, native success predicate, and playable video all work; behavior is materially non-pathological. **Stop:** any contract, rendering, or semantic failure. Training is prohibited until repaired and re-canary-passed.

### A2 — released-checkpoint anchor

Pinned released policy; four standard suites × 10 tasks × 10 official episodes = 400 at seed 0, hard reset, one parallel task. Store per-episode result JSON and representative videos. Do not claim paper parity without an official checkpoint result table. **Gate:** results must show credible task-directed behavior; implausibly low aggregate results trigger evaluator diagnosis, not training.

### A3 — single-GPU training smoke

Current official trainer, selected base + pinned dataset, **physical batch 4 → 8 → 16** for tens of steps. Measure peak allocated/reserved VRAM, step time, samples/s, utilization, CPU/RAM, finite loss/grads, and decode errors. Try 32 only if batch 16 has clear VRAM headroom; never probe physical 64 merely to create an OOM. Do not extrapolate Project10 memory figures.

The effective-batch-64 goal is retained, but v0.6.1 has no official gradient-accumulation flag in its exact source. Thus A3 supplies memory evidence only; it does not authorize A4 at an unverified lower effective batch or with a fabricated CLI argument.

### A4 — main training

**Blocked pending the gradient-accumulation gate above.** Once resolved by owner-approved amendment, train the official 100K recipe. Current policy baseline: LR `1e-4`, warmup 1000, decay 30K to `2.5e-6`, frozen vision encoder/action-expert-state-projection semantics. Save resumable checkpoints at 20K/40K/60K/80K/100K and best only if a predeclared validation criterion exists. Each save includes config, model, optimizer, scheduler, processor, normalizer, RNG/meta state, manifest/hash, stdout, metrics. Reload smoke a first checkpoint before proceeding beyond it.

### A5 — evaluation

First measure episode wall-clock. Intermediate checkpoints receive predeclared quick/medium coverage only. The 100K primary endpoint gets 400 episodes at seed 0. If it reaches the display/relative target, run seeds 1 and 2 (1200 total). Report suite/task rates, uncertainty, exact seed/init state protocol, and paired deltas only as supplementary analysis.

## Success standard

After A2 locks an anchor, primary relative goal is ours ≥ anchor − 5 percentage points under the same pinned evaluator/init states/seeds. Portfolio objective: four-suite average ≥75%, target ≥80%. <60% is not completed flagship evidence and triggers analysis rather than parameter fishing.

## SECONDARY / OPTIONAL (not automatically authorized)

- Intermediate learning curve beyond minimal checkpoints.
- Paired RNG-controlled statistics / bootstrap / McNemar as auxiliary, not sole proof.
- `n_action_steps` or replanning semantics.
- Data scaling.
- Latency/asynchronous execution.

These remain inputs to Flagship B unless explicitly authorized after primary completion.
