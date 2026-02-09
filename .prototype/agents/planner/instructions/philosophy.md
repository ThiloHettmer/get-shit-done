## Solo Developer + Claude Workflow

Planning for ONE person (the user) and ONE implementer (Claude).

- No teams, stakeholders, ceremonies, coordination overhead
- User = visionary/product owner, Claude = builder
- Estimate effort in Claude execution time, not human dev time

## Plans Are Prompts

PLAN.md IS the prompt (not a document that becomes one). Contains:

- Objective (what and why)
- Context (@file references)
- Tasks (with verification criteria)
- Success criteria (measurable)

## Quality Degradation Curve

| Context Usage | Quality   | Claude's State          |
| ------------- | --------- | ----------------------- |
| 0-30%         | PEAK      | Thorough, comprehensive |
| 30-50%        | GOOD      | Confident, solid work   |
| 50-70%        | DEGRADING | Efficiency mode begins  |
| 70%+          | POOR      | Rushed, minimal         |

**Rule:** Plans should complete within ~50% context. More plans, smaller scope, consistent quality. Each plan: 2-3 tasks max.

## Ship Fast

Plan -> Execute -> Ship -> Learn -> Repeat

**Anti-enterprise patterns (delete if seen):**

- Team structures, RACI matrices, stakeholder management
- Sprint ceremonies, change management processes
- Human dev time estimates (hours, days, weeks)
- Documentation for documentation's sake
