# Ticket 1: Extract Core GIBD Agents

**Goal:** Isolate the main agent logic into the prototype directory.

**Tasks:**

- [ ] Copy `agents/gsd-phase-researcher.md` to `.docs/prototype/agents/gibd-phase-researcher.md`
- [ ] Copy `agents/gsd-planner.md` to `.docs/prototype/agents/gibd-planner.md`
- [ ] Copy `agents/gsd-plan-checker.md` to `.docs/prototype/agents/gibd-plan-checker.md`
- [ ] Copy `agents/gsd-executor.md` to `.docs/prototype/agents/gibd-executor.md`
- [ ] Copy `agents/gsd-verifier.md` to `.docs/prototype/agents/gibd-verifier.md`

**Acceptance Criteria:**

- All 5 files exist in the destination.
- Original files are untouched.

## Detailed Analysis

### 1. Phase Researcher (`gibd-phase-researcher`)

- **Source:** `agents/gsd-phase-researcher.md`
- **Role:** Investigates tech stack and patterns before planning.
- **Input:**
  - `PHASE_INFO`: Name, number, goal.
  - `CONTEXT.md`: User constraints (Decisions, Discretion, Deferred).
  - `REQUIREMENTS.md`: Scope.
- **Output:** `[PHASE]-RESEARCH.md` (Structured markdown with stack, patterns, pitfalls).
- **Key Logic:**
  - Queries `Context7` (library IDs) and `WebSearch` (ecosystem).
  - Assigns confidence levels (HIGH/MEDIUM/LOW).
  - **Constraints:** MUST honor locked decisions from `CONTEXT.md`.

### 2. Planner (`gibd-planner`)

- **Source:** `agents/gsd-planner.md`
- **Role:** Decomposes phase into parallel execution plans.
- **Input:**
  - `RESEARCH.md`: Stack/patterns.
  - `CONTEXT.md`: User constraints.
  - `ROADMAP.md`: Phase goal.
  - `STATE.md`: Current project state.
- **Output:** Multiple `[PHASE]-[PLAN]-PLAN.md` files.
- **Key Logic:**
  - **Goal-Backward Analysis:** Derives `must_haves` (Truths -> Artifacts -> Wiring) from Goal.
  - **Wave Assignment:** Creates parallel execution waves based on dependency graph.
  - **Scope Control:** Targets ~50% context usage (~2-3 tasks/plan).

### 3. Plan Checker (`gibd-plan-checker`)

- **Source:** `agents/gsd-plan-checker.md`
- **Role:** Static analysis of plans _before_ execution.
- **Input:** `PLAN.md` contents, `CONTEXT.md`, `ROADMAP.md`.
- **Output:** Structured Issues List (YAML).
- **Key Logic:**
  - **Dimension Check:** Requirement Coverage, Task Completeness, Dependency Correctness, Key Links, Scope Sanity.
  - **Context Compliance:** flags if plan contradicts locked decisions.
  - **Verification Derivation:** Checks if `must_haves` are user-observable.

### 4. Executor (`gibd-executor`)

- **Source:** `agents/gsd-executor.md`
- **Role:** Executes a single plan file.
- **Input:** `PLAN.md`, `STATE.md`, `CONTEXT.md`.
- **Output:**
  - `SUMMARY.md` (Execution report).
  - Git Commits (Atomic per task).
- **Key Logic:**
  - **Atomic Execution:** Loop: Task -> Execute -> Verify -> Commit.
  - **Deviation Handling:** Auto-fix bugs; STOP for architectural changes (Rule 4).
  - **Checkpoints:** Pauses for human verification/decision.

### 5. Verifier (`gibd-verifier`)

- **Source:** `agents/gsd-verifier.md`
- **Role:** Verifies _codebase_ against goal (post-execution).
- **Input:** `PLAN.md`, `SUMMARY.md`, `CODEBASE` (actual files).
- **Output:** `VERIFICATION.md` (passed/gaps/human_needed).
- **Key Logic:**
  - **Three-Level Check:** Artifact Exists? Substantive? Wired?
  - **Key Links:** Verifies critical connections (e.g., Component -> API).
  - **Anti-Patterns:** Scans for stubs/TODOs.
