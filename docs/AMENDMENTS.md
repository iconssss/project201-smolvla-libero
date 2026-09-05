# Amendments

## 2026-09-06 — PRE-GPU stack and memory-protocol correction

- **Old:** LeRobot v0.6.0 with deferred R1 revision resolution; A3 probes 16→32→64 and assumes gradient accumulation alternatives.
- **New:** LeRobot `v0.6.1` at `7e241bd630a3719a56157a497ce5d08f244784f1`; all Git/Hub revisions locked in `environment/stack_lock.json`; A3 probes 4→8→16 and 32 only with batch-16 headroom.
- **Reason:** authoritative PyPI provenance and exact v0.6.1 source audit. The source lacks a gradient-accumulation configuration field, so a `main`-only CLI flag must not be invented.
- **Result exposure:** none. No GPU, remote connection, download, training, evaluation, or result existed before this amendment; it is not result-driven.
- **Interpretation:** A4 remains blocked until the owner explicitly approves a compatible solution that preserves effective batch 64. This amendment does not alter any reported experimental result because none exists.
