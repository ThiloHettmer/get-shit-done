# Frontmatter Compression

**Priority:** P2  
**Category:** B - Compressed Formats  
**Estimated Token Savings:** 4.5-6k per project  
**Implementation Complexity:** Low  
**Risk Level:** Medium (file format change)

## Overview

PLAN.md and SUMMARY.md frontmatter uses verbose YAML with long key names and repeated structures. This task compresses frontmatter using abbreviated keys and compact syntax.

## Current Format

```yaml
---
phase: 01-foundation
plan: 02
type: execute
wave: 2
depends_on: ["01-01"]
files_modified: 
  - "src/app/api/auth/register/route.ts"
  - "src/app/api/auth/login/route.ts"
autonomous: true
gap_closure: false

must_haves:
  truths:
    - "User can register with email"
    - "User can log in"
  artifacts:
    - path: "src/app/api/auth/register/route.ts"
      provides: "Registration endpoint"
      exports: ["POST"]
  key_links:
    - from: "src/components/RegisterForm.tsx"
      to: "/api/auth/register"
---
```

**Token count: ~350 tokens**

## Proposed Format

```yaml
---
p: 01-foundation | pl: 02 | t: exec | w: 2
deps: [01-01] | auto: y | gap: n
files: [src/app/api/auth/*.ts]
must: {
  truth: [register-email, login-jwt],
  files: [api/auth/register→POST, api/auth/login→POST],
  links: [RegisterForm→/api/auth/register]
}
---
```

**Token count: ~180 tokens**
**Savings: 170 tokens per file**

## Key Abbreviations

```
phase → p
plan → pl
type → t
wave → w
depends_on → deps
files_modified → files
autonomous → auto
gap_closure → gap
must_haves → must
truths → truth
artifacts → files
key_links → links
```

## What This Achieves

- **50% frontmatter reduction** while maintaining structure
- **Human readable** - still parseable by humans
- **Machine friendly** - easier to parse programmatically
- **Consistent format** across all files

## Token Impact

- PLAN.md: 350 → 180 tokens = 170 tokens saved × 30 plans = 5.1k
- SUMMARY.md: Similar savings × 30 summaries = 5.1k
- **Total: ~10k tokens saved per project**
- **Per phase: 1.5-2k tokens** (files loaded multiple times)

## Implementation Requirements

1. Define complete abbreviation mapping
2. Update frontmatter parser to handle both formats (backwards compatibility)
3. Update frontmatter writer to use compressed format
4. Update all templates with compressed frontmatter examples
5. Migration tool for existing projects
6. Update documentation

## Affected Files

**Templates:**
- `get-shit-done/templates/phase-prompt.md` - Update PLAN frontmatter
- `get-shit-done/templates/summary.md` - Update SUMMARY frontmatter

**Agents that write frontmatter:**
- `agents/gsd-planner.md` - Writes PLAN frontmatter
- `agents/gsd-executor.md` - Writes SUMMARY frontmatter

**Agents that read frontmatter:**
- `agents/gsd-planner.md` - Reads prior summaries
- `agents/gsd-executor.md` - Reads plan frontmatter
- `agents/gsd-verifier.md` - Reads plans and summaries
- `get-shit-done/workflows/execute-phase.md` - Reads wave numbers

**Documentation:**
- `.docs/xml-format.md` - Update frontmatter examples

## Success Criteria

- [ ] Abbreviation mapping fully defined
- [ ] Parser handles both old and new formats
- [ ] Writer outputs compressed format
- [ ] All agents work with compressed format
- [ ] Human readability maintained
- [ ] Token usage reduced by target amount
- [ ] Migration guide for existing projects

## Dependencies

Consider doing after other optimizations to minimize churn on file format

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
