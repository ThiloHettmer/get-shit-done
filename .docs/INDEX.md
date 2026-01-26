# Documentation Index

Complete reference for all GSD documentation.

## Getting Started

**New to GSD?** Start here:

1. **[README.md](./README.md)** - Documentation overview
   - What GSD does
   - System philosophy
   - File organization
   - Getting help

2. **[Quick Reference](./quick-reference.md)** - Cheat sheet
   - Command lookup
   - Common patterns
   - File structure
   - Troubleshooting

## Understanding GSD

**Want to understand how it works?**

### Core Documentation

3. **[Architecture](./architecture.md)** - System design
   - Component layers
   - File system structure
   - Multi-agent orchestration
   - Data flow
   - State management
   - Performance characteristics

4. **[Core Concepts](./core-concepts.md)** - Fundamental principles
   - Plans are prompts
   - Context engineering
   - Goal-backward methodology
   - Multi-agent pattern
   - Atomic commits
   - Checkpoints
   - State management
   - XML formatting
   - Progressive disclosure
   - Solo developer workflow

### Detailed References

5. **[Workflows](./workflows.md)** - Orchestration logic
   - execute-phase (wave-based execution)
   - execute-plan (single plan)
   - verify-phase (goal-backward)
   - discover-phase (research)
   - discuss-phase (capture vision)
   - verify-work (UAT)
   - diagnose-issues (debugging)
   - complete-milestone (archive)
   - map-codebase (brownfield)

6. **[XML Format](./xml-format.md)** - Prompt structure
   - Why XML?
   - Task types (auto, TDD, checkpoints)
   - Plan structure
   - Workflow patterns
   - Common tags
   - Validation rules
   - Examples

## Contributing

**Want to contribute to GSD?**

7. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development guide
   - Branch strategy
   - Commit conventions
   - Release process
   - Testing
   - Pull requests

8. **[GSD-STYLE.md](../GSD-STYLE.md)** - Coding style
   - File structure conventions
   - XML tag conventions
   - Naming patterns
   - Language & tone
   - Anti-patterns
   - Context engineering rules

## Project Files

**Main project documentation:**

9. **[README.md](../README.md)** - Main project README
   - What GSD is
   - Installation
   - Workflow overview
   - Commands
   - Configuration
   - Troubleshooting

10. **[CHANGELOG.md](../CHANGELOG.md)** - Version history
    - Release notes
    - Breaking changes
    - New features
    - Bug fixes

## By Topic

### Installation & Setup

- **Installation**: [README.md](../README.md#getting-started)
- **Configuration**: [Quick Reference](./quick-reference.md#configuration)
- **Permissions**: [README.md](../README.md#recommended-skip-permissions-mode)

### Using GSD

- **Workflow sequence**: [Quick Reference](./quick-reference.md#workflow-sequence)
- **Commands**: [Quick Reference](./quick-reference.md#commands-cheatsheet)
- **Phase execution**: [Workflows](./workflows.md#1-execute-phasemd)
- **Verification**: [Workflows](./workflows.md#3-verify-phasemd)
- **Debugging**: [Workflows](./workflows.md#7-diagnose-issuesmd)

### Understanding GSD

- **System design**: [Architecture](./architecture.md)
- **Philosophy**: [Core Concepts](./core-concepts.md)
- **Context management**: [Core Concepts](./core-concepts.md#2-context-engineering)
- **Multi-agent pattern**: [Core Concepts](./core-concepts.md#4-multi-agent-orchestration)

### Writing Plans

- **Plan structure**: [XML Format](./xml-format.md#plan-structure)
- **Task types**: [XML Format](./xml-format.md#task-types)
- **Checkpoints**: [XML Format](./xml-format.md#type-checkpointhuman-verify)
- **TDD tasks**: [XML Format](./xml-format.md#type-auto-tddtrue)

### Customizing GSD

- **Adding commands**: [Architecture](./architecture.md#adding-commands)
- **Adding agents**: [Architecture](./architecture.md#adding-agents)
- **Adding workflows**: [Architecture](./architecture.md#adding-workflows)
- **Local overrides**: [Architecture](./architecture.md#customization)

### Contributing

- **Development setup**: [CONTRIBUTING.md](../CONTRIBUTING.md#setting-up-development)
- **Branch strategy**: [CONTRIBUTING.md](../CONTRIBUTING.md#branch-strategy)
- **Commit format**: [CONTRIBUTING.md](../CONTRIBUTING.md#commits)
- **Style guide**: [GSD-STYLE.md](../GSD-STYLE.md)

## By Role

### For Users

Start here → understand workflows → reference when needed:

1. [README.md](../README.md) - Install and basic usage
2. [Quick Reference](./quick-reference.md) - Commands and patterns
3. [Workflows](./workflows.md) - Deep dive on specific workflows

### For Contributors

Understand system → learn style → start contributing:

1. [Architecture](./architecture.md) - How GSD works
2. [Core Concepts](./core-concepts.md) - Design principles
3. [GSD-STYLE.md](../GSD-STYLE.md) - Coding conventions
4. [CONTRIBUTING.md](../CONTRIBUTING.md) - Development workflow

### For Researchers

Study the meta-prompting system:

1. [Core Concepts](./core-concepts.md) - Fundamental patterns
2. [Architecture](./architecture.md) - System design
3. [XML Format](./xml-format.md) - Prompt structure
4. [Workflows](./workflows.md) - Orchestration patterns

## By Question

### "How do I...?"

| Question | Answer |
|----------|--------|
| Install GSD? | [README.md](../README.md#getting-started) |
| Start a project? | [Quick Reference](./quick-reference.md#workflow-sequence) |
| Execute a phase? | [Workflows](./workflows.md#1-execute-phasemd) |
| Debug an issue? | [Quick Reference](./quick-reference.md#troubleshooting) |
| Add a command? | [Architecture](./architecture.md#adding-commands) |
| Customize GSD? | [Quick Reference](./quick-reference.md#configuration) |

### "What is...?"

| Question | Answer |
|----------|--------|
| A plan? | [Core Concepts](./core-concepts.md#1-plans-are-prompts) |
| A wave? | [Architecture](./architecture.md#wave-based-execution) |
| A checkpoint? | [Core Concepts](./core-concepts.md#6-checkpoints) |
| Goal-backward? | [Core Concepts](./core-concepts.md#3-goal-backward-methodology) |
| Context engineering? | [Core Concepts](./core-concepts.md#2-context-engineering) |

### "Why does GSD...?"

| Question | Answer |
|----------|--------|
| Use XML? | [XML Format](./xml-format.md#why-xml) |
| Spawn agents? | [Core Concepts](./core-concepts.md#4-multi-agent-orchestration) |
| Commit per task? | [Core Concepts](./core-concepts.md#5-atomic-commits) |
| Split plans? | [Core Concepts](./core-concepts.md#2-context-engineering) |
| Use waves? | [Architecture](./architecture.md#wave-based-execution) |

### "Where is...?"

| Item | Location |
|------|----------|
| Commands? | `commands/gsd/*.md` |
| Workflows? | `get-shit-done/workflows/*.md` |
| Agents? | `agents/gsd-*.md` |
| Templates? | `get-shit-done/templates/*.md` |
| References? | `get-shit-done/references/*.md` |
| Project state? | `.planning/STATE.md` |

## Concept Map

```
GSD System
├── User Interface (Commands)
│   └── See: Quick Reference - Commands
├── Orchestration (Workflows)
│   ├── Phase execution
│   ├── Plan execution
│   └── Verification
│   └── See: Workflows
├── Execution (Agents)
│   ├── Planner
│   ├── Executor
│   ├── Verifier
│   └── Debugger
│   └── See: Architecture - Agent Types
└── State (Files)
    ├── PROJECT.md (vision)
    ├── ROADMAP.md (phases)
    ├── STATE.md (position)
    └── Plans & Summaries
    └── See: Architecture - File System
```

## Learning Path

### Path 1: User (I want to build with GSD)

```
1. Install GSD
   └─ README.md#getting-started
   
2. Understand workflow
   └─ Quick Reference#workflow-sequence
   
3. Run first project
   └─ Follow: new-project → discuss → plan → execute
   
4. Reference commands as needed
   └─ Quick Reference#commands-cheatsheet
   
5. Deep dive on specific features
   └─ Workflows (verification, debugging, etc.)
```

### Path 2: Contributor (I want to improve GSD)

```
1. Understand system design
   └─ Architecture
   
2. Learn core concepts
   └─ Core Concepts
   
3. Study coding style
   └─ GSD-STYLE.md
   
4. Set up development
   └─ CONTRIBUTING.md#setting-up-development
   
5. Make first contribution
   └─ CONTRIBUTING.md#pull-request-guidelines
```

### Path 3: Researcher (I want to study meta-prompting)

```
1. Read system overview
   └─ README.md#system-overview
   
2. Study core principles
   └─ Core Concepts
   
3. Analyze architecture
   └─ Architecture
   
4. Examine prompt structure
   └─ XML Format
   
5. Trace execution flow
   └─ Workflows
```

## Version Information

This documentation corresponds to:
- **GSD Version**: 1.9.13
- **Documentation Date**: 2026-01-26
- **Documentation Version**: 1.0.0

See [CHANGELOG.md](./CHANGELOG.md) for documentation updates.

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/glittercowboy/get-shit-done/issues)
- **Discord**: [Join Community](https://discord.gg/5JJgD5svVS)
- **Discussions**: [GitHub Discussions](https://github.com/glittercowboy/get-shit-done/discussions)

## Next Steps

Not sure where to start?

- **New user**: Start with [README.md](./README.md)
- **Quick lookup**: Go to [Quick Reference](./quick-reference.md)
- **Understanding system**: Read [Architecture](./architecture.md)
- **Contributing**: Check [CONTRIBUTING.md](../CONTRIBUTING.md)
