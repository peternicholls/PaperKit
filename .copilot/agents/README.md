# Agent Specifications

This directory contains YAML specifications for all agents in the system.

## Organization

```
agents/
├── README.md         ← You are here
├── paper-system.yaml ← System router agent
├── core/             ← Core paper writing agents
│   ├── research-consolidator.yaml
│   ├── paper-architect.yaml
│   ├── section-drafter.yaml
│   ├── quality-refiner.yaml
│   ├── reference-manager.yaml
│   └── latex-assembler.yaml
└── specialist/       ← Support agents
    ├── brainstorm.yaml
    ├── problem-solver.yaml
    ├── tutor.yaml
    └── librarian.yaml
```

## Agent Categories

### Core Agents
The six core agents that handle the main paper writing workflow:

| Agent | Role | Purpose |
|-------|------|---------|
| Research Consolidator | Synthesizer | Synthesize research into reference docs |
| Paper Architect | Architect | Design structure and outline |
| Section Drafter | Writer | Write individual sections |
| Quality Refiner | Editor | Improve drafts for quality |
| Reference Manager | Bibliographer | Manage citations and bibliography |
| LaTeX Assembler | Engineer | Build final document |

### Specialist Agents
Support agents for specific tasks:

| Agent | Role | Purpose |
|-------|------|---------|
| Brainstorm | Idea Generator | Explore ideas creatively |
| Problem-Solver | Problem Solver | Analyze and solve blockers |
| Tutor | Mentor | Provide feedback on drafts |
| Librarian | Research Guide | Find and evaluate sources |

### System Agents
Internal agents for orchestration:

| Agent | Role | Purpose |
|-------|------|---------|
| Paper System | Orchestrator | Route commands, manage consent |

## Agent YAML Structure

Each agent YAML file includes:

```yaml
name: "agent-name"
display-name: "Human Readable Name"
description: "What this agent does"
role: "Role Name"
category: "category"
version: "1.0"

personality:
  tone: "Academic but accessible"
  style: "Objective and narrative-driven"
  expertise: "Relevant expertise areas"

capabilities:
  primary: "Main capability"
  secondary:
    - "Additional capability 1"
    - "Additional capability 2"

triggers:
  commands:
    - "command pattern 1"
    - "command pattern 2"
  intents:
    - "When user wants X"

inputs:
  required:
    - input-name: "Description"
  optional:
    - optional-input: "Description"

outputs:
  primary:
    - path: "output/path/"
      format: "markdown|yaml|tex"
  secondary:
    - path: "memory/file.yaml"
      action: "update"

behavioral-rules:
  - "Rule 1"
  - "Rule 2"

collaboration-hints:
  works-well-with:
    - "other-agent"
  receives-input-from:
    - "upstream-agent"
  provides-input-to:
    - "downstream-agent"
```

## Adding a New Agent

1. Create YAML file in appropriate folder (`core/` or `specialist/`)
2. Follow the structure template above
3. Register in `.copilot/agents.yaml` master registry
4. Create corresponding command if needed
5. Update documentation

## Documentation Reference

Full agent documentation is in `open-agents/agents/`:
- [research_consolidator.md](../../open-agents/agents/research_consolidator.md)
- [paper_architect.md](../../open-agents/agents/paper_architect.md)
- [section_drafter.md](../../open-agents/agents/section_drafter.md)
- [quality_refiner.md](../../open-agents/agents/quality_refiner.md)
- [reference_manager.md](../../open-agents/agents/reference_manager.md)
- [latex_assembler.md](../../open-agents/agents/latex_assembler.md)
