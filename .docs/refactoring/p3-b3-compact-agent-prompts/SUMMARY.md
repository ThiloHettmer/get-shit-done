# Compact Agent Prompts

**Priority:** P3  
**Category:** B - Compressed Formats  
**Estimated Token Savings:** 33-44k initial load  
**Implementation Complexity:** Medium  
**Risk Level:** Medium (affects agent behavior)

## Overview

Agent prompts contain extensive philosophy sections and verbose execution flows. This task distills agents to operational essence while externalizing philosophical context.

## Current Approach

**gsd-executor (7,800 tokens):**
- Role description: 300 tokens
- Philosophy section: 500 tokens (explaining context engineering, quality curves, etc.)
- Execution flow: 3,000 tokens (20 detailed steps)
- Deviation rules: 2,000 tokens (4 rules with extensive examples)
- Checkpoint protocol: 2,000 tokens (detailed patterns)

**Most of this is explanatory content for understanding WHY, not operational WHAT.**

## Proposed Approach

**gsd-executor (3,200 tokens):**

```markdown
<role>GSD executor: atomic PLAN.md execution, per-task commits, SUMMARY creation</role>

<critical_rules>
1. Load STATE.md before anything
2. Execute tasks sequentially
3. Commit after each task: type(phase-plan): description
4. STOP at checkpoints, return structured format
5. Create SUMMARY.md using @templates/summary.md#format
</critical_rules>

<flow>
load_state → load_plan → execute_tasks → create_summary → update_state
</flow>

<deviations>
Auto-fix: bugs, missing-critical, blocking-issues
Ask user: architectural-changes
@references/execution.md#deviation-rules (full details)
</deviations>

<checkpoints>
Types: human-verify (90%), decision (9%), human-action (1%)
@references/execution.md#checkpoints (full protocol)
</checkpoints>
```

**Key changes:**
- Philosophy externalized (referenced, not embedded)
- Execution flow condensed to essentials
- Detailed patterns moved to references
- Keep operational instructions only

## What This Achieves

- **40-50% agent prompt reduction**
- **Faster agent initialization** 
- **Easier maintenance** - update references, not 11 agents
- **Clearer operational focus** - no philosophical bloat

## Token Impact

**Per agent reduction:**
- Executor: 7,800 → 3,200 (savings: 4,600)
- Planner: 8,200 → 3,500 (savings: 4,700)
- Verifier: 4,500 → 2,000 (savings: 2,500)
- Average across 11 agents: ~3,000 tokens saved each

**Initial load savings:** 11 agents × 3,000 = **33k tokens**

**Per-spawn savings:** Minimal (agents loaded once per session), but benefits from G3 (lazy loading)

## Implementation Requirements

1. Identify operational essentials vs explanatory content
2. Extract philosophy/examples to reference docs
3. Rewrite agents with distilled prompts
4. Ensure no loss of critical instructions
5. Test agent behavior thoroughly
6. Update references with extracted content

## Affected Files

**All agent files** (11 total):
- `agents/gsd-executor.md`
- `agents/gsd-planner.md`
- `agents/gsd-verifier.md`
- `agents/gsd-debugger.md`
- `agents/gsd-researcher.md`
- `agents/gsd-plan-checker.md`
- `agents/gsd-roadmapper.md`
- `agents/gsd-codebase-mapper.md`
- `agents/gsd-project-researcher.md`
- `agents/gsd-research-synthesizer.md`
- `agents/gsd-integration-checker.md`

**References (expanded):**
- `get-shit-done/references/execution.md` - Deviation rules, checkpoint protocol
- `get-shit-done/references/planning.md` - Planning philosophy, goal-backward methodology

## Success Criteria

- [ ] Agent prompts distilled to operational essentials
- [ ] Philosophy/examples moved to references
- [ ] No regression in agent behavior
- [ ] Token usage reduced by target amount
- [ ] Easier to maintain operational instructions

## Dependencies

Works extremely well with:
- D1 (unified agent base) - both reduce agent verbosity
- D2 (consolidated references) - target for extracted content
- G3 (lazy agent loading) - compact core enables better lazy loading

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
