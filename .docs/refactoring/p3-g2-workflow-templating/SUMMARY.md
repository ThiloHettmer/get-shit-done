# Workflow Templating

**Priority:** P3  
**Category:** G - Agent Architecture Changes  
**Estimated Token Savings:** 8-12k per phase  
**Implementation Complexity:** High  
**Risk Level:** High (fundamental restructuring)

## Overview

Workflow files contain full orchestration logic (2-5k tokens each). This task creates parameterized workflow engine with compact configs, sharing common orchestration patterns.

## Current Approach

**Each workflow is self-contained:**

```markdown
# execute-phase.md (4,500 tokens)
<purpose>Execute all plans in phase using wave-based parallel execution</purpose>

<process>
<step name="load_state">
Read STATE.md...
[300 tokens of detailed instructions]
</step>

<step name="discover_plans">
List all PLAN.md files...
[400 tokens]
</step>

<step name="group_by_wave">
Read wave from frontmatter...
[300 tokens]
</step>

<step name="execute_waves">
For each wave...
[1,500 tokens]
</step>

<step name="handle_checkpoints">
When checkpoint hit...
[800 tokens]
</step>

<step name="verify_phase">
Spawn verifier...
[400 tokens]
</step>
</process>
```

**Similar patterns repeated in:**
- `verify-phase.md`
- `diagnose-issues.md`
- `complete-milestone.md`

## Proposed Approach

**Workflow config (compact):**

```yaml
# workflows/execute-phase.config (200 tokens)
workflow_type: wave-orchestration
agents:
  - type: gsd-executor
    spawn: parallel-by-wave
    input: plan-content
checkpoint_handling: continuation-spawn
result_collection: summary-verification
post_execution:
  - spawn: gsd-verifier
  - update: STATE.md
  - update: ROADMAP.md
```

**Workflow engine (shared, loaded once):**

```markdown
# workflows/engine/wave-orchestration.md (2,000 tokens)
Generic wave-based orchestration pattern.

Steps:
1. Load state
2. Discover plans
3. Group by wave
4. Execute wave agents in parallel
5. Handle checkpoints
6. Collect results
7. Run post-execution

[Parameterized by workflow config]
```

## What This Achieves

- **80% reduction** in workflow file size
- **Shared patterns** across similar workflows
- **Easier maintenance** - update engine, all workflows benefit
- **Configuration over code** - workflows become declarative

## Token Impact

**Current:**
- 12 workflow files × 2,500 tokens average = 30k tokens
- Loaded 3-5 times per phase = 90-150k tokens per project

**Optimized:**
- 12 config files × 200 tokens = 2.4k tokens
- 3 engine files × 2,000 tokens = 6k tokens (loaded once)
- Total: 8.4k tokens
- Loaded 3-5 times: 25-42k tokens per project

**Savings: 65-108k per project (8-12k per phase)**

## Implementation Requirements

1. Identify common orchestration patterns
2. Design workflow engine architecture
3. Create engine templates (wave-orchestration, sequential, conditional)
4. Convert existing workflows to configs
5. Implement engine interpreter
6. Test all workflow types with engine
7. Ensure no loss of functionality

## Affected Files

**Create:**
```
workflows/engine/
├── wave-orchestration.md
├── sequential-execution.md
└── conditional-flow.md

workflows/configs/
├── execute-phase.yaml
├── verify-phase.yaml
├── diagnose-issues.yaml
└── [12 total configs]
```

**Convert to configs:**
- All 12 existing workflow files

**Update:**
- Command files that reference workflows
- Agent files that reference workflows

## Success Criteria

- [ ] Workflow engine implemented and tested
- [ ] Common patterns extracted to engine templates
- [ ] All workflows converted to configs
- [ ] Engine correctly interprets all configs
- [ ] No regression in orchestration behavior
- [ ] Token usage reduced by target amount
- [ ] Easier to add new workflows (just config)

## Dependencies

**High complexity - implement last:**
- Requires stable agent architecture
- Works after other optimizations proven

**Conflicts with:**
- May not be worth complexity if other optimizations are sufficient

## Follow-up Tasks

This task directory will be broken down into smaller implementation tasks in a later phase.

**Note:** This is highest risk/complexity optimization. Consider implementing only if earlier optimizations don't meet token reduction targets.
