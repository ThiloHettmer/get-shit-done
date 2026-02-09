# Ticket 4: Research & Implementation of Plan Checker Blackbox

**Goal:** Implement the `gibd-plan-checker` as a quality gate runner.

## Research: Data & State Requirements

| Source            | Data Item        | Injection Mode                 |
| ----------------- | ---------------- | ------------------------------ |
| `*-PLAN.md`       | Generated Plans  | `<plans_to_check>` XML block   |
| `ROADMAP.md`      | Phase Goal       | `<phase_goal>` XML block       |
| `REQUIREMENTS.md` | Phase Scope      | `<requirements>` XML block     |
| `CONTEXT.md`      | Compliance Rules | `<user_constraints>` XML block |

**Tasks:**

- [ ] Create `src/orchestration/agents/plan-checker.ts`.
- [ ] Implement `composePrompt` for Plan Checker:
  - Injects all plans generated in the previous step.
  - Injects requirements to check coverage.
- [ ] Implement `StaticAnalyzer` shim:
  - Wrapper around `gsd-tools.js verify plan-structure` (or local equivalent) to provide baseline structural checks to the agent.
- [ ] Implement `IssueAggregator`: extracts YAML issue blocks from agent response.

**Acceptance Criteria:**

- Running `gibd-runner check --phase 01` returns a structured list of issues (Blockers/Warnings).
- If no issues, returns "passed".
