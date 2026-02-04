# Planning, Decomposition & Goal-Backward Strategy

## The Decomposition Problem

LLMs struggle to execute vague or large instructions (e.g., "Build a blog"). They excel at small, specific steps (e.g., "Create a `Post` model in `schema.prisma`").
**Planning** is the process of translating the former into a sequence of the latter.

## Methodology: Goal-Backward Planning

Forward planning ("What should I do first?") often leads to "rabbit holes" or busywork.
**Goal-Backward Planning** asks: "What must be TRUE for the goal to be achieved?"

### The Protocol

1.  **State the Goal**: "User can login with Email".
2.  **Derive Observable Truths**:
    - Basic: "Input field accepts text".
    - Functional: "Submit button sends POST request".
    - Outcome: "Valid credentials set a Cookie".
3.  **Derive Artifacts**: What files must exist for the truth to be valid?
    - `login-form.tsx`
    - `/api/login/route.ts`
4.  **Derive Wiring**: How do they connect?
    - "Form calls Route".

## The Plan Structure (XML Prompts)

We use XML for plans because it is highly parseable by LLMs and enforces strict structure. A Plan is a **Prompt** for the Executor.

```xml
<plan>
  <objective>precise goal</objective>
  <context>
    @src/utils/auth.ts
    @prisma/schema.prisma
  </context>

  <task type="auto">
    <action>Create POST endpoint...</action>
    <verify>curl verification command</verify>
    <done>Returns 200 OK</done>
  </task>

  <task type="checkpoint:human-verify">
    <instruction>Check the UI for alignment</instruction>
  </task>
</plan>
```

## Automated Chunking (The 50% Rule)

The Planner is explicitly instructed to "Chunk" work.

- **Time Heuristic**: Each task = 15-60 mins of LLM execution.
- **Context Cost**:
  - < 3 files modified = Low Cost.
  - > 5 files modified = High Cost (Split Plan).
- **Complexity Heuristic**:
  - CRUD = Low.
  - Auth/Crypto/Payment = High (Limit to 1 task per plan).

## Recursive Planning

For highly complex tasks, use **Recursive Planning**:

1.  **Master Plan**: High-level phases.
2.  **Phase Plan**: Broken down into "Plans".
3.  **TDD Plan**: If a task is complex (Logic/Algo), create a specific **TDD Plan** (Red-Green-Refactor).

## Dependency Graphing

The Planner must explicitly output dependencies to enable parallelization.

- `needs`: [Plan ID] - Wait for this.
- `creates`: [File/Type] - Outputs this.
- `wave`: [Int] - Calculated execution group.

**Vertical Slices vs Horizontal Layers**:
Prefer Vertical Slices (Feature A: DB+API+UI) over Horizontal (All DBs, All APIs). Vertical slices are less coupled and allow better parallelization.
