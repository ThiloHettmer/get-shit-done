# Summary Frontmatter Scanning

**Priority:** P3  
**Category:** A - Selective Context Loading  
**Estimated Token Savings:** 12-20k per planning phase  
**Implementation Complexity:** Low  
**Risk Level:** Low

## Overview

Planner agents scan all SUMMARY.md files to build dependency context. This task scans only frontmatter (first 30 lines) to quickly identify relevant summaries, then loads full content only for matches.

## Current Behavior

**Planner workflow:**
1. Discover all SUMMARY.md files (20-40 files)
2. Read each file completely (2,000-2,500 tokens each)
3. Extract frontmatter metadata (dependency graph, tech stack, patterns)
4. Determine which are relevant to current phase
5. Actually use content from 3-5 relevant summaries

**Token load:**
- 30 summaries × 2,000 tokens = 60,000 tokens
- Actually relevant: 4 summaries = 8,000 tokens
- **Waste: 52,000 tokens**

## Proposed Behavior

**Phase 1: Quick scan (frontmatter only):**

```bash
for summary in phases/*/SUMMARY.md; do
  head -30 "$summary"  # Just frontmatter (200-400 tokens)
done
```

**Frontmatter contains:**
- phase, plan, subsystem
- requires, provides, affects
- tech-stack added
- key-files created

**Phase 2: Match relevant summaries:**

```javascript
// Current phase: 05-core-features, subsystem: UI
matches = summaries.filter(s => 
  s.affects.includes('05') ||      // Explicitly affects current
  s.subsystem === 'UI' ||          // Same subsystem
  s.provides.some(p => needed(p))  // Provides something we need
)
// Returns 3-5 matches
```

**Phase 3: Load full content for matches only:**

```bash
for match in matches; do
  cat "$match"  # Full 2,000 tokens, but only 3-5 files
done
```

## What This Achieves

- **85-90% reduction** in SUMMARY loading for planning
- **Faster planning** - quick scan identifies relevance
- **Focused context** - only load what's actually needed
- **Scales better** - as project grows, scan stays fast

## Token Impact

**Early project (10 summaries):**
- Current: 10 × 2,000 = 20,000 tokens
- Optimized: 10 × 300 (scan) + 3 × 2,000 (full) = 9,000 tokens
- Savings: 11,000 tokens

**Late project (40 summaries):**
- Current: 40 × 2,000 = 80,000 tokens
- Optimized: 40 × 300 (scan) + 4 × 2,000 (full) = 20,000 tokens
- **Savings: 60,000 tokens**

**Per planning phase: 12-60k tokens saved** (increases with project size)

## Implementation Requirements

1. Ensure all SUMMARY frontmatter is in first 30 lines
2. Implement frontmatter-only scan utility
3. Define relevance matching criteria
4. Update planner to scan first, load selectively
5. Test planning quality with selective loading
6. Add fallback to load all if relevance unclear

## Affected Files

**Update planner:**
- `agents/gsd-planner.md` - Implement scan → match → load pattern

**Update templates:**
- `get-shit-done/templates/summary.md` - Ensure frontmatter is compact and first

**New utilities:**
- Frontmatter scanner
- Relevance matcher

## Success Criteria

- [ ] Frontmatter scanner implemented
- [ ] Relevance matching criteria defined
- [ ] Planner scans before loading
- [ ] Only relevant summaries loaded fully
- [ ] Planning quality maintained
- [ ] Token usage reduced by target amount
- [ ] Scales well with project size

## Dependencies

Works extremely well with:
- C2 (dependency graph cache) - frontmatter provides graph data
- B2 (frontmatter compression) - smaller frontmatter = faster scans

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
