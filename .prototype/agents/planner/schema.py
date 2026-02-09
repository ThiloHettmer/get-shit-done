"""
Planner Agent Input/Output Schemas

Defines the data contracts for the isolated planner agent.
All inputs are preprocessed by the orchestrator; the agent is a pure function.
"""

from dataclasses import dataclass, field
from typing import Literal, Optional
from enum import Enum


# ─── Enums ─────────────────────────────────────────────────────────────────────

class PlannerMode(str, Enum):
    """Operating mode for the planner agent."""
    STANDARD = "standard"          # Normal phase planning
    GAP_CLOSURE = "gap_closure"    # Planning from verification gaps
    REVISION = "revision"          # Updating plans based on checker feedback


class TaskType(str, Enum):
    """Task execution types."""
    AUTO = "auto"                              # Fully autonomous
    CHECKPOINT_HUMAN_VERIFY = "checkpoint:human-verify"  # Pauses for visual verification
    CHECKPOINT_DECISION = "checkpoint:decision"           # Pauses for user choice
    CHECKPOINT_HUMAN_ACTION = "checkpoint:human-action"   # Rare: manual step required
    TDD = "tdd"                                            # Test-driven development


class PlanType(str, Enum):
    """Plan types."""
    EXECUTE = "execute"
    TDD = "tdd"


class PlannerStatus(str, Enum):
    """Planner return status."""
    COMPLETE = "complete"          # Planning finished successfully
    CHECKPOINT = "checkpoint"      # Human interaction required
    INCONCLUSIVE = "inconclusive"  # Could not complete (needs guidance)


# ─── Domain Models ─────────────────────────────────────────────────────────────

@dataclass
class Artifact:
    """An artifact that must exist for the plan to succeed."""
    path: str                      # File path
    provides: str                  # What this artifact provides
    min_lines: Optional[int] = None
    exports: list[str] = field(default_factory=list)
    contains: Optional[str] = None


@dataclass
class KeyLink:
    """A critical connection between artifacts."""
    from_path: str                 # Source artifact
    to_path: str                   # Target artifact
    via: str                       # How they connect (e.g., "fetch in useEffect")
    pattern: Optional[str] = None  # Regex pattern to verify connection


@dataclass
class MustHaves:
    """Goal-backward verification criteria."""
    truths: list[str]              # Observable behaviors (user perspective)
    artifacts: list[Artifact]       # Files that must exist
    key_links: list[KeyLink]        # Critical connections


@dataclass
class Task:
    """A single task within a plan."""
    name: str
    task_type: TaskType
    files: list[str] = field(default_factory=list)
    action: Optional[str] = None
    verify: Optional[str] = None
    done: Optional[str] = None
    
    # Checkpoint-specific fields
    what_built: Optional[str] = None       # For human-verify
    how_to_verify: Optional[str] = None    # For human-verify
    decision: Optional[str] = None         # For decision
    options: list[dict] = field(default_factory=list)  # For decision
    resume_signal: Optional[str] = None    # How to resume after checkpoint


@dataclass
class Plan:
    """A complete execution plan."""
    plan_number: str               # e.g., "01", "02"
    objective: str                 # What this plan accomplishes
    purpose: str                   # Why this matters
    output: str                    # Artifacts created
    
    # Frontmatter fields
    phase: str                     # Phase identifier
    plan_type: PlanType
    wave: int
    depends_on: list[str]
    files_modified: list[str]
    autonomous: bool
    must_haves: MustHaves
    
    # Optional
    user_setup: list[dict] = field(default_factory=list)
    gap_closure: bool = False
    
    # Content
    tasks: list[Task] = field(default_factory=list)
    verification: Optional[str] = None     # Overall phase checks
    success_criteria: Optional[str] = None  # Measurable completion


@dataclass
class UserDecision:
    """A locked decision from CONTEXT.md."""
    topic: str
    choice: str
    rationale: Optional[str] = None


@dataclass
class DeferredIdea:
    """An idea explicitly deferred to future phases."""
    idea: str
    reason: Optional[str] = None


@dataclass
class DiscretionArea:
    """An area where the planner has freedom to choose."""
    area: str
    guidance: Optional[str] = None


@dataclass
class PhaseContext:
    """Parsed user decisions from CONTEXT.md."""
    decisions: list[UserDecision] = field(default_factory=list)
    deferred_ideas: list[DeferredIdea] = field(default_factory=list)
    discretion_areas: list[DiscretionArea] = field(default_factory=list)


@dataclass
class CheckerIssue:
    """An issue found by the plan checker."""
    plan: str
    dimension: str
    severity: Literal["blocker", "warning", "info"]
    description: str
    task: Optional[int] = None
    fix_hint: Optional[str] = None


# ─── Input Schema ──────────────────────────────────────────────────────────────

@dataclass
class PlannerInput:
    """
    Input to the planner agent.
    
    All context is preprocessed by the orchestrator.
    The planner receives everything it needs upfront.
    """
    
    # Required
    phase_number: str              # e.g., "16", "2.1"
    phase_name: str                # e.g., "foundation", "auth"
    phase_goal: str                # Goal from ROADMAP.md
    mode: PlannerMode
    
    # Context (preprocessed by orchestrator)
    roadmap_content: str           # Full ROADMAP.md content
    state_content: Optional[str] = None       # STATE.md content
    requirements_content: Optional[str] = None  # REQUIREMENTS.md content
    
    # Phase-specific context
    phase_context: Optional[PhaseContext] = None  # Parsed CONTEXT.md - CRITICAL
    research_content: Optional[str] = None        # RESEARCH.md content
    
    # Codebase context (preprocessed)
    codebase_stack: Optional[str] = None          # STACK.md
    codebase_architecture: Optional[str] = None   # ARCHITECTURE.md  
    codebase_conventions: Optional[str] = None    # CONVENTIONS.md
    
    # History (preprocessed)
    phase_history_digest: Optional[dict] = None   # From history-digest
    relevant_summaries: list[str] = field(default_factory=list)  # Prior SUMMARY.md contents
    
    # Gap closure mode
    verification_content: Optional[str] = None    # VERIFICATION.md
    uat_content: Optional[str] = None             # UAT.md
    
    # Revision mode
    existing_plans: list[str] = field(default_factory=list)  # Current PLAN.md contents
    checker_issues: list[CheckerIssue] = field(default_factory=list)
    
    # Configuration
    phase_dir: str = ""            # Where to write plans (for reference)
    depth: Literal["quick", "standard", "comprehensive"] = "standard"


# ─── Output Schema ─────────────────────────────────────────────────────────────

@dataclass
class CheckpointData:
    """Data for checkpoint returns."""
    checkpoint_type: str           # human-verify, decision, human-action
    context: str                   # What needs to be decided/verified
    options: list[dict] = field(default_factory=list)  # For decisions
    resume_signal: str = ""        # How user should respond


@dataclass  
class PlannerOutput:
    """
    Output from the planner agent.
    
    Returns structured data; orchestrator handles file writing and git.
    """
    
    # Status
    status: PlannerStatus
    
    # On COMPLETE: Plans created
    plans: list[Plan] = field(default_factory=list)
    wave_count: int = 0
    
    # Wave structure for display
    wave_structure: dict[int, list[str]] = field(default_factory=dict)  # wave -> plan IDs
    
    # On CHECKPOINT: What needs user input
    checkpoint: Optional[CheckpointData] = None
    
    # On INCONCLUSIVE: Why we couldn't complete
    inconclusive_reason: Optional[str] = None
    attempts: int = 0
    
    # Always present
    warnings: list[str] = field(default_factory=list)
    
    # Context compliance report (if CONTEXT.md was provided)
    decisions_honored: list[str] = field(default_factory=list)
    deferred_excluded: list[str] = field(default_factory=list)
    
    # Summary for display
    summary: str = ""
    next_steps: str = ""


# ─── Serialization Helpers ─────────────────────────────────────────────────────

def plan_to_markdown(plan: Plan) -> str:
    """
    Convert a Plan object to PLAN.md markdown format.
    
    This is used by the orchestrator to write the actual files.
    """
    lines = []
    
    # Frontmatter
    lines.append("---")
    lines.append(f"phase: {plan.phase}")
    lines.append(f"plan: {plan.plan_number}")
    lines.append(f"type: {plan.plan_type.value}")
    lines.append(f"wave: {plan.wave}")
    lines.append(f"depends_on: {plan.depends_on}")
    lines.append(f"files_modified: {plan.files_modified}")
    lines.append(f"autonomous: {str(plan.autonomous).lower()}")
    
    if plan.user_setup:
        lines.append(f"user_setup: {plan.user_setup}")
    
    if plan.gap_closure:
        lines.append("gap_closure: true")
    
    # must_haves
    lines.append("")
    lines.append("must_haves:")
    lines.append("  truths:")
    for truth in plan.must_haves.truths:
        lines.append(f'    - "{truth}"')
    
    lines.append("  artifacts:")
    for artifact in plan.must_haves.artifacts:
        lines.append(f'    - path: "{artifact.path}"')
        lines.append(f'      provides: "{artifact.provides}"')
        if artifact.min_lines:
            lines.append(f"      min_lines: {artifact.min_lines}")
        if artifact.exports:
            lines.append(f"      exports: {artifact.exports}")
    
    lines.append("  key_links:")
    for link in plan.must_haves.key_links:
        lines.append(f'    - from: "{link.from_path}"')
        lines.append(f'      to: "{link.to_path}"')
        lines.append(f'      via: "{link.via}"')
        if link.pattern:
            lines.append(f'      pattern: "{link.pattern}"')
    
    lines.append("---")
    lines.append("")
    
    # Objective
    lines.append("<objective>")
    lines.append(plan.objective)
    lines.append("")
    lines.append(f"Purpose: {plan.purpose}")
    lines.append(f"Output: {plan.output}")
    lines.append("</objective>")
    lines.append("")
    
    # Tasks
    lines.append("<tasks>")
    lines.append("")
    for task in plan.tasks:
        lines.append(f'<task type="{task.task_type.value}">')
        lines.append(f"  <name>{task.name}</name>")
        
        if task.task_type == TaskType.AUTO:
            lines.append(f"  <files>{', '.join(task.files)}</files>")
            lines.append(f"  <action>{task.action}</action>")
            lines.append(f"  <verify>{task.verify}</verify>")
            lines.append(f"  <done>{task.done}</done>")
        elif task.task_type == TaskType.CHECKPOINT_HUMAN_VERIFY:
            lines.append(f"  <what-built>{task.what_built}</what-built>")
            lines.append(f"  <how-to-verify>{task.how_to_verify}</how-to-verify>")
            lines.append(f"  <resume-signal>{task.resume_signal}</resume-signal>")
        elif task.task_type == TaskType.CHECKPOINT_DECISION:
            lines.append(f"  <decision>{task.decision}</decision>")
            lines.append("  <options>")
            for opt in task.options:
                lines.append(f'    <option id="{opt.get("id", "")}">')
                lines.append(f"      <name>{opt.get('name', '')}</name>")
                lines.append(f"      <pros>{opt.get('pros', '')}</pros>")
                lines.append(f"      <cons>{opt.get('cons', '')}</cons>")
                lines.append("    </option>")
            lines.append("  </options>")
            lines.append(f"  <resume-signal>{task.resume_signal}</resume-signal>")
        
        lines.append("</task>")
        lines.append("")
    
    lines.append("</tasks>")
    lines.append("")
    
    # Verification
    if plan.verification:
        lines.append("<verification>")
        lines.append(plan.verification)
        lines.append("</verification>")
        lines.append("")
    
    # Success criteria
    if plan.success_criteria:
        lines.append("<success_criteria>")
        lines.append(plan.success_criteria)
        lines.append("</success_criteria>")
        lines.append("")
    
    # Output section
    lines.append("<output>")
    lines.append(f"After completion, create `.planning/phases/{plan.phase}/{plan.phase}-{plan.plan_number}-SUMMARY.md`")
    lines.append("</output>")
    
    return "\n".join(lines)
