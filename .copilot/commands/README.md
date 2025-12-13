# Command Specifications

This directory contains YAML specifications for all slash commands and natural language triggers.

## Organization

```
commands/
├── README.md     ← You are here
└── paper/        ← Paper-related commands
    ├── init.yaml
    ├── objectives.yaml
    ├── requirements.yaml
    ├── spec.yaml
    ├── plan.yaml
    ├── sprint-plan.yaml
    ├── tasks.yaml
    ├── review.yaml
    ├── research.yaml
    ├── draft.yaml
    ├── refine.yaml
    ├── refs.yaml
    ├── assemble.yaml
    └── specialist/
        ├── brainstorm.yaml
        ├── solve.yaml
        ├── tutor-feedback.yaml
        ├── librarian-research.yaml
        ├── librarian-sources.yaml
        └── librarian-gaps.yaml
```

## Command Categories

### Setup Commands
Initialize project and create canonical documents:

| Command | Display | Agent |
|---------|---------|-------|
| `/paper.init` | Init session / capture goals | paper-architect |
| `/paper.objectives` | Set aims & objectives | paper-architect |
| `/paper.requirements` | Set technical requirements | paper-architect |
| `/paper.spec` | Set content specification | paper-architect |

### Sprint Commands
Plan and manage focused work sessions:

| Command | Display | Agent |
|---------|---------|-------|
| `/paper.sprint-plan` | Plan a sprint | paper-architect |
| `/paper.tasks` | Manage sprint tasks | paper-system |
| `/paper.review` | Review sprint | paper-system |

### Core Writing Commands
The main paper writing workflow:

| Command | Display | Agent |
|---------|---------|-------|
| `/paper.plan` | Plan paper outline | paper-architect |
| `/paper.research` | Research & consolidate | research-consolidator |
| `/paper.draft` | Draft section | section-drafter |
| `/paper.refine` | Refine section | quality-refiner |
| `/paper.refs` | Manage references | reference-manager |
| `/paper.assemble` | Assemble & compile | latex-assembler |

### Specialist Commands
Support for specific tasks:

| Command | Display | Agent |
|---------|---------|-------|
| `/paper.brainstorm` | Brainstorm | brainstorm |
| `/paper.solve` | Solve problem | problem-solver |
| `/paper.tutor-feedback` | Get tutor feedback | tutor |
| `/paper.librarian-research` | Find sources | librarian |
| `/paper.librarian-sources` | Track sources | librarian |
| `/paper.librarian-gaps` | Identify gaps | librarian |

## Command YAML Structure

Each command YAML file includes:

```yaml
name: "paper.command-name"
display-name: "Human Readable Display"
description: "What this command does"
category: "setup|sprint|core|specialist"
version: "1.0"

entry-points:
  primary: "/paper.command-name"
  alternates:
    - "natural language trigger"
    - "*short-form"

routing:
  primary-agent: "agent-name"
  workflow: "workflow-name"
  load-order:
    - "open-agents/INSTRUCTIONS.md"
    - "open-agents/agents/agent_spec.md"

inputs:
  parameter-name:
    type: "string|choice|boolean"
    required: true|false
    default: "default-value"
    options:  # for choice type
      - "option1"
      - "option2"

outputs:
  files:
    - "path/to/output.md"
  memory:
    - "working-reference.md (updated)"

consent-required: true|false
tools-used:
  - "tool-name.sh"

behavioral-rules:
  - "Behavior rule 1"
  - "Behavior rule 2"

success-criteria:
  - "Criterion 1"
  - "Criterion 2"
```

## Adding a New Command

1. Create YAML file in `paper/` or `paper/specialist/`
2. Follow the structure template above
3. Register in `.copilot/commands.yaml` master registry
4. Ensure agent exists for routing
5. Update workflow if command is part of a sequence
