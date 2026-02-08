1. Extract the Core Orchestration Pattern
   Create a generic orchestration spec that works with any LLM:
   markdown# Generic Multi-Agent Task Execution System

## Core Components

### Orchestrator (Main Agent)

- Reads task plan
- Identifies execution segments
- Spawns sub-agents with context
- Handles checkpoints
- Aggregates results
- Updates state

### Executor (Sub-Agent)

- Receives task segment
- Executes autonomously
- Returns structured result
- No memory between spawns

### State Manager (File-based)

- Current position tracking
- Decision accumulation
- Completion markers (SUMMARY files)
- No database, no locks

## Execution Protocol

### Phase 1: Parse Plan

```
Input: task-plan.md
Output: {
  segments: [
    {id: 1, tasks: [1,2,3], routing: "subagent"},
    {id: 2, type: "checkpoint", subtype: "human-verify"},
    {id: 3, tasks: [4,5], routing: "subagent"}
  ]
}
```

### Phase 2: Execute Segments

```
For each segment:
  IF segment.routing == "subagent":
    result = spawn_agent({
      prompt: build_executor_prompt(segment),
      timeout: 600,
      model: "fast" | "smart"
    })

    IF result.status == "checkpoint":
      present_to_user(result.checkpoint_data)
      user_input = wait_for_user()
      spawn_continuation_agent(user_input, result.completed_work)

  IF segment.type == "checkpoint":
    present_checkpoint(segment)
    user_input = wait_for_user()
```

### Phase 3: Aggregate

```
Create SUMMARY.md from all segment results
Update STATE.md with decisions and position
```

2. Extract the Deviation Rules (Generic)
   markdown# Deviation Handling Rules (Framework Agnostic)

## Rule 1: Auto-fix bugs

**Trigger**: Code doesn't work correctly
**Action**: Fix immediately, document in summary
**Examples**: Logic errors, null checks, broken validation

## Rule 2: Auto-add critical functionality

**Trigger**: Missing essential features for correctness/security
**Action**: Add immediately, document in summary
**Examples**: Error handling, input validation, auth checks

## Rule 3: Auto-fix blockers

**Trigger**: Cannot complete current task
**Action**: Fix to unblock, document in summary  
**Examples**: Missing dependencies, wrong types, broken imports

## Rule 4: Ask about architecture

**Trigger**: Significant structural changes needed
**Action**: STOP, present to user, wait for decision
**Examples**: New database tables, framework switches, API changes

## Priority

1. If Rule 4 applies → ASK
2. If Rules 1-3 apply → FIX + DOCUMENT
3. If unsure → ASK (Rule 4)
4. Extract the Checkpoint Protocol (Generic)
   markdown# Checkpoint Protocol (Framework Agnostic)

## Checkpoint Types

### Type 1: human-verify (90%)

**Purpose**: Agent completed automation, human confirms correctness
**Structure**:

```json
{
  "type": "human-verify",
  "what_built": "Deployed app to https://...",
  "how_to_verify": [
    "Visit https://...",
    "Check layout renders correctly",
    "No console errors"
  ],
  "resume_signal": "approved | describe issues"
}
```

### Type 2: decision (9%)

**Purpose**: Human makes architectural choice
**Structure**:

```json
{
  "type": "decision",
  "decision": "Select auth provider",
  "context": "Need user authentication",
  "options": [
    {
      "id": "supabase",
      "name": "Supabase Auth",
      "pros": ["Built-in", "Free tier"],
      "cons": ["Vendor lock-in"]
    }
  ],
  "resume_signal": "Select: {option_id}"
}
```

### Type 3: human-action (1%)

**Purpose**: Truly unavoidable manual step
**Structure**:

```json
{
  "type": "human-action",
  "action": "Click email verification link",
  "what_automated": "Created account, sent verification email",
  "manual_step": "Check inbox, click link",
  "verification": "API key works after verification",
  "resume_signal": "done"
}
```

## Display Format (Terminal/UI)

```
╔═══════════════════════════════════════════════════════╗
║  CHECKPOINT: {Type}                                   ║
╚═══════════════════════════════════════════════════════╝

Progress: {X}/{Y} tasks complete
Task: {current task name}

{checkpoint-specific content}

────────────────────────────────────────────────────────
→ YOUR ACTION: {resume instruction}
────────────────────────────────────────────────────────
```

4. Extract the Task Plan Format (Generic)
   markdown# Task Plan Format (Framework Agnostic)

## Plan Structure

```xml


    phase-plan
    true|false



    What this plan achieves and why



    References to prior work, decisions, constraints




      Task name
      Files to create/modify
      What to do
      How to confirm it worked
      Completion criteria



      What was automated
      Steps to test
      How to continue




    Overall plan completion criteria


```

## Task Types

- `auto` - Agent executes autonomously
- `checkpoint:human-verify` - Agent waits for human confirmation
- `checkpoint:decision` - Agent waits for human choice
- `checkpoint:human-action` - Agent waits for manual step completion

5. Create Generic Implementation Template
   python# orchestrator.py - Framework Agnostic Orchestrator

class Orchestrator:
def **init**(self, llm_client, state_manager):
self.llm = llm_client # Any LLM API
self.state = state_manager

    def execute_plan(self, plan_path):
        """Main orchestration loop"""

        # 1. Parse plan into segments
        segments = self.parse_plan(plan_path)

        # 2. Execute each segment
        for segment in segments:
            if segment.type == "auto":
                result = self.execute_auto_segment(segment)

            elif segment.type.startswith("checkpoint"):
                result = self.execute_checkpoint(segment)

            # 3. Handle failures
            if result.status == "failed":
                self.handle_failure(result)

        # 4. Aggregate results
        self.create_summary(segments)

    def execute_auto_segment(self, segment):
        """Spawn sub-agent for autonomous execution"""

        prompt = self.build_executor_prompt(segment)

        # Use any LLM client (OpenAI, Anthropic, local model)
        response = self.llm.complete(
            prompt=prompt,
            timeout=600,
            model="smart"  # or "fast"
        )

        return self.parse_response(response)

    def execute_checkpoint(self, segment):
        """Present checkpoint to user, wait for input"""

        self.display_checkpoint(segment)
        user_input = self.wait_for_user()

        # If checkpoint was mid-execution, spawn continuation
        if segment.has_prior_work:
            return self.spawn_continuation(segment, user_input)

        return {"status": "success", "user_choice": user_input}

    def build_executor_prompt(self, segment):
        """Build prompt for sub-agent"""

        return f"""

You are executing a task segment.

## Context

{self.state.load_context()}

## Your Tasks

{segment.tasks}

## Deviation Rules

{self.load_deviation_rules()}

## Instructions

1. Execute each task
2. Apply deviation rules automatically
3. Document all deviations
4. Return structured result

## Output Format

{{
  "status": "success|failed|checkpoint",
  "tasks_completed": [...],
  "files_modified": [...],
  "deviations": [...],
  "checkpoint_data": {{}} // if status == "checkpoint"
}}
""" 6. Create Generic State Manager
python# state_manager.py - File-based state tracking

import json
from pathlib import Path

class StateManager:
def **init**(self, project_root):
self.root = Path(project_root)
self.planning_dir = self.root / ".planning"

    def is_plan_complete(self, plan_id):
        """Check if SUMMARY exists for this plan"""
        summary_path = self.planning_dir / f"{plan_id}-SUMMARY.md"
        return summary_path.exists()

    def get_next_incomplete_plan(self, phase_dir):
        """Find first PLAN without matching SUMMARY"""
        plans = sorted(phase_dir.glob("*-PLAN.md"))

        for plan in plans:
            plan_id = plan.stem.replace("-PLAN", "")
            if not self.is_plan_complete(plan_id):
                return plan

        return None

    def save_decision(self, decision, rationale):
        """Append decision to STATE.md"""
        state_file = self.planning_dir / "STATE.md"

        with open(state_file, "a") as f:
            f.write(f"\n| {decision} | {rationale} |\n")

    def update_position(self, phase, plan):
        """Update current position in STATE.md"""
        # Parse STATE.md, update position section
        pass

7. Create Generic Sub-Agents Executor

# executor.py - What sub-agents receive

class TaskExecutor:
def **init**(self, llm_client):
self.llm = llm_client
self.deviations = []

    def execute_task(self, task):
        """Execute single task with deviation handling"""

        try:
            # Attempt task execution
            result = self.run_task_action(task)

            # Apply deviation rules
            if self.is_bug(result):
                result = self.apply_rule_1(result)  # Auto-fix

            elif self.is_missing_critical(result):
                result = self.apply_rule_2(result)  # Auto-add

            elif self.is_blocking(result):
                result = self.apply_rule_3(result)  # Auto-fix blocker

            elif self.is_architectural(result):
                return self.create_checkpoint("decision", result)

            return result

        except AuthenticationError as e:
            # Dynamic checkpoint for auth gates
            return self.create_auth_checkpoint(e)

    def create_checkpoint(self, checkpoint_type, data):
        """Return structured checkpoint for orchestrator"""

        return {
            "status": "checkpoint",
            "type": checkpoint_type,
            "completed_work": self.get_completed_tasks(),
            "checkpoint_data": data
        }

8. Usage Example

python# main.py - How you'd use the system

from orchestrator import Orchestrator
from state_manager import StateManager
from llm_client import LLMClient # Your choice of LLM

# Initialize

llm = LLMClient(provider="openai", model="gpt-4") # or anthropic, local, etc.
state = StateManager(project_root="./my-project")
orchestrator = Orchestrator(llm, state)

# Execute a plan

orchestrator.execute_plan(".planning/phases/01-foundation/01-01-PLAN.md")

# Or execute entire phase

orchestrator.execute_phase(phase_number=1)
