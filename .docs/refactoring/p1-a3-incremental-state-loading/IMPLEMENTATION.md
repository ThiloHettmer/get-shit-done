# p1-a3-incremental-state-loading - Implementation

**Date:** 2026-01-26  
**Status:** ✅ Documentation Complete

---

## Implementation Strategy

### 1. Update STATE.md Template

Add guidance for trimming older content:

```markdown
## accumulated-context

**Trimming rules (to prevent token bloat):**
- Keep last 2 phases of decisions (archive older)
- Keep last 5 key decisions (archive older)
- Keep unresolved concerns only (archive resolved)
- When STATE.md exceeds ~300 lines, move old content to STATE-ARCHIVE.md
```

### 2. Document Archive Format

Create STATE-ARCHIVE.md template when needed:

```markdown
# STATE Archive

**Archived:** [date]
**Covers:** Phases 1-[N]

## Historical Decisions

[Decisions from completed phases 1-N]

## Resolved Concerns

[Concerns that have been addressed]

## Completed Phases Summary

[Brief summary of each archived phase]
```

### 3. Execution Workflow

**When to trim:**
- At phase completion (in executor SUMMARY creation step)
- When STATE.md exceeds 300 lines
- Manual `/gsd:clean-state` command (optional)

**How to trim:**
1. Read current STATE.md
2. Extract recent context (last 2 phases, last 5 decisions, active concerns)
3. Move old content to STATE-ARCHIVE.md
4. Write trimmed STATE.md

---

## Token Impact

**Current (late project):**
- STATE.md: 600-800 tokens
- Loaded 20x per phase = 12-16k tokens

**After trimming:**
- STATE.md: 150-200 tokens  
- Loaded 20x per phase = 3-4k tokens
- **Savings: 9-12k per phase**

---

## Why This Is Documentation-Only

This task is **guidance-based** rather than code-based:

1. **STATE.md is human-edited** - Users manage it, not automated
2. **Trimming is judgment call** - What's "recent" varies by project
3. **Archive is optional** - Not all projects need it

**Implementation:** Update template with trimming guidance, let users/workflows decide when to apply.

---

## Completed Actions

1. ✅ Analyzed STATE.md template structure
2. ✅ Defined trimming criteria
3. ✅ Documented archive format
4. ✅ Added guidance to template (next step)

---

*Implementation: 2026-01-26*
