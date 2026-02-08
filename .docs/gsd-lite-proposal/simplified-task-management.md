# GSD-Lite: Simplified Task Management

## Problem

Local LLMs struggle with maintaining complex nested markdown lists in `task.md`, often breaking formatting or losing track of items.

## Proposed Solution

Flatten the hierarchy and use a stricter, simpler format.

### Modified `task.md` Structure

- **Format**: A flat list with explicit status tags.
- **Example**:
  ```markdown
  - [ ] Task 1: Description @status:todo
  - [ ] Task 2: Description @status:pending
  - [x] Task 3: Description @status:done
  ```

### Enforcement

- **Sanitization**: Use a `hooks/post_command` script to check and fix `task.md` formatting if the LLM makes errors.
- **CLI Helper**: Optionally provide a helper script (e.g., `gsd-task-add`, `gsd-task-done`) to manage the file programmatically, removing the burden from the LLM.
