## Building the Dependency Graph

**For each task, record:**

- `needs`: What must exist before this runs
- `creates`: What this produces
- `has_checkpoint`: Requires user interaction?

**Wave assignment algorithm:**

```
waves = {}
for each plan in plan_order:
  if plan.depends_on is empty:
    plan.wave = 1
  else:
    plan.wave = max(waves[dep] for dep in plan.depends_on) + 1
  waves[plan.id] = plan.wave
```

## Vertical Slices vs Horizontal Layers

**Vertical slices (PREFER):**

```
Plan 01: User feature (model + API + UI)
Plan 02: Product feature (model + API + UI)
Plan 03: Order feature (model + API + UI)
```

Result: All three run parallel (Wave 1)

**Horizontal layers (AVOID):**

```
Plan 01: Create User model, Product model, Order model
Plan 02: Create User API, Product API, Order API
Plan 03: Create User UI, Product UI, Order UI
```

Result: Fully sequential (02 needs 01, 03 needs 02)

**When vertical slices work:** Features are independent, self-contained, no cross-feature dependencies.

**When horizontal layers necessary:** Shared foundation required (auth before protected features), genuine type dependencies, infrastructure setup.
