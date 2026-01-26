# Lazy Template Loading

**Priority:** P0 (Quick Win)  
**Category:** A - Selective Context Loading  
**Estimated Token Savings:** 8-12k per phase  
**Implementation Complexity:** Medium  
**Risk Level:** Low

## Overview

Currently, every agent loads complete template files unconditionally (e.g., `summary.md` at 2,500 tokens). This task implements section-based template loading where agents only load the specific sections they need.

## Current Behavior

```markdown
<!-- Agent loads entire template -->
@templates/summary.md (2,500 tokens)
```

Every agent spawn that needs template guidance loads the full file, even though they may only need 20-30% of the content.

## Proposed Behavior

```markdown
<!-- Agent loads only needed sections -->
@templates/summary.md#frontmatter (400 tokens)
@templates/summary.md#task-commits (300 tokens)
```

## What This Achieves

- **Reduces per-agent token load** by 60-70% for template content
- **No behavior change** - agents still get the guidance they need
- **Maintains readability** - full templates remain intact for human reference
- **Easy to implement** - additive change, doesn't break existing functionality

## Token Impact

- Current: 2,500 tokens per template load × 5-6 loads per phase = 12.5-15k tokens
- Optimized: 700-900 tokens per template load × 5-6 loads = 4.2-5.4k tokens
- **Savings: 8-10k tokens per phase**

## Implementation Requirements

1. Add section anchors to all template files (e.g., `## frontmatter`, `## task-commits`)
2. Implement section parser that extracts content between anchors
3. Update agent prompts to request specific sections instead of full templates
4. Add fallback to load full template if section not found (backwards compatibility)

## Affected Files

- `get-shit-done/templates/*.md` (all 18 templates)
- Agent prompts that load templates (gsd-executor, gsd-planner, gsd-verifier)
- Workflow files that reference templates

## Success Criteria

- [ ] All templates have clearly marked sections with anchors
- [ ] Section loading mechanism implemented and tested
- [ ] Agents load only required sections
- [ ] No regression in agent output quality
- [ ] Token usage reduced by target amount

## Dependencies

None - can be implemented independently

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
