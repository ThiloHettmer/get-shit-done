# Realistic Token Reduction Strategy

**Date:** 2026-01-26  
**Context:** After discovering that `@file.md#section` syntax doesn't work in Cursor/OpenCode  
**Status:** Actionable implementation plan

---

## Current Situation

### What Doesn't Work

The recent p0-a1 and p0-a2 refactoring tasks created excellent **design documentation** but deliver **zero actual token savings** because:

1. **`@file.md#section` syntax is not supported** by Cursor or OpenCode
   - Both platforms load entire files regardless of `#anchor`
   - The section references are architectural prep, not functional code

2. **Conditional loading is pseudocode** in `execute-phase.md`
   - The `{if plan.autonomous === false}` blocks are comments
   - Orchestrator doesn't parse or execute these conditions
   - All agents receive the same full context

3. **Claimed savings are theoretical**
   - p0-a1: "8-12k tokens per phase" - Not realized
   - p0-a2: "27k tokens per phase" - Not realized
   - Combined: "35k per phase" - Pure projection

### What We Have

✅ Standardized section naming conventions (lowercase-hyphen)  
✅ Excellent documentation of intended behavior  
✅ Detailed token measurements (of hypothetical implementation)  
✅ Infrastructure ready for when platforms add support  
❌ **Zero functional token reduction**

---

## Actual Options for Token Reduction

### Option 1: Manual Section Extraction ⭐ RECOMMENDED
**Effort:** High | **Reward:** High | **Risk:** Medium

The orchestrator reads files, parses markdown sections, and inlines only needed parts.

**Implementation:**
```javascript
// Orchestrator needs section parsing logic
function extractSection(filePath, sectionName) {
  const content = readFile(filePath)
  const sections = parseMarkdownHeadings(content)
  return sections[sectionName] || content // fallback to full file
}

// Build prompt with extracted sections
const prompt = `
<execution_context>
${extractSection('templates/summary.md', 'file-template')}
${plan.autonomous === false ? extractSection('references/checkpoints.md', 'checkpoint-protocol') : ''}
</execution_context>
`
```

**Token Savings:** 8-12k per phase (p0-a1 target becomes real)  
**Timeline:** 3-5 days implementation  

---

### Option 2: Split Large Files ⭐ QUICK WIN
**Effort:** Low | **Reward:** Medium | **Risk:** Low

Instead of sections in one file, create actual separate files that can be conditionally referenced.

**Current Structure:**
```
references/
  checkpoints.md          (5,390 tokens - 1,078 lines)
  tdd.md                  (1,315 tokens - 263 lines)
```

**New Structure:**
```
references/
  checkpoints/
    human-verify.md       (~500 tokens - verification patterns)
    decision.md           (~400 tokens - decision checkpoints)
    human-action.md       (~200 tokens - manual action gates)
    core.md               (~800 tokens - shared checkpoint logic)
  tdd/
    red-green-refactor.md (~600 tokens - TDD cycle)
    test-patterns.md      (~400 tokens - test structure)
    core.md               (~300 tokens - TDD philosophy)
  execution/
    deviation-rules.md    (~2,000 tokens)
    task-commit.md        (~800 tokens)
    authentication.md     (~1,000 tokens)
```

**Usage:**
```markdown
<!-- Standard autonomous plan -->
@references/execution/task-commit.md
@references/git-integration.md

<!-- Plan with checkpoints -->
@references/execution/task-commit.md
@references/checkpoints/human-verify.md
@references/git-integration.md

<!-- TDD plan -->
@references/execution/task-commit.md
@references/tdd/red-green-refactor.md
@references/git-integration.md
```

**Token Savings:** 27k per phase (p0-a2 target becomes real)  
**Timeline:** 1-2 days file reorganization  
**Works Today:** Yes - standard file references

---

### Option 3: True Conditional Orchestrator ⭐ ESSENTIAL
**Effort:** Medium | **Reward:** High | **Risk:** Low

Make the orchestrator actually parse plan frontmatter and conditionally load files.

**Current (pseudocode in comments):**
```markdown
{if plan.autonomous === false OR plan.autonomous is missing:}
@~/.claude/get-shit-done/references/checkpoints.md
{/if}
```

**Actual Implementation:**
```typescript
// In execute-phase.md orchestrator
async function buildExecutorPrompt(planPath: string) {
  const planContent = readFile(planPath)
  const planMeta = parseFrontmatter(planContent)
  
  // Core files (always loaded)
  const contextFiles = [
    'workflows/execute-plan.md',
    'templates/summary.md#file-template', // if Option 1 implemented
    'references/git-integration.md'
  ]
  
  // Conditional loading based on plan metadata
  if (planMeta.autonomous === false || planMeta.autonomous === undefined) {
    contextFiles.push('references/checkpoints.md')
  }
  
  if (planMeta.type === 'tdd') {
    contextFiles.push('references/tdd.md')
  }
  
  // Load and inline all files
  const context = contextFiles.map(file => {
    if (file.includes('#')) {
      const [path, section] = file.split('#')
      return extractSection(path, section) // Option 1
    }
    return readFile(file)
  }).join('\n\n')
  
  return buildPrompt(context, planContent, stateContent)
}
```

**Token Savings:** Enables all conditional loading strategies  
**Timeline:** 2-3 days orchestrator logic  
**Prerequisites:** Frontmatter parsing, file reading utilities

---

### Option 4: Compress Agent Prompts ⭐ QUICK WIN
**Effort:** Low | **Reward:** Medium | **Risk:** Low

Agents use verbose explanations. Compress without losing meaning.

**Example - Current (verbose):**
```markdown
<deviation_rules>
**While executing tasks, you WILL discover work not in the plan.** This is normal.

Apply these rules automatically. Track all deviations for Summary documentation.

---

**RULE 1: Auto-fix bugs**

**Trigger:** Code doesn't work as intended (broken behavior, incorrect output, errors)

**Action:** Fix immediately, track for Summary

**Examples:**
- Wrong SQL query returning incorrect data
- Logic errors (inverted condition, off-by-one, infinite loop)
- Type errors, null pointer exceptions, undefined references
```

**Compressed (same info):**
```markdown
<deviation_rules>
Auto-apply, track all for Summary.

**Rule 1 - Auto-fix bugs:** Broken behavior/errors/logic issues → fix immediately

**Examples:** SQL errors, off-by-one, type errors, null refs
```

**Files to Compress:**
- `agents/gsd-executor.md` - Currently ~784 lines, target ~500 lines
- `agents/gsd-planner.md` - Currently ~1,386 lines, target ~900 lines
- `agents/gsd-verifier.md` - Currently ~779 lines, target ~500 lines

**Token Savings:** ~2-3k per agent × 5-8 spawns = 10-24k per phase  
**Timeline:** 2-3 days editing  
**Risk:** Low - careful rewriting maintains meaning

---

### Option 5: Lazy Agent Loading (p2-g3)
**Effort:** High | **Reward:** Very High | **Risk:** Medium-High

Extract agent protocols to separate files, spawn with minimal core, load protocols on-demand.

**Current Structure:**
```
agents/
  gsd-executor.md         (7,800 tokens all loaded upfront)
    - Core execution        (~2,000 tokens)
    - Deviation rules       (~2,000 tokens)
    - Checkpoint protocol   (~2,000 tokens)
    - TDD execution         (~1,500 tokens)
    - Git/commit            (~1,500 tokens)
```

**Target Structure:**
```
agents/
  gsd-executor.md         (3,500 tokens - minimal core)
    - Role & critical steps
    - Basic execution flow
    - Git integration (always needed)

references/execution-protocols/
  deviation-handling.md   (2,000 tokens - on-demand)
  checkpoint-return.md    (2,000 tokens - on-demand)
  tdd-cycle.md           (1,500 tokens - on-demand)
```

**Loading Logic:**
```typescript
// Agent starts minimal
spawn(executorCore)

// Load protocols when triggered
if (task.type === 'checkpoint') {
  injectProtocol('checkpoint-return.md')
}

if (discoveredDeviation) {
  injectProtocol('deviation-handling.md')
}
```

**Challenge:** Agents need mechanism to "request" additional context mid-execution.

**Token Savings:** 24-40k per phase (as estimated in p2-g3)  
**Timeline:** 1-2 weeks implementation + testing  
**Risk:** Medium-high - requires dynamic protocol injection

---

### Option 6: Inline-Only Prompts
**Effort:** High | **Reward:** Maximum Control | **Risk:** High

Abandon `@` syntax completely. Orchestrator builds entire prompt programmatically.

**Benefits:**
- Complete control over what's loaded
- Can implement any conditional logic
- Can extract sections, compress, transform
- Maximum token efficiency

**Drawbacks:**
- Lose markdown-based prompt simplicity
- Orchestrator becomes complex
- Harder to maintain/debug prompts
- Complete rewrite of spawn logic

**Token Savings:** Maximum possible  
**Timeline:** 2-3 weeks full rewrite  
**Recommended:** Only if other options insufficient

---

## Recommended Implementation Plan

### Phase 1: Quick Wins (1-2 days) 🎯 START HERE

**Goal:** Immediate token reduction with minimal risk

1. ✅ **Split Large Reference Files** (Option 2)
   - Break `checkpoints.md` into separate files
   - Break `tdd.md` into separate files
   - Create focused, modular reference files
   - **Savings:** ~15-20k per phase

2. ✅ **Compress Agent Prompts** (Option 4)
   - Edit `gsd-executor.md` for terseness
   - Edit `gsd-planner.md` for terseness
   - Remove verbose examples, keep essentials
   - **Savings:** ~10-15k per phase

3. ✅ **True Conditional Orchestrator** (Option 3)
   - Implement frontmatter parsing
   - Add conditional file loading logic
   - Make the `{if}` blocks actually work
   - **Savings:** Enables all conditional strategies

**Phase 1 Total Savings:** 25-35k per phase  
**As % of phase execution:** 0.15-0.35% reduction (phase uses 10-20M tokens)  
**But across 20 phases:** 500-700k total reduction

---

### Phase 2: Manual Section Loading (3-5 days)

**Goal:** Enable section-based loading without platform support

1. ✅ **Implement Section Parser** (Option 1)
   - Markdown heading parser
   - Section extraction utilities
   - Fallback to full file if section missing

2. ✅ **Update Template References**
   - Use section extraction for templates
   - Inline only needed sections
   - Test all agent spawn paths

3. ✅ **Update Reference Loading**
   - Extract protocol sections on-demand
   - Combine with file splitting from Phase 1

**Phase 2 Additional Savings:** 10-15k per phase  
**Cumulative with Phase 1:** 35-50k per phase (0.25-0.5% reduction)

---

### Phase 3: Lazy Agent Loading (1-2 weeks)

**Goal:** Dynamic protocol loading for maximum efficiency

1. ✅ **Extract Agent Protocols** (Option 5)
   - Move deviation rules to separate file
   - Move checkpoint protocols to separate file
   - Move TDD protocols to separate file

2. ✅ **Implement Dynamic Loading**
   - Agent core spawns minimal
   - Load protocols when triggered
   - Test all execution paths

3. ✅ **Validate Quality**
   - Ensure no regression in agent behavior
   - Verify all protocols load correctly
   - Test edge cases

**Phase 3 Additional Savings:** 20-30k per phase  
**Cumulative total:** 55-80k per phase (0.4-0.8% reduction)  
**Over full project:** 1.1-1.6M tokens saved

---

## Total Realistic Savings

### Real-World Context

**Actual token usage from production:**
- Planning phase: **~25M tokens input** (24M cached on DeepSeek)
- Phase 1 execution: **10-20M tokens input**
- Single project: **~200-300M total tokens** (planning + all phases)

**Current optimization targets:**
- Per execution phase: 55-80k tokens saved
- This is **0.5-0.8%** of phase execution tokens
- But multiplied across 20 phases = **1.1-1.6M tokens**
- That's **~1% of total project cost**

### Conservative Estimate (Per Project)
- Phase 1 quick wins: 25k × 20 phases = **500k tokens**
- Phase 2 section loading: 10k × 20 phases = **200k tokens**
- Phase 3 lazy loading: 20k × 20 phases = **400k tokens**
- **Total: 1.1M tokens saved**

**Cost impact:** $0.30 per project (at $0.27/1M tokens)  
**Percentage reduction:** ~0.5-1% of total project tokens

### Optimistic Estimate (Per Project)
- Phase 1 quick wins: 35k × 20 phases = **700k tokens**
- Phase 2 section loading: 15k × 20 phases = **300k tokens**
- Phase 3 lazy loading: 30k × 20 phases = **600k tokens**
- **Total: 1.6M tokens saved**

**Cost impact:** $0.43 per project (at $0.27/1M tokens)  
**Percentage reduction:** ~0.8-1.5% of total project tokens

### Reality Check

The savings are **modest in percentage terms** but meaningful when:
- Running dozens of projects
- Using expensive models (Claude Opus vs DeepSeek)
- Every optimization compounds

**The real win:** Better than 0% improvement (current status)

---

## What NOT to Do

### ❌ Wait for Platform Support
Don't wait for Cursor/OpenCode to add `@file.md#section` syntax.
- Unknown timeline
- May never happen
- We can implement it ourselves

### ❌ Continue Documenting Without Implementing
The current p0-a1/p0-a2 work is excellent documentation but delivers zero value.
- No more theoretical measurements
- No more pseudocode in comments
- Implement actual working code

### ❌ Over-optimize Prematurely
Don't jump to Option 6 (Inline-Only Prompts) without trying simpler options first.
- Start with file splitting
- Add conditional loading
- Only go full inline if needed

---

## Success Metrics

### Phase 1 Complete When:
- [ ] Reference files split and organized
- [ ] Agents compressed by 20-30%
- [ ] Orchestrator conditionally loads files
- [ ] All execution paths tested
- [ ] Measured token savings documented

### Phase 2 Complete When:
- [ ] Section parser implemented
- [ ] Template loading uses sections
- [ ] Backwards compatibility maintained
- [ ] Additional 10-15k savings validated

### Phase 3 Complete When:
- [ ] Agent protocols extracted
- [ ] Dynamic loading working
- [ ] No quality regression
- [ ] Full 55-80k per phase savings achieved

---

## Next Steps

1. **Decide on approach** - Review options, confirm Phase 1 plan
2. **Create implementation branch** - `feat/actual-token-reduction`
3. **Start with file splitting** - Quick win, low risk
4. **Implement conditional logic** - Make orchestrator smart
5. **Measure real savings** - Track actual token usage
6. **Iterate based on results** - Adjust strategy as needed

---

## Notes

- This plan prioritizes **working code over documentation**
- Each phase delivers **measurable token reduction**
- Phases can be implemented **incrementally**
- Success is validated by **actual usage metrics**
- The goal is **real savings, not theoretical projections**

### Important Context

**Real-world scale from production usage:**
- Planning: 25M tokens (24M cached on DeepSeek)
- Phase execution: 10-20M tokens per phase
- Full project: 200-300M tokens total

**These optimizations provide:**
- Modest percentage gains (0.5-1.5% per project)
- But meaningful absolute savings (1.1-1.6M tokens)
- Compound effect across multiple projects
- Better than current 0% improvement

**The honest assessment:** This isn't revolutionary, but it's better than vaporware documentation.

---

**Status:** Ready to implement  
**Blocked by:** None  
**Requires:** Decision to proceed with Phase 1
