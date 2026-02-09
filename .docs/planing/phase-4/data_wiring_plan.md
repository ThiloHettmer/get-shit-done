# Phase 4: Data Wiring & State Hydration

**Goal:** Implement the logic to feed real filesystem data into the Blackbox Runners (Phase 2), replacing the mock inputs with actual project state.

## 1. State Hydration Strategy

The blackbox runners expect structured inputs (e.g., `ResearcherInput`, `PlannerInput`). We need adapters to read the filesystem and construct these objects.

### A. Context Loader (`loadProjectContext`)

- **Source:** `.planning/` directory.
- **Responsibility:** Read `PROJECT.md`, `ROADMAP.md`, `STATE.md`.
- **Transformation:**
  - Parse markdown into JSON/objects.
  - Extract "Locked Decisions" from `CONTEXT.md`.
  - Extract "Phase Goal" from `ROADMAP.md`.

### B. Phase Loader (`loadPhaseContext`)

- **Source:** `.planning/phases/{phase_id}/` (or similar structure).
- **Responsibility:**
  - Identify current phase state.
  - Load existing `RESEARCH.md` if available.
  - Load existing `PLAN.md` files for the Planner/Checker.

### C. File System Adapter

- **Role:** Provide a safe interface for agents to read/write files.
- **Mechanism:**
  - `readFile(path)`: Returns content (simulating `read_resource`).
  - `writeFile(path, content)`: Writes to disk (simulating `write_resource`).
  - **Constraint:** Sandboxed to the project root.

## 2. Wiring the Runners

Connect the data loaders to the runners defined in Phase 2.

### `hydrateAndRunResearcher(phaseId)`

1.  Call `loadProjectContext()` to get roadmap/constraints.
2.  Construct `ResearcherInput`.
3.  Call `runGIBDResearcher(input)`.
4.  Save output to `.planning/phases/{phaseId}/RESEARCH.md`.

### `hydrateAndRunPlanner(phaseId)`

1.  Call `loadPhaseContext(phaseId)` to get Research/Roadmap.
2.  Construct `PlannerInput`.
3.  Call `runGIBDPlanner(input)`.
4.  Save outputs to `.planning/phases/{phaseId}/{planId}-PLAN.md`.

## 3. Tooling Integration

Ensure the runners uses the GSD standard tools (Context7, WebSearch, etc.) correctly via the new adapter layer, rather than hardcoded CLI calls.
