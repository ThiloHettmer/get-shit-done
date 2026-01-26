# Section Naming Conventions

## Overview

All templates now use consistent section anchor names for selective loading. Section anchors follow the **lowercase-hyphen** format.

## Naming Rules

1. **All lowercase** - No uppercase letters
2. **Hyphens for spaces** - Replace spaces with hyphens
3. **Remove special characters** - Remove parentheses, slashes, colons
4. **No abbreviations** - Use full words (e.g., `performance` not `perf`)
5. **Descriptive** - Name should clearly indicate section content

## Examples

| Original Heading | Section Anchor |
|-----------------|----------------|
| `## File Template` | `## file-template` |
| `## Goal Achievement` | `## goal-achievement` |
| `## State of the Art (2024-2025)` | `## state-of-the-art` |
| `## Don't Hand-Roll` | `## dont-hand-roll` |
| `## Files Created/Modified` | `## files-created-modified` |

## Common Section Names

### Template Structure
- `file-template` - The actual template content to use
- `frontmatter-guidance` / `frontmatter-schema` / `frontmatter-fields` - Frontmatter documentation
- `guidelines` - General usage guidelines
- `example` / `examples` / `good-example` - Example usage
- `usage` / `usage-guidelines` - How to use the template

### Content Sections
- `overview` - High-level description
- `summary` - Summary information
- `context` - Contextual information
- `requirements` - Requirements documentation
- `phases` / `phase-details` - Phase information
- `tasks` / `task-commits` - Task-related content
- `verification` - Verification criteria
- `performance` / `performance-metrics` - Performance data

### Guidance Sections
- `anti-patterns` / `anti-patterns-found` - What not to do
- `common-pitfalls` - Common mistakes
- `dont-hand-roll` - Pre-built solutions to use
- `automation-first-rule` - Automation guidance

### Project-Specific
- `goal-achievement` - Goal verification
- `requirements-coverage` - Requirements mapping
- `gaps` / `gaps-summary` - Identified gaps
- `decisions-made` / `key-decisions` - Decision documentation
- `deviations-from-plan` - Deviations tracking

## Usage in References

To reference a specific section from an agent or workflow file:

```markdown
@~/.claude/get-shit-done/templates/summary.md#frontmatter-guidance
@~/.claude/get-shit-done/templates/phase-prompt.md#file-template
@~/.claude/get-shit-done/templates/verification-report.md#goal-achievement
```

## Backwards Compatibility

Templates can still be referenced without section anchors:

```markdown
@~/.claude/get-shit-done/templates/summary.md
```

This will load the full template file as before.

## Implementation Notes

- Section anchors are standard Markdown heading IDs
- GitHub/Markdown parsers auto-generate these anchors from headings
- No special tooling required - works natively with Markdown
- Cursor/Claude can reference sections using the `#section-name` syntax

## Benefits

1. **Token Reduction** - Load only needed sections (60-70% savings)
2. **Clarity** - Clear what content is being loaded
3. **Maintainability** - Easy to find and reference specific guidance
4. **Backwards Compatible** - Old references still work

## Validation

All templates have been validated to ensure:
- ✅ All section headings use lowercase-hyphen format
- ✅ No duplicate section names within a file
- ✅ Section names are descriptive and consistent
- ✅ Common sections use standard names across templates
