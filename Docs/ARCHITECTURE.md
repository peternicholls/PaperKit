# System Architecture and File Overview

System name: Copilot Research Paper Assistant Kit (formerly Academic Specification Paper Writing System).

## 📊 Complete File Structure

```
color-math-spec/
│
├── 📖 DOCUMENTATION (Start Here!)
│   ├── AGENTS.md                    ← ENTRY POINT (read this first)
│   ├── SYSTEM_GUIDE.md              ← Quick start guide
│   ├── SETUP_COMPLETE.md            ← Initialization checklist  
│   ├── README_SYSTEM.md             ← Complete system summary
│   └── COPILOT.md                   ← Integration notes
│
├── 📚 OPEN AGENT SYSTEM
│   └── open-agents/
│       ├── README.md                ← System intro
│       ├── INSTRUCTIONS.md          ← COMPLETE DOCUMENTATION (80+ KB)
│       │
│       ├── agents/                  ← THE AGENTS (6 specialized agents)
│       │   ├── research_consolidator.md      (Research synthesizer)
│       │   ├── paper_architect.md            (Structure designer)
│       │   ├── section_drafter.md            (Writer)
│       │   ├── quality_refiner.md            (Editor)
│       │   ├── reference_manager.md          (Bibliographer)
│       │   └── latex_assembler.md            (Integration engineer)
│       │
│       ├── tools/                   ← BUILD AND VALIDATION
│       │   ├── build-latex.sh       (Compile LaTeX → PDF)
│       │   ├── lint-latex.sh        (Check syntax)
│       │   ├── validate-structure.py (Validate paper structure)
│       │   └── format-references.py (Format bibliography)
│       │
│       ├── memory/                  ← SYSTEM STATE (YAML tracking)
│       │   ├── paper-metadata.yaml      (Paper info, goals, status)
│       │   ├── section-status.yaml      (Track each section's progress)
│       │   ├── research-index.yaml      (Catalog all research)
│       │   └── revision-log.md          (Change history)
│       │
│       ├── source/                  ← YOUR RESEARCH INPUT
│       │   ├── research-notes/      (Research materials & notes)
│       │   ├── ideas/               (Discussions & sparks)
│       │   └── reference-materials/ (PDFs, links, sources)
│       │
│       ├── output-drafts/           ← STAGE 1: FIRST DRAFTS
│       │   ├── outlines/            (Paper structure & outline)
│       │   ├── sections/            (Individual section drafts)
│       │   └── full-versions/       (Complete draft versions)
│       │
│       ├── output-refined/          ← STAGE 2: ITERATED & IMPROVED
│       │   ├── research/            (Synthesized research docs)
│       │   ├── sections/            (Refined section drafts)
│       │   ├── references/          (Formatted bibliography)
│       │   └── full-versions/       (Refined complete versions)
│       │
│       └── output-final/            ← STAGE 3: READY FOR PUBLICATION
│           ├── pdf/                 (Compiled PDFs)
│           └── latex/               (Final LaTeX files)
│
└── 📄 LATEX DOCUMENT (Publication Output)
    └── latex/
        ├── main.tex                 ← MAIN DOCUMENT (integrates all)
        ├── preamble.tex             (Packages, configuration)
        ├── metadata.tex             (Title, author, abstract)
        ├── settings.tex             (Customization, macros)
        │
        ├── sections/                ← ATOMIC SECTION FILES
        │   ├── 01_introduction.tex
        │   ├── 02_background.tex
        │   ├── 03_methodology.tex
        │   ├── 04_results.tex
        │   ├── 05_prior_work.tex
        │   ├── 06_implications.tex
        │   └── 07_conclusion.tex
        │
        ├── appendices/
        │   └── A_supplementary.tex
        │
        └── references/
            └── references.bib       (BibTeX database - Harvard style)
```

---

## 🎯 Agent Routing Map

```
User Input
    │
    ├─→ "Research [topic]"
    │   └─→ Research Consolidator
    │       └─→ output-refined/research/
    │
    ├─→ "Outline the paper"
    │   └─→ Paper Architect
    │       └─→ output-drafts/outlines/
    │
    ├─→ "Draft [section]"
    │   └─→ Section Drafter
    │       └─→ output-drafts/sections/
    │
    ├─→ "Refine this draft"
    │   └─→ Quality Refiner
    │       └─→ output-refined/sections/
    │
    ├─→ "Format references"
    │   └─→ Reference Manager
    │       └─→ output-refined/references/
    │
    └─→ "Assemble the paper"
        └─→ LaTeX Assembler
            └─→ latex/main.tex → output-final/pdf/main.pdf
```

---

## 📈 Progressive Refinement Pipeline

```
INPUT                 AGENTS              OUTPUT
─────────────────────────────────────────────────────────────

Research Notes    ─→  Research         ─→  output-refined/research/
Papers               Consolidator          (Synthesized docs)
Links                                      

Scope/Goals       ─→  Paper            ─→  output-drafts/outlines/
Research Needs       Architect             (Structure, outline)
                                          latex/sections/ (skeleton)

Outline           ─→  Section          ─→  output-drafts/sections/
Research          Drafter             (Draft .tex files)
Citations                               

Draft Sections    ─→  Quality          ─→  output-refined/sections/
User Feedback        Refiner           (Refined .tex files)

Refined Section   ─→  Reference        ─→  latex/references/
Scattered Cites      Manager           references.bib
                                        (Formatted bibliography)

All Refined       ─→  LaTeX            ─→  latex/main.tex
Sections             Assembler         (Integrated)
Bibliography                           output-final/pdf/
                                       (Compiled PDF)
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────┐
│  USER INTERACTION LAYER                             │
│  (You talking to agents)                            │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  AGENT LAYER (6 Specialized Agents)                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │Research  │  │Architect │  │Drafter   │  ...      │
│  └──────────┘  └──────────┘  └──────────┘           │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  WORKFLOW LAYER (Progressive Refinement)            │
│  Research → Outline → Draft → Refine → Assemble     │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  OUTPUT LAYER (Three Stages)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │Drafts    │→ │Refined   │→ │Final     │           │
│  │(rough)   │  │(iterated)│  │(ready)   │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│  STORAGE LAYER (File System)                        │
│  LaTeX files, PDFs, YAML tracking, references       │
└─────────────────────────────────────────────────────┘
```

---

## 📊 File Statistics

| Category | Count | Size | Purpose |
|----------|-------|------|---------|
| **Documentation** | 4 | 5+ KB | Getting started & reference |
| **Agent Specs** | 6 | 50+ KB | Detailed agent specifications |
| **LaTeX Files** | 10 | 5+ KB | Document template & sections |
| **Scripts** | 4 | 2+ KB | Build, lint, validate |
| **Memory Files** | 4 | 1+ KB | Tracking & metadata |
| **Directories** | 20+ | - | Organized workflow stages |
| **Total** | 48+ | 65+ KB | Complete system |

---

## ✨ Key System Properties

### Architecture Quality
- ✓ Modular agent design (no overlap)
- ✓ Clear separation of concerns
- ✓ Progressive disclosure (load on demand)
- ✓ Atomic LaTeX sections (small, manageable files)
- ✓ YAML memory (efficient state tracking)

### User Experience
- ✓ Clear routing (which agent for which task)
- ✓ Simple entry point (AGENTS.md)
- ✓ Comprehensive documentation
- ✓ Organized folder structure
- ✓ Automated build process

### Academic Quality
- ✓ Harvard citation management
- ✓ Professional LaTeX configuration
- ✓ Formal writing standards
- ✓ Logical paper structure
- ✓ Bibliography integrity checking

### Development Workflow
- ✓ Git version control
- ✓ Clean commit history
- ✓ Logical file organization
- ✓ No clutter or temporary files
- ✓ Professional structure

---

## 🎓 How Agents Work Together

```
┌──────────────────────────────────────────────────────┐
│ User: "I want to write a paper on X"                 │
└─────────────────┬──────────────────────────────────┘
                  │
         ┌────────▼────────┐
         │ Paper Architect │
         │ (reads goal)    │
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
Research Consolidator    Section Drafter
(synthesizes research)    (writes sections)
    │                           │
    └─────────────┬─────────────┘
                  │
         ┌────────▼─────────┐
         │ Quality Refiner  │
         │ (improves draft) │
         └────────┬─────────┘
                  │
         ┌────────▼────────────────┐
         │ Reference Manager       │
         │ (manages bibliography)  │
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

## 🚀 System Activation Sequence

When you start using the system:

```
1. You read AGENTS.md
   ↓
2. You read SYSTEM_GUIDE.md
   ↓
3. You read open-agents/INSTRUCTIONS.md
   ↓
4. You define your paper's scope
   ↓
5. You ask Paper Architect to outline
   ↓
6. You provide research materials
   ↓
7. You ask Research Consolidator to synthesize
   ↓
8. You ask Section Drafter to write (iterate)
   ↓
9. You ask Quality Refiner to improve (iterate)
   ↓
10. You ask Reference Manager to format bibliography
   ↓
11. You ask LaTeX Assembler to build
   ↓
FINAL PDF PRODUCED ✓
```

---

## 💾 Memory System Design

```
paper-metadata.yaml
├── title
├── scope
├── goals
├── target_length
├── deadline
├── status (planning|drafting|refining|assembling)
└── progress (0-100)

section-status.yaml
├── introduction
│   ├── status (outline|drafted|refined|final)
│   ├── words
│   ├── completeness (0-100)
│   ├── refinement_passes
│   └── notes
├── background
├── methodology
├── results
├── prior_work
├── implications
└── conclusion

research-index.yaml
└── sources[]
    ├── title
    ├── authors[]
    ├── year
    ├── citation_key
    ├── source_type
    ├── file
    ├── url
    ├── topics[]
    └── notes

revision-log.md
└── entries[]
    ├── date
    ├── agent
    ├── action
    ├── files[]
    ├── notes
    └── status
```

---

## 🔧 Tool Integration Points

```
build-latex.sh
├─→ pdflatex main.tex (first pass)
├─→ bibtex main (bibliography)
├─→ pdflatex main.tex (second pass)
├─→ pdflatex main.tex (third pass)
└─→ Copy to output-final/pdf/

lint-latex.sh
├─→ Check braces matching
├─→ Check math delimiters
├─→ Check environments
├─→ Check citations exist
└─→ Check section files exist

validate-structure.py
├─→ Verify section files
├─→ Check metadata
├─→ Report section status
└─→ Show completion percentage

format-references.py
├─→ Parse bibliography
├─→ Validate BibTeX format
├─→ Check required fields
└─→ Report issues
```

---

## 📋 Reading Order (Recommended)

```
FOR QUICK START (30 minutes)
1. This file (System Architecture) - 10 min
2. AGENTS.md - 5 min
3. SYSTEM_GUIDE.md - 15 min

FOR COMPLETE UNDERSTANDING (90 minutes)
1. All of above - 30 min
2. open-agents/INSTRUCTIONS.md - 60 min

FOR SPECIFIC TASKS (on demand)
- open-agents/agents/[agent_name].md

FOR TROUBLESHOOTING
- SETUP_COMPLETE.md
- open-agents/tools/ help text
```

---

## ✅ System Readiness Checklist

- [x] All 6 agents fully specified
- [x] Complete documentation (15,000+ words)
- [x] LaTeX template with 7 section files
- [x] Build and validation tools (4 scripts)
- [x] Memory system for tracking (4 YAML files)
- [x] Organized folder structure (20+ directories)
- [x] Entry point and quick reference
- [x] Git repository initialized with clean commits
- [x] Academic standards enforced
- [x] Ready for immediate use

**Status: COMPLETE AND READY ✅**

---

**Everything is in place. Begin when you're ready!**
