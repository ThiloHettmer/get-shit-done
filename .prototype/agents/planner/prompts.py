"""
Planner Agent Prompts

Loads instruction files from the instructions/ directory and provides
prompt builders for different operating modes.
"""

from pathlib import Path
from functools import lru_cache


# ─── Instruction Loader ────────────────────────────────────────────────────────

INSTRUCTIONS_DIR = Path(__file__).parent / "instructions"


@lru_cache(maxsize=20)
def load_instruction(name: str) -> str:
    """
    Load an instruction file by name.

    Args:
        name: Instruction file name without .md extension

    Returns:
        Contents of the instruction file
    """
    path = INSTRUCTIONS_DIR / f"{name}.md"
    if not path.exists():
        raise FileNotFoundError(f"Instruction file not found: {path}")
    return path.read_text()


# ─── Instruction Accessors ─────────────────────────────────────────────────────


def get_role() -> str:
    return load_instruction("role")


def get_context_fidelity() -> str:
    return load_instruction("context-fidelity")


def get_philosophy() -> str:
    return load_instruction("philosophy")


def get_task_breakdown() -> str:
    return load_instruction("task-breakdown")


def get_dependency_graph() -> str:
    return load_instruction("dependency-graph")


def get_goal_backward() -> str:
    return load_instruction("goal-backward")


def get_scope_estimation() -> str:
    return load_instruction("scope-estimation")


def get_gap_closure() -> str:
    return load_instruction("gap-closure")


def get_revision() -> str:
    return load_instruction("revision")


# ─── System Prompt Builder ─────────────────────────────────────────────────────


def build_system_prompt(mode: str) -> str:
    """
    Build the system prompt for the planner agent.

    Args:
        mode: "standard", "gap_closure", or "revision"

    Returns:
        Complete system prompt string
    """
    sections = [
        f"<role>\n{get_role()}\n</role>",
        f"<context_fidelity>\n{get_context_fidelity()}\n</context_fidelity>",
        f"<philosophy>\n{get_philosophy()}\n</philosophy>",
        f"<task_breakdown>\n{get_task_breakdown()}\n</task_breakdown>",
        f"<dependency_graph>\n{get_dependency_graph()}\n</dependency_graph>",
        f"<goal_backward>\n{get_goal_backward()}\n</goal_backward>",
        f"<scope_estimation>\n{get_scope_estimation()}\n</scope_estimation>",
    ]

    if mode == "gap_closure":
        sections.append(f"<gap_closure_mode>\n{get_gap_closure()}\n</gap_closure_mode>")
    elif mode == "revision":
        sections.append(f"<revision_mode>\n{get_revision()}\n</revision_mode>")

    return "\n\n".join(sections)


# ─── User Prompt Builder ───────────────────────────────────────────────────────


def build_user_prompt(
    phase_number: str, phase_name: str, phase_goal: str, mode: str, context: dict
) -> str:
    """
    Build the user prompt with all context.

    Args:
        phase_number: Phase number (e.g., "16")
        phase_name: Phase name (e.g., "foundation")
        phase_goal: Goal from roadmap
        mode: Operating mode
        context: Dict of context fields

    Returns:
        Complete user prompt string
    """
    lines = [
        "<planning_context>",
        f"**Phase:** {phase_number} - {phase_name}",
        f"**Goal:** {phase_goal}",
        f"**Mode:** {mode}",
        "",
    ]

    if context.get("state_content"):
        lines.append(f"**Project State:**\n{context['state_content']}")
        lines.append("")

    if context.get("requirements_content"):
        lines.append(f"**Requirements:**\n{context['requirements_content']}")
        lines.append("")

    # CRITICAL: Phase context (user decisions)
    if context.get("phase_context"):
        lines.append("**Phase Context (USER DECISIONS - CRITICAL):**")
        lines.append("IMPORTANT: Honor these decisions exactly.")
        lines.append("")

        pc = context["phase_context"]
        if pc.get("decisions"):
            lines.append("## Locked Decisions (MUST implement)")
            for d in pc["decisions"]:
                lines.append(f"- **{d['topic']}**: {d['choice']}")
            lines.append("")

        if pc.get("deferred_ideas"):
            lines.append("## Deferred Ideas (MUST NOT include)")
            for d in pc["deferred_ideas"]:
                lines.append(f"- {d['idea']}")
            lines.append("")

        if pc.get("discretion_areas"):
            lines.append("## Claude's Discretion")
            for d in pc["discretion_areas"]:
                lines.append(f"- {d['area']}")
            lines.append("")

    if context.get("research_content"):
        lines.append(f"**Research:**\n{context['research_content']}")
        lines.append("")

    # Codebase context
    codebase_parts = []
    if context.get("codebase_stack"):
        codebase_parts.append(f"**Stack:**\n{context['codebase_stack']}")
    if context.get("codebase_architecture"):
        codebase_parts.append(f"**Architecture:**\n{context['codebase_architecture']}")
    if context.get("codebase_conventions"):
        codebase_parts.append(f"**Conventions:**\n{context['codebase_conventions']}")

    if codebase_parts:
        lines.append("**Codebase Context:**")
        lines.extend(codebase_parts)
        lines.append("")

    # Mode-specific context
    if mode == "gap_closure":
        if context.get("verification_content"):
            lines.append(f"**Verification Gaps:**\n{context['verification_content']}")
        if context.get("uat_content"):
            lines.append(f"**UAT Gaps:**\n{context['uat_content']}")

    if mode == "revision":
        if context.get("existing_plans"):
            lines.append("**Existing Plans:**")
            for plan in context["existing_plans"]:
                lines.append(f"```\n{plan}\n```")
        if context.get("checker_issues"):
            lines.append("**Checker Issues:**")
            for issue in context["checker_issues"]:
                lines.append(
                    f"- [{issue['severity']}] {issue['dimension']}: {issue['description']}"
                )
                if issue.get("fix_hint"):
                    lines.append(f"  Fix hint: {issue['fix_hint']}")

    lines.append("</planning_context>")
    lines.append("")
    lines.append("<instructions>")
    lines.append("Create executable plans following the methodology above.")
    lines.append(
        "Return plans as structured data that can be serialized to PLAN.md format."
    )
    lines.append("</instructions>")

    return "\n".join(lines)
