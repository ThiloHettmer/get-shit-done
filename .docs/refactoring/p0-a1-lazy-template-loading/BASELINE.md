# Baseline Token Measurements - p0-a1-lazy-template-loading

**Date:** 2026-01-26
**Branch:** refactor-token-usage

## Template File Sizes (Pre-Optimization)

Below are line counts for all template files. Token count is approximately 4-5 tokens per line for markdown.

### All Templates (by size, largest first)

```
567 lines - phase-prompt.md
529 lines - research.md
322 lines - verification-report.md
311 lines - user-setup.md
283 lines - context.md
247 lines - UAT.md
246 lines - summary.md
231 lines - requirements.md
202 lines - roadmap.md
184 lines - project.md
182 lines - planner-subagent-prompt.md
149 lines - discovery.md
144 lines - debug-subagent-prompt.md
136 lines - state.md
122 lines - milestone.md
98 lines - continue-here.md
77 lines - milestone-archive.md
77 lines - DEBUG.md
```

**Total:** ~4,100 lines across 18 templates
**Average:** ~228 lines per template

## Estimated Token Usage (Current)

**Per template load:**
- Small templates (50-100 lines): ~250-500 tokens
- Medium templates (100-200 lines): ~500-1,000 tokens
- Large templates (200-250 lines): ~1,000-2,500 tokens

**Average template:** ~2,000 tokens

**Per phase (5-6 template loads):** 10,000-12,000 tokens

## Target After Optimization

**Section-based loading:**
- Average section: 30-50 lines = ~150-400 tokens
- Per template load (2-3 sections): ~700-900 tokens

**Expected savings:** 60-70% per template load

**Per phase savings:** 6,000-8,000 tokens (matches SUMMARY.md estimate of 8-12k)

## Measurement Notes

- Token counts are approximate (vary by tokenizer)
- Actual savings depend on which sections agents need
- Some templates may have higher/lower section reuse
