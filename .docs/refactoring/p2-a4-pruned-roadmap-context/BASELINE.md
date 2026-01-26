# P2-A4 Baseline Measurements

**Date:** 2026-01-26  
**Task:** Pruned Roadmap Context

## Current Token Usage

### Roadmap Template Analysis

**File:** `get-shit-done/templates/roadmap.md`
- Word count: 838 words
- Estimated tokens: ~1,100-1,200 tokens (at 1.3-1.4 words per token)

**Structure:**
- 4 example phases in initial-roadmap section
- Each phase contains:
  - Goal statement (~10-15 words)
  - Dependencies (~5 words)
  - Requirements list (~10-20 words)
  - Success criteria (2-5 items, ~50-100 words)
  - Plans count (~3 words)
  - Plan list with descriptions (~30-80 words per phase)
- Progress table (~50-100 words)

**Per-Phase Estimate:**
- Minimal phase entry: ~200 tokens
- Standard phase entry: ~300-400 tokens  
- Detailed phase entry: ~400-500 tokens

### Scaling Projections

| Phase Count | Full ROADMAP.md | Current+Adjacent Only |
|-------------|-----------------|----------------------|
| 3 phases    | ~1,500 tokens   | ~800 tokens          |
| 5 phases    | ~2,500 tokens   | ~900 tokens          |
| 8 phases    | ~4,000 tokens   | ~1,000 tokens        |
| 10 phases   | ~5,000 tokens   | ~1,000 tokens        |

**Savings per phase execution:**
- Early project (3 phases): ~700 tokens
- Mid project (5 phases): ~1,600 tokens
- Large project (10 phases): ~4,000 tokens

**Across 10 phase executions:**
- Early: ~7k tokens saved
- Mid: ~16k tokens saved
- Large: ~40k tokens saved

## Implementation Target

**Create:** `.planning/ROADMAP-CURRENT.md`
- Header + milestone info: ~100 tokens
- Previous phase (brief): ~100 tokens
- Current phase (full): ~400 tokens
- Next phase (brief): ~100 tokens
- **Total:** ~700-1,000 tokens (constant regardless of project size)

## Files That Load ROADMAP.md

### Should Use Pruned Version (ROADMAP-CURRENT.md)
- `agents/gsd-planner.md` - Line 416
- `agents/gsd-verifier.md` - Indirectly via workflow

### Should Keep Full Version (ROADMAP.md)
- `get-shit-done/workflows/execute-phase.md`
- `get-shit-done/workflows/execute-plan.md`
- All commands that manipulate roadmap structure
- User-facing documentation

## Expected Outcome

**Token reduction:** 700-4,000 tokens per phase execution  
**Scaling:** Savings increase with project size  
**No information loss:** Current phase context fully preserved  
**Backward compatible:** Full ROADMAP.md still maintained for orchestrators
