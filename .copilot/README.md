# Copilot Research Paper Assistant Kit

**Configuration-driven system for academic paper research and writing.**

This directory contains the system configuration, agents, commands, workflows, and memory files that power the Copilot Research Paper Assistant.

## Directory Structure

```
.copilot/
├── README.md              ← You are here
├── agents.yaml            ← Master agent registry
├── commands.yaml          ← Master command registry
├── workflows.yaml         ← Master workflow registry
│
├── agents/                ← Agent specifications
│   ├── core/              ← Core paper writing agents
│   ├── specialist/        ← Support agents (brainstorm, tutor, etc.)
│   └── README.md
│
├── commands/              ← Command specifications
│   └── paper/             ← Paper-related commands
│
├── workflows/             ← Workflow definitions
│   ├── setup/             ← Initialization workflows
│   ├── sprint/            ← Sprint planning workflows
│   └── paper/             ← Core writing workflows
│
├── memory/                ← System-managed state (protected)
│   ├── paper-metadata.yaml
│   ├── research-index.yaml
│   ├── section-status.yaml
│   ├── working-reference.md
│   └── revision-log.md
│
├── config/                ← Configuration files
│   ├── settings.yaml      ← System settings
│   └── consent.yaml       ← Consent policies
│
├── tools/                 ← Tool registry
│   └── tools.yaml         ← Tool specifications
│
└── modules/               ← Future extensibility
    └── README.md
```

## Quick Start

### For Users

1. **Start a new paper:** Say "init paper" or use \`/paper.init\`
2. **Research a topic:** "Research [topic]" or \`/paper.research\`
3. **Draft a section:** "Draft introduction" or \`/paper.draft\`
4. **Refine writing:** "Refine this draft" or \`/paper.refine\`
5. **Build document:** "Assemble paper" or \`/paper.assemble\`

### For System Understanding

- **Agents:** See [agents/README.md](agents/README.md) for how agents work
- **Commands:** See [commands/README.md](commands/README.md) for available commands
- **Workflows:** See [workflows/README.md](workflows/README.md) for orchestration
- **Memory:** See [memory/README.md](memory/README.md) for state management

## Master Registries

### agents.yaml
Single source of truth for all agent definitions, capabilities, and routing.

### commands.yaml
Maps user commands (slash commands, natural language) to agents.

### workflows.yaml
Defines orchestration sequences for multi-step processes.

## Key Concepts

### Agents
Specialized roles that handle different aspects of paper writing:
- **Research Consolidator:** Synthesizes research materials
- **Paper Architect:** Designs paper structure
- **Section Drafter:** Writes individual sections
- **Quality Refiner:** Improves drafts
- **Reference Manager:** Manages citations
- **LaTeX Assembler:** Builds final document

### Workflows
Orchestrated sequences that guide the paper writing process:
- **Initialization:** Set up project goals and structure
- **Sprint:** Focused work sessions with planning and review
- **Core Writing:** Plan → Research → Draft → Refine → Assemble

### Memory
System-managed files that track project state:
- Paper metadata (title, scope, audience)
- Research index (consolidated sources)
- Section status (draft/refined/complete)
- Working reference (session handoff)

## Consent Gate

Tools requiring file modifications need user consent:
- **Allow once:** Single execution
- **Allow for session:** Current chat session
- **Allow for workspace:** This workspace permanently
- **Always allow:** Global machine-level approval

Consent log: \`.vscode/agent-consent.log\` (gitignored)

## Tools Integration

Tools are registered in \`tools/tools.yaml\`:
- **build-latex.sh:** Compile LaTeX to PDF
- **lint-latex.sh:** Check LaTeX syntax
- **validate-structure.py:** Validate paper structure
- **format-references.py:** Format bibliography

## Design Principles

1. **Configuration-driven:** All behavior defined in YAML files
2. **Modular architecture:** Agents, commands, workflows are independent
3. **Protected state:** Memory files are system-managed
4. **Progressive disclosure:** Complexity revealed as needed
5. **BMAD-inspired:** Follows proven agent orchestration patterns

## Extending the System

To add new capabilities:
1. Create agent YAML in \`agents/specialist/\`
2. Register in \`agents.yaml\`
3. Create command YAML in \`commands/paper/\`
4. Register in \`commands.yaml\`
5. Update workflows if needed

---

**Version:** 1.0.0  
**System Name:** Copilot Research Paper Assistant Kit
