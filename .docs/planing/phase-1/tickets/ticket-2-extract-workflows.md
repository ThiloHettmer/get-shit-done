# Ticket 2: Extract Dependency Workflows

**Goal:** Copy the workflows that the core agents depend on to function autonomously.

**Tasks:**

- [ ] Copy `get-shit-done/workflows/execute-plan.md` to `.docs/prototype/workflows/execute-plan.md`
- [ ] Copy `get-shit-done/workflows/plan-phase.md` to `.docs/prototype/workflows/plan-phase.md`
- [ ] Copy `get-shit-done/workflows/verify-phase.md` to `.docs/prototype/workflows/verify-phase.md`

**Acceptance Criteria:**

- All 3 files exist in `.docs/prototype/workflows/`.
- References inside these files are noted for update (Ticket 4 will handle the actual update).

## Detailed Analysis

### 1. Execute Plan Workflow (`execute-plan.md`)

- **Source:** `get-shit-done/workflows/execute-plan.md`
- **Purpose:** Orchestrates the execution of a single `PLAN.md` file. It's the "runtime environment" for the Executor agent.
- **Key Steps:**
  - Init Context (loads state, config).
  - Identify Plan (finds next unexecuted plan).
  - Parse Segments (handles Checkpoints vs. Autonomous).
  - **Spawn Subagent:** Spawns `gsd-executor` (needs update to `gibd-executor`).
  - Verify & Commit (loops through tasks).
  - Create Summary.
- **Adaptation Needs:**
  - Change subagent spawn type from `gsd-executor` to `gibd-executor`.
  - Update paths to point to `.docs/prototype/`.
  - Ensure `init` commands work with the prototype structure (or stub if necessary).

### 2. Plan Phase Workflow (`plan-phase.md`)

- **Source:** `get-shit-done/workflows/plan-phase.md`
- **Purpose:** Manages the entire planning lifecycle: Research -> Plan -> Verify -> Refine.
- **Key Steps:**
  - **Research:** Spawns `gsd-phase-researcher` (needs update to `gibd-phase-researcher`).
  - **Plan:** Spawns `gsd-planner` (needs update to `gibd-planner`).
  - **Verify:** Spawns `gsd-plan-checker` (needs update to `gibd-plan-checker`).
  - **Revision Loop:** If issues found, re-spawns planner/checker (up to 3x).
- **Adaptation Needs:**
  - Update all 3 subagent types (`gsd-*` -> `gibd-*`).
  - Update context loading to look at prototype directories.

### 3. Verify Phase Workflow (`verify-phase.md`)

- **Source:** `get-shit-done/workflows/verify-phase.md`
- **Purpose:** Runs post-execution verification to ensure the Phase Goal was met (not just tasks done).
- **Key Steps:**
  - Establish `must_haves` (from Plan frontmatter or Roadmap).
  - Verify Truths (observable behaviors).
  - Verify Artifacts (existence & substance).
  - Verify Wiring (key links).
  - Generate Report (`VERIFICATION.md`).
- **Adaptation Needs:**
  - This workflow is often executed _by_ a subagent (or assumes it is one).
  - Needs to ensure it uses the `gibd-verifier` logic/patterns.
  - Paths for `gsd-tools` might need adjustment or mocking if excluding the binary.
