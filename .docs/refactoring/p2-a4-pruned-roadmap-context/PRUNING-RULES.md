# ROADMAP Pruning Rules

## Pruning Strategy

**Principle:** Show enough context to orient agents without overwhelming them.

### What to Include in ROADMAP-CURRENT.md

1. **Header** (always include):
   - Milestone name
   - Overview paragraph
   - Phase numbering note

2. **Previous Phase** (abbreviated):
   - Phase number + name
   - Status: ✓ COMPLETE
   - Brief summary (1-2 sentences) of what was built
   - NO plans list, NO full details

3. **Current Phase** (full details):
   - Phase number + name + status marker (← CURRENT)
   - Full goal
   - Full dependencies
   - Full requirements
   - Full success criteria
   - Full plans list with checkboxes

4. **Next Phase** (abbreviated):
   - Phase number + name
   - Brief summary of what's planned
   - NO plans list, NO full details

5. **Progress Table** (filtered):
   - Only show: previous phase + current phase + next phase
   - Omit other phases

### Edge Cases

**First phase (no previous):**
- Skip previous phase section
- Show current (full) + next (brief)

**Last phase (no next):**
- Show previous (brief) + current (full)
- Skip next phase section

**Single phase milestone:**
- Show only current phase (full)
- Add note: "Single phase milestone"

**Decimal phases (2.1 between 2 and 3):**
- Previous = 2, Current = 2.1, Next = 2.2 or 3
- Respect numeric ordering including decimals

## Pruning Algorithm

```bash
# Input: ROADMAP.md, CURRENT_PHASE_NUM
# Output: ROADMAP-CURRENT.md

1. Extract header section (milestone, overview) → include in output

2. Parse all phase entries from ROADMAP.md

3. Determine adjacent phases:
   prev_phase = CURRENT_PHASE_NUM - 1 (or largest decimal before current)
   next_phase = CURRENT_PHASE_NUM + 1 (or smallest phase after current)

4. For prev_phase:
   - Extract: phase number, name, status
   - Generate brief summary from goal (first sentence)
   - Format as abbreviated entry

5. For current_phase:
   - Extract ALL details unchanged
   - Add " ← CURRENT" marker to heading

6. For next_phase:
   - Extract: phase number, name
   - Generate brief summary from goal (first sentence)
   - Format as abbreviated entry

7. Create filtered progress table with 3 rows

8. Write ROADMAP-CURRENT.md
```

## Format Examples

### Abbreviated Phase (Previous/Next)

```markdown
### Phase 4: Database Layer ✓ COMPLETE
Built PostgreSQL schema with Prisma ORM, user/project models, and migrations.
```

### Full Phase (Current)

```markdown
### Phase 5: Core Features ← CURRENT
**Goal:** Implement main application features (task management, user dashboard, project workflows)
**Depends on:** Phase 4 (database schema)
**Requirements:** [REQ-05, REQ-06, REQ-07]
**Success Criteria:**
  1. User can create and manage tasks
  2. Dashboard shows project overview
  3. Workflows execute correctly
**Plans:** 3 plans

Plans:
- [ ] 05-01-PLAN.md — Task management API and UI
- [ ] 05-02-PLAN.md — Dashboard implementation
- [ ] 05-03-PLAN.md — Workflow engine
```

### Filtered Progress Table

```markdown
## progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 4. Database Layer | 2/2 | Complete | 2026-01-20 |
| 5. Core Features | 1/3 | In progress | - |
| 6. Polish & Testing | 0/2 | Not started | - |
```

## When to Regenerate

ROADMAP-CURRENT.md should be regenerated:
- After each plan completes (current phase progress updates)
- When transitioning to next phase
- When ROADMAP.md structure changes

**Who regenerates:**
- Execute-phase workflow after plan completion
- Roadmapper when creating/updating ROADMAP.md
- Transition workflow when moving between phases

## Maintenance Notes

- ROADMAP-CURRENT.md is derived, not manually edited
- Full ROADMAP.md remains source of truth
- Pruned version is generated automatically
- Both files committed to git for transparency
