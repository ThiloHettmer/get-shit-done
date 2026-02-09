# Ticket 2: Research & Implementation of Researcher Blackbox

**Goal:** Implement the `gibd-phase-researcher` runner with fully isolated context injection.

## Research: Data & State Requirements

| Source            | Data Item          | Injection Mode                |
| ----------------- | ------------------ | ----------------------------- |
| `PHASE_INFO`      | Name, Num, Goal    | `<phase_info>` XML block      |
| `CONTEXT.md`      | User Decisions     | `<user_decisions>` XML block  |
| `REQUIREMENTS.md` | Full content       | `<requirements>` XML block    |
| `ROADMAP.md`      | Related phase info | `<roadmap_context>` XML block |
| `STATE.md`        | Project state      | `<project_state>` XML block   |

**Tasks:**

- [ ] Create `src/orchestration/agents/phase-researcher.ts`.
- [ ] Implement `composePrompt` for Researcher:
  - Read `PHASE_INFO` from Roadmap.
  - Read `CONTEXT.md` from phase directory.
  - Read `STATE.md` and `REQUIREMENTS.md`.
  - Wrap all into the XML blocks identified in research.
- [ ] Implement `execute()`: calls LLM and returns the `ResearcherOutput` schema.
- [ ] Implement `ArtifactWriter`: writes the result to `.planning/phases/[PHASE]/[PHASE]-RESEARCH.md`.

**Acceptance Criteria:**

- Running `gibd-runner research --phase 01` creates a valid `RESEARCH.md` file using local logic only.
- Output respects all `CONTEXT.md` constraints.
