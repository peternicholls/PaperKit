# PaperKit - Research Paper Assistant Kit

**Version:** alpha-1.0.0

A complete **Open Agent System** for planning, researching, structuring, drafting, refining, and publishing high-quality academic specification papers in LaTeX format.

## 🚀 Quick Start

### Installation

**Prerequisites:**
- Bash (macOS/Linux/WSL)
- Git (recommended)
- Python 3.8+ (recommended for validation tools)
- Node.js (optional)

### Base Installation (Recommended)

Run the base installation script to install PaperKit to your home directory:

```bash
curl -sSL https://raw.githubusercontent.com/peternicholls/PaperKit/master/scripts/base-install.sh | bash
```

This creates `~/paperkit` with the default configuration containing agents, workflows, and tools. After the initial bootstrap, `./paperkit` is the normal user-facing interface.

**Alternatively:** You can manually download the files from the GitHub repository and place them in your home directory at `~/paperkit/`.

**Updating?** If you already have PaperKit installed, you'll be prompted with update options and the ability to create a backup.

**Windows Users:** Use **Windows Subsystem for Linux (WSL)**. Windows support is currently WSL-only, and the normal PaperKit workflow runs from a bash shell inside WSL.

### Alternative Installation Methods

#### For Mac/Linux (Custom Location):

```bash
# Clone the repository
git clone https://github.com/peternicholls/PaperKit.git
cd PaperKit

# Initialize via the PaperKit CLI
./paperkit init
```

`./paperkit init` is the public setup command. The installer shell scripts are implementation details behind the CLI and are not the normal user workflow.

#### For Windows:

Use WSL for the supported Windows workflow:

```powershell
# Open WSL, then run the normal PaperKit CLI flow
wsl
git clone https://github.com/peternicholls/PaperKit.git
cd PaperKit
./paperkit init
```

### Python Environment Setup (Recommended)

PaperKit includes Python validation tools and utilities. We recommend using a virtual environment:

#### Mac/Linux:

```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

If `python3 -m venv .venv` fails on Ubuntu, Debian, or WSL with an `ensurepip` error, install the distro venv package first and rerun the command:

```bash
sudo apt update
sudo apt install python3-venv
# If needed for your exact interpreter version:
sudo apt install python3.12-venv
```

If it fails on macOS, install a full Python 3 distribution first, for example:

```bash
brew install python
```

#### Windows:

```powershell
# Create a virtual environment
python -m venv .venv

# Activate the environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### What Gets Installed:

- **PyYAML** - For parsing metadata and configuration files
- **jsonschema** - For validating agent definitions and manifests

#### Alternative: Use System Python

If you prefer not to use a virtual environment:

```bash
# Mac/Linux
pip3 install --user -r requirements.txt

# Windows
pip install --user -r requirements.txt
```

**Note:** The virtual environment needs to be activated each time you open a new terminal session.

## 🔄 Updating PaperKit

### Automatic Update (Base Installation)

If you installed PaperKit using the base installation script, updating is simple:

```bash
curl -sSL https://raw.githubusercontent.com/peternicholls/PaperKit/master/scripts/base-install.sh | bash
```

The script will:
1. Detect your existing installation at `~/paperkit`
2. Prompt you to choose an update method:
   - **Update** (recommended): Pull latest changes while preserving your work
   - **Backup and reinstall**: Create a timestamped backup, then fresh install
   - **Cancel**: Exit without making changes

If you have local changes (uncommitted work), the script will:
- Automatically stash your changes before updating
- Provide instructions to restore them after the update completes

### Manual Update (Custom Location)

If you cloned the repository to a custom location:

```bash
cd /path/to/your/PaperKit
git pull origin master
./paperkit generate  # Regenerate IDE integration files
```

If you have local changes:

```bash
cd /path/to/your/PaperKit
git stash  # Save your changes
git pull origin master
git stash pop  # Restore your changes
./paperkit generate
```

### Installation Steps (Custom Location)

1. **Navigate to your project directory** - The CLI will set up PaperKit in your current location
   ```bash
   cd /path/to/your/project
   ```

2. **Run the CLI setup command**
   ```bash
   ./paperkit init
   ```

   This will:
   - Verify you're in the correct directory
   - Check for required dependencies
   - Detect your platform (macOS/Linux/WSL)
   - Create necessary directory structures
   - Set up the agent system

3. **Regenerate generated IDE files only when needed**
   ```bash
   ./paperkit generate
   ./paperkit generate --target=copilot
   ./paperkit generate --target=codex
   ```

4. **Follow the prompts** - `./paperkit init` may ask you to confirm:
   - IDE integration choices
   - Whether to proceed if the directory is not empty
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
| `.paper/_cfg/agent-manifest.yaml` | Complete agent catalog |
| `.paper/_cfg/workflow-manifest.yaml` | Complete workflow catalog |
| `.paper/_cfg/tool-manifest.yaml` | Complete tool catalog |
| `SYSTEM-PLANNING/SYSTEM_GUIDE.md` | System overview |
| `open-agents/INSTRUCTIONS.md` | Legacy full documentation |

## 🔧 Requirements

### Required
- **Bash** (macOS/Linux/WSL)
- A directory where you want to create your research paper project

### Recommended
- **Git** - For version control
- **Python 3.8+** - For validation and formatting tools
  - Create a virtual environment: `python3 -m venv .venv`
  - Activate: `source .venv/bin/activate` (Mac/Linux) or `.venv\Scripts\activate` (Windows)
  - Install deps: `pip install -r requirements.txt`
   - On Debian/Ubuntu/WSL, if venv creation fails with `ensurepip`, install `python3-venv` first
   - On macOS, if venv creation fails, install a full Python distribution such as Homebrew Python
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
