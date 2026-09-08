# A5 Result Summary

Project201 is a single-RTX4090 reproduction of SmolVLA fine-tuning on LIBERO. The project first validated the released checkpoint evaluator, then fine-tuned from the immutable full `lerobot/smolvla_base` pretrained-policy snapshot, and finally evaluated the frozen 100K endpoint in closed loop.

## Training and checkpoint

- A4 completed 100,000 optimizer updates at effective batch 64 (6.4M sample presentations) on one RTX 4090.
- The primary checkpoint is `A4_100k_final/checkpoints/100000/pretrained_model`.
- This is **pretrained-policy initialization with partial-parameter fine-tuning**: 99,880,992 of 450,046,176 parameters were trainable; the 86,433,024-parameter vision encoder remained frozen.
- A pre-launch contract audit found that the base checkpoint’s static interface did not represent the LIBERO runtime interface. The frozen `--policy.input_features=null` correction allowed `make_policy()` to rebuild the 2-camera / 8D-state / 7D-action interface from LIBERO metadata, while strict loading retained zero missing, unexpected, or shape-mismatched keys.

## A5 closed-loop protocol

The final evaluation used four LIBERO suites, task IDs 0–9, 10 fixed-init-state episodes per task, seed 0, hard reset, relative control, native success predicate, 256×256 observations, and W1 serial execution. Both policies’ closed-loop controller horizon was fixed through the evaluator to `n_action_steps=1`; batch size was 1, async environments were disabled, and maximum parallel tasks was 1.

## Final result

| Suite | Episodes | Success rate |
| --- | ---: | ---: |
| Spatial | 100 | 82.0% |
| Object | 100 | 78.0% |
| Goal | 100 | 80.0% |
| LIBERO-10 / Long | 100 | 46.0% |
| **Overall** | **400** | **71.5% (286/400)** |

The evaluator reported 25,604.024 s pure rollout time (64.010 s/episode). All 400 videos, `eval_info.json`, the final log, and frozen command/config snapshots were preserved. The final audit found no OOM, NaN/Inf, Traceback, processor/data/contract error, or checkpoint-corruption match.

## Archive-ready wording and supporting analyses

Recommended public wording: “A single-seed closed-loop LIBERO reproduction using pretrained-policy initialization and partial-parameter fine-tuning, with a frozen vision encoder, reached 71.5% endpoint success (286/400) under a frozen 400-episode protocol.”

The task-level comparison is documented in [A2_A5_DESCRIPTIVE_COMPARISON.md](A2_A5_DESCRIPTIVE_COMPARISON.md); it is an endpoint/descriptive comparison, not a causal statement or a multi-seed statistical estimate. Existing-log training dynamics are documented in [A4_TRAINING_DYNAMICS.md](A4_TRAINING_DYNAMICS.md).

## Scope of the claim

This is a reproducible, single-GPU, single-seed closed-loop LIBERO result. The retained artifacts support inspection and rerun planning, but this result alone does not justify SOTA, full-parameter fine-tuning, universal-improvement, or real-robot-deployment claims.
