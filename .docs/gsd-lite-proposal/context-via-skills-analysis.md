# Analysis: Context Injection via Agent Skills vs. Directory References

## The Question

> "Would it be easier for the LLM if we inject the context (states, project details, etc) through agent-skills instead of referencing some directory in the project?"

## Analysis

### Option A: Directory References (Current "Granular" Proposal)

**Mechanism**: Context is stored in `.planning/codebase/*.md`. The LLM navigates this via `ls` or `INDEX.md` and explicitly reads files.

- **Pros**:
  - **Git-Tracked**: Context lives with the code. Every commit has matching context.
  - **Transparent**: User sees exactly what the AI sees (markdown files).
  - **Stateless Agent**: The agent doesn't need "pre-warming"; it just looks at the disk.
- **Cons**:
  - **Friction**: Requires multiple tool calls (`list_dir` -> `view_file`).
  - **Discovery**: LLM might fail to look in the right place if not prompted.

### Option B: Context via Agent Skills (Proposed)

**Mechanism**: A custom "Skill" (e.g., `project-context-skill`) is loaded. This skill essentially "injects" knowledge or provides specialized tools to get it.

- **Pros**:
  - **Zero Friction**: If context is injected into the System Prompt via the skill, the LLM "just knows" it immediately.
  - **Abstraction**: A tool like `get_architecture_context()` is easier for an LLM to use than navigating a file tree.
- **Cons**:
  - **Token Explosion**: If we inject _text_ via the skill, we return to the "context overload" problem.
  - **Portability**: Skills are often global or user-specific, whereas Project Context is repo-specific. Sharing the repo requires the other user to install the skill.
  - **Staleness**: If the skill defines static text, it gets outdated fast.

### Hybrid Solution: The "Context Manager" Skill

The best approach leverages the **interface** of a Skill but keeps the **storage** in the Directory.

**Concept**: A generic `codebase-context` skill that is installed once, but reads from the local project's `.planning/` directory.

**Workflow**:

1.  **Storage**: We still keep granular files (`.planning/codebase/auth.md`) so they are git-tracked.
2.  **Interface**: We add a **Skill** that provides high-level tools:
    - `get_project_summary()` -> Reads `INDEX.md` and returns a summary.
    - `get_domain_context(domain="auth")` -> Automatically finds and reads `.planning/codebase/architecture/auth.md`.

**Why this is better for Local LLMs**:

- **Structured**: The LLM calls a function `get_domain_context(domain="auth")` which is a strong, deterministic signal.
- **Efficient**: No need to `ls`, `grep`, or guess file paths.
- **Safe**: Limits context verification to the specific requested domain (Lazy Loading).

## Recommendation

**Do not store data in Skills.** Store data in **Files**, but use a **Skill (Tools)** to retrieve it.

We should create a **`context-manager`** skill as part of GSD-Lite that abstracts the file system operations for the LLM.
