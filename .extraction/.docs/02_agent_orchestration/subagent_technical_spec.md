# Subagent Technical Specification: Instructions, Context & Token Economy

## 1. Subagent Implementation & Instructions

A "Subagent" is not a person or a chatbot. It is a **deterministic specialized worker** instantiated for a single purpose.

### 1.1 The Definition Structure

Every subagent is defined by a "Skill Definition" (YAML/JSON) containing:

1.  **System Prompt**: The immutable persona and strict rules (e.g., "You are a specialized Goal-Backward Planner...").
2.  **Tool Definitions**: The specific subset of tools allowed (e.g., `read_file`, `grep`, but NOT `write_file` for a researcher).
3.  **Input Schema**: What data triggers this agent?
4.  **Output Schema**: What strict format must it return? (e.g., `<plan>...</plan>` XML).

### 1.2 The "Instruction" Payload

When spawning an agent, we send a **Single Composite Prompt**:

```markdown
# SYSTEM

[System Prompt content...]

# CONTEXT (Injected)

[Relevant file contents...]

# TASK

"Analyze the `CONTEXT` and produce a `PLAN` for the `INPUT` goal."

# INPUT

User Goal: "Add OAuth."
```

**Rule**: The agent must never need to "ask" for its initial context. It must be provided in the spawn payload.

---

## 2. Context Injection Mechanics (The "Assembler")

Context Injection is the programmatic process of selecting and loading the _minimum viable context_ into the agent's window _before_ the first token is generated.

### 2.1 The Injection Strategy: "Slicing"

We do NOT dump the repo. We inject specific "Slices" based on the Agent Type.

**Example: The Planner Slice**
The Orchestrator runs a script to assemble the prompt:

1.  **Project State**: Reads `.planning/PROJECT.md` -> Injects as `<project_vision>...</project_vision>`.
2.  **Roadmap**: Reads `.planning/ROADMAP.md` -> Injects as `<roadmap_status>...</roadmap_status>`.
3.  **Phase Specs**: Reads `.planning/CONTEXT.md` -> Injects as `<current_constraints>...</current_constraints>`.
4.  **No Code**: The Planner typically does _not_ see code files, only structures/outlines.

**Example: The Executor Slice**

1.  **The Plan**: Reads `PLAN.md` -> Injects as `<mission_protocol>...</mission_protocol>`.
2.  **Target Files**: If the plan mentions `src/auth.ts`, the Orchestrator reads that file and injects it.
3.  **No History**: The Executor does _not_ see the Roadmap or Project Vision. It only sees its Task.

### 2.2 Dynamic File Loading

The subagent is allowed to use `read_file` to pull in _additional_ context, but this is "Active Context" (costs execution tokens) vs "Injected Context" (available immediately).

---

## 3. Token Economy & Preventing Context Bloat

The primary enemy is "Context Bloat" — the accumulation of irrelevant history that degrades model performance.

### 3.1 The "Fire and Forget" Lifecycle (Ephemeral Context)

1.  **Spawn**: Process Starts. Token Count = `System + Injected Context`. (~5k-10k tokens).
2.  **Work**: Agent generates thoughts/tool calls. Token Count grows.
3.  **Threshold**: If Token Count > 60% of Window:
    - **Action**: FORCED TERMINATION.
    - **Fallback**: Agent must summarize current state to a file, and a _new_ agent spawns to pick up.
4.  **Terminate**: Process Ends. **Memory is Wiped.** The Token Count resets to 0 for the next agent.

### 3.2 Artifact-Based Handoff (The "Baton")

Since agents have no memory after termination, how do we pass knowledge?
**Artifacts**.

- Agent A (Researcher) works for 50k tokens. It learns a lot.
- Agent A writes `DISCOVERY.md` (compressed summary, 2k tokens).
- Agent A dies.
- Agent B (Planner) spawns. It reads `DISCOVERY.md`.

**Result**: We compressed 50k of "thought/search" tokens into 2k of "context" tokens for the next agent.
**Rule**: Never pass the chat history. Pass the Artifact.

### 3.3 Strict Output Formats (Parsing Efficiency)

Chatty agents waste tokens. Subagents must use XML/JSON.

- **Bad**: "Okay, I have analyzed the dependencies and I think we should update these three..."
- **Good**:
  `xml
    <analysis>
      <dep>react@19</dep>
      <action>update</action>
    </analysis>
    `
  **Optimization**: We use `<stop_sequences>` to cut off the model immediately after `</response>`, preventing "Are there any other questions?" fluff.
