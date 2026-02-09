# Phase 5: Full Orchestration (LangGraph)

**Goal:** Implement the execution loop to connect the GIBD agents using a state graph.

## 1. The State Graph (`GSDState`)

Define the shared state passed between nodes in the graph.

- **Project Root:** Base path.
- **Active Phase:** ID of the phase being worked on.
- **Artifacts:** Content of relevant markdown files.
- **Planning State:** Status, list of plan IDs, validation issues.
- **Execution State:** Wave status, completed plans, deviations.

## 2. The Nodes

Each GIBD runner from Phase 2 becomes a node in the graph.

- `research_node`: Calls `hydrateAndRunResearcher`.
- `plan_node`: Calls `hydrateAndRunPlanner`.
- `check_plan_node`: Calls `hydrateAndRunPlanChecker`.
- `execute_node`: Calls `hydrateAndRunExecutor`.
- `verify_node`: Calls `hydrateAndRunVerifier`.

## 3. The Edges (Transitions)

Define the logic for moving between nodes.

- **Start** -> `research_node`
- `research_node` -> `plan_node`
- `plan_node` -> `check_plan_node`
- `check_plan_node`:
  - If **Issues Found** -> `plan_node` (Revision Mode).
  - If **Passed** -> `execute_node`.
- `execute_node` -> `verify_node`
- `verify_node`:
  - If **Passed** -> **End** (Phase Complete).
  - If **Gaps Found** -> `plan_node` (Gap Closure Mode).

## 4. Human-in-the-Loop

Implement breakpoints for user decisions.

- **Planning Approval:** Before executing plans.
- **Checkpoint Handling:** Pause execution if Executor hits a checkpoint.
- **Deviation Review:** If Executor proposes architectural changes.

## 5. Entry Point (`gibd-cli`)

Create a simple CLI to start the graph.

- `gibd start [phase-id]`
