# Project Charter

## Objective

On exactly one RTX 4090 (24 GB), reproduce the current official SmolVLA × LIBERO pipeline from `lerobot/smolvla_base`, then produce auditable closed-loop results across LIBERO Spatial, Object, Goal, and Long. Preserve resumable checkpoints, hashes, environment manifest, result JSON/CSV, and representative success/failure videos.

## Non-negotiable constraints

- One GPU only; no DDP, FSDP, ZeRO, or multi-GPU fallback.
- Current official stack is authoritative; Project10 is history and engineering evidence only.
- Released-checkpoint evaluator validation precedes our training.
- Primary reproduction precedes research extensions.
- Any post-freeze change is logged in `AMENDMENTS.md`; failed runs remain in the ledger.
- Runtime must not import, symlink, or depend on `901-Project10`.

## Scope

Primary: A0–A5 in `04_PRIMARY_PROTOCOL_DRAFT.md`. Future latency/replanning/data-scaling work is explicitly secondary and requires a new authorization/amendment.

## Evidence standard

Every expensive run records command, UTC timestamps, code commit, exact Hub revisions, seeds, system manifest, config, checkpoint hash, machine-readable result, and video provenance. A reload test is required for each final checkpoint format.
