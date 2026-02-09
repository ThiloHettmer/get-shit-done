# GSD Framework Refactoring - Endgoal Specification

## Overview

This document defines the target architecture for refactoring the Get-Shit-Done (GSD) framework. The refactoring transforms the current LLM-orchestrated system into a modular, blackbox architecture with centralized orchestration and preprocessed context.

**Purpose**: Extract and isolate all logic from the existing GSD framework to enable:

- Independent agent development and testing
- External orchestration via LangGraph or similar tools
- Template-based workflows with preprocessed context
- Incremental improvements without system-wide breakage

**Scope**: This is a REFACTORING project - we are restructuring existing functionality, not designing new features.

---

## Core Architectural Principles

### 1. Agent Isolation

**Current State**: Agents are embedded within command files, share state through filesystem reads, and orchestrate other agents directly.

**Target State**:

- Each agent exists in its own directory with complete isolation
- Agents have zero knowledge of other agents
- Agents do not spawn other agents
- Agents do not manage workflow state
- Agents are pure functions: `input data → processing → output data`

**Structure**:

```
agents/
├── planner/
│   ├── agent.py           # Core agent logic
│   ├── schema.py          # Input/output data models
│   ├── prompts.py         # Agent prompts/templates
│   └── README.md          # Agent documentation
├── executor/
│   ├── agent.py
│   ├── schema.py
│   ├── prompts.py
│   └── README.md
├── verifier/
│   ├── agent.py
│   ├── schema.py
│   ├── prompts.py
│   └── README.md
└── researcher/
    ├── agent.py
    ├── schema.py
    ├── prompts.py
    └── README.md
```

### 2. Independent Invocation

**Requirement**: Every agent must be callable standalone for testing and debugging.

**Interface Pattern**:

```python
# Each agent exposes a standard interface
def invoke(input_data: AgentInput) -> AgentOutput:
    """
    Execute agent logic with provided input.

    Args:
        input_data: Validated input conforming to agent's schema

    Returns:
        Validated output conforming to agent's schema
    """
    pass
```

**Benefits**:

- Unit testing individual agents
- Debugging agent behavior in isolation
- Swapping agent implementations
- Running agents outside the workflow

### 3. Uniform Data Structures

**Current State**: Agents communicate via unstructured filesystem artifacts (PLAN.md, SUMMARY.md) with inconsistent formats.

**Target State**:

- Defined schemas for all agent inputs and outputs
- Validation at agent boundaries
- Serializable data structures (JSON/Pydantic models)
- Backward compatibility tracking

**Example Schema**:

```python
class PlannerInput(BaseModel):
    phase_number: int
    phase_description: str
    requirements: List[Requirement]
    context: PreprocessedContext
    codebase_map: CodebaseMap
    user_decisions: Optional[Dict[str, Any]]

class PlannerOutput(BaseModel):
    plans: List[TaskPlan]
    dependencies: List[Dependency]
    verification_criteria: List[VerificationCriterion]
    warnings: List[str]
```

### 4. Centralized Orchestration

**Current State**: Workflow logic embedded in agents - planner spawns checker, executor manages waves, verifier spawns debuggers.

**Target State**:

- All orchestration logic extracted to central orchestrator
- Orchestrator handles:
  - Workflow state transitions (PLANNING → EXECUTION → VERIFICATION)
  - Agent spawning and coordination
  - Parallel execution management
  - Error handling and retry logic
  - Checkpoint management for user interaction
- Agents are stateless workers that process inputs

**Orchestrator Responsibilities**:

```
Orchestrator:
├── State Management
│   ├── Track current phase
│   ├── Maintain workflow state
│   └── Persist checkpoint data
├── Agent Coordination
│   ├── Spawn agents with preprocessed context
│   ├── Collect agent outputs
│   ├── Route data between agents
│   └── Handle agent failures
├── Workflow Logic
│   ├── Decide when to plan vs execute vs verify
│   ├── Determine parallelization opportunities
│   ├── Manage task chunking
│   └── Trigger user interactions
└── Context Preprocessing
    ├── Load codebase maps
    ├── Gather relevant context
    ├── Fill templates with data
    └── Package inputs for agents
```

### 5. Preprocessed Context

**Current State**: Agents gather context during execution via multiple tool calls (reading files, searching code, analyzing dependencies).

**Target State**:

- Context collection happens BEFORE agent invocation
- Orchestrator or preprocessing step gathers all necessary data
- Agents receive complete context as structured input
- Agents can still request additional context but don't do heavy discovery

**Context Types**:

```
PreprocessedContext:
├── Codebase Map (from codebase-mapper)
│   ├── Technology stack
│   ├── Architecture patterns
│   ├── File structure
│   ├── Conventions
│   ├── Testing patterns
│   └── Integration points
├── Domain Research (from researcher)
│   ├── Ecosystem knowledge
│   ├── Implementation patterns
│   ├── Known pitfalls
│   └── Best practices
├── User Decisions (from discuss-phase)
│   ├── Implementation preferences
│   ├── Design choices
│   ├── Constraints
│   └── Edge case handling
└── Project Metadata
    ├── Requirements
    ├── Roadmap
    ├── Current phase
    └── Previous work
```

**Benefits**:

- Agents get better instructions upfront
- Reduced redundant context gathering
- Faster agent execution
- Better token efficiency
- Easier to audit what context agents see

### 6. Decoupled Templates/Data/Workflows

**Current State**: Templates (PLAN.md structure), data schemas, and workflow logic mixed together in agent prompts.

**Target State**: Complete separation into distinct concerns.

#### Templates

**Location**: `templates/`
**Purpose**: Define output formats and structures

```
templates/
├── plans/
│   ├── task_plan.xml          # XML structure for task plans
│   └── phase_plan.md          # Phase planning template
├── summaries/
│   ├── execution_summary.md   # Post-execution summary
│   └── verification_report.md # Verification results
└── context/
    ├── codebase_context.md    # Codebase analysis template
    └── research_context.md    # Research findings template
```

#### Data Schemas

**Location**: `schemas/`
**Purpose**: Define all data structures used in the system

```
schemas/
├── agent_io/
│   ├── planner.py         # Planner input/output schemas
│   ├── executor.py        # Executor input/output schemas
│   └── verifier.py        # Verifier input/output schemas
├── workflow/
│   ├── state.py           # Workflow state schema
│   ├── checkpoint.py      # Checkpoint data schema
│   └── events.py          # Event schemas
└── domain/
    ├── codebase.py        # Codebase map schema
    ├── requirements.py    # Requirements schema
    └── plans.py           # Plan structure schema
```

#### Workflows

**Location**: `workflows/`
**Purpose**: Define workflow logic separate from agents

```
workflows/
├── planning_workflow.py    # Planning phase workflow
├── execution_workflow.py   # Execution phase workflow
├── verification_workflow.py # Verification phase workflow
└── utils/
    ├── chunking.py        # Task chunking logic
    ├── parallelization.py # Parallel execution logic
    └── checkpointing.py   # User interaction checkpoints
```

### 7. Blackbox Refactorability

**Principle**: Internal agent implementation can change freely without affecting external callers.

**Contract Requirements**:

- Input schema is stable and versioned
- Output schema is stable and versioned
- Agent behavior is well-documented
- Breaking changes follow semver

**Enables**:

- Improving agent prompts without touching orchestrator
- Swapping LLM providers per agent
- Optimizing agent internals
- A/B testing different implementations
- Gradual agent improvements

**Example**:

```python
# v1.0.0 - Original implementation
class PlannerV1:
    def invoke(self, input: PlannerInput) -> PlannerOutput:
        # Original logic using simple prompting
        pass

# v1.1.0 - Improved implementation (same interface)
class PlannerV1_1:
    def invoke(self, input: PlannerInput) -> PlannerOutput:
        # Improved logic with chain-of-thought
        # External callers see no difference
        pass
```

---

## Component Breakdown

### Agents to Extract

Based on current GSD implementation, these agents need isolation:

1. **Planner** (`gsd-planner.md`)
   - Input: Phase description, requirements, preprocessed context
   - Output: Task plans with verification criteria
   - Current issues: Spawns checker agent, manages plan iteration

2. **Executor** (`gsd-executor.md`)
   - Input: Single task plan, codebase context
   - Output: Execution summary, file changes
   - Current issues: Embedded in execute-phase orchestrator

3. **Verifier** (`gsd-verifier.md`)
   - Input: Phase goals, implementation changes
   - Output: Verification report, issues found
   - Current issues: Spawns debugger agents

4. **Researcher** (`gsd-researcher.md`)
   - Input: Research domain, focus areas
   - Output: Structured research findings
   - Current issues: Manages parallel research agents internally

5. **Debugger** (`gsd-debugger.md`)
   - Input: Bug description, relevant context
   - Output: Diagnosis, fix plan
   - Current issues: Manages debug session state

6. **Codebase Mapper** (`gsd-codebase-mapper.md`)
   - Input: Focus area (tech/arch/quality/concerns)
   - Output: Structured codebase analysis
   - Current issues: Writes documents directly instead of returning data

### Context Collectors to Extract

These are preprocessing functions, not agents:

1. **Codebase Analysis**
   - Parallel exploration of tech stack, architecture, conventions, concerns
   - Output: CodebaseMap structure

2. **Domain Research**
   - Research ecosystem, implementation patterns, pitfalls
   - Output: ResearchContext structure

3. **User Decision Capture**
   - Interactive discussion of implementation choices
   - Output: UserDecisions structure

4. **Requirement Analysis**
   - Parse and structure requirements
   - Output: Requirements structure

### Workflow Orchestrators to Extract

These manage agent coordination:

1. **Planning Orchestrator**
   - Gather context → spawn planner → spawn checker → iterate
   - Current location: `/gsd:plan-phase` command

2. **Execution Orchestrator**
   - Chunk plans → spawn executors in waves → collect results
   - Current location: `/gsd:execute-phase` command

3. **Verification Orchestrator**
   - Spawn verifier → analyze results → spawn debuggers if needed
   - Current location: `/gsd:verify-work` command

---

## Target Directory Structure

```
.docs/prototype/
├── agents/                      # Isolated agent implementations
│   ├── planner/
│   ├── executor/
│   ├── verifier/
│   ├── researcher/
│   ├── debugger/
│   └── codebase_mapper/
├── schemas/                     # All data structure definitions
│   ├── agent_io/
│   ├── workflow/
│   └── domain/
├── templates/                   # Output format templates
│   ├── plans/
│   ├── summaries/
│   └── context/
├── workflows/                   # Orchestration logic
│   ├── planning_workflow.py
│   ├── execution_workflow.py
│   ├── verification_workflow.py
│   └── utils/
├── context_collectors/          # Context preprocessing
│   ├── codebase_analyzer.py
│   ├── domain_researcher.py
│   ├── decision_capturer.py
│   └── requirement_parser.py
├── orchestrator/                # Central orchestration engine
│   ├── state_manager.py
│   ├── agent_coordinator.py
│   └── checkpoint_handler.py
├── utils/                       # Shared utilities
│   ├── file_ops.py
│   ├── git_ops.py
│   └── validation.py
└── tests/                       # Test suite
    ├── agents/
    ├── workflows/
    └── integration/
```

---

## Refactoring Strategy

### Phase 1: Schema Definition

1. Define all input/output schemas for agents
2. Define workflow state schemas
3. Define domain model schemas (codebase map, requirements, plans)
4. Create validation utilities

### Phase 2: Agent Extraction

For each agent:

1. Create isolated directory structure
2. Extract agent logic from current commands
3. Separate prompts into prompts.py
4. Define schema.py with input/output models
5. Create agent.py with invoke() interface
6. Write agent README with usage examples
7. Create unit tests

### Phase 3: Template Extraction

1. Extract XML plan templates
2. Extract markdown templates (summaries, reports)
3. Define template variables and fill logic
4. Create template validation

### Phase 4: Context Collector Extraction

1. Extract codebase mapping logic
2. Extract research logic
3. Extract decision capture logic
4. Make each collector standalone
5. Define collector output schemas

### Phase 5: Workflow Extraction

1. Extract planning workflow orchestration
2. Extract execution workflow orchestration
3. Extract verification workflow orchestration
4. Remove orchestration from agent code
5. Create workflow state management

### Phase 6: Central Orchestrator

1. Create state management layer
2. Create agent coordination layer
3. Create checkpoint handling
4. Wire workflows together
5. Add error handling and retry logic

### Phase 7: Integration & Testing

1. Integration tests for full workflows
2. Verify all agents work standalone
3. Verify orchestrator manages state correctly
4. Performance testing
5. Documentation

---

## Success Criteria

The refactoring is complete when:

✅ **Isolation**

- Each agent runs independently with test harness
- No agent imports or calls another agent
- All agents have documented interfaces

✅ **Data Contracts**

- All inputs/outputs have schemas
- Validation passes at agent boundaries
- Breaking changes are versioned

✅ **Orchestration**

- Workflow logic exists outside agents
- Orchestrator manages all agent coordination
- State management is centralized

✅ **Context Preprocessing**

- Context collectors are separate from agents
- Agents receive structured, preprocessed context
- Context gathering is auditable

✅ **Decoupling**

- Templates separated from code
- Data schemas separated from logic
- Workflows separated from agents

✅ **Blackbox Property**

- Agent internals can change without breaking callers
- Stable interfaces documented
- Unit tests cover agent contracts

✅ **Maintainability**

- Clear separation of concerns
- Each component has single responsibility
- Easy to locate and modify specific behavior

---

## Migration Path

This refactoring enables future work:

1. **Template-driven workflows**: Upfront LLM fills templates with research/tickets
2. **LangGraph integration**: Replace custom orchestrator with LangGraph
3. **Smaller task chunks**: Chunking logic isolated in workflows
4. **Better verification**: Verifier improvements don't affect other agents
5. **Custom implementations**: Swap out individual agents for different approaches

---

## Non-Goals

This refactoring does NOT:

- ❌ Design new features or capabilities
- ❌ Change user-facing commands or workflows
- ❌ Optimize performance (unless refactoring enables it)
- ❌ Replace LLM providers or models
- ❌ Implement LangGraph integration (just prepare for it)
- ❌ Change template formats (just decouple them)

---

## Open Questions

Document decisions as refactoring progresses:

1. **Schema versioning**: How to handle schema evolution?
2. **Error propagation**: How should agent errors propagate to orchestrator?
3. **Partial failures**: How to handle partial workflow completion?
4. **Checkpoint format**: What's the standard checkpoint data structure?
5. **Testing strategy**: Unit vs integration test boundaries?

---

## Notes

- Prototype location: `.docs/prototype/`
- Reference implementation: Current GSD in main repo
- This is REFACTORING - preserve existing functionality
- Focus on clean separation, not optimization
- Document all architectural decisions
