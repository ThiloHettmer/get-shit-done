# Token Reduction Refactoring Tasks

This directory contains the breakdown of all token optimization tasks for the Get Shit Done framework. Each subdirectory represents a distinct optimization that will be further broken down into implementation tasks.

## Overview

Based on the analysis in `..token-reduction-analysis.md`, we have identified **20 major optimization tasks** organized by priority and implementation phase.

**Total estimated savings: 40-60% token reduction**

---

## Priority P0: Quick Wins (3-4 weeks)

These tasks provide high impact with low risk and should be implemented first.

| Task | Category | Token Savings | Complexity | Risk |
|------|----------|---------------|------------|------|
| [p0-a1-lazy-template-loading](./p0-a1-lazy-template-loading/) | Selective Loading | 8-12k/phase | Medium | Low |
| [p0-a2-context-aware-references](./p0-a2-context-aware-references/) | Selective Loading | 5-8k/executor | Low | Low |
| [p0-d1-unified-agent-base](./p0-d1-unified-agent-base/) | Structural | 22-33k initial + 2-3k/spawn | Medium | Low |

**Phase 1 P0 Total: ~100-150k tokens per project**

---

## Priority P1: Medium Priority (4-6 weeks)

These tasks provide good impact with reasonable implementation effort.

| Task | Category | Token Savings | Complexity | Risk |
|------|----------|---------------|------------|------|
| [p1-a3-incremental-state-loading](./p1-a3-incremental-state-loading/) | Selective Loading | 1.5-3k/phase | Low | Low |
| [p1-b1-abbreviated-xml-tags](./p1-b1-abbreviated-xml-tags/) | Compressed Formats | 8-12k/phase | Low | Medium |
| [p1-e1-batch-agent-communication](./p1-e1-batch-agent-communication/) | Execution Patterns | 15-40k/phase | High | Medium |
| [p1-c2-dependency-graph-cache](./p1-c2-dependency-graph-cache/) | Caching | 8-12k/planning | Medium | Low |
| [p1-d2-consolidated-references](./p1-d2-consolidated-references/) | Structural | 4-6k/phase | Low | Low |

**Phase 1 P1 Total: ~50-100k tokens per project**

---

## Priority P2: Lower Priority (6-10 weeks)

These tasks provide moderate impact or require more complex implementation.

| Task | Category | Token Savings | Complexity | Risk |
|------|----------|---------------|------------|------|
| [p2-g3-lazy-agent-loading](./p2-g3-lazy-agent-loading/) | Agent Architecture | 24-40k/phase | High | Medium |
| [p2-b2-frontmatter-compression](./p2-b2-frontmatter-compression/) | Compressed Formats | 4.5-6k/project | Low | Medium |
| [p2-a4-pruned-roadmap-context](./p2-a4-pruned-roadmap-context/) | Selective Loading | 3-6k/phase | Low | Low |
| [p2-d3-hierarchical-templates](./p2-d3-hierarchical-templates/) | Structural | 6-9k/phase | Medium | Low |
| [p2-e2-summary-streaming](./p2-e2-summary-streaming/) | Execution Patterns | 16k/verification | Medium | Low |
| [p2-c3-codebase-map-selective](./p2-c3-codebase-map-selective/) | Caching | 8-12k/planning | Medium | Low |

**Phase 2 Total: ~80-120k tokens per project**

---

## Priority P3: Nice-to-Have (10-18 weeks)

These tasks provide smaller gains or have higher complexity/risk. Implement only if earlier optimizations don't meet targets.

| Task | Category | Token Savings | Complexity | Risk |
|------|----------|---------------|------------|------|
| [p3-f2-abbreviated-must-haves](./p3-f2-abbreviated-must-haves/) | Metadata | 9-12k/project | Medium | Medium |
| [p3-b3-compact-agent-prompts](./p3-b3-compact-agent-prompts/) | Compressed Formats | 33-44k initial | Medium | Medium |
| [p3-e3-progressive-detail-loading](./p3-e3-progressive-detail-loading/) | Execution Patterns | 1-1.5k/plan | High | Medium |
| [p3-g1-shared-context-pool](./p3-g1-shared-context-pool/) | Agent Architecture | 3.2-4.8k/phase | High | Medium |
| [p3-g2-workflow-templating](./p3-g2-workflow-templating/) | Agent Architecture | 8-12k/phase | High | High |
| [p3-a5-summary-frontmatter-scanning](./p3-a5-summary-frontmatter-scanning/) | Selective Loading | 12-20k/planning | Low | Low |

**Phase 3 Total: ~60-100k tokens per project**

---

## Implementation Strategy

### Phase 1: Foundation (Weeks 1-6)
**Target: 25-30% reduction**

1. Implement P0 tasks first (highest ROI, lowest risk)
2. Build infrastructure for selective loading
3. Establish testing framework for token measurement
4. Create migration tooling

**Deliverables:**
- Lazy template loading working
- Context-aware reference loading
- Unified agent base
- Token measurement dashboard

### Phase 2: Optimization (Weeks 7-14)
**Target: Additional 15-20% reduction**

1. Implement P1 tasks
2. Begin P2 tasks (lazy agent loading, hierarchical templates)
3. Format optimizations (XML tags, frontmatter)
4. Advanced caching mechanisms

**Deliverables:**
- Batch agent communication
- Dependency graph cache
- Consolidated references
- Format compression

### Phase 3: Advanced (Weeks 15-22)
**Target: Additional 5-10% reduction**

1. Implement remaining P2 tasks
2. Selectively implement P3 tasks based on needs
3. Polish and optimization
4. Documentation updates

**Deliverables:**
- Lazy agent loading
- Progressive detail loading (if needed)
- Complete documentation
- Migration guides

---

## Dependencies & Conflicts

### Complementary Tasks (Implement Together)
- **A1 + D3:** Lazy template loading + Hierarchical templates
- **D1 + B3:** Unified agent base + Compact agent prompts
- **D2 + G3:** Consolidated references + Lazy agent loading
- **C2 + A5:** Dependency graph cache + Summary frontmatter scanning
- **A3 + C2:** Incremental state + Dependency graph (both modify STATE.md)

### Conflicting Tasks (Choose One)
- **E1 vs G1:** Batch agent communication vs Shared context pool (different context-passing strategies)
- **E3 vs E1:** Progressive detail loading vs Batch communication (incompatible approaches)

### Sequential Dependencies
- **A1 before D3:** Need section loading before hierarchical templates
- **D1 before B3:** Unified base before compacting agents
- **D2 before G3:** Consolidated references before lazy loading protocols

---

## Task Status Tracking

| Priority | Total Tasks | Not Started | In Progress | Complete | % Complete |
|----------|-------------|-------------|-------------|----------|------------|
| P0 | 3 | 3 | 0 | 0 | 0% |
| P1 | 5 | 5 | 0 | 0 | 0% |
| P2 | 6 | 6 | 0 | 0 | 0% |
| P3 | 6 | 6 | 0 | 0 | 0% |
| **Total** | **20** | **20** | **0** | **0** | **0%** |

---

## Next Steps

1. **Review this breakdown** with project maintainers
2. **Prioritize P0 tasks** for immediate implementation
3. **Set up token measurement** infrastructure
4. **Create detailed implementation plans** for each P0 task
5. **Begin implementation** with p0-a1-lazy-template-loading

Each task directory contains a `SUMMARY.md` with:
- Detailed overview
- Current vs proposed behavior
- Token impact analysis
- Implementation requirements
- Affected files
- Success criteria
- Dependencies

Task directories will be further broken down into granular implementation tasks as work progresses.

---

## Token Savings Summary

### Conservative Estimate (40% reduction)
- **Current per project:** 1.7M-2.6M tokens
- **After optimizations:** 1.0M-1.6M tokens
- **Savings:** 0.7M-1.0M tokens per project

### Optimistic Estimate (50% reduction)
- **After optimizations:** 0.85M-1.3M tokens
- **Savings:** 0.85M-1.3M tokens per project

### Real-World Impact (Based on 35M token project)
- **Current:** 35M tokens
- **After P0+P1:** ~24.5M tokens (30% reduction)
- **After P0+P1+P2:** ~18.9M tokens (46% reduction)
- **After all optimizations:** ~16.5M tokens (53% reduction)

**Cost savings (at $0.27/1M tokens):**
- Current: $9.45 per project
- After all: $4.46 per project
- **Savings: $5 per project (53%)**

---

## Questions & Discussion

For questions about specific tasks or the overall strategy, refer to:
- `../token-reduction-analysis.md` - Comprehensive analysis
- Individual task `SUMMARY.md` files - Task-specific details
- Project maintainers - Strategic decisions

**Status:** Planning phase complete, ready for P0 implementation
