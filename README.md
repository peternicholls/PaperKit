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

This system provides a structured workflow for academic paper writing through specialized agents:

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

## Routing Logic

Use these triggers to invoke specific agents:

| When you say... | Agent invoked | Output location |
|-----------------|---------------|------------------|
| "Research..." / "consolidate research" | Research Consolidator | `output-refined/research/` |
| "Outline the paper" / "structure..." | Paper Architect | `output-drafts/outlines/` |
| "Draft [section name]" | Section Drafter | `output-drafts/sections/` |
| "Refine..." / "improve quality" | Quality Refiner | `output-refined/sections/` |
| "Format references" / "bibliography" | Reference Manager | `output-refined/references/` |
| "Assemble" / "build document" | LaTeX Assembler | `latex/`, `output-final/pdf/` |

---

## The Writing Workflow

### Typical Flow

1. **Define Scope** (You) → Set paper goals, audience, research direction
2. **Consolidate Research** (Research Consolidator) → Gather and synthesize sources
3. **Create Outline** (Paper Architect) → Define sections and logical flow
4. **Draft Sections** (Section Drafter) → Write individual sections sequentially
5. **Refine Quality** (Quality Refiner) → Iterate on clarity and coherence
6. **Manage References** (Reference Manager) → Maintain bibliography integrity
7. **Assemble & Publish** (LaTeX Assembler) → Create final document

### Iterative Refinement

You're not locked into a linear workflow. Typical patterns:

**Spiral Refinement:**
```
Draft Introduction → Refine → Get User Feedback → Redraft → Refine Again
```

**Just-in-Time Research:**
```
Draft Section → Realize Gap → Consolidate Research → Continue Draft
```

**Continuous Integration:**
```
Draft Section 1 → Draft Section 2 → Refine Both → Assembly → Catch Issues → Local Refinement
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

1. **Install dependencies** — See [DEPENDENCIES.md](DEPENDENCIES.md) for installation guide
   - Run `./tools/check-dependencies.sh` to verify your setup
2. **Define your paper scope** — Know your topic, audience, and goals
3. **Review the system** — Read this README and `INSTRUCTIONS.md`
4. **Prepare research** — Collect sources in `source/research-notes/`
5. **Initialize LaTeX** — Ensure `latex/` directory structure exists

### Typical First Session

```bash
# 1. Create paper outline
"Outline a paper about [topic]"

# 2. Consolidate initial research  
"Consolidate research on [topic]"

# 3. Draft first section
"Draft the introduction section"

# 4. Refine what you wrote
"Refine the introduction draft"
```

### Quick Start Checklist

- [ ] Define paper scope and goals
- [ ] Gather research materials in `source/research-notes/`
- [ ] Create paper outline (Paper Architect)
- [ ] Consolidate research (Research Consolidator)  
- [ ] Draft sections iteratively (Section Drafter)
- [ ] Refine for quality (Quality Refiner)
- [ ] Manage references (Reference Manager)
- [ ] Assemble final document (LaTeX Assembler)

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

### Support

- **Installation help:** See [DEPENDENCIES.md](DEPENDENCIES.md)
- **Dependency check:** Run `./tools/check-dependencies.sh`
- **Agent details:** See `agents/*.md` for specifications
- **System architecture:** See `INSTRUCTIONS.md`
