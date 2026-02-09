# Ticket 6: Research & Implementation of Phase Verifier Blackbox

**Goal:** Implement the `gibd-verifier` as a final goal-backward verification runner.

## Research: Data & State Requirements

| Source         | Data Item        | Injection Mode                       |
| -------------- | ---------------- | ------------------------------------ |
| `*-PLAN.md`    | Initial Intent   | `<plan_intent>` XML block            |
| `*-SUMMARY.md` | Execution Claims | `<execution_summaries>` XML block    |
| `ROADMAP.md`   | Phase Goal       | `<phase_goal>` XML block             |
| `CODEBASE`     | Actual Files     | Accessible via `Read` / `Bash` tools |

**Tasks:**

- [ ] Create `src/orchestration/agents/verifier.ts`.
- [ ] Implement `composePrompt` for Verifier:
  - Consolidates all instructions from the phase goal and plans.
- [ ] Implement `VerificationLogic`:
  - Three-level check logic: Exists? Substantive? Wired?
  - Agent should use `grep` and `cat` to perform these checks.
- [ ] Implement `ReportGenerator`: extracts the `<verification_report>` and writes `VERIFICATION.md`.

**Acceptance Criteria:**

- Running `gibd-runner verify --phase 01` generates a `VERIFICATION.md` with status `passed` or `gaps_found`.
