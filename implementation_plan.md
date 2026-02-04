# Implementation Plan: Orchestration Redesign (V3: Production Hardened)

## Goal
Harden the V2 architecture to be **production-ready** by addressing rollback, race conditions, dependencies, and timeouts.
This V3 design merges the **clean sequential architecture of V2** with the **operational robustness of the original GSD executor**.

## User Review Required
> [!CRITICAL]
> **No Magic Rollback**: We rely on **Atomic Git Commits** per task. If a task fails, we revert via Git.
> **Explicit Dependencies**: The Orchestrator will now VALIDATE `depends_on` before spawning an agent.
> **Host Responsibility**: The Host handles timeouts (e.g., SIGKILL after 10m) and "Stop-and-Return" resumption.

## Proposed Changes

### 1. Robust Host Interface (`host_interface.md`) 
- **`spawn_agent`**: Add `timeout_seconds` and `max_tokens` to arguments.
- **`checkpoint`**: Formalize the Return Object schema.
- **State**: Define `update_state(key, value, atomic=true)`.

### 2. Hardened Orchestrator (`orchestrator.md`)
- **Dependency Graph**: Sort tasks topologically *or* check `dependencies` array before `spawn_agent`.
- **Circuit Breaker**: `gap_plan_count` variable in state. Max 2 iterations.
- **Progress Tracking**: Write to `.meta/progress.log` for user visibility.

### 3. Operational Skills (`skills/*.md`)
- **Executor**: 
    - **Atomic Commits**: STRICT rule to `git commit` after every atomic sub-task.
    - **Self-Correction**: Try/Catch blocks within the agent's logic (e.g., if test fails, fix it).
- **Planner**: 
    - **DAG Output**: Explicit `depends_on` array in JSON tasks.
    - **Context Budget**: Heuristic "Max 3 files per task".

## Verification Plan
- **Analysis**: Verify that the new `orchestrator.md` handles the "Partial Failure" scenario (Executor crashes half-way).
- **Proof**: Show that the Git Commit strategy allows clean recovery.
