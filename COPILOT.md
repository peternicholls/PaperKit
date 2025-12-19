## Paper Kit: Agentic Academic Style Paper Writing System — GitHub Copilot Integration

This repo includes Copilot agent and slash-command scaffolding that routes into the Open Agent System with 10 specialized agents.

### Entry Points

- **Chat Modes**: Select agent from Copilot Chat dropdown (e.g., `paper-architect`)
- **Agent definitions**: Located in [.github/agents/](.github/agents/) with one file per agent
- **Full system config**: [.copilot/agents.yaml](.copilot/agents.yaml) defines all agents and their capabilities

### Source of Truth

- **Canonical definitions are in `.paperkit/`** (agents, workflows, tools).
- **Do not edit** `.github/agents` or `.codex/prompts` independently; they derive from `.paper`.
- **Keep in sync** by regenerating derived layers after changes in `.paper`.

### Ten Specialized Agents

#### Core Paper Writing Agents
| Command | Agent | Purpose |
|---------|-------|---------|
| `paper-research-consolidator` | Research Consolidator (Alex) | Synthesize research into coherent documents |
| `paper-architect` | Paper Architect (Morgan) | Design paper structure and outline |
| `paper-section-drafter` | Section Drafter (Jordan) | Write individual sections with rigor |
| `paper-quality-refiner` | Quality Refiner (Riley) | Improve clarity, flow, and polish |
| `paper-reference-manager` | Reference Manager (Harper) | Harvard citations & bibliography validation |
| `paper-latex-assembler` | LaTeX Assembler (Taylor) | Integrate sections and compile PDF |

#### Specialist Support Agents
| Command | Agent | Purpose |
|---------|-------|---------|
| `paper-brainstorm` | Brainstorm Coach (Carson) | Creative ideation and exploration |
| `paper-problem-solver` | Problem Solver (Quinn) | Analyze blockers and find solutions |
| `paper-tutor` | Review Tutor (Sage) | Constructive feedback on drafts |
| `paper-librarian` | Research Librarian (Ellis) | Forensic audit: extract quotable evidence with section mapping |

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
| `extract-citations` | Extract all citations from LaTeX files |
| `validate-citations` | Validate citations against BibTeX database |
| `citation-completeness` | Check all required BibTeX fields |
| `format-bibliography` | Format bibliography in Harvard style |

### Artifacts & Rigor

- Apply PhD-level rigor across agents. Revisit already processed sources; valuable quotes and validations often emerge on a second pass.
- Artifact paths used by Librarian/Consolidator/Drafter/Refiner:
	- `open-agents/planning/20251218-group-tutor-reviews/tasks-artifacts`
	- `open-agents/planning/20251218-group-tutor-reviews/research-artifacts`
- Direct quotes must include page numbers via `\cite[p. <page>]{key}`.
- Tooling: `open-agents/tools/extract-evidence.sh` — batch evidence extraction using `pdftotext` + `grep` with context.

### Tools Available

| Tool | Path | Purpose |
|------|------|---------|
| Build LaTeX | `open-agents/tools/build-latex.sh` | Compile document to PDF |
| Lint LaTeX | `open-agents/tools/lint-latex.sh` | Check LaTeX syntax |
| Validate Structure | `open-agents/tools/validate-structure.py` | Validate paper structure |
| Format References | `open-agents/tools/format-references.py` | Format Harvard citations |

### Configuration Files

| File | Purpose |
|------|---------|
| `.paperkit/_cfg/agent-manifest.yaml` | All agents catalog |
| `.paperkit/_cfg/workflow-manifest.yaml` | All workflows catalog |
| `.paperkit/_cfg/tool-manifest.yaml` | All tools catalog |
| `.paperkit/_cfg/guides/harvard-citation-guide.md` | Harvard citation style guide |
| `.paperkit/_cfg/resources/citation-rules.yaml` | Citation validation rules |

### Consent Gate (Tools)

Before running tools that modify files:
1. Prompt for scope: Allow once / Allow for session / Allow for workspace / Always allow
2. Store scope in VS Code `workspaceState` or `globalState`
3. Optional local log (gitignored): `.vscode/agent-consent.log`

### Output Directories

| Output Type | Location |
|-------------|----------|
| Draft sections | `.paperkit/data/output-drafts/sections/` |
| Refined sections | `.paperkit/data/output-refined/sections/` |
| Final PDF | `.paperkit/data/output-final/pdf/` |
| BibTeX database | `latex/references/references.bib` |

### Notes

- **Progressive disclosure**: Agents load only their specific configuration on demand
- **Menu-driven**: Each agent presents an interactive menu of options
- **Handoff support**: Working reference at `open-agents/memory/working-reference.md` maintains context

### Academic Integrity

- Academic integrity is paramount—use reputable sources and proper Harvard-style citations.
- Never summarize or quote academic papers without attribution; every quote needs text, page number, and full citation.
- Use open access channels when downloading papers; do not fabricate or guess citations.
