# Consolidated References

**Priority:** P1  
**Category:** D - Structural Refactoring  
**Estimated Token Savings:** 4-6k per phase  
**Implementation Complexity:** Low  
**Risk Level:** Low

## Overview

The 9 reference files have overlapping content and redundant section headers/examples. This task merges related references and modularizes them for selective loading.

## Current Structure

```
references/
├── checkpoints.md           (~3,000 tokens)
├── continuation-format.md   (~2,000 tokens)
├── git-integration.md       (~3,000 tokens)
├── model-profiles.md        (~2,000 tokens)
├── planning-config.md       (~1,500 tokens)
├── questioning.md           (~1,500 tokens)
├── tdd.md                   (~3,000 tokens)
├── ui-brand.md             (~1,500 tokens)
└── verification-patterns.md (~2,500 tokens)
```

**Issues:**
- Checkpoint + continuation patterns overlap (checkpoint resumption)
- Git integration appears in multiple references
- Examples repeated across files
- Section headers and formatting add ~20% overhead

## Proposed Structure

```
references/
├── execution.md              (~6,000 tokens)
│   ├── #checkpoints
│   ├── #continuation
│   ├── #git-protocol
│   └── #deviation-handling
├── planning.md               (~4,000 tokens)
│   ├── #tdd
│   ├── #verification
│   └── #config-schema
├── interaction.md            (~3,000 tokens)
│   ├── #questioning
│   ├── #ui-brand
│   └── #model-profiles
```

**Load selectively:**
```markdown
@references/execution.md#checkpoints    (when needed)
@references/execution.md#git-protocol   (always)
@references/planning.md#tdd             (for TDD plans only)
```

## What This Achieves

- **Eliminates redundant content** across references
- **Modular loading** - load only needed sections
- **Easier maintenance** - related patterns in one file
- **Reduced overhead** - fewer file headers and repeated examples

## Token Impact

- Current: 9 files × ~2,000 tokens average = ~18k total reference content
- Redundancy reduction: ~20% overlap = 3.6k tokens
- Consolidated: 3 files × ~4,300 tokens = ~13k tokens
- **Savings: 5k tokens in reference content**
- **Per phase: 4-6k savings** (references loaded 2-3 times)

## Implementation Requirements

1. Analyze overlap across current references
2. Design consolidated file structure with sections
3. Merge content into consolidated files
4. Add section anchors for selective loading
5. Update all references to new file paths
6. Delete old reference files
7. Update documentation

## Affected Files

**Create:**
- `get-shit-done/references/execution.md` (new consolidated)
- `get-shit-done/references/planning.md` (new consolidated)
- `get-shit-done/references/interaction.md` (new consolidated)

**Delete:**
- `get-shit-done/references/checkpoints.md`
- `get-shit-done/references/continuation-format.md`
- `get-shit-done/references/git-integration.md`
- `get-shit-done/references/questioning.md`
- `get-shit-done/references/tdd.md`
- `get-shit-done/references/ui-brand.md`
- `get-shit-done/references/verification-patterns.md`

**Update references in:**
- All agent files (11 files)
- All workflow files (12 files)
- All templates that reference these (18 files)

## Success Criteria

- [ ] Consolidated references created with clear sections
- [ ] All content preserved (no information loss)
- [ ] Redundancy eliminated
- [ ] All references updated to new paths
- [ ] Old files deleted
- [ ] Token usage reduced by target amount
- [ ] Documentation updated

## Dependencies

Works well with A1 (lazy template loading) - both use section-based loading

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
