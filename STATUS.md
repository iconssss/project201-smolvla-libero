# Status

**Milestone:** PRE-GPU revision audit completed on 2026-09-06 (Asia/Shanghai). Stack pins are frozen in `environment/stack_lock.json`.

**Authorized now:** local repository/documentation work and static/source/official-source reconnaissance only.

**Explicitly not authorized:** remote connection, GPU allocation/use, package installation, model or dataset downloads, long smoke tests, training, or benchmark rollout.

**Launch gate:** passed by protocol. The primary source baseline is immutable current-main commit `3f2c29ef7e44b1ddccbcda3b6a63939e53639e9e`, whose official accelerator stack exposes the locked accumulation syntax. GPU execution remains prohibited until explicitly authorized.

**Next trigger (after the above gate is resolved):** the project owner explicitly states: `4090已经开好，可以开始远端阶段`.

**First remote action:** released-checkpoint A1 canary — one task, three episodes, with video and hard-reset semantics. Do not train first.
