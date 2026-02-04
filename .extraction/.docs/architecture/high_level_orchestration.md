# High-Level Orchestration Architecture: The "Meta-Shell"

## 1. The Core Concept

The proposed architecture abstracts the specific "Claude Code" dependencies of `get-shit-done` into a generalized **Meta-Shell** pattern.
This system does not run inside a Python script; it runs _inside the LLM's context_, driven by executable Markdown files.

### The Stack layers

1.  **Infrastructure Layer** (The "Runtime")
2.  **State Layer** (The "File DB")
3.  **Orchestration Layer** (The "Meta-Agent")
4.  **Execution Layer** (The "Subagents")

---

## 2. Layer-by-Layer Architecture

### Layer 1: Infrastructure (The Runtime)

To extract this, you need a "Host" capable of:

- **Tool Use**: Specifically `read_file`, `write_file`, `run_command`, and crucially `task()` (or `spawn_agent`).
- **Recursive Prompting**: The ability to effectively "read instructions on how to behave" from a file and immediately adopt that persona.

**Extraction Strategy**:
Define a standard **"Host Interface"** that any LLM driver (Claude Code, OpenGen, custom Python script) must implement:

```typescript
interface Host {
  spawnAgent(systemPrompt: string, userTask: string): Promise<string>; // Returns artifact content
  readFile(path: string): string;
  writeFile(path: string, content: string): void;
}
```

### Layer 2: State (The File DB)

This is the "Hard Disk" of the AI. It replaces the LLM's context window.

**Components**:

- **`ROOT/.meta/`**: The hidden directory for system state.
- **`project.json`**: Static configuration (goals, constraints).
- **`state.md`**: Volatile memory (current step, blocking issues).
- **`artifacts/`**: The directory where subagents dump their outputs (`plan.xml`, `research.json`).

**Extraction Strategy**:
Don't use ad-hoc filenames. Standardize the schema:

- `active_context.md`: The file that is ALWAYS injected into the Orchestrator.
- `history.log`: A curated log of _completed_ high-level actions (not chat logs).

### Layer 3: Orchestration (The "Meta-Agent")

This is the heart of the extraction. The Orchestrator is **NOT** a fixed Python script. It is an LLM instantiated with a **Workflow Definition**.

**The Workflow Definition (Markdown)**:
Instead of `plan-phase.md` (which is shell-heavy), we define a cleaner DSL (Domain Specific Language) in Markdown that the LLM interprets:

```markdown
# Workflow: Feature Implementation

## Step 1: Check State

Action: Read `.meta/state.md`.
Logic: If `status == "planning"`, go to Step 2.

## Step 2: Spawn Planner

Action: Call `task()` tool.

- Role: "Architect"
- Context: `project.json` + `user_request`
- Output: `.meta/artifacts/plan.xml`

## Step 3: Validate

Action: Read `.meta/artifacts/plan.xml`.
Logic: If `<risk>high</risk>`, trigger "Human Approval".
```

**Why this is extractable**: You supply this Markdown file to _any_ sufficiently smart LLM (Opus, GPT-4), and it _becomes_ the Orchestrator.

### Layer 4: Execution (The Subagents)

These are the ephemeral workers.

**Extraction Strategy**:
Decouple "Skills" from "Workflows".

- **Skill Library**: A folder of `.md` files defining _only_ the Persona and Tools for a subagent (e.g., `skills/researcher.md`).
- **Injection**: The Orchestrator reads `skills/researcher.md` and passes it as the System Prompt to `spawnAgent()`.

---

## 3. The Data Flow (The "Artifact Bus")

How data moves without Context Bloat:

1.  **User Request** -> Written to `state.md`.
2.  **Orchestrator** reads `state.md`.
3.  **Orchestrator** spawns **Planner**.
4.  **Planner** writes `plan.xml` to disk. **Planner Dies.**
5.  **Orchestrator** reads `plan.xml`.
6.  **Orchestrator** spawns **Executor** (and injects `plan.xml` content).
7.  **Executor** writes Code + `summary.md`. **Executor Dies.**
8.  **Orchestrator** reads `summary.md`, updates `state.md`.

## 4. Technical Specification for Extraction

To build this independent framework, you need to build:

1.  **The Bootstrap Script**: A simple CLI tool (`npx meta-shell`) that:
    - Initializes the `.meta` folder.
    - Provides the `spawn_agent` tool implementation (connecting to an LLM API).
2.  **The Standard Library**:
    - `orchestrator.md`: The main loop logic.
    - `skills/`: The standard personas (Planner, Coder, Reviewer).
3.  **The State Manager**:
    - A utility to robustly read/write the JSON/Markdown state files to prevent corruption.

This architecture decouples the "Brain" (Prompts/Workflows) from the "Body" (CLI/API calls), making it highly portable.
