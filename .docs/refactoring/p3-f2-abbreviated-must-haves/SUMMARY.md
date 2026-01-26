# Abbreviated Must-Haves

**Priority:** P3  
**Category:** F - Metadata Optimization  
**Estimated Token Savings:** 9-12k per project  
**Implementation Complexity:** Medium  
**Risk Level:** Medium (affects verification logic)

## Overview

The `must_haves` frontmatter section in PLAN.md uses verbose goal-backward criteria. This task compresses the format while maintaining semantic meaning for verification.

## Current Format

```yaml
must_haves:
  truths:
    - "User can register with email and password"
    - "User can log in and receive JWT cookie"
    - "Sessions persist across browser restarts"
  artifacts:
    - path: "src/app/api/auth/register/route.ts"
      provides: "Registration endpoint"
      exports: ["POST"]
    - path: "src/app/api/auth/login/route.ts"
      provides: "Login endpoint"
      exports: ["POST"]
  key_links:
    - from: "src/components/RegisterForm.tsx"
      to: "/api/auth/register"
      via: "fetch on form submit"
      pattern: "fetch.*auth/register"
```

**Token count: ~600 tokens**

## Proposed Format

```yaml
must:
  can: [register-email, login-jwt, persist-session]
  has: [
    api/auth/register→POST,
    api/auth/login→POST
  ]
  links: [
    RegisterForm→/api/auth/register:fetch
  ]
```

**Token count: ~280 tokens**
**Savings: 320 tokens per plan**

## Compression Strategy

**Truths → Capabilities (can):**
- "User can register with email" → `register-email`
- "User can log in and receive JWT" → `login-jwt`
- Use kebab-case shorthand for common patterns

**Artifacts → Has:**
- Path + exports → `api/auth/register→POST`
- Drop "provides" description (implied by path name)

**Key Links → Links:**
- From + to + via → `RegisterForm→/api/auth/register:fetch`
- Pattern removed (can be inferred from filenames)

## What This Achieves

- **50% reduction** in must-haves size
- **Maintains verifiability** - all checks still possible
- **Easier to scan** - compact format
- **Less typing** for manual plan creation

## Token Impact

- Per plan: 600 → 280 tokens = 320 tokens saved
- 30 plans per project = **9.6k tokens saved**
- Loaded multiple times during verification = **12-15k total impact**

## Implementation Requirements

1. Define compression rules for truths, artifacts, links
2. Create truth shorthand vocabulary (register-email, login-jwt, etc.)
3. Update planner to output compressed format
4. Update verifier to parse compressed format
5. Update verification logic to work with shortcuts
6. Create expansion utility (for debugging/human reading)
7. Migration tool for existing plans

## Affected Files

**Update planner:**
- `agents/gsd-planner.md` - Output compressed must_haves

**Update verifier:**
- `agents/gsd-verifier.md` - Parse and verify compressed format
- `get-shit-done/workflows/verify-phase.md` - Handle compressed format

**Update templates:**
- `get-shit-done/templates/phase-prompt.md` - Show compressed format

**Documentation:**
- `.docs/xml-format.md` - Document compression format
- `.docs/core-concepts.md` - Update goal-backward examples

## Success Criteria

- [ ] Compression rules fully defined
- [ ] Planner outputs compressed must_haves
- [ ] Verifier correctly parses compressed format
- [ ] Verification accuracy maintained
- [ ] Token usage reduced by target amount
- [ ] Expansion utility available for debugging

## Dependencies

Works with B2 (frontmatter compression) - both compress frontmatter

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
