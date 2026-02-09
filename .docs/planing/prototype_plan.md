# Phase 1: Recursive Migration & Isolation

**Goal:** Physically copy the agent logic AND all referenced artifacts (workflows, templates) from the original directory to `.docs/prototype/` and rename them to the GIBD namespace.

### 1. Agent Migration (Core Personas)

- **Source:** `agents/*`
- [ ] Copy `gsd-phase-researcher.md` -> `gibd-phase-researcher.md`
- [ ] Copy `gsd-planner.md` -> `gibd-planner.md`
- [ ] Copy `gsd-plan-checker.md` -> `gibd-plan-checker.md`
- [ ] Copy `gsd-executor.md` -> `gibd-executor.md`
- [ ] Copy `gsd-verifier.md` -> `gibd-verifier.md`

### 2. Dependency Extraction (Validation & Templates)

The agents reference external files (e.g., `<execution_context> @~/.claude/get-shit-done/workflows/execute-plan.md`). These must be copied and the agents updated to point to the new local copies.

#### Workflows (`.docs/prototype/workflows/`)

- [ ] `execute-plan.md` (referenced by Executor)
- [ ] `plan-phase.md` (referenced by Planner)
- [ ] `verify-phase.md` (referenced by Verifier)

#### Templates (`.docs/prototype/templates/`)

- [ ] `summary.md` (referenced by Executor for `SUMMARY.md` creation)
- [ ] `verification.md` (referenced by Verifier for `VERIFICATION.md` creation)

#### Step 3: Reference Rewriting

- [ ] **Planner (`gibd-planner.md`)**: Update `@~/.claude/...` references to point to `.docs/prototype/...`
- [ ] **Executor (`gibd-executor.md`)**: Update `@~/.claude/get-shit-done/workflows/execute-plan.md` to `.docs/prototype/workflows/execute-plan.md`
- [ ] **Verifier (`gibd-verifier.md`)**: Update template references.
