# PaperKit: Agentic Academic Paper Writing System
[![Version](https://img.shields.io/github/v/tag/peternicholls/PaperKit?label=version&sort=semver)](.paperkit/_cfg/version.yaml)

PaperKit is a **document-first, agentic workflow** for researching and writing **high-quality academic papers** in **LaTeX** (compiled to PDF) with **verifiable citations** and repeatable builds.

- **Core Framework:** `.paperkit/` (agents, workflows, tools, schemas).
- **Multi-IDE:** GitHub Copilot (CLI and VS Code), MS Copilot, OpenAI Codex CLI (and more can be generated via shims.).

---

## Quick Start

**One-line installation (recommended):**

```bash
curl -sSL https://raw.githubusercontent.com/peternicholls/PaperKit/master/scripts/base-install.sh | bash
```

That bootstrap command installs PaperKit into `~/paperkit`. After that, use `./paperkit ...` commands as the normal interface.

**Or clone and run locally:**

```bash
git clone https://github.com/peternicholls/PaperKit.git
cd PaperKit
./paperkit init
```

## ‼️ IMPORTANT Activate Your Agent System

After installation, use the CLI for setup and regeneration:

```bash
./paperkit init                           # Set up or repair the local PaperKit installation
./paperkit generate                       # Regenerate all IDE files when needed
./paperkit generate --target=copilot      # Regenerate Copilot files only
./paperkit generate --target=codex        # Regenerate Codex files only
```

`./paperkit init` is the normal user-facing setup command in a repo checkout. Use `./paperkit generate` after editing `.paperkit/` or when you want to refresh generated IDE files.

For detailed installation instructions, prerequisites, and platform-specific guidance, see [INSTALL-INSTRUCTIONS.md](INSTALL-INSTRUCTIONS.md).

For all available commands, see [Commands Reference](Docs/COMMANDS.md)



## Table of Contents

1. [Quick Start](#quick-start)
2. [Is this for me?](#is-this-for-me)
3. [Why PaperKit was Created](#why-paperkit-was-created)
4. [What PaperKit Does](#what-paperkit-does)
5. [Installation](#installation)
6. [System Architecture](#system-architecture)
7. [The Ten Agents](#the-ten-agents)
8. [Writing Your Paper](#writing-your-paper)
9. [Tools & Commands](#tools--commands)
10. [Getting Help](#getting-help)



## Is this for me?

PaperKit uses LaTeX as the *output format*, but you don’t need to be a LaTeX expert. In practice you write and review small section files, and PaperKit’s structure + build tools handle the assembly.

### Why LaTeX (instead of Markdown or newer systems)?

It’s still the most widely-supported “final mile” for academic PDFs: strong bibliography/citation tooling, robust cross-references/figures/tables, and broad compatibility with publisher templates and reproducible builds. If you already love Markdown/Quarto/Typst, PaperKit can still be useful as a workflow framework—but the built-in tooling currently assumes a LaTeX build target.

Best fit if you:
- Write academic papers and want the work broken into small, reviewable section files (even if you’re not fluent in LaTeX).
- Care about academic integrity (quotes with page numbers, complete references, and "don’t invent citations").
- Want an agent workflow that can be installed into your editor and regenerated from a single Core Framework.

Probably not if you:
- Want a chat-only writing tool with no local document workflow.
- Don’t want LaTeX anywhere in the workflow (and don’t need citation rigor, however the research librarian tool can still be useful).

### Contributing
We really welcome contributions to this project by submitting issues, feature requests, or pull requests. Just fork the project and start working on your improvements! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.



## Why PaperKit was Created

PaperKit started as a personal toolkit for drafting a single, complex academic paper with strict citation and reproducibility requirements. I wanted a workflow that stayed honest under pressure: if a model produced fluent text, I still needed the underlying sources to be verifiable. It currently supports the Harvard citation style (Cite Them Right, 11th Edition) but could be adapted to others in the future.

As the workflow matured, it became clear the same building blocks solved problems that show up in most serious writing projects:

- **Multi-IDE, one Core Framework**: define agents and workflows once in `.paperkit/`, then generate IDE-specific wrappers.
- **Modular LaTeX that stays reviewable**: keep sections atomic, keep diffs small, and make build steps repeatable.
- **Less manual bibliography pain**: validate citations and manage references as part of the workflow, not an afterthought.
- **Document-first evidence to counter hallucinations**: treat PDFs and web sources as primary data; pull quotes (with page numbers) and citations from the source material before they enter drafts.
- **Reusable rigor**: forensic audit and research-mapping tools turned out to be useful beyond the original paper.

Under the hood, that means PaperKit pushes you toward good academic hygiene: attribute summaries and quotes, keep complete references, prefer reputable/open sources where possible, and don’t invent citations when something can’t be verified.

As it grew beyond that initial paper, I realized it could be useful to others too—so I generalized it into a framework with manifests, generators, and schema validation, making it easy to adopt the same outline → draft → audit → PDF loop with minimal friction.

## What PaperKit Does

PaperKit is a **complete system for academic paper writing** with:

✓ **10 specialized agents** — Each handles one aspect of paper creation
✓ **Multi-IDE support** — Works with GitHub Copilot (VS Code) or OpenAI Codex
✓ **Agent Skills** — Reusable instruction documents (agentskills.io standard)
✓ **Compositional Workflows** — Multi-step task orchestration
✓ **Modular LaTeX** — Small atomic section files for clean version control
✓ **Progressive refinement** — Multiple passes to improve clarity and quality
✓ **Citation management** — Harvard style (Cite Them Right) with validation
✓ **Build automation** — Compile, lint, and validate your document
✓ **Core Framework** — All definitions centralized in `.paperkit/`
✓ **Forensic audit tools** — Extract evidence from PDFs with context and mapping

### Meet The Agents

PaperKit ships with 10 agents (core + specialist). Each has a light persona and a sweet spot—try them in order or drop in where you need help.

| Agent | Persona vibe | Best for |
|-------|--------------|---------|
| 🧠 **Brainstorm Coach** | Curious collaborator | Shaping angles, hypotheses, and scope |
| 🏗️ **Paper Architect** | Structure-first organizer | Turning ideas into an outline and section plan |
| 📖 **Research Librarian** | Evidence hunter | Finding sources, extracting quotes/evidence |
| 🔬 **Research Consolidator** | Synthesis partner | Summarizing and structuring research into notes |
| ✍️ **Section Drafter** | Focused writer | Drafting sections one at a time |
| 💎 **Quality Refiner** | Polisher | Tightening clarity, flow, and tone |
| 🎓 **Review Tutor** | Thoughtful reviewer | Spot-checking drafts and suggesting improvements |
| 📚 **Reference Manager** | Detail hawk | Validating citations and formatting bibliography |
| 🔧 **LaTeX Assembler** | Builder | Compiling the final PDF reliably |
| 🔬 **Problem Solver** | Analysis partner | Unblocking tricky steps, edge cases, and research snags |

You’ll typically interact with them through your IDE or CLI of choice:

- **GitHub Copilot (VS Code):** open Copilot Chat and select an agent/mode.
- **Core Framework:** `.paperkit/`.
- **Generated IDE files:** `.github/agents/` and `.codex/prompts/`.

In VSCode, you can pick an agent from the Copilot Chat dropdown (e.g., `paper-architect`) and type your request. The agent responds with structured output you can review and edit. In Codex, you can type `/paper-architect` to invoke the same agent.

## Workflows

Workflows combine multiple agents in sequences. Key workflows:

| Workflow | Steps |
|----------|-------|
| **Paper Creation** | Architect → Research → Drafter → Refiner → Reference Manager → Assembler |
| **Citation Management** | Reference Manager validates → extracts → formats → checks completeness |
| **Forensic Audit** | Research Librarian pulls evidence and quotations, maps it to sections, validates, and produces audits of gaps in the research |
| **Feedback Loop** | Drafter → Review Tutor → Refiner → Quality check |

### If you just want to get moving, try this typical workflow:

| Step | Agent | Purpose |
|---:|---|---|
| 1 | 🧠 **Paper Brainstorm** | Explore angles, hypotheses, and scope |
| 2 | 🏗️ **Paper Architect** | Produce outline + section plan |
| 3 | 📖 **Research Librarian** | Find sources and extract evidence |
| 4 | 🔬 **Research Consolidator** | Synthesize research into usable notes |
| 5 | ✍️ **Section Drafter** | Draft each section (one at a time) |
| 6 | 💎 **Quality Refiner** | Improve clarity and flow |
| 7 | 📚 **Reference Manager** | Validate and format citations/bibliography |
| 8 | 🔧 **LaTeX Assembler** | Build the final PDF |

This is only a suggested starting point—you can adapt the workflow to your needs, skipping or repeating steps as necessary.

## Agent Skills

PaperKit includes **Agent Skills**—instruction documents that teach agents HOW to perform specific tasks. Skills follow the [agentskills.io](https://agentskills.io) specification.

| Skill | Description |
|-------|-------------|
| `humanizer` | Remove AI writing patterns from text |
| `academic-writing` | Academic paper composition guidelines |
| `harvard-citations` | Harvard citation style (Cite Them Right) |
| `latex-best-practices` | LaTeX document best practices |

Skills are automatically loaded by agents when relevant. You can also invoke them directly:

```bash
# List available skills
python .paperkit/tools/skill_registry.py skills --list

# Get skill details
python .paperkit/tools/skill_registry.py skills --get harvard-citations
```

**Note**: Skills (SKILL.md) teach agents HOW to do things. Compositional Workflows (YAML) define WHAT steps to execute. See [docs/dev/SKILLS.md](docs/dev/SKILLS.md) for the full architecture.


## Academic Integrity

PaperKit enforces rigorous citation standards:

- **Every claim** must have a source or be your own contribution
- **Direct quotes** must include exact text, page number, and full citation
- **Harvard style** (Cite Them Right, 11th Edition) for all citations
- **Open access** preferred; never fabricate or guess citations
- **Forensic audit** tools help verify and map evidence to sections



## Installation

### Requirements

- **macOS** (Intel/Apple Silicon) or **Linux** or **Windows**
- **Bash** (macOS/Linux/WSL)
- **Python 3.7+** (for validation and tools)
- **LaTeX distribution** (pdflatex, bibtex)
- **GitHub Copilot** or **OpenAI Codex** (or both)

### Base Installation

Run the base installation script to install PaperKit to your home directory:

```bash
curl -sSL https://raw.githubusercontent.com/peternicholls/PaperKit/master/scripts/base-install.sh | bash
```

This creates `~/paperkit` with the default configuration containing agents, workflows, and tools. After the bootstrap step, treat `./paperkit` as the public interface.

**Alternatively:** You can manually download the files from the GitHub repository and place them in your home directory at `~/paperkit/`.

**Updating?** If you already have PaperKit installed, you'll be prompted with update options and the ability to create a backup. For more information on updating, see [INSTALL-INSTRUCTIONS.md](INSTALL-INSTRUCTIONS.md).

**Windows Users:** Use **Windows Subsystem for Linux (WSL)**. Windows support is currently WSL-only, and the normal PaperKit workflow runs from a bash shell inside WSL.

### Repository Checkout Workflow

If you prefer to work from a cloned repository in a custom location, use the CLI workflow:

```bash
git clone https://github.com/peternicholls/PaperKit.git
cd PaperKit
./paperkit init
```

Use `./paperkit generate` later when you need to refresh generated IDE files after editing `.paperkit/`.

### Verify Dependencies

```bash
./.paperkit/tools/check-dependencies.sh
```

For platform-specific setup, including WSL guidance for Windows, see [INSTALL-INSTRUCTIONS.md](INSTALL-INSTRUCTIONS.md).

---

## System Architecture

The full directory layout and architectural details live in [Docs/ARCHITECTURE.md](Docs/ARCHITECTURE.md).

### Core Framework Principle

**`.paperkit/` is the Core Framework.** All other agent files and directories are derived:

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

### Command Separation

PaperKit separates **user commands** from **developer commands** for security:

- **`./paperkit`** - User commands (init, generate, latex, evidence, version info)
- **`./paperkit-dev`** - Developer commands (release, version modifications)

Developer commands require authorization via git user.email to prevent accidental system modifications. See [Developer Commands](.paperkit/docs/developer-commands.md) for details.


## Writing Your Paper

### Typical Workflow

```bash
# 1. Initialize
./paperkit init                    # Set up the project and IDE integration

# 2. Plan (in your IDE, invoke agents)
Paper Architect                    # Create outline
Research Consolidator              # Synthesize research

# 3. Draft & Refine (sprint-based)
Section Drafter                    # Write each section
Quality Refiner                    # Polish for clarity
Review Tutor                       # Get feedback (as needed)

# 4. References
Reference Manager                  # Format bibliography

# 5. Build & Review
./paperkit latex build             # Compile PDF
./paperkit latex open              # Preview output
```

Run `./paperkit generate` only when you have changed `.paperkit/` definitions or want to regenerate a specific IDE target.

### Using with GitHub Copilot (VS Code)

**First, ensure agents are generated:**
```bash
./paperkit generate --target=copilot
```

Then in VS Code:
1. Open Copilot Chat (Cmd+Shift+I)
2. Select agent from dropdown (e.g., `paper-architect`)
3. Type your request: "Create an outline for my paper on color science"
4. Agent responds with structured approach

### Using with OpenAI Codex

**First, ensure prompts are generated:**
```bash
./paperkit generate --target=codex
```

Then in your editor:
1. Create a new file or open existing
2. Type `/paper-` to see available agents
3. Select agent: `/paper-architect`
4. Provide instructions


## Commands Reference

All commands use the `./paperkit` CLI. For detailed command documentation, see [Docs/COMMANDS.md](Docs/COMMANDS.md).

### Setup & Validation

```bash
./paperkit init                           # Initialize PaperKit
./paperkit validate                       # Validate schemas & structure
./paperkit help                           # Show all commands
```

### Generate IDE Files

```bash
./paperkit generate                       # Generate all IDE files
./paperkit generate --target=copilot      # Generate Copilot agents only
./paperkit generate --target=codex        # Generate Codex prompts only
./paperkit generate --check               # Check if files up to date
```

### Version Management

```bash
./paperkit version                        # Show current version
./paperkit version --info                 # Show full version info (JSON)
./paperkit version --set alpha-1.3.0      # Set version
./paperkit version --bump patch           # Bump version (major|minor|patch)
./paperkit version --build 45             # Add build metadata (+45)
./paperkit version --test                 # Run version system tests
```

### LaTeX Document

```bash
./paperkit latex build                    # Build PDF document
./paperkit latex lint                     # Check LaTeX syntax
./paperkit latex open                     # Open built PDF
```

### Evidence Extraction

```bash
./paperkit evidence extract <pdf_dir> <output_md> [terms...]
```


## LaTeX Structure

For a comprehensive guide on how the final LaTeX document is assembled, see [Docs/LATEX-ASSEMBLY.md](Docs/LATEX-ASSEMBLY.md).

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
# Build PDF (automated 3-pass compilation)
./paperkit latex build

# Check syntax before building
./paperkit latex lint

# Preview the result
./paperkit latex open
```

### Output
PDF appears in: `open-agents/output-final/pdf/main.pdf`

For detailed information on the LaTeX assembly process, including file structure, 3-pass compilation, and customization, see [Docs/LATEX-ASSEMBLY.md](Docs/LATEX-ASSEMBLY.md).


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
./paperkit validate                    # Validate schemas and structure
./paperkit generate --check            # Check if IDE files need updating
./paperkit latex lint                  # Check LaTeX syntax
```


## Getting Help

### Documentation

- **[Docs/COMMANDS.md](Docs/COMMANDS.md)** — Complete commands reference
- **[Docs/LATEX-ASSEMBLY.md](Docs/LATEX-ASSEMBLY.md)** — How the final LaTeX document is assembled
- **[docs/dev/SKILLS.md](docs/dev/SKILLS.md)** — Agent Skills & Workflows architecture
- **AGENTS.md** — Quick reference for all agents
- **.paperkit/docs/github-copilot-instructions.md** — Copilot usage guide
- **.paperkit/docs/codex-instructions.md** — Codex usage guide
- **.paperkit/docs/legacy-agent-examples.md** — Example templates and patterns
- **.paperkit/_cfg/guides/harvard-citation-guide.md** — Citation style guide

### Troubleshooting

**Validate your setup:**
```bash
./paperkit validate
```

**Check LaTeX syntax:**
```bash
./paperkit latex lint
```

**Regenerate IDE files:**
```bash
./paperkit generate --check   # See what's missing
./paperkit generate           # Regenerate all
```

**Test version system:**
```bash
./paperkit version --test
```

### Support Channels

- **GitHub Issues:** [Report a bug](https://github.com/peternicholls/PaperKit/issues)
- **GitHub Discussions:** [Ask questions](https://github.com/peternicholls/PaperKit/discussions)
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md)



## Version

Current version: See [version.yaml](.paperkit/_cfg/version.yaml)

**Quick check:**
```bash
./paperkit version              # Show current version
./paperkit version --info       # Show full details
./paperkit version --help       # Show version management options
```

For version management documentation, see:
- [Version System README](.paperkit/docs/version-system-readme.md)
- [Commands Reference](Docs/COMMANDS.md)

Last updated: December 2025

## Recent Updates
See [CHANGELOG.md](CHANGELOG.md) for an overview of changes and RELEASE-NOTES.md for detailed notes about each release.



**Ready to write?** → Start with `./paperkit init`
