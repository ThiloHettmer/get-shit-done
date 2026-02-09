# Ticket 1: Implementation of `gibd-runner.ts` Core

**Goal:** Create the base TypeScript infrastructure for the "Blackbox Runner" that can load and execute isolated agents.

**Tasks:**

- [ ] Create `src/orchestration/gibd-runner.ts`.
- [ ] Implement `Agent` abstract class:
  - Methods: `loadPersona()`, `handleToolCall()`, `execute()`.
- [ ] Implement `BlackboxRunner` registry:
  - Registry to map agent names (e.g., "researcher") to their concrete classes.
- [ ] Implement basic filesystem shell:
  - Methods to read `.planning` files without using `gsd-tools.js`.

**Acceptance Criteria:**

- Runner exists and can be invoked with `ts-node`.
- Can load a markdown file and print its frontmatter.

**Ticket Source:** `.docs/planing/phase-2/tickets/ticket-1-runner-core.md`
