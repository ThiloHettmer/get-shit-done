# Shared Context Pool

**Priority:** P3  
**Category:** G - Agent Architecture Changes  
**Estimated Token Savings:** 3.2-4.8k per phase  
**Implementation Complexity:** High  
**Risk Level:** Medium (orchestrator becomes stateful)

## Overview

Each agent currently loads STATE.md, config.json independently. This task has the orchestrator maintain shared context and inject only deltas to agents.

## Current Behavior

**Every agent loads independently:**
```javascript
// Agent 1 (executor for plan 01-01)
loads STATE.md (300 tokens)
loads config.json (150 tokens)
loads PROJECT.md (500 tokens)

// Agent 2 (executor for plan 01-02)  
loads STATE.md (300 tokens) - duplicate!
loads config.json (150 tokens) - duplicate!
loads PROJECT.md (500 tokens) - duplicate!

// Agent 3 (verifier)
loads STATE.md (300 tokens) - duplicate!
loads config.json (150 tokens) - duplicate!
loads PROJECT.md (500 tokens) - duplicate!
```

**Total: 950 tokens × 8 agents = 7,600 tokens of duplicate loading**

## Proposed Behavior

**Orchestrator maintains shared pool:**

```javascript
// Orchestrator loads once per phase
const sharedContext = {
  project: read('PROJECT.md'),          // 500 tokens
  state: read('STATE.md'),              // 300 tokens
  config: read('config.json'),          // 150 tokens
  lastUpdate: timestamp
}

// Agent prompt includes only deltas
spawnExecutor({
  prompt: `
    Execute plan 01-02
    
    Delta since last agent:
    - New decision: Use jose library for JWT
    - Transition: Phase 01 → Phase 02
    
    [Full context available via @shared-context ref if needed]
  `,
  sharedContext: contextRef
})
```

**Agent receives:**
- Delta: 100-200 tokens (what changed)
- Reference to full context: 50 tokens
- Loads full context only if needed

## What This Achieves

- **Eliminates redundant loading** of static context
- **Orchestrator becomes stateful** - manages shared state
- **Agents get focused deltas** - only what changed
- **Reduced token load** per agent spawn

## Token Impact

**Per agent:**
- Current: 950 tokens (STATE + config + PROJECT)
- Optimized: 150-250 tokens (delta only)
- Savings: 700-800 tokens per agent

**Per phase (8 agents):**
- **Savings: 5.6-6.4k tokens**

**Tradeoff:** Orchestrator becomes more complex, needs to track changes

## Implementation Requirements

1. Implement shared context pool in orchestrator
2. Define delta format (what changed since last agent)
3. Implement context reference mechanism
4. Update orchestrator to maintain pool throughout phase
5. Update agents to accept delta + reference
6. Add fallback for agents that need full context
7. Test with state changes during execution

## Affected Files

**Update orchestrator:**
- `get-shit-done/workflows/execute-phase.md` - Maintain shared pool
- Add context pool management logic

**Update agents to accept deltas:**
- `agents/gsd-executor.md`
- `agents/gsd-planner.md`
- `agents/gsd-verifier.md`

**New utilities:**
- Context delta calculator
- Context pool manager

## Success Criteria

- [ ] Shared context pool implemented
- [ ] Delta format defined and working
- [ ] Orchestrator maintains pool correctly
- [ ] Agents work with deltas
- [ ] Fallback to full context works
- [ ] Token usage reduced by target amount
- [ ] No regression in agent behavior

## Dependencies

**Conflicts with:**
- E1 (batch agent communication) - both modify how context is passed to agents
- Choose one approach based on which is more effective

**Works with:**
- A3 (incremental state loading) - keeps shared STATE.md small

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
