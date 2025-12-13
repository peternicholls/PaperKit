# PaperKit - Research Paper Assistant Kit

**Version:** alpha-1.0.0

A complete **Open Agent System** for planning, researching, structuring, drafting, refining, and publishing high-quality academic specification papers in LaTeX format.

## 🚀 Quick Start

### Installation

**Prerequisites:**
- Bash (Mac/Linux) or PowerShell (Windows)
- Git (recommended)
- Python 3 (recommended for some tools)
- Node.js (optional)

### For Mac/Linux:

```bash
# Option 1: Using the paperkit command
./paperkit init

# Option 2: Direct installation
./paperkit-install.sh
```

### For Windows:

```powershell
# Run in PowerShell
.\paperkit-install.ps1
```

### Installation Steps

1. **Navigate to your project directory** - The installer will set up PaperKit in your current location
   ```bash
   cd /path/to/your/project
   ```

2. **Run the installer** - The script will:
   - Verify you're in the correct directory
   - Check for required dependencies
   - Detect your platform (Mac/Linux/Windows)
   - Create necessary directory structures
   - Set up the agent system

3. **Follow the prompts** - The installer will ask you to confirm:
   - Installation directory is correct
   - Whether to proceed if directory is not empty
   - Whether to reinitialize if PaperKit is already present

## 📋 What You Get

### 10 Specialized Agents

#### Core Paper Writing Agents
- 🔬 **Research Consolidator** - Synthesize research into coherent documents
- 🏗️ **Paper Architect** - Design paper structure and outline
- ✍️ **Section Drafter** - Write individual sections with rigor
- 💎 **Quality Refiner** - Improve clarity, flow, and polish
- 📚 **Reference Manager** - Manage citations and bibliography
- 🔧 **LaTeX Assembler** - Integrate sections and compile PDF

#### Specialist Support Agents
- 🧠 **Brainstorm Coach** - Creative ideation and exploration
- 🔬 **Problem Solver** - Analyze blockers and find solutions
- 🎓 **Review Tutor** - Constructive feedback on drafts
- 📖 **Research Librarian** - Find and organize sources

### Directory Structure

```
.paper/                    ← Agent system container
├── _cfg/                  ← Configuration and manifests
├── core/                  ← Core paper writing agents
├── specialist/            ← Support agents
├── docs/                  ← IDE-specific instructions
└── data/                  ← All outputs

.github/agents/            ← GitHub Copilot chat modes
.codex/prompts/            ← OpenAI Codex prompts

latex/                     ← Final LaTeX document
├── main.tex
├── sections/
└── references/

open-agents/               ← Legacy system (preserved)
```

## 🎯 Usage

### For GitHub Copilot (VS Code):
1. Open Copilot Chat
2. Select an agent from the dropdown (e.g., `paper-architect`)
3. The agent activates and presents a menu

### For OpenAI Codex:
1. Type `/paper-` to see available prompts
2. Select a prompt (e.g., `/paper-architect`)
3. The agent activates and presents a menu

### Typical Workflow

1. **Define scope** → Use Paper Architect to outline
2. **Research** → Use Research Consolidator + Librarian
3. **Structure** → Paper Architect creates outline and LaTeX skeleton
4. **Draft** → Section Drafter writes one section at a time
5. **Get Feedback** → Review Tutor provides critique
6. **Refine** → Quality Refiner improves each section
7. **Manage Refs** → Reference Manager validates citations
8. **Assemble** → LaTeX Assembler compiles final PDF

## 🛠️ Available Tools

```bash
# Build and compile LaTeX document
./open-agents/tools/build-latex.sh

# Check LaTeX syntax before compilation
./open-agents/tools/lint-latex.sh

# Validate paper structure
python3 ./open-agents/tools/validate-structure.py
```

## 📦 Distribution

### Creating a Bundle

To create a distributable bundle:

```bash
./paperkit-bundle.sh
```

This creates `paperkit-alpha-1.0.0.tar.gz` containing all necessary files.

### Sharing PaperKit

1. Share the bundle file: `paperkit-alpha-1.0.0.tar.gz`
2. Users extract: `tar -xzf paperkit-alpha-1.0.0.tar.gz`
3. Users navigate: `cd paperkit-alpha-1.0.0`
4. Users initialize: `./paperkit init`

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| `AGENTS.md` | Quick reference for all agents |
| `.paper/docs/github-copilot-instructions.md` | VS Code Copilot usage |
| `.paper/docs/codex-instructions.md` | OpenAI Codex usage |
| `.paper/_cfg/agent-manifest.csv` | Complete agent catalog |
| `SYSTEM-PLANNING/SYSTEM_GUIDE.md` | System overview |
| `open-agents/INSTRUCTIONS.md` | Legacy full documentation |

## 🔧 Requirements

### Required
- **Bash** (Mac/Linux) or **PowerShell** (Windows)
- A directory where you want to create your research paper project

### Recommended
- **Git** - For version control
- **Python 3** - For validation and formatting tools
- **LaTeX** - For compiling the final PDF (TeX Live, MiKTeX, or similar)

### Optional
- **Node.js** - For additional tooling support

## ✨ Key Features

✓ **10 specialized agents** for the complete paper workflow  
✓ **Multi-IDE support** - GitHub Copilot and OpenAI Codex  
✓ **Progressive disclosure** - agents load on demand  
✓ **Menu-driven interaction** - each agent presents options  
✓ **Modular LaTeX architecture** - atomic sections  
✓ **Harvard citation style** and bibliography management  
✓ **Configuration per module** - customize behavior  
✓ **Agent manifest** - discover all available agents  
✓ **Cross-platform** - Mac, Linux, Windows support  
✓ **Simple installation** - No Docker or CI complexity  

## 🤝 Support

For issues or questions:
1. Check `AGENTS.md` for agent-specific help
2. Review documentation in `.paper/docs/`
3. Consult the system guide in `SYSTEM-PLANNING/`

## 📝 Version

**Current Version:** alpha-1.0.0

This is an alpha release. The core functionality is stable, but some features are still being refined.

## 🎓 Getting Started Example

After installation, try this:

1. Open your IDE with GitHub Copilot or Codex
2. Activate the `paper-architect` agent
3. Say: "Create an outline for my paper on [your topic]"
4. Follow the agent's guidance through the paper writing workflow

---

**PaperKit** - Formerly known as "Academic Specification Paper Writing System"

Built on the **Open Agent System** architecture - using AI coding assistants as general-purpose agent hosts.
