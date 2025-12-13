**CRITICAL: Read `.paper/docs/github-copilot-instructions.md` for GitHub Copilot or `.paper/docs/codex-instructions.md` for OpenAI Codex.**

---

## Paper Kit: Agentic Academic Style Paper Writing System

This project uses a complete **Open Agent System** for planning, researching, structuring, drafting, refining, and publishing high-quality academic specification papers in LaTeX format.

### ⚡ Quick Start

**For GitHub Copilot (VS Code):**
1. Open Copilot Chat
2. Select agent from dropdown (e.g., `paper-architect`)
3. Agent activates and presents menu

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
| 📚 **Reference Manager** | Harper | Manage citations and bibliography | `paper-reference-manager` |
| 🔧 **LaTeX Assembler** | Taylor | Integrate sections and compile PDF | `paper-latex-assembler` |

#### Specialist Support Agents

| Agent | Persona | Purpose | Trigger |
|-------|---------|---------|---------|
| 🧠 **Brainstorm Coach** | Carson | Creative ideation and exploration | `paper-brainstorm` |
| 🔬 **Problem Solver** | Quinn | Analyze blockers and find solutions | `paper-problem-solver` |
| 🎓 **Review Tutor** | Sage | Constructive feedback on drafts | `paper-tutor` |
| 📖 **Research Librarian** | Ellis | Find and organize sources | `paper-librarian` |

### 📊 Quick Reference Table

| You say... | Agent | Output Location |
|-----------|-------|-----------------|
| "Research X" | Research Consolidator | `.paper/data/output-refined/research/` |
| "Outline the paper" | Paper Architect | `.paper/data/output-drafts/outlines/` |
| "Draft section Y" | Section Drafter | `.paper/data/output-drafts/sections/` |
| "Refine this" | Quality Refiner | `.paper/data/output-refined/sections/` |
| "Manage citations" | Reference Manager | `latex/references/references.bib` |
| "Build the document" | LaTeX Assembler | `.paper/data/output-final/pdf/` |
| "Brainstorm ideas" | Brainstorm Coach | `planning/YYYYMMDD-[name]/` |
| "I'm stuck on..." | Problem Solver | `planning/YYYYMMDD-[name]/` |
| "Review this draft" | Review Tutor | `planning/YYYYMMDD-[name]/` |
| "Find sources for..." | Research Librarian | `planning/YYYYMMDD-[name]/` |

### 📁 Directory Structure

```
.paper/                           ← Main agent system container
├── _cfg/                         ← Configuration and manifests
│   ├── manifest.yaml            ← System version info
│   ├── agent-manifest.csv       ← All agents catalog
│   ├── workflow-manifest.csv    ← All workflows catalog
│   ├── tool-manifest.csv        ← All tools catalog
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

open-agents/                      ← Legacy system (preserved)
```

### 🎯 Typical Workflow

1. **Define scope** → Use Paper Architect to outline
2. **Research** → Use Research Consolidator + Librarian
3. **Structure** → Paper Architect creates outline and LaTeX skeleton
4. **Draft** → Section Drafter writes one section at a time
5. **Get Feedback** → Review Tutor provides critique
6. **Refine** → Quality Refiner improves each section
7. **Manage Refs** → Reference Manager validates citations
8. **Assemble** → LaTeX Assembler compiles final PDF

### 🛠️ Tools Available

```bash
# Build and compile LaTeX document
./open-agents/tools/build-latex.sh

# Check LaTeX syntax before compilation
./open-agents/tools/lint-latex.sh

# Validate paper structure
python3 ./open-agents/tools/validate-structure.py
```

### 📖 Documentation

| Document | Purpose |
|----------|---------|
| `.paper/docs/github-copilot-instructions.md` | VS Code Copilot usage |
| `.paper/docs/codex-instructions.md` | OpenAI Codex usage |
| `.paper/_cfg/agent-manifest.csv` | Complete agent catalog |
| `SYSTEM-PLANNING/SYSTEM_GUIDE.md` | System overview |
| `open-agents/INSTRUCTIONS.md` | Legacy full documentation |

### ✨ Key Features

✓ **10 specialized agents** for the complete paper workflow  
✓ **Multi-IDE support** - GitHub Copilot and OpenAI Codex  
✓ **Progressive disclosure** - agents load on demand  
✓ **Menu-driven interaction** - each agent presents options  
✓ **Modular LaTeX architecture** - atomic sections  
✓ **Harvard citation style** and bibliography management  
✓ **Configuration per module** - customize behavior  
✓ **Agent manifest** - discover all available agents  

### 🚀 Next Step

1. Open GitHub Copilot Chat in VS Code
2. Select `paper-architect` from the agent dropdown
3. Say "Create an outline for my paper on [topic]"
