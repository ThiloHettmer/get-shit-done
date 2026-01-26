# Summary Streaming

**Priority:** P2  
**Category:** E - Execution Pattern Changes  
**Estimated Token Savings:** 16k per verification phase  
**Implementation Complexity:** Medium  
**Risk Level:** Low

## Overview

Verifier agents load complete SUMMARY.md files (2,000-2,500 tokens each) to check deliverables. This task implements section-based loading where only accomplishments and files sections are loaded for verification.

## Current Behavior

**Verifier workflow:**
1. Load 8-10 SUMMARY.md files from phase (full files)
2. Extract accomplishments to verify
3. Extract files to check existence
4. Ignore performance metrics, deviation details, session notes

**Token load:**
- 10 summaries × 2,000 tokens = 20,000 tokens
- Actually uses: ~20% of content (4,000 tokens)
- **Waste: 16,000 tokens**

## Proposed Behavior

**Load via section streaming:**
```markdown
# Instead of full SUMMARY
@.planning/phases/01-foundation/01-02-SUMMARY.md#accomplishments
@.planning/phases/01-foundation/01-02-SUMMARY.md#files-created

# Gets only:
## Accomplishments
- JWT authentication working
- User registration endpoint complete

## Files Created/Modified
- src/app/api/auth/register/route.ts
- src/app/api/auth/login/route.ts
```

**Token load:**
- 10 summaries × 400 tokens (2 sections) = 4,000 tokens
- **Savings: 16,000 tokens per verification**

## What This Achieves

- **80% reduction** in summary loading for verification
- **Faster verification** - less content to process
- **Focused checks** - only relevant sections visible
- **No behavior change** - same verification performed

## Token Impact

**Per verification phase:**
- Current: 20k tokens (full summaries)
- Optimized: 4k tokens (relevant sections)
- **Savings: 16k tokens**

**Per complete project (3-5 verifications):**
- **Savings: 48-80k tokens**

## Implementation Requirements

1. Ensure all SUMMARY files have consistent section headers
2. Implement section extraction for SUMMARY files
3. Update verifier agent to request specific sections
4. Update verification workflow to pass section references
5. Test verification accuracy with partial summaries
6. Add fallback to load full summary if sections missing

## Affected Files

**Update verifier:**
- `agents/gsd-verifier.md` - Request only accomplishments + files sections

**Update verification workflow:**
- `get-shit-done/workflows/verify-phase.md` - Pass section references
- `get-shit-done/workflows/verify-work.md` - Similar updates

**Ensure templates have sections:**
- `get-shit-done/templates/summary.md` - Verify section headers

## Success Criteria

- [ ] Section-based SUMMARY loading implemented
- [ ] Verifier loads only accomplishments + files sections
- [ ] Verification accuracy maintained
- [ ] Token usage reduced by target amount
- [ ] Fallback works for older summaries without sections

## Dependencies

Works well with:
- A1 (lazy template loading) - same section-loading mechanism
- D3 (hierarchical templates) - summaries already have sections

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
