# Academic Specification Paper Writing System

An **Open Agent System** for planning, researching, structuring, drafting, refining, and publishing high-quality academic specification papers in LaTeX format using a progressive, iterative research and writing methodology.

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
11. [Forensic Audit Protocol](#forensic-audit-protocol)
12. [Citation Workflows](#citation-workflows)

---

## System Overview

### Purpose

This system transforms your specification paper research and writing into a structured, collaborative workflow between you and specialized agents. Rather than producing documents in isolation, agents help you:

- **Research** consolidate and synthesize information from multiple sources
- **Structure** create logical outlines and section hierarchies
- **Draft** progressively write each section with academic rigor
- **Refine** improve quality, clarity, and coherence iteratively
- **Reference** maintain accurate citations (Harvard system) and bibliography
- **Assemble** integrate sections into a polished LaTeX document

### Core Philosophy

1. **Progressive Disclosure** — Only load what's needed; agents load on demand
2. **Atomic Context** — Each agent works on focused tasks; no massive context bloat
3. **Iterative Excellence** — Write, refine, redraft, improve—multiple passes for quality
4. **Structured Collaboration** — You think strategically; agents execute systematically
5. **No Noise** — Only create documents that serve the paper; no unnecessary summaries
6. **LaTeX as Foundation** — The final document lives in modular LaTeX files from day one

---

## How This System Works

### The Pointer Pattern (Progressive Disclosure)

When you invoke an agent command:

```
User: "/paper draft introduction"
         ↓
    AGENTS.md (entry point with read directive)
         ↓
        ## Forensic Audit Protocol

        ### Mission
        Provide PhD-level rigor in extracting and documenting evidence from all collected PDFs and sources. Every claim in the paper should be traceable to a quotable finding with section mapping and Harvard-style citation.

        ### Academic Integrity Standards
        - Never fabricate: Only cite sources you have actually collected/read
        - Direct quotation: Use exact quotes with quotation marks and page numbers where available
        - Harvard citation: Author-date in-text citations; complete BibTeX entries
        - Source verification: Prefer open access; confirm accessibility before extraction

        ### Extraction Methodology
        1. Inventory first: List ALL available PDFs before extraction
        2. Systematic coverage: Process each source methodically; do not cherry-pick
        3. Tool-assisted extraction: Use `pdftotext` + `grep` with context flags (`-A 10 -B 3`)
        4. Context preservation: Include surrounding sentences for proper interpretation
        5. Section mapping: Map each finding to specific paper sections (§02–§12)
        6. BibTeX entries: Create/update entries for every new source cited
        7. Document gaps: Explicitly note missing evidence for any claim

        ### Document Search Protocol
        - Timeouts: Set maximum search iterations when fetching documents online
        - Boundaries: Define a max number of attempts before escalating to manual retrieval
        - Terminal downloads: Prefer `wget` or `curl` for controlled retries and integrity checks
        - Verify content: Confirm file integrity and format before adding to inventory

        ### Search Efficiency Guidelines
        - Pre-filter targets: Prefer academic databases (arXiv, institutional repos)
        - Log queries: Record search terms and failed searches to avoid duplication
        - Cache successes: Maintain a record of source locations for quick re-access
        - Escalate blocks: If not locatable after three attempts, flag for manual intervention
        - Check access: Confirm open-access or institutional access before extraction

        ### Tools
        - `open-agents/tools/extract-evidence.sh` — batch `pdftotext` + `grep` with context capture
        - `open-agents/tools/lint-latex.sh` — validate LaTeX syntax before compilation
        - `open-agents/tools/validate-structure.py` — validate paper section integrity

        ### Outputs
        - `open-agents/output-refined/research/COMPREHENSIVE_EVIDENCE_EXTRACTION.md`
        - `open-agents/output-refined/research/CITATION_MAP.md`
        - Updated `latex/references/references.bib` (via Reference Manager)

        ### Quality Checklist
        - [ ] Inventory all sources before extraction
        - [ ] Use exact quotes with page numbers where available
        - [ ] Map findings to sections (§02–§12)
        - [ ] Maintain Harvard citation format
        - [ ] Note gaps explicitly; do not hide missing evidence
        - [ ] Add/validate BibTeX entries as you go
        - [ ] Update citation map with each finding
        - [ ] Produce handoff document for next agent

        ---

        ## Citation Workflows

        These workflows are executed by the Reference Manager and integrated across agents:

        - extract-citations: Parse LaTeX and markdown to extract all citations and direct quotes
        - validate-citations: Verify all citations match `references.bib` and appear in text
        - citation-completeness: Check required BibTeX fields per source type
        - format-bibliography: Generate Harvard-style bibliography in `output-refined/references/`

        Integration points:
        - Section Drafter inserts `\cite{}` placeholders; Reference Manager resolves
        - Research Librarian adds/updates BibTeX entries during extraction
        - LaTeX Assembler validates that all citations resolve during build
        
        ---
        
        ## Artifacts & Rigor
        
        Agents should consistently apply PhD-level rigor and leverage existing research artifacts across the project:
        
        - Primary artifact locations:
          - open-agents/planning/20251218-group-tutor-reviews/tasks-artifacts
          - open-agents/planning/20251218-group-tutor-reviews/research-artifacts
        - When documents are renamed or moved (e.g., into tasks-artifacts), agents must update their inventories and continue processing—do not skip prior work.
        - Revisit previously reviewed sources as needed; deeper quotes, validations, and philosophical framing often emerge on second pass.
        - Maintain section mapping (§02–§12) for every extracted finding and enforce Harvard citation style, including page numbers for direct quotes.
        
        These practices apply to Research Librarian, Research Consolidator, Section Drafter, Quality Refiner, and Reference Manager.

         ↓
    .paper/core/agents/section-drafter.md (full agent definition—loaded on demand)
         ↓
    Agent executes, produces output, updates memory
```

This three-layer architecture:
- **Keeps initial context small** (only INSTRUCTIONS.md at start)
- **Scales efficiently** (full agent defs load only when needed)
- **Enables complex workflows** (agents can reference each other)

### What Each Layer Does

| Layer | File | Role |
|-------|------|------|
| Entry | `AGENTS.md` | Quick reference, tool detection, pointer to instructions |
| Index | `open-agents/INSTRUCTIONS.md` | This file—agent catalog, routing, workflow documentation |
| Agents | `.paper/core/agents/*.md` and `.paper/specialist/agents/*.md` | Full agent definitions (canonical source of truth) |

> **Note:** Legacy agent files in `open-agents/agents/` are deprecated. See `.paper/` for canonical definitions.

---

## Project Structure

### The open-agents/ Container

```
open-agents/
├── README.md                    # Human-readable system intro
├── INSTRUCTIONS.md              # This file—full documentation
│
├── agents/                      # ⚠️ DEPRECATED - see .paper/
│   └── DEPRECATED.md            # Migration notice
│
├── tools/                       # Scripts and tools
│   ├── build-latex.sh          # LaTeX compilation script
│   ├── validate-structure.py   # Paper structure validator
│   ├── lint-latex.sh           # LaTeX syntax checking
│   ├── format-references.py    # Reference formatter (Harvard)
│   └── extract-evidence.sh     # Forensic audit extraction
```

### Canonical Agent Definitions (.paper/)

```
.paper/
├── core/agents/                 # Core paper writing agents
│   ├── latex-assembler.md
│   ├── paper-architect.md
│   ├── quality-refiner.md
│   ├── reference-manager.md
│   ├── research-consolidator.md
│   └── section-drafter.md
│
├── specialist/agents/           # Support agents
│   ├── brainstorm.md
│   ├── librarian.md
│   ├── problem-solver.md
│   └── tutor.md
│
├── _cfg/                        # Configuration and manifests
│   ├── agents/                  # YAML agent metadata
│   ├── workflows/               # Workflow definitions
│   ├── tools/                   # Tool definitions
│   └── guides/                  # Style guides
```
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
 
### 7. Research Librarian (`agents/research_librarian.md`)

**Purpose:** Conduct comprehensive, systematic evidence extraction from collected PDFs and sources, ensuring academic integrity and providing exhaustive quotable findings mapped to paper sections.

**When to use:**
- User requests an audit of collected sources or “extract all evidence”
- Gaps remain for claims requiring direct quotations or quantitative anchors
- Need to inventory sources, verify accessibility, and standardize extraction outputs

**Input:** PDFs and source files under `open-agents/source/reference-materials/` or user-provided paths

**Output:**
- Exhaustive evidence documents in `open-agents/output-refined/research/`
- Updated `latex/references/references.bib` via Reference Manager
- Citation map and audit report files in `open-agents/output-refined/research/`

See full agent spec in [.paper/specialist/agents/librarian.md](.paper/specialist/agents/librarian.md).


| User says... | Agent to Use | Output Location |
|--------------|--------------|-----------------|
| "Research..." or "consolidate research on..." | Research Consolidator | `output-refined/research/` |
| "Outline the paper" or "structure the paper" | Paper Architect | `output-drafts/outlines/` |
| "Draft the introduction" or "draft [section]" | Section Drafter | `output-drafts/sections/` |
| "Refine this draft" or "improve quality" | Quality Refiner | `output-refined/sections/` |
| "Format references" or "create bibliography" | Reference Manager | `output-refined/references/` |
| "Assemble the paper" or "build document" | LaTeX Assembler | `latex/main.tex`, `output-final/pdf/` |

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

```bash
cd latex/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The `build-latex.sh` tool automates this.

---

## Managing the System

> **Important:** Agent definitions now live in `.paper/`. The `open-agents/agents/` directory is deprecated.

### Adding a New Agent

1. Create `.paper/core/agents/{name}.md` or `.paper/specialist/agents/{name}.md` following the anatomy template
2. Create invocation command in your IDE agent system (Copilot Chat/Codex prompt) or run `paperkit generate`
3. Add to agent manifest in `.paper/_cfg/agent-manifest.yaml`
4. Commit

### Editing an Agent

1. Locate `.paper/core/agents/{name}.md` or `.paper/specialist/agents/{name}.md`
2. Modify behaviors, update output locations if needed
3. Run `paperkit generate` to update IDE-specific files
4. Commit

### Removing an Agent

1. Delete the agent file from `.paper/core/agents/` or `.paper/specialist/agents/`
2. Remove from `.paper/_cfg/agent-manifest.yaml`
3. Run `paperkit generate` to clean up IDE files
4. Commit

---

## Git Commit Protocol

Commit frequently in logical batches:

```bash
# After each agent completes a task
git add open-agents/output-drafts/sections/introduction.tex
git commit -m "Draft: introduction section (2500 words)"

# After research consolidation
git add open-agents/output-refined/research/
git commit -m "Research: consolidate color science foundations"

# After refinement pass
git add open-agents/output-refined/sections/
git commit -m "Refine: introduction for clarity and flow"

# After assembly and successful build
git add latex/
git add open-agents/output-final/pdf/
git commit -m "Assemble: integrate all sections, compile successful"
```

**Commit message format:**
```
{action}: {description}

Optional body with details about changes made,
decisions, or notes for the reader.
```

**Actions:** Draft, Refine, Research, Assemble, Add, Update, Remove

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

## Quick Start Checklist

- [ ] Read this INSTRUCTIONS.md completely
- [ ] Review desired paper scope and goals with the Paper Architect
- [ ] Gather and consolidate research materials with Research Consolidator
- [ ] Create paper outline with Paper Architect
- [ ] Begin drafting sections with Section Drafter
- [ ] Iteratively refine with Quality Refiner
- [ ] Manage references throughout with Reference Manager
- [ ] Build and validate final document with LaTeX Assembler

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

This Open Agent System provides:

✓ **Six specialized agents** for research, structuring, drafting, refining, referencing, and assembly  
✓ **Modular LaTeX architecture** for efficient context and parallel work  
✓ **Progressive disclosure** (load agents on demand, not all at once)  
✓ **Iterative refinement** support for academic quality  
✓ **Memory system** to track state without context bloat  
✓ **Automation tools** for building, linting, validating  
✓ **Clear workflows** for planning, drafting, and publication  
✓ **Academic rigor** with Harvard referencing and proper citations  

To begin: Follow the routing logic above to invoke the appropriate agent for your current task.
