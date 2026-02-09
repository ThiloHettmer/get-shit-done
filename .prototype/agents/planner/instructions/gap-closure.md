## Planning from Verification Gaps

Triggered when mode is GAP_CLOSURE. Creates plans to address verification or UAT failures.

**Process:**

1. Parse gaps from verification_content or uat_content
2. Each gap has: truth (failed behavior), reason, artifacts (files with issues), missing (things to add/fix)
3. Load existing summaries to understand what's already built
4. Find next plan number (if plans 01-03 exist, next is 04)
5. Group gaps into plans by: same artifact, same concern, dependency order

**Gap closure task format:**

```xml
<task name="{fix_description}" type="auto">
  <files>{artifact.path}</files>
  <action>
    {For each item in gap.missing:}
    - {missing item}

    Reference existing code: {from summaries}
    Gap reason: {gap.reason}
  </action>
  <verify>{How to confirm gap is closed}</verify>
  <done>{Observable truth now achievable}</done>
</task>
```

Plans should have `gap_closure: true` in frontmatter.
