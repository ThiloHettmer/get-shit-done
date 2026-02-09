# GIBD Phase Planning Process

This document defines the standard workflow for converting a high-level Phase Plan into detailed, research-backed execution tickets. Use this process when instructed to "plan" or "detail" a specific phase.

## Prerequisites

- A high-level plan for the phase exists (e.g., `phase-2/blackbox_plan.md`).
- The Phase ID is known (e.g., "Phase 2").

## Workflow Steps

### 1. Structure Initialization

1.  **Create Directory:** Ensure `.docs/planing/phase-[N]/tickets/` exists.
2.  **Read Context:** Read the high-level phase plan file to understand the scope and objectives.
3.  **Draft Stubs:** Create initial markdown files for each distinct task/component in the phase (e.g., `ticket-1-task-name.md`).

### 2. Deep Research (The "Get Shit Done" Loop)

Perform this step for _each_ ticket stub. Do not assume; verify.

1.  **Identify Targets:** List the concepts, files, or agents mentioned in the ticket.
2.  **Locate Source of Truth:**
    - Use `find_by_name` to locate relevant files in the `get-shit-done` codebase.
    - Use `grep_search` to find usages and references.
3.  **Analyze Logic:**
    - Use `view_file` to read the actual content of the source files.
    - Identify:
      - **Inputs/Outputs:** What does this component consume and produce?
      - **Dependencies:** What other files/workflows does it need?
      - **Adaptation Needs:** What specific changes are required to move it to the GIBD prototype (e.g., renaming, path updates)?

### 3. Ticket Refinement (The Output)

Rewrite each ticket stub with the gathered intelligence. Structuring the ticket this way ensures the Executor Agent has everything they need.

**Ticket Template:**

```markdown
# Ticket [N]: [Title]

**Goal:** [Clear, single-sentence objective]

**Tasks:**

- [ ] [Specific Action 1]
- [ ] [Specific Action 2]
      ...

**Acceptance Criteria:**

- [Condition 1]
- [Condition 2]

## Detailed Analysis

[Summary of research findings]

### [Component Name]

- **Source:** `[Path found during research]`
- **Purpose:** `[Summary of role]`
- **Adaptation Strategy:**
  - [Specific instruction, e.g., "Rename X to Y"]
  - [Specific context, e.g., "Update imports to point to .docs/prototype"]
```

### 4. Holistic Review

1.  **Coverage Check:** Do the detailed tickets collectively achieve _all_ goals in the high-level phase plan?
2.  **Independence Check:** Can Ticket N be executed without blocked dependencies from Ticket N+1? (Order matters).
3.  **Instruction Quality:** Are the instructions specific enough that an agent without prior context could execute them?

## Execution

Once this process is complete for a phase, the user can simple say "Execute Ticket 1 of Phase X", and the agent will have a comprehensive blueprint to follow.
