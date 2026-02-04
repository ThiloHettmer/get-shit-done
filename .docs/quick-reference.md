# Quick Reference

Fast lookup for common GSD patterns and commands.

## Workflow Sequence

```bash
# 1. Initialize project
/gsd:new-project

# 2. For each phase:
/gsd:discuss-phase 1    # Capture your vision (optional but recommended)
/gsd:plan-phase 1       # Create executable plans
/gsd:execute-phase 1    # Run all plans with verification
/gsd:verify-work 1      # Manual user acceptance testing (optional)

# 3. Complete milestone
/gsd:complete-milestone
/gsd:new-milestone      # Start next version
```

## Commands CheatSheet

### Core Workflow
| Command | When | What it does |
|---------|------|--------------|
| `/gsd:new-project` | Starting new | Questions → Research → Requirements → Roadmap |
| `/gsd:discuss-phase [N]` | Before planning | Capture your implementation vision |
| `/gsd:plan-phase <N>` | After discussion | Research → Create atomic plans |
| `/gsd:execute-phase <N>` | After planning | Wave-based parallel execution |
| `/gsd:verify-work [N]` | After execution | Manual UAT with auto-fix planning |
| `/gsd:complete-milestone` | All phases done | Archive → Tag → Prepare next |

### Navigation
| Command | What it shows |
|---------|---------------|
| `/gsd:progress` | Current position, next steps |
| `/gsd:help` | All commands with descriptions |

### Phase Management
| Command | What it does |
|---------|--------------|
| `/gsd:add-phase` | Append phase to roadmap |
| `/gsd:insert-phase [N]` | Insert urgent work between phases |
| `/gsd:remove-phase [N]` | Remove future phase |

### Brownfield
| Command | When | What it does |
|---------|------|--------------|
| `/gsd:map-codebase` | Existing codebase | Analyze stack, architecture, conventions |

### Quick Mode
| Command | When | What it does |
|---------|------|--------------|
| `/gsd:quick` | Ad-hoc tasks | Fast path: plan → execute → commit |

### Utilities
| Command | What it does |
|---------|--------------|
| `/gsd:settings` | Configure GSD (mode, depth, profiles) |
| `/gsd:set-profile <profile>` | Switch model profile (quality/balanced/budget) |
| `/gsd:debug [desc]` | Systematic debugging with state |
| `/gsd:add-todo [desc]` | Capture idea for later |

## File Structure

```
.planning/
├── config.json                  # GSD settings
├── PROJECT.md                   # Vision & requirements
├── REQUIREMENTS.md              # Detailed requirements  
├── ROADMAP.md                   # Phase breakdown
├── STATE.md                     # Current position & decisions
├── codebase/                    # Brownfield analysis
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   └── ...
├── research/                    # Domain research (optional)
│   └── [topic]/
├── phases/                      # Phase directories
│   ├── 01-foundation/
│   │   ├── 01-CONTEXT.md        # User decisions
│   │   ├── 01-RESEARCH.md       # Discovery findings
│   │   ├── 01-01-PLAN.md        # Executable plan
│   │   ├── 01-01-SUMMARY.md     # Execution results
│   │   ├── 01-VERIFICATION.md   # Phase verification
│   │   └── 01-UAT.md            # User acceptance testing
│   └── 02-core/
└── quick/                       # Quick mode tasks
    └── 001-task-name/
```

## Plan Frontmatter

```yaml
---
phase: 01-foundation              # Phase ID
plan: 02                          # Plan number
type: execute                     # or "tdd"
wave: 2                           # Execution wave
depends_on: ["01-01"]             # Dependencies
files_modified:                   # Files touched
  - "src/app/api/auth.ts"
autonomous: true                  # false if checkpoints
gap_closure: false                # true if fixing gaps

must_haves:                       # Goal-backward verification
  truths:
    - "User can register"
  artifacts:
    - path: "src/app/api/auth.ts"
      provides: "Auth endpoints"
  key_links:
    - from: "src/components/Form.tsx"
      to: "/api/auth"
      via: "fetch"
---
```

## Task Types

### Auto Task
```xml
<task type="auto">
  <name>Create user model</name>
  <files>src/models/user.ts</files>
  <action>Specific instructions...</action>
  <verify>npm run build succeeds</verify>
  <done>User model exported with auth fields</done>
</task>
```

### TDD Task
```xml
<task type="auto" tdd="true">
  <name>Implement validation</name>
  <files>src/utils/validate.ts, src/utils/validate.test.ts</files>
  <behavior>Given X → expect Y</behavior>
  <implementation>How to make tests pass</implementation>
</task>
```

### Checkpoint - Human Verify
```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Deployed to https://app.vercel.app</what-built>
  <how-to-verify>
    1. Visit URL
    2. Test feature X
    3. Verify behavior Y
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### Checkpoint - Decision
```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Choose database</decision>
  <context>Why it matters</context>
  <options>
    <option id="postgres">
      <name>PostgreSQL</name>
      <pros>Mature, ACID</pros>
      <cons>Setup overhead</cons>
    </option>
  </options>
  <resume-signal>Select: postgres, mysql, ...</resume-signal>
</task>
```

## Commit Conventions

```bash
# Task commit
git commit -m "feat(01-02): implement user registration

- Add POST /api/auth/register endpoint
- Validate email uniqueness
- Hash password with bcrypt
- Return JWT in httpOnly cookie"

# Plan completion (metadata)
git commit -m "docs(01-02): complete user authentication plan

Tasks completed: 3/3
- Registration endpoint
- Login endpoint  
- Session middleware

SUMMARY: .planning/phases/01-foundation/01-02-SUMMARY.md"

# Phase completion
git commit -m "docs(phase-01): complete phase execution

Phase 01: Foundation
- 4 plans executed
- Auth, database, API setup complete

VERIFICATION: .planning/phases/01-foundation/01-VERIFICATION.md"
```

Types: `feat`, `fix`, `test`, `refactor`, `docs`, `chore`

## Configuration

`.planning/config.json`:

```json
{
  "mode": "interactive",           // "yolo" or "interactive"
  "depth": "standard",             // "quick", "standard", "comprehensive"
  "model_profile": "balanced",     // "quality", "balanced", "budget"
  "workflow": {
    "research": true,              // Research before planning?
    "plan_check": true,            // Verify plans?
    "verifier": true               // Verify after execution?
  },
  "parallelization": {
    "enabled": true                // Parallel execution?
  },
  "planning": {
    "commit_docs": true            // Commit .planning/ files?
  }
}
```

## Model Profiles

| Agent | quality | balanced | budget |
|-------|---------|----------|--------|
| Planner | Opus | Opus | Sonnet |
| Executor | Opus | Sonnet | Sonnet |
| Verifier | Sonnet | Sonnet | Haiku |

## Context Budget

| Component | Target | Max |
|-----------|--------|-----|
| Orchestrator | 10% | 20% |
| Planner | 30% | 50% |
| Executor | 40% | 50% |
| Verifier | 20% | 40% |

**Rule:** Plans = 2-3 tasks max to stay under 50% context.

## Quality Curve

| Context | Quality | State |
|---------|---------|-------|
| 0-30% | PEAK | Thorough |
| 30-50% | GOOD | Solid |
| 50-70% | DEGRADING | Rushed |
| 70%+ | POOR | Minimal |

**Stop BEFORE degradation. Split instead of growing.**

## Deviation Rules

Applied automatically during execution:

| Rule | Trigger | Action |
|------|---------|--------|
| 1 | Bug found | Fix immediately, track |
| 2 | Missing critical functionality | Add immediately, track |
| 3 | Blocker prevents completion | Fix immediately, track |
| 4 | Architectural change needed | STOP, return checkpoint |

## Checkpoint Patterns

**Golden rules:**
1. If Claude can run it, Claude runs it
2. Claude sets up verification environment
3. User only does what requires human judgment
4. Secrets from user, automation from Claude

**Usage:**
- 90% - human-verify (visual/functional checks)
- 9% - decision (implementation choices)
- 1% - human-action (truly unavoidable manual steps)

## Wave-Based Execution

Plans grouped by dependencies:

```
Wave 1 (parallel):
  01-01-PLAN.md (no dependencies)
  01-02-PLAN.md (no dependencies)
    ↓
Wave 2 (parallel):
  01-03-PLAN.md (depends on 01-01)
  01-04-PLAN.md (depends on 01-02)
    ↓
Wave 3 (sequential):
  01-05-PLAN.md (depends on 01-03, 01-04)
```

Wave number computed during planning, read from frontmatter during execution.

## Goal-Backward Verification

1. **State the goal** (outcome, not task)
2. **Derive truths** (what must be TRUE?)
3. **Derive artifacts** (what must EXIST?)
4. **Derive wiring** (what must be CONNECTED?)
5. **Identify key links** (where will this break?)

Output: `must_haves` in plan frontmatter.

## Common Patterns

### Fresh Agent Spawn

```python
# Read files BEFORE spawning (@ doesn't work across Task boundaries)
plan_content = read('.planning/phases/01-*/01-01-PLAN.md')
state_content = read('.planning/STATE.md')

# Inline content to agent
spawn_agent(f"""
<context>
Plan:
{plan_content}

State:
{state_content}
</context>

Execute this plan...
""")
```

### Checkpoint Continuation

```python
# Agent hits checkpoint, returns structured message
checkpoint = agent_result

# Orchestrator presents to user
user_response = present(checkpoint.details)

# Spawn FRESH continuation agent (not resume)
continuation = spawn_agent(
    prompt=build_continuation(
        plan=plan,
        completed=checkpoint.completed_tasks,
        resume_from=checkpoint.current_task,
        user_response=user_response
    )
)
```

### Gap Closure

```python
# After verification finds gaps
if verification.status == 'gaps_found':
    # User: /gsd:plan-phase 1 --gaps
    gaps = read_verification_gaps()
    new_plans = create_gap_closure_plans(gaps)
    
    # User: /gsd:execute-phase 1 --gaps-only
    execute(plans_with_gap_closure_true)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Commands not found | Restart Claude Code, verify `~/.claude/commands/gsd/` exists |
| Context degradation | Plans too large - split into more plans (2-3 tasks max) |
| Agent fails | Check SUMMARY.md missing, see agent output for errors |
| Checkpoint not resuming | Expected - spawns fresh agent with explicit state |
| Plans execute sequentially | Check wave numbers - same wave = parallel |
| STATE.md missing | Run `/gsd:new-project` or reconstruct from artifacts |

## Anti-Patterns

### Don't Do This

❌ Plans with >3 tasks  
❌ Generic XML tags (`<section>`, `<item>`)  
❌ Vague tasks ("add authentication")  
❌ Temporal language ("we changed X")  
❌ Enterprise patterns (sprint ceremonies, story points)  
❌ Human time estimates (days, weeks)  
❌ Asking user to run CLI commands (Claude does this)

### Do This Instead

✅ Plans with 2-3 tasks  
✅ Semantic XML tags (`<objective>`, `<action>`)  
✅ Specific tasks ("Create JWT login endpoint with jose library")  
✅ Current state only ("Uses JWT for auth")  
✅ Solo developer patterns  
✅ Context budget estimates (%, tokens)  
✅ Claude runs CLI, user verifies results

## Common Commands

```bash
# Install/update
npx get-shit-done-cc@latest

# Start project
/gsd:new-project

# Work on phase
/gsd:discuss-phase 1
/gsd:plan-phase 1
/gsd:execute-phase 1
/gsd:verify-work 1

# Quick fix
/gsd:quick

# Check status
/gsd:progress

# Debug
/gsd:debug "Login returns 500"

# Settings
/gsd:settings
/gsd:set-profile quality
```

## Resources

- **Main README**: [../README.md](../README.md)
- **Style Guide**: [../GSD-STYLE.md](../GSD-STYLE.md)
- **Contributing**: [../CONTRIBUTING.md](../CONTRIBUTING.md)
- **Architecture**: [./architecture.md](./architecture.md)
- **Core Concepts**: [./core-concepts.md](./core-concepts.md)
- **Workflows**: [./workflows.md](./workflows.md)
- **XML Format**: [./xml-format.md](./xml-format.md)
