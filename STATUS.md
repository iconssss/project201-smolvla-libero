# Status

**Milestone:** PRE-GPU revision audit completed on 2026-09-06 (Asia/Shanghai). Stack pins are frozen in `environment/stack_lock.json`.

**Authorized now:** local repository/documentation work and static/source/official-source reconnaissance only.

**Explicitly not authorized:** remote connection, GPU allocation/use, package installation, model or dataset downloads, long smoke tests, training, or benchmark rollout.

**Open protocol gate:** the exact v0.6.1 source does not expose a gradient-accumulation CLI/config field. Do not lower effective batch 64 or invent an unsupported flag. Owner direction is required before A4.

**Next trigger (after the above gate is resolved):** the project owner explicitly states: `4090已经开好，可以开始远端阶段`.

**First remote action:** released-checkpoint A1 canary — one task, three episodes, with video and hard-reset semantics. Do not train first.
