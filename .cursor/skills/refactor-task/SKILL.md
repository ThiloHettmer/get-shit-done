# Token Reduction Refactoring Skill

**Trigger:** When user wants to work on a token reduction refactoring task  
**Usage:** `@refactor-task [task-name]` or "work on refactoring task [task-name]"

---

## Purpose

This skill autonomously implements token reduction refactoring tasks from `.docs/refactoring/`. It follows a structured workflow: read summary → research → create subtasks → implement → validate. The agent proceeds through all phases automatically, reporting progress but not waiting for user approval.

---

## When to Use This Skill

Use when the user asks to:
- "Work on refactoring task [name]"
- "Implement [task-name] from refactoring docs"
- "Start working on p0-a1-lazy-template-loading"
- "Refactor [task-name]"

---

## Workflow

**Note:** This workflow executes autonomously. Progress is reported at each phase, but the agent proceeds without waiting for user approval.

### Phase 1: Read & Understand (5-10 minutes)

**1. Load the task summary:**
```bash
# User provides task name like "p0-a1-lazy-template-loading"
TASK_DIR=".docs/refactoring/${TASK_NAME}"
cat "${TASK_DIR}/SUMMARY.md"
```

**2. Extract key information:**
- Priority level (P0/P1/P2/P3)
- Category (A/B/C/D/E/F/G)
- Token savings estimate
- Implementation complexity
- Risk level
- Current behavior
- Proposed behavior
- Affected files list
- Dependencies on other tasks

**3. Present summary to user and proceed:**
```markdown
## Task: [Task Name]
**Priority:** [P0/P1/P2/P3] | **Category:** [Category] | **Risk:** [Low/Medium/High]

**Token Savings:** [X-Y]k per [phase/project]

**What We're Changing:**
[Current → Proposed in 2-3 sentences]

**Files to Modify:** [N] files
**Dependencies:** [List or "None"]

Proceeding to research phase...
```

---

### Phase 2: Research & Analysis (10-20 minutes)

**1. Examine affected files:**
- Read all files listed in "Affected Files" section
- Understand current implementation patterns
- Identify related code that might be impacted
- Check for existing utilities that could be reused

**2. Trace dependencies:**
- Check if dependent tasks are complete (if any)
- Identify files that reference the files we'll modify
- Search for patterns that might be affected

**3. Document findings:**
```markdown
## Research Findings

### Current Implementation
- [Key patterns found]
- [How it currently works]
- [Token usage points identified]

### Impact Analysis
- [What will change]
- [What might break]
- [Edge cases to handle]

### Dependencies Status
- [✓/✗] Task X: [status]
- [✓/✗] Task Y: [status]

### Risks Identified
- [Risk 1]: [Mitigation]
- [Risk 2]: [Mitigation]
```

---

### Phase 3: Create Subtasks (5-10 minutes)

**1. Break down implementation into atomic steps:**

Based on "Implementation Requirements" section, create 5-15 subtasks following this pattern:

```markdown
## Implementation Subtasks

### Setup
- [ ] 1. Create backup branch for rollback
- [ ] 2. Create test directory/files for validation
- [ ] 3. Document baseline token measurements

### Core Implementation
- [ ] 4. [Specific change to specific file]
- [ ] 5. [Next specific change]
- [ ] 6. [Another change]
[... continue based on requirements]

### Integration
- [ ] [N-2]. Update all references to modified files
- [ ] [N-1]. Run tests and verify no regressions

### Validation
- [ ] [N]. Measure token reduction
- [ ] [N+1]. Validate against success criteria
- [ ] [N+2]. Document changes in task directory
```

**2. Sequence subtasks correctly:**
- Setup tasks first
- Core implementation in logical order
- Integration after core changes
- Validation last

**3. Present subtasks and proceed:**
```markdown
## Subtasks Created

I've broken this down into [N] subtasks:

**Setup (3 tasks):** Preparation and baseline
**Core ([X] tasks):** Main implementation changes
**Integration ([Y] tasks):** Wire everything together
**Validation ([Z] tasks):** Verify success

Beginning implementation...
```

---

### Phase 4: Implementation (30-90 minutes)

**Execute subtasks sequentially:**

**For each subtask:**

1. **Announce what you're doing:**
   ```markdown
   ### Subtask [N]: [Description]
   
   Working on: [specific file/change]
   Expected outcome: [what this achieves]
   ```

2. **Make the change:**
   - Read affected files
   - Make precise modifications
   - Follow the proposed approach from SUMMARY.md
   - Maintain backwards compatibility where specified

3. **Verify the change:**
   - Check syntax (if applicable)
   - Verify references are updated
   - Run any relevant tests
   - Check for linter errors

4. **Mark complete:**
   ```markdown
   ✓ Subtask [N] complete
   - Changed: [files]
   - Result: [outcome]
   ```

5. **Continue to next subtask**

**Key Principles:**
- Make changes incrementally (one subtask at a time)
- Test after each significant change
- Don't skip subtasks
- If a subtask fails, diagnose and adapt approach automatically
- Keep user informed of progress (but continue working)
- Proceed through all subtasks without waiting for approval

---

### Phase 5: Validation (10-20 minutes)

**1. Verify Success Criteria:**

Load success criteria from SUMMARY.md and check each one:

```markdown
## Validation Results

Checking success criteria from SUMMARY.md:

- [✓/✗] Criterion 1: [Result]
- [✓/✗] Criterion 2: [Result]
- [✓/✗] Criterion 3: [Result]
[... all criteria from SUMMARY.md]

**Status:** [X]/[Y] criteria met
```

**2. Measure Token Reduction:**

Estimate token savings achieved:
- Count tokens in modified files (before/after)
- Compare against estimated savings in SUMMARY
- Report actual vs expected

```markdown
## Token Measurement

**Estimated Savings:** [X-Y]k tokens per [phase/project]

**Actual Measurements:**
- File 1: [before] → [after] tokens (saved: [diff])
- File 2: [before] → [after] tokens (saved: [diff])
- Total: ~[N]k tokens saved

**Result:** [Met/Below/Exceeded] expectations
```

**3. Test Quality:**

Run quality checks:
```bash
# Check for syntax errors
find . -name "*.md" -type f | head -5 | xargs cat > /dev/null

# Check for broken references
grep -r "@.*\.md" agents/ get-shit-done/ | grep -v "^Binary" | head -10

# Run linter if applicable
npm run lint 2>/dev/null || echo "No linter configured"
```

**4. Document Completion:**

Create completion report in task directory:

```markdown
# [Task Name] - Completion Report

**Date:** [YYYY-MM-DD]
**Implemented by:** Cursor AI Agent
**Status:** [Complete/Partial]

## Changes Made

### Files Modified
- [file1]: [what changed]
- [file2]: [what changed]

### Implementation Notes
- [Key decision 1]
- [Key decision 2]
- [Deviations from plan, if any]

## Validation Results

### Success Criteria: [X]/[Y] met
[List criteria with checkmarks]

### Token Savings: ~[N]k tokens
[Breakdown by file/category]

### Quality Checks
- Syntax: [Pass/Fail]
- References: [Pass/Fail]
- Tests: [Pass/Fail]

## Issues Encountered
[List any issues and how they were resolved, or "None"]

## Follow-up Tasks
[Any remaining work or related tasks to consider, or "None"]

## Recommendations
[Suggestions for related improvements or next tasks]
```

**5. Update refactoring README:**

Mark task as complete in `.docs/refactoring/README.md`:
- Change status from "Not Started" to "Complete"
- Update percentage complete
- Add completion date

---

## Error Handling

### If Research Reveals Issues

**Problem:** Current implementation doesn't match SUMMARY expectations

**Action:**
1. Document discrepancy clearly
2. Automatically adjust approach to match reality
3. Note the discrepancy in completion report
4. Proceed with adapted implementation

### If Subtask Fails

**Problem:** A subtask cannot be completed as planned

**Action:**
1. Diagnose the issue
2. Report the problem with details
3. Automatically try alternative approaches:
   - First: Modify approach for this subtask
   - If that fails: Skip and mark as follow-up in completion report
   - If critical: Note the blocker and continue with other subtasks
4. Proceed to next subtask

### If Validation Fails

**Problem:** Success criteria not met or token savings below expected

**Action:**
1. Identify which criteria failed
2. Analyze why (implementation issue or unrealistic expectation)
3. Automatically attempt to fix implementation issues
4. If some criteria cannot be met, document as partial completion
5. Report final status with explanation of what was/wasn't achieved

### If Dependencies Missing

**Problem:** Task depends on incomplete task

**Action:**
1. Report missing dependencies
2. Automatically assess if task can proceed with workarounds
3. If possible: implement with notes about dependencies in completion report
4. If blocked: document blocker and proceed with non-dependent parts

---

## Best Practices

### DO:
- ✅ Read SUMMARY.md thoroughly before starting
- ✅ Break work into small, testable subtasks
- ✅ Validate after each significant change
- ✅ Keep user informed of progress (but don't wait for approval)
- ✅ Document everything clearly
- ✅ Measure token savings accurately
- ✅ Check backwards compatibility
- ✅ Update all references when moving/renaming
- ✅ Make reasonable autonomous decisions when issues arise
- ✅ Proceed through all phases without stopping

### DON'T:
- ❌ Skip the research phase
- ❌ Make changes without understanding impact
- ❌ Modify files not listed in SUMMARY
- ❌ Skip validation steps
- ❌ Assume token savings without measuring
- ❌ Leave broken references
- ❌ Forget to update documentation
- ❌ Wait for user approval between phases
- ❌ Stop work when encountering minor issues

---

## Example Usage

**User:** "Work on refactoring task p0-a1-lazy-template-loading"

**Agent Response:**
```markdown
## Starting Refactoring: p0-a1-lazy-template-loading

Loading task summary...

[Presents task overview from Phase 1]

Beginning research phase to examine:
- 18 template files
- 3 agent files (executor, planner, verifier)
- 2 workflow files

This will take ~10 minutes...
```

---

## Integration with Other Skills

- **After completion:** Suggest running related optimization tasks
- **Before starting:** Check if prerequisite tasks are complete
- **During work:** Reference `.docs/token-reduction-analysis.md` for context
- **For testing:** Consider creating test project to validate changes

---

## Success Metrics

A task is considered successfully completed when:

1. ✅ All success criteria from SUMMARY.md are met (or documented as partial)
2. ✅ Token savings achieved (within -20% to +50% of estimate)
3. ✅ No regressions in existing functionality
4. ✅ All tests pass (or no new failures)
5. ✅ Documentation updated appropriately
6. ✅ Completion report created in task directory

---

## Notes

- **Estimated time per task:** 1-3 hours depending on complexity
- **P0 tasks:** Highest priority, implement first
- **P3 tasks:** Lower priority, implement only if needed
- **Conflicting tasks:** Check `.docs/refactoring/README.md` for conflicts before starting
- **Token measurement:** Use approximate counts (exact tokenization varies by model)

---

## Progress Reporting

You should inform the user at these points (without waiting for approval):

1. **After Phase 1 (Read):** Present task overview and proceed to research
2. **After Phase 2 (Research):** Present findings and proceed to subtask creation
3. **After Phase 3 (Subtasks):** Show subtask breakdown and begin implementation
4. **During Phase 4 (Implementation):** Report progress on each subtask
5. **After Phase 5 (Validation):** Present final results and completion status

---

## Related Files

- **Task Summaries:** `.docs/refactoring/*/SUMMARY.md`
- **Overall Analysis:** `.docs/token-reduction-analysis.md`
- **Progress Tracking:** `.docs/refactoring/README.md`
- **Templates:** `get-shit-done/templates/*.md`
- **Agents:** `agents/gsd-*.md`
- **Workflows:** `get-shit-done/workflows/*.md`
- **References:** `get-shit-done/references/*.md`
