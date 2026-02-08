# GSD Component Manifest

This document maps the internal GSD agents and tools to the external orchestration components defined in `component_schemas.ts`.

## 1. Phase Researcher
- **Internal Agent:** `gsd-phase-researcher`
- **Schema:** `ResearcherInput` -> `ResearcherOutput`
- **Source:** `agents/gsd-phase-researcher.md`
- **Tooling:** `gsd-tools.js init plan-phase` (extracts inputs)

## 2. Planner
- **Internal Agent:** `gsd-planner`
- **Schema:** `PlannerInput` -> `PlannerOutput`
- **Source:** `agents/gsd-planner.md`
- **Tooling:** 
  - Inputs: `gsd-tools.js init plan-phase` + `RESEARCH.md`
  - Outputs: `[PHASE]-[PLAN]-PLAN.md` files

## 3. Plan Checker
- **Internal Agent:** `gsd-plan-checker`
- **Schema:** `PlanCheckerInput` -> `PlanCheckerOutput`
- **Source:** `agents/gsd-plan-checker.md`
- **Tooling:** `gsd-tools.js verify plan-structure` (internal logic used by agent)

## 4. Executor
- **Internal Agent:** `gsd-executor`
- **Schema:** `ExecutorInput` -> `ExecutorOutput`
- **Source:** `agents/gsd-executor.md`
- **Tooling:** `gsd-tools.js init execute-phase`

## 5. Phase Verifier
- **Internal Agent:** `gsd-verifier`
- **Schema:** `PhaseVerifierInput` -> `PhaseVerifierOutput`
- **Source:** `agents/gsd-verifier.md`
- **Tooling:** `gsd-tools.js init verify-work`

## Extraction Strategy
To "extract" these components, we need to wrap the internal agent prompts and `gsd-tools.js` logic into the interfaces defined in `component_schemas.ts`.

### Wrapper Logic
For each component, the wrapper must:
1. **Hydrate State:** Use `gsd-tools.js` to load the `GSDOrchestratorState` from disk.
2. **Transform Input:** Map the State to the specific Component Input schema.
3. **Invoke Agent:** Call the LLM with the agent's system prompt and the structured input.
4. **Parse Output:** validate the agent's response and map it to the Component Output schema.
5. **Update State:** Write the results back to disk (`SUMMARY.md`, `STATE.md`, etc.) and update the in-memory State object.
