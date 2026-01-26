# Incremental State Loading

**Priority:** P1  
**Category:** A - Selective Context Loading  
**Estimated Token Savings:** 1.5-3k per phase  
**Implementation Complexity:** Low  
**Risk Level:** Low

## Overview

STATE.md grows unbounded as the project progresses, with every completed plan adding to the "Decisions Made" table. This task implements a trimmed state file that loads only recent context, with full history archived separately.

## Current Behavior

STATE.md contains:
- Current position (100 tokens)
- ALL decisions from all phases (grows 50-100 tokens per plan)
- ALL concerns ever raised (grows 30-50 tokens per issue)
- Complete session history (50-100 tokens)

**Token growth:** 200 tokens → 400 tokens → 600 tokens → 800 tokens as project progresses

Loaded by every agent (15-25 times per phase).

## Proposed Structure

```yaml
# .planning/STATE.md (trimmed - 150-200 tokens)
phase: 5
recent_decisions: [last 5 decisions only]
active_concerns: [unresolved issues only]
current_position: [current phase details]

# .planning/STATE-ARCHIVE.md (rarely loaded - 400+ tokens)
phase_history: [complete history of phases 1-3]
all_decisions: [all decisions ever made]
resolved_concerns: [historical issues]
```

## What This Achieves

- **Prevents token bloat** as project grows
- **Keeps recent context** that's actually relevant
- **Maintains history** in archive for occasional reference
- **Backwards compatible** - existing projects can migrate

## Token Impact

- Current: 400-800 tokens per load × 20 loads = 8-16k per phase (late project)
- Optimized: 150-200 tokens per load × 20 loads = 3-4k per phase
- **Savings: 5-12k per phase (increases with project size)**

## Implementation Requirements

1. Define "recent" criteria (last 2 phases, last 5 decisions, unresolved concerns only)
2. Implement STATE.md trimming logic in executor/orchestrator
3. Create STATE-ARCHIVE.md when archiving old content
4. Update state readers to check archive if needed
5. Migration script for existing projects

## Affected Files

- `.planning/STATE.md` (new trimmed format)
- `.planning/STATE-ARCHIVE.md` (new archive file)
- `agents/gsd-executor.md` - Update state writing logic
- `get-shit-done/workflows/execute-phase.md` - Update state reading
- `get-shit-done/templates/state.md` - Update template

## Success Criteria

- [ ] STATE.md stays under 200 tokens regardless of project size
- [ ] Archive file captures full history
- [ ] Agents can access archive when needed
- [ ] No loss of important context
- [ ] Token usage reduced by target amount

## Dependencies

None - can be implemented independently

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
