# Planner Agent Analysis

This document analyzes the existing GSD planner agent system to understand what needs to be isolated for the prototype.

## Overview

The planner agent is part of a three-tier architecture:

1. **Command** (`commands/gsd/plan-phase.md`) - Entry point, defines tools and agent reference
2. **Workflow** (`get-shit-done/workflows/plan-phase.md`) - Orchestration logic
3. **Agent** (`agents/gsd-planner.md`) - Core planning logic

## Files Analyzed

| File                                    | Size        | Purpose                                                  |
| --------------------------------------- | ----------- | -------------------------------------------------------- |
| `agents/gsd-planner.md`                 | 1,158 lines | Core planner agent with role, philosophy, execution flow |
| `agents/gsd-plan-checker.md`            | 623 lines   | Verifies plans before execution                          |
| `commands/gsd/plan-phase.md`            | 45 lines    | Command entry point                                      |
| `get-shit-done/workflows/plan-phase.md` | 377 lines   | Orchestration workflow                                   |
| `get-shit-done/bin/gsd-tools.js`        | 4,598 lines | CLI utility (113 functions)                              |

---

## Current Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ User Invokes: /gsd:plan-phase [phase]                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Command: commands/gsd/plan-phase.md                             │
│ - Defines allowed tools: Read, Write, Bash, Glob, Grep, Task,  │
│   WebFetch, mcp__context7__*                                    │
│ - References agent: gsd-planner                                 │
│ - References workflow: plan-phase.md                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Workflow: get-shit-done/workflows/plan-phase.md                 │
│                                                                 │
│ Steps:                                                          │
│ 1. Initialize (load context via gsd-tools init)                 │
│ 2. Parse arguments                                              │
│ 3. Validate phase                                               │
│ 4. Load CONTEXT.md (user decisions)                             │
│ 5. Handle research (spawn gsd-phase-researcher if needed)       │
│ 6. Check existing plans                                         │
│ 7. Spawn gsd-planner agent ◄── CORE AGENT                       │
│ 8. Handle planner return                                        │
│ 9. Spawn gsd-plan-checker agent                                 │
│ 10. Handle checker return                                       │
│ 11. Revision loop (max 3 iterations)                            │
│ 12. Present final status                                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                      ┌───────┴───────┐
                      ▼               ▼
┌────────────────────────────┐  ┌─────────────────────────────────┐
│ gsd-planner                │  │ gsd-plan-checker                │
│ (agents/gsd-planner.md)    │  │ (agents/gsd-plan-checker.md)    │
│                            │  │                                 │
│ Creates PLAN.md files      │  │ Verifies plan quality           │
│ Returns structured output  │  │ Returns PASSED or ISSUES FOUND  │
└────────────────────────────┘  └─────────────────────────────────┘
```

---

## Planner Agent Deep Dive

### Key Sections in `gsd-planner.md`

| Section                | Lines     | Purpose                                    |
| ---------------------- | --------- | ------------------------------------------ |
| `<role>`               | 1-26      | Agent identity and responsibilities        |
| `<context_fidelity>`   | 28-55     | User decision handling (CRITICAL)          |
| `<philosophy>`         | 57-95     | Solo dev workflow, plans as prompts        |
| `<discovery_levels>`   | 97-126    | Research depth determination               |
| `<task_breakdown>`     | 128-212   | Task anatomy, types, sizing                |
| `<dependency_graph>`   | 214-281   | Needs/creates, waves, parallelism          |
| `<scope_estimation>`   | 283-333   | Context budget (50% target)                |
| `<plan_format>`        | 335-442   | PLAN.md structure with YAML frontmatter    |
| `<goal_backward>`      | 444-541   | Goal-backward methodology                  |
| `<checkpoints>`        | 543-630   | Human-verify, decision, human-action types |
| `<tdd_integration>`    | 632-676   | TDD plan handling                          |
| `<gap_closure_mode>`   | 678-736   | Planning from verification gaps            |
| `<revision_mode>`      | 738-828   | Revising plans based on checker feedback   |
| `<execution_flow>`     | 830-1066  | Step-by-step execution (13 steps)          |
| `<structured_returns>` | 1068-1122 | Output formats                             |
| `<success_criteria>`   | 1124-1158 | Completion checklists                      |

### Execution Flow Steps

1. **load_project_state** - Load planning context via `gsd-tools.js init`
2. **load_codebase_context** - Load relevant codebase maps
3. **identify_phase** - Read ROADMAP.md, find phase to plan
4. **mandatory_discovery** - Apply discovery level protocol (Level 0-3)
5. **read_project_history** - Load phase history digest, select relevant phases
6. **gather_phase_context** - Load CONTEXT.md, RESEARCH.md, DISCOVERY.md
7. **break_into_tasks** - Decompose phase into tasks
8. **build_dependency_graph** - Map needs/creates for each task
9. **assign_waves** - Calculate wave numbers from dependencies
10. **group_into_plans** - Group tasks into 2-3 task plans
11. **derive_must_haves** - Apply goal-backward methodology
12. **estimate_scope** - Verify context budget
13. **confirm_breakdown** - Present breakdown, wait for confirmation
14. **write_phase_prompt** - Write PLAN.md files
15. **validate_plan** - Use gsd-tools to validate structure
16. **update_roadmap** - Update ROADMAP.md with plan list
17. **git_commit** - Commit planning docs
18. **offer_next** - Return structured outcome

---

## External Dependencies

### 1. gsd-tools.js Functions Used by Planner

| Function                                    | Purpose                                    |
| ------------------------------------------- | ------------------------------------------ |
| `init plan-phase <phase>`                   | Load all planning context, returns JSON    |
| `roadmap get-phase <N>`                     | Get phase info from ROADMAP.md             |
| `history-digest`                            | Aggregate SUMMARY.md data from past phases |
| `state-snapshot`                            | Structured parse of STATE.md               |
| `frontmatter validate <path> --schema plan` | Validate PLAN.md frontmatter               |
| `verify plan-structure <path>`              | Verify PLAN.md structure                   |
| `commit <msg> --files <paths>`              | Git commit planning docs                   |

### 2. Context Files Read

| File                         | Purpose                                       |
| ---------------------------- | --------------------------------------------- |
| `.planning/STATE.md`         | Current project state                         |
| `.planning/ROADMAP.md`       | Phase list and goals                          |
| `.planning/REQUIREMENTS.md`  | Project requirements                          |
| `.planning/codebase/*.md`    | Codebase analysis (STACK, ARCHITECTURE, etc.) |
| `{phase_dir}/*-CONTEXT.md`   | User decisions from /gsd:discuss-phase        |
| `{phase_dir}/*-RESEARCH.md`  | Research findings                             |
| `{phase_dir}/*-DISCOVERY.md` | Discovery findings                            |
| `{phase_dir}/*-SUMMARY.md`   | Past phase summaries                          |

### 3. Files Created

| File                             | Purpose                               |
| -------------------------------- | ------------------------------------- |
| `{phase_dir}/{phase}-NN-PLAN.md` | Execution plans with YAML frontmatter |

### 4. Subagents Spawned

| Agent                  | When                        | Purpose             |
| ---------------------- | --------------------------- | ------------------- |
| `gsd-phase-researcher` | Before planning (if needed) | Research domain     |
| `gsd-plan-checker`     | After planning              | Verify plan quality |

---

## Plan Schema

### PLAN.md Frontmatter (Required)

```yaml
---
phase: XX-name # e.g., "16-foundation"
plan: NN # Plan number (01, 02, etc.)
type: execute # "execute" or "tdd"
wave: N # Execution wave (1, 2, 3...)
depends_on: [] # Plan IDs this plan requires
files_modified: [] # Files this plan touches
autonomous: true # false if plan has checkpoints
user_setup: [] # Human-required setup (optional)

must_haves:
  truths: [] # Observable behaviors
  artifacts: [] # Files that must exist
  key_links: [] # Critical connections
---
```

### Task XML Structure

```xml
<tasks>
  <task type="auto">
    <name>Task 1: [Action-oriented name]</name>
    <files>path/to/file.ext</files>
    <action>[Specific implementation]</action>
    <verify>[Command or check]</verify>
    <done>[Acceptance criteria]</done>
  </task>
</tasks>
```

### Structured Return Formats

1. **PLANNING COMPLETE** - Standard success
2. **GAP CLOSURE PLANS CREATED** - Gap closure mode success
3. **CHECKPOINT REACHED** - Human interaction needed
4. **REVISION COMPLETE** - After addressing checker feedback

---

## What Orchestrator Currently Provides

The workflow (`plan-phase.md`) provides these to the planner via Task() spawn:

```markdown
<planning_context>
**Phase:** {phase_number}
**Mode:** {standard | gap_closure}

**Project State:** {state_content}
**Roadmap:** {roadmap_content}
**Requirements:** {requirements_content}

**Phase Context:**
{context_content}

**Research:** {research_content}
**Gap Closure (if --gaps):** {verification_content} {uat_content}
</planning_context>

<downstream_consumer>
Output consumed by /gsd:execute-phase. Plans need:

- Frontmatter (wave, depends_on, files_modified, autonomous)
- Tasks in XML format
- Verification criteria
- must_haves for goal-backward verification
  </downstream_consumer>

<quality_gate>

- [ ] PLAN.md files created in phase directory
- [ ] Each plan has valid frontmatter
- [ ] Tasks are specific and actionable
- [ ] Dependencies correctly identified
- [ ] Waves assigned for parallel execution
- [ ] must_haves derived from phase goal
      </quality_gate>
```

---

## Isolation Requirements

To isolate the planner agent as per the refactoring plan:

### Input Schema (What Planner Receives)

```python
class PlannerInput(BaseModel):
    phase_number: str
    phase_name: str
    mode: Literal["standard", "gap_closure", "revision"]

    # Context
    state_content: Optional[str]
    roadmap_content: str
    requirements_content: Optional[str]
    context_content: Optional[str]  # User decisions - CRITICAL
    research_content: Optional[str]

    # Gap closure mode
    verification_content: Optional[str]
    uat_content: Optional[str]

    # Revision mode
    existing_plans: Optional[List[str]]
    checker_issues: Optional[List[dict]]

    # Preprocessed context
    codebase_map: Optional[dict]
    phase_history_digest: Optional[dict]
```

### Output Schema (What Planner Returns)

```python
class PlannerOutput(BaseModel):
    status: Literal["complete", "checkpoint", "inconclusive"]

    # On complete
    plans: List[Plan]
    wave_count: int

    # Plan structure
    class Plan(BaseModel):
        plan_number: str
        objective: str
        wave: int
        depends_on: List[str]
        files_modified: List[str]
        autonomous: bool
        tasks: List[Task]
        must_haves: MustHaves

    # On checkpoint
    checkpoint_type: Optional[str]
    checkpoint_data: Optional[dict]

    # Always
    warnings: List[str]
    next_steps: str
```

---

## Key Observations for Isolation

1. **Context is CRITICAL**: The planner heavily depends on CONTEXT.md (user decisions). This must be in the input schema.

2. **Goals Flow from Orchestrator**: The orchestrator extracts phase goals from ROADMAP.md and passes them to the planner.

3. **gsd-tools Dependency**: Many operations use `gsd-tools.js`. In the isolated agent:
   - Validation can be done by orchestrator before/after
   - Git commits should NOT be in the agent (orchestrator responsibility)
   - File reading should be preprocessed

4. **Subagent Spawning**: The planner currently doesn't spawn other agents directly - the workflow does. This aligns with the refactoring goal.

5. **Modes**: Three distinct modes with different inputs:
   - **Standard**: Normal phase planning
   - **Gap Closure**: Planning from verification gaps
   - **Revision**: Updating plans based on checker feedback

6. **Structured Returns**: The planner already uses structured return formats. These map well to output schemas.

---

## Prototype Directory Structure

```
.prototype/
├── agents/
│   └── planner/
│       ├── agent.py          # Core agent logic (invoke function)
│       ├── schema.py         # PlannerInput, PlannerOutput
│       ├── prompts.py        # Extracted prompts from gsd-planner.md
│       └── README.md         # Agent documentation
├── schemas/
│   ├── agent_io/
│   │   └── planner.py        # Shared with agents/planner/schema.py
│   └── domain/
│       └── plans.py          # Plan, Task, MustHaves structures
└── templates/
    └── plans/
        └── task_plan.xml     # Task XML template
```

---

## Next Steps

1. **Define `PlannerInput` schema** based on what the workflow provides
2. **Define `PlannerOutput` schema** based on structured returns
3. **Extract prompts** from `gsd-planner.md` into `prompts.py`
4. **Create `invoke()` function** that takes input, generates output
5. **Remove orchestration logic** (git commits, file discovery, subagent spawning)
6. **Add validation** at input/output boundaries
