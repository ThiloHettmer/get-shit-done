# Test Scenarios - p0-a2-context-aware-references

## Objective

Verify that conditional reference loading works correctly for all plan types and safely falls back to loading all references when metadata is unclear.

## Test Scenarios

### Scenario 1: Standard Autonomous Plan

**Plan metadata:**
```yaml
type: execute
autonomous: true
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ❌ checkpoints.md (not needed)
- ❌ tdd.md (not needed)

**Expected token load:** ~1,270 tokens (references only)

---

### Scenario 2: Plan with Checkpoints

**Plan metadata:**
```yaml
type: execute
autonomous: false
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ✅ checkpoints.md (needed - autonomous: false)
- ❌ tdd.md (not needed)

**Expected token load:** ~6,660 tokens (references only)

---

### Scenario 3: TDD Plan (Autonomous)

**Plan metadata:**
```yaml
type: tdd
autonomous: true
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ❌ checkpoints.md (not needed)
- ✅ tdd.md (needed - type: tdd)

**Expected token load:** ~2,585 tokens (references only)

---

### Scenario 4: TDD Plan with Checkpoints

**Plan metadata:**
```yaml
type: tdd
autonomous: false
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ✅ checkpoints.md (needed - autonomous: false)
- ✅ tdd.md (needed - type: tdd)

**Expected token load:** ~7,975 tokens (references only - all loaded)

---

### Scenario 5: Missing `autonomous` Flag (Safe Fallback)

**Plan metadata:**
```yaml
type: execute
# autonomous: MISSING
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ✅ checkpoints.md (loaded - safe default)
- ❌ tdd.md (not needed)

**Expected token load:** ~6,660 tokens (safe fallback)

**Reasoning:** Better to load checkpoints unnecessarily than to miss them when needed.

---

### Scenario 6: Missing `type` Flag (Safe Fallback)

**Plan metadata:**
```yaml
# type: MISSING
autonomous: true
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ❌ checkpoints.md (not needed - autonomous: true)
- ✅ tdd.md (loaded - safe default)

**Expected token load:** ~2,585 tokens (safe fallback)

**Reasoning:** Type defaults to "execute", but loading TDD reference is safe if unclear.

---

### Scenario 7: Malformed Frontmatter (Full Fallback)

**Plan metadata:**
```yaml
# Malformed or unparseable
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ✅ checkpoints.md (loaded - safe default)
- ✅ tdd.md (loaded - safe default)

**Expected token load:** ~7,975 tokens (full fallback)

**Reasoning:** When in doubt, load everything. Quality over optimization.

---

### Scenario 8: Gap Closure Plan (Future Enhancement)

**Plan metadata:**
```yaml
type: execute
autonomous: true
gap_closure: true
```

**Expected references loaded:**
- ✅ execute-plan.md (always)
- ✅ summary.md (always)
- ✅ git-integration.md (always)
- ❌ checkpoints.md (not needed)
- ❌ tdd.md (not needed)
- ✅ verification-patterns.md (future - if gap_closure flag implemented)

**Current behavior:** Gap closure flag not yet implemented, treat as standard plan

**Future enhancement:** Load verification-patterns.md when gap_closure: true

---

## Validation Checklist

For each scenario:

- [ ] Parse plan frontmatter correctly
- [ ] Apply conditional loading logic
- [ ] Include correct references in execution_context
- [ ] No broken references or missing guidance
- [ ] Safe fallback when metadata unclear
- [ ] Token usage matches expectations

## Success Criteria

1. ✅ Standard autonomous plans load minimal references (~1,270 tokens)
2. ✅ Checkpoint plans load checkpoints.md (~6,660 tokens)
3. ✅ TDD plans load tdd.md (~2,585 tokens)
4. ✅ Missing metadata defaults to safe fallback (load more, not less)
5. ✅ No execution quality regression
6. ✅ Per-executor savings: 5-7k tokens on average

## Testing Approach

Since this is meta-prompting (agents reading these workflows):

1. **Syntax validation:** Ensure conditional logic is valid Markdown/prose
2. **Logic validation:** Trace through each scenario manually
3. **Safe defaults:** Verify fallback behavior is safe (load when uncertain)
4. **Documentation:** Clear comments explaining conditional logic

No runtime testing needed - the orchestrator (human or agent) interprets the workflow prose and applies the logic.

## Edge Cases

| Edge Case | Behavior | Safe? |
|-----------|----------|-------|
| Empty frontmatter | Load all references | ✅ Safe |
| Only `type` field | Use type, default autonomous: false | ✅ Safe |
| Only `autonomous` field | Default type: execute | ✅ Safe |
| Unknown type value | Treat as "execute" | ✅ Safe |
| `autonomous: null` | Treat as false (load checkpoints) | ✅ Safe |

**Principle:** When in doubt, over-include rather than under-include. Quality > optimization.
