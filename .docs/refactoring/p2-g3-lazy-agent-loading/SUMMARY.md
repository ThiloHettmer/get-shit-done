# Lazy Agent Loading

**Priority:** P2  
**Category:** G - Agent Architecture Changes  
**Estimated Token Savings:** 24-40k per phase  
**Implementation Complexity:** High  
**Risk Level:** Medium

## Overview

Currently, agent definitions load upfront with full 7-8k token prompts including all protocols. This task loads agent core (~2k tokens) and lazy-loads sub-protocols only when triggered.

## Current Behavior

**gsd-executor loaded with:**
- Core role and execution flow (~2,000 tokens)
- Deviation rules (~2,000 tokens) - used only when deviation found
- Checkpoint protocol (~2,000 tokens) - used only when checkpoint hit
- TDD cycle (~1,500 tokens) - used only for TDD tasks
- Git integration (~1,500 tokens) - always used

**Total: ~7,800 tokens per executor spawn**

Most spawns never use deviation rules or checkpoints, yet load them anyway.

## Proposed Behavior

**Agent spawn loads core:**
```markdown
<role>Execute PLAN.md atomically</role>
<critical_steps>
1. load_state → read STATE.md
2. execute_tasks → run each task
3. commit_task → atomic commit per task
4. create_summary → write SUMMARY.md
</critical_steps>
<always_load>@protocols/git-integration.md</always_load>
```

**Sub-protocols loaded on-trigger:**
```javascript
// When deviation detected
if (discoveredWork !== inPlan) {
  load('@protocols/deviation-handling.md')  // 2k tokens on-demand
}

// When checkpoint hit
if (task.type.startsWith('checkpoint')) {
  load('@protocols/checkpoint-return.md')   // 2k tokens on-demand
}

// When TDD task
if (task.tdd === true) {
  load('@protocols/tdd-cycle.md')           // 1.5k tokens on-demand
}
```

## What This Achieves

- **Massive token reduction** for typical agent spawns
- **Just-in-time loading** of specialized protocols
- **Faster agent initialization** with minimal core
- **No quality loss** - protocols loaded when needed

## Token Impact

**Typical executor (no checkpoints, no TDD, no deviations):**
- Current: 7,800 tokens
- Optimized: 2,000 (core) + 1,500 (git) = 3,500 tokens
- **Savings: 4,300 tokens per spawn**

**With 8-10 agent spawns per phase:**
- **34-43k tokens saved per phase**

**Executor with checkpoint:**
- Optimized: 3,500 + 2,000 (checkpoint) = 5,500 tokens
- Still saves 2,300 tokens

## Implementation Requirements

1. Split agent prompts into core + protocol modules
2. Create protocol directory structure
3. Implement dynamic protocol loading mechanism
4. Define trigger conditions for each protocol
5. Update agent logic to request protocols when needed
6. Test all agent paths (with/without protocols)
7. Ensure no regression in agent behavior

## Affected Files

**Create protocol modules:**
```
get-shit-done/protocols/
├── deviation-handling.md
├── checkpoint-return.md
├── tdd-cycle.md
├── continuation-handling.md
└── authentication-gates.md
```

**Update agents:**
- `agents/gsd-executor.md` - Split into core + triggers
- `agents/gsd-planner.md` - Split planning protocols
- `agents/gsd-verifier.md` - Split verification protocols

**Update orchestrators:**
- `get-shit-done/workflows/execute-phase.md` - Support protocol loading

## Success Criteria

- [ ] Protocol modules created and tested
- [ ] Agents load minimal core on spawn
- [ ] Protocols loaded dynamically when triggered
- [ ] All agent behaviors maintained
- [ ] Token usage reduced by target amount
- [ ] No regression in execution quality

## Dependencies

Works well with D2 (consolidated references) - protocols could live in references

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
