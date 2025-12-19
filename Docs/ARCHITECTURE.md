# System Architecture and File Overview

PaperKit is a document-first, agentic workflow for writing academic papers with verifiable citations. The source of truth lives in `.paperkit/`; IDE-facing files are generated from there.

## Core Layout (Source of Truth → Generated → Outputs)

```
PaperKit/
├── .paperkit/                      ← Core Framework (edit here)
│   ├── _cfg/                       ← manifests, schemas, guides
│   ├── core/agents/                ← core agent specs (6)
│   ├── specialist/agents/          ← specialist agent specs (4)
│   ├── tools/                      ← build, lint, validate, evidence
│   ├── docs/                       ← IDE usage guides
│   └── data/                       ← agent outputs (drafts/refined)
│       ├── output-drafts/
│       │   └── outlines/
│       └── output-refined/
│           ├── research/
│           └── references/
│           # output-final/ is created by build workflows when needed
│
├── .github/agents/                 ← Generated Copilot chat modes
├── .codex/prompts/                 ← Generated Codex prompts
├── AGENTS.md, COPILOT.md           ← Generated reference files
│
├── latex/                          ← Publication document
│   ├── main.tex
│   ├── preamble.tex
│   ├── metadata.tex
│   ├── settings.tex
│   ├── sections/                   ← Atomic sections (12)
│   │   ├── ...
│   ├── appendices/
│   │   ├── ...
│   └── references/
│       └── references.bib
│
├── paperkit                       ← CLI entrypoint for generation/validation
├── paperkit-generate*.sh          ← Helpers for regenerating derived files
└── open-agents/                   ← Legacy system (kept for reference)
```

## Agent System (10 agents)

### Core Paper Writing Agents (6)

| Agent | Role | Located | Generated Mode |
|-------|------|---------|----------------|
| 🔬 **Research Consolidator** | Synthesize research into coherent documents | `.paperkit/core/agents/research-consolidator.md` | `paper-research-consolidator` |
| 🏗️ **Paper Architect** | Design structure, create outlines, establish flow | `.paperkit/core/agents/paper-architect.md` | `paper-architect` |
| ✍️ **Section Drafter** | Write sections with academic rigor | `.paperkit/core/agents/section-drafter.md` | `paper-section-drafter` |
| 💎 **Quality Refiner** | Improve clarity, flow, coherence | `.paperkit/core/agents/quality-refiner.md` | `paper-quality-refiner` |
| 📚 **Reference Manager** | Manage citations, format bibliography (Harvard) | `.paperkit/core/agents/reference-manager.md` | `paper-reference-manager` |
| 🔧 **LaTeX Assembler** | Integrate sections, validate, compile PDF | `.paperkit/core/agents/latex-assembler.md` | `paper-latex-assembler` |

### Specialist Support Agents (4)

| Agent | Role | Located | Generated Mode |
|-------|------|---------|----------------|
| 🧠 **Brainstorm Coach** | Generate ideas, explore alternatives | `.paperkit/specialist/agents/brainstorm.md` | `paper-brainstorm` |
| 🧩 **Problem Solver** | Identify blockers, analyze root causes | `.paperkit/specialist/agents/problem-solver.md` | `paper-problem-solver` |
| 🎓 **Review Tutor** | Provide feedback, critique drafts | `.paperkit/specialist/agents/tutor.md` | `paper-tutor` |
| 📖 **Research Librarian** | Find sources, extract evidence, forensic audit | `.paperkit/specialist/agents/librarian.md` | `paper-librarian` |

---

## 🎯 Agent Routing Map

```
User Input
    │
    ├─→ "Brainstorm ideas for..."
    │   └─→ Brainstorm Coach
    │       └─→ planning/YYYYMMDD-session/
    │
    ├─→ "Outline the paper" or "Create structure"
    │   └─→ Paper Architect
    │       └─→ .paperkit/data/output-drafts/outlines/
    │           latex/sections/ (skeleton)
    │
    ├─→ "Find sources for..." or "Extract evidence"
    │   └─→ Research Librarian
    │       └─→ planning/YYYYMMDD-session/ (evidence logs)
    │
    ├─→ "Research [topic]" or "Consolidate research"
    │   └─→ Research Consolidator
    │       └─→ .paperkit/data/output-refined/research/
    │
    ├─→ "Draft [section]" or "Write the intro"
    │   └─→ Section Drafter
    │       └─→ latex/sections/
    │
    ├─→ "Refine this draft" or "Improve clarity"
    │   └─→ Quality Refiner
    │       └─→ latex/sections/ (refined in place)
    │
    ├─→ "Review this section" or "Give feedback"
    │   └─→ Review Tutor
    │       └─→ planning/YYYYMMDD-session/ (feedback notes)
    │
    ├─→ "Validate citations" or "Format bibliography"
    │   └─→ Reference Manager
    │       └─→ latex/references/references.bib
    │           .paperkit/data/output-refined/references/
    │
    ├─→ "I'm stuck on..." or "Help me solve..."
    │   └─→ Problem Solver
    │       └─→ planning/YYYYMMDD-session/ (analysis)
    │
    └─→ "Assemble the paper" or "Build the document"
        └─→ LaTeX Assembler
            └─→ .paperkit/data/output-final/pdf/main.pdf
```

---

## 📈 Progressive Refinement Pipeline

```
INPUT                    AGENTS                   OUTPUT
────────────────────────────────────────────────────────────────────

Ideas/Scope          ─→  Brainstorm Coach     ─→  planning/sessions/
Hypothesis              Problem Solver             (exploration notes)

Scope/Goals          ─→  Paper Architect      ─→  .paperkit/data/output-drafts/
Research Needs                                      outlines/
                                                    latex/sections/ (skeleton)

Research Questions   ─→  Research Librarian   ─→  planning/sessions/
PDF Sources                                         (evidence with page numbers)

Research Notes       ─→  Research             ─→  .paperkit/data/output-refined/
Papers                  Consolidator              research/
Links                                              (synthesized docs)

Outline              ─→  Section Drafter      ─→  latex/sections/
Research Synthesis                                 (draft .tex files)

Draft Sections       ─→  Quality Refiner      ─→  latex/sections/
                        Review Tutor               (refined .tex files)
                                                   planning/sessions/feedback

Refined Sections     ─→  Reference Manager    ─→  latex/references/references.bib
Scattered Citations                                .paperkit/data/output-refined/
                                                   references/

All Refined          ─→  LaTeX Assembler      ─→  .paperkit/data/output-final/pdf/
Sections + Bib                                     (compiled PDF)
```

---

## 🔄 Data Flow Architecture

```
┌────────────────────────────────────────────────────────────┐
│  USER INTERACTION LAYER                                    │
│  (You talking to agents via Copilot/Codex)                │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  AGENT LAYER (10 Specialized Agents)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Brainstorm│  │Architect │  │Librarian │  │Research  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │Drafter   │  │Refiner   │  │Tutor     │  │RefMgr    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│  ┌──────────┐  ┌──────────┐                               │
│  │Solver    │  │Assembler │                               │
│  └──────────┘  └──────────┘                               │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  WORKFLOW LAYER (Progressive Refinement)                   │
│  Brainstorm → Plan → Research → Draft → Refine → Assemble │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  OUTPUT LAYER (Multiple Stages)                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
│  │Planning    │  │Drafts      │→ │Refined     │→          │
│  │(sessions)  │  │(rough)     │  │(iterated)  │           │
│  └────────────┘  └────────────┘  └────────────┘           │
│                                         │                   │
│                                         ▼                   │
│                                   ┌────────────┐            │
│                                   │Final       │            │
│                                   │(ready)     │            │
│                                   └────────────┘            │
└────────────────────┬───────────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────────┐
│  STORAGE LAYER (File System)                               │
│  .paperkit/ (source), latex/ (document), generated/        │
└────────────────────────────────────────────────────────────┘
```

---

## ✨ Key System Properties

### Architecture Quality
- ✓ Modular agent design (no overlap, clear responsibilities)
- ✓ Source of truth in `.paperkit/` with generated IDE layers
- ✓ Clear separation of concerns (10 specialized agents)
- ✓ Progressive disclosure (agents load on demand)
- ✓ Atomic LaTeX sections (12 small, manageable files)
- ✓ Schema validation for consistency

### User Experience
- ✓ Clear routing (which agent for which task)
- ✓ Simple entry point (AGENTS.md, SYSTEM_GUIDE.md)
- ✓ Multi-IDE support (Copilot, Codex, extensible)
- ✓ Comprehensive documentation (20,000+ words)
- ✓ Organized folder structure (source → generated → output)
- ✓ Automated build process (one command to PDF)
- ✓ Menu-driven agent interactions

### Academic Quality
- ✓ Harvard citation management (Cite Them Right, 11th ed.)
- ✓ Professional LaTeX configuration
- ✓ Formal writing standards enforced
- ✓ Logical paper structure (12 sections + appendices)
- ✓ Bibliography integrity checking
- ✓ Forensic audit capability (evidence extraction with page numbers)
- ✓ Citation validation workflows

### Development Workflow
- ✓ Git version control friendly
- ✓ Clean separation of concerns
- ✓ Logical file organization
- ✓ Regeneration from source (no drift)
- ✓ Validation tooling (schema + structure)
- ✓ Professional structure

---

## 🎓 How Agents Work Together

```
┌──────────────────────────────────────────────────────────┐
│ User: "I want to write a paper on X"                     │
└─────────────────┬────────────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │ Brainstorm Coach│
         │ (explore ideas) │
         └────────┬────────┘
                  │
         ┌────────▼────────┐
         │ Paper Architect │
         │ (create outline)│
         └────────┬────────┘
                  │
         ┌────────▼──────────────────┐
         │ Creates outline           │
         │ Defines section structure │
         │ Plans research needs      │
         └────────┬──────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
    ▼                           ▼
Research Librarian      Section Drafter
(finds evidence)        (writes sections)
    │                           │
    ▼                           ▼
Research Consolidator   Quality Refiner
(synthesizes)           (improves draft)
    │                           │
    └─────────────┬─────────────┘
                  │
         ┌────────▼────────────┐
         │ Review Tutor        │
         │ (provides feedback) │
         └────────┬────────────┘
                  │
         ┌────────▼────────────────┐
         │ Reference Manager       │
         │ (validates citations)   │
         └────────┬────────────────┘
                  │
         ┌────────▼──────────────┐
         │ LaTeX Assembler       │
         │ (builds final PDF)    │
         └────────┬──────────────┘
                  │
              FINAL PDF
             (ready to share)
```

---

## 🔧 Tool Integration Points

```
build-latex.sh
├─→ cd latex/
├─→ pdflatex main.tex (first pass)
├─→ bibtex main (process bibliography)
├─→ pdflatex main.tex (second pass - resolve citations)
├─→ pdflatex main.tex (third pass - resolve cross-refs)
├─→ mkdir -p ../.paperkit/data/output-final/pdf/
└─→ cp main.pdf ../.paperkit/data/output-final/pdf/

lint-latex.sh
├─→ Check braces matching {}
├─→ Check math delimiters $ $$
├─→ Check environments (begin/end pairs)
├─→ Check citation keys exist in .bib
├─→ Check section files referenced in main.tex exist
└─→ Report issues with line numbers

validate-structure.py
├─→ Verify all 12 section files present
├─→ Check appendices A-D exist
├─→ Verify references.bib exists
├─→ Parse section completeness
└─→ Generate status report

format-references.py
├─→ Parse references.bib
├─→ Validate BibTeX format
├─→ Check required fields (author, title, year, etc.)
├─→ Validate Harvard style compliance
└─→ Report missing/incomplete entries

extract-evidence.sh
├─→ Convert PDFs to text (pdftotext)
├─→ Grep for search terms
├─→ Extract context (±3 lines)
├─→ Include page numbers
└─→ Output markdown with citations
```

---

## 📊 System Statistics

| Category | Count | Purpose |
|----------|-------|---------|
| **Core Agents** | 6 | Research, architecture, drafting, refining, references, assembly |
| **Specialist Agents** | 4 | Brainstorming, problem-solving, tutoring, library research |
| **LaTeX Sections** | 12 | Atomic section files (01-12) |
| **LaTeX Appendices** | 4 | Supplementary material (A-D) |
| **Build Scripts** | 5 | Build, lint, validate, format, extract |
| **CLI Commands** | 10+ | init, generate, validate, build, etc. |
| **Generated Files** | 20+ | Copilot agents, Codex prompts, docs |
| **Documentation Files** | 10+ | Guides, architecture, setup, instructions |

---

## 📋 Reading Order (Recommended)

```
FOR QUICK START (15 minutes)
1. Docs/SYSTEM_GUIDE.md - 5 min (quick start)
2. AGENTS.md - 3 min (agent reference)
3. This file (Docs/ARCHITECTURE.md) - 7 min (understand structure)

FOR COMPLETE UNDERSTANDING (45 minutes)
1. All of above - 15 min
2. README.md - 15 min (full system overview)
3. .paperkit/docs/github-copilot-instructions.md - 10 min (IDE usage)
4. COPILOT.md - 5 min (integration notes)

FOR SPECIFIC TASKS (on demand)
- .paperkit/core/agents/[agent-name].md (agent details)
- .paperkit/specialist/agents/[agent-name].md (specialist agents)
- .paperkit/_cfg/guides/harvard-citation-guide.md (citation style)

FOR DEVELOPMENT/CUSTOMIZATION
- .paperkit/_cfg/schemas/ (validation schemas)
- .paperkit/_cfg/workflows/ (workflow definitions)
- .paperkit/_cfg/tools/ (tool metadata)
```

---

## 🚀 System Activation Sequence

When you start using PaperKit:

```
1. Run ./paperkit init
   ↓ (generates IDE files, validates setup)
   
2. Read Docs/SYSTEM_GUIDE.md
   ↓ (understand workflow)
   
3. Open Copilot Chat, select paper-architect
   ↓ (or use Codex with /paper-architect)
   
4. Define your paper's scope and goals
   ↓
   
5. Paper Architect creates outline
   ↓ (outline in .paperkit/data/output-drafts/outlines/)
   
6. Research Librarian finds evidence
   ↓ (evidence with page numbers in planning/)
   
7. Research Consolidator synthesizes
   ↓ (consolidated docs in .paperkit/data/output-refined/research/)
   
8. Section Drafter writes sections (iterate)
   ↓ (sections in latex/sections/)
   
9. Quality Refiner improves sections (iterate)
   ↓ (refined in place)
   
10. Review Tutor provides feedback (optional)
   ↓ (feedback in planning/)
   
11. Reference Manager validates citations
   ↓ (updates latex/references/references.bib)
   
12. LaTeX Assembler builds PDF
   ↓
   
FINAL PDF in .paperkit/data/output-final/pdf/ ✓
```

---

## 🔄 Regeneration & Governance

### Source of Truth Principle

`.paperkit/` is the **only** place to edit agents, workflows, and tools:
- Agent definitions: `.paperkit/core/agents/` and `.paperkit/specialist/agents/`
- Workflows: `.paperkit/_cfg/workflows/`
- Tools: `.paperkit/tools/` (implementations) and `.paperkit/_cfg/tools/` (metadata)
- Schemas: `.paperkit/_cfg/schemas/`
- Guides: `.paperkit/_cfg/guides/`

### Generated Files (Do Not Edit Directly)

These are auto-generated from `.paperkit/`:
- `.github/agents/paper-*.agent.md` (Copilot chat modes)
- `.codex/prompts/paper-*.md` (Codex prompts)
- `AGENTS.md` (quick reference)
- `COPILOT.md` (integration guide)

### Regeneration Workflow

```bash
# 1. Edit source in .paperkit/
vim .paperkit/core/agents/paper-architect.md

# 2. Check what's out of sync
./paperkit generate --check

# 3. Regenerate all derived files
./paperkit generate

# 4. Validate everything
./paperkit validate

# 5. Commit both source and generated
git add .paperkit/ .github/ .codex/ AGENTS.md COPILOT.md
git commit -m "Update Paper Architect agent"
```

### Academic Integrity Enforcement

All agents follow strict principles:
- **Cite every source** - never summarize or quote without attribution
- **Include page numbers** - direct quotes must have exact page reference
- **Harvard style** - Cite Them Right, 11th edition format
- **Open access preferred** - use accessible, reputable sources
- **Never fabricate** - if uncertain, flag for verification rather than guess
- **Forensic audit** - evidence extraction includes context and page numbers

---

## ✅ System Readiness

- [x] 10 specialized agents fully defined
- [x] Complete documentation (20,000+ words)
- [x] LaTeX template with 12 sections + 4 appendices
- [x] Build and validation tools (5 scripts)
- [x] Multi-IDE support (Copilot, Codex)
- [x] Regeneration system (source → generated)
- [x] Schema validation framework
- [x] Citation workflows (extract, validate, format)
- [x] Forensic audit capability
- [x] Academic integrity enforcement

**Status: COMPLETE AND READY ✅**

---

**Everything is in place. Begin when you're ready!**
