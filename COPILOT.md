## Paper Kit: Agentic Academic Style Paper Writing System — GitHub Copilot Integration

This repo includes Copilot agent and slash-command scaffolding that routes into the Open Agent System with 10 specialized agents.

### Entry Points

- **Chat Modes**: Select agent from Copilot Chat dropdown (e.g., `paper-architect`)
- **Agent definitions**: Located in [.github/agents/](.github/agents/) with one file per agent
- **Full system config**: [.copilot/agents.yaml](.copilot/agents.yaml) defines all agents and their capabilities

### Source of Truth

- **Canonical definitions are in `.paperkit/`** (agents, workflows, tools).
- **Do not edit** `.github/agents` or `.codex/prompts` independently; they are generated from `.paperkit/`.
- **Keep in sync** by running `./paperkit generate` after changes in `.paperkit/`.

### Ten Specialized Agents

#### Core Paper Writing Agents
| Command | Agent | Purpose |
|---------|-------|---------|
| `paper-research-consolidator` | Research Consolidator (Alex) | Research Consolidator |
| `paper-architect` | Paper Architect (Morgan) | Paper Architect |
| `paper-section-drafter` | Section Drafter (Jordan) | Section Drafter |
| `paper-quality-refiner` | Quality Refiner (Riley) | Quality Refiner |
| `paper-reference-manager` | Academic Bibliographer & Reference Specialist (Harper) | Academic Bibliographer & Reference Specialist |
| `paper-latex-assembler` | LaTeX Assembler (Taylor) | LaTeX Assembler |

#### Specialist Support Agents
| Command | Agent | Purpose |
|---------|-------|---------|
| `paper-brainstorm` | Brainstorm Coach (Carson) | Brainstorm Coach |
| `paper-problem-solver` | Problem Solver (Quinn) | Problem Solver |
| `paper-tutor` | Review Tutor (Sage) | Review Tutor |
| `paper-librarian` | Research Librarian — Forensic Audit (Ellis) | Research Librarian — Forensic Audit |

### Slash Commands
- `/paper.init` → Initialize and update working reference
- `/paper.plan` → Paper Architect - outline and structure
- `/paper.research` → Research Consolidator - synthesize sources
- `/paper.draft` → Section Drafter - write sections
- `/paper.refine` → Quality Refiner - improve drafts
- `/paper.refs` → Reference Manager - manage citations
- `/paper.assemble` → LaTeX Assembler - compile PDF

### Reference Manager Workflows

The Reference Manager (Harper) supports comprehensive Harvard-style citation management:

| Workflow | Description |
|----------|-------------|
| `extract-citations` | Extract all citations from LaTeX sections |
| `validate-citations` | Validate against BibTeX database |
| `citation-completeness` | Check required fields for all entries |
| `format-bibliography` | Format in Harvard style (Cite Them Right) |

### Activation Protocol

Each agent follows this protocol when activated:

1. **Load Definition**: Agent loads its full definition from `.paperkit/{module}/agents/{name}.md`
2. **Load Config**: Reads module configuration from `.paperkit/{module}/config.yaml`
3. **Initialize Context**: Sets up working memory and resources
4. **Present Menu**: Displays interactive menu with available workflows
5. **Process Commands**: Responds to user input following persona and workflows

### Configuration

Agents are configured at two levels:

1. **Module Config**: `.paperkit/core/config.yaml` and `.paperkit/specialist/config.yaml`
2. **Agent Metadata**: `.paperkit/_cfg/agents/{agent-name}.yaml`

### Output Locations

| Agent | Primary Output Path |
|-------|---------------------|
| Research Consolidator | `.paperkit/data/output-refined/research/` |
| Paper Architect | `.paperkit/data/output-drafts/outlines/` |
| Section Drafter | `.paperkit/data/output-drafts/sections/` |
| Quality Refiner | `.paperkit/data/output-refined/sections/` |
| Reference Manager | `latex/references/references.bib` |
| LaTeX Assembler | `.paperkit/data/output-final/pdf/` |
| Brainstorm Coach | `planning/YYYYMMDD-session-name/` |
| Problem Solver | `planning/YYYYMMDD-session-name/` |
| Review Tutor | `planning/YYYYMMDD-session-name/` |
| Research Librarian | `planning/YYYYMMDD-session-name/` |

### Quick Commands

```bash
# Generate IDE files from source
./paperkit generate

# Validate agent/workflow/tool definitions
./paperkit validate

# Build LaTeX document
./.paperkit/tools/build-latex.sh

# Lint LaTeX before compilation
./.paperkit/tools/lint-latex.sh
```

### Academic Integrity

All agents follow strict academic integrity protocols:

- **Citation Required**: Every quote needs text, page number, and full citation
- **Harvard Style**: Cite Them Right format (author-date system)
- **Source Verification**: Only reputable academic sources and open access channels
- **No Fabrication**: Never guess or make up citations; flag uncertainties

---

*This file is auto-generated from `.paperkit/` manifests. Run `./paperkit generate` to regenerate.*
