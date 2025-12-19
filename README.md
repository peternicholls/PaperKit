# PaperKit: Agentic Academic Paper Writing System

An **Open Agent System** for writing high-quality academic specification papers in LaTeX format. Ten specialized agents—coordinated through GitHub Copilot or OpenAI Codex—handle research consolidation, paper structuring, section drafting, quality refinement, reference management, and document assembly.

**Source of Truth:** `.paperkit/` — canonical agents, workflows, tools, and configuration  
**Multi-IDE Support:** GitHub Copilot, OpenAI Codex (or both)  
**Latest:** Enhanced installer with IDE selection, JSON schema validation, forensic audit tools, centralized implementations

---

## Quick Start

```bash
./paperkit init
```

This launches an interactive installer with:
- IDE selection (GitHub Copilot, OpenAI Codex, or both)
- Automatic file generation for your chosen IDE(s)
- Dependency verification

For detailed setup, see [Installation](#installation)

---

## Table of Contents

1. [What PaperKit Does](#what-paperkit-does)
2. [Installation](#installation)
3. [System Architecture](#system-architecture)
4. [The Ten Agents](#the-ten-agents)
5. [Workflows](#workflows)
6. [Writing Your Paper](#writing-your-paper)
7. [Tools & Commands](#tools--commands)
8. [LaTeX Structure](#latex-structure)
9. [Managing the System](#managing-the-system)
10. [Getting Help](#getting-help)

---

## What PaperKit Does

PaperKit is a **complete system for academic paper writing** with:

✓ **10 specialized agents** — Each handles one aspect of paper creation  
✓ **Multi-IDE support** — Works with GitHub Copilot (VS Code) or OpenAI Codex  
✓ **Modular LaTeX** — Small atomic section files for clean version control  
✓ **Progressive refinement** — Multiple passes to improve clarity and quality  
✓ **Citation management** — Harvard style (Cite Them Right) with validation  
✓ **Build automation** — Compile, lint, and validate your document  
✓ **Source of truth** — All definitions centralized in `.paperkit/`  
✓ **Forensic audit tools** — Extract evidence from PDFs with context and mapping  

### The Agents

| Agent | Role |
|-------|------|
| 🔬 **Research Consolidator** | Synthesize research into coherent documents |
| 🏗️ **Paper Architect** | Design paper structure and outlines |
| ✍️ **Section Drafter** | Write individual sections with rigor |
| 💎 **Quality Refiner** | Improve clarity, flow, and polish |
| 📚 **Reference Manager** | Manage bibliography and citations (Harvard) |
| 🔧 **LaTeX Assembler** | Integrate sections and compile PDF |
| 🧠 **Brainstorm Coach** | Explore ideas and alternatives |
| 🔬 **Problem Solver** | Analyze blockers and find solutions |
| 🎓 **Review Tutor** | Provide constructive feedback |
| 📖 **Research Librarian** | Find sources and extract evidence |

---

## Installation

### Requirements

- **macOS** (Intel/Apple Silicon) or **Linux** or **Windows**
- **Bash** (for shell scripts) or **PowerShell** (for Windows)
- **Python 3.7+** (for validation and tools)
- **LaTeX distribution** (pdflatex, bibtex)
- **GitHub Copilot** or **OpenAI Codex** (or both)

### Verify Dependencies

```bash
./.paper/tools/check-dependencies.sh
```

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/peternicholls/PaperKit.git
cd PaperKit

# 2. Run the installer
./paperkit init

# 3. Select your IDE(s) when prompted
# - GitHub Copilot (VS Code)
# - OpenAI Codex
# - Both
# - None (manual usage only)
```

The installer will:
- Create IDE-specific files (`.github/agents/`, `.codex/prompts/`)
- Verify your LaTeX installation
- Check Python dependencies
- Create necessary directories

### Alternative: Manual Setup

For Windows or if you prefer not to run scripts:

```bash
# Generate IDE files manually
./paperkit generate --target=copilot    # GitHub Copilot only
./paperkit generate --target=codex      # OpenAI Codex only
./paperkit generate                     # Both

# Validate your setup
./paperkit validate
```

### PowerShell (Windows)

```powershell
# Run the Windows installer
.\paperkit-install-v2.sh

# Or use PowerShell generator
.\paperkit-generate.ps1
```

---

## System Architecture

### Directory Structure

```
.paperkit/                           ← CANONICAL SOURCE OF TRUTH
├── _cfg/                         ← Configuration & manifests
│   ├── agent-manifest.yaml       ← All agents catalog
│   ├── workflow-manifest.yaml    ← All workflows catalog
│   ├── tool-manifest.yaml        ← All tools catalog
│   ├── agents/                   ← Agent definitions (YAML)
│   ├── workflows/                ← Workflow definitions (YAML)
│   ├── tools/                    ← Tool definitions (YAML)
│   ├── schemas/                  ← JSON schemas for validation
│   └── guides/                   ← Style guides (Harvard citations)
│
├── core/                         ← Core paper agents
│   └── agents/                   ← Research, architect, drafter, refiner
│
├── specialist/                   ← Support agents
│   └── agents/                   ← Brainstorm, tutor, librarian, solver
│
├── tools/                        ← Tool implementations
│   ├── build-latex.sh
│   ├── lint-latex.sh
│   ├── extract-evidence.sh
│   ├── format-references.py
│   ├── validate-structure.py
│   └── check-dependencies.sh
│
├── docs/                         ← Documentation
│   ├── github-copilot-instructions.md
│   ├── codex-instructions.md
│   └── legacy-agent-examples.md
│
└── data/                         ← Outputs (drafts, refined, final)

.github/agents/                   ← GitHub Copilot chat agents
├── paper-architect.agent.md
├── paper-brainstorm.agent.md
└── ... (one per agent)

.codex/prompts/                   ← OpenAI Codex prompts
├── paper-architect.md
├── paper-brainstorm.md
└── ... (one per agent)

latex/                            ← LaTeX document
├── main.tex
├── sections/                     ← 01_introduction.tex, etc.
├── appendices/                   ← A_supplementary.tex, etc.
└── references/                   ← references.bib

paperkit                          ← Main CLI
paperkit-validate.py              ← Schema validator
paperkit-generate.sh              ← Generator (bash)
paperkit-generate.ps1             ← Generator (PowerShell)
```

### Source of Truth Principle

**`.paperkit/` is canonical.** All other directories are derived:

- **Agent definitions** live in `.paperkit/core/agents/` and `.paperkit/specialist/agents/`
- **IDE files** (`.github/agents/`, `.codex/prompts/`) are generated from `.paperkit/agents/`
- **Tool implementations** live in `.paperkit/tools/`
- **Tool metadata** lives in `.paperkit/_cfg/tools/`
- **Workflows** defined in `.paperkit/_cfg/workflows/`
- **Schemas** in `.paperkit/_cfg/schemas/`

To update the system, edit `.paperkit/` and regenerate IDE files:

```bash
./paperkit generate                 # Regenerate all IDE files
./paperkit generate --target=copilot  # Regenerate Copilot only
```

---

## The Ten Agents

### Core Writing Agents

#### 🔬 Research Consolidator
**Synthesize research into coherent documents with proper citations.**

Use when:
- You've collected multiple research sources
- You need research synthesized into narrative form
- You want to consolidate scattered notes

Output: Consolidated research documents in `.paperkit/data/output-refined/research/`

#### 🏗️ Paper Architect
**Design paper structure, create outlines, establish logical flow.**

Use when:
- You need to outline the paper
- You want to plan section structure
- You need a detailed table of contents

Output: Outline and LaTeX skeleton in `.paperkit/data/output-drafts/outlines/`

#### ✍️ Section Drafter
**Write individual sections with academic rigor and clarity.**

Use when:
- You're ready to draft a specific section
- You have research and need it written up
- You want sections written in proper LaTeX format

Output: Section drafts in `.paperkit/data/output-drafts/sections/`

#### 💎 Quality Refiner
**Improve clarity, coherence, grammar, and logical flow.**

Use when:
- You want to polish a draft
- Clarity needs improvement
- Logical connections are weak

Output: Refined sections in `.paperkit/data/output-refined/sections/`

#### 📚 Reference Manager
**Manage bibliography, format citations (Harvard style), validate entries.**

Use when:
- You need citations formatted
- You want to validate your bibliography
- You need to add new sources
- You want completeness checks on citations

Output: Validated bibliography in `latex/references/references.bib`

#### 🔧 LaTeX Assembler
**Integrate sections, compile to PDF, validate document structure.**

Use when:
- All sections are ready
- You're preparing final document
- You need to compile and check for errors

Output: Final PDF in `.paperkit/data/output-final/pdf/`

### Support Agents

#### 🧠 Brainstorm Coach
**Explore ideas, generate alternatives, creative thinking.**

#### 🔬 Problem Solver
**Analyze blockers, identify root causes, find solutions.**

#### 🎓 Review Tutor
**Provide constructive feedback, critique drafts, suggest improvements.**

#### 📖 Research Librarian
**Find sources, extract evidence, forensic audit of PDFs with context mapping.**

---

## Workflows

Workflows combine multiple agents in sequences. Key workflows:

| Workflow | Steps |
|----------|-------|
| **Paper Creation** | Architect → Research → Drafter → Refiner → Reference Manager → Assembler |
| **Citation Management** | Reference Manager validates → extracts → formats → checks completeness |
| **Forensic Audit** | Librarian extracts evidence → maps to sections → validates → produces report |
| **Feedback Loop** | Drafter → Review Tutor → Refiner → Quality check |

---

## Writing Your Paper

### Typical Workflow

```bash
# 1. Initialize
./paperkit init                    # Set up IDE selection

# 2. Plan (in your IDE, invoke agents)
Paper Architect                    # Create outline
Research Consolidator              # Synthesize research

# 3. Draft & Refine (sprint-based)
Section Drafter                    # Write each section
Quality Refiner                    # Polish for clarity
Review Tutor                       # Get feedback (as needed)

# 4. References
Reference Manager                  # Format bibliography

# 5. Assemble
LaTeX Assembler                    # Compile final PDF
```

### Using with GitHub Copilot (VS Code)

1. Open Copilot Chat (Cmd+Shift+I)
2. Select agent from dropdown (e.g., `paper-architect`)
3. Type your request: "Create an outline for my paper on color science"
4. Agent responds with structured approach

### Using with OpenAI Codex

1. Create a new file or open existing
2. Type `/paper-` to see available agents
3. Select agent: `/paper-architect`
4. Provide instructions

---

## Tools & Commands

### CLI Commands

```bash
./paperkit init                           # Initialize (IDE selection)
./paperkit generate                       # Generate all IDE files
./paperkit generate --target=copilot      # Generate Copilot agents only
./paperkit generate --target=codex        # Generate Codex prompts only
./paperkit generate --check               # Check if files up to date
./paperkit validate                       # Validate schemas & structure
./paperkit version                        # Show version
./paperkit help                           # Show help
```

### Tool Scripts

```bash
# Build LaTeX
./.paperkit/tools/build-latex.sh [--clean] [--final]

# Check LaTeX syntax
./.paperkit/tools/lint-latex.sh

# Extract evidence from PDFs (forensic audit)
./.paperkit/tools/extract-evidence.sh <pdf_dir> <output_md> [terms...]

# Validate paper structure
python3 ./.paperkit/tools/validate-structure.py

# Format bibliography (Harvard style)
python3 ./.paperkit/tools/format-references.py --validate <file.bib>

# Check dependencies
./.paperkit/tools/check-dependencies.sh
```

### Schema Validation

```bash
# Full validation with Python
python3 paperkit-validate.py

# Validation options
python3 paperkit-validate.py --verbose        # Detailed output
python3 paperkit-validate.py --agents-only    # Agents only
python3 paperkit-validate.py --ide-sync       # Check IDE file sync
```

---

## LaTeX Structure

### Main Document

`latex/main.tex`:
```tex
\input{preamble}
\input{metadata}

\begin{document}
\maketitle
\tableofcontents

\input{sections/01_introduction}
\input{sections/02_background}
...

\appendix
\input{appendices/A_supplementary}

\printbibliography
\end{document}
```

### Section Files

Each section is atomic:
```tex
\section{Introduction}

\subsection{Motivation}
Your content here...

\cite{source_key}
```

### Build Process

```bash
# Automated
./.paperkit/tools/build-latex.sh

# Manual (3 passes for cross-references)
cd latex/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Output
PDF appears in: `.paperkit/data/output-final/pdf/main.pdf`

---

## Managing the System

### Add a New Agent

1. Create `.paperkit/core/agents/new-agent.md` (or `.paperkit/specialist/agents/`)
2. Follow agent template from existing agents
3. Update `.paperkit/_cfg/agent-manifest.yaml`
4. Regenerate IDE files:
   ```bash
   ./paperkit generate
   ```

### Update an Existing Agent

1. Edit `.paperkit/core/agents/agent-name.md`
2. Regenerate IDE files:
   ```bash
   ./paperkit generate
   ```

### Add a New Tool

1. Create implementation in `.paperkit/tools/tool-name.sh` (or `.py`)
2. Create definition in `.paperkit/_cfg/tools/tool-name.yaml`
3. Update `.paperkit/_cfg/tool-manifest.yaml`
4. Document in `.paperkit/tools/README.md`

### Validate Changes

```bash
./paperkit validate                    # Quick check
python3 paperkit-validate.py --verbose # Full validation
```

---

## Academic Integrity

PaperKit enforces rigorous citation standards:

- **Every claim** must have a source or be your own contribution
- **Direct quotes** must include exact text, page number, and full citation
- **Harvard style** (Cite Them Right, 11th Edition) for all citations
- **Open access** preferred; never fabricate or guess citations
- **Forensic audit** tools help verify and map evidence to sections

---

## Getting Help

### Documentation

- **AGENTS.md** — Quick reference for all commands
- **.paperkit/docs/github-copilot-instructions.md** — Copilot usage guide
- **.paperkit/docs/codex-instructions.md** — Codex usage guide
- **.paperkit/docs/legacy-agent-examples.md** — Example templates and patterns
- **.paperkit/_cfg/guides/harvard-citation-guide.md** — Citation style guide

### Troubleshooting

**Check dependencies:**
```bash
./.paper/tools/check-dependencies.sh
```

**Validate your setup:**
```bash
./paperkit validate
```

**Check LaTeX syntax:**
```bash
./.paperkit/tools/lint-latex.sh
```

**Regenerate IDE files:**
```bash
./paperkit generate --check   # See what's missing
./paperkit generate           # Regenerate all
```

### Support Channels

- **GitHub Issues:** [Report a bug](https://github.com/peternicholls/PaperKit/issues)
- **GitHub Discussions:** [Ask questions](https://github.com/peternicholls/PaperKit/discussions)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## Key Features at a Glance

| Feature | Details |
|---------|---------|
| **Agents** | 10 specialized, modular, chainable |
| **IDEs** | GitHub Copilot (VS Code), OpenAI Codex, or both |
| **Source of Truth** | `.paperkit/` canonical, derived to IDE formats |
| **LaTeX** | Modular sections, clean diffs, parallel work |
| **Citations** | Harvard style with validation workflows |
| **Tools** | Build, lint, validate, extract evidence |
| **Validation** | JSON schemas for agents, workflows, tools |
| **Forensic Audit** | Extract evidence from PDFs with context |
| **Installation** | Interactive, IDE selection, dependency check |

---

## Quick Reference

```bash
# Setup
./paperkit init                           # One-time initialization

# Generate/validate
./paperkit generate                       # Regenerate IDE files
./paperkit validate                       # Validate schemas
./paperkit version                        # Show version

# Build
./.paperkit/tools/build-latex.sh             # Compile PDF
./.paperkit/tools/lint-latex.sh              # Check syntax
./.paperkit/tools/check-dependencies.sh      # Verify system

# Tools
python3 ./.paperkit/tools/validate-structure.py
python3 ./.paperkit/tools/format-references.py --validate refs.bib
./.paperkit/tools/extract-evidence.sh <pdf_dir> <output_md> [terms]
```

---

## Version

Current version: See [VERSION](VERSION) file

Last updated: December 2025

---

**Ready to write?** → Start with `./paperkit init`
