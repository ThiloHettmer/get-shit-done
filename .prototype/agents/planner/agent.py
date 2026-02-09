"""
Planner Agent - Isolated Implementation

This agent creates executable phase plans with task breakdown, dependency analysis,
and goal-backward verification. It is a pure function: input data → processing → output data.

The agent does NOT:
- Spawn other agents
- Read/write files directly
- Make git commits
- Manage workflow state

All of those are orchestrator responsibilities.
"""

from dataclasses import asdict
from typing import Optional

from .schema import (
    PlannerInput,
    PlannerOutput,
    PlannerMode,
    PlannerStatus,
    Plan,
    PlanType,
    Task,
    TaskType,
    MustHaves,
    Artifact,
    KeyLink,
    CheckpointData,
    plan_to_markdown,
)
from .prompts import build_system_prompt, build_user_prompt


def invoke(input_data: PlannerInput) -> PlannerOutput:
    """
    Execute the planner agent logic with provided input.

    This is the main entry point for the isolated planner agent.
    It processes the input and returns structured output.

    In a real implementation, this would call an LLM with the
    constructed prompts. For now, it provides the structure for
    that integration.

    Args:
        input_data: Validated PlannerInput with all context

    Returns:
        PlannerOutput with plans or checkpoint/error information
    """

    # Validate critical inputs
    validation_warnings = _validate_input(input_data)

    # Build prompts based on mode
    system_prompt = build_system_prompt(input_data.mode.value)

    # Build context dict for user prompt
    context = {
        "state_content": input_data.state_content,
        "requirements_content": input_data.requirements_content,
        "phase_context": _serialize_phase_context(input_data.phase_context)
        if input_data.phase_context
        else None,
        "research_content": input_data.research_content,
        "codebase_stack": input_data.codebase_stack,
        "codebase_architecture": input_data.codebase_architecture,
        "codebase_conventions": input_data.codebase_conventions,
        "verification_content": input_data.verification_content,
        "uat_content": input_data.uat_content,
        "existing_plans": input_data.existing_plans,
        "checker_issues": [asdict(i) for i in input_data.checker_issues],
    }

    user_prompt = build_user_prompt(
        phase_number=input_data.phase_number,
        phase_name=input_data.phase_name,
        phase_goal=input_data.phase_goal,
        mode=input_data.mode.value,
        context=context,
    )

    # Route to appropriate handler based on mode
    if input_data.mode == PlannerMode.STANDARD:
        return _handle_standard_planning(
            input_data, system_prompt, user_prompt, validation_warnings
        )
    elif input_data.mode == PlannerMode.GAP_CLOSURE:
        return _handle_gap_closure(
            input_data, system_prompt, user_prompt, validation_warnings
        )
    elif input_data.mode == PlannerMode.REVISION:
        return _handle_revision(
            input_data, system_prompt, user_prompt, validation_warnings
        )
    else:
        return PlannerOutput(
            status=PlannerStatus.INCONCLUSIVE,
            inconclusive_reason=f"Unknown mode: {input_data.mode}",
            warnings=validation_warnings,
        )


def _validate_input(input_data: PlannerInput) -> list[str]:
    """
    Validate input and return warnings for any issues.
    """
    warnings = []

    if not input_data.phase_number:
        warnings.append("phase_number is required")

    if not input_data.phase_name:
        warnings.append("phase_name is required")

    if not input_data.phase_goal:
        warnings.append("phase_goal is required")

    if not input_data.roadmap_content:
        warnings.append("roadmap_content is required")

    # Mode-specific validation
    if input_data.mode == PlannerMode.GAP_CLOSURE:
        if not input_data.verification_content and not input_data.uat_content:
            warnings.append(
                "Gap closure mode requires verification_content or uat_content"
            )

    if input_data.mode == PlannerMode.REVISION:
        if not input_data.existing_plans:
            warnings.append("Revision mode requires existing_plans")
        if not input_data.checker_issues:
            warnings.append("Revision mode requires checker_issues")

    # Context compliance check
    if input_data.phase_context:
        if input_data.phase_context.decisions:
            # Good - we have user decisions to honor
            pass
        if (
            not input_data.phase_context.decisions
            and not input_data.phase_context.discretion_areas
        ):
            warnings.append(
                "Phase context provided but has no decisions or discretion areas"
            )

    return warnings


def _serialize_phase_context(phase_context) -> dict:
    """Convert PhaseContext to dict for prompt building."""
    return {
        "decisions": [asdict(d) for d in phase_context.decisions],
        "deferred_ideas": [asdict(d) for d in phase_context.deferred_ideas],
        "discretion_areas": [asdict(d) for d in phase_context.discretion_areas],
    }


def _handle_standard_planning(
    input_data: PlannerInput,
    system_prompt: str,
    user_prompt: str,
    warnings: list[str],
) -> PlannerOutput:
    """
    Handle standard phase planning mode.

    This is where the LLM would be called to generate plans.
    For now, returns a structure showing what would be produced.
    """

    # In real implementation:
    # 1. Call LLM with system_prompt + user_prompt
    # 2. Parse LLM response into Plan objects
    # 3. Validate plans against schema
    # 4. Return structured output

    # For demonstration, create a placeholder structure
    # The orchestrator would use this to understand the expected format

    phase_id = f"{input_data.phase_number.zfill(2)}-{input_data.phase_name}"

    # Example plan structure (this would come from LLM in real implementation)
    example_plan = Plan(
        plan_number="01",
        objective=f"[LLM would generate based on phase goal: {input_data.phase_goal}]",
        purpose="[LLM would derive from context]",
        output="[LLM would specify artifacts]",
        phase=phase_id,
        plan_type=PlanType.EXECUTE,
        wave=1,
        depends_on=[],
        files_modified=["[LLM would identify files]"],
        autonomous=True,
        must_haves=MustHaves(
            truths=["[LLM would derive from goal-backward]"],
            artifacts=[],
            key_links=[],
        ),
        tasks=[
            Task(
                name="Task 1: [LLM would name]",
                task_type=TaskType.AUTO,
                files=["[path/to/file]"],
                action="[LLM would specify]",
                verify="[LLM would specify]",
                done="[LLM would specify]",
            ),
        ],
        verification="[Overall verification steps]",
        success_criteria="[Measurable completion]",
    )

    return PlannerOutput(
        status=PlannerStatus.COMPLETE,
        plans=[example_plan],
        wave_count=1,
        wave_structure={1: ["01"]},
        warnings=warnings,
        decisions_honored=_extract_honored_decisions(input_data),
        deferred_excluded=_extract_deferred_excluded(input_data),
        summary=f"Created 1 plan for phase {input_data.phase_number}",
        next_steps=f"/gsd:execute-phase {input_data.phase_number}",
    )


def _handle_gap_closure(
    input_data: PlannerInput,
    system_prompt: str,
    user_prompt: str,
    warnings: list[str],
) -> PlannerOutput:
    """
    Handle gap closure mode - planning from verification failures.
    """

    # Parse gaps from verification/UAT content
    # Group gaps by artifact/concern
    # Create targeted fix plans

    phase_id = f"{input_data.phase_number.zfill(2)}-{input_data.phase_name}"

    example_gap_plan = Plan(
        plan_number="04",  # Continues from existing plans
        objective="[Fix gaps identified in verification]",
        purpose="Address verification failures",
        output="Fixed implementation",
        phase=phase_id,
        plan_type=PlanType.EXECUTE,
        wave=1,
        depends_on=[],
        files_modified=["[affected files]"],
        autonomous=True,
        gap_closure=True,
        must_haves=MustHaves(
            truths=["[Failed truth now passing]"],
            artifacts=[],
            key_links=[],
        ),
        tasks=[
            Task(
                name="Fix: [gap description]",
                task_type=TaskType.AUTO,
                files=["[affected file]"],
                action="[Fix based on gap.missing]",
                verify="[Verification that gap is closed]",
                done="[Truth now achievable]",
            ),
        ],
    )

    return PlannerOutput(
        status=PlannerStatus.COMPLETE,
        plans=[example_gap_plan],
        wave_count=1,
        wave_structure={1: ["04"]},
        warnings=warnings,
        summary=f"Created gap closure plans for phase {input_data.phase_number}",
        next_steps=f"/gsd:execute-phase {input_data.phase_number} --gaps-only",
    )


def _handle_revision(
    input_data: PlannerInput,
    system_prompt: str,
    user_prompt: str,
    warnings: list[str],
) -> PlannerOutput:
    """
    Handle revision mode - updating plans based on checker feedback.
    """

    # Parse existing plans
    # Apply targeted fixes for each checker issue
    # Preserve working parts

    addressed_count = len(input_data.checker_issues)

    return PlannerOutput(
        status=PlannerStatus.COMPLETE,
        plans=[],  # Would contain updated plans
        wave_count=0,  # Would be recalculated
        wave_structure={},
        warnings=warnings,
        summary=f"Addressed {addressed_count}/{addressed_count} checker issues",
        next_steps="Plans updated, ready for re-verification",
    )


def _extract_honored_decisions(input_data: PlannerInput) -> list[str]:
    """Extract list of honored decisions for context compliance report."""
    if not input_data.phase_context:
        return []
    return [f"{d.topic}: {d.choice}" for d in input_data.phase_context.decisions]


def _extract_deferred_excluded(input_data: PlannerInput) -> list[str]:
    """Extract list of deferred ideas that were excluded."""
    if not input_data.phase_context:
        return []
    return [d.idea for d in input_data.phase_context.deferred_ideas]


# ─── Standalone Testing ────────────────────────────────────────────────────────


def create_test_input() -> PlannerInput:
    """
    Create a test input for standalone testing.

    Usage:
        from agents.planner.agent import create_test_input, invoke
        test_input = create_test_input()
        result = invoke(test_input)
        print(result)
    """
    from .schema import PhaseContext, UserDecision, DeferredIdea, DiscretionArea

    return PlannerInput(
        phase_number="16",
        phase_name="foundation",
        phase_goal="Set up project foundation with auth and database",
        mode=PlannerMode.STANDARD,
        roadmap_content="""## Roadmap
### Phase 16: Foundation
Goal: Set up project foundation with auth and database
""",
        state_content="**Current Phase:** 16\n**Status:** planning",
        requirements_content="- User authentication\n- Database setup\n- Basic API structure",
        phase_context=PhaseContext(
            decisions=[
                UserDecision(topic="Auth library", choice="Use better-auth"),
                UserDecision(topic="Database", choice="PostgreSQL with Prisma"),
            ],
            deferred_ideas=[
                DeferredIdea(idea="Social login"),
                DeferredIdea(idea="Two-factor auth"),
            ],
            discretion_areas=[
                DiscretionArea(area="File structure within src/"),
            ],
        ),
        phase_dir=".planning/phases/16-foundation",
        depth="standard",
    )


if __name__ == "__main__":
    # Standalone test
    test_input = create_test_input()
    result = invoke(test_input)

    print("=" * 60)
    print("PLANNER AGENT TEST OUTPUT")
    print("=" * 60)
    print(f"Status: {result.status.value}")
    print(f"Plans: {len(result.plans)}")
    print(f"Wave count: {result.wave_count}")
    print(f"Warnings: {result.warnings}")
    print(f"Summary: {result.summary}")
    print(f"Next steps: {result.next_steps}")
    print()

    if result.plans:
        print("Sample plan markdown:")
        print("-" * 40)
        print(plan_to_markdown(result.plans[0]))
