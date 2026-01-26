# Context-Aware Reference Loading

**Priority:** P0 (Quick Win)  
**Category:** A - Selective Context Loading  
**Estimated Token Savings:** 5-8k per executor spawn  
**Implementation Complexity:** Low  
**Risk Level:** Low

## Overview

Currently, executor agents load all reference files unconditionally (checkpoints, TDD, git, continuation). This task implements conditional loading based on plan characteristics, loading only relevant references.

## Current Behavior

Every executor agent loads:
- `checkpoints.md` (~3k tokens)
- `tdd.md` (~3k tokens)
- `git-integration.md` (~3k tokens)
- `continuation-format.md` (~2k tokens)

**Total: ~11k tokens per executor spawn**

Only ~30% of this content is typically used by any given executor.

## Proposed Behavior

```javascript
// Conditional loading based on plan metadata
if (plan.has_checkpoints) load('checkpoints.md')      // Only if needed
if (plan.type === 'tdd') load('tdd.md')              // Only for TDD plans
if (plan.gap_closure) load('verification-patterns.md') // Only for gap closure
// Always load git-integration.md (used by all)
```

## What This Achieves

- **Reduces reference overhead** by 70-80% for most executors
- **Smarter context usage** - agents only see relevant guidance
- **No quality loss** - agents still get all necessary information
- **Simple implementation** - straightforward conditional logic

## Token Impact

- Current: ~11k tokens per executor × 3-5 executors = 33-55k per phase
- Optimized: ~3-4k tokens per executor × 3-5 executors = 9-20k per phase
- **Savings: 24-35k tokens per phase (5-8k per executor)**

## Implementation Requirements

1. Add metadata flags to PLAN.md frontmatter (already exists: `autonomous`, `type`, `gap_closure`)
2. Implement conditional loading logic in executor agent prompt
3. Update executor workflow to pass plan metadata
4. Ensure git-integration.md is always loaded (minimal, always relevant)

## Affected Files

- `agents/gsd-executor.md` - Add conditional loading logic
- `get-shit-done/workflows/execute-plan.md` - Pass plan metadata
- Reference files remain unchanged

## Success Criteria

- [ ] Executor only loads relevant reference files
- [ ] Plans with checkpoints load checkpoint reference
- [ ] TDD plans load TDD reference
- [ ] Gap closure plans load verification patterns
- [ ] No regression in execution quality
- [ ] Token usage reduced by target amount

## Dependencies

None - can be implemented independently

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
