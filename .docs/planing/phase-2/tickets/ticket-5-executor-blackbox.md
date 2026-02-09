# Ticket 5: Research & Implementation of Executor Blackbox

**Goal:** Implement the `gibd-executor` as an atomic task runner.

## Research: Data & State Requirements

| Source          | Data Item       | Injection Mode                        |
| --------------- | --------------- | ------------------------------------- |
| `*-PLAN.md`     | Single Plan     | `<active_plan>` XML block             |
| `STATE.md`      | Global progress | `<project_state>` XML block           |
| `CONTEXT.md`    | Vision Fallback | `<user_vision>` XML block             |
| `workflows/...` | Logic files     | Injected as `@` references in persona |

**Tasks:**

- [ ] Create `src/orchestration/agents/executor.ts`.
- [ ] Implement `AtomicExecutionLoop`:
  - For each task in plan:
    - Invoke LLM.
    - Execute reported tool calls (Bash/Write/Git).
    - Commit changed files.
- [ ] Implement `CheckpointHandler`:
  - Detect `type="checkpoint"` in plan or agent output.
  - Halt and return structured state for human interaction.
- [ ] Implement `SummaryGenerator`: parses the final `<summary>` block and writes `SUMMARY.md`.

**Acceptance Criteria:**

- Runner can execute a single `PLAN.md` file.
- Creates individual git commits per task.
- Generates `SUMMARY.md`.
