# Planner Agent

Isolated implementation of the GSD planner agent.

## Overview

This agent creates executable phase plans with task breakdown, dependency analysis, and goal-backward verification. It is implemented as a **pure function**: input data → processing → output data.

## Architecture Principles

- **No Side Effects**: Agent does not read/write files, make git commits, or spawn other agents
- **Preprocessed Context**: All context is provided upfront by the orchestrator
- **Structured I/O**: Defined schemas for inputs and outputs
- **Blackbox Design**: Internal implementation can change without affecting callers

## Usage

```python
from agents.planner import invoke, PlannerInput, PlannerMode, plan_to_markdown

# Create input with preprocessed context
input_data = PlannerInput(
    phase_number="16",
    phase_name="foundation",
    phase_goal="Set up project foundation with auth and database",
    mode=PlannerMode.STANDARD,
    roadmap_content="...",  # Full ROADMAP.md content
    state_content="...",    # STATE.md content
    requirements_content="...",
    # ... other context fields
)

# Invoke the agent
output = invoke(input_data)

# Handle the result
if output.status == PlannerStatus.COMPLETE:
    for plan in output.plans:
        # Convert to markdown and write to file
        markdown = plan_to_markdown(plan)
        path = f".planning/phases/{plan.phase}/{plan.phase}-{plan.plan_number}-PLAN.md"
        # orchestrator writes file...
elif output.status == PlannerStatus.CHECKPOINT:
    # Handle checkpoint (present to user)
    pass
elif output.status == PlannerStatus.INCONCLUSIVE:
    # Handle failure
    print(output.inconclusive_reason)
```

## Operating Modes

### Standard Mode

Normal phase planning from roadmap/requirements.

```python
input_data = PlannerInput(
    mode=PlannerMode.STANDARD,
    # ... context
)
```

### Gap Closure Mode

Planning to fix verification failures.

```python
input_data = PlannerInput(
    mode=PlannerMode.GAP_CLOSURE,
    verification_content="...",  # From VERIFICATION.md
    uat_content="...",           # From UAT.md
    # ... context
)
```

### Revision Mode

Updating plans based on checker feedback.

```python
input_data = PlannerInput(
    mode=PlannerMode.REVISION,
    existing_plans=["..."],  # Current PLAN.md contents
    checker_issues=[...],    # Issues from plan checker
    # ... context
)
```

## Input Schema

| Field              | Type         | Required | Description                            |
| ------------------ | ------------ | -------- | -------------------------------------- |
| `phase_number`     | str          | Yes      | Phase number (e.g., "16")              |
| `phase_name`       | str          | Yes      | Phase name (e.g., "foundation")        |
| `phase_goal`       | str          | Yes      | Goal from ROADMAP.md                   |
| `mode`             | PlannerMode  | Yes      | STANDARD, GAP_CLOSURE, or REVISION     |
| `roadmap_content`  | str          | Yes      | Full ROADMAP.md content                |
| `phase_context`    | PhaseContext | No       | User decisions (CRITICAL when present) |
| `research_content` | str          | No       | RESEARCH.md content                    |
| ...                |              |          | See schema.py for full list            |

## Output Schema

| Field               | Type           | Description                           |
| ------------------- | -------------- | ------------------------------------- |
| `status`            | PlannerStatus  | COMPLETE, CHECKPOINT, or INCONCLUSIVE |
| `plans`             | List[Plan]     | Created plans (on COMPLETE)           |
| `wave_count`        | int            | Number of execution waves             |
| `wave_structure`    | dict           | Wave → plan ID mapping                |
| `checkpoint`        | CheckpointData | Checkpoint info (on CHECKPOINT)       |
| `warnings`          | List[str]      | Validation warnings                   |
| `decisions_honored` | List[str]      | Context compliance report             |
| `summary`           | str            | Human-readable summary                |
| `next_steps`        | str            | Suggested next command                |

## Files

| File          | Purpose                                  |
| ------------- | ---------------------------------------- |
| `agent.py`    | Main invoke() function and mode handlers |
| `schema.py`   | Input/output data models                 |
| `prompts.py`  | Extracted prompts from gsd-planner.md    |
| `__init__.py` | Package exports                          |

## Testing

Run standalone test:

```bash
cd .prototype
python -m agents.planner.agent
```

Or in Python:

```python
from agents.planner import create_test_input, invoke

test_input = create_test_input()
result = invoke(test_input)
print(result.summary)
```

## Orchestrator Integration

The orchestrator is responsible for:

1. **Context Preprocessing**: Load and parse all context files
2. **Agent Invocation**: Call `invoke()` with `PlannerInput`
3. **File Writing**: Use `plan_to_markdown()` to write PLAN.md files
4. **Git Operations**: Commit planning docs
5. **Verification Loop**: Spawn plan checker, handle revisions
6. **User Interaction**: Present checkpoints, collect responses
