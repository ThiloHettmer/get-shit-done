# Meta-Shell V3.1: User Guide

This guide explains how to use, configure, and extend the Meta-Shell V3.1.

## 1. Quick Start

### The Main Prompt

To run the orchestrator, your Host system should feed the following prompt to the LLM (Orchestrator Agent):

```markdown
You are the Meta-Orchestrator. Your goal is to drive the project to completion.
Use the `spawn_agent` tool to delegate work.
Follow the workflow defined in: orchestrator.md

Current State:

- Phase: 1 (Planning)
- Context: .meta/context.md
- Session: .meta/session.json

Begin by analyzing the state and spawning the Planner if needed.
```

### 2. Workflow Overview

The system follows a strict **Sequential Execution Model**:

1.  **Planning Phase**:
    - The Orchestrator calls `spawn_agent("planner")`.
    - Planner reads `context.md` and outputs a `plan.json` (DAG of tasks).
2.  **Execution Loop**:
    - Orchestrator iterates through `plan.json` tasks.
    - Validate dependencies -> Spawn `executor` -> Handle Result.
    - If `executor` fails -> HALT with Rollback instructions.
3.  **Verification**:
    - Orchestrator calls `spawn_agent("verifier")`.
    - If successful -> Phase Complete.
    - If failed -> Increment Gap Count -> Re-plan.

### 3. Adding New Skills (Subagents)

To add a new capability (e.g., `designer`):

1.  **Create Skill File**: `skills/designer.md`
    - Define Persona ("You are a UI Designer").
    - Define Input/Output Schema (JSON).
2.  **Register in Host**:
    - Ensure your Host runtime maps `agent_name="designer"` to this system prompt.
3.  **Update Orchestrator**:
    - Modify `orchestrator.md` to call `spawn_agent("designer")` where appropriate (e.g., inside the Execution Loop if a task type is "design").

### 4. Configuration

Configuration handles behavior limits and paths.

**File**: `.meta/config.json` (Example)

```json
{
  "max_gap_retries": 2,
  "timeouts": {
    "planner": 300,
    "executor": 600
  },
  "paths": {
    "context": ".meta/context.md",
    "artifacts": ".meta/artifacts/"
  }
}
```

### 5. Runtime Interactions

**Handling Checkpoints**:
If the system halts with `CHECKPOINT REACHED`, the Host will prompt you:

```text
[CHECKPOINT] Decision Required: Which Auth Provider?
Options: [1] Auth0, [2] Supabase
> 1
```

The Host then resumes the Orchestrator with your input injected.

**Handling Failures**:
If the system halts with `TASK FAILED`:

```text
[ERROR] Task 03 Failed.
[ROLLBACK] Run: git revert --no-edit a1b2c3d
```

1. Run the git command.
2. Restart the Orchestrator.
