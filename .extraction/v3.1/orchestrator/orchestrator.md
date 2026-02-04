# Meta-Orchestrator Workflow (V3.1: Production Hardened)

> **Architecture Note**: Sequential execution, atomic checkpoints, deadlock prevention.

## Phase 1: Planning

### Step 1.1: Initialize

**Action**: Call `read_state()`.

- IF `session.json` missing: CREATE default (Phase=1, Task=0, GapCount=0).

### Step 1.2: Generate Plan (with DAG)

**Action**: Call `spawn_agent("planner", ...)` (timeout=300s).

**Result Handling**:

- Parse `plan.json`.
- **V3.1 Topology Check**: Iterate tasks. IF `task[i]` depends on `task[j]` AND `j >= i`, HALT "Invalid Topology: Task {i} depends on future task {j}".
- **V3.1 Budget Warning**: IF `task.files.length > 3`, LOG WARN "Task {id} exceeds context budget".
- **Action**: Write `artifacts/plan.json`.

---

## Phase 2: Execution Loop

### Step 2.1: Load & Validate

**Action**: Read `artifacts/plan.json`.

### Step 2.2: Execution Router

**Logic**: WHILE `current_task_idx < plan.tasks.length`:

    LET `task = plan.tasks[current_task_idx]`

    // **Dependency Check**
    IF `task.dependencies`:
        FOR EACH `dep_id`: IF `read_state(dep_id).status != "complete"`: HALT "Dependency violation".

    // **Spawn Executor**
    **Action**: `log_progress("Executing " + task.title)`
    **Action**: Spawn "executor" (timeout=600s).

    // **Response Handling**
    CASE `response.status`:
        "success":
            - `summary` = JSON.parse(response.data)
            - IF `summary.status == "complete"`:
                - `update_state(..., lock_timeout=5000)`
                - CONTINUE
            - ELSE IF `summary.status == "failed"`:
                 - LOG ERROR "Task Failed: " + summary.message
                 - **V3.1 Rollback Log**: IF `summary.commits`:
                     - LOG INFO "To Rollback, Run: git revert --no-edit " + summary.commits.join(" ")
                 - HALT

        "checkpoint":
            - HALT "Checkpoint Reached: " + response.data.message

        "timeout":
             - HALT "Task Timeout: Agent exceeded 600s"

### Step 2.3: Phase Verification

**Logic**: When Loop Completes.

**Action**: Spawn "verifier".

CASE `verifier.passed`:
TRUE: HALT "Phase Complete"
FALSE: - `gap_count = read_state("gap_count")` - IF `gap_count >= 2`: HALT "Max Retries Exceeded" - ELSE: `update_state("gap_count", gap_count + 1)`; GOTO Step 1.2

---

## Operational Safety

1.  **Atomic State**: Uses `lock_timeout=5000` to prevent deadlocks.
2.  **Topology Validated**: Plan structure checked before execution.
3.  **Rollback Visibility**: Explicit git commands logged on failure.
