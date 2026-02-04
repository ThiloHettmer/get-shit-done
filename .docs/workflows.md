# Workflows

Workflows are the orchestration logic of GSD. They coordinate agents, manage state, and handle user interactions.

## Workflow Architecture

### Hierarchy

```
Commands (thin wrappers)
  ↓ @-reference
Workflows (orchestration logic)
  ↓ spawn agents
Agents (autonomous execution)
```

**Commands** validate and present.  
**Workflows** coordinate and route.  
**Agents** execute and deliver.

### Common Pattern

All workflows follow this structure:

```xml
<purpose>What this accomplishes</purpose>

<required_reading>
Files to load before starting
</required_reading>

<process>
  <step name="step_1" priority="first">
    Specific instructions
  </step>
  <step name="step_2">
    More instructions
  </step>
</process>

<success_criteria>
When is workflow complete?
</success_criteria>
```

## Core Workflows

### 1. execute-phase.md

**Purpose:** Execute all plans in a phase using wave-based parallel execution.

**When:** After `/gsd:plan-phase` creates plans.

**Flow:**

```
1. load_project_state
   └─ Read STATE.md, config.json
   
2. validate_phase
   └─ Confirm phase exists, has plans
   
3. discover_plans
   └─ List all PLAN.md files
   └─ Check for SUMMARY.md (skip if exists)
   └─ Extract wave number from frontmatter
   
4. group_by_wave
   └─ Group plans by wave number
   └─ Report wave structure to user
   
5. execute_waves (for each wave)
   ├─ Read all plan files in wave
   ├─ Spawn gsd-executor agents (parallel)
   ├─ Wait for completion
   ├─ Verify SUMMARYs exist
   └─ Report what was built
   
6. verify_phase_goal
   └─ Spawn gsd-verifier
   └─ Check must-haves against codebase
   └─ Route by status (passed/gaps_found/human_needed)
   
7. update_roadmap
   └─ Mark phase complete
   └─ Commit (if commit_docs: true)
   
8. offer_next
   └─ Show next phase or milestone completion
```

**Key Features:**

- **Wave-based execution**: Plans in same wave run in parallel
- **Checkpoint handling**: Pause for user verification, resume with fresh agent
- **Gap closure**: After verification, can create/execute gap closure plans
- **Resumable**: Re-run command skips completed plans

**Parallelization:**

```bash
# Phase with 4 plans across 2 waves:
# Wave 1: Plans 01, 02 (parallel)
# Wave 2: Plans 03, 04 (parallel)

Wave 1 start:
├─ Spawn executor for 01-01-PLAN.md
├─ Spawn executor for 01-02-PLAN.md
└─ Wait for both

Wave 1 complete → Wave 2 start:
├─ Spawn executor for 01-03-PLAN.md
├─ Spawn executor for 01-04-PLAN.md
└─ Wait for both

Phase complete → Verify → Update roadmap
```

**Context Efficiency:**

- Orchestrator: ~10-15%
- Agents: Fresh 200k each
- Main session stays responsive

### 2. execute-plan.md

**Purpose:** Execute a single plan - run by executor agent.

**When:** Spawned by execute-phase orchestrator or quick mode.

**Flow:**

```
1. load_project_state
   └─ Read STATE.md, config.json
   
2. load_plan
   └─ Parse frontmatter, tasks, verification
   └─ Load @-referenced files
   
3. record_start_time
   └─ Capture for duration tracking
   
4. determine_execution_pattern
   ├─ Fully autonomous (no checkpoints)
   ├─ Has checkpoints (pause-resume pattern)
   └─ Continuation (resume from checkpoint)
   
5. execute_tasks (for each task)
   ├─ type="auto" → execute, commit
   ├─ type="checkpoint:*" → STOP, return checkpoint
   ├─ TDD task → RED-GREEN-REFACTOR cycle
   └─ Apply deviation rules (auto-fix bugs/blockers)
   
6. create_summary
   └─ Use summary.md template
   └─ Document tasks, commits, deviations
   
7. update_state
   └─ Update position, decisions, issues
   
8. final_commit
   └─ Commit SUMMARY.md and STATE.md (if configured)
```

**Deviation Rules:**

Automatically applied during execution:

| Rule | Trigger | Action |
|------|---------|--------|
| 1 | Bug found | Fix immediately, track |
| 2 | Missing critical functionality | Add immediately, track |
| 3 | Blocker prevents task completion | Fix immediately, track |
| 4 | Architectural change needed | STOP, return checkpoint |

**TDD Execution:**

```xml
<task type="auto" tdd="true">
  <name>Implement email validation</name>
  <files>src/utils/validate.ts, src/utils/validate.test.ts</files>
  <behavior>
    Given email string:
    - Valid format → true
    - Invalid format → false
    - Empty string → false
  </behavior>
  <implementation>
    Use regex pattern for RFC 5322 basic validation
  </implementation>
</task>
```

Executor flow:
1. **RED**: Write failing test, verify it fails, commit
2. **GREEN**: Implement to pass, verify it passes, commit
3. **REFACTOR**: Clean up if needed, commit if changes

Result: 2-3 atomic commits per TDD task.

### 3. verify-phase.md

**Purpose:** Verify phase achieved its goal using goal-backward methodology.

**When:** After execute-phase completes all plans.

**Flow:**

```
1. load_phase_context
   ├─ Read phase goal from ROADMAP.md
   ├─ Load all plan frontmatter (must_haves)
   └─ Aggregate truths, artifacts, key_links
   
2. verify_truths
   └─ For each truth: can user actually do this?
   
3. verify_artifacts
   ├─ Check files exist
   ├─ Verify min_lines if specified
   ├─ Check exports if specified
   └─ Verify contains patterns if specified
   
4. verify_key_links
   └─ Search for connection patterns
   └─ Confirm wiring exists
   
5. identify_gaps
   └─ Truth not verifiable → gap
   └─ Artifact missing/incomplete → gap
   └─ Key link not found → gap
   
6. determine_status
   ├─ All verified → "passed"
   ├─ Gaps found → "gaps_found"
   └─ Needs human testing → "human_needed"
   
7. write_verification_report
   └─ Create {phase}-VERIFICATION.md
   
8. return_result
   └─ Structured report with status and gaps
```

**Status Routing:**

```
passed:
  → Phase complete, continue to next

gaps_found:
  → Offer /gsd:plan-phase {X} --gaps
  → Creates gap closure plans
  → User runs /gsd:execute-phase {X} --gaps-only

human_needed:
  → Present verification checklist
  → User tests manually
  → If issues → treat as gaps_found
```

**Example Gap:**

```yaml
- truth: "User can send a message"
  status: gap
  reason: "API endpoint exists but not wired to UI"
  artifacts:
    - path: "src/app/api/chat/route.ts"
      status: exists
      issue: null
    - path: "src/components/Chat.tsx"
      status: exists
      issue: "No fetch call to /api/chat"
  missing:
    - "Add onSubmit handler to form"
    - "Call fetch('/api/chat', {method: 'POST', body})"
    - "Update messages state with response"
```

### 4. discover-phase.md

**Purpose:** Research domain before planning.

**When:** 
- `/gsd:new-project` (optional but recommended)
- `/gsd:research-phase` (explicit research)
- `/gsd:plan-phase` triggers if phase needs discovery

**Flow:**

```
1. understand_domain
   └─ Parse phase description
   └─ Extract key technologies, patterns, integrations
   
2. formulate_questions
   └─ What standards exist?
   └─ What libraries are popular?
   └─ What are common patterns?
   └─ What are known pitfalls?
   
3. spawn_researchers (parallel)
   ├─ gsd-phase-researcher: "Stack & Tools"
   ├─ gsd-phase-researcher: "Features & Patterns"
   ├─ gsd-phase-researcher: "Architecture"
   └─ gsd-phase-researcher: "Pitfalls"
   
4. synthesize_findings
   └─ Spawn gsd-research-synthesizer
   └─ Consolidate findings into RESEARCH.md
   
5. create_discovery_document
   └─ {phase}-RESEARCH.md in phase directory
```

**Discovery Levels:**

| Level | When | Time | Output |
|-------|------|------|--------|
| 0 - Skip | Pure internal work | 0 min | None |
| 1 - Quick | Single library, low risk | 2-5 min | Context only |
| 2 - Standard | 2-3 options, medium risk | 15-30 min | RESEARCH.md |
| 3 - Deep | Architectural, high risk | 60+ min | RESEARCH.md |

**RESEARCH.md Structure:**

```markdown
# Phase Research: {Name}

## Standard Stack
Libraries and tools commonly used:
- {library}: {why, when to use}

## Architecture Patterns
Common approaches:
- {pattern}: {description, pros/cons}

## Don't Hand-Roll
Things to use libraries for:
- {concern}: Use {library} because {reason}

## Common Pitfalls
Known issues to avoid:
- {pitfall}: {how to avoid}
```

### 5. discuss-phase.md

**Purpose:** Capture user's implementation vision before planning.

**When:** After roadmap created, before planning.

**Flow:**

```
1. load_phase_goal
   └─ Read from ROADMAP.md
   
2. analyze_gray_areas
   └─ Identify decisions user should make
   └─ Visual features → layout, density, interactions
   └─ APIs/CLIs → response format, error handling
   └─ Content → structure, tone, depth
   └─ Organization → grouping, naming, exceptions
   
3. ask_progressive_questions
   └─ Present gray areas as options
   └─ Use AskUserQuestion tool
   └─ Drill down based on responses
   └─ Continue until user satisfied
   
4. create_context_document
   └─ {phase}-CONTEXT.md in phase directory
   └─ Essential features (user's priorities)
   └─ Implementation details (locked decisions)
   └─ Boundaries (explicitly out of scope)
```

**Example Questions:**

```
Gray Area: Layout for task list

Options:
A) Table view - Dense, sortable, keyboard nav
B) Card grid - Visual, responsive, drag-drop
C) Kanban board - Status columns, drag between
D) Something else - Describe your vision

User selects: B - Card grid

Follow-up: Card grid details

Density:
A) Compact - 3-4 cards per row, minimal spacing
B) Comfortable - 2-3 cards per row, medium spacing
C) Spacious - 1-2 cards per row, generous spacing

User selects: B - Comfortable

Empty state:
A) Show placeholder cards with "Add task" prompt
B) Show illustration + "Get started" message
C) Show tutorial/onboarding flow
D) Just show "No tasks yet" message

User selects: A - Placeholder cards
```

**CONTEXT.md Output:**

```markdown
# Phase Context: Task Management UI

## Essential Features

**Card grid layout:**
- 2-3 cards per row on desktop
- Single column on mobile
- Medium spacing between cards
- Responsive breakpoints at 768px, 1024px

## Implementation Details

**Empty state:**
- Show 3 placeholder cards
- Each with dashed border
- "Add your first task" in center card
- Click any placeholder → create modal

**Card interactions:**
- Hover: subtle shadow + scale(1.02)
- Click card → expand in modal
- Click anywhere outside → collapse
- No drag-drop (deferred to v2)

## Boundaries

**Out of scope for this phase:**
- Drag and drop reordering
- Bulk actions (select multiple)
- Advanced filtering (tags, dates)
- Keyboard shortcuts (beyond tab/enter)
```

### 6. verify-work.md

**Purpose:** Manual user acceptance testing with automated fix planning.

**When:** After execute-phase and verify-phase complete.

**Flow:**

```
1. load_phase_deliverables
   └─ Extract from VERIFICATION.md or plans
   └─ Convert to testable items
   
2. present_testable_items
   └─ One at a time
   └─ "Can you do X? (yes/no/describe issue)"
   
3. for_each_response
   ├─ "yes" → mark passed, continue
   ├─ "no" → ask for description
   └─ description → mark failed with details
   
4. diagnose_failures
   └─ Spawn gsd-debugger for each failure
   └─ Analyze root cause
   └─ Propose fix
   
5. create_gap_closure_plans
   └─ Convert fixes to executable plans
   └─ Ready for /gsd:execute-phase {X} --gaps-only
   
6. write_uat_document
   └─ {phase}-UAT.md with results
```

**Example UAT Flow:**

```
Deliverable 1: User can register with email
> Can you register with email? (yes/no/describe issue)

User: no - form submits but shows "500 error"

[Spawning debugger...]

Debugger found:
- Root cause: Missing unique constraint on users.email
- SQL error on duplicate email insert
- Error not handled, returns 500

Fix plan created: 01-05-PLAN.md
- Add unique constraint to schema
- Update registration endpoint error handling
- Return 400 with "Email already exists" message

Continue testing? (y/n)
```

**UAT.md Output:**

```markdown
# User Acceptance Testing: Authentication

**Status:** diagnosed  
**Date:** 2026-01-26  
**Tester:** User

## Results

| # | Deliverable | Result | Notes |
|---|-------------|--------|-------|
| 1 | User can register | ✗ FAIL | 500 error on submit |
| 2 | User can log in | ✓ PASS | Works as expected |
| 3 | User can log out | ✓ PASS | Session cleared |

## Failed Items

### 1. User can register

**Issue:** Form submits but returns 500 error

**Root Cause:**
- Missing unique constraint on users.email
- Duplicate email causes SQL error
- Error not caught, returns generic 500

**Fix Plan:** 01-05-PLAN.md
- Add unique constraint to schema
- Update error handling in registration endpoint
- Return 400 with specific message

## Next Steps

Run `/gsd:execute-phase 1 --gaps-only` to execute fix plans.
```

### 7. diagnose-issues.md

**Purpose:** Systematic debugging with persistent state.

**When:**
- `/gsd:debug` command
- `/gsd:verify-work` encounters failures
- User reports bug after phase complete

**Flow:**

```
1. understand_issue
   └─ Get description from user
   └─ Classify: error, unexpected behavior, performance
   
2. gather_context
   ├─ Recent commits (git log)
   ├─ Modified files (git diff)
   ├─ Logs (if available)
   └─ Related plans/summaries
   
3. form_hypotheses
   └─ What could cause this?
   └─ What changed recently?
   └─ What assumptions might be wrong?
   
4. test_hypotheses
   └─ Read relevant code
   └─ Check for common issues
   └─ Run verification commands
   
5. identify_root_cause
   └─ Specific file + line/function
   └─ Why it's broken
   └─ How it manifests
   
6. propose_fix
   └─ Specific changes needed
   └─ Why this fixes it
   └─ How to verify fix
   
7. create_fix_plan (optional)
   └─ If user wants, create executable plan
   └─ Ready for /gsd:execute-phase or /gsd:quick
   
8. create_debug_document
   └─ .planning/debug/DEBUG-{N}.md
   └─ Full diagnostic report
```

**Example Debug Session:**

```
Issue: "Login works but session expires immediately"

Hypotheses:
1. Cookie not being set correctly
2. Session duration misconfigured  
3. Cookie being cleared on response

Testing:
- Check browser DevTools → Cookie exists but expires: Session
- Check login endpoint → maxAge: 900000 (15 min)
- Check response headers → Set-Cookie: httpOnly, secure, sameSite

Root Cause Found:
- Cookie expires set to "Session" (browser session)
- maxAge in code: 900000ms (correct)
- But expires attribute not set on cookie
- Next.js Edge runtime requires explicit expires

Fix:
- Add expires: new Date(Date.now() + 900000) to cookie options
- Verify cookie persists with expires timestamp

File: src/app/api/auth/login/route.ts
Line: 42 - cookies().set() call
```

### 8. complete-milestone.md

**Purpose:** Archive milestone, tag release, prepare for next.

**When:** After all phases in milestone complete.

**Flow:**

```
1. verify_milestone_complete
   └─ Check all phases marked complete
   └─ Verify no pending TODOs marked "blocking"
   
2. create_milestone_archive
   └─ Copy current ROADMAP.md to archive
   └─ milestone-archive.md
   
3. update_project_file
   └─ Move active requirements to validated
   └─ Update "What This Is" if needed
   
4. create_git_tag
   └─ Tag format: v{major}.{minor}.{patch}
   └─ Annotation: milestone summary
   
5. prepare_next_milestone
   └─ Clear ROADMAP.md
   └─ Increment milestone number
   └─ Set status: "Ready for /gsd:new-milestone"
```

### 9. map-codebase.md

**Purpose:** Analyze existing codebase before starting work (brownfield).

**When:** Before `/gsd:new-project` on existing codebase.

**Flow:**

```
1. scan_project_structure
   └─ Find package.json, build config, etc.
   └─ Identify project type (Next.js, React, Node, etc.)
   
2. spawn_mappers (parallel)
   ├─ gsd-codebase-mapper: "Stack & Dependencies"
   ├─ gsd-codebase-mapper: "Architecture & Patterns"
   ├─ gsd-codebase-mapper: "File Structure"
   ├─ gsd-codebase-mapper: "Conventions"
   ├─ gsd-codebase-mapper: "Integrations"
   ├─ gsd-codebase-mapper: "Testing"
   └─ gsd-codebase-mapper: "Concerns & Tech Debt"
   
3. create_codebase_documents
   └─ .planning/codebase/
       ├─ STACK.md
       ├─ ARCHITECTURE.md
       ├─ STRUCTURE.md
       ├─ CONVENTIONS.md
       ├─ INTEGRATIONS.md
       ├─ TESTING.md
       └─ CONCERNS.md
```

**Usage in Planning:**

Planner loads relevant codebase docs:

| Phase Keywords | Load |
|----------------|------|
| UI, frontend | CONVENTIONS, STRUCTURE |
| API, backend | ARCHITECTURE, CONVENTIONS |
| database | ARCHITECTURE, STACK |
| testing | TESTING, CONVENTIONS |
| integration | INTEGRATIONS, STACK |

## Workflow Patterns

### 1. Orchestrator Pattern

```python
def orchestrator_workflow():
    # Load state (lightweight)
    state = read_state()
    
    # Discover work
    items = discover_items()
    
    # Spawn agents (parallel where possible)
    results = []
    for item in items:
        agent = spawn_agent(item)
        results.append(agent)
    
    # Wait for completion
    wait_all(results)
    
    # Update state (lightweight)
    update_state(results)
```

**Keep orchestrator under 20% context.**

### 2. Agent Spawning Pattern

```python
# Bad: Spawn with @-references
spawn_agent(prompt="""
@.planning/STATE.md
@.planning/phases/01-*/01-01-PLAN.md
""")
# @-references don't work across Task boundaries

# Good: Inline content
state_content = read_file('.planning/STATE.md')
plan_content = read_file('.planning/phases/01-*/01-01-PLAN.md')

spawn_agent(prompt=f"""
<context>
Project state:
{state_content}

Plan:
{plan_content}
</context>

Execute this plan...
""")
```

### 3. Checkpoint Pattern

```python
# Executor hits checkpoint
task = next_task()
if task.type.startswith('checkpoint'):
    return checkpoint_message(
        completed_tasks=completed,
        current_task=task,
        checkpoint_details=task.details,
        awaited=task.resume_signal
    )
    # Agent STOPS here, orchestrator handles user interaction

# Orchestrator receives checkpoint
if result.is_checkpoint:
    user_response = present_checkpoint(result)
    
    # Spawn fresh continuation agent (NOT resume)
    continuation_agent = spawn_agent(
        prompt=build_continuation_prompt(
            plan=plan,
            completed_tasks=result.completed_tasks,
            resume_task=result.current_task,
            user_response=user_response
        )
    )
```

**Why fresh agent vs resume:**
- Resume uses Claude Code's internal serialization
- Parallel tool calls break serialization
- Fresh agents more reliable
- Explicit state management clearer

### 4. Gap Closure Pattern

```python
# After verification finds gaps
if verification.status == 'gaps_found':
    # User runs: /gsd:plan-phase {X} --gaps
    
    # Planner reads gaps
    gaps = read_verification_gaps(phase)
    
    # Creates additional plans
    next_plan_num = get_next_plan_number(phase)
    for gap_group in cluster_gaps(gaps):
        plan = create_plan(
            phase=phase,
            plan_num=next_plan_num,
            gap_closure=True,
            tasks=derive_tasks_from_gaps(gap_group)
        )
        next_plan_num += 1
    
    # User runs: /gsd:execute-phase {X} --gaps-only
    
    # Executor skips non-gap-closure plans
    plans = discover_plans(phase)
    gap_plans = [p for p in plans if p.gap_closure and not p.completed]
    execute_wave_based(gap_plans)
```

## Testing Workflows

Workflows are tested through:

1. **Integration tests**: Full flow from command to state update
2. **Agent tests**: Spawn agents with test prompts, verify outputs
3. **Manual testing**: Run actual commands in test projects

See [Testing](./testing.md) for details.

## Next Steps

- **Commands**: See [Commands](./commands.md) for user-facing API
- **Agents**: See [Agents](./agents.md) for agent details
- **Templates**: See [Templates](./templates.md) for output structures
