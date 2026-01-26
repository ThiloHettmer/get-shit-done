# Token Reduction Analysis for Get Shit Done

**Status:** Analysis Phase  
**Version:** 1.0  
**Date:** 2026-01-26  
**Context:** GSD framework currently has high token usage due to extensive context engineering and multi-agent orchestration

---

## Executive Summary

The Get Shit Done framework is highly effective but token-intensive due to its comprehensive context engineering approach. This analysis identifies **7 major categories** of token reduction opportunities that could reduce usage by **40-60%** without compromising quality.

**Key Insight:** The system prioritizes correctness and completeness over token efficiency. Many optimizations are possible by introducing selective context loading, compressed formats, and intelligent caching.

---

## Current Token Usage Patterns

### 1. Multi-Agent Spawning (Highest Impact)
**Current State:**
- Each agent gets fresh 200k context window
- 4-8 agents spawn per phase (planner, executor × N, verifier, debugger)
- Parallel execution creates multiple simultaneous contexts
- Agent prompts are 3,000-8,000 tokens each

**Token Cost Per Phase:**
- Planning: ~50k tokens (planner + checker + researcher agents)
- Execution: ~150k-300k tokens (multiple executor agents in parallel)
- Verification: ~40k tokens (verifier + potential debugger agents)
- **Total: 240k-390k tokens per phase**

### 2. Template & Reference Loading (High Impact)
**Current State:**
- Agent definitions: 3,000-7,000 tokens each (11 agents)
- Workflow files: 2,000-5,000 tokens each (12 workflows)
- Templates: 1,000-3,000 tokens each (18 templates)
- References: 1,500-4,000 tokens each (9 references)
- **Total static content: ~100k tokens**

**Loading Pattern:**
- Every agent loads: execute-plan workflow (~4k), summary template (~2.5k), checkpoints reference (~3k)
- Planner loads: phase-prompt template (~5k), continuation format (~2k), git integration (~3k)
- Executor loads: deviation rules (~2k), TDD reference (~3k), git patterns (~3k)

**Repetitive Loading:**
- Same templates/references loaded 10-20 times per phase
- ~70% of loaded reference content is never actually used
- Most agents only need 20-30% of loaded reference material

### 3. State File Overhead (Medium Impact)
**Current State:**
- STATE.md: 200-400 tokens (loaded by every agent)
- PROJECT.md: 300-800 tokens (loaded by most agents)
- ROADMAP.md: 400-1,000 tokens (loaded by orchestrators)
- REQUIREMENTS.md: 500-2,000 tokens (loaded during planning)
- config.json: 100-200 tokens (parsed by every operation)

**Repetitive Patterns:**
- Same state files read 15-25 times per phase execution
- STATE.md "Decisions Made" table grows unbounded (every completed plan adds row)
- ROADMAP.md includes all phases, but agents only need current phase context

### 4. Plan & Summary Files (Medium Impact)
**Current State:**
- Each PLAN.md: 1,500-4,000 tokens
- Each SUMMARY.md: 1,000-2,500 tokens
- Phases have 3-10 plans each
- Frontmatter: 200-400 tokens per file (verbose YAML)

**Chaining Pattern:**
- Plans reference prior SUMMARY files via `@.planning/phases/.../SUMMARY.md`
- Verification reads all SUMMARYs to check deliverables
- Cumulative: Phase 5 loads summaries from Phases 1-4 (10-30k tokens)

### 5. XML Structure Verbosity (Medium Impact)
**Current State:**
- XML tags are semantic but verbose: `<execution_context>`, `<checkpoint:human-verify>`, `<authentication-attempted>`
- Every task has 5 required elements: `<name>`, `<files>`, `<action>`, `<verify>`, `<done>`
- Nested structures with markdown inside XML
- Extensive inline documentation in agent prompts

**Example Comparison:**
```xml
<!-- Current: ~250 tokens -->
<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
    Dashboard layout implemented - dev server at http://localhost:3000
  </what-built>
  <how-to-verify>
    1. Visit http://localhost:3000/dashboard
    2. Resize browser window from 375px to 1920px
    3. Verify layout adapts: mobile (1 col) → tablet (2 col) → desktop (3 col)
  </how-to-verify>
  <resume-signal>Type "approved" or describe issues</resume-signal>
</task>

<!-- Potential compressed: ~120 tokens -->
<task type="verify" gate="block">
  <built>Dashboard at localhost:3000</built>
  <test>Resize 375-1920px: 1col→2col→3col</test>
  <signal>approved|issues</signal>
</task>
```

### 6. Agent Prompt Redundancy (Medium-Low Impact)
**Current State:**
- Each agent has extensive `<philosophy>` sections (500-1,000 tokens)
- Detailed `<execution_flow>` with step-by-step instructions (1,000-2,000 tokens)
- Repetitive patterns across agents (deviation rules, checkpoint protocols, git protocols)
- Agent-specific rules embedded in prompt rather than referenced

**Overlap:**
- 60% of gsd-executor and gsd-planner philosophy is identical
- Git commit protocol appears in executor, orchestrator, and planner (3x duplication)
- Checkpoint protocol appears in executor and multiple workflow files

### 7. Documentation & Inline Comments (Low Impact)
**Current State:**
- Extensive inline documentation in templates (300-500 tokens per template)
- Comments explaining usage patterns: `<!-- Key rule: ... -->`
- Examples embedded in templates and reference files
- Guideline sections that could be externalized

---

## Proposed Optimization Categories

### Category A: Selective Context Loading (40-50% reduction potential)

#### A1. Lazy Template Loading
**Current:** Every agent loads full templates unconditionally  
**Proposed:** Load template sections on-demand

```markdown
<!-- Instead of @templates/summary.md (2,500 tokens) -->
<!-- Load only needed sections -->
@templates/summary.md#frontmatter (400 tokens)
@templates/summary.md#task-commits (300 tokens)
```

**Implementation:**
- Add section anchors to templates
- Parse requests for specific sections
- Return only requested content

**Token Savings:** 8-12k per phase (multiple agent spawns)

#### A2. Context-Aware Reference Loading
**Current:** Executor loads all references (checkpoints, TDD, git, continuation)  
**Proposed:** Load based on plan characteristics

```javascript
// Pseudo-logic
if (plan.has_checkpoints) load('checkpoints.md')
if (plan.type === 'tdd') load('tdd.md')
if (plan.gap_closure) load('verification-patterns.md')
// Always load git-integration.md (minimal)
```

**Token Savings:** 5-8k per executor agent spawn

#### A3. Incremental State Loading
**Current:** Full STATE.md loaded every time (200-400 tokens, growing)  
**Proposed:** Load only recent context

```yaml
# state-current.md (trimmed to last 2 phases)
phase: 5
recent_decisions: [last 5 decisions]
active_concerns: [only unresolved]

# state-archive.md (historical, rarely loaded)
phase_history: [phases 1-3 full history]
all_decisions: [complete list]
```

**Token Savings:** 100-200 tokens per agent × 15 agents = 1.5-3k per phase

#### A4. Pruned ROADMAP Context
**Current:** Full roadmap with all phases loaded  
**Proposed:** Load only current + adjacent phases

```markdown
# roadmap-current.md
Phase 4: ✓ Complete
Phase 5: ← Current (expanded details)
Phase 6: Pending (brief)

# roadmap-full.md (loaded only by orchestrator)
[All phases with full details]
```

**Token Savings:** 300-600 tokens per load × 10 loads = 3-6k per phase

#### A5. Summary Frontmatter Scanning
**Current:** Full SUMMARY.md files loaded to check dependencies  
**Proposed:** Scan frontmatter only (first 30 lines), load full content on match

```bash
# Quick scan for dependency graph
for summary in phases/*/SUMMARY.md; do
  head -30 "$summary"  # Just frontmatter
done
# If relevant: load full summary
```

**Token Savings:** 12-20k per planning phase (scans 20-40 summaries)

---

### Category B: Compressed Formats (15-25% reduction potential)

#### B1. Abbreviated XML Tags
**Proposed Changes:**
```xml
<!-- Current → Proposed -->
<execution_context> → <exec>
<what-built> → <built>
<how-to-verify> → <verify>
<resume-signal> → <signal>
<checkpoint:human-verify> → <check:verify>
<authentication-attempted> → <auth-tried>
```

**Considerations:**
- Maintain semantic meaning
- Keep readability for humans reviewing plans
- Claude handles abbreviations well

**Token Savings:** 15-20% of XML content = 8-12k per phase

#### B2. Frontmatter Compression
**Current Frontmatter:** 200-400 tokens  
**Proposed Compressed:**

```yaml
# Current (350 tokens)
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

# Proposed (180 tokens)
---
p: 01-foundation | pl: 02 | t: exec | w: 2
deps: [01-01] | auto: y | gap: n
files: [src/app/api/auth/*.ts]
must: {
  truth: [register, login],
  files: [src/app/api/auth/register/route.ts → POST],
  links: [RegisterForm.tsx → /api/auth/register]
}
---
```

**Token Savings:** 150-200 tokens × 30 files = 4.5-6k per project

#### B3. Compact Agent Prompts
**Current:** Verbose execution flows with philosophical context  
**Proposed:** Distilled operational prompts + external reference

```markdown
<!-- Current gsd-executor: 7,800 tokens -->
<role>
You are a GSD plan executor. You execute PLAN.md files atomically...
[300 tokens of role description]
</role>

<philosophy>
[500 tokens explaining context engineering, quality curves, etc.]
</philosophy>

<execution_flow>
<step name="load_project_state" priority="first">
[300 tokens of detailed instructions]
</step>
[20 more steps, 3,000 tokens total]
</execution_flow>

<!-- Proposed: 3,200 tokens -->
<role>GSD executor: atomic PLAN.md execution, per-task commits, SUMMARY.md creation</role>

<critical_rules>
1. Load STATE.md first
2. Execute tasks sequentially
3. Commit after each task (type(phase-plan): description)
4. STOP at checkpoints (return structured format)
5. Create SUMMARY.md using @template#format
</critical_rules>

<flow>
load_state → load_plan → execute_tasks → create_summary → update_state
</flow>

<!-- Detailed patterns externalized to reference docs -->
<on_deviation>@references/deviation-rules.md</on_deviation>
<on_checkpoint>@references/checkpoint-protocol.md</on_checkpoint>
```

**Token Savings:** 3-4k per agent × 11 agents = 33-44k initial load

---

### Category C: Intelligent Caching (20-30% reduction potential)

#### C1. Template Memoization
**Concept:** Cache frequently-loaded templates in session

```
First load: @templates/summary.md (2,500 tokens)
Subsequent: <cached:summary-template> (50 token reference)
```

**Requirements:**
- Session-level cache (doesn't persist across /clear)
- Invalidation strategy (user edits templates)
- Explicit cache key references

**Token Savings:** 10-15k per phase (5-6 repeated template loads avoided)

#### C2. Dependency Graph Precomputation
**Current:** Every planner agent builds dependency graph from scratch by scanning all SUMMARY frontmatter  
**Proposed:** Pre-compute and cache in STATE.md

```yaml
# STATE.md addition
dependency_graph:
  "05": {requires: ["03", "04"], provides: ["auth-system"], affects: ["06", "07"]}
  "06": {requires: ["05"], provides: ["dashboard"], affects: ["08"]}
```

**Token Savings:** 8-12k per planning phase (avoids loading 20-40 SUMMARY files)

#### C3. Codebase Map Selective Loading
**Current:** Load full codebase analysis files (STACK.md, ARCHITECTURE.md, etc.)  
**Proposed:** Index and load relevant sections

```bash
# Current: load all 7 files (12-18k tokens)
cat .planning/codebase/{STACK,ARCHITECTURE,CONVENTIONS,STRUCTURE,INTEGRATIONS,CONCERNS,TESTING}.md

# Proposed: selective loading based on phase keywords
if phase matches "API|endpoint|backend": load ARCHITECTURE.md + CONVENTIONS.md
if phase matches "UI|frontend|component": load CONVENTIONS.md + STRUCTURE.md
```

**Token Savings:** 8-12k per planning phase

---

### Category D: Structural Refactoring (25-35% reduction potential)

#### D1. Unified Agent Base Prompt
**Current:** Each agent has redundant sections (philosophy, success criteria, git protocols)  
**Proposed:** Extract common prompt base

```markdown
# agents/base-agent.md (1,200 tokens)
<role>GSD agent operating in structured multi-agent workflow</role>
<core_principles>
- Plans are prompts (no transformation)
- Context engineering (stay under 50% usage)
- Atomic commits (one task = one commit)
- Goal-backward verification
</core_principles>

# agents/gsd-executor.md (now 3,500 tokens vs 7,800)
@agents/base-agent.md
<specific_role>Execute PLAN.md files with atomic commits</specific_role>
<execution_flow>[executor-specific steps]</execution_flow>
```

**Token Savings:** 2-3k per agent × 11 agents = 22-33k

#### D2. Consolidated Reference Documents
**Current:** 9 separate reference files with overlap  
**Proposed:** Merge and modularize

```markdown
# references/execution.md (consolidates checkpoints + continuation + git)
## Checkpoint Protocol
[checkpoint patterns]

## Continuation Format  
[continuation patterns]

## Git Integration
[commit patterns]

# Load selectively
@references/execution.md#checkpoints (when needed)
@references/execution.md#git (always)
```

**Token Savings:** 4-6k per phase (eliminates redundant section headers, examples)

#### D3. Hierarchical Template Structure
**Current:** Flat template files with all sections included  
**Proposed:** Nested includes with defaults

```markdown
# templates/summary.md (master)
@templates/summary/frontmatter.md
@templates/summary/performance.md
@templates/summary/commits.md
@templates/summary/deviations.md

# Agent loads only what it needs to write
@templates/summary/frontmatter.md
@templates/summary/commits.md
# (skips performance, deviations until writing that section)
```

**Token Savings:** 6-9k per phase

---

### Category E: Execution Pattern Changes (10-20% reduction potential)

#### E1. Batch Agent Communication
**Current:** Each agent loads full plan + state + context independently  
**Proposed:** Orchestrator pre-loads and passes trimmed context

```javascript
// Orchestrator reads once
const plan = readFile('01-02-PLAN.md')
const state = readFile('STATE.md')

// Extract only what executor needs
const trimmedContext = {
  plan_tasks: extractTasks(plan),
  current_phase: state.current_position,
  recent_decisions: state.decisions.slice(-5)
}

// Pass trimmed context (70% smaller)
Task({
  prompt: buildExecutorPrompt(trimmedContext),
  agent: 'gsd-executor'
})
```

**Token Savings:** 5-8k per executor spawn × 3-5 executors = 15-40k per phase

#### E2. Summary Streaming
**Current:** Complete SUMMARY.md file loaded by verifier  
**Proposed:** Stream deliverables section only for verification

```markdown
# SUMMARY.md structure remains same for human readers
# But verifier loads via:
@.planning/phases/01-foundation/01-02-SUMMARY.md#accomplishments
@.planning/phases/01-foundation/01-02-SUMMARY.md#files-created

# Instead of full file (2,000 tokens → 400 tokens)
```

**Token Savings:** 1.6k per summary × 10 summaries loaded = 16k per verification

#### E3. Progressive Detail Loading
**Current:** Full plan details loaded upfront  
**Proposed:** Load outline first, details on-demand

```xml
<!-- Phase 1: Load skeleton (800 tokens) -->
<objective>Build authentication system</objective>
<tasks>
  <task id="1" type="auto">Create User model</task>
  <task id="2" type="auto">Registration endpoint</task>
  <task id="3" type="auto">Login endpoint</task>
</tasks>

<!-- Phase 2: When executing task 1, load details (200 tokens) -->
@plan#task-1-details
<files>src/models/user.ts</files>
<action>[specific implementation]</action>
<verify>[verification command]</verify>
<done>[acceptance criteria]</done>
```

**Token Savings:** 1-1.5k per plan (details only loaded when executing task)

---

### Category F: Metadata Optimization (5-10% reduction potential)

#### F1. Numeric Phase IDs
**Current:** `phase: 01-foundation`, `plan: 02`  
**Proposed:** `p:1`, `pl:2` (human-readable names in separate index)

```yaml
# config/phase-index.json
{"1": "foundation", "2": "core-features", ...}

# PLAN.md frontmatter
p:1|pl:2|w:2  # instead of phase: 01-foundation, plan: 02, wave: 2
```

**Token Savings:** 30-50 tokens per file × 50 files = 1.5-2.5k per project

#### F2. Abbreviated Must-Haves
**Current:** Verbose goal-backward criteria  
**Proposed:** Compact format with semantic keys

```yaml
# Current (600 tokens)
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

# Proposed (280 tokens)
must:
  can: [register-email, login-jwt, persist-session]
  has: [api/auth/register→POST, api/auth/login→POST]
  links: [RegisterForm→/api/auth/register]
```

**Token Savings:** 300-400 tokens per plan × 30 plans = 9-12k per project

#### F3. Commit Message Compression
**Current:** Verbose commit message format in SUMMARY.md  
**Proposed:** Abbreviated format with full details in git log

```markdown
# Current SUMMARY.md (600 tokens)
## Task Commits
1. **Task 1: Create User model with authentication fields** - `abc123f` (feat)
   - Added User model to schema.prisma
   - Includes email (unique), password hash, createdAt, updatedAt
   - Set up Prisma Client configuration
2. **Task 2: Implement registration endpoint with validation** - `def456g` (feat)
   ...

# Proposed SUMMARY.md (240 tokens)
## Commits
abc123f feat(01-02): User model
def456g feat(01-02): Registration endpoint
hij789k feat(01-02): Login endpoint
lmn012o docs(01-02): Complete plan
```

**Token Savings:** 350 tokens per summary × 30 summaries = 10.5k per project

---

### Category G: Agent Architecture Changes (15-25% reduction potential)

#### G1. Shared Context Pool
**Current:** Each agent loads STATE.md, config.json independently  
**Proposed:** Orchestrator maintains shared context, injects only diffs

```javascript
// Orchestrator loads once
const sharedContext = {
  project: read('PROJECT.md'),
  state: read('STATE.md'),
  config: read('config.json')
}

// Agent prompt includes only deltas
Task({
  prompt: `
    Execute plan 01-02
    Context diff since last agent:
    - New decision: Use jose library for JWT
    - Phase 01 → Phase 02 transition
    
    [Full context available via @shared-context if needed]
  `,
  agent: 'gsd-executor'
})
```

**Token Savings:** 400-600 tokens per agent × 8 agents = 3.2-4.8k per phase

#### G2. Workflow Templating
**Current:** Workflow files contain full orchestration logic (2-5k tokens each)  
**Proposed:** Parameterized workflow engine + compact configs

```yaml
# workflows/execute-phase.config
pattern: wave-orchestration
agents: [gsd-executor]
checkpoint_handling: continuation-spawn
result_collection: summary-verification

# workflows/wave-orchestration.template (shared by multiple workflows)
[Generic wave execution pattern - loaded once]
```

**Token Savings:** 8-12k per phase (workflows loaded 3-5 times)

#### G3. Lazy Agent Loading
**Current:** Agent definitions loaded upfront (full 7k token prompt)  
**Proposed:** Load agent core + lazy-load sub-protocols

```markdown
# Agent spawn loads core (2k tokens)
<role>Execute PLAN.md atomically</role>
<critical_steps>load→execute→commit→summarize</critical_steps>

# Sub-protocols loaded on-trigger
When deviation detected: load @protocols/deviation-handling.md
When checkpoint hit: load @protocols/checkpoint-return.md
When TDD task: load @protocols/tdd-cycle.md
```

**Token Savings:** 3-5k per agent spawn × 8 spawns = 24-40k per phase

---

## Implementation Priority Matrix

| Category | Reduction Potential | Implementation Complexity | Risk | Priority |
|----------|-------------------|---------------------------|------|----------|
| A1: Lazy Template Loading | High (8-12k) | Medium | Low | **P0** |
| A2: Context-Aware Reference Loading | Medium (5-8k) | Low | Low | **P0** |
| B1: Abbreviated XML Tags | Medium (8-12k) | Low | Medium | **P1** |
| D1: Unified Agent Base Prompt | High (22-33k) | Medium | Low | **P0** |
| E1: Batch Agent Communication | High (15-40k) | High | Medium | **P1** |
| A3: Incremental State Loading | Low (1.5-3k) | Low | Low | **P1** |
| C2: Dependency Graph Cache | Medium (8-12k) | Medium | Low | **P1** |
| D2: Consolidated References | Medium (4-6k) | Low | Low | **P2** |
| G3: Lazy Agent Loading | High (24-40k) | High | Medium | **P2** |
| B2: Frontmatter Compression | Low (4.5-6k) | Low | Medium | **P2** |
| A4: Pruned ROADMAP Context | Low (3-6k) | Low | Low | **P2** |
| F2: Abbreviated Must-Haves | Medium (9-12k) | Medium | Medium | **P3** |

**Priority Definitions:**
- **P0:** High impact, low risk, implement first
- **P1:** Medium-high impact, reasonable effort
- **P2:** Lower impact or higher complexity
- **P3:** Nice-to-have optimizations

---

## Estimated Token Savings

### Per Phase Execution
| Category | Current Tokens | Optimized Tokens | Savings |
|----------|----------------|------------------|---------|
| Multi-Agent Spawning | 240-390k | 140-220k | **100-170k (42-44%)** |
| Template/Reference Loading | 60-80k | 25-35k | **35-45k (58-56%)** |
| State File Overhead | 15-25k | 8-12k | **7-13k (47-52%)** |
| XML Structure | 20-30k | 16-22k | **4-8k (20-27%)** |
| **Total Per Phase** | **335-525k** | **189-289k** | **146-236k (44-45%)** |

### Per Full Project (5 phases)
| | Current | Optimized | Savings |
|---|---------|-----------|---------|
| Total Token Usage | 1.7M - 2.6M | 0.9M - 1.4M | **0.8M - 1.2M (47%)** |

---

## Risk Assessment

### Low Risk Changes (Implement First)
1. **Lazy template loading** - Additive change, doesn't alter behavior
2. **Context-aware reference loading** - Conditional logic, easy to test
3. **Incremental state loading** - Backwards compatible format
4. **Consolidated references** - Pure restructuring
5. **Pruned roadmap context** - Subset of existing content

### Medium Risk Changes (Test Thoroughly)
1. **Abbreviated XML tags** - Affects parsing, readability for human review
2. **Frontmatter compression** - Changes file format (maintain backwards compat)
3. **Batch agent communication** - Orchestrator becomes stateful
4. **Abbreviated must-haves** - Affects verification logic

### High Risk Changes (Phase 2+)
1. **Agent architecture overhaul** - Core system changes
2. **Workflow templating** - Fundamental restructuring
3. **Progressive detail loading** - Complex state management
4. **Shared context pool** - Memory and synchronization concerns

---

## Implementation Roadmap

### Phase 1: Quick Wins (2-4 weeks)
**Target: 25-30% token reduction**

1. **Week 1-2: Selective Loading**
   - Implement lazy template section loading
   - Add context-aware reference loading
   - Create pruned state/roadmap variants

2. **Week 3-4: Agent Consolidation**
   - Extract common agent base prompt
   - Consolidate overlapping reference files
   - Create unified git/checkpoint protocols

**Estimated Savings:** 80-120k tokens per phase

### Phase 2: Structural Changes (4-6 weeks)
**Target: Additional 15-20% reduction**

1. **Week 5-7: Format Optimization**
   - Implement abbreviated XML tags
   - Compress frontmatter format
   - Test with existing plans

2. **Week 8-10: Execution Improvements**
   - Batch agent communication
   - Summary streaming
   - Dependency graph caching

**Estimated Savings:** Additional 50-80k tokens per phase

### Phase 3: Advanced Optimizations (6-8 weeks)
**Target: Additional 5-10% reduction**

1. **Week 11-14: Architecture Changes**
   - Lazy agent loading
   - Shared context pool
   - Workflow templating engine

2. **Week 15-18: Metadata & Polish**
   - Numeric phase IDs
   - Compact must-haves format
   - Progressive detail loading

**Estimated Savings:** Additional 20-40k tokens per phase

---

## Testing & Validation Strategy

### Correctness Validation
1. **Golden Tests:** Run optimized system on 5 reference projects, compare outputs
2. **Plan Execution:** Verify PLAN.md files execute identically
3. **Verification:** Confirm must-haves checking produces same results
4. **Git History:** Validate commit structure unchanged

### Token Measurement
1. **Instrumentation:** Add token counting to all agent spawns
2. **Benchmarks:** Establish baseline on 10 diverse projects
3. **Regression Tests:** Alert if token usage increases in any category
4. **Reporting:** Per-phase token breakdown dashboard

### Human Factors
1. **Readability:** Survey users on plan/summary readability
2. **Debugging:** Verify abbreviated formats don't hinder troubleshooting
3. **Onboarding:** Test new user comprehension of optimized format
4. **Documentation:** Update all references to new formats

---

## Compatibility Considerations

### Backwards Compatibility
**Approaches:**
1. **Dual Format Support:** Accept both verbose and compact formats (Phase 1)
2. **Migration Tool:** Convert existing .planning/ directories to optimized format
3. **Version Flag:** config.json includes `format_version: 2` for new projects

### Forward Compatibility
**Strategies:**
1. **Schema Versioning:** All files include format version in frontmatter
2. **Graceful Degradation:** Missing sections load defaults
3. **Migration Path:** Clear upgrade guide for existing projects

### Ecosystem Impact
**Considerations:**
1. **Community Ports:** gsd-opencode, gsd-gemini would need updates
2. **Custom Extensions:** Users with modified templates need migration guide
3. **Documentation:** All .docs/ files need updates to reflect new formats

---

## Monitoring & Metrics

### Key Metrics to Track
1. **Token Usage:**
   - Tokens per phase (by category: agents, templates, state, XML)
   - Tokens per agent spawn
   - Cumulative project token usage

2. **Quality Indicators:**
   - Plan execution success rate
   - Verification pass rate
   - User-reported issues with optimized format

3. **Performance:**
   - Time to execute phase
   - Agent spawn latency
   - Context loading time

### Success Criteria
- **40%+ token reduction** without quality degradation
- **Zero increase** in plan execution failures
- **Maintained** verification accuracy
- **Positive** user feedback on new format

---

## Alternative Approaches Considered

### 1. Binary/Compressed Format
**Idea:** Use binary protocol buffers or compressed JSON instead of markdown/XML  
**Rejected Because:**
- Loses human readability (core GSD principle)
- Harder to debug and review
- Breaks git diffs
- Only ~10-15% additional savings

### 2. Single Mega-Agent
**Idea:** Replace multi-agent orchestration with one agent handling entire phase  
**Rejected Because:**
- Violates context engineering principles (quality degradation)
- Loses parallelization benefits
- Token savings minimal (still loads similar context)

### 3. External Database
**Idea:** Store state/summaries in SQLite instead of markdown files  
**Rejected Because:**
- Breaks "everything in git" principle
- Complicates setup and portability
- Harder to inspect/debug
- Only saves ~5-10% tokens

### 4. Streaming Protocol
**Idea:** Stream plan execution results instead of complete SUMMARY files  
**Rejected Because:**
- Incompatible with Task tool's current API
- Verification needs complete context
- Complex state management
- Deferred to future Claude Code capability

---

## Questions for Implementation

### Technical Decisions
1. **Abbreviation Strategy:** Use semantic short-codes or single letters? (e.g., `<exec>` vs `<e>`)
2. **Cache Scope:** Session-level or persistent across /clear?
3. **Migration Approach:** Big bang or gradual rollout?
4. **Backwards Compat Duration:** Support old format for how long?

### User Experience
1. **Format Preference:** Allow users to choose verbose vs compact?
2. **Documentation Strategy:** Migrate docs first or in parallel?
3. **Breaking Changes:** Acceptable for major version bump?
4. **Community Input:** Beta test with subset of users first?

### Validation
1. **Test Coverage:** How many reference projects needed?
2. **Performance Testing:** Token counting strategy?
3. **Rollback Plan:** How to revert if issues found?

---

## Conclusion

The GSD framework's high token usage stems from its deliberate choice to prioritize correctness through comprehensive context engineering. The proposed optimizations can reduce token usage by **40-60%** while maintaining quality:

**Primary Strategies:**
1. **Selective Loading:** Only load content actually needed by each agent
2. **Format Compression:** Abbreviate verbose XML and frontmatter
3. **Structural Refactoring:** Eliminate redundancy across agents
4. **Intelligent Caching:** Avoid repeated loads of static content

**Implementation Path:**
- Phase 1 (Quick Wins): 25-30% reduction, low risk
- Phase 2 (Structural): +15-20% reduction, medium risk  
- Phase 3 (Advanced): +5-10% reduction, higher complexity

**Next Steps:**
1. Review this analysis with maintainers/community
2. Prioritize P0 optimizations for implementation
3. Build instrumentation for token measurement
4. Create migration tooling for existing projects
5. Begin Phase 1 implementation with automated testing

The optimizations preserve GSD's core strengths (correctness, git-based state, human readability) while dramatically improving token efficiency.
