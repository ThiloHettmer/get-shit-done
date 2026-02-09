## Planning from Checker Feedback

Triggered when mode is REVISION. NOT starting fresh — making targeted updates to existing plans.

**Mindset:** Surgeon, not architect. Minimal changes for specific issues.

### Revision Strategy by Dimension

| Dimension              | Strategy                                 |
| ---------------------- | ---------------------------------------- |
| requirement_coverage   | Add task(s) for missing requirement      |
| task_completeness      | Add missing elements to existing task    |
| dependency_correctness | Fix depends_on, recompute waves          |
| key_links_planned      | Add wiring task or update action         |
| scope_sanity           | Split into multiple plans                |
| must_haves_derivation  | Derive and add must_haves to frontmatter |

### Making Updates

**DO:** Edit specific flagged sections, preserve working parts, update waves if dependencies change.

**DO NOT:** Rewrite entire plans for minor issues, add unnecessary tasks, break existing working plans.

### Validation After Revision

- [ ] All flagged issues addressed
- [ ] No new issues introduced
- [ ] Wave numbers still valid
- [ ] Dependencies still correct
