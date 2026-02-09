# Prototype Development Plan: GIBD Agent Extraction (Blackbox Isolation)

This plan prioritizes the **extraction and isolation of agents** into a new system called **GIBD (Get It Better Done)**. The goal is to copy not just the agent personas but **all their dependencies (workflows, templates)** into the prototype directory to create truly independent "blackboxes" that do not rely on the original codebase.

## Phase 1: Recursive Migration & Isolation

**Goal:** Physically copy the agent logic AND all referenced artifacts (workflows, templates) from the original directory to `.docs/prototype/` and rename them to the GIBD namespace.

### 1. Agent Migration (Core Personas)

- **Source:** `agents/*`
- **Destination:** `.docs/prototype/agents/`
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

## Phase 3: Validation Checklist

**Goal:** Verify that the extracted agents are truly "blackbox" and independent.

- [ ] **Dependency Check:** Grep for `@~/.claude` in `.docs/prototype/` to ensure no external references remain.
- [ ] **Template Check:** Verify that `gibd-executor.md` and `gibd-verifier.md` point to the local `templates/`.
- [ ] **Workflow Check:** Verify that `gibd-planner.md` and `gibd-executor.md` point to the local `workflows/`.
- [ ] **Input/Output Contract:** Verify that each `gibd-*.md` file clearly defines its expected inputs and outputs in the `<role>` or `<input_format>` sections.

## Phase 4: Data Wiring (Deferred)

Logic to feed real filesystem data into the Step 2 runners.

## Phase 5: Full Orchestration (Deferred)

LangGraph implementation.
