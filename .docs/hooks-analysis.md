# Analysis & Evaluation: Hooks for Smaller Models

Based on an analysis of the `get-shit-done` project, here is the evaluation regarding "hooks" for smaller models/packages.

The project uses a structured orchestration system defined in Markdown files within the `workflows/` directory. The "granularity" you are looking for is currently managed by the **Architectural Pattern** rather than a specific code "hook".

## 1. The "Hook" Location

The exact place to inject your "smaller package" instructions is in the **Orchestrator Workflows**.
Specifically, the system explicitly spawns the `gsd-executor` (the large agent) in two critical locations. These are the points you need to intercept or modify to use your smaller, granular agents.

- **Primary Hook (Plan Level):** `workflows/execute-plan.md`
  - **Step:** `segment_execution` (Lines 350-525)
  - **Logic:** This step parses "segments" (tasks between checkpoints) and spawns a subagent to execute them.
  - **Current State:** It explicitly calls `Task(..., subagent_type="gsd-executor")`.
  - **Opportunity:** This is where you can swap `gsd-executor` for your more granular agent (e.g., `gsd-micro-tasker`) or inject exact, prompt-engineered instructions limiting the scope for smaller models.

- **Secondary Hook (Phase Level):** `workflows/execute-phase.md`
  - **Step:** `execute_waves` (Lines 247-376)
  - **Current State:** It spawns parallel agents for autonomous plans, also hardcoded to `gsd-executor`.

## 2. Granularity Mechanism

The project _does_ have a mechanism for granularity called **Segmentation**.

- In `execute-plan.md`, the `parse_segments` step (Lines 154-300) breaks a `PLAN.md` file into smaller chunks based on "Checkpoints".
- If you insert checkpoints (e.g., `type="checkpoint:human-verify"`) into a plan, the system automatically breaks the execution into smaller "packets" (segments). Each segment is a fresh context window.
- **For smaller models:** You can exploit this by ensuring plans are heavily segmented (either manually or by modifying the planner to insert more checkpoints), forcing the system to feed smaller "packages" of tasks to the agents.

## Recommendation

Since you mentioned you already have the split instructions (presumably new Agent definitions or Prompts), you have two options to "hook" them in:

1.  **Dynamic Agent Selection (Recommended):**
    Modify `workflows/execute-plan.md` to resolve the `subagent_type` from `config.json` (similar to how it currently resolves `executor_model`).
    - _Add to `resolve_model_profile` step:_ Read an `agent_type` variable from config.
    - _Modify `segment_execution` step:_ Change `subagent_type="gsd-executor"` to `subagent_type="{agent_type}"`.
      This allows you to switch between the "Heavy" executor and your "Small/Granular" executor purely via configuration.

2.  **Force Granularity via Logic:**
    Modify the `parse_segments` step in `execute-plan.md` to automatically enforce segmentation (e.g., "every 1 task is a segment") when a "small model" profile is detected. This forces the existing system to process in micro-batches without changing the agent definition itself.

**Conclusion:** The project is modular enough that you don't need to rewrite the engine. You just need to modify `workflows/execute-plan.md` to point to your new "instructions" (Agent) instead of the default one.
