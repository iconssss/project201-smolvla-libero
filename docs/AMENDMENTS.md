# Amendments

## 2026-09-06 — PRE-GPU stack and memory-protocol correction

- **Old:** LeRobot v0.6.0 with deferred R1 revision resolution; A3 probes 16→32→64 and assumes gradient accumulation alternatives.
- **New:** LeRobot `v0.6.1` at `7e241bd630a3719a56157a497ce5d08f244784f1`; all Git/Hub revisions locked in `environment/stack_lock.json`; A3 probes 4→8→16 and 32 only with batch-16 headroom.
- **Reason:** authoritative PyPI provenance and exact v0.6.1 source audit. The source lacks a gradient-accumulation configuration field, so a `main`-only CLI flag must not be invented.
- **Result exposure:** none. No GPU, remote connection, download, training, evaluation, or result existed before this amendment; it is not result-driven.
- **Interpretation:** A4 remains blocked until the owner explicitly approves a compatible solution that preserves effective batch 64. This amendment does not alter any reported experimental result because none exists.

## 2026-09-06 — Current-main native-accumulation launch protocol

- **Old:** `v0.6.1` / `7e241bd630a3719a56157a497ce5d08f244784f1` was the primary training baseline, so A4 was blocked by its absent accumulation runtime; A2 preceded A3; the generic VLM-only SmolVLA command was ambiguous with primary initialization.
- **New:** primary LeRobot is immutable official-main snapshot `3f2c29ef7e44b1ddccbcda3b6a63939e53639e9e`; v0.6.1 remains stable fallback/reference only and must never mix with primary. Primary initialization is full `lerobot/smolvla_base` fine-tuning from Hub SHA `4d2f2b37fa245361ef1efe6d91ce96b8bd4af511` through a local immutable `--policy.path` snapshot.
- **Reason:** post-v0.6.1 official accelerator work provides native gradient accumulation. Static audit of the frozen source and matching docs confirms `--accelerator.gradient_accumulation.steps=<a>`, micro-batch `steps`, scheduler advancement in the micro-batch loop, and pretrained-policy path resolution.
- **Protocol:** A1 canary → A3 (batch 8, then 16 only with headroom; 4 OOM fallback) → A2 400-episode anchor → freeze A4 config → A4. Set `a=64/b`; target 100K optimizer updates / 6.4M presentations with all timing values scaled to microsteps. Physical batch 32/64 probes are excluded.
- **Result exposure:** none. This amendment occurs before any GPU result, remote connection, model/data acquisition, training, or evaluation. It is a PRE-GPU protocol correction, **not a result-driven change**.

## 2026-09-07 — PRE-A4 training-throughput preflight

- **Old frozen execution configuration:** physical batch 16 with gradient accumulation 4, while preserving effective batch 64.
- **Measured candidates:** with identical immutable assets, full pretrained-policy initialization, optimizer/scheduler policy, precision, seed, TorchCodec, one GPU, and effective batch 64, B16/A4, B32/A2, and B64/A1 each completed a warmup plus 20 measured optimizer updates. Their steady throughputs were respectively 85.53, 116.40, and 118.75 samples/s; their process-NVML peaks were 5.27, 8.58, and 14.91 GiB. All runs had finite loss/gradients and no OOM/NaN/Inf.
- **New frozen execution configuration:** B64/A1. This is the shortest observed update time (0.53895 s/update), 27.97% faster than B16/A4, while retaining 9.65 GiB below the 24.56 GiB GPU capacity. The scientific target is unchanged: effective batch 64, 100,000 optimizer updates, and 6.4M sample presentations. Accordingly the formal microstep schedule is 100,000 total, warmup 1,000, decay 30,000, and checkpoint interval 20,000.
- **Execution layer:** `num_workers=4`, prefetch factor 4, persistent workers, and spawn were retained. Source audit confirms these are DataLoader parallelism controls; sampler, sample ordering, data semantics, optimizer, scheduler, and seed are unchanged.
- **Result exposure:** none; optimization was performed before A4 launch. This is a PRE-A4 execution optimization, **not a result-driven amendment**. The frozen remote evidence is `environment/a4_speed_preflight_B16_A4.json`, `environment/a4_speed_preflight_B32_A2.json`, `environment/a4_speed_preflight_B64_A1.json`, and `environment/PRE_A4_THROUGHPUT_AMENDMENT.md`.

## 2026-09-07 — PRE-A4 LIBERO input-contract correction

- **Original full-base static contract:** the immutable `lerobot/smolvla_base` config declares three cameras, 6D state, and 6D action.
- **Frozen-source behavior:** `make_policy()` always rebuilds `output_features` from current dataset metadata, but rebuilds `input_features` only when the pretrained config's input features are empty. The startup config is logged before dataset construction and `make_policy()`, so its static 3/6/6 display is not the processed-batch contract.
- **Correction:** retain the complete immutable pretrained-policy path and add only `--policy.input_features=null`. This lets official `make_policy()` derive the task-specific input and output interfaces from frozen LIBERO metadata.
- **Corrected runtime contract:** two cameras, 8D state, and 7D action. Processor normalization uses the frozen LIBERO dataset statistics after the recorded rename map.
- **Weight integrity:** strict pretrained loading completed with 0 missing keys, 0 unexpected keys, and 0 shape mismatches. Full `smolvla_base` initialization is preserved; this is not the generic `policy.type=smolvla` plus VLM-only initialization recipe.
- **Invalid prefix:** the earlier approximately 70-microstep launch is designated `INVALID_PRECONTRACT_RUN`; it has no valid checkpoint and must never be resumed or included in A4 results.
- **Result exposure:** this correction is frozen before the first valid A4 training run starts. It follows a contract audit and does not use a valid A4 training result to select or tune the method; therefore it is **not result-driven**.

## 2026-09-07 — A5 common closed-loop horizon protocol

- **Observed checkpoint defaults:** the released anchor has `chunk_size=50, n_action_steps=1`; A4 final has `chunk_size=50, n_action_steps=50`.
- **New A5 evaluator protocol:** both anchor and A4 evaluations use `--policy.n_action_steps=1`. This is a per-evaluation runtime override, not a checkpoint, source, processor, dataset or revision modification.
- **Reason:** the frozen evaluator invokes `policy.select_action()` once per environment step. Keeping the distinct native horizons would compare different closed-loop re-inference frequencies rather than only policies. Common `1` matches the released anchor's native configuration.
- **Verification:** exact A4 runtime smoke confirmed override parsing, preserved 2-camera/8D-state/7D-action contract, and showed the override queue is empty after each action (replan on the next environment step). A bounded 5-episode protocol smoke completed without contract/runtime errors. Evidence: remote `environment/A5_HORIZON_ANALYSIS.md`.
- **Scope:** this amendment freezes only the A5 evaluator controller horizon. Task list, fixed init states, seed mapping, reset, timeout, native success predicate, processors, assets and primary checkpoint remain unchanged.
