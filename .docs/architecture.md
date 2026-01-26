# Architecture

GSD is a meta-prompting system that orchestrates Claude Code through structured prompts, specialized agents, and state management.

## System Design

### Core Principle

**The orchestrator's job is coordination, not execution.**

GSD uses a **thin orchestrator + autonomous agents** pattern:

- **Orchestrators** (10-15% context): Discover, validate, spawn, collect
- **Agents** (fresh 200k context each): Execute work autonomously

This prevents context degradation in the main session while allowing deep work in subagents.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│  Slash Commands (/gsd:* ) + Interactive Prompts         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                     Command Layer                        │
│  • Validates arguments                                   │
│  • Loads @-referenced workflows                          │
│  • Delegates to workflows                                │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Workflow Layer                         │
│  • Reads project state                                   │
│  • Spawns specialized agents                             │
│  • Handles checkpoints                                   │
│  • Updates state                                         │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                     Agent Layer                          │
│  Specialized Agents (Fresh Context Each):               │
│  • gsd-planner       → Creates executable plans         │
│  • gsd-executor      → Runs plans, commits tasks        │
│  • gsd-verifier      → Validates deliverables           │
│  • gsd-debugger      → Diagnoses failures               │
│  • gsd-researcher    → Investigates domain              │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   State Management                       │
│  .planning/ directory structure:                         │
│  • PROJECT.md        → Vision & requirements            │
│  • ROADMAP.md        → Phase breakdown                  │
│  • STATE.md          → Current position & decisions     │
│  • phases/           → Plans, summaries, verification   │
└─────────────────────────────────────────────────────────┘
```

## File System Architecture

### Installation Structure

GSD can be installed globally or locally:

**Global Installation:**
```
~/.claude/
├── commands/gsd/          # Slash commands
│   └── *.md
├── agents/                # Agent definitions  
│   └── gsd-*.md
└── get-shit-done/         # Runtime files
    ├── workflows/
    ├── templates/
    └── references/
```

**Local Installation:**
```
./.claude/
└── [same structure as global]
```

When both exist, local overrides global (for project-specific customization).

### Project Structure

Each GSD project creates a `.planning/` directory:

```
.planning/
├── config.json              # GSD settings
├── PROJECT.md               # Project vision
├── REQUIREMENTS.md          # Detailed requirements
├── ROADMAP.md               # Phase structure
├── STATE.md                 # Session state
├── codebase/                # Codebase analysis (brownfield)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── INTEGRATIONS.md
│   ├── CONCERNS.md
│   └── TESTING.md
├── research/                # Domain research (optional)
│   └── [topic]/
│       ├── SUMMARY.md
│       ├── STACK.md
│       ├── FEATURES.md
│       ├── ARCHITECTURE.md
│       └── PITFALLS.md
├── phases/                  # Phase directories
│   ├── 01-foundation/
│   │   ├── 01-CONTEXT.md       # User decisions (from discuss-phase)
│   │   ├── 01-RESEARCH.md      # Research findings (from plan-phase)
│   │   ├── 01-01-PLAN.md       # Executable plan
│   │   ├── 01-01-SUMMARY.md    # Execution results
│   │   ├── 01-02-PLAN.md
│   │   ├── 01-02-SUMMARY.md
│   │   ├── 01-VERIFICATION.md  # Phase verification
│   │   └── 01-UAT.md           # User acceptance testing
│   └── 02-core-features/
│       └── [same pattern]
├── quick/                   # Quick mode tasks
│   ├── 001-fix-bug/
│   │   ├── PLAN.md
│   │   └── SUMMARY.md
│   └── 002-add-feature/
└── todos/                   # Captured ideas
    └── *.md
```

## Component Architecture

### 1. Commands (User Interface)

**Location:** `commands/gsd/*.md`

**Structure:**
```yaml
---
name: gsd:command-name
description: One-line description
argument-hint: "<required>" or "[optional]"  
allowed-tools: [Read, Write, Bash, Glob, Grep]
---
<objective>...</objective>
<execution_context>@workflow references</execution_context>
<context>...</context>
<process>...</process>
<success_criteria>...</success_criteria>
```

**Responsibilities:**
- Validate arguments
- Load workflow via @-references
- Delegate to workflow
- Present results to user

**Design:** Commands are thin wrappers. Heavy logic lives in workflows.

### 2. Workflows (Orchestration Logic)

**Location:** `get-shit-done/workflows/*.md`

**Key Workflows:**

| Workflow | Purpose |
|----------|---------|
| `execute-phase.md` | Wave-based parallel plan execution |
| `execute-plan.md` | Single plan execution (run by executor agent) |
| `discovery-phase.md` | Research before planning |
| `discuss-phase.md` | Capture user decisions |
| `verify-phase.md` | Goal-backward verification |
| `verify-work.md` | User acceptance testing |
| `diagnose-issues.md` | Debug failures |

**Structure:**
```xml
<purpose>What this accomplishes</purpose>
<process>
  <step name="step_name">...</step>
</process>
<success_criteria>...</success_criteria>
```

**Pattern:**
1. Load state (STATE.md, config.json)
2. Validate preconditions
3. Spawn agents for heavy work
4. Collect results
5. Update state
6. Commit (if configured)
7. Present next steps

### 3. Agents (Autonomous Execution)

**Location:** `agents/gsd-*.md`

**Agent Types:**

| Agent | Model | Purpose | Context Budget |
|-------|-------|---------|----------------|
| gsd-planner | opus/sonnet | Create executable plans | ~40% |
| gsd-executor | opus/sonnet | Execute plans, commit tasks | ~50% |
| gsd-verifier | sonnet/haiku | Verify deliverables | ~30% |
| gsd-debugger | sonnet | Diagnose failures | ~40% |
| gsd-researcher | opus/sonnet | Domain research | ~50% |
| gsd-plan-checker | sonnet | Validate plans | ~30% |
| gsd-roadmapper | opus | Create project roadmap | ~40% |
| gsd-codebase-mapper | sonnet | Analyze existing code | ~50% |

**Agent Structure:**
```yaml
---
name: gsd-agent-name
description: What this agent does
tools: [Read, Write, Bash, Glob, Grep]
color: green  # UI hint
---
<role>...</role>
<philosophy>...</philosophy>
<execution_flow>
  <step name="step_name">...</step>
</execution_flow>
<success_criteria>...</success_criteria>
```

**Key Patterns:**

1. **Self-contained context loading**
   - Agents load their own STATE.md, config, etc.
   - No reliance on parent context

2. **Structured returns**
   - Return markdown with specific format
   - Orchestrator parses and routes

3. **Fresh context per agent**
   - Each spawn gets 200k tokens
   - No accumulated context garbage

### 4. Templates (Output Structures)

**Location:** `get-shit-done/templates/*.md`

**Key Templates:**

| Template | Output |
|----------|--------|
| `project.md` | PROJECT.md |
| `roadmap.md` | ROADMAP.md |
| `state.md` | STATE.md |
| `phase-prompt.md` | PLAN.md |
| `summary.md` | SUMMARY.md |
| `verification-report.md` | VERIFICATION.md |
| `UAT.md` | UAT.md |

**Template Features:**
- Placeholders: `[Name]`, `{variable}`
- Frontmatter: YAML metadata
- Guidelines: Usage instructions
- Evolution notes: How template changes over lifecycle

### 5. References (Design Documentation)

**Location:** `get-shit-done/references/*.md`

**Key References:**

| Reference | Content |
|-----------|---------|
| `checkpoints.md` | Checkpoint patterns |
| `git-integration.md` | Commit conventions |
| `model-profiles.md` | Model selection |
| `planning-config.md` | Configuration schema |
| `tdd.md` | TDD workflows |
| `ui-brand.md` | Output formatting |
| `verification-patterns.md` | Goal-backward verification |

**Usage:**
- @-referenced by agents for deep knowledge
- Design documentation for contributors
- Pattern library for consistency

## Data Flow

### Project Initialization

```
User: /gsd:new-project
  ↓
Command: new-project.md
  ↓
Workflow: discovery-phase.md
  ↓
  1. Ask questions (AskUserQuestion)
  2. Spawn gsd-researcher agents (optional)
  3. Extract requirements
  4. Spawn gsd-roadmapper
  ↓
Creates: PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md
  ↓
Commits: docs(init): initialize project structure
```

### Phase Execution

```
User: /gsd:execute-phase 1
  ↓
Command: execute-phase.md
  ↓
Workflow: execute-phase.md (orchestrator mode)
  ↓
  1. Load STATE.md, config.json
  2. Discover plans (01-01-PLAN.md, 01-02-PLAN.md, ...)
  3. Group by wave (from frontmatter)
  4. For each wave:
     - Read plan files
     - Spawn gsd-executor agents (parallel)
     - Wait for completion
     - Verify SUMMARYs exist
  5. Spawn gsd-verifier
  6. Update ROADMAP.md, STATE.md
  ↓
Creates: Multiple SUMMARY.md files, VERIFICATION.md
Commits: Per-task commits + docs(01): complete phase execution
```

### Checkpoint Handling

```
Executor agent hits checkpoint:human-verify
  ↓
Agent returns structured checkpoint message:
  - Completed tasks table (with commits)
  - Current task + blocker
  - Checkpoint details
  - What's awaited
  ↓
Orchestrator presents to user
  ↓
User responds: "approved" / "done" / issues
  ↓
Orchestrator spawns continuation agent:
  - Same plan
  - Completed tasks from checkpoint
  - Resume point specified
  - User response included
  ↓
Continuation agent:
  1. Verifies previous commits
  2. Continues from resume point
  3. May hit another checkpoint (repeat)
  4. Or completes plan
```

## State Management

### STATE.md Structure

```markdown
# Project State

## Current Position
Phase: 3 of 5 (Database Layer)
Plan: 2 of 4
Status: In progress
Last activity: 2026-01-26 - Completed 03-02-PLAN.md

Progress: ████████░░░░░░░░░░░░ 40%

## Decisions Made
| Decision | Rationale | Phase | Date |
|----------|-----------|-------|------|
| Use Prisma ORM | Type-safe, migrations, works with Edge | 03 | 2026-01-25 |

## Issues & Concerns
| Issue | Impact | Status | Notes |
|-------|--------|--------|-------|
| None | - | - | - |

## Session Continuity
Last session: 2026-01-26 14:30 UTC
Stopped at: Completed 03-02-PLAN.md
Resume file: None
```

**Purpose:**
- Persistent memory across sessions
- Decision tracking
- Progress visualization
- Resume points

**Updated by:**
- Executor agents (after each plan)
- Orchestrators (after each phase)

### Config Schema

```json
{
  "mode": "interactive",           // "yolo" or "interactive"
  "depth": "standard",             // "quick", "standard", "comprehensive"
  "model_profile": "balanced",     // "quality", "balanced", "budget"
  "workflow": {
    "research": true,              // Research before planning?
    "plan_check": true,            // Verify plans before execution?
    "verifier": true               // Verify after execution?
  },
  "parallelization": {
    "enabled": true                // Run independent plans in parallel?
  },
  "planning": {
    "commit_docs": true            // Commit .planning/ to git?
  }
}
```

## Multi-Agent Orchestration

### Wave-Based Execution

Plans are grouped into waves based on dependencies:

```
Wave 1 (parallel):
  ├─ 01-01-PLAN.md (User model)
  └─ 01-02-PLAN.md (Product model)
        ↓
Wave 2 (parallel):
  ├─ 01-03-PLAN.md (User API - depends on 01-01)
  └─ 01-04-PLAN.md (Product API - depends on 01-02)
        ↓
Wave 3 (sequential):
  └─ 01-05-PLAN.md (Dashboard - depends on 01-03, 01-04)
```

**Implementation:**
1. Planner assigns wave numbers during planning
2. Executor reads wave from frontmatter
3. Groups plans by wave
4. Spawns all autonomous plans in wave simultaneously
5. Waits for wave completion
6. Proceeds to next wave

**Benefits:**
- Maximum parallelism
- Clean dependency resolution
- Predictable execution order
- No race conditions (file ownership)

### Agent Spawning

```javascript
// Conceptual pattern (actual is via Claude Code Task tool)

// Orchestrator (10% context)
const plans = discoverPlans(phaseDir);
const waves = groupByWave(plans);

for (const wave of waves) {
  // Read files once, inline to subagent prompts
  const planContents = wave.plans.map(p => fs.readFileSync(p.path));
  const stateContent = fs.readFileSync('.planning/STATE.md');
  
  // Spawn all agents in wave simultaneously
  const agents = wave.plans.map(plan => 
    spawnAgent('gsd-executor', {
      prompt: buildExecutorPrompt(plan, stateContent),
      model: getModelForProfile('executor')
    })
  );
  
  // Wait for completion (Task tool blocks)
  const results = await Promise.all(agents);
  
  // Verify SUMMARYs exist
  verifyCompletion(results);
}
```

**Key points:**
- Orchestrator stays thin (reads, spawns, waits)
- Agents get inlined content (no @-references across Task boundaries)
- Fresh 200k context per agent
- Parallel execution within waves

## Context Engineering

### Context Budget Management

| Component | Target | Max |
|-----------|--------|-----|
| Orchestrator | 10-15% | 20% |
| Planner agent | 30-40% | 50% |
| Executor agent | 40-50% | 60% |
| Verifier agent | 20-30% | 40% |

**Strategies:**

1. **Aggressive atomicity**: More plans, smaller scope
2. **Intelligent summarization**: Frontmatter for quick scanning
3. **Lazy loading**: Read only what's needed
4. **Fresh agents**: Subagents start at 0% context

### File Size Limits

Enforced by planner to prevent context bloat:

| File | Max Size | Why |
|------|----------|-----|
| PLAN.md | ~3 tasks | Fits in 50% executor context |
| SUMMARY.md | ~2 pages | Quick reference, not full history |
| CONTEXT.md | ~3 pages | User decisions, not spec |
| RESEARCH.md | ~5 pages | Key findings, not full research |

**Principle:** Quality degrades beyond these sizes. Split instead of growing.

## Progressive Disclosure

Information flows through layers:

```
Command (What?)
  ↓ @-reference
Workflow (How?)
  ↓ @-reference  
Template (Structure?)
  ↓ @-reference
Reference (Why?)
```

**Example:**
```
/gsd:execute-phase
  ↓ @workflows/execute-phase.md
Orchestrator reads phases, spawns executors
  ↓ @workflows/execute-plan.md
Executor reads tasks, commits per task
  ↓ @references/checkpoints.md
Checkpoint patterns for verification
```

Each layer adds detail without overwhelming early readers.

## Git Integration

### Commit Strategy

**Per-Task Commits:**
```
feat(01-02): implement user registration endpoint

- Add POST /api/auth/register route
- Validate email format and uniqueness
- Hash password with bcrypt
- Return JWT in httpOnly cookie
```

**Per-Plan Commits:**
```
docs(01-02): complete user authentication plan

Tasks completed: 3/3
- Create registration endpoint
- Add login endpoint
- Implement session middleware

SUMMARY: .planning/phases/01-foundation/01-02-SUMMARY.md
```

**Phase Commits:**
```
docs(phase-01): complete phase execution

Phase 01: Foundation
- 4 plans executed
- User auth, database, API setup complete

VERIFICATION: .planning/phases/01-foundation/01-VERIFICATION.md
```

### Benefits

1. **Git bisect** finds exact failing task
2. **Git revert** on specific task, not whole phase
3. **Git blame** traces line to task context
4. **Git history** as context for future Claude sessions
5. **Clear audit trail** for AI-generated code

## Extensibility

### Adding Commands

1. Create `commands/gsd/new-command.md`
2. Follow frontmatter schema
3. Delegate to workflow via @-reference
4. Install/update GSD

### Adding Agents

1. Create `agents/gsd-new-agent.md`
2. Define tools, role, execution flow
3. Use in workflow via Task tool
4. Add to model profile mapping

### Adding Workflows

1. Create `get-shit-done/workflows/new-workflow.md`
2. Structure with `<step>` elements
3. Reference from commands
4. Document in this file

### Customization

**Local Overrides:**
- Install GSD locally: `npx get-shit-done-cc --local`
- Modify files in `./.claude/`
- Local version takes precedence over global

**Project-Specific:**
- Modify `.planning/config.json`
- Add custom templates
- Adjust model profiles

## Performance

### Context Window Usage

Typical phase execution:

```
Main context (orchestrator):
  0% ─ Load state
  5% ─ Discover plans  
 10% ─ Spawn agents
 10% ─ Wait (agents work in parallel)
 15% ─ Collect results
 20% ─ Update state
```

Agents work in parallel with fresh contexts. Main session stays responsive.

### Parallelization

Phase with 4 plans, 2 waves:

**Without parallelization:**
- Plan 1: 30 min
- Plan 2: 30 min
- Plan 3: 30 min
- Plan 4: 30 min
- **Total: 120 min**

**With parallelization:**
- Wave 1 (Plans 1-2 parallel): 30 min
- Wave 2 (Plans 3-4 parallel): 30 min
- **Total: 60 min**

Real-world speedup: 40-60% reduction in wall time.

## Error Handling

### Failure Recovery

**Agent fails during execution:**
1. No SUMMARY.md created
2. Orchestrator detects missing SUMMARY
3. Reports failure with agent output
4. User decides: retry, skip, or debug

**Checkpoint fails to resolve:**
1. User repeatedly reports issues
2. Orchestrator offers: skip plan or abort phase
3. STATE.md updated with partial progress
4. User can resume later

**Context limit hit:**
1. Claude stops mid-execution
2. STATE.md captures position
3. User runs command again
4. Discovers completed plans, skips them
5. Resumes from next incomplete plan

## Security

### Permissions

GSD requires:
- **File system**: Read/write `.planning/`, project files
- **Git**: Commit, tag, log, status (not push)
- **Shell**: Date, echo, grep, ls (basic tools)

GSD does NOT:
- Push to remote automatically
- Run with sudo/elevated privileges
- Execute arbitrary user code
- Store credentials (except in .env files user creates)

### Safe Defaults

- `.planning/` can be gitignored (sensitive projects)
- `commit_docs: false` skips committing plans
- Interactive mode requires approval at each step
- Deviation rules prevent silent breakage

## Next Steps

- **Workflows**: Deep dive into [Workflows](./workflows.md)
- **Agents**: Learn about [Agents](./agents.md)
- **Commands**: Reference [Commands](./commands.md)
