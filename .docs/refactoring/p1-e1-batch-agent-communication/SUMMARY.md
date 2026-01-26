# Batch Agent Communication

**Priority:** P1  
**Category:** E - Execution Pattern Changes  
**Estimated Token Savings:** 15-40k per phase  
**Implementation Complexity:** High  
**Risk Level:** Medium

## Overview

Currently, each executor agent loads full plan + state + context files independently. This task has the orchestrator pre-load and trim context once, then pass condensed context to all agents in the wave.

## Current Behavior

**Per executor agent:**
1. Load PLAN.md (2,000-4,000 tokens)
2. Load STATE.md (200-400 tokens)
3. Load PROJECT.md (300-800 tokens)
4. Load ROADMAP.md (400-1,000 tokens)
5. Load config.json (100-200 tokens)
6. Load referenced SUMMARYs (2,000-5,000 tokens)

**Total per agent:** 5,000-11,000 tokens
**With 3-5 executors:** 15,000-55,000 tokens of repeated loading

## Proposed Behavior

**Orchestrator does once:**
```javascript
// Read files once
const plan = readFile('01-02-PLAN.md')
const state = readFile('STATE.md')
const project = readFile('PROJECT.md')

// Extract only what executors need
const trimmedContext = {
  plan_tasks: extractTasks(plan),                    // Just <tasks> section
  plan_objective: extractObjective(plan),            // Just objective
  current_phase: state.current_position,             // Not full state
  recent_decisions: state.decisions.slice(-5),       // Last 5, not all
  project_vision: project.goals,                     // Core vision only
  constraints: extractConstraints(project)           // Key constraints
}

// Pass to all agents (70% smaller than full files)
spawnExecutors(trimmedContext)
```

## What This Achieves

- **Eliminates redundant file reads** across parallel agents
- **Reduces context bloat** by passing only relevant excerpts
- **Orchestrator becomes smarter** - does preprocessing
- **Agents stay focused** - get exactly what they need

## Token Impact

- Current per agent: 5-11k tokens
- Optimized per agent: 2-4k tokens (trimmed context)
- Per phase (3-5 agents): **15-40k tokens saved**

## Implementation Requirements

1. Implement context extraction utilities (extract tasks, objectives, etc.)
2. Update orchestrator to pre-load and trim context
3. Modify agent prompts to accept trimmed context format
4. Ensure trimmed context is sufficient for execution
5. Add fallback mechanism if agents need additional context
6. Test execution quality with trimmed context

## Affected Files

- `get-shit-done/workflows/execute-phase.md` - Orchestrator logic
- `agents/gsd-executor.md` - Accept trimmed context
- New utility module for context extraction

## Success Criteria

- [ ] Orchestrator loads shared files once per wave
- [ ] Context extraction utilities implemented and tested
- [ ] Agents successfully execute with trimmed context
- [ ] No regression in execution quality
- [ ] Token usage reduced by target amount
- [ ] Error handling for missing context

## Dependencies

None - can be implemented independently, but benefits from A2 (context-aware loading)

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
