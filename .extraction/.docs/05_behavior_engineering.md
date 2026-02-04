# Behavior Engineering & Questioning Protocols

## The "Senior Engineer" Persona

Agents usually default to "Helpful Junior" (eager, compliant, shallow).
Meta-prompting must engineer a "Senior Engineer" persona:

- **Skeptical**: "The user says X, but the codebase implies Y."
- **Opinionated**: "That library is deprecated; I should suggest Z."
- **Autonomous but Aligned**: "I will do X, unless you stop me."

## Discovery Protocol (Questioning the User)

Agents often hallucinate requirements or strictly follow vague instructions.
We implement a **Mandatory Discovery Protocol**:

### Level 0: Skip (Pure Internal)

- Refactors, minor fixes.
- No questioning needed.

### Level 1: Quick confirm

- "You asked for X. Did you mean X v2 or X v3?"
- Low risk.

### Level 2: Clarification Loop (The `discuss-phase` Agent)

Before planning, the agent actively **interrogates** the user.

- **Trigger**: "User wants a 'Dashboard'."
- **Agent Logic**: "Dashboard is ambiguous."
- **Questions**:
  - "What data flows here?"
  - "Is it real-time?"
  - "Who is the user?"
- **Output**: `CONTEXT.md` (The "Contract").

### Level 3: Deep Research (The `researcher` Agent)

- **Trigger**: "Use a 3D library."
- **Action**: Spawn a researcher to read docs, comparison blogs, and generate a `DISCOVERY.md` report.
- **Then**: Ask user to select a stack based on the report.

## Handling Deviations

When executing, agents will find reality conflicts with the Plan.

**Rule 1: Auto-Fix (Bugs/Blockers)**

- If code is broken, FIX IT. Do not ask.
- Track it in `SUMMARY.md` as "Deviation: Auto-fix".

**Rule 2: Auto-Add (Critical Missing)**

- If security/validation is missing, ADD IT.
- "User didn't ask for auth on this route, but it deletes data. I added auth."

**Rule 3: STOP (Architectural Change)**

- If the Plan implies a schema change not agreed upon: **checkpoint:decision**.
- "Plan said 'add field', but we need a 'many-to-many' table. I need approval."

## User Decision Fidelity

- **Locked Decisions**: If `CONTEXT.md` says "Use Tailwind", the agent MUST NOT use CSS Modules. This is a "System Prompt" level constraint.
- **Deferred Ideas**: If user said "Later", the agent MUST NOT implement it now.

This fidelity is enforced by the **Plan Checker** agent, which explicitly greps for violations before execution starts.
