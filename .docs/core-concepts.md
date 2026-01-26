# Core Concepts

Understanding these fundamental concepts is essential to working with or contributing to GSD.

## 1. Plans Are Prompts

**The most important concept in GSD.**

### Traditional Approach (Wrong)

```
Plan Document (Markdown)
  ↓ [transformation layer]
System Prompt (structured format)
  ↓ [interpretation]
Claude executes
```

Problems:
- Information loss during transformation
- Interpretation drift
- Indirection makes debugging hard

### GSD Approach (Correct)

```
PLAN.md (XML-structured markdown)
  ↓ [direct load]
Claude executes
```

**PLAN.md IS the prompt.** No transformation layer. What you write is what Claude reads.

### Implications

1. **Write for execution, not documentation**
   ```xml
   <!-- BAD: Documentation style -->
   <task>
     <description>The system should implement authentication</description>
   </task>
   
   <!-- GOOD: Executable instruction -->
   <task type="auto">
     <name>Create JWT authentication endpoint</name>
     <files>src/app/api/auth/login/route.ts</files>
     <action>
       POST endpoint accepting {email, password}.
       Query User table by email (case-insensitive).
       Compare password with bcrypt.
       On match: create JWT with jose library, set httpOnly cookie, return 200.
       On mismatch: return 401 with {error: "Invalid credentials"}.
     </action>
     <verify>curl -X POST localhost:3000/api/auth/login returns 200 + Set-Cookie</verify>
     <done>Valid creds → 200+cookie, invalid → 401</done>
   </task>
   ```

2. **Precision matters**
   - Vague language → vague execution
   - Specific instructions → specific results
   - Include what to AVOID and WHY

3. **Context is explicit**
   - Plans use @-references to load other files
   - No implicit knowledge assumptions
   - If Claude needs it, reference it

4. **Testing is built-in**
   - Every task has `<verify>` and `<done>`
   - Verification is part of execution, not separate
   - Plans specify how to prove completion

## 2. Context Engineering

### The Quality Degradation Curve

Claude's output quality varies with context usage:

```
Quality
   ↑
100%│██████╗
    │      ║ PEAK
 80%│      ║ (0-30%)
    │      ╚═════════╗
 60%│                ║ GOOD
    │                ║ (30-50%)
 40%│                ╚═══════════╗
    │                            ║ DEGRADING
 20%│                            ║ (50-70%)
    │                            ╚═══════════╗
  0%│                                        ║ POOR (70%+)
    └────────────────────────────────────────────→
    0%                                      100%
                Context Usage
```

**Key insight:** Claude enters "efficiency mode" above 50% context. It starts summarizing, skipping details, rushing to completion.

### GSD's Solution: Aggressive Atomicity

**Don't try to optimize context usage. Split work instead.**

| Approach | Plan Size | Context/Plan | Quality |
|----------|-----------|--------------|---------|
| "Efficient" | 10 tasks | 80% | POOR - rushed, incomplete |
| GSD | 2-3 tasks | 40-50% | GOOD - thorough, verified |

**More plans = consistent quality.**

Each plan completes in GOOD zone. No degradation, ever.

### Context Budget Rules

| Component | Target | Max |
|-----------|--------|-----|
| Orchestrator | 10% | 20% |
| Planner | 30% | 50% |
| Executor | 40% | 50% |
| Verifier | 20% | 40% |

**Plans: 2-3 tasks maximum.** This keeps executor in GOOD zone.

### Fresh Context Pattern

```
Main Session (Orchestrator)
├─ 10% context: Discover, spawn, collect
│
├─ Spawn Agent A (Fresh 200k context)
│  └─ 40% context: Execute plan 1
│
├─ Spawn Agent B (Fresh 200k context)
│  └─ 40% context: Execute plan 2
│
└─ 15% context: Collect results, update state
```

**Main session never accumulates garbage.** Heavy work happens in fresh subagent contexts.

## 3. Goal-Backward Methodology

Traditional planning asks: "What should we build?"

Goal-backward planning asks: "What must be TRUE for the goal to be achieved?"

### The Process

**Step 1: State the Goal**
```
Phase: Working chat interface
```

**Step 2: Derive Observable Truths (User Perspective)**
```
What must be TRUE:
- User can see existing messages
- User can type a new message
- User can send the message
- Sent message appears in the list
- Messages persist across page refresh
```

**Step 3: Derive Required Artifacts**
```
For "User can see existing messages":
- Message list component (renders Message[])
- Messages state (loaded from somewhere)
- API route (provides messages)
- Message type definition
```

**Step 4: Derive Required Wiring**
```
Message list component wiring:
- Imports Message type (not using 'any')
- Receives messages prop or fetches from API
- Maps over messages to render
- Handles empty state
```

**Step 5: Identify Key Links**
```
Critical connections:
- Input onSubmit → API call
- API save → database
- Component → real data (not placeholder)
```

### Must-Haves Output

Plans include `must_haves` in frontmatter:

```yaml
must_haves:
  truths:
    - "User can see existing messages"
    - "User can send a message"
    - "Messages persist across refresh"
  artifacts:
    - path: "src/components/Chat.tsx"
      provides: "Message list rendering"
      min_lines: 30
    - path: "src/app/api/chat/route.ts"
      provides: "Message CRUD"
      exports: ["GET", "POST"]
  key_links:
    - from: "src/components/Chat.tsx"
      to: "/api/chat"
      via: "fetch in useEffect"
      pattern: "fetch.*api/chat"
```

### Verification Uses Must-Haves

Verifier agent checks:
1. **Truths**: Can user actually do these things?
2. **Artifacts**: Do these files exist with required content?
3. **Key links**: Are critical connections present?

If gaps found → gap closure plans created.

## 4. Multi-Agent Orchestration

### The Thin Orchestrator Pattern

**Orchestrators don't do heavy work. They coordinate specialists.**

```python
# Pseudocode for execute-phase orchestrator

def execute_phase(phase_num):
    # Load state (lightweight)
    state = read_state()
    plans = discover_plans(phase_num)
    waves = group_by_wave(plans)
    
    # For each wave
    for wave in waves:
        # Spawn agents (parallel in wave)
        agents = [
            spawn_executor(plan) 
            for plan in wave.plans
        ]
        
        # Wait for completion (Task tool blocks)
        results = wait_all(agents)
        
        # Verify (lightweight)
        verify_completions(results)
    
    # Verify phase goal
    spawn_verifier(phase_num)
    
    # Update state (lightweight)
    update_roadmap()
    update_state()
```

**Orchestrator: ~10-15% context**
**Agents: Fresh 200k context each**

### Why This Works

**Traditional monolithic approach:**
```
Main session starts at 0%
├─ Plan phase 1: now 30%
├─ Execute plan 1: now 60%
├─ Execute plan 2: now 85% [DEGRADING]
├─ Execute plan 3: now 95% [POOR]
└─ Verify phase: now 100% [RUSHED]
```

**GSD multi-agent approach:**
```
Main session (orchestrator): 10%
├─ Spawn executor A: fresh 0% → 40%
├─ Spawn executor B: fresh 0% → 40%
├─ Spawn executor C: fresh 0% → 40%
└─ Spawn verifier: fresh 0% → 30%

Main session: still 15%
```

**Result:** Consistent GOOD/PEAK quality across all work.

### Agent Specialization

Each agent optimized for its job:

| Agent | Context Target | Complexity |
|-------|----------------|------------|
| Planner | 30-40% | Medium - needs project history |
| Executor | 40-50% | High - reads code, writes code, commits |
| Verifier | 20-30% | Low - checks must-haves |
| Debugger | 30-40% | Medium - analyzes failures |
| Researcher | 40-50% | High - explores ecosystem |

**Specialists do better than generalists.**

## 5. Atomic Commits

### Every Task = One Commit

```bash
# Task 1 complete
git add src/models/user.ts
git commit -m "feat(01-02): create User model with auth fields"

# Task 2 complete  
git add src/app/api/auth/register/route.ts
git commit -m "feat(01-02): implement registration endpoint"

# Task 3 complete
git add src/app/api/auth/login/route.ts
git commit -m "feat(01-02): implement login endpoint"

# Plan complete (metadata only)
git add .planning/phases/01-*/01-02-SUMMARY.md
git commit -m "docs(01-02): complete user authentication plan"
```

### Benefits

1. **Git bisect finds exact failing task**
   ```bash
   git bisect start
   git bisect bad HEAD
   git bisect good v1.0
   # Git binary searches commits
   # "feat(01-02): implement login endpoint" is bad
   # Now you know exactly which task broke things
   ```

2. **Surgical reverts**
   ```bash
   # Revert just Task 2, keep Tasks 1 and 3
   git revert abc123f
   ```

3. **Context for future Claude sessions**
   ```bash
   git log --oneline
   # feat(01-02): implement login endpoint
   # feat(01-02): implement registration endpoint
   # feat(01-02): create User model
   
   # Claude reads this and understands what was built
   ```

4. **Clear audit trail**
   - Who: Claude (via Co-Authored-By)
   - What: Specific task
   - When: Timestamp
   - Why: Task description + plan context

### Commit Format

```
{type}({phase}-{plan}): {task-description}

- {key change 1}
- {key change 2}

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `test`: Tests (TDD RED)
- `refactor`: Code cleanup (TDD REFACTOR)
- `docs`: Documentation (SUMMARYs, metadata)
- `chore`: Config, dependencies

## 6. Checkpoints

### Automation-First Principle

**Golden rule:** If Claude can run it, Claude runs it.

Checkpoints are for:
- ✅ Visual verification (does UI look right?)
- ✅ Functional testing (does feature work?)
- ✅ Human decisions (choose between options)
- ✅ Secrets (provide API keys)

Checkpoints are NOT for:
- ❌ Running CLI commands (Claude does this)
- ❌ Starting servers (Claude does this)
- ❌ Deploying apps (Claude uses CLI)
- ❌ Creating databases (Claude uses provider CLI)

### Checkpoint Types

**checkpoint:human-verify (90%)**
```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
    Deployed to Vercel at https://myapp.vercel.app
    (Claude already ran `vercel --yes`)
  </what-built>
  <how-to-verify>
    1. Visit https://myapp.vercel.app
    2. Click "Sign Up" button
    3. Fill form and submit
    4. Confirm redirect to dashboard
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

**checkpoint:decision (9%)**
```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Which authentication provider?</decision>
  <context>
    Project needs social login. Budget: $0/month initially.
  </context>
  <options>
    <option id="clerk">
      <name>Clerk</name>
      <pros>Generous free tier, great DX, edge-ready</pros>
      <cons>Lock-in, pricing jumps at scale</cons>
    </option>
    <option id="nextauth">
      <name>NextAuth.js</name>
      <pros>Open source, no lock-in, flexible</pros>
      <cons>More setup, DB required, custom edge work</cons>
    </option>
  </options>
  <resume-signal>Select: clerk, nextauth, or describe alternative</resume-signal>
</task>
```

**checkpoint:human-action (1% - rare)**
```xml
<task type="checkpoint:human-action" gate="blocking">
  <automation-attempted>
    Sent email verification via SendGrid API.
    Email ID: abc123def456
  </automation-attempted>
  <what-you-need-to-do>
    Check your email inbox and click the verification link.
  </what-you-need-to-do>
  <ill-verify-after>
    Query SendGrid API for email.verified = true
  </ill-verify-after>
  <resume-signal>Type "done" when verified</resume-signal>
</task>
```

### Checkpoint Flow

```
Executor runs tasks 1-3 (auto)
  ↓
Executor hits task 4 (checkpoint:human-verify)
  ↓
Executor STOPS, returns structured message:
  - Completed: tasks 1-3 with commits
  - Current: task 4 blocked at checkpoint
  - Details: what to verify
  ↓
Orchestrator presents to user
  ↓
User responds: "approved"
  ↓
Orchestrator spawns continuation agent:
  - Same plan
  - Resume from task 5
  - Previous commits verified
  ↓
Continuation agent runs tasks 5-6
  ↓
Creates SUMMARY.md
```

**Key:** Fresh continuation agent, not resume. More reliable with parallel tool calls.

## 7. State Management

### STATE.md - Project Memory

```markdown
# Project State

## Current Position
Phase: 3 of 5 (Database Layer)
Plan: 2 of 4
Status: In progress
Last activity: 2026-01-26 - Completed 03-02-PLAN.md

Progress: ████████░░░░░░░░░░░░ 40%

## Decisions Made
| Decision | Rationale | Phase |
|----------|-----------|-------|
| Use Prisma | Type-safe, migrations | 03 |
| PostgreSQL on Vercel | Integrated, scales | 03 |

## Issues & Concerns
| Issue | Impact | Status |
|-------|--------|--------|
| DB connection pooling | May timeout under load | Monitoring |
```

**Purpose:**
- Persistent memory across sessions
- Accumulates decisions from SUMMARYs
- Tracks blockers and concerns
- Shows current position in roadmap

**Updated by:**
- Executors after each plan
- Orchestrators after each phase
- Users via /gsd:pause-work

### ROADMAP.md - Phase Structure

```markdown
# Project Roadmap

## Milestone: v1.0 - MVP Launch

### Phase 1: Foundation ✓ COMPLETE
**Goal:** Authentication, database, basic API

Plans:
- [x] 01-01-PLAN.md — User model and Prisma setup
- [x] 01-02-PLAN.md — Registration and login endpoints
- [x] 01-03-PLAN.md — Session middleware

**Completed:** 2026-01-20

### Phase 2: Core Features
**Goal:** Main app functionality

Plans:
- [ ] 02-01-PLAN.md — Dashboard UI
- [ ] 02-02-PLAN.md — Data display components
```

**Purpose:**
- Shows big picture
- Tracks phase completion
- Links to plans
- Shows dependencies

## 8. XML Prompt Formatting

### Why XML?

1. **Semantic structure** - Tags have meaning, not just hierarchy
2. **Claude-optimized** - Claude excels at following XML instructions
3. **Unambiguous** - No ambiguity in nested markdown
4. **Validatable** - Can be parsed and validated

### Conventions

**Use semantic tags, not generic ones:**
```xml
<!-- BAD: Generic tags -->
<section name="objective">
  <content>Build auth system</content>
</section>

<!-- GOOD: Semantic tags -->
<objective>
  Build JWT authentication with refresh rotation
</objective>
```

**Markdown inside XML for content:**
```xml
<objective>
## Primary Goal
Build authentication system

## Success Criteria
- Users can register
- Users can log in
- Sessions persist 15 minutes
</objective>
```

**Attributes for metadata:**
```xml
<task type="auto" tdd="true">
  <name>...</name>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>...</what-built>
</task>
```

### Common Tags

**Plan structure:**
- `<objective>` - What and why
- `<execution_context>` - @-references to workflows
- `<context>` - Project files to load
- `<tasks>` - Container for task list
- `<task>` - Individual task
- `<verification>` - Overall checks
- `<success_criteria>` - Measurable completion

**Task structure:**
- `<name>` - Action-oriented task name
- `<files>` - Paths created/modified
- `<action>` - Implementation instructions
- `<verify>` - How to prove it works
- `<done>` - Acceptance criteria

**Checkpoint structure:**
- `<what-built>` - What Claude automated
- `<how-to-verify>` - Steps for user
- `<resume-signal>` - How to continue

## 9. Progressive Disclosure

Information flows through layers:

```
Layer 1: Command
├─ What: /gsd:execute-phase
├─ When: After planning complete
└─ Who: User invokes

Layer 2: Workflow  
├─ How: Wave-based orchestration
├─ Why: Parallel execution
└─ Where: execute-phase.md

Layer 3: Agent
├─ Details: Task execution, commits
├─ Patterns: Deviation handling
└─ Who: gsd-executor

Layer 4: Reference
├─ Deep dive: Checkpoint patterns
├─ Examples: Full implementations
└─ Where: checkpoints.md
```

**Each layer answers different questions:**
- Command: "Should I use this?"
- Workflow: "What happens?"
- Agent: "How does it work?"
- Reference: "Why this design?"

**Benefits:**
1. Quick start without overwhelming
2. Deep dive available when needed
3. Documentation at appropriate depth
4. No redundancy

## 10. Depth vs Compression

### Depth Setting

| Depth | Meaning | Plans/Phase |
|-------|---------|-------------|
| Quick | Aggressive compression | 1-3 |
| Standard | Balanced | 3-5 |
| Comprehensive | Resist compression | 5-10 |

**Key principle:** Depth controls compression tolerance, NOT target count.

### Correct Usage

```
Complex auth phase with depth=quick:
- Compress to 3 plans
- Each plan covers multiple concerns
- Acceptable because depth=quick

Simple "add config" phase with depth=comprehensive:
- Still 1 plan
- Don't pad to reach 5 plans
- That's all there is
```

**Derive from work, don't pad to numbers.**

### When to Split Plans

**ALWAYS split:**
- More than 3 tasks
- Multiple subsystems (DB + API + UI)
- Any task modifies >5 files
- Discovery + implementation

**CONSIDER splitting:**
- >5 files total
- Complex domains (auth, payments)
- Natural boundaries (Setup → Core → Polish)

## 11. Solo Developer Pattern

### What GSD Avoids

❌ **Enterprise Patterns:**
- Sprint ceremonies
- Story points
- RACI matrices
- Stakeholder management
- Change advisory boards
- Team coordination
- Knowledge transfer docs
- Retrospectives

❌ **Team Artifacts:**
- Sprint planning docs
- Velocity tracking
- Capacity planning
- Confluence pages
- Status reports

❌ **Temporal Language:**
- "We changed X to Y"
- "Previously we used"
- "No longer supported"
- "Instead of the old way"

(Exception: CHANGELOG.md, git commits)

### What GSD Embraces

✅ **Solo Workflow:**
- You describe what you want
- Claude researches and plans
- Claude executes and verifies
- You test and approve
- Repeat

✅ **Technical Focus:**
- Executable specifications
- Automated verification
- Clear git history
- Working software

✅ **Direct Communication:**
- Imperative voice
- No filler ("just", "simply", "basically")
- No sycophancy ("Great!", "Awesome!")
- Factual, technical, brief

## Summary

These 11 concepts form the foundation of GSD:

1. **Plans are prompts** - No transformation layer
2. **Context engineering** - Quality curve, fresh agents
3. **Goal-backward** - What must be TRUE?
4. **Multi-agent** - Thin orchestrator, specialist agents
5. **Atomic commits** - One task, one commit
6. **Checkpoints** - Automation first, verify after
7. **State management** - Persistent project memory
8. **XML formatting** - Semantic, Claude-optimized
9. **Progressive disclosure** - Layers of detail
10. **Depth vs compression** - Derive from work
11. **Solo developer** - No enterprise theater

Understanding these enables effective use and contribution to GSD.

## Next Steps

- **Architecture**: [System design and components](./architecture.md)
- **Workflows**: [Detailed workflow guide](./workflows.md)
- **Commands**: [Command reference](./commands.md)
