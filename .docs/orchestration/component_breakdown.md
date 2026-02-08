# Component Breakdown and Orchestration Data Structures

## 1. System Overview

The GSD framework decomposes complex software tasks into three distinct phases: **Planning**, **Execution**, and **Verification**. 
To orchestrate this externally (e.g., via LangGraph), we treat each agent as a functional "black box" with defined inputs (State) and outputs (Artifacts).

The primary state carrier is the **Project Context**, which is aggregated by `gsd-tools.js` and passed to agents.

---

## 2. Autonomous Components

### A. Phase Researcher (`gsd-phase-researcher`)
**Goal:** Gather sufficient context to allow the Planner to create actionable tasks without hallucinating.

- **Trigger:** Start of a new phase (or `--research` flag).
- **Input Data (JSON):**
  ```json
  {
    "phase_number": "01",
    "phase_name": "foundation",
    "requirements": "Content of REQUIREMENTS.md",
    "roadmap_context": "Phase section from ROADMAP.md",
    "user_decisions": "Content of CONTEXT.md (if exists)",
    "current_state": "Snapshot of STATE.md"
  }
  ```
- **Output:** `[PHASE]-RESEARCH.md`
- **Orchestration Logic:**
  - If `RESEARCH.md` exists, skip (unless forced).
  - If output contains `## RESEARCH BLOCKED`, halt and ask user.

### B. Planner (`gsd-planner`)
**Goal:** Decompose the Phase Goal into a series of executable `PLAN.md` files with dependency management.

- **Trigger:** After research is complete.
- **Input Data (JSON):**
  ```json
  {
    "mode": "standard | gap_closure",
    "phase_number": "01",
    "project_state": "Content of STATE.md",
    "roadmap": "Content of ROADMAP.md",
    "requirements": "Content of REQUIREMENTS.md",
    "context": "Content of CONTEXT.md (User Decisions)",
    "research": "Content of RESEARCH.md",
    "verification_gaps": "Content of VERIFICATION.md (only in gap_closure mode)"
  }
  ```
- **Output:** One or more `[PHASE]-[PLAN]-PLAN.md` files.
- **Orchestration Logic:**
  - Must validate that User Decisions (from `CONTEXT.md`) are respected.
  - Generates "Waves" for parallel execution.

### C. Plan Checker (`gsd-plan-checker`)
**Goal:** Critic / Quality Gate for generated plans.

- **Trigger:** After Planning, before Execution.
- **Input Data:**
  ```json
  {
    "plans": ["Content of Plan 01", "Content of Plan 02"...],
    "requirements": "Content of REQUIREMENTS.md",
    "user_decisions": "Content of CONTEXT.md"
  }
  ```
- **Output:** Structured Feedback (Pass/Fail + Issues List).
- **Orchestration Logic:**
  - If Fail: Loop back to Planner with `mode: revision` and specific issues.
  - Max iterations (e.g., 3) before asking human to intervene.

### D. Executor (`gsd-executor`)
**Goal:** Execute a single Plan file. This is the "Builder".

- **Trigger:** Execution Phase. Can run in parallel for plans in the same "Wave".
- **Input Data:**
  ```json
  {
    "plan_content": "Content of specific PLAN.md",
    "project_state": "Content of STATE.md",
    "config": "Content of config.json"
  }
  ```
- **Output:**
  - `SUMMARY.md` (Report of what was built)
  - Git Commits (Code changes)
  - Checkpoint Signal (if user intervention needed)
- **Orchestration Logic:**
  - **Waves:** Run all Wave 1 Executors in parallel. Wait for all to finish before Wave 2.
  - **Checkpoints:** If Executor hits `type="checkpoint"`, it pauses and saves state. Orchestrator must ask User, then spawn a **Continuation Agent**.

### E. Phase Verifier (`gsd-verifier`)
**Goal:** Verify if the high-level Phase Goal (from Roadmap) was achieved.

- **Trigger:** After all plans in the phase are executed.
- **Input Data:**
  - Phase Directory path
  - Phase Goal (from Roadmap)
  - `must_haves` criteria (derived during Planning)
- **Output:** `VERIFICATION.md` with status (`passed`, `human_needed`, `gaps_found`).
- **Orchestration Logic:**
  - `passed`: Mark phase complete.
  - `gaps_found`: Trigger `gap_closure` loop (Back to Planner with `--gaps`).
  - `human_needed`: Notify User.

---

## 3. Data Structure & State Management

To orchestrate this, you need a central **State Object** that persists across the graph execution.

### Proposed Orchestration State
```typescript
interface GSDState {
  // Project Context
  projectRoot: string;
  config: ProjectConfig;
  
  // Current Scope
  activePhase: {
    number: string;
    name: string;
    dir: string;
  };

  // Execution State
  execution: {
    waves: number;
    currentWave: number;
    completedPlans: string[]; // IDs
    activePlans: string[]; // IDs
    blockers: string[];
  };

  // Artifact Cache (loaded by init tools)
  artifacts: {
    roadmap: string;
    state: string;
    requirements: string;
    context?: string; // User decisions
    research?: string;
  };
}
```

### Data Flow Diagram

1.  **Start Phase** -> Load `GSDState` (via `gsd-tools.js init`)
2.  **Research Node**:
    - Check `artifacts.research`.
    - If missing -> Call Phase Researcher -> Update `artifacts.research`.
3.  **Planning Node**:
    - Call Planner with `artifacts`.
    - Output -> specific `PLAN.md` files on disk.
4.  **Verification Node**:
    - Read `PLAN.md` files.
    - Call Plan Checker.
    - If Issues -> **Revision Node** -> Update `PLAN.md` files -> loop.
5.  **Execution Node**:
    - Index Plans (Wave grouping).
    - **Loop over Waves**:
        - Parallel execute plans in Wave N.
        - Monitor for Checkpoints.
        - Aggregate `SUMMARY.md` results.
6.  **Phase Verification Node**:
    - Call Phase Verifier.
    - Update State/Roadmap.

## 4. Key Files for Extraction
- **`manifest`**: `get-shit-done/bin/gsd-tools.js` (The brain/utility belt)
- **`prompts`**: `agents/*.md` (The instructions/personas)
- **`workflows`**: `commands/gsd/*.md` & `get-shit-done/workflows/*.md` (The logic to implement in LangGraph)
