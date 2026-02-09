"""
Planner Agent

Isolated planner agent for the GSD framework.
Creates executable phase plans with task breakdown, dependency analysis,
and goal-backward verification.

Usage:
    from agents.planner import invoke, PlannerInput, PlannerMode

    input_data = PlannerInput(
        phase_number="16",
        phase_name="foundation",
        phase_goal="Set up project foundation",
        mode=PlannerMode.STANDARD,
        roadmap_content="...",
        # ... other context
    )

    output = invoke(input_data)

    if output.status == PlannerStatus.COMPLETE:
        for plan in output.plans:
            markdown = plan_to_markdown(plan)
            # Write to file...
"""

from .agent import invoke, create_test_input
from .schema import (
    # Input/Output
    PlannerInput,
    PlannerOutput,
    # Enums
    PlannerMode,
    PlannerStatus,
    PlanType,
    TaskType,
    # Domain models
    Plan,
    Task,
    MustHaves,
    Artifact,
    KeyLink,
    PhaseContext,
    UserDecision,
    DeferredIdea,
    DiscretionArea,
    CheckerIssue,
    CheckpointData,
    # Helpers
    plan_to_markdown,
)
from .prompts import (
    build_system_prompt,
    build_user_prompt,
    ROLE,
    PHILOSOPHY,
    TASK_BREAKDOWN,
    GOAL_BACKWARD,
)

__all__ = [
    # Main entry point
    "invoke",
    "create_test_input",
    # Input/Output
    "PlannerInput",
    "PlannerOutput",
    # Enums
    "PlannerMode",
    "PlannerStatus",
    "PlanType",
    "TaskType",
    # Domain models
    "Plan",
    "Task",
    "MustHaves",
    "Artifact",
    "KeyLink",
    "PhaseContext",
    "UserDecision",
    "DeferredIdea",
    "DiscretionArea",
    "CheckerIssue",
    "CheckpointData",
    # Helpers
    "plan_to_markdown",
    "build_system_prompt",
    "build_user_prompt",
]
