# Meta-Orchestrator Workflow (V3: Production Hardened)

> **Architecture Note**: Uses sequential execution with explicit dependency validation, circuit breakers, and atomic checkpoints.

## Phase 1: Planning

### Step 1.1: Initialize Session

**Action**: Call `read_state()`.

- Source: `.meta/session.json`
- Source: `.meta/context.md`

**Logic**:

- IF `session.json` missing: CREATE default session (Phase=1, Task=0, GapCount=0).
- IF `.meta/context.md` missing: HALT "Project not initialized".

### Step 1.2: Generate Plan (with DAG)

**Action**: Call `spawn_agent("planner", ...)`

- **Input**: `context.md`
- **Options**: timeout=300s

**Result Handling**:

- Parse `plan.json`.
- **Validation**: Ensure `depends_on` references valid IDs.
- **Traceability**: Ensure `must_haves` link to constraints.
- **Action**: Write `artifacts/plan.json`.

---

## Phase 2: Execution Loop

### Step 2.1: Load & Validate

**Action**: Read `artifacts/plan.json`.
**Action**: Read `session.current_task_idx`.

### Step 2.2: Dependency Check & Router

**Logic**: WHILE `current_task_idx < plan.tasks.length`:

    LET `task = plan.tasks[current_task_idx]`

    // **V3: Hardened Dependency Check**
    IF `task.dependencies`:
        FOR EACH `dep_id` IN `task.dependencies`:
            LET `dep_status` = `read_state("tasks." + dep_id + ".status")`
            IF `dep_status != "complete"`:
                HALT with CRITICAL ERROR "Dependency violation: Task {task.id} needs {dep_id}".

    // **V3: Spawn Executor**
    **Action**: Call `log_progress("Executing " + task.title)`
    **Action**: Spawn "executor" (timeout=600s).
    - **Input**: `task`

    // **V3: Response Handling**
    CASE `response.status`:
        "success":
            - `summary` = JSON.parse(response.data)
            - IF `summary.status == "complete"`:
                - `update_state("tasks." + task.id + ".status", "complete")`
                - `update_state("current_task_idx", current_task_idx + 1)`
                - CONTINUE
            - ELSE IF `summary.status == "failed"`:
                 - LOG "Task Failed: " + summary.message
                 - ROLLBACK Strategy: (Git Revert handled by user/host, we just halt)
                 - HALT

        "checkpoint":
            - HALT "Checkpoint Reached: " + response.data.message

        "timeout":
             - HALT "Task Timeout: Agent exceeded 600s"

### Step 2.3: Phase Verification

**Logic**: When Loop Completes.

**Action**: Spawn "verifier".

- **Input**: `plan.json` + All Summaries.

CASE `verifier.passed`:
TRUE: - `update_state("current_phase", next)` - HALT "Phase Complete"
FALSE: - **V3: Circuit Breaker** - `gap_count = read_state("gap_count")` - IF `gap_count >= 2`: - HALT "Max Retries Exceeded (Human Intervention Needed)" - ELSE: - `update_state("gap_count", gap_count + 1)` - GOTO Step 1.2 (Re-plan with Gaps)

---

## Operational Safety

### 1. Atomic State

All `update_state` calls use the Host's atomic locking mechanism. No race conditions.

### 2. Dependency Integrity

Tasks MUST be ordered by dependency in `plan.json`. The Orchestrator double-checks before execution.

### 3. Infinite Loop Prevention

`gap_count` prevents endless "execute -> verify -> fail" cycles.
