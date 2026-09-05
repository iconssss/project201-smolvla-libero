# Primary Protocol Draft

**Status:** Draft frozen for PRE-GPU execution ordering. Exact immutable revisions are locked in `environment/stack_lock.json`; R1 only verifies them. Any later change requires `AMENDMENTS.md`.

## PRIMARY

### A0 — reconnaissance (complete)

Current-stack and historical-asset audits are complete. Gate: this document and remote plan committed locally.

### A1 — released-checkpoint canary

Load pinned `HuggingFaceVLA/smolvla_libero` with its bundled processors. First run: one task × three official fixed init states, `batch=1`, hard resets, relative control, video enabled. Then Spatial tasks 2 and Long tasks 2, three episodes each. Record reset/action/success/video evidence.

**Pass:** render, state/image keys, processor/normalizer, finite actions, termination, native success predicate, and playable video all work; behavior is materially non-pathological. **Stop:** any contract, rendering, or semantic failure. A1 is first: failure prohibits A3, A2, and A4 until repaired and re-canary-passed.

### A3 — single-GPU training smoke

Use the current-main official trainer, the full pinned base snapshot, and pinned dataset for tens of microsteps. On exactly one RTX 4090 24 GB, attempt **physical batch 8 first**. Attempt **16 only with clear VRAM headroom at 8**. Use **4 only as an OOM fallback**. Do not try 32 in this primary smoke and never probe physical 64 merely to manufacture an OOM. Measure peak allocated VRAM, peak reserved VRAM, step time, samples/s, GPU utilization, CPU/RAM, finite loss/grads, and processor/data errors. Do not extrapolate Project10 memory figures.

Let final physical batch be `b`, only where `b` is an integer factor of 64. Set `a = 64 / b` with the exact official primary-source flag `--accelerator.gradient_accumulation.steps=<a>`. Effective batch is therefore `b × 1 GPU × a = 64`: batch 8 uses accumulation 8, batch 16 uses accumulation 4, and fallback batch 4 uses accumulation 16. The trainer remains unmodified.

### A2 — released-checkpoint anchor

Only after A3 selects `b`, run the pinned released policy through four standard suites × 10 tasks × 10 official episodes = 400 at seed 0, hard reset, one parallel task. Store per-episode result JSON and representative videos. Do not claim paper parity without an official checkpoint result table. **Gate:** results must show credible task-directed behavior; implausibly low aggregate results trigger evaluator diagnosis, not training.

### Freeze exact A4 configuration

After A2 passes, freeze the primary source SHA, every Hub/Git SHA, resolved local full-base `--policy.path`, selected `b`, `a`, the exact command, and expected output directory. Do not reselect pins or batch size during A4.

### A4 — main training

Train from the **full pinned `lerobot/smolvla_base` pretrained policy snapshot** via the current-main `--policy.path` mechanism; do not replace it with the generic `--policy.type=smolvla --policy.load_vlm_weights=true` VLM-only reference path. Target 100,000 optimizer updates at effective batch 64, hence 6.4M sample presentations. Because `steps` means microsteps, set `micro_steps = 100000 × a`, `warmup_microsteps = 1000 × a`, `decay_microsteps = 30000 × a`, and `save_freq_microsteps = 20000 × a`.

For batch 8/accumulation 8, that is 800,000 microsteps (warmup 8,000; decay 240,000; save every 160,000). For batch 16/accumulation 4, it is 400,000 microsteps (warmup 4,000; decay 120,000; save every 80,000). Record both `microstep` and `optimizer_update`; checkpoints are semantically 20K/40K/60K/80K/100K **optimizer updates**. Current released-policy defaults (LR `1e-4`, warmup 1000 updates, decay 30K updates to `2.5e-6`) are preserved in these scaled units.

Save resumable checkpoints at those semantic labels and best only if a predeclared validation criterion exists. Each save includes config, model, optimizer, scheduler, processor, normalizer, RNG/meta state, manifest/hash, stdout, metrics. Reload smoke a first checkpoint before proceeding beyond it.

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
