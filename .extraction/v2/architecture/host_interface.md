# Meta-Shell Host Interface (V2)

## Overview

The Meta-Shell assumes it is running on a "Host" — a runtime environment capable of LLM inference, file I/O, and tool execution. Ideally, this Host is also an Agent, but it can be a simple script.

## 1. The Host Protocol

The Host MUST provide the following tools to the Orchestrator.

### `spawn_agent`

Spawns a specialized sub-agent with a fresh context window.

**Signature**:

```typescript
spawn_agent(
    agent_name: string,      // e.g., "planner", "executor"
    system_prompt: string,   // The full persona definition
    user_message: string,    // The specific task input
    model_hint?: string      // "fast" | "smart" (optional)
) -> Promise<string>         // Returns the raw string response
```

**Contract**:

- The Host ensures the sub-agent has NO access to the Orchestrator's history (Fresh Context).
- The Host handles API errors/retries internally.
- The returned string is the raw output (which the Orchestrator handles parsing).

### `read_file` / `write_file`

Standard file operations.

### `read_state` / `update_state`

Atomic operations for the `.meta/session.json` state file.

**Signature**:

```typescript
read_state(key?: string) -> Promise<any>
update_state(key: string, value: any) -> Promise<void>
```

---

## 2. Data Schemas (JSON)

### Plan Artifact (`plan.json`)

Produced by: **Planner**
Consumed by: **Orchestrator**, **Executor**

```json
{
  "phase_id": "01",
  "objective": "Implement User Auth",
  "tasks": [
    {
      "id": "01-01",
      "title": "Create Auth Helper",
      "description": "Implement JWT signing...",
      "files": ["src/auth.ts"],
      "verification_cmd": "npm test tests/auth.test.ts",
      "dependencies": []
    },
    {
      "id": "01-02",
      "title": "Create Login Route",
      "dependencies": ["01-01"]
    }
  ],
  "must_haves": [
    { "truth": "User can login", "evidence_required": "200 OK from /login" }
  ]
}
```

### Execution Summary (`summary.json`)

Produced by: **Executor**
Consumed by: **Orchestrator**, **Verifier**

```json
{
  "task_id": "01-01",
  "status": "complete", // or "blocked", "failed"
  "changes": [{ "file": "src/auth.ts", "action": "created" }],
  "verification_result": {
    "command": "npm test tests/auth.test.ts",
    "output": "PASS",
    "success": true
  },
  "notes": "Used 'jose' library instead of jsonwebtoken per constraints."
}
```

### Checkpoint Signal (`checkpoint.json`)

Produced by: **Executor** (via `status` field) or **Orchestrator**
Consumed by: **Host** (to pause execution)

```json
{
  "type": "checkpoint",
  "reason": "decision_required",
  "message": "Which auth provider?",
  "options": ["Auth0", "Supabase", "Firebase"]
}
```

### Session State (`.meta/session.json`)

Managed by: **Orchestrator**

```json
{
  "session_id": "uuid",
  "current_phase": "01",
  "current_task_idx": 0,
  "status": "executing",
  "retry_count": 0,
  "variables": {
    "research_done": true,
    "last_error": null
  }
}
```
