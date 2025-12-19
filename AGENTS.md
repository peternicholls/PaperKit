**CRITICAL: Read `.paperkit/docs/github-copilot-instructions.md` for GitHub Copilot or `.paperkit/docs/codex-instructions.md` for OpenAI Codex.**

---

## Paper Kit: Agentic Academic Style Paper Writing System

This project uses a complete **Open Agent System** for planning, researching, structuring, drafting, refining, and publishing high-quality academic specification papers in LaTeX format.

### ⚡ Quick Start

**For GitHub Copilot (VS Code):**
1. Open Copilot Chat
2. Select agent from dropdown (e.g., `paper-architect`)
3. Agent activates and presents menu

### 🧭 Source of Truth

- **Canonical definitions** live in `.paperkit/` (agents, workflows, tools, guides).
- **Derived layers** (.github/agents, .codex/prompts, AGENTS.md, COPILOT.md) mirror `.paper`.
- **Edit only in `.paper`**; regenerate or sync external layers to avoid drift.

**For OpenAI Codex:**
1. Type `/paper-` to see available prompts
2. Select prompt (e.g., `/paper-architect`)
3. Agent activates and presents menu

### 🎯 Ten Specialized Agents

#### Core Paper Writing Agents

| Agent | Persona | Purpose | Trigger |
|-------|---------|---------|---------|
| 🔬 **Research Consolidator** | Alex | Synthesize research into coherent documents | `paper-research-consolidator` |
| 🏗️ **Paper Architect** | Morgan | Design paper structure and outline | `paper-architect` |
| ✍️ **Section Drafter** | Jordan | Write individual sections with rigor | `paper-section-drafter` |
| 💎 **Quality Refiner** | Riley | Improve clarity, flow, and polish | `paper-quality-refiner` |
| 📚 **Reference Manager** | Harper | Academic bibliographer - Harvard citations & validation | `paper-reference-manager` |
| 🔧 **LaTeX Assembler** | Taylor | Integrate sections and compile PDF | `paper-latex-assembler` |

#### Specialist Support Agents

| Agent | Persona | Purpose | Trigger |
|-------|---------|---------|---------|
| 🧠 **Brainstorm Coach** | Carson | Creative ideation and exploration | `paper-brainstorm` |
| 🔬 **Problem Solver** | Quinn | Analyze blockers and find solutions | `paper-problem-solver` |
| 🎓 **Review Tutor** | Sage | Constructive feedback on drafts | `paper-tutor` |
| 📖 **Research Librarian** | Ellis | Forensic audit: extract quotable evidence with section mapping | `paper-librarian` |

### 📊 Quick Reference Table

| You say... | Agent | Output Location |
|-----------|-------|-----------------|
| "Research X" | Research Consolidator | `.paperkit/data/output-refined/research/` |
| "Outline the paper" | Paper Architect | `.paperkit/data/output-drafts/outlines/` |
| "Draft section Y" | Section Drafter | `.paperkit/data/output-drafts/sections/` |
| "Refine this" | Quality Refiner | `.paperkit/data/output-refined/sections/` |
| "Validate citations" | Reference Manager | `latex/references/references.bib` |
| "Format bibliography" | Reference Manager | `.paperkit/data/output-refined/references/` |
| "Build the document" | LaTeX Assembler | `.paperkit/data/output-final/pdf/` |
| "Brainstorm ideas" | Brainstorm Coach | `planning/YYYYMMDD-[name]/` |
| "I'm stuck on..." | Problem Solver | `planning/YYYYMMDD-[name]/` |
| "Review this draft" | Review Tutor | `planning/YYYYMMDD-[name]/` |
| "Find sources for..." | Research Librarian | `planning/YYYYMMDD-[name]/` |

### 📁 Directory Structure

```
.paperkit/                           ← Main agent system container
├── _cfg/                         ← Configuration and manifests
│   ├── manifest.yaml            ← System version info
│   ├── agent-manifest.yaml      ← All agents catalog
│   ├── workflow-manifest.yaml   ← All workflows catalog
│   ├── tool-manifest.yaml       ← All tools catalog
│   ├── agents/                  ← Individual agent definitions (YAML)
│   ├── workflows/               ← Individual workflow definitions (YAML)
│   ├── tools/                   ← Individual tool definitions (YAML)
│   ├── guides/                  ← Style guides (Harvard citation guide)
│   ├── schemas/                 ← JSON Schemas for validation
│   └── ides/                    ← IDE-specific configs
│
├── core/                         ← Core paper writing module
│   ├── config.yaml              ← Module configuration
│   └── agents/                  ← Agent definitions
│
├── specialist/                   ← Support agents module
│   ├── config.yaml
│   └── agents/
│
├── tools/                        ← Tool implementations
│   ├── build-latex.sh
│   ├── lint-latex.sh
│   ├── extract-evidence.sh
│   └── *.py
│
├── docs/                         ← IDE instructions
│   ├── github-copilot-instructions.md
│   └── codex-instructions.md
│
└── data/                         ← All outputs
    ├── output-drafts/
    ├── output-refined/
    └── output-final/

.github/agents/                   ← GitHub Copilot chat modes
├── paper-*.agent.md             ← One per agent

.codex/prompts/                   ← OpenAI Codex prompts
├── paper-*.md                   ← One per agent

latex/                            ← Final LaTeX document
├── main.tex
├── sections/
└── references/

open-agents/                      ← Legacy system (deprecated)
```

### 🎯 Typical Workflow

1. **Define scope** → Use Paper Architect to outline
2. **Research** → Use Research Consolidator + Librarian
3. **Structure** → Paper Architect creates outline and LaTeX skeleton
4. **Draft** → Section Drafter writes one section at a time
5. **Get Feedback** → Review Tutor provides critique
6. **Refine** → Quality Refiner improves each section
7. **Validate Refs** → Reference Manager validates citations (Harvard style)
8. **Assemble** → LaTeX Assembler compiles final PDF

### 🛡️ Academic Integrity

- Academic integrity is paramount—always use reputable sources and Harvard-style citations.
- Never summarize or quote without attribution; include quote text, page number, and full citation.
- Use open access channels when downloading papers; never fabricate or guess citations.

### 🛠️ Tools Available

```bash
# Build and compile LaTeX document
./.paperkit/tools/build-latex.sh

# Check LaTeX syntax before compilation
./.paperkit/tools/lint-latex.sh

# Validate paper structure
python3 ./.paperkit/tools/validate-structure.py

# Extract evidence from PDFs (forensic audit)
./.paperkit/tools/extract-evidence.sh <pdf_dir> <output_md> [terms...]
```

### 📚 Citation Workflows

The Reference Manager (Harper) supports comprehensive citation management:

| Workflow | Description |
|----------|-------------|
| `extract-citations` | Extract all citations from LaTeX files |
| `validate-citations` | Validate citations against BibTeX database |
| `citation-completeness` | Check all required BibTeX fields |
| `format-bibliography` | Format bibliography in Harvard style |

### 🧪 Forensic Audit Protocol (Rigor)

- Apply PhD-level rigor across agents; revisit previously processed sources to uncover deeper quotes, validations, and philosophical framing.
- Prioritize quantitative anchors and exact quotations with page numbers.
- Map every extracted finding to paper sections (§02–§12).
- Artifact paths for audited materials:
    - `open-agents/planning/20251218-group-tutor-reviews/tasks-artifacts`
    - `open-agents/planning/20251218-group-tutor-reviews/research-artifacts`
- Tooling: `open-agents/tools/extract-evidence.sh` for batch `pdftotext` + `grep` extraction.

### 📖 Documentation

| Document | Purpose |
|----------|---------|
| `.paperkit/docs/github-copilot-instructions.md` | VS Code Copilot usage |
| `.paperkit/docs/codex-instructions.md` | OpenAI Codex usage |
| `.paperkit/_cfg/agent-manifest.yaml` | Complete agent catalog |
| `.paperkit/_cfg/workflow-manifest.yaml` | Complete workflow catalog |
| `.paperkit/_cfg/tool-manifest.yaml` | Complete tool catalog |
| `.paperkit/_cfg/guides/harvard-citation-guide.md` | Harvard citation style guide |
| `SYSTEM-PLANNING/SYSTEM_GUIDE.md` | System overview |
| `open-agents/INSTRUCTIONS.md` | Legacy full documentation |

### ✨ Key Features

✓ **10 specialized agents** for the complete paper workflow  
✓ **Multi-IDE support** - GitHub Copilot and OpenAI Codex  
✓ **Progressive disclosure** - agents load on demand  
✓ **Menu-driven interaction** - each agent presents options  
✓ **Modular LaTeX architecture** - atomic sections  
✓ **Harvard citation style** (Cite Them Right) with validation  
✓ **Citation workflows** - extract, validate, format, check completeness  
✓ **Configuration per module** - customize behavior  
✓ **Agent manifest** - discover all available agents  

### 🚀 Next Step

1. Open GitHub Copilot Chat in VS Code
2. Select `paper-architect` from the agent dropdown
3. Say "Create an outline for my paper on [topic]"
