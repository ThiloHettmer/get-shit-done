# XML Format Reference

GSD uses XML for structured prompts. This document defines the schema and conventions.

## Why XML?

1. **Semantic structure** - Tags convey meaning, not just hierarchy
2. **Claude-optimized** - Claude excels at following XML instructions
3. **Unambiguous** - No confusion with nested markdown
4. **Validatable** - Can be parsed and checked programmatically

## Core Principles

### 1. Semantic Tags Only

**Use tags that describe purpose, not structure.**

```xml
<!-- BAD: Generic tags -->
<section name="objective">
  <content>Build authentication</content>
</section>

<!-- GOOD: Semantic tags -->
<objective>
  Build authentication
</objective>
```

Common anti-patterns to avoid:
- `<section>`, `<item>`, `<content>`, `<data>`

Use instead:
- `<objective>`, `<action>`, `<verify>`, `<context>`

### 2. Markdown Inside XML

**Use Markdown for content formatting inside XML blocks.**

```xml
<objective>
## Primary Goal
Implement JWT authentication with refresh token rotation

## Success Criteria
- Users can register with email/password
- Users can log in and receive JWT
- Tokens refresh automatically before expiry
- Sessions persist across browser restarts
</objective>
```

### 3. Attributes for Metadata

**Use attributes for classification and flags, not content.**

```xml
<!-- Type classification -->
<task type="auto" tdd="true">
  <name>Implement email validation</name>
</task>

<!-- Gate specification -->
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>Deployed to Vercel</what-built>
</task>

<!-- Priority hint -->
<step name="load_state" priority="first">
  Read STATE.md before any operation
</step>
```

## Plan Structure

### Frontmatter (YAML)

```yaml
---
phase: 01-foundation
plan: 02
type: execute                    # or "tdd"
wave: 2
depends_on: ["01-01"]
files_modified: 
  - "src/app/api/auth/register/route.ts"
  - "src/app/api/auth/login/route.ts"
autonomous: true                  # false if has checkpoints
gap_closure: false                # true if fixing verification gaps

must_haves:
  truths:
    - "User can register with email"
    - "User can log in"
  artifacts:
    - path: "src/app/api/auth/register/route.ts"
      provides: "Registration endpoint"
      exports: ["POST"]
  key_links:
    - from: "src/components/RegisterForm.tsx"
      to: "/api/auth/register"
      via: "fetch on form submit"
      pattern: "fetch.*auth/register"

# Optional: only if external services involved
user_setup:
  - service: sendgrid
    why: "Email verification"
    env_vars:
      - name: SENDGRID_API_KEY
        source: "SendGrid Dashboard → Settings → API Keys"
---
```

### Plan Body

```xml
<objective>
[What and why this plan accomplishes]

Purpose: [Why this matters for project]
Output: [What artifacts will be created]
</objective>

<execution_context>
@~/.claude/get-shit-done/workflows/execute-plan.md
@~/.claude/get-shit-done/templates/summary.md
@~/.claude/get-shit-done/references/checkpoints.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md

# Only reference prior SUMMARYs if genuinely needed
@.planning/phases/01-foundation/01-01-SUMMARY.md

# Reference relevant source files
@src/models/user.ts
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create registration endpoint</name>
  <files>src/app/api/auth/register/route.ts</files>
  <action>
    Create POST endpoint at /api/auth/register.
    
    Accept JSON body: {email, password}
    
    Validate:
    - Email format (RFC 5322)
    - Password min 8 chars
    - Email not in use (case-insensitive check)
    
    On success:
    - Hash password with bcrypt (cost: 10)
    - Insert User record
    - Return 201 with {user: {id, email}}
    
    On validation fail:
    - Return 400 with {error: string}
    
    Use Prisma Client for DB access.
    Do NOT use jsonwebtoken library (CommonJS issues) - use jose instead.
  </action>
  <verify>
    curl -X POST localhost:3000/api/auth/register \
      -H "Content-Type: application/json" \
      -d '{"email":"test@example.com","password":"password123"}' \
    returns 201
  </verify>
  <done>
    Valid registration → 201 + user object
    Duplicate email → 400 with error
    Invalid input → 400 with error
  </done>
</task>

<task type="auto">
  <name>Task 2: Create login endpoint</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>
    Create POST endpoint at /api/auth/login.
    
    Accept JSON body: {email, password}
    
    Query User by email (case-insensitive).
    Compare password with bcrypt.
    
    On match:
    - Create JWT with jose library
    - Claims: {userId, email}
    - Expiry: 15 minutes
    - Set as httpOnly cookie
    - Return 200 with {user: {id, email}}
    
    On mismatch:
    - Return 401 with {error: "Invalid credentials"}
  </action>
  <verify>
    curl -X POST localhost:3000/api/auth/login \
      -H "Content-Type: application/json" \
      -d '{"email":"test@example.com","password":"password123"}' \
    returns 200 with Set-Cookie header
  </verify>
  <done>
    Valid credentials → 200 + cookie + user
    Invalid credentials → 401
  </done>
</task>

</tasks>

<verification>
Run both endpoints with valid and invalid inputs.
Verify cookies set correctly.
Verify passwords hashed in database.
</verification>

<success_criteria>
- [ ] Registration endpoint accepts valid signups
- [ ] Registration rejects duplicate emails
- [ ] Login endpoint returns JWT cookie
- [ ] Login rejects invalid credentials
- [ ] Passwords stored as bcrypt hashes
</success_criteria>

<output>
After completion, create `.planning/phases/01-foundation/01-02-SUMMARY.md`
</output>
```

## Task Types

### type="auto"

Standard autonomous task. Executor runs without user intervention.

```xml
<task type="auto">
  <name>Task name: action-oriented</name>
  <files>file1.ts, file2.ts</files>
  <action>
    Specific implementation instructions.
    Include what to avoid and WHY.
  </action>
  <verify>Command or check to prove completion</verify>
  <done>Measurable acceptance criteria</done>
</task>
```

**Required elements:**
- `<name>` - Action-oriented task name
- `<files>` - Paths created or modified (if creating/modifying files)
- `<action>` - Specific instructions, including anti-patterns
- `<verify>` - How to prove task complete
- `<done>` - Acceptance criteria

### type="auto" tdd="true"

TDD task with RED-GREEN-REFACTOR cycle.

```xml
<task type="auto" tdd="true">
  <name>Implement password validation</name>
  <files>
    src/utils/validatePassword.ts,
    src/utils/validatePassword.test.ts
  </files>
  <behavior>
    Given password string:
    - Length < 8 → false
    - No uppercase → false
    - No number → false
    - Valid → true
  </behavior>
  <implementation>
    Check length >= 8
    Check /[A-Z]/ for uppercase
    Check /[0-9]/ for number
    Return boolean
  </implementation>
</task>
```

**Additional elements for TDD:**
- `<behavior>` - Expected behavior in testable terms
- `<implementation>` - How to implement once tests pass

Executor will:
1. RED: Write test, verify it fails, commit
2. GREEN: Implement, verify it passes, commit
3. REFACTOR: Clean up if needed, commit

### type="checkpoint:human-verify"

Pause for human to verify automated work.

```xml
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
    Description of what Claude automated.
    Include URLs, running servers, deployed apps.
  </what-built>
  <how-to-verify>
    1. Exact step with URL or command
    2. What to check
    3. Expected behavior
    4. How to confirm success
  </how-to-verify>
  <resume-signal>
    Type "approved" to continue, or describe issues to fix
  </resume-signal>
</task>
```

**Elements:**
- `<what-built>` - What Claude did (automated)
- `<how-to-verify>` - Numbered steps for user
- `<resume-signal>` - How user continues

**Examples:**

```xml
<!-- UI verification -->
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
    Dashboard layout implemented - dev server at http://localhost:3000
  </what-built>
  <how-to-verify>
    1. Visit http://localhost:3000/dashboard
    2. Resize browser window from 375px to 1920px
    3. Verify layout adapts: mobile (1 col) → tablet (2 col) → desktop (3 col)
    4. Confirm no horizontal scroll at any size
    5. Check that nav collapses to hamburger below 768px
  </how-to-verify>
  <resume-signal>Type "approved" or describe layout issues</resume-signal>
</task>

<!-- Deployment verification -->
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
    Deployed to production at https://myapp.vercel.app
    (ran vercel --prod)
  </what-built>
  <how-to-verify>
    1. Visit https://myapp.vercel.app
    2. Test user registration flow
    3. Test login with registered user
    4. Verify you can access protected /dashboard route
    5. Log out and confirm redirect to login
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>
```

### type="checkpoint:decision"

User chooses between implementation options.

```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>What's being decided</decision>
  <context>
    Why this matters.
    Relevant constraints (budget, timeline, requirements).
  </context>
  <options>
    <option id="option-a">
      <name>Option A Name</name>
      <pros>
        - Benefit 1
        - Benefit 2
      </pros>
      <cons>
        - Tradeoff 1
        - Tradeoff 2
      </cons>
    </option>
    <option id="option-b">
      <name>Option B Name</name>
      <pros>Benefits</pros>
      <cons>Tradeoffs</cons>
    </option>
  </options>
  <resume-signal>
    Select: option-a, option-b, or describe alternative
  </resume-signal>
</task>
```

**Example:**

```xml
<task type="checkpoint:decision" gate="blocking">
  <decision>Choose authentication provider</decision>
  <context>
    Project needs social login (Google, GitHub).
    Budget: $0/month initially, <$50/month at 10k users.
    Requirements: Edge runtime compatible (Vercel).
  </context>
  <options>
    <option id="clerk">
      <name>Clerk</name>
      <pros>
        - Free tier: 10k MAU
        - Excellent DX, pre-built components
        - Edge runtime native
        - Social providers included
      </pros>
      <cons>
        - Vendor lock-in
        - Pricing jumps at 10k+ users ($25/mo → $99/mo)
        - Less control over auth flow
      </cons>
    </option>
    <option id="nextauth">
      <name>NextAuth.js (Auth.js)</name>
      <pros>
        - Open source, no lock-in
        - Full control over flow
        - No usage-based pricing
        - Large community
      </pros>
      <cons>
        - More setup required
        - Database needed for sessions
        - Custom work for Edge runtime
        - No pre-built UI
      </cons>
    </option>
    <option id="supabase">
      <name>Supabase Auth</name>
      <pros>
        - Free tier: 50k MAU
        - Database included
        - Real-time features
        - Edge functions support
      </pros>
      <cons>
        - Vendor lock-in (PostgreSQL)
        - Less mature than competitors
        - May need custom flows
      </cons>
    </option>
  </options>
  <resume-signal>
    Select: clerk, nextauth, supabase, or describe custom solution
  </resume-signal>
</task>
```

### type="checkpoint:human-action"

Truly unavoidable manual step (rare - <1% of checkpoints).

```xml
<task type="checkpoint:human-action" gate="blocking">
  <automation-attempted>
    What Claude already did via CLI/API.
  </automation-attempted>
  <what-you-need-to-do>
    The single unavoidable manual step.
  </what-you-need-to-do>
  <ill-verify-after>
    How Claude will verify you completed it.
  </ill-verify-after>
  <resume-signal>Type "done" when complete</resume-signal>
</task>
```

**Only use for:**
- Email verification links
- SMS 2FA codes
- Manual account approvals
- Credit card 3D Secure flows

**Do NOT use for:**
- Deploying (use CLI)
- Creating cloud resources (use provider CLI/API)
- Running commands (Claude does this)
- Starting servers (Claude does this)

**Example:**

```xml
<task type="checkpoint:human-action" gate="blocking">
  <automation-attempted>
    Configured Stripe webhook endpoint at https://myapp.com/api/webhooks/stripe.
    Sent test webhook via Stripe CLI.
  </automation-attempted>
  <what-you-need-to-do>
    In Stripe Dashboard:
    1. Go to Developers → Webhooks
    2. Add endpoint: https://myapp.com/api/webhooks/stripe
    3. Select events: payment_intent.succeeded, payment_intent.failed
    4. Copy webhook signing secret
    5. Paste secret here: [user pastes]
  </what-you-need-to-do>
  <ill-verify-after>
    Will add secret to .env.local as STRIPE_WEBHOOK_SECRET.
    Will send test event via Stripe CLI.
    Will verify webhook handler receives and processes event.
  </ill-verify-after>
  <resume-signal>Paste webhook signing secret</resume-signal>
</task>
```

## Workflow Structure

Workflows use `<step>` elements:

```xml
<process>

<step name="load_state" priority="first">
Read .planning/STATE.md before any operation.

Parse current position, decisions, blockers.
</step>

<step name="discover_plans">
List all PLAN.md files in phase directory:

```bash
ls .planning/phases/01-*/*-PLAN.md
```

Extract wave numbers from frontmatter.
</step>

<step name="execute_waves">
For each wave in sequence:
  1. Read all plan files
  2. Spawn gsd-executor agents (parallel)
  3. Wait for completion
  4. Verify SUMMARYs exist
</step>

</process>
```

**Step Attributes:**
- `name` - snake_case identifier
- `priority` - Optional: "first", "second" (execution order hint)

## Agent Structure

Agents define roles and execution flows:

```xml
<role>
You are a GSD {agent-name}. You {primary-purpose}.

Your job: {specific-responsibility}

Core responsibilities:
- {responsibility-1}
- {responsibility-2}
</role>

<philosophy>
Core principles guiding this agent's work.

## Principle 1
Explanation...

## Principle 2
Explanation...
</philosophy>

<execution_flow>

<step name="step_1" priority="first">
Instructions...
</step>

<step name="step_2">
More instructions...
</step>

</execution_flow>

<success_criteria>
Agent work complete when:
- [ ] Criterion 1
- [ ] Criterion 2
</success_criteria>
```

## Common Tags Reference

### Commands

- `<objective>` - What/why/when to use command
- `<execution_context>` - @-references to workflows
- `<context>` - Dynamic content, arguments
- `<process>` - Implementation steps
- `<success_criteria>` - Measurable completion

### Workflows

- `<purpose>` - What workflow accomplishes
- `<required_reading>` - Files to load first
- `<process>` - Container for steps
- `<step>` - Individual execution step
- `<success_criteria>` - Completion criteria

### Plans

- `<objective>` - What and why
- `<execution_context>` - @-references
- `<context>` - Files to load
- `<tasks>` - Container for task list
- `<task>` - Individual task
- `<verification>` - Overall checks
- `<success_criteria>` - Measurable completion
- `<output>` - Where to create SUMMARY

### Tasks

**Auto task:**
- `<name>` - Task name
- `<files>` - Paths
- `<action>` - Instructions
- `<verify>` - Proof
- `<done>` - Acceptance

**TDD task:**
- `<behavior>` - Expected behavior
- `<implementation>` - How to implement

**Checkpoint task:**
- `<what-built>` - What was automated
- `<how-to-verify>` - Steps
- `<resume-signal>` - How to continue

**Decision task:**
- `<decision>` - What to decide
- `<context>` - Why it matters
- `<options>` - Option list
- `<resume-signal>` - How to respond

**Human action task:**
- `<automation-attempted>` - What Claude did
- `<what-you-need-to-do>` - Manual step
- `<ill-verify-after>` - Verification
- `<resume-signal>` - How to continue

### Agents

- `<role>` - Agent purpose
- `<philosophy>` - Guiding principles
- `<execution_flow>` - Step-by-step process
- `<success_criteria>` - Completion criteria

## Validation Rules

1. **No generic tags**: No `<section>`, `<item>`, `<content>`
2. **Semantic meaning**: Tags describe purpose
3. **Markdown for content**: Use Markdown inside XML
4. **Attributes for metadata**: Classification and flags
5. **Required elements**: Each task type has required fields
6. **Clear resume signals**: Always specify how to continue

## Examples

See:
- `get-shit-done/templates/phase-prompt.md` - Full plan example
- `agents/gsd-planner.md` - Agent with XML structure
- `get-shit-done/workflows/execute-phase.md` - Workflow steps

## Next Steps

- **Templates**: See [Templates](./templates.md) for structure
- **Core Concepts**: See [Core Concepts](./core-concepts.md#8-xml-prompt-formatting) for design rationale
