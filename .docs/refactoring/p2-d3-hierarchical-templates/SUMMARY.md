# Hierarchical Template Structure

**Priority:** P2  
**Category:** D - Structural Refactoring  
**Estimated Token Savings:** 6-9k per phase  
**Implementation Complexity:** Medium  
**Risk Level:** Low

## Overview

Templates are flat files with all sections included. This task breaks templates into nested components with master files that include sub-templates, allowing selective loading.

## Current Structure

```markdown
# templates/summary.md (2,500 tokens)
## Frontmatter guidelines (500 tokens)
## Performance section (300 tokens)
## Accomplishments section (200 tokens)
## Task commits format (400 tokens)
## Files created format (200 tokens)
## Decisions format (300 tokens)
## Deviations format (600 tokens)
[... all sections loaded every time ...]
```

Agent needs only 2-3 sections but loads entire template.

## Proposed Structure

```markdown
# templates/summary.md (master - 200 tokens)
SUMMARY.md template for plan completion documentation.

Sections available:
@templates/summary/frontmatter.md
@templates/summary/performance.md
@templates/summary/commits.md
@templates/summary/deviations.md

Load what you need based on execution context.

# templates/summary/frontmatter.md (500 tokens)
[Frontmatter guidelines only]

# templates/summary/commits.md (400 tokens)
[Task commit format only]

# templates/summary/deviations.md (600 tokens)
[Deviation documentation format]
```

**Agent loads selectively:**
```markdown
@templates/summary.md#overview        (50 tokens - just structure)
@templates/summary/frontmatter.md     (500 tokens - always needed)
@templates/summary/commits.md         (400 tokens - always needed)
# Skip deviations unless deviations occurred
```

## What This Achieves

- **Modular template loading** - take only what's needed
- **Easier maintenance** - edit sections independently
- **Clearer structure** - each file has one concern
- **Reusable components** - share common sections

## Token Impact

**Typical SUMMARY creation:**
- Current: Load full template (2,500 tokens)
- Optimized: Load 3-4 sections (950-1,350 tokens)
- **Savings: 1,150-1,550 tokens per load**

**Per phase (3-5 plan executions):**
- **Savings: 3.5-7.8k tokens**

**Similar savings for PLAN.md template:**
- Current: ~5,000 tokens (large template)
- Optimized: ~2,000 tokens (selective sections)
- **Additional 9k per planning phase**

## Implementation Requirements

1. Analyze all templates and identify logical sections
2. Create subdirectories for each template (e.g., `templates/summary/`, `templates/plan/`)
3. Split templates into component files
4. Create master template with section index
5. Update agent prompts to load specific sections
6. Update workflow instructions for template usage
7. Test each template type with selective loading

## Affected Files

**Restructure templates:**
```
templates/
├── summary/
│   ├── frontmatter.md
│   ├── performance.md
│   ├── commits.md
│   ├── deviations.md
│   └── files.md
├── plan/
│   ├── frontmatter.md
│   ├── objective.md
│   ├── tasks.md
│   └── verification.md
├── summary.md (master index)
└── phase-prompt.md (master index)
```

**Update agents:**
- `agents/gsd-executor.md` - Load summary sections selectively
- `agents/gsd-planner.md` - Load plan sections selectively

**Update workflows:**
- `get-shit-done/workflows/execute-plan.md` - Reference new structure

## Success Criteria

- [ ] All templates split into logical sections
- [ ] Master template files serve as indexes
- [ ] Agents load only needed sections
- [ ] No regression in output quality
- [ ] Token usage reduced by target amount
- [ ] Easier to maintain templates

## Dependencies

Works extremely well with A1 (lazy template loading) - both enable selective loading

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
