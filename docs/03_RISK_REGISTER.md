# Risk Register

| Risk | P | Impact | Detection | Mitigation | Stop / pivot |
|---|---|---:|---|---|---|
| Released checkpoint contract mismatch | M | Critical | A1 feature/action/video canary | pin model + processor revision; inspect config | no sensible action/success semantics: stop before training |
| Primary source drift/mix | M | Critical | R1 `git rev-parse HEAD`, `lerobot-* --help`, import/version manifest | source checkout at `3f2c29e`; stable `v0.6.1` reference only | any moving-main or fallback mix: stop and restore exact checkout |
| Accumulation/schedule unit error | M | Critical | R1 help + frozen command review; training banner factorization | use only `--accelerator.gradient_accumulation.steps=A`; scale steps, warmup, decay and saves in microsteps | semantic mismatch: stop before A4 and amend |
| LIBERO API mismatch | M | High | R1 import + one hard reset | pin upstream and package versions | cannot create/reset: stop A1 |
| Processor/normalizer mismatch | M | Critical | hash artifacts; checkpoint reload forward | load bundled processor, preserve serialized pipeline | mismatch/nonfinite output: stop |
| EGL/MuJoCo failure | M | High | A1 headless render/video | `MUJOCO_GL=egl`, single task/env, audit GPU mapping | no reliable render: stop before A2 |
| Batch OOM | M | High | A3 batch 8 first; 16 only with clear 8-batch headroom; 4 only after OOM | record allocated/reserved VRAM and retain effective-batch-64 requirement | no stable divisor-of-64 batch: stop; no batch-32/64 probe |
| Incorrect initialization | M | Critical | R2 manifest plus R6 inspect resolved `--policy.path` | full local `smolvla_base` SHA snapshot; generic VLM-only command is reference only | wrong/mutable snapshot: stop before A3/A4 |
| Throughput too low | M | Medium | A3 measured step time | tune workers/backend only after correctness | revise GPU budget before A4 |
| Eval wall-clock excessive | M | Medium | A1/A2 measured episode time | staged quick/medium/full evaluation | budget breach: amend eval cadence, not semantics |
| Video disk growth | M | Medium | track bytes/episode | canary all; full benchmark representative videos only | disk threshold: stop new videos after manifest |
| HF cache/data size surprise | M | High | R2 `du`, free space checks | isolated cache; use 1.9-GB video data | below reserve threshold: stop download |
| Checkpoint disk growth | H | High | measure first checkpoint | retain mandated 20/40/60/80/100K + best; hash | insufficient durable storage: do not launch A4 |
| Instance interruption | M | High | heartbeat/system audit | frequent resumable checkpoints, local manifests | cannot resume exact state: log and amend |
| Resume corrupted/incomplete | M | High | R7 first-checkpoint reload smoke | validate model, optimizer, scheduler, processors | reload failure: repair before continuation |
| Network/download failure | M | Medium | R2 hash/retry logs | resumable Hub transfer, cache manifest | repeated failures: preserve partial state and pause |
| Dataset revision drift | M | Critical | capture immutable SHA before fetch | revision CLI flag everywhere | missing pin: results non-comparable, stop |
| Stochastic results | H | High | same init states/seeds; 3 seeds | official hard resets; paired analysis secondary | unstable anchor: diagnose evaluator first |
