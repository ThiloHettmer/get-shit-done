# Progressive Detail Loading

**Priority:** P3  
**Category:** E - Execution Pattern Changes  
**Estimated Token Savings:** 1-1.5k per plan  
**Implementation Complexity:** High  
**Risk Level:** Medium (requires state management)

## Overview

Currently, executors load complete PLAN.md with all task details upfront. This task loads plan skeleton first, then loads task details on-demand as each task is executed.

## Current Behavior

**Executor loads full plan immediately:**

```xml
<objective>Build authentication system</objective>

<tasks>
<task type="auto">
  <name>Task 1: Create User model</name>
  <files>src/models/user.ts</files>
  <action>
    Create User model in Prisma schema with:
    - id (UUID, primary key)
    - email (unique, lowercase)
    - passwordHash (bcrypt, cost 10)
    [300 tokens of detailed instructions]
  </action>
  <verify>prisma db push && npm test</verify>
  <done>User model exists in schema, migrations run, tests pass</done>
</task>

<task type="auto">
  <name>Task 2: Registration endpoint</name>
  [400 tokens of instructions loaded but not used yet]
</task>

<task type="auto">
  <name>Task 3: Login endpoint</name>
  [400 tokens of instructions loaded but not used yet]
</task>
</tasks>
```

**Token load:** 3,000-4,000 tokens (full plan)
**Initially used:** ~1,000 tokens (objective + task 1)

## Proposed Behavior

**Phase 1: Load skeleton (800 tokens):**

```xml
<objective>Build authentication system</objective>
<tasks>
  <task id="1" type="auto">Create User model</task>
  <task id="2" type="auto">Registration endpoint</task>
  <task id="3" type="auto">Login endpoint</task>
</tasks>
```

**Phase 2: When executing task 1, load details (300 tokens):**

```xml
@plan#task-1-details
<files>src/models/user.ts</files>
<action>[detailed instructions]</action>
<verify>prisma db push && npm test</verify>
<done>User model exists, tests pass</done>
```

**Phase 3: After task 1 complete, load task 2 details:**

```xml
@plan#task-2-details
[next task instructions]
```

## What This Achieves

- **Reduces initial context load** by 60-70%
- **Just-in-time detail loading** - only what's currently needed
- **Better focus** - executor sees current task clearly
- **Complex state management** - requires tracking position

## Token Impact

**Per plan:**
- Current: 3,000-4,000 tokens (full plan)
- Optimized: 800 (skeleton) + 300-400 per task = 1,700-2,400 tokens total
- **Savings: 1,300-1,600 tokens per plan**

**Per phase (3-5 plans):**
- **Savings: 4-8k tokens**

**Tradeoff:** More complex loading logic, requires splitting PLAN.md into sections

## Implementation Requirements

1. Define skeleton PLAN format (objectives + task IDs only)
2. Implement task detail sections in PLAN.md
3. Update planner to create both skeleton and detail sections
4. Update executor to load skeleton first, details on-demand
5. Add state tracking for current task position
6. Test execution with progressive loading
7. Ensure no loss of context between tasks

## Affected Files

**Update planner:**
- `agents/gsd-planner.md` - Generate skeleton + detail sections

**Update executor:**
- `agents/gsd-executor.md` - Progressive loading logic
- Add task position tracking

**Update templates:**
- `get-shit-done/templates/phase-prompt.md` - Show progressive format

**Update workflows:**
- `get-shit-done/workflows/execute-plan.md` - Support progressive loading

## Success Criteria

- [ ] Skeleton PLAN format defined
- [ ] Planner generates both skeleton and details
- [ ] Executor loads progressively
- [ ] Task details loaded just-in-time
- [ ] No regression in execution quality
- [ ] Token usage reduced by target amount
- [ ] State tracking works correctly

## Dependencies

**Requires:**
- A1 (lazy template loading) - same section-loading mechanism

**Conflicts with:**
- E1 (batch agent communication) - orchestrator can't pre-load trimmed context if details aren't loaded

Consider which provides more value before implementing both.

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
