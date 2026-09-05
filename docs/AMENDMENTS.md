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
