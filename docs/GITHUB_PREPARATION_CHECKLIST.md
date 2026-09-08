# GitHub Preparation Checklist

## Ready for review

- [x] A5 result summary and audit are written with bounded claims.
- [x] README draft is separate (`README_A5_DRAFT.md`); the existing root README is not overwritten automatically.
- [x] Interview guide covers implementation, contract correction, evaluation semantics, and low GPU utilization.
- [x] Large checkpoints, videos, outputs, logs, caches, and the local credential document remain ignored.

## Review before any commit

- [ ] Merge or replace the legacy root README deliberately; it currently describes the obsolete PRE-GPU state.
- [ ] Review `git status` and preserve pre-existing user changes before staging.
- [ ] Verify `.agents/references/PARATERA_LOCAL_CREDENTIAL.md` remains ignored and contains no copied credential in tracked files.
- [ ] Keep remote output paths and private instance identifiers out of public-facing prose where unnecessary.
- [ ] Decide whether to publish lightweight result tables/selected provenance manifests only; do not add checkpoints, videos, or raw runtime caches.
- [ ] Review result wording: simulated single-seed closed-loop LIBERO result, not SOTA, real-robot deployment, universal improvement, or full fine-tuning.

## No automatic Git action

No commit, tag, remote creation, or push was performed. A human review should select the final README and staging set.

