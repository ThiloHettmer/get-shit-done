# Meta-Shell Host Interface (V3.1: Hardened)

## Overview

The V3.1 Host Interface defines strict contracts for operational reliability, handling **timeouts**, **atomic updates** with dead-lock prevention, and **checkpoint resumption**.

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
        timeout_seconds?: number, // e.g. 600
        max_tokens?: number,
        resume_data?: {           // V3.1: Explicit resume context
            checkpoint_id: string,
            user_input: any
        }
    }
) -> Promise<AgentResponse>
```

**Return Type (`AgentResponse`)**:

```typescript
type AgentResponse = {
  status: "success" | "timeout" | "error" | "checkpoint";
  data: string; // The raw output
  metadata: {
    tokens_used: number;
    duration_ms: number;
  };
};
```

**Contract**:

- **Timeout**: If execution exceeds `timeout_seconds`, the Host MUST terminate the process, CLEAN UP partial writes (if possible), and return `status: "timeout"`.
- **Resume**: If `resume_data` is provided, it is injected into the agent's context (e.g., "User replied: Use Auth0").

### `update_state`

Atomically updates the session state.

**Signature**:

```typescript
// V3.1: Added lock_timeout_ms to prevent deadlocks
update_state(
    key: string,
    value: any,
    lock_timeout_ms: number = 5000
) -> Promise<void>
```

**Contract**:

- Must acquire a lock before writing.
- If lock cannot be acquired within `lock_timeout_ms`, throw an Error (do not hang indefinitely).

### `log_progress`

Writes to a user-visible log stream.

```typescript
log_progress(message: string, level: "info" | "warn" | "error") -> void
```

---

## 2. Checkpoint Signal Schema

When `spawn_agent` returns `status: "checkpoint"`, the `data` field contains:

```json
{
  "type": "checkpoint",
  "reason": "decision_required | human_action",
  "message": "Which auth provider?",
  "options": ["Auth0", "Supabase"],
  "resume_id": "step_2_auth_decision"
}
```

The Host MUST:

1.  Pause execution.
2.  Display `message` and `options` to the User.
3.  Wait for input.
4.  (On resume) Check for `resume_id` and pass input to `spawn_agent` via `resume_data`.
