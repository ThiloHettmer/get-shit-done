# Meta-Prompting & Context Engineering Framework

## Core Philosophy: The "Fresh Context" Paradigm

The central constraint of current LLM (Large Language Model) application engineering is **Context Rot**. As a conversation or task progresses, the context window fills with:

1.  **Noise**: Verbose logs, extensive file contents, and reasoning steps.
2.  **Drift**: Subtle deviations from the original instructions.
3.  **Performance Degradation**: Models become "lazy", skip steps, or hallucinate as context usage approaches 60-70%.

### The Solution: Ephemeral Agents & Externalized State

Instead of a single long-running chat session, this framework utilizes a **recursive, multi-agent architecture** where every significant unit of work is performed by a fresh agent with a pristine context window.

**Key Rule**: No agent should ever operate with >50% context usage. If a task requires more, it must be decomposed.

## Architecture Guidelines

### 1. State as the "Source of Truth"

Complex state must never rely on the LLM's context memory. State is externalized into structured Markdown/JSON files that act as the persistent memory store (the "Database" of the agent system).

- **`PROJECT.md`**: Immutable vision and high-level goals.
- **`ROADMAP.md`**: The dynamic plan of phases and status.
- **`STATE.md`**: The volatile "RAM" - current focus, recent decisions, blockers.
- **`CONTEXT.md`**: User preferences and constraints for the current phase.

### 2. The Hierarchy of Scope

To maintain the "Fresh Context" rule, work is rigorously decomposed:

1.  **Milestone** (Weeks): A major version or release.
2.  **Phase** (Days): A logical grouping of features (e.g., "Authentication System").
3.  **Plan** (Hours): A strictly bounded unit of work (2-3 atomic tasks).
4.  **Task** (15-60 mins): A single execute-commit cycle.

### 3. The Orchestrator Pattern

The "Orchestrator" is a thin logic layer (often a script or a master agent) that:

1.  **Reads State**: checks `STATE.md`.
2.  **Spawns Agent**: Starts a specialized subagent (Planner, Executor, Verifier) with specific instructions.
3.  **Waits**: It does _not_ interfere.
4.  **Integrates**: Reads the artifact produced by the agent (e.g., `PLAN.md`, `SUMMARY.md`).
5.  **Routes**: Decides the next step (e.g., if Plan is done -> Verify; if Checkpoint -> Prompt User).

## Context Injection Strategy

Agents are not given the entire history. They are given **Context Slices**:

- **Planner Agent**: Receives `PROJECT.md`, `ROADMAP.md`, `CONTEXT.md` (Constraints), and `[Phase Goal]`.
- **Executor Agent**: Receives _only_ the specific `PLAN.md` it is executing. It does not need to know about the entire roadmap, only its atomic mission.
- **Verifier Agent**: Receives `REQUIREMENTS.md` and the `SUMMARY.md` of what was built.

## Verification & Feedback Loops

Autonomous agents cannot be trusted implicitly. Every loop must close with verification.

- **Plan Verification**: A "Plan Checker" agent reviews the `PLAN.md` against `REQUIREMENTS.md` before execution begins.
- **Execution Verification**: Each task in a plan generally includes a `<verify>` step.
- **Phase Verification**: A "Verifier" agent audits the codebase after execution to ensure alignment with goals.

## Metrics & KPIs for LLMs

- **Context Efficiency**: % of tokens used per successful commit.
- **Reversion Rate**: How often a task needs to be redone.
- **Intervention Rate**: Frequency of human checkpoints triggered.
