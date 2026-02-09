# Ticket 3: Extract Templates

**Goal:** Copy the templates used by the core agents to ensure consistent output format.

**Tasks:**

- [ ] Copy `get-shit-done/templates/summary.md` to `.docs/prototype/templates/summary.md`
- [ ] Copy `get-shit-done/templates/verification-report.md` to `.docs/prototype/templates/verification-report.md`

**Acceptance Criteria:**

- Both template files exist in `.docs/prototype/templates/`.
- Templates are ready for updates in Ticket 4.

## Detailed Analysis

### 1. Summary Template (`summary.md`)

- **Source:** `get-shit-done/templates/summary.md`
- **Purpose:** Used by `gibd-executor` (via `execute-plan.md`) to generate the `[PHASE]-[PLAN]-SUMMARY.md` file after plan execution.
- **Key Sections:**
  - **Frontmatter:** Machine-readable metadata (phase, plan, tech-stack, metrics). Crucial for dependency graph and automatic context loading in future phases.
  - **Accomplishments:** Bulleted list of what was shipped.
  - **Deviations:** Documents auto-fixes (Rules 1-3) and architectural decisions (Rule 4).
  - **Issues Encountered:** Unexpected blockers.
- **Adaptation Needs:**
  - Verify frontmatter fields align with GIBD needs (likely keep as is, it's robust).
  - Ensure instructions for filling it out (e.g., `gsd-tools` usage) can be mapped to GIBD equivalents or instructions.

### 2. Verification Report Template (`verification-report.md`)

- **Source:** `get-shit-done/templates/verification-report.md`
- **Purpose:** Used by `gibd-verifier` (or the verification workflow) to generate `[PHASE]-VERIFICATION.md` _after_ all plans in a phase are executed.
- **Key Sections:**
  - **Status:** `passed` | `gaps_found` | `human_needed`.
  - **Goal Achievement:** Table of Observable Truths (Verified/Failed).
  - **Artifacts:** Table of files checked (Exists/Substantive/Stub).
  - **Wiring:** Table of key links (Wired/Not).
  - **Fix Plans:** Strategies for closing gaps.
- **Adaptation Needs:**
  - This template structure is critical for the `gibd-verifier` to output structured data that the Orchestrator can parse.
  - Ensure the output path logic in the template (or instructions surrounding it) points to the correct location in the prototype.
