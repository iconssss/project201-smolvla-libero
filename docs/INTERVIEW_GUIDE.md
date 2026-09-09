# Project201 Interview Guide

## 20-second HR version

I completed an end-to-end SmolVLA reproduction on one RTX 4090: 100,000
fine-tuning updates followed by 400 closed-loop LIBERO episodes. The frozen
checkpoint reached 71.5% overall success across 40 tasks. More importantly, I
validated the model/data/action interface, checkpoint reload, controller
horizon, exact episode coverage, and all rollout evidence, so the result is
traceable rather than just a training-loss screenshot.

## 60-second technical version

I started from a pinned full SmolVLA policy, audited a mismatch between its
static 3-camera/6D/6D metadata and LIBERO's runtime 2-camera/8D/7D contract,
and applied the minimal official-factory correction without dropping base
weights. I then completed 100K partial-fine-tuning updates, froze and
strict-reloaded the checkpoint, and evaluated it over four suites, 40 tasks,
and 400 fixed-init episodes. The final endpoint was 71.5%. I also aligned the
closed-loop horizon to one action per replan and rejected vectorized schedulers
that changed episode counts. The project shows that I can own the whole VLA
experimental chain—from stack and checkpoint integrity to closed-loop failure
analysis—while keeping the claim limited to a single-seed simulation result.

## What did you build?

An auditable single-RTX4090 pipeline that fine-tunes SmolVLA from a pinned pretrained-policy snapshot on LIBERO and evaluates the 100K endpoint in a frozen 400-episode closed-loop protocol. The endpoint achieved 71.5% overall success: Spatial 82%, Object 78%, Goal 80%, and Long 46%.

## Why SmolVLA and LIBERO?

SmolVLA provides a practical VLA policy with a serialized processor/policy stack, while LIBERO provides task suites, fixed initialization states, native success predicates, and headless simulation suitable for controlled closed-loop validation. The project’s contribution is careful reproduction engineering rather than a new model.

## How did you handle the camera/state/action mismatch?

The full base checkpoint’s static config showed 3 cameras / 6D state / 6D action, while LIBERO requires two cameras, 8D state, and 7D action. I audited the frozen runtime rather than trusting startup logging: `make_policy()` rebuilt output features from dataset metadata, but rebuilt input features only when empty. The minimal frozen correction `--policy.input_features=null` enabled construction from LIBERO metadata. Strict loading then had 0 missing, 0 unexpected, and 0 shape-mismatched keys; a real processed batch confirmed the final contract.

## Why is this not full fine-tuning?

Runtime parameter audit showed 99.88M of 450.05M parameters trainable, with the entire 86.43M-parameter vision encoder frozen. The accurate term is pretrained-policy initialization followed by partial-parameter fine-tuning.

## Why use `n_action_steps=1`?

The released anchor’s native horizon was 1 while A4’s checkpoint default was 50. Since the evaluator invokes `select_action()` once per environment step, native horizons would compare different closed-loop replanning frequencies. The approved evaluator-only override set both to 1 without altering checkpoints, processors, data, source, or revisions.

## Why W1 serial execution despite low GPU utilization?

GPU utilization is bursty in serial closed-loop simulation: EGL physics/rendering, observation processing, and per-step inference alternate. W2/W4 experiments did not preserve semantics: five requested episodes produced six/eight videos and changed success sequences. W1 was therefore the only validated exact-episode configuration. Low utilization alone is not evidence that a higher-batch execution is scientifically interchangeable.

## How did you make the benchmark credible?

Pins, checkpoint hashes, command/config snapshots, offline mode, EGL, hard reset, fixed init states, task coverage, machine-readable results, 400 videos, and error scans were all retained. A5 completed 400 episodes and 40 task records under one frozen protocol; the final audit found no OOM, NaN/Inf, Traceback, processor/data/contract errors, or checkpoint corruption.

## What would you do next?

First analyze the existing endpoint artifacts, especially the Long-suite gap, without changing the completed result. Any additional seed, scheduler/evaluator engineering, ablation, or real-robot work requires a new explicit protocol and authorization.

## Claims I deliberately do not make

- Not SOTA and not a novel model architecture.
- Not full-parameter fine-tuning: 99.88M / 450.05M parameters were trainable.
- Not a multi-seed significance claim; the released-anchor comparison is
  descriptive only.
- Not a real-robot deployment result.
