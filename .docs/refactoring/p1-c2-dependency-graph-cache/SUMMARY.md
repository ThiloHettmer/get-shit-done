# Dependency Graph Cache

**Priority:** P1  
**Category:** C - Intelligent Caching  
**Estimated Token Savings:** 8-12k per planning phase  
**Implementation Complexity:** Medium  
**Risk Level:** Low

## Overview

Currently, every planner agent builds the dependency graph from scratch by scanning all SUMMARY frontmatter (20-40 files). This task precomputes and caches the dependency graph in STATE.md.

## Current Behavior

**Planner workflow:**
1. Scan all SUMMARY.md files (20-40 files)
2. Extract frontmatter from each (200-400 tokens × 30 = 6-12k tokens)
3. Build dependency graph:
   - Which phases provide what
   - Which phases depend on what
   - What tech stack is available
   - What patterns are established
4. Determine what context to load for current plan

**Every planning phase repeats this scan.**

## Proposed Behavior

**STATE.md addition:**
```yaml
dependency_graph:
  "01": {provides: ["auth-system", "user-model"], tech: ["jose", "bcrypt"]}
  "02": {requires: ["01"], provides: ["dashboard"], tech: ["react", "tailwind"]}
  "03": {requires: ["01", "02"], provides: ["api-layer"], tech: ["prisma"]}
  "04": {requires: ["03"], provides: ["payments"], tech: ["stripe"]}
  "05": {requires: ["03"], provides: ["admin-panel"], affects: ["06"]}

tech_stack_available: ["jose", "bcrypt", "react", "tailwind", "prisma", "stripe"]
patterns_established: ["JWT auth", "Prisma ORM", "API routes"]
```

**Planner reads graph (500 tokens), knows immediately:**
- What phases affect current phase
- What tech is available
- What patterns to follow
- Which SUMMARYs to load (only relevant ones)

**Updated by executor** after each plan completes.

## What This Achieves

- **Avoids redundant SUMMARY scanning** every planning phase
- **Faster planning** - immediate context awareness
- **Selective SUMMARY loading** - only load what's relevant
- **Incremental updates** - maintained as project progresses

## Token Impact

- Current: Scan 30 SUMMARYs × 200-400 tokens = 6-12k per planning phase
- Optimized: Load graph from STATE (500 tokens), load 2-4 relevant SUMMARYs (800-1,600 tokens)
- **Savings: 5-10k tokens per planning phase**

## Implementation Requirements

1. Define dependency graph schema (YAML format in STATE.md)
2. Implement graph builder (runs once at project start, updates incrementally)
3. Update executor to write graph entry after each plan completes
4. Update planner to read and use graph for selective loading
5. Implement graph query utilities (find dependencies, find providers, etc.)
6. Migration for existing projects (scan and build graph once)

## Affected Files

- `.planning/STATE.md` - Add dependency_graph section
- `agents/gsd-executor.md` - Update graph after plan completion
- `agents/gsd-planner.md` - Use graph for selective loading
- `get-shit-done/templates/state.md` - Update template
- New utility module for graph operations

## Success Criteria

- [ ] Dependency graph schema defined
- [ ] Graph maintained in STATE.md
- [ ] Planner uses graph to load only relevant SUMMARYs
- [ ] Graph updated after each plan execution
- [ ] Token usage reduced by target amount
- [ ] No regression in planning quality

## Dependencies

Works well with A3 (incremental state loading) - both modify STATE.md

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
