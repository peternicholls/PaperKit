# Paper Kit: Agentic Academic Style Paper Writing System

An **Open Agent System** for writing high-quality academic specification papers in LaTeX format. Six specialized agents handle research consolidation, paper structuring, section drafting, quality refinement, reference management, and document assembly using a progressive, iterative methodology.

**Quick Start:** Jump to [Getting Started](#getting-started) or [The Writing Workflow](#the-writing-workflow)

---

## Table of Contents

1. [System Overview](#system-overview)
2. [How This System Works](#how-this-system-works)
3. [Project Structure](#project-structure)
4. [Available Agents](#available-agents)
5. [Routing Logic](#routing-logic)
6. [The Writing Workflow](#the-writing-workflow)
7. [LaTeX Architecture](#latex-architecture)
8. [Managing the System](#managing-the-system)
9. [Git Commit Protocol](#git-commit-protocol)
10. [File Naming Conventions](#file-naming-conventions)

---

## System Overview

Paper Kit provides a structured workflow for academic paper writing through specialized agents:

- **Research Consolidator** — Synthesize information from multiple sources
- **Paper Architect** — Create logical outlines and section hierarchies  
- **Section Drafter** — Write individual sections with academic rigor
- **Quality Refiner** — Improve clarity, coherence, and polish iteratively
- **Reference Manager** — Maintain citations (Harvard style) and bibliography
- **LaTeX Assembler** — Integrate sections into final document

### Design Principles

- **Progressive Disclosure** — Agents load on demand; minimal initial context
- **Modular LaTeX** — Small, focused section files for clean version control
- **Iterative Quality** — Multiple refinement passes for excellence
- **Structured Outputs** — Clear file organization; no unnecessary artifacts
- **System Identity** — Codename `PaperKit`

---

## How This System Works

### Architecture: Progressive Disclosure

Agents load on demand through a three-layer pattern:

```
User Request → AGENTS.md → INSTRUCTIONS.md → Specific Agent → Output
```

**Benefits:**
- Small initial context (only loads what's needed)
- Efficient scaling (agents load when invoked)
- Complex workflows supported (agents can chain)

**Layer Details:**

| Layer | File | Purpose |
|-------|------|---------|
| Entry | `AGENTS.md` | Quick reference and routing |
| Index | `open-agents/INSTRUCTIONS.md` | Full system documentation |
| Agents | `open-agents/agents/*.md` | Individual agent specifications |

**Workflow:** Each agent reads its specification, executes tasks, writes outputs to structured directories, and updates system memory.

---

## Project Structure

### The open-agents/ Container

```
open-agents/
├── README.md                    # Human-readable system intro
├── INSTRUCTIONS.md              # This file—full documentation
│
├── agents/                      # Agent definitions
│   ├── research_consolidator.md
│   ├── paper_architect.md
│   ├── section_drafter.md
│   ├── quality_refiner.md
│   ├── reference_manager.md
│   └── latex_assembler.md
│
├── tools/                       # Scripts and tools
│   ├── build-latex.sh          # LaTeX compilation script
│   ├── validate-structure.py   # Paper structure validator
│   ├── lint-latex.sh           # LaTeX syntax checking
│   └── format-references.py    # Reference formatter (Harvard)
│
├── memory/                      # System memory (created automatically)
│   ├── paper-metadata.yaml      # Paper title, scope, goals
│   ├── research-index.yaml      # Research sources and notes
│   ├── section-status.yaml      # Section status tracking
│   └── revision-log.md          # Change history
│
├── source/                      # Input materials
│   ├── research-notes/          # Your collected research
│   ├── ideas/                   # Sparks of imagination, discussions
│   ├── reference-materials/     # PDFs, links, source materials
│   └── user-stubs/              # Starting points, sketches
│
├── output-drafts/               # First drafts and working versions
│   ├── outlines/                # Paper outlines and structures
│   ├── sections/                # Individual section drafts
│   └── full-versions/           # Complete draft versions
│
├── output-refined/              # Refined, intermediate versions
│   ├── research/                # Consolidated research documents
│   ├── sections/                # Quality-refined section drafts
│   ├── references/              # Formatted bibliographies
│   └── full-versions/           # Refined complete versions
│
└── output-final/                # Ready for publication
    ├── latex/                   # Final LaTeX files
    └── pdf/                     # Compiled PDFs
```

### The latex/ Directory (at project root)

```
latex/
├── main.tex                     # Main document (inputs all sections)
├── preamble.tex                 # Document class, packages, macros
├── metadata.tex                 # Title page, author, abstract metadata
├── settings.tex                 # Configuration (fonts, spacing, etc.)
│
├── sections/                    # Individual section files
│   ├── 01_introduction.tex
│   ├── 02_background.tex
│   ├── 03_methodology.tex
│   └── ...
│
├── appendices/                  # Appendix sections
│   ├── A_supplementary.tex
│   ├── B_detailed_proofs.tex
│   └── ...
│
└── references/                  # Bibliography and reference handling
    └── references.bib           # BibTeX database
```

---

## Available Agents

### 1. Research Consolidator (`agents/research_consolidator.md`)

**Purpose:** Synthesize and organize research materials into coherent, well-documented reference documents.

**When to use:**
- User has collected multiple research sources and notes
- User says "consolidate research on..." or "research..."
- User wants to synthesize findings into a coherent narrative
- User provides research stubs or partial notes

**Input:** Research notes, links, excerpts, ideas from `source/research-notes/`

**Output:** 
- Consolidated research documents in `output-refined/research/`
- Updated `memory/research-index.yaml` with source tracking
- Markdown with Harvard-style citations ready for paper integration

**Example:** User provides scattered notes on color science theory → Agent synthesizes into coherent "Color Science Foundations" document with proper citations.

---

### 2. Paper Architect (`agents/paper_architect.md`)

**Purpose:** Design paper structure, outline sections and subsections, establish logical flow.

**When to use:**
- User wants to outline the paper
- User says "structure the paper" or "create an outline"
- User has a scope and needs a hierarchical organization
- User wants to plan research direction before drafting

**Input:** Paper scope, goals, user specifications from discussion

**Output:**
- Detailed outline in `output-drafts/outlines/paper_outline.md`
- Section-by-section breakdown with expected content
- Updated `memory/paper-metadata.yaml` with structure
- LaTeX skeleton with section files in `latex/sections/`

**Example:** User describes goal → Agent creates multi-level outline from Introduction through Conclusion, with estimated section lengths and research needs.

---

### 3. Section Drafter (`agents/section_drafter.md`)

**Purpose:** Write individual paper sections with academic rigor, clarity, and logical progression.

**When to use:**
- User asks to "draft [section name]"
- User says "write the introduction" or "draft methods section"
- User is ready to write a specific part of the paper
- User provides section outline or key points

**Input:** 
- Section outline from Paper Architect
- Relevant research from Research Consolidator
- User specifications and direction

**Output:**
- Section draft in `output-drafts/sections/[section_name].tex`
- Placeholder citations with `\cite{}` commands
- Updated `memory/section-status.yaml` with completion percentage
- References to integrated sources

**Core behaviors:**
- Write in LaTeX format with semantic markup
- Use clear academic language and logical transitions
- Include placeholder citations for all claims
- Flag areas needing more research
- Integrate research consolidations where appropriate

**Example:** User specifies introduction goals → Agent drafts 2000-word introduction with proper academic framing, motivation, and scope definition.

---

### 4. Quality Refiner (`agents/quality_refiner.md`)

**Purpose:** Improve draft quality through iterative refinement—clarity, coherence, grammar, logical flow.

**When to use:**
- User asks to "refine this draft"
- User says "improve section quality"
- User wants to iterate on a draft section
- User is unhappy with clarity or logical flow

**Input:** Draft sections from `output-drafts/sections/`

**Output:** 
- Refined version in `output-refined/sections/`
- Change summary noting improvements made
- Suggestions for deeper revision if applicable
- Updated section status

**Refinement focuses on:**
- Clarity: Is every sentence understandable?
- Coherence: Do sentences flow logically? Do paragraphs connect?
- Academic tone: Appropriate formality and voice?
- Citations: Are placeholders placed correctly?
- Length: Is section appropriately detailed?
- Audience: Would a specialist understand? Would a generalist?

**Example:** User submits draft introduction → Agent refines for clarity, ensures logical flow from problem statement through scope definition.

---

### 5. Reference Manager (`agents/reference_manager.md`)

**Purpose:** Manage bibliographic data, format references in Harvard style, maintain bibliography consistency.

**When to use:**
- User wants to format references
- User asks to "create bibliography"
- User provides new sources to add
- User needs citation formatting help

**Input:** 
- Research documents with source citations
- Reference list in any format
- `latex/references/references.bib` file

**Output:**
- Updated `references.bib` in BibTeX format
- Harvard-formatted bibliography in `output-refined/references/`
- Citation formatting guide
- Validation report (missing authors, inconsistent formatting)

**Maintains:**
- BibTeX entries for all sources
- Harvard citation style consistency
- Footnote formatting where needed
- Cross-references between sections

**Example:** User provides research document with citations → Agent extracts sources, converts to BibTeX, validates formatting, generates Harvard-style bibliography.

---

### 6. LaTeX Assembler (`agents/latex_assembler.md`)

**Purpose:** Integrate section files into complete LaTeX document, compile, validate, and produce final PDF.

**When to use:**
- User says "assemble the paper" or "build the document"
- User is ready for document integration
- User needs to compile and validate the document
- User wants final output

**Input:** 
- All refined section files from `output-refined/sections/`
- References from `references.bib`
- LaTeX configuration files

**Output:**
- Integrated `latex/main.tex`
- Compiled PDF in `output-final/pdf/`
- Build log with any warnings or errors
- Validation report on structure, citations, cross-references

**Responsibilities:**
- Ensure all `\input{}` statements correctly reference section files
- Validate LaTeX syntax and package compatibility
- Run BibTeX for bibliography generation
- Compile document and catch errors early
- Generate table of contents automatically
- Verify all citations are in bibliography
- Create clean final PDF

**Example:** User has all refined sections → Agent integrates into main.tex, compiles, validates all citations, produces publication-ready PDF.

---

## Commands: Setup to Publication

### Initialization Phase

| Command | Purpose | Agent |
|---------|---------|-------|
| `/paper.init` | Initialize session & capture goals | Paper Architect |
| `/paper.objectives` | Set aims, objectives, success criteria | Paper Architect |
| `/paper.requirements` | Define technical & format requirements | Paper Architect |
| `/paper.spec` | Define content specification & direction | Paper Architect |

### Core Writing Workflow

| Command | Purpose | Agent |
|---------|---------|-------|
| `/paper.plan` | Create detailed paper outline & structure | Paper Architect |
| `/paper.research` | Consolidate & synthesize research materials | Research Consolidator |
| `/paper.draft` | Draft individual paper section | Section Drafter |
| `/paper.refine` | Refine & improve draft for quality | Quality Refiner |
| `/paper.refs` | Manage bibliography and citations | Reference Manager |
| `/paper.assemble` | Integrate sections and compile to PDF | LaTeX Assembler |

### Sprint Planning

| Command | Purpose | Agent |
|---------|---------|-------|
| `/paper.sprint-plan` | Create and plan a new sprint | Paper Architect |
| `/paper.tasks` | Track and update sprint tasks | System Router |
| `/paper.review` | Review sprint outcomes & plan next | System Router |

### Specialist Support

| Command | Purpose | Agent |
|---------|---------|-------|
| `/paper.brainstorm` | Brainstorm ideas & explore options | Brainstorm Agent |
| `/paper.solve` | Solve blockers & identify root causes | Problem-Solver Agent |
| `/paper.tutor-feedback` | Get feedback & critique on draft | Tutor Agent |
| `/paper.librarian-research` | Find and research sources | Librarian Agent |
| `/paper.librarian-sources` | Evaluate and track sources | Librarian Agent |
| `/paper.librarian-gaps` | Identify research gaps | Librarian Agent |

---

## The Writing Workflow

### Phase 1: Initialization (One-time Setup)

Establish your paper's goals and constraints before writing:

```bash
/paper.init              # Initialize session, capture primary goal
/paper.objectives        # Define aims, objectives, success criteria  
/paper.requirements      # Technical & formatting requirements
/paper.spec             # Content specification & direction
```

**Outputs:** Planning documents in `planning/0000-Project-Overview/` with system memory updated.

### Phase 2: Planning & Research (Pre-writing)

Prepare structure and research materials:

```bash
/paper.plan             # Create detailed outline from goals
/paper.research         # Consolidate collected research materials
```

You now have a paper structure and supporting research ready for drafting.

### Phase 3: Sprint-Based Drafting & Refinement (Iterative)

Develop the paper in manageable sprints:

**Start each sprint:**
```bash
/paper.sprint-plan      # Plan this sprint's work (typically 3-5 sections)
```

**For each section in the sprint:**
```bash
/paper.draft "section name"       # Write the section
/paper.refine "section name"      # Polish for clarity (1-2 passes)
```

**Manage sprint progress:**
```bash
/paper.tasks            # Track and update task status
/paper.review           # Review sprint, identify blockers, plan next sprint
```

**Repeat Phase 3 sprints** until all sections are drafted and refined.

### Phase 4: Assembly & Publication (Final)

Prepare the complete, publication-ready document:

```bash
/paper.refs             # Finalize bibliography and citations
/paper.assemble         # Integrate all sections, compile final PDF
```

**Result:** Publication-ready document in `output-final/pdf/`.

### Support Commands (Use Anytime)

Throughout any phase, invoke specialist agents to support your work:

```bash
/paper.brainstorm       # Explore ideas or creative alternatives
/paper.tutor-feedback   # Get expert feedback on a draft
/paper.librarian-research  # Find sources for a specific topic
/paper.librarian-gaps   # Identify research gaps
/paper.solve            # Troubleshoot blockers or unclear sections
```

### Common Workflow Patterns

**Full Path (New Paper):**
```
/paper.init → /paper.objectives → /paper.requirements → /paper.spec
→ /paper.plan → /paper.research
→ /paper.sprint-plan → /paper.draft → /paper.refine → /paper.tasks → /paper.review (repeat)
→ /paper.refs → /paper.assemble
```

**Resume Existing Session:**
```
/paper.init --resume → /paper.sprint-plan → draft/refine → /paper.review
```

**When You Get Stuck:**
```
/paper.solve → identify root cause
/paper.tutor-feedback → get expert feedback
/paper.brainstorm → explore alternatives
```

**Research Gap Found During Drafting:**
```
/paper.librarian-research → find sources
/paper.research → consolidate into reference document
/paper.draft (resume) → continue with new research
```

---

## LaTeX Architecture

### Why Modular LaTeX?

- **Context Efficiency:** Section files stay small (agents don't drown in context)
- **Parallel Work:** Multiple agents can work on different sections
- **Version Control:** Git diffs are clean and meaningful
- **Rebuild Speed:** Only changed sections are recompiled
- **Team Friendly:** Easy to share sections or collaborate

### The Main Document Structure

`latex/main.tex`:
```tex
\input{preamble}
\input{metadata}

\begin{document}

\maketitle
\tableofcontents

% Sections
\input{sections/01_introduction}
\input{sections/02_background}
\input{sections/03_methodology}
...

% Appendices
\appendix
\input{appendices/A_supplementary}
...

\printbibliography

\end{document}
```

### Section File Format

Each section is an atomic `.tex` file:
```tex
\section{Introduction}

\subsection{Motivation}
Your content here...

\subsection{Scope and Objectives}
More content...
```

Agents write sections this way, making assembly trivial.

### Build Process

**Manual build:**
```bash
cd latex/
pdflatex main.tex
bibtex main
pdflatex main.tex  # Resolve references
pdflatex main.tex  # Final pass
```

**Automated build:**
```bash
./open-agents/tools/build-latex.sh
```

**Validation:**
```bash
./open-agents/tools/lint-latex.sh        # Check syntax
./open-agents/tools/validate-structure.py # Verify structure
```

---

## Managing the System

### Adding a New Agent

1. Create `open-agents/agents/{name}.md` following the anatomy template
2. Create command in `.claude/commands/paper/{command}.md`
3. Add to "Available Agents" section above
4. Add routing entry
5. Commit

### Editing an Agent

1. Locate `open-agents/agents/{name}.md`
2. Modify behaviors, update output locations if needed
3. Update routing table if triggers change
4. Commit

### Removing an Agent

1. Delete `open-agents/agents/{name}.md`
2. Delete associated command file
3. Remove from "Available Agents" and routing table
4. Commit

---

## Git Commit Protocol

Commit after each agent completes work:

**Format:** `{Action}: {description}`

**Actions:** `Draft`, `Refine`, `Research`, `Assemble`, `Update`

**Examples:**
```bash
# After drafting
git add output-drafts/sections/
git commit -m "Draft: introduction section (2500 words)"

# After research
git add output-refined/research/
git commit -m "Research: consolidate color science foundations"

# After refinement
git add output-refined/sections/
git commit -m "Refine: introduction clarity and flow"

# After assembly
git add latex/ output-final/
git commit -m "Assemble: compile v1.0 with all sections"
```

**Best practices:**
- Commit logical units of work
- Include word counts for sections
- Note version numbers for assemblies
- Add details in commit body when needed

---

## File Naming Conventions

### Source Materials
```
source/research-notes/topic_name.md
source/ideas/topic_or_date.md
source/reference-materials/source_description.pdf (or .md with links)
source/user-stubs/section_name_stub.tex
```

### Draft Outputs
```
output-drafts/outlines/paper_outline.md
output-drafts/sections/section_name.tex
output-drafts/full-versions/draft_v01.tex
```

### Refined Outputs
```
output-refined/research/research_topic.md
output-refined/sections/section_name.tex
output-refined/references/full_bibliography.md
output-refined/full-versions/refined_v01.tex
```

### Memory Files
```
memory/paper-metadata.yaml
memory/research-index.yaml
memory/section-status.yaml
memory/revision-log.md
```

### LaTeX Files
```
latex/main.tex
latex/sections/01_introduction.tex
latex/sections/02_background.tex
latex/appendices/A_supplementary.tex
latex/references/references.bib
```

**Conventions:**
- Use lowercase with underscores: `section_name.tex` (not SectionName.tex)
- Number sections for ordering: `01_`, `02_`, etc.
- Use descriptive names: `color_science_background.tex` not `section2.tex`
- Versions use: `filename_v01.tex`, `filename_v02.tex`

---

## Getting Started

### First-Time Setup

1. **Read this README** — Understand the system structure and workflow
2. **Review AGENTS.md** — Quick reference for all commands and agents
3. **Define your paper scope** — Know your topic, audience, and goals
4. **Prepare research materials** — Collect sources in `open-agents/source/research-notes/`
5. **Initialize the system** — Run `/paper.init` to begin

### Typical First Session

```bash
# Initialization (30 minutes)
/paper.init                    # Capture goal, audience, scope
/paper.objectives              # Define specific aims & success criteria
/paper.requirements            # Set technical & formatting requirements
/paper.spec                    # Define content direction

# Planning & Research (1-2 hours)
/paper.plan                    # Create detailed outline
/paper.research                # Consolidate research materials

# You're now ready to begin drafting
/paper.sprint-plan             # Plan first sprint (3-5 sections)
```

### Quick Start Checklist

- [ ] Read README.md (you're here!)
- [ ] Read AGENTS.md for command reference
- [ ] Review planning/0000-Project-Overview/ (if you have existing notes)
- [ ] Prepare research materials in `open-agents/source/research-notes/`
- [ ] Run `/paper.init` to initialize session
- [ ] Run `/paper.objectives`, `/paper.requirements`, `/paper.spec`
- [ ] Run `/paper.plan` to create outline
- [ ] Run `/paper.research` to consolidate research
- [ ] Start first sprint with `/paper.sprint-plan`
- [ ] Draft sections with `/paper.draft`
- [ ] Refine with `/paper.refine`
- [ ] Use `/paper.refs` and `/paper.assemble` for final publication

---

## Memory System

The system maintains several `.yaml` files in `memory/` to track state:

### paper-metadata.yaml
```yaml
title: "Paper Title Here"
scope: "Clear scope description"
audience: "Target audience"
target_length: "8000-10000 words"
deadline: "YYYY-MM-DD"
status: "drafting | refining | assembling"
```

### section-status.yaml
```yaml
sections:
  introduction:
    status: "drafted"
    words: 2500
    refinement_passes: 1
  background:
    status: "drafting"
    words: 1200
    refinement_passes: 0
```

### research-index.yaml
```yaml
sources:
  - title: "Source Title"
    authors: ["Author Names"]
    citation_key: "author_year"
    file: "source/research-notes/filename.md"
    topics: ["topic1", "topic2"]
```

These are updated automatically by agents and help maintain context without massive files.

---

## Summary

### Key Features

✓ **Six specialized agents** — Research, structure, draft, refine, reference, assemble  
✓ **Modular LaTeX** — Small files, clean diffs, parallel work  
✓ **Progressive loading** — Agents load on demand for efficiency  
✓ **Iterative quality** — Multiple refinement passes  
✓ **Memory system** — Track state without bloat  
✓ **Build automation** — Compile, lint, validate tools included  
✓ **Harvard citations** — Proper academic referencing  

### Next Steps

1. Review [Getting Started](#getting-started) above
2. Read `INSTRUCTIONS.md` for detailed agent specifications
3. Invoke your first agent using [Routing Logic](#routing-logic)
4. Follow [The Writing Workflow](#the-writing-workflow) for best results

### Support & Community

- **Installation help:** See [DEPENDENCIES.md](DEPENDENCIES.md)
- **Dependency check:** Run `./tools/check-dependencies.sh`
- **Agent details:** See `agents/*.md` for specifications
- **System architecture:** See `INSTRUCTIONS.md`
- **Version info:** See [VERSION](VERSION)
- **Questions & discussions:** Visit [GitHub Discussions](https://github.com/peternicholls/PaperKit/discussions)
- **Report bugs:** Open an [issue](https://github.com/peternicholls/PaperKit/issues)
- **Contribute:** See [CONTRIBUTING.md](CONTRIBUTING.md)
