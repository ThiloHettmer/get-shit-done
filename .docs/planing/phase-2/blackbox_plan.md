# Prototype Development Plan: GIBD Blackbox Runner (Orchestrator Lite)

This plan details the creation of a TypeScript runner (`gibd-runner.ts`) that invokes isolated agents with their local dependencies. This runner will replace the complex `gsd-tools.js` logic for this prototype, focusing on defining agent inputs, outputs, and internal blackbox logic.

## Phase 2: Blackbox Runner (The "Orchestrator Lite")

**Goal:** Create a TypeScript runner (`gibd-runner.ts`) that invokes these _isolated_ agents with their new local dependencies. This replaces the complex `gsd-tools.js` logic for this prototype.

### 1. Phase Researcher (`gibd-phase-researcher`)

- **Role:** Investigates tech stack and patterns before planning.
- **Dependencies:** None (starts the phase).
- **Inputs (Context Injection):**
  - `PHASE_INFO`: Name, number, goal.
  - `CONTEXT.md`: User constraints (Locked Decisions, Discretion, Deferred).
  - `REQUIREMENTS.md`: Scope of work.
- **Internal Logic:**
  - Queries `Context7`/`WebSearch` for stack validation.
  - Generates confidence levels for technical choices.
- **Output:** `[PHASE]-RESEARCH.md`.

### 2. Planner (`gibd-planner`)

- **Role:** Decomposes phase into parallel execution plans.
- **Dependencies:** Research, Roadmap.
- **Inputs:**
  - `RESEARCH.md`: stack/patterns from Step 1.
  - `CONTEXT.md`: User constraints (CRITICAL: cannot violate these).
  - `ROADMAP.md`: The Phase Goal.
  - `STATE.md`: Current project state (to know what exists).
- **Internal Logic:**
  - "Goal-Backward" analysis (derive `must_haves` from goal).
  - Dependency graph creation (Classes/Model -> API -> UI).
  - Wave assignment for parallel execution.
- **Output:** Multiple `[PHASE]-[PLAN]-PLAN.md` files.

### 3. Plan Checker (`gibd-plan-checker`)

- **Role:** Static analysis of the plans before execution.
- **Dependencies:** Generated Plans.
- **Inputs:**
  - `PLAN.md` contents.
  - `CONTEXT.md`: Check compliance with user decisions.
  - `ROADMAP.md`: Verify goal achievement.
- **Internal Logic:**
  - Verifies "Goal-Backward" completeness (do tasks actually achieve the goal?).
  - Checks for "Context Compliance" (did we ignore a user decision?).
  - Checks scope budget (files/tasks per plan).
- **Output:** Structured Issues List (YAML).

### 4. Executor (`gibd-executor`)

- **Role:** Executes a single plan file.
- **Dependencies:** A validated Plan.
- **Inputs:**
  - `PLAN.md`: The specific plan to run.
  - `STATE.md`: Global state.
  - `CONTEXT.md`: User vision (fallback reference).
- **Internal Logic:**
  - **Atomic Execution**: Loop through tasks -> Execute -> Verify -> Commit.
  - **Deviation Handling**: Auto-fix bugs/missing files; Stop for architectural changes.
  - **Checkpoints**: Pause execution if human verification needed.
- **Output:**
  - `SUMMARY.md`: Execution report.
  - Git Commits.

### 5. Phase Verifier (`gibd-verifier`)

- **Role:** Verifies the _codebase_ against the goal (not just the plans).
- **Dependencies:** Completed execution (Summary + Code).
- **Inputs:**
  - `PLAN.md`: What was intended.
  - `SUMMARY.md`: What was claimed done.
  - `CODEBASE`: The actual files.
- **Internal Logic:**
  - **Three-Level Check**:
    1.  Artifact Exists?
    2.  Artifact Substantive? (not a stub)
    3.  Artifact Wired? (imported and used)
  - **Gap Analysis**: Compare actual code vs `must_haves`.
- **Output:** `VERIFICATION.md` (passed/failed/gaps).

## Phase 4: Data Wiring (Deferred)

Logic to feed real filesystem data into the Step 2 runners.

## Phase 5: Full Orchestration (Deferred)

LangGraph implementation.
