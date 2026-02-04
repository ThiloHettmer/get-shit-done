# Meta-Orchestrator Workflow (V2: Sequential/JSON)

> **Architecture Note**: This workflow assumes a strictly sequential execution model. It manages state via strict JSON schemas and handles errors explicitly.

## Phase 1: Planning

### Step 1.1: Initialize Session

**Action**: Call `read_state()`.

- Source: `.meta/session.json`
- Source: `.meta/context.md` (Project Vision)

**Logic**:

- IF `session.json` missing: CREATE default session structure (Phase=1, Task=0).
- IF `.meta/context.md` missing: HALT with error "Project not initialized".

### Step 1.2: Research Check

**Logic**:

- IF `session.variables.research_done != true`:
  - **Action**: Call `spawn_agent("researcher", research_prompt, "Research objectives")`.
  - **Result**: Parse JSON response. Write to `artifacts/research.json`.
  - **Action**: Call `update_state("variables.research_done", true)`.

### Step 1.3: Generate Plan

**Action**: Call `spawn_agent("planner")`.

- **Input**: `context.md` + `research.json` (if exists).
- **System Prompt**: `skills/planner.md` (Enforcing JSON output).

**Result Handling**:

- Parse result as `plan.json`.
- Validate against JSON Schema.
- IF Invalid: Retry (Max 3).
- **Action**: Write `artifacts/plan.json`.

---

## Phase 2: Execution Loop

### Step 2.1: Load Plan

**Action**: Read `artifacts/plan.json`.
**Action**: Read `session.current_task_idx`.

### Step 2.2: Task Execution Router

**Logic**: WHILE `current_task_idx < plan.tasks.length`:

    LET `task = plan.tasks[current_task_idx]`

    **Action**: Spawn Executor logic.
    - **Skill**: `skills/executor.md`
    - **Input**: `task` (JSON object)

    **Spawn Interaction**:
    - **Call**: `spawn_agent("executor", executor_skill, JSON.stringify(task))`
    - **Return**: `artifacts/summary_{task.id}.json`

    **Result Handling**:
    - IF `summary.status == "complete"`:
        - **Action**: `update_state("current_task_idx", current_task_idx + 1)`
        - CONTINUE Loop.

    - IF `summary.status == "checkpoint"`:
        - **Action**: HALT Orchestrator.
        - **Reason**: `checkpoint_required`
        - **Message**: `summary.message`
        - (Host must pause here and wait for User Input).

    - IF `summary.status == "failed"`:
         - IF `task.retry_count < 3`:
             - RETRY task.
         - ELSE:
             - HALT with "Task Failed".

### Step 2.3: Phase Verification

**Logic**: When Loop Completes (All tasks done).

**Action**: Call `spawn_agent("verifier")`.

- **Input**: `plan.json` + `summary_*.json` (All summaries).
- **Output**: `artifacts/verification.json`.

**Logic**:

- IF `verification.passed == true`:
  - **Action**: `update_state("current_phase", next_phase)`.
  - HALT with "Phase Complete".
- ELSE:
  - **Action**: Generate Gap Plan (Go back to Step 1.3 with specific Gaps).

---

## Error Handling Strategies

### 1. JSON Parsing Errors

- **Try**: Parse Agent Output.
- **Catch**: If JSON invalid, Spawn "Fixer Agent" to repair JSON structure (1 attempt).
- **Fail**: If still invalid, HALT.

### 2. Context Limits

- **Strategy**: Pass ONLY the specific task JSON to the Executor, not the whole Plan.
- **Strategy**: Pass ONLY the relevant file summaries, not full trees.
