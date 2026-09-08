# Project201 — SmolVLA × LIBERO

Project201 is an auditable, single-RTX-4090 reproduction of partial-parameter SmolVLA fine-tuning and closed-loop evaluation in LIBERO. It focuses on a reproducible runtime contract, checkpoint integrity, and preserved evaluation evidence.

## Pipeline

`Pinned pretrained policy → LIBERO runtime-contract construction → partial-parameter fine-tuning → checkpoint audit → frozen closed-loop evaluation → machine-readable results, videos, and logs`

## Training

- Initialization: immutable full `lerobot/smolvla_base` pretrained-policy snapshot.
- A4: PASS — 100,000 optimizer updates, effective batch 64, and 6.4M sample presentations on one RTX 4090.
- Fine-tuning scope: 99,880,992 of 450,046,176 parameters were trainable; the 86,433,024-parameter vision encoder remained frozen.
- Runtime-contract correction: `--policy.input_features=null` lets the frozen runtime construct the actual LIBERO interface (two cameras, 8D state, 7D action) while preserving strict checkpoint loading.

## A5 closed-loop endpoint result

A5: PASS. The frozen endpoint evaluation uses four LIBERO suites, task IDs 0–9, 10 fixed-init episodes per task, seed 0, hard reset, relative control, native LIBERO success predicate, and common `n_action_steps=1`. Execution is W1 serial (`batch_size=1`, synchronous environment, one parallel task) on one GPU.

| Suite | Episodes | Endpoint success |
| --- | ---: | ---: |
| Spatial | 100 | 82.0% |
| Object | 100 | 78.0% |
| Goal | 100 | 80.0% |
| LIBERO-10 / Long | 100 | 46.0% |
| **Overall** | **400** | **71.5% (286/400)** |

This is a single-seed, fixed-init-state, simulated closed-loop LIBERO endpoint result. It is a reproducible endpoint observation, not a causal comparison, a multi-seed statistical estimate, or a real-robot result.

## Evidence and analysis

- [A4 checkpoint finalize audit](docs/A4_FINALIZE_AUDIT.md)
- [A5 final audit](docs/A5_FINAL_AUDIT_REPORT.md)
- [A2 vs A5 task-level descriptive comparison](docs/A2_A5_DESCRIPTIVE_COMPARISON.md)
- [A4 training dynamics from the existing log](docs/A4_TRAINING_DYNAMICS.md)
- [Frozen revisions and environment lock](environment/stack_lock.json)

Large data, checkpoints, videos, raw results, caches, logs, and credentials are excluded from Git. The public repository retains documentation, scripts, aggregate tables, and visualizations needed to understand the completed run.
