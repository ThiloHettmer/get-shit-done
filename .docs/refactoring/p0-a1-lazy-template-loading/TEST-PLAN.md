# Test Plan - p0-a1-lazy-template-loading

## Objective

Verify that section-based template loading:
1. Reduces token usage by 60-70%
2. Maintains backwards compatibility
3. Doesn't break existing agent functionality

## Test Scenarios

### 1. Section Anchor Validation

**Test:** All templates have properly formatted section anchors

**Method:**
```bash
# Check for section anchors in each template
for file in get-shit-done/templates/*.md; do
  echo "Checking $(basename $file)..."
  grep "^## " "$file" | head -5
done
```

**Success criteria:**
- Each template has at least 2-3 section anchors
- Anchors use consistent naming (lowercase, hyphens)
- No duplicate anchor names within a file

### 2. Documentation Validation

**Test:** Section reference syntax is documented

**Method:**
- Check `templates/config.json` has section reference examples
- Verify README or architecture docs mention section loading

**Success criteria:**
- Clear examples of syntax: `@template.md#section-name`
- Explanation of fallback behavior
- List of available sections per template

### 3. Agent Reference Update

**Test:** Agent files use section references where applicable

**Method:**
```bash
# Check agent files for section references
grep -n "@.*templates.*#" agents/*.md
```

**Success criteria:**
- At least 3 agent files updated with section references
- References point to valid sections
- Backwards compatible (old references still work)

### 4. Token Reduction Measurement

**Test:** Measure actual token savings

**Method:**
- Before: Count tokens in full template loads
- After: Count tokens in typical section loads
- Compare against baseline

**Success criteria:**
- Average section load: 700-900 tokens
- Reduction of 60-70% from baseline (2,000-2,500 tokens)
- Total phase savings: 6,000-8,000 tokens

### 5. Backwards Compatibility

**Test:** Full template references still work

**Method:**
- Try loading template without section specifier
- Verify full file loads correctly

**Success criteria:**
- `@template.md` (no section) loads full file
- No errors or warnings
- Existing workflows unaffected

## Validation Checklist

- [ ] All templates have section anchors
- [ ] Section naming is consistent
- [ ] Documentation includes section reference syntax
- [ ] Agent files updated with section references
- [ ] Workflow files updated (if applicable)
- [ ] Token reduction measured and documented
- [ ] Backwards compatibility verified
- [ ] No regressions in agent output quality

## Notes

- Token measurement is approximate (varies by model tokenizer)
- Focus on relative reduction, not absolute numbers
- Prioritize most-used templates (summary.md, phase-prompt.md)
