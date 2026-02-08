# GSD-Lite: Unified Task Workflow

## Problem

The current workflow involves too many transitions (`Discuss` -> `Plan` -> `Execute` -> `Verify`), causing local LLMs to lose state and context.

## Proposed Solution: `gsd:task`

A consolidated command for "Plan & Execute" in one flow.

### Command Definition: `commands/gsd/task.md`

- **Context**: Loads `.planning/CONTEXT_LITE.md` and `.planning/task.md`.
- **Prompt**:
  1.  **Read**: Get the top item from `task.md`.
  2.  **Plan**: Formulate a quick plan (scratchpad) in the conversation.
  3.  **Execute**: Perform the necessary code changes.
  4.  **Verify**: Run verification commands immediately.
  5.  **Update**: Mark the task as done in `task.md`.
- **Benefit**: Reduces context switching and "hand-offs" between agents, keeping the model focused on the immediate objective.
