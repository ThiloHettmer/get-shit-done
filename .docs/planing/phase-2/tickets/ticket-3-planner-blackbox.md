# Ticket 3: Research & Implementation of Planner Blackbox

**Goal:** Implement the `gibd-planner` runner with goal-backward context injection.

## Research: Data & State Requirements

| Source            | Data Item           | Injection Mode                  |
| ----------------- | ------------------- | ------------------------------- |
| `*-RESEARCH.md`   | Domain findings     | `<research_findings>` XML block |
| `CONTEXT.md`      | User Constraints    | `<user_constraints>` (CRITICAL) |
| `ROADMAP.md`      | Phase Goal          | `<phase_roadmap>` XML block     |
| `STATE.md`        | Current Files/State | `<current_state>` XML block     |
| `VERIFICATION.md` | (If gap closure)    | `<verification_gaps>` XML block |

**Tasks:**

- [ ] Create `src/orchestration/agents/planner.ts`.
- [ ] Implement `composePrompt` for Planner:
  - Must prioritize `<user_constraints>` as per `gibd-planner.md` instruction line 47.
  - Injects `RESEARCH.md` as the primary implementation blueprint.
- [ ] Implement `outputParser`:
  - Planner returns multiple plans. Implement logic to extract and write each `<plan>` to a separate file: `[PHASE]-[PLAN]-PLAN.md`.
- [ ] Implement `WaveAssigner`: reads frontmatter and assigns initial waves for parallelization.

**Acceptance Criteria:**

- Running `gibd-runner plan --phase 01` generates 1-3 `PLAN.md` files.
- Each plan contains `must_haves` in the frontmatter.
