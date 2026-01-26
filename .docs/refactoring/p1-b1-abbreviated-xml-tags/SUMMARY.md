# Abbreviated XML Tags

**Priority:** P1  
**Category:** B - Compressed Formats  
**Estimated Token Savings:** 8-12k per phase  
**Implementation Complexity:** Low  
**Risk Level:** Medium (affects human readability)

## Overview

XML tags in plans and workflows are semantically clear but verbose. This task shortens common tags while maintaining readability and Claude's comprehension.

## Current Behavior

```xml
<execution_context>...</execution_context>          (19 chars)
<checkpoint:human-verify>...</checkpoint:human-verify>  (50 chars)
<authentication-attempted>...</authentication-attempted>  (52 chars)
<what-built>...</what-built>                        (24 chars)
<how-to-verify>...</how-to-verify>                  (30 chars)
<resume-signal>...</resume-signal>                  (30 chars)
```

Plans contain 50-100 XML tags each, templates and agents even more.

## Proposed Abbreviations

```xml
<exec>...</exec>                    (10 chars, -47%)
<check:verify>...</check:verify>    (26 chars, -48%)
<auth-tried>...</auth-tried>        (24 chars, -54%)
<built>...</built>                  (14 chars, -42%)
<verify>...</verify>                (16 chars, -47%)
<signal>...</signal>                (16 chars, -47%)
```

**Guidelines:**
- Keep semantic meaning clear
- Prioritize frequently-used tags
- Maintain human readability
- Claude handles abbreviations well

## What This Achieves

- **15-20% reduction** in XML token overhead
- **Maintained semantics** - abbreviated but clear
- **No logic changes** - pure format optimization
- **Faster to type** - benefit for manual plan editing

## Token Impact

- Plans: 1,500-4,000 tokens × 30% XML = 450-1,200 tokens
- 40% XML compression = 180-480 tokens saved per plan
- 30 plans per project = **5.4-14.4k tokens saved**

## Implementation Requirements

1. Define abbreviation mapping for all common tags
2. Update XML format reference documentation
3. Update all templates with abbreviated tags
4. Update all agent prompts with new tags
5. Update all workflow files
6. Ensure backwards compatibility (accept both formats during migration)
7. Test Claude's comprehension with abbreviated format

## Affected Files

- `get-shit-done/templates/*.md` (18 files) - Update tag usage
- `agents/*.md` (11 files) - Update tag references
- `get-shit-done/workflows/*.md` (12 files) - Update tag usage
- `.docs/xml-format.md` - Update documentation
- Existing PLAN.md files in projects - Migration needed

## Success Criteria

- [ ] Abbreviation mapping defined and documented
- [ ] All templates use abbreviated tags
- [ ] Agents recognize and work with abbreviated format
- [ ] Human readability maintained
- [ ] Claude comprehension verified
- [ ] Token usage reduced by target amount
- [ ] Migration guide for existing projects

## Dependencies

None - can be implemented independently, but consider doing after other optimizations to minimize churn

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
