# Meta-Shell Host Interface (V3: Hardened)

## Overview

The V3 Host Interface defines stricter contracts for operational reliability, specifically handling **timeouts**, **atomic updates**, and **signals**.

## 1. The Host Protocol

### `spawn_agent`

Spawns a specialized sub-agent with strict operational limits.

**Signature**:

```typescript
spawn_agent(
    agent_name: string,
    system_prompt: string,
    user_message: string,
    options: {
        model_hint?: "fast" | "smart",
        timeout_seconds?: number, // e.g. 600 (10 mins)
        max_tokens?: number       // Cost control
    }
) -> Promise<AgentResponse>
```

**Return Type (`AgentResponse`)**:

```typescript
type AgentResponse = {
  status: "success" | "timeout" | "error" | "checkpoint";
  data: string; // The raw output (or error message)
  metadata: {
    tokens_used: number;
    duration_ms: number;
  };
};
```

**Contract**:

- **Timeout**: If the agent exceeds `timeout_seconds`, the Host MUST terminate the process and return `status: "timeout"`.
- **Isolation**: The Host ensures the sub-agent has NO access to the Orchestrator's history.

### `update_state`

Atomically updates the session state.

**Signature**:

```typescript
// Updates a nested key path (e.g., "variables.retry_count")
// Uses a lock file or transactional write to prevent race conditions.
update_state(key: string, value: any) -> Promise<void>
```

### `log_progress`

Writes to a user-visible log stream.

**Signature**:

```typescript
log_progress(message: string, level: "info" | "warn" | "error") -> void
```

---

## 2. Checkpoint Signal Schema

When `spawn_agent` returns `status: "checkpoint"`, the `data` field contains this JSON:

```json
{
  "type": "checkpoint",
  "reason": "decision_required | human_action",
  "message": "Which auth provider?",
  "options": ["Auth0", "Supabase"],
  "resume_id": "step_2_auth_decision" // Optional: ID for resuming
}
```

The Host MUST:

1.  Pause execution.
2.  Display `message` and `options` to the User.
3.  Wait for input.
4.  (On resume) Pass the user input to the _next_ agent spawn.
