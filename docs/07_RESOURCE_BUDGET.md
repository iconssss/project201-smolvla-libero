# Resource Budget (planning estimate; no remote measurement yet)

## Storage

The only dataset selected by default is video-backed `lerobot/libero` (official listed download: 1.9 GB). Its 69.9-GB PNG alternative is a contingency, not an additional baseline download. SmolVLA/released weights, Python/CUDA packages, and checkpoint serialization are not yet measured under the selected tag, so this budget intentionally reserves substantially above nominal model files.

| Category | Planning allowance | Basis / caveat |
|---|---:|---|
| environment + PyTorch + build/cache | 25 GB | can vary strongly with CUDA wheels and source build cache |
| LeRobot/LIBERO source and dependencies | 5 GB | excludes duplicated conda/pip caches after cleanup |
| selected LIBERO data + metadata/decode cache | 8 GB | 1.9-GB official download plus margin |
| HF model/released-anchor/base cache | 12 GB | 0.5–0.6B models plus duplicate revisions and snapshots |
| active output/temp + logs | 15 GB | decode, reports, retained raw outputs |
| one resumable checkpoint | 4 GB reserve | conservative: model + optimizer/scheduler/processors; measure at R7 |
| mandated six checkpoints + best | 28 GB | 7 × 4 GB reserve; deduplicate only after hash verification |
| rollout videos | 20 GB | representative all stages + compressed final set; cap and index |
| operational free-space reserve | 20 GB | downloads/checkpoint atomic writes |

| Tier | Capacity | Interpretation |
|---|---:|---|
| Minimum | **100 GB** | only if R2/R5 measurements confirm ≤4-GB checkpoints and video cap is enforced |
| Recommended | **150 GB** | practical requested shared persistent volume; supports stated checkpoint/video evidence with margin |
| Comfortable | **250 GB** | permits an image-dataset contingency, additional validation artifacts, or interrupted downloads without cleanup pressure |

**Recommendation:** request **250 GB persistent shared NVMe** if available; accept **150 GB only** with the video-backed dataset and a written checkpoint/video quota. Do not request 100 GB unless R2/R5 actual size evidence validates it.

## GPU-time estimate

These are ranges, not promises. They must be recalculated from A1/A2 episode seconds and A3 measured step time.

| Phase | Estimate on 1×4090 | Assumption |
|---|---:|---|
| A1 canary (15 episodes) | 0.5–2 h | first-time JIT/cache/EGL/debug allowance dominates |
| A3 smoke | 1–3 h | batch 8, conditional 16, and batch 4 only after OOM; report microstep timing |
| A2 released anchor (400 episodes) | 8–24 h | 1.2–3.6 min/episode including reset/video; measure before treating as budget |
| A4 100K updates | pending A3 measurement | `100000 × a × measured_microstep_seconds / 3600`, plus checkpoint overhead; 400K microsteps at b=16/a=4 or 800K at b=8/a=8 |
| A5 quick/intermediate eval | 4–18 h | coverage intentionally deferred until episode time is known |
| A5 endpoint 400 episodes | 8–24 h | same measured rate as A2 |
| A5 three seeds (1200 episodes) | 24–72 h | three complete 400-episode runs |

The old fixed A4 wall-clock range is retired because current-main counts microsteps, not optimizer updates. A3 supplies the only valid per-microstep basis for the A4 estimate. Mandatory pre-training work is A1+A3+A2; if A1 fails, A3/A2/A4–A5 are not spent, and if A2 fails its credibility gate, A4–A5 are not spent.

## Network and local backup

- Initial selected data transfer: official listed 1.9 GB; reserve 5–10 GB for retry/metadata overhead.
- Models and dependencies: reserve 15–30 GB total download traffic until R2 records exact bytes; do not claim an exact size pre-download.
- At each milestone copy small, decisive evidence to the local repository: environment/stack lock, commands, configs, manifests, hashes, result JSON/CSV, aggregated figures, and video index.
- Retain raw videos/checkpoints on persistent remote storage, then selectively copy representative videos and final checkpoint manifests locally; never commit model/data/credentials.
