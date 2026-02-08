# Meta-Shell State Examples

This document defines the exact structure of the state files referenced in the Orchestrator prompt.

## 1. The Context File (`.meta/context.md`)

This file is the **Immutable Source of Truth** for the project. It defines _what_ is being built. The Planner reads this to generate tasks.

**Example Content:**

```markdown
# Project: SuperTasker CLI

## Vision

Build a lightweight CLI for managing tasks, optimized for speed and keyboard-only usage.

## Tech Stack

- Language: Rust
- Database: SQLite
- UI: TUI (Ratatui crate)

## Architecture Constraints

1.  **Zero Config**: Must run out of the box without complex setup.
2.  **Offline First**: No internet dependency required for core functions.
3.  **Command Pattern**: All actions must be accessible via CLI args (e.g. `task add "buy milk"`).

## Current Phase Focus

Phase 1: MVP - Core CRUD operations and basic TUI list view.
```

---

## 2. The Session File (`.meta/session.json`)

This file is the **Mutable Runtime State**. The Host updates this file atomically. It tracks _where_ we are in the process.

**Schema:**

```typescript
interface SessionState {
  sessionId: string;
  status: "planning" | "executing" | "verifying" | "halted";
  currentPhase: number;
  gapCount: number; // For circuit breaker
  plan?: {
    tasks: {
      id: string;
      title: string;
      status: "pending" | "complete" | "failed";
      dependencies: string[];
      commits?: string[]; // Tracked for rollback
    }[];
    currentTaskIdx: number;
  };
  variables: Record<string, any>; // Arbitrary agent memory
}
```

**Example (Runtime Snapshot):**

```json
{
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "executing",
  "currentPhase": 1,
  "gapCount": 0,
  "plan": {
    "currentTaskIdx": 1,
    "tasks": [
      {
        "id": "01",
        "title": "Setup Cargo Project",
        "status": "complete",
        "dependencies": [],
        "commits": ["a1b2c3d"]
      },
      {
        "id": "02",
        "title": "Implement SQLite Schema",
        "status": "pending",
        "dependencies": ["01"],
        "commits": []
      },
      {
        "id": "03",
        "title": "Build TUI List View",
        "status": "pending",
        "dependencies": ["02"]
      }
    ]
  },
  "variables": {
    "last_verification_failed": false
  }
}
```

## How They Are Used

1.  **Host** reads `session.json`.
2.  **Host** constructs the Prompt:
    > "Current State: Phase 1 (Executing Task 02), Context: [Content of context.md]"
3.  **Orchestrator** (LLM) decides:
    > "Ah, Task 01 is done. Task 02 is pending. I will spawn Executor for Task 02."
