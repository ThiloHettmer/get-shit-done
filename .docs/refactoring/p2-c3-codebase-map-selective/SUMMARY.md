# Codebase Map Selective Loading

**Priority:** P2  
**Category:** C - Intelligent Caching  
**Estimated Token Savings:** 8-12k per planning phase  
**Implementation Complexity:** Medium  
**Risk Level:** Low

## Overview

Currently, planners load all 7 codebase analysis files (12-18k tokens total) regardless of phase type. This task implements keyword-based selective loading of only relevant codebase context.

## Current Behavior

**Planner loads all codebase files:**
```bash
cat .planning/codebase/STACK.md           # 1,500-2,500 tokens
cat .planning/codebase/ARCHITECTURE.md    # 2,000-3,000 tokens
cat .planning/codebase/CONVENTIONS.md     # 1,500-2,500 tokens
cat .planning/codebase/STRUCTURE.md       # 1,500-2,500 tokens
cat .planning/codebase/INTEGRATIONS.md    # 1,500-2,500 tokens
cat .planning/codebase/CONCERNS.md        # 1,000-2,000 tokens
cat .planning/codebase/TESTING.md         # 1,500-2,500 tokens
```

**Total: 12,000-18,000 tokens**

Most phases only need 2-3 of these files based on what they're building.

## Proposed Behavior

**Keyword-based selective loading:**

```javascript
// Phase: "Build user authentication API"
keywords = ["API", "auth", "endpoint", "backend"]

if (matches(keywords, ["API", "endpoint", "backend"])) {
  load('ARCHITECTURE.md')  // API patterns
  load('CONVENTIONS.md')    // Code conventions
  load('STACK.md')          // Tech stack
  // Skip: STRUCTURE, INTEGRATIONS, CONCERNS, TESTING
}

// Phase: "Build dashboard UI components"
keywords = ["UI", "dashboard", "components", "frontend"]

if (matches(keywords, ["UI", "frontend", "components"])) {
  load('CONVENTIONS.md')    // Code conventions
  load('STRUCTURE.md')      // Component structure
  load('STACK.md')          // Frontend tech
  // Skip: ARCHITECTURE, INTEGRATIONS, CONCERNS, TESTING
}
```

**Mapping rules:**

| Phase Keywords | Load These Files |
|----------------|-----------------|
| API, backend, endpoints | ARCHITECTURE, CONVENTIONS, STACK |
| UI, frontend, components | CONVENTIONS, STRUCTURE, STACK |
| database, schema, models | ARCHITECTURE, STACK, CONVENTIONS |
| testing, tests | TESTING, CONVENTIONS |
| integration, external API | INTEGRATIONS, STACK, ARCHITECTURE |
| refactor, cleanup | CONCERNS, ARCHITECTURE, CONVENTIONS |
| setup, config | STACK, STRUCTURE |
| (default) | STACK, ARCHITECTURE |

## What This Achieves

- **60-70% reduction** in codebase context loading
- **More focused planning** - relevant patterns only
- **Faster planning** - less content to process
- **Scales better** - as codebase analysis grows

## Token Impact

**Typical phase:**
- Current: 12-18k tokens (all 7 files)
- Optimized: 4-6k tokens (2-3 relevant files)
- **Savings: 8-12k tokens per planning phase**

**Per project (5 planning phases):**
- **Savings: 40-60k tokens**

## Implementation Requirements

1. Define keyword → file mapping rules
2. Implement keyword extraction from phase goals
3. Update planner to load selectively based on keywords
4. Create index file listing which files cover which topics
5. Add fallback to load all if keywords don't match
6. Test planning quality with selective loading

## Affected Files

**Create:**
- `.planning/codebase/INDEX.md` - Maps topics to files

**Update:**
- `agents/gsd-planner.md` - Add selective loading logic
- `get-shit-done/workflows/map-codebase.md` - Generate INDEX.md
- `agents/gsd-codebase-mapper.md` - Include indexing step

## Success Criteria

- [ ] Keyword mapping rules defined and documented
- [ ] INDEX.md generated during codebase mapping
- [ ] Planner loads only relevant codebase files
- [ ] Planning quality maintained
- [ ] Token usage reduced by target amount
- [ ] Fallback works when keywords unclear

## Dependencies

None - can be implemented independently

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
