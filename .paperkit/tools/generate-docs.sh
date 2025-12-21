#!/bin/bash
# PaperKit Documentation Generator
# Generates AGENTS.md and COPILOT.md from .paperkit/ source of truth
# Usage: ./paperkit-generate-docs.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERKIT_ROOT="${SCRIPT_DIR}"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info_msg() { echo -e "${BLUE}ℹ ${NC}$1"; }
success_msg() { echo -e "${GREEN}✓ ${NC}$1"; }
error_msg() { echo -e "${RED}✗ ${NC}$1"; }

# Check .paperkit exists
if [ ! -d "${PAPERKIT_ROOT}/.paperkit" ]; then
    error_msg ".paperkit/ directory not found. Run from PaperKit root."
    exit 1
fi

# Check Python and pyyaml
# Use venv Python if available, otherwise fall back to system Python
if [ -f "${PAPERKIT_ROOT}/.venv/bin/python" ]; then
    PYTHON_CMD="${PAPERKIT_ROOT}/.venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    error_msg "Python 3 is required but not found."
    exit 1
fi

if ! "$PYTHON_CMD" -c "import yaml" 2>/dev/null; then
    error_msg "PyYAML is required. Install with: pip install pyyaml"
    exit 1
fi

info_msg "Generating documentation from .paperkit/ manifests..."

# Generate AGENTS.md
"$PYTHON_CMD" << 'PYTHON_SCRIPT'
import yaml
import os
from pathlib import Path

paperkit_root = Path(os.getcwd())
manifest_path = paperkit_root / '.paperkit' / '_cfg' / 'agent-manifest.yaml'

# Load agent manifest
with open(manifest_path) as f:
    manifest = yaml.safe_load(f)

agents = manifest['agents']

# Separate core and specialist agents
core_agents = [a for a in agents if a.get('module') == 'core']
specialist_agents = [a for a in agents if a.get('module') == 'specialist']

# Generate AGENTS.md
agents_md = """**CRITICAL: Read `.paperkit/docs/github-copilot-instructions.md` for GitHub Copilot or `.paperkit/docs/codex-instructions.md` for OpenAI Codex.**

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
- **Derived layers** (.github/agents, .codex/prompts, AGENTS.md, COPILOT.md) are generated files.
- **Edit only in `.paperkit/`**; regenerate derived layers with `./paperkit generate` to avoid drift.

**For OpenAI Codex:**
1. Type `/paper-` to see available prompts
2. Select prompt (e.g., `/paper-architect`)
3. Agent activates and presents menu

### 🎯 Ten Specialized Agents

#### Core Paper Writing Agents

| Agent | Persona | Purpose | Trigger |
|-------|---------|---------|---------|
"""

# Add core agents to table
for agent in core_agents:
    icon = agent.get('icon', '📄')
    title = agent.get('title', agent['name'].title())
    display_name = agent.get('displayName', 'Agent')
    name = agent['name']
    # Get description from YAML file if it exists
    yaml_path = paperkit_root / agent['path']
    description = title
    if yaml_path.exists():
        with open(yaml_path) as yf:
            agent_yaml = yaml.safe_load(yf)
            if 'description' in agent_yaml:
                description = agent_yaml['description']
    
    trigger = f"paper-{name}" if not name.startswith('paper-') else name
    agents_md += f"| {icon} **{title}** | {display_name} | {description} | `{trigger}` |\n"

agents_md += """
#### Specialist Support Agents

| Agent | Persona | Purpose | Trigger |
|-------|---------|---------|---------|
"""

# Add specialist agents to table
for agent in specialist_agents:
    icon = agent.get('icon', '🔧')
    title = agent.get('title', agent['name'].title())
    display_name = agent.get('displayName', 'Agent')
    name = agent['name']
    yaml_path = paperkit_root / agent['path']
    description = title
    if yaml_path.exists():
        with open(yaml_path) as yf:
            agent_yaml = yaml.safe_load(yf)
            if 'description' in agent_yaml:
                description = agent_yaml['description']
    
    trigger = f"paper-{name}" if not name.startswith('paper-') else name
    agents_md += f"| {icon} **{title}** | {display_name} | {description} | `{trigger}` |\n"

agents_md += """
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

---

*This file is auto-generated from `.paperkit/` manifests. Run `./paperkit generate` to regenerate.*
"""

# Write AGENTS.md
with open(paperkit_root / 'AGENTS.md', 'w') as f:
    f.write(agents_md)

print("✓ Generated AGENTS.md")

# Generate COPILOT.md
copilot_md = """## Paper Kit: Agentic Academic Style Paper Writing System — GitHub Copilot Integration

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
"""

# Add core agents
for agent in core_agents:
    name = agent['name']
    display_name = agent.get('displayName', 'Agent')
    title = agent.get('title', name.title())
    trigger = f"paper-{name}" if not name.startswith('paper-') else name
    
    yaml_path = paperkit_root / agent['path']
    description = title
    if yaml_path.exists():
        with open(yaml_path) as yf:
            agent_yaml = yaml.safe_load(yf)
            if 'description' in agent_yaml:
                description = agent_yaml['description']
    
    copilot_md += f"| `{trigger}` | {title} ({display_name}) | {description} |\n"

copilot_md += """
#### Specialist Support Agents
| Command | Agent | Purpose |
|---------|-------|---------|
"""

# Add specialist agents
for agent in specialist_agents:
    name = agent['name']
    display_name = agent.get('displayName', 'Agent')
    title = agent.get('title', name.title())
    trigger = f"paper-{name}" if not name.startswith('paper-') else name
    
    yaml_path = paperkit_root / agent['path']
    description = title
    if yaml_path.exists():
        with open(yaml_path) as yf:
            agent_yaml = yaml.safe_load(yf)
            if 'description' in agent_yaml:
                description = agent_yaml['description']
    
    copilot_md += f"| `{trigger}` | {title} ({display_name}) | {description} |\n"

copilot_md += """
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
"""

# Write COPILOT.md
with open(paperkit_root / 'COPILOT.md', 'w') as f:
    f.write(copilot_md)

print("✓ Generated COPILOT.md")

PYTHON_SCRIPT

success_msg "Documentation generation complete!"
info_msg "Generated: AGENTS.md, COPILOT.md"
