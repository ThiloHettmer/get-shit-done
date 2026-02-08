# GSD-Lite: Granular Codebase Mapping

## Problem

The current 7 monolithic files (`STACK.md`, `ARCHITECTURE.md`, `INTEGRATIONS.md`, `STRUCTURE.md`, `CONVENTIONS.md`, `TESTING.md`, `CONCERNS.md`) are too large for local LLMs, leading to:

- Context window overflow
- Difficulty in focused retrieval
- "Hallucination" due to irrelevant details being loaded

## Proposed Solution: Index-First Architecture

Instead of dumping everything into a few files, we should use a **hierarchical, reference-based system**.

### 1. The Structure

Instead of `.planning/codebase/ARCHITECTURE.md`, we use:

- `.planning/codebase/INDEX.md` (High-level map)
- `.planning/codebase/architecture/core.md`
- `.planning/codebase/architecture/auth.md`
- `.planning/codebase/architecture/database.md`
- ... (domain-specific files)

### 2. The Index (`INDEX.md`)

This file acts as a "Site Map" for the AI. It contains:

- Summary of the project
- Links to specialized context files
- Brief description of what each file contains

**Example `INDEX.md`:**

```markdown
# Project Context Index

## Architecture

- [Core Patterns](architecture/core.md): MVC structure, dependency injection
- [Authentication](architecture/auth.md): JWT implementation, user roles
- [Database](architecture/database.md): Schema design, migrations

## Technology Stack

- [Frontend](stack/frontend.md): React 18, Tailwind
- [Backend](stack/backend.md): Node.js, Express
```

### 3. Agent Workflow

Instead of `gsd-codebase-mapper` trying to fit everything in one file, it should:

1.  **Survey**: Initial scan to identify major modules/domains.
2.  **Split**: Decide on logical boundaries (e.g., specific features or layers).
3.  **Generate**: Create focused markdown files for each domain.
4.  **Link**: Update `INDEX.md` with references to these new files.

### 4. Consumption Strategy (Lazy Loading)

When a task starts:

1.  LLM reads `INDEX.md`.
2.  LLM determines which specific context files are relevant to the _current task_.
3.  LLM uses `read_file` to load _only_ those files.

**Benefits:**

- **Drastically reduced context usage**: Only load what you need.
- **Improved focus**: LLM isn't distracted by unrelated architecture details.
- **Scalability**: Can handle massive projects without hitting token limits.
