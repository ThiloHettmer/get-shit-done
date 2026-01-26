# Unified Agent Base Prompt

**Priority:** P0 (Quick Win)  
**Category:** D - Structural Refactoring  
**Estimated Token Savings:** 22-33k initial + 2-3k per agent spawn  
**Implementation Complexity:** Medium  
**Risk Level:** Low

## Overview

Currently, each of the 11 agents has redundant sections (philosophy, success criteria, git protocols, deviation rules). This task extracts common content into a shared base prompt that all agents reference.

## Current Behavior

Each agent contains:
- Role description (200-300 tokens)
- Philosophy section (500-1,000 tokens) - **80% overlap across agents**
- Core principles (300-500 tokens) - **90% identical**
- Git commit protocol (400-600 tokens) - **100% duplicated in 3 agents**
- Success criteria patterns (200-400 tokens) - **70% similar**

**Example duplication:**
- gsd-executor: 7,800 tokens
- gsd-planner: 8,200 tokens
- gsd-verifier: 4,500 tokens

Common content across all: ~1,200 tokens per agent

## Proposed Structure

```markdown
# agents/base-agent.md (1,200 tokens - loaded once per session)
<role>GSD agent operating in structured multi-agent workflow</role>
<core_principles>
- Plans are prompts (no transformation)
- Context engineering (stay under 50% usage)
- Atomic commits (one task = one commit)
- Goal-backward verification
- Solo developer workflow
</core_principles>
<git_protocol>
[Standard commit format, staging rules, etc.]
</git_protocol>

# agents/gsd-executor.md (now 3,500 tokens vs 7,800)
@agents/base-agent.md
<specific_role>Execute PLAN.md files with atomic commits</specific_role>
<execution_flow>[executor-specific steps]</execution_flow>
<deviation_rules>[executor-specific rules]</deviation_rules>
```

## What This Achieves

- **Eliminates redundancy** across 11 agent definitions
- **Easier maintenance** - update common patterns in one place
- **Consistent behavior** - all agents follow same core principles
- **Significant token savings** - both initial and per-spawn

## Token Impact

**Initial savings:**
- 11 agents × 1,200 tokens common content = 13,200 tokens duplicated
- Replace with 1 base agent = 1,200 tokens
- **Initial savings: 12k tokens**

**Per-spawn savings:**
- Each agent prompt reduced by 2-4k tokens
- Average 50-100 agent spawns per project
- **Per-project savings: 100-400k tokens**

## Implementation Requirements

1. Create `agents/base-agent.md` with common content
2. Extract shared philosophy, principles, git protocol
3. Update all 11 agent files to reference base
4. Ensure agent-specific content remains in respective files
5. Test each agent type for quality maintenance

## Affected Files

All agent files:
- `agents/gsd-executor.md`
- `agents/gsd-planner.md`
- `agents/gsd-verifier.md`
- `agents/gsd-debugger.md`
- `agents/gsd-researcher.md`
- `agents/gsd-plan-checker.md`
- `agents/gsd-roadmapper.md`
- `agents/gsd-codebase-mapper.md`
- `agents/gsd-project-researcher.md`
- `agents/gsd-research-synthesizer.md`
- `agents/gsd-integration-checker.md`

## Success Criteria

- [ ] Base agent file created with common content
- [ ] All agents reference base and maintain specific sections
- [ ] No regression in agent behavior or output quality
- [ ] Token usage reduced by target amount
- [ ] Easier to maintain common patterns

## Dependencies

None - can be implemented independently

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.
