# Ticket 4: Rename and Update References

**Goal:** Finalize the migration by renaming all copied files and updating internal references to point to the local prototype paths.

**Tasks:**

- [ ] Rename `gibd-phase-researcher.md` (Self-referential name headers).
- [ ] Rename `gibd-planner.md` (Self-referential name headers).
- [ ] Rename `gibd-plan-checker.md` (Self-referential name headers).
- [ ] Rename `gibd-executor.md` (Self-referential name headers).
- [ ] Rename `gibd-verifier.md` (Self-referential name headers).
- [ ] Update `tools` section in all agents to reflect local capability (or remove `mcp__`).
- [ ] In ALL files (`agents/*.md`, `workflows/*.md`, `templates/*.md`):
  - [ ] Replace `@~/.claude/get-shit-done/` with `@.docs/prototype/` (or relative paths).
  - [ ] Replace references to `gsd-` agents/workflows with `gibd-` equivalents.
  - [ ] Replace `gsd:command` references (if they are hardcoded instructions) to be generic or point to `gibd` instructions.
  - [ ] **Crucial:** Update `init` command calls (e.g., `gsd-tools.js init`) to either point to a local script if we extract it, or mock/simplify them if we are removing the binary dependency. _Decision:_ For now, keep the command but wrap it or note it as a dependency to eventually replace.

**Acceptance Criteria:**

- All agents utilize `gibd-*` naming in their frontmatter/descriptions.
- Grep for `~/.claude` in `.docs/prototype/` returns 0 hits (except maybe comments explaining origin).
- Grep for `gsd-` returns hits only where it refers to the legacy tool, not the active agent being called.
- Workflows reference the _local_ prototype templates and other workflows.

## Detailed Analysis

### Renaming Strategy (`gsd-` -> `gibd-`)

- **Agents:**
  - `gsd-phase-researcher` -> `gibd-phase-researcher`
  - `gsd-planner` -> `gibd-planner`
  - `gsd-plan-checker` -> `gibd-plan-checker`
  - `gsd-executor` -> `gibd-executor`
  - `gsd-verifier` -> `gibd-verifier`
- **Workflows:**
  - `execute-plan.md` -> (Keep filename, update internal refs)
  - `plan-phase.md` -> (Keep filename, update internal refs)
  - `verify-phase.md` -> (Keep filename, update internal refs)
- **Templates:**
  - `summary.md` -> (Keep filename)
  - `verification-report.md` -> (Keep filename)

### Reference Updates

- **Path Replacements:**
  - Find: `~/.claude/get-shit-done/`
  - Replace: `.docs/prototype/` (or relative path like `../templates/`)
- **Agent Self-References:**
  - Check `name:` field in YAML frontmatter of agent files.
  - Check `<role>` description.
- **Workflow Orchestration:**
  - In `plan-phase.md` and `execute-plan.md`, specifically look for how subagents are spawned.
  - Example: `subagent_type="gsd-planner"` must become `subagent_type="gibd-planner"`.
- **Tooling (`gsd-tools.js`):**
  - References to `node ~/.claude/get-shit-done/bin/gsd-tools.js` abound.
  - **Strategy:** We are _not_ extracting the binary in Phase 1 Tickets 1-3.
  - **Action:** For now, _keep_ the reference if the binary is needed for the prototype to run _on this machine_ (since it exists).
  - **Long-term:** We will need to create a `gibd-tools` or equivalent script in a future phase.
  - **Immediate Fix:** Ensure the path is correct for the USER's machine, or alias it. A better approach for the _blackbox_ is to assume tools are available via a standardized CLI wrapper, or document this dependency clearly. Ticket 4 should flag this: "Review `gsd-tools.js` usage".
