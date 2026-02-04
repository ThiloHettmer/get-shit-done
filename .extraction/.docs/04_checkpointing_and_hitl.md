# Checkpointing, HITL & Interruptible Agents

## The "Stop and Return" Protocol

In standard scripts, `input()` pauses execution. In Agentic workflows, **Agents cannot "pause"**. They consume tokens while waiting.
Instead, when an agent needs user input, it must:

1.  **Serialize State**: Save progress to disk/summary.
2.  **Emit Signal**: Output a strict "Checkpoint Reached" message.
3.  **Terminate**: The process ends.

The Orchestrator sees the signal, prompts the user (CLI/UI), and then **Spawns a NEW Agent** (Continuation Agent) to resume.

## Checkpoint Types

### 1. `checkpoint:human-verify` (Approvals)

- **Usage**: 90% of cases. Visual checks, flow verification.
- **Prompt**: "I built X. Go to URL Y. Tell me if it looks right."
- **Behavior**: Blocking gate. Agent cannot proceed until "Approved".

### 2. `checkpoint:decision` (Branching)

- **Usage**: Architectural choices, Ambiguity resolution.
- **Prompt**: "I can use Library A (Pros/Cons) or Library B (Pros/Cons). Choose."
- **Structure**:
  ```xml
  <options>
    <option id="a">React Query</option>
    <option id="b">SWR</option>
  </options>
  ```

### 3. `checkpoint:human-action` (Unavoidable Manual Tasks)

- **Usage**: 2FA, SMS codes, Email links, credit card entry.
- **Constraint**: ONLY for things the agent _cannot_ do via API/CLI.
- **Prompt**: "I triggered the email. Click the link. Type 'done' when ready."

## Authentication Gates (Dynamic Checkpoints)

Agents often encounter auth walls (e.g., `vercel login`, `gh auth login`).
**Protocol**:

1.  Agent tries command: `vercel deploy`.
2.  Stderr: `Error: Not authenticated`.
3.  **Agent Logic**: DO NOT RETRY.
4.  **Action**: Dynamically generate a `checkpoint:human-action`.
5.  **Output**: "I hit an auth wall. Run `vercel login`. Resuming shortly."

## Human-in-the-Loop (HITL) Design Patterns

### The "Skeptical" Loop

Assume the Agent is wrong until proven right.

1.  Agent: "I fixed the bug."
2.  Orchestrator: "Show proof." (Run verification/test).
3.  Orchestrator -> User: "Agent says it fixed bug X. Tests pass. Do you want to verify manually?"

### Resume Fidelity

When resuming after a checkpoint, the new agent needs:

1.  **Summary of Completed Tasks**: What was done before the pause.
2.  **Current Task Context**: Where exactly did we stop?
3.  **User Input**: The answer/decision provided by the user.

**Anti-Pattern**: DO NOT re-read the entire chat history. Read the `SUMMARY.md` + `CHECKPOINT_DATA.json`.
