# Research: Orchestration Mechanics in `get-shit-done`

## 1. The "Natural Language Orchestrator" Pattern

Unlike traditional agent frameworks (LangChain, AutoGen) that use Python/JS classes to manage state, `get-shit-done` uses **Markdown-based Workflows** as the executable code for the Orchestrator.

- **The Runtime**: The Main Agent (e.g., Claude Code, OpenCode).
- **The Code**: files like `commands/gsd/plan-phase.md`.
- **The State**: Markdown files on disk (`.planning/STATE.md`).

**Implication**: The Orchestrator is _itself_ an LLM agent following a valid "Prompt Program". It reads the `.md` file and executes the steps (Running bash commands, logic checks, and spawning subagents) autonomously.

## 2. Spawning Mechanics ("The Task Tool")

Subagents are not spawned via a specialized API endpoint but via a **Tool Call** that the Main Agent invokes.

### The Syntax (from `plan-phase.md`)

```python
Task(
  prompt="First, read ~/.claude/agents/gsd-planner.md...\n\n" + filled_prompt,
  subagent_type="general-purpose",
  model="{planner_model}",
  description="Plan Phase {phase}"
)
```

1.  **`subagent_type`**: Maps to a specific configuration/persona.
2.  **`model`**: Dynamically resolved from `config.json` (allowing "Budget" vs "Quality" profiles).
3.  **`prompt`**: A massive concatenated string containing System Instructions + Context.

## 3. Context Injection: The "Assembler" Pattern

The Orchestrator explicitly _assembles_ the context slice before spawning. It does not rely on the subagent to "pull" context; it "pushes" it.

### The Assembly Pipeline (Step-by-Step)

1.  **Read**: The Orchestrator execute `cat` commands to read content.
    ```bash
    STATE_CONTENT=$(cat .planning/STATE.md)
    ```
2.  **Filter**: It only reads what is needed (e.g., `gsd-planner` gets `ROADMAP.md` but not code files).
3.  **Interpolate**: The content is injected into the `<planning_context>` XML block in the prompt string.

**Why this is Brilliant**:

- **Determinism**: The subagent sees _exactly_ what the rules say it should see.
- **Token Control**: The Orchestrator controls the budget by choosing what to `cat`.
- **Security**: The subagent works in a sandbox defined by the prompt.

## 4. Instruction Engineering Analysis

### What makes them "Special"?

- **Self-Correction Loops**: The Orchestrator has logic to _verify_ the subagent's output (e.g., `gsd-plan-checker`). If the check fails, the Orchestrator typically creates a **Revision Loop** (up to 3 iterations) where it feeds the error report back to the Planner.
- **Strict Handshakes**: The "Contract" between Orchestrator and Subagent is the **Artifact** (`PLAN.md`). The Orchestrator checks for the _existence_ of valid files as a success criterion.

### What should be improved?

- **Prompt String injection**: The current method relies on string concatenation of shell variables. If a file is massive, this command might fail or truncate. A better approach (Spec recommendation) is to tell the subagent "Read file X" rather than dumping file X into the prompt, _unless_ the file is small (like `STATE.md`).
- **Error Handling**: If `Task()` fails (e.g. API error), the orchestration file relies on the model's natural recovery. Harder "Try/Catch" blocks in the markdown logic (using `<rescue>` tags or similar) could be more robust.

## 5. Alignment with Technical Spec

The current implementation aligns 90% with the `.docs/02_agent_orchestration/subagent_technical_spec.md`.

- **Ephemeral**: Yes, `Task()` starts a fresh context.
- **Artifact-based**: Yes, `PLAN.md` is the bus.
- **Context Slicing**: Yes, via specific `cat` commands.

**Deviation**: The Spec suggests strict XML outputs. The current `gsd-planner` outputs Markdown files (`PLAN.md`). This is actually _better_ for this specific use case as the artifact IS the final product, but for internal logic (like "Decide next step"), XML is preferred.
