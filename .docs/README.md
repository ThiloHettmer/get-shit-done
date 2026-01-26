# Get Shit Done - Technical Documentation

**Version:** 1.9.13  
**Type:** Meta-prompting, context engineering, and spec-driven development system  
**Target:** Claude Code & OpenCode

## About This Documentation

This documentation provides a comprehensive technical reference for the Get Shit Done (GSD) system. It's intended for:

- Contributors working on GSD itself
- Advanced users wanting to understand the internal architecture
- Developers creating extensions or modifications
- Anyone interested in meta-prompting systems for AI coding assistants

## Documentation Structure

### Core Documentation

- **[Architecture](./architecture.md)** - System design, components, and interactions
- **[Core Concepts](./core-concepts.md)** - Fundamental principles and patterns
- **[Workflows](./workflows.md)** - Detailed workflow explanations
- **[Commands](./commands.md)** - Complete command reference
- **[Agents](./agents.md)** - Specialized AI agent system

### Reference Material

- **[Templates](./templates.md)** - File templates and structure
- **[XML Format](./xml-format.md)** - XML schema and conventions
- **[Git Integration](./git-integration.md)** - Commit patterns and history
- **[Configuration](./configuration.md)** - Settings and customization

### Development

- **[Contributing](./contributing.md)** - Development setup and guidelines
- **[Installation](./installation.md)** - Installation system mechanics
- **[Testing](./testing.md)** - Testing approaches and patterns

## Quick Start for Contributors

1. **Read**: [Architecture](./architecture.md) to understand the system design
2. **Review**: [Core Concepts](./core-concepts.md) for fundamental patterns
3. **Study**: [GSD-STYLE.md](../GSD-STYLE.md) for coding conventions
4. **Check**: [CONTRIBUTING.md](../CONTRIBUTING.md) for workflow

## System Overview

### What GSD Does

GSD solves **context rot** - the quality degradation that happens as Claude fills its context window. It does this through:

1. **Context Engineering** - Structured file management and size constraints
2. **Multi-Agent Orchestration** - Fresh context windows for execution
3. **Atomic Task Execution** - Small, verifiable units of work
4. **State Management** - Project memory across sessions

### Key Design Principles

```
Plans are Prompts → PLAN.md files execute directly, not transformed
Fresh Context → Subagents get 200k tokens each, zero degradation  
Atomic Commits → Each task = one commit, full git history
Goal-Backward → Derive requirements from desired outcomes
Solo Developer → No enterprise patterns, just you + Claude
```

### Architecture Layers

```
┌─────────────────────────────────────────────────┐
│  User Interface (Slash Commands)                │
│  /gsd:new-project, /gsd:execute-phase, etc.    │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Orchestrators (Thin Coordination Layer)        │
│  Discover → Validate → Spawn → Collect          │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  Specialized Agents (Autonomous Execution)      │
│  Planner → Executor → Verifier → Debugger       │
└─────────────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────┐
│  State Management (.planning/ directory)        │
│  PROJECT.md, ROADMAP.md, STATE.md, Plans, etc. │
└─────────────────────────────────────────────────┘
```

## Philosophy

From the README:

> "The complexity is in the system, not in your workflow."

GSD is designed for **solo developers** building with Claude. It avoids:

- ❌ Enterprise patterns (sprint ceremonies, story points, RACI matrices)
- ❌ Team coordination overhead
- ❌ Human time estimates (hours, days, weeks)
- ❌ Documentation theater
- ❌ Vague abstractions

Instead it focuses on:

- ✅ Executable specifications
- ✅ Automated verification
- ✅ Clean git history
- ✅ Fast iteration
- ✅ Working software

## Context Engineering

GSD manages Claude's context budget deliberately:

| Context Usage | Quality | State |
|---------------|---------|-------|
| 0-30% | PEAK | Thorough, comprehensive |
| 30-50% | GOOD | Confident, solid |
| 50-70% | DEGRADING | Efficiency mode begins |
| 70%+ | POOR | Rushed, minimal |

**The rule:** Stop BEFORE quality degrades. Keep plans under 50% context usage.

## File Organization

```
your-project/
├── .planning/                    # GSD state (can be gitignored)
│   ├── PROJECT.md               # Project vision & requirements
│   ├── ROADMAP.md               # Phase breakdown
│   ├── STATE.md                 # Current position & decisions
│   ├── REQUIREMENTS.md          # Detailed requirements
│   ├── config.json              # GSD settings
│   ├── codebase/                # Codebase analysis (brownfield)
│   ├── phases/                  # Phase directories
│   │   └── 01-foundation/
│   │       ├── 01-01-PLAN.md    # Executable plan
│   │       ├── 01-01-SUMMARY.md # Completion summary
│   │       ├── 01-CONTEXT.md    # User decisions
│   │       └── 01-RESEARCH.md   # Discovery findings
│   └── quick/                   # Quick mode tasks
└── .claude/                     # Claude Code config
    ├── commands/gsd/            # Slash commands
    ├── agents/                  # Agent definitions
    └── get-shit-done/           # GSD runtime files
```

## Workflow Overview

```mermaid
graph TD
    A[/gsd:new-project] --> B[Discovery & Requirements]
    B --> C[Create ROADMAP.md]
    C --> D[/gsd:discuss-phase N]
    D --> E[/gsd:plan-phase N]
    E --> F[/gsd:execute-phase N]
    F --> G[/gsd:verify-work N]
    G --> H{More phases?}
    H -->|Yes| D
    H -->|No| I[/gsd:complete-milestone]
    I --> J[/gsd:new-milestone]
    J --> D
```

Each phase follows: **discuss → plan → execute → verify**

## Getting Help

- **Issues**: Bug reports and feature requests at [GitHub](https://github.com/glittercowboy/get-shit-done/issues)
- **Discord**: [Join the community](https://discord.gg/5JJgD5svVS)
- **Documentation**: This directory
- **Code**: Read [GSD-STYLE.md](../GSD-STYLE.md) for implementation patterns

## Next Steps

- New to GSD? Start with [Architecture](./architecture.md)
- Contributing? Read [Contributing](./contributing.md)
- Deep dive? Check [Core Concepts](./core-concepts.md)
