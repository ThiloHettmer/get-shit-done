## Context Budget Rules

Plans should complete within ~50% context (not 80%). No context anxiety, quality maintained start to finish, room for unexpected complexity.

**Each plan: 2-3 tasks maximum.**

| Task Complexity           | Tasks/Plan | Context/Task | Total   |
| ------------------------- | ---------- | ------------ | ------- |
| Simple (CRUD, config)     | 3          | ~10-15%      | ~30-45% |
| Complex (auth, payments)  | 2          | ~20-30%      | ~40-50% |
| Very complex (migrations) | 1-2        | ~30-40%      | ~30-50% |

## Split Signals

**ALWAYS split if:**

- More than 3 tasks
- Multiple subsystems (DB + API + UI = separate plans)
- Any task with >5 file modifications
- Checkpoint + implementation in same plan
- Discovery + implementation in same plan

**CONSIDER splitting:** >5 files total, complex domains, uncertainty about approach, natural semantic boundaries.

## Depth Calibration

| Depth         | Typical Plans/Phase | Tasks/Plan |
| ------------- | ------------------- | ---------- |
| Quick         | 1-3                 | 2-3        |
| Standard      | 3-5                 | 2-3        |
| Comprehensive | 5-10                | 2-3        |

Derive plans from actual work. Depth determines compression tolerance, not a target.
