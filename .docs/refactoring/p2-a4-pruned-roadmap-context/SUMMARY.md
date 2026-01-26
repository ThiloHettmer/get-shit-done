# Pruned Roadmap Context

**Priority:** P2  
**Category:** A - Selective Context Loading  
**Estimated Token Savings:** 3-6k per phase  
**Implementation Complexity:** Low  
**Risk Level:** Low

## Overview

ROADMAP.md contains all phases with full details. Agents typically only need current + adjacent phases. This task creates a pruned view with only relevant context.

## Current Behavior

ROADMAP.md loaded by agents contains:
- Milestone header (100 tokens)
- All completed phases with full details (200-400 tokens each × 3-5)
- Current phase with full details (300-500 tokens)
- All future phases with full details (200-400 tokens each × 3-5)

**Total: 2,000-5,000 tokens** depending on project size

Most agents only need to know:
- Where they are (current phase)
- What came before (dependencies)
- What's coming next (context)

## Proposed Structure

```markdown
# .planning/ROADMAP-CURRENT.md (600-1,000 tokens)
## Milestone: v1.0 - MVP Launch

### Phase 4: Database Layer ✓ COMPLETE
Brief summary of what was built

### Phase 5: Core Features ← CURRENT
**Goal:** [full details for current phase]
**Plans:** [full plan list]
**Dependencies:** Phase 4 (database schema)

### Phase 6: Polish & Testing
Brief summary of what's planned

# .planning/ROADMAP.md (full - loaded only by orchestrator)
[Complete roadmap with all phase details]
```

## What This Achieves

- **Focused context** - agents see only relevant phases
- **Prevents token bloat** as project grows
- **Maintains full roadmap** for human reference
- **Easy navigation** - current phase prominently marked

## Token Impact

**Early project (3 phases):**
- Full: 1,500 tokens
- Pruned: 800 tokens
- Savings: 700 tokens

**Late project (10 phases):**
- Full: 4,500 tokens
- Pruned: 1,000 tokens
- Savings: 3,500 tokens

**Per phase (loaded 10 times):**
- **Savings: 7k-35k tokens** (scales with project size)

## Implementation Requirements

1. Define "adjacent" criteria (current ± 1 phase, or current + all dependencies)
2. Implement roadmap pruning logic
3. Update roadmap writer to maintain both versions
4. Update agents to load ROADMAP-CURRENT.md instead of ROADMAP.md
5. Orchestrator still loads full ROADMAP.md for complete view
6. Migration for existing projects

## Affected Files

**Create:**
- `.planning/ROADMAP-CURRENT.md` (pruned view)

**Update readers:**
- `agents/gsd-planner.md` - Load pruned roadmap
- `agents/gsd-executor.md` - Load pruned roadmap
- `agents/gsd-verifier.md` - Load pruned roadmap

**Orchestrator keeps full:**
- `get-shit-done/workflows/execute-phase.md` - Still loads full ROADMAP.md

**Update writers:**
- Roadmap update logic - Maintain both files

**Templates:**
- `get-shit-done/templates/roadmap.md` - Note pruning behavior

## Success Criteria

- [ ] Pruned roadmap format defined
- [ ] Both files maintained automatically
- [ ] Agents load only pruned version
- [ ] Current phase context fully available
- [ ] No loss of necessary information
- [ ] Token usage reduced by target amount

## Dependencies

None - can be implemented independently

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
