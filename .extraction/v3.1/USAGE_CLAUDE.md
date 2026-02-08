# Meta-Shell V3.1 - User Guide

## What Is This?

Meta-Shell is an AI orchestration system that breaks complex software projects into phases, plans the work, executes tasks with specialized AI agents, and verifies the results.

**Think of it as**: A project manager (Orchestrator) that delegates work to specialists (Planner, Executor, Researcher, Verifier).

---

## Quick Start

### 1. Initialize Your Project

Create the project structure:

```bash
mkdir -p .meta artifacts skills
```

Create `.meta/context.md` with your project vision:

```markdown
# Project: Task Manager App

## Goal

Build a full-stack task management application with user authentication.

## Tech Stack

- Frontend: React + TypeScript
- Backend: Node.js + Express
- Database: PostgreSQL
- Auth: JWT tokens

## Phases

1. Project setup & database schema
2. User authentication
3. Task CRUD operations
4. Frontend UI
5. Deployment

## Constraints

- Must use TypeScript everywhere
- Tests required for all API endpoints
- No external UI libraries (custom CSS only)
```

### 2. Start the Orchestrator

**Prompt the main agent:**

```
I have a project at /path/to/my-project with .meta/context.md defined.

Please act as the Meta-Orchestrator (V3.1).
Read .meta/context.md and execute Phase 1.

Use the orchestrator workflow from your skills directory.
```

### 3. The System Works Automatically

The Orchestrator will:

1. **Plan** the phase (spawns Planner agent)
2. **Execute** tasks sequentially (spawns Executor agents)
3. **Verify** the results (spawns Verifier agent)
4. **Report** completion or errors

---

## Example Prompts

### Starting a New Phase

```
Execute Phase 2 (User Authentication) for the project at /path/to/project.

Context is in .meta/context.md.
Use the Meta-Orchestrator V3.1 workflow.
```

### Resuming After Checkpoint

```
The orchestrator paused at a checkpoint asking "Which auth provider?"

My answer: Use Auth0

Please resume execution with this input.
```

### Handling a Failure

```
Task 02-03 failed with error "Database connection refused".

I've fixed the connection string in .env

Please retry the task.
```

### Manual Verification

```
Phase 2 is complete. Before moving to Phase 3, I want to manually test the authentication.

Please pause and show me:
1. What endpoints were created
2. How to test them
3. What the verification criteria are
```

---

## How the Workflow Works

```
┌─────────────────────────────────────────────────────────┐
│                    YOU (Human)                          │
│                                                         │
│  "Execute Phase 2 for my project"                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              ORCHESTRATOR (Main Agent)                  │
│                                                         │
│  Reads: .meta/context.md, .meta/session.json          │
│  Manages: Task sequencing, checkpoints, retries       │
└─┬───────────────────────────────────────────────────┬───┘
  │                                                   │
  │ Phase 1: Planning                                 │
  ▼                                                   │
┌─────────────────┐      ┌──────────────────┐        │
│   RESEARCHER    │      │     PLANNER      │        │
│                 │─────▶│                  │        │
│ Discovers       │      │ Creates task     │        │
│ constraints     │      │ list (plan.json) │        │
└─────────────────┘      └──────────────────┘        │
                                │                     │
                                │                     │
  Phase 2: Execution            │                     │
                                ▼                     │
                    ┌────────────────────┐            │
                    │    EXECUTOR #1     │            │
                    │  (Task 02-01)      │            │
                    └──────────┬─────────┘            │
                               │                      │
                               ▼                      │
                    ┌────────────────────┐            │
                    │    EXECUTOR #2     │            │
                    │  (Task 02-02)      │            │
                    └──────────┬─────────┘            │
                               │                      │
  Phase 3: Verification        │                      │
                               ▼                      │
                    ┌────────────────────┐            │
                    │     VERIFIER       │            │
                    │                    │            │
                    │ Checks all tasks   │            │
                    │ against must_haves │            │
                    └──────────┬─────────┘            │
                               │                      │
                               ▼                      │
                    ┌────────────────────┐            │
                    │   Phase Complete   │◀───────────┘
                    └────────────────────┘
```

---

## Configuration

### Project Structure

```
my-project/
├── .meta/
│   ├── context.md          # Your project vision (YOU WRITE THIS)
│   └── session.json        # Orchestrator state (AUTO-GENERATED)
│
├── artifacts/
│   ├── plan.json           # Generated by Planner
│   ├── research.json       # Generated by Researcher (optional)
│   ├── summary_01-01.json  # Generated by Executors
│   └── verification.json   # Generated by Verifier
│
├── skills/                 # Agent definitions (SYSTEM PROVIDED)
│   ├── orchestrator.md
│   ├── planner.md
│   ├── executor.md
│   ├── researcher.md
│   └── verifier.md
│
└── src/                    # Your actual code (GENERATED BY EXECUTORS)
    └── ...
```

### Session State (`.meta/session.json`)

Auto-generated, but you can inspect/edit:

```json
{
  "session_id": "uuid-here",
  "current_phase": "02",
  "current_task_idx": 3,
  "status": "executing",
  "gap_count": 0,
  "variables": {
    "research_done": true,
    "last_error": null
  }
}
```

**Manual edits** (when needed):

- Reset to specific task: Change `current_task_idx`
- Skip research: Set `research_done: true`
- Reset retry counter: Set `gap_count: 0`

---

## Adding Custom Sub-Agents

### 1. Create Agent Definition

Create `skills/my-agent.md`:

```markdown
# Skill: My Custom Agent

## Persona

You are a [role description]. You [what you do].

## Input Context

- `input_var`: Description of what you receive

## Output Schema

\`\`\`json
{
"field1": "value",
"field2": 123
}
\`\`\`

## Execution Rules

1. Rule one
2. Rule two
3. Output ONLY valid JSON
```

### 2. Use in Orchestrator

Modify `orchestrator.md` to spawn your agent:

```typescript
// In the appropriate workflow step:
Action: spawn_agent(
  "my-agent",
  read_file("skills/my-agent.md"),
  JSON.stringify(input_data),
  { timeout_seconds: 300 },
);
```

### Example Custom Agent: Security Auditor

```markdown
# Skill: Security Auditor

## Persona

You are a Security Engineer. You scan code for vulnerabilities.

## Input Context

- `files`: Array of file paths to audit

## Output Schema

\`\`\`json
{
"vulnerabilities": [
{
"severity": "high | medium | low",
"file": "path/to/file.ts",
"line": 42,
"issue": "SQL injection risk",
"fix": "Use parameterized queries"
}
],
"passed": true
}
\`\`\`

## Execution Rules

1. Check for: SQL injection, XSS, CSRF, hardcoded secrets
2. Output one vulnerability per issue found
3. Set `passed: false` if any HIGH severity found
```

---

## Common Scenarios

### Scenario 1: Starting Fresh

```
Prompt: "Initialize and execute Phase 1 of my project.
Context is in .meta/context.md at /path/to/project.
Use Meta-Orchestrator V3.1."

Result:
- Researcher analyzes requirements
- Planner creates task list
- Executors implement tasks
- Verifier checks completion
- Reports "Phase 1 Complete"
```

### Scenario 2: Checkpoint (Decision Needed)

```
Orchestrator: "Checkpoint: Which database?"
Options: ["PostgreSQL", "MySQL", "MongoDB"]

Your Response: "Use PostgreSQL"

Orchestrator: Resumes with your choice, continues execution
```

### Scenario 3: Task Failure

```
Orchestrator: "Task 03-04 failed: npm test returned errors"

Logs show:
- Commits: [abc123, def456]
- Rollback: git revert --no-edit abc123 def456

Your Options:
1. Fix the test manually, then "retry Task 03-04"
2. Run rollback command, investigate
3. Skip task (if non-critical): "mark Task 03-04 as skipped"
```

### Scenario 4: Timeout

```
Orchestrator: "Task 02-05 timed out after 600 seconds"

System automatically:
- Ran git reset --hard HEAD
- Cleaned up uncommitted files

Your Action:
- Investigate why task took so long
- Increase timeout if needed: modify orchestrator.md
- Retry: "retry Task 02-05 with timeout=1200"
```

### Scenario 5: Phase Complete, Moving On

```
Orchestrator: "Phase 2 Complete. All tasks verified."

Artifacts created:
- summary_02-01.json
- summary_02-02.json
- verification.json

Your Options:
1. "Execute Phase 3" (continue)
2. "Show me what was built in Phase 2" (review)
3. "Manually test Phase 2" (validation)
```

---

## Timeouts & Limits

### Default Timeouts

- **Planner**: 300 seconds (5 minutes)
- **Executor**: 600 seconds (10 minutes)
- **Verifier**: 300 seconds (5 minutes)
- **Lock Timeout**: 5000ms (5 seconds)

### Changing Timeouts

Edit the spawn call in `orchestrator.md`:

```typescript
spawn_agent("executor", ..., {
    timeout_seconds: 1200  // 20 minutes
})
```

### Retry Limits

- **Self-correction**: 2 attempts per executor
- **Gap plans**: 2 retries per phase
- **Lock acquisition**: 5 second timeout

---

## Troubleshooting

### "Invalid Topology" Error

**Cause**: Task depends on a later task
**Fix**: Edit `plan.json` to reorder tasks, or fix dependencies array

```json
// BAD:
{ "id": "01", "dependencies": ["02"] }  // 01 depends on future 02
{ "id": "02", "dependencies": [] }

// GOOD:
{ "id": "01", "dependencies": [] }
{ "id": "02", "dependencies": ["01"] }  // 02 depends on past 01
```

### "Dependency Violation" Error

**Cause**: Trying to execute task before its dependency completed
**Check**: `.meta/session.json` - verify dependency task status is "complete"

### "Lock Timeout" Error

**Cause**: State file locked by another process or crashed agent
**Fix**:

1. Check for orphaned processes
2. Manually remove `.meta/session.json.lock` if exists
3. Retry

### "Max Retries Exceeded"

**Cause**: Phase verification failed twice
**Options**:

1. Review `verification.json` to see what failed
2. Manually fix the issues
3. Reset gap_count: Edit `session.json`, set `gap_count: 0`
4. Retry phase

### Executor Created Files But Didn't Commit

**Cause**: Likely timeout or crash
**Fix**:

```bash
git status                    # See uncommitted files
git reset --hard HEAD         # Clean workspace
# Then retry task
```

---

## Best Practices

### 1. Write Clear Context

**Good context.md:**

```markdown
## Constraints

- Must use TypeScript (not JavaScript)
- All API routes need authentication middleware
- Database migrations must be reversible
- Test coverage minimum: 80%
```

**Bad context.md:**

```markdown
## Constraints

- Use good practices
- Make it scalable
```

### 2. Keep Phases Small

**Good**: "Phase 2: User Registration Endpoint"
**Bad**: "Phase 2: Complete User Management System"

### 3. Define Success Criteria

In your context.md:

```markdown
## Phase 1 Success Criteria

- Database schema created
- Migrations run successfully
- Can insert a test user
- Foreign keys enforced
```

### 4. Monitor Progress

Watch the logs:

```
[INFO] Executing Task 02-01: Create auth helper
[INFO] Executing Task 02-02: Create login route
[WARN] Task 02-03 exceeds context budget (5 files)
[ERROR] Task 02-04 failed: Verification returned non-zero
```

### 5. Commit Often (For Executors)

Each executor commits per sub-task, enabling:

- Granular rollback
- Clear git history
- Easy debugging

---

## Advanced Usage

### Custom Verification Commands

In `plan.json` (generated by Planner, but you can template):

```json
{
  "id": "03-02",
  "title": "User Login API",
  "verification_cmd": "npm test tests/auth.test.ts && curl -f localhost:3000/health"
}
```

### Conditional Research

Skip research for simple phases:

```json
// In session.json
{
  "variables": {
    "research_done": true // Skip researcher for this phase
  }
}
```

### Multi-Agent Collaboration

Create a "reviewer" agent that checks executor output:

```markdown
# Skill: Code Reviewer

## Input

- `summary.json` from executor
- Files modified

## Output

\`\`\`json
{
"approved": true,
"suggestions": ["Add error handling to line 42"]
}
\`\`\`
```

Integrate into orchestrator between execution and verification.

---

## FAQ

**Q: Can I pause and resume later?**
A: Yes. Session state in `.meta/session.json` tracks progress. Just re-run the orchestrator prompt.

**Q: What if I disagree with the plan?**
A: Edit `artifacts/plan.json` before execution starts, or ask: "Revise the plan to [your changes]"

**Q: Can I run multiple phases in parallel?**
A: No. V3.1 uses sequential execution. This is intentional for reliability.

**Q: How do I see what was built?**
A: Check `artifacts/summary_*.json` files, or ask: "Show me all changes from Phase 2"

**Q: Can I use different AI models?**
A: Yes. Set `model_hint: "smart"` for complex tasks (Opus) or `"fast"` for simple tasks (Sonnet)

**Q: What happens to my code if something fails?**
A: Executors commit atomically. Failed tasks don't commit broken code. Use logged rollback commands if needed.

---

## Example Full Session

```
YOU: "Initialize project, execute Phase 1: Database Setup.
Context at /home/user/myapp/.meta/context.md"

ORCHESTRATOR: "Reading context... Spawning Planner..."

PLANNER: "Phase 1 plan created:
- Task 01-01: Initialize Prisma
- Task 01-02: Create User schema
- Task 01-03: Create Task schema
- Task 01-04: Run migrations"

ORCHESTRATOR: "Executing Task 01-01..."

EXECUTOR: "✓ Task 01-01 complete. Commits: [a1b2c3]"

ORCHESTRATOR: "Executing Task 01-02..."

EXECUTOR: "✓ Task 01-02 complete. Commits: [d4e5f6]"

ORCHESTRATOR: "Executing Task 01-03..."

EXECUTOR: "✓ Task 01-03 complete. Commits: [g7h8i9]"

ORCHESTRATOR: "Executing Task 01-04..."

EXECUTOR: "✓ Task 01-04 complete. Commits: [j0k1l2]"

ORCHESTRATOR: "All tasks complete. Spawning Verifier..."

VERIFIER: "✓ Verification passed:
- Database schema exists
- Migrations ran successfully
- Foreign keys enforced"

ORCHESTRATOR: "Phase 1 Complete.
Next: Execute Phase 2 (User Authentication)"

YOU: "Execute Phase 2"

[Process repeats...]
```

---

## Summary

**To use Meta-Shell:**

1. **Create** `.meta/context.md` with your project vision
2. **Prompt** the orchestrator: "Execute Phase [N] using V3.1"
3. **Monitor** progress via logs
4. **Respond** to checkpoints when needed
5. **Handle** failures using logged rollback commands
6. **Continue** to next phase when complete

**The system handles:**

- Breaking work into tasks
- Executing with specialized agents
- Verifying results
- Managing state
- Recovering from errors

**You handle:**

- Defining project vision
- Making decisions at checkpoints
- Reviewing phase completions
- Manual rollback execution (when needed)

---

**Ready to start? Create your `.meta/context.md` and prompt the orchestrator!**
