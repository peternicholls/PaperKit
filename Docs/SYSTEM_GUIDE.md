# PaperKit — Quick Start Guide

Welcome to PaperKit! This is your complete system for writing high-quality academic papers with 10 specialized agents.

---

## 🎯 What You Have Now

A **document-first, agentic workflow** for writing academic papers in LaTeX with:

- **10 specialized agents** (6 core + 4 specialist) that guide you through the entire process
- **Multi-IDE support** — Works with GitHub Copilot (VS Code) or OpenAI Codex
- **Modular LaTeX** — 12 atomic section files for clean version control
- **Progressive refinement** — Multiple passes to improve clarity and quality
- **Citation management** — Harvard style (Cite Them Right) with validation
- **Build automation** — One command compiles your document to PDF
- **Core Framework** — All definitions centralized in `.paperkit/`
- **Forensic audit tools** — Extract evidence from PDFs with page numbers

`.paperkit/` is the source of truth; `.github/agents/`, `.codex/prompts/`, AGENTS.md, and COPILOT.md are generated from it.

---

## ⚡ Quick Start (3 Steps)

### 1. Initialize Your System

Run the initialization command:

```bash
./paperkit init
```

This will:
- Verify dependencies (LaTeX, Python, Git)
- Generate IDE-specific files
- Validate your setup
- Show you what's ready

**Safe to rerun anytime** to repair or update generated assets.

### 2. Activate an Agent

**In GitHub Copilot (VS Code):**
1. Open Copilot Chat (Cmd+Shift+I or Ctrl+Shift+I)
2. Click the mode selector at the top
3. Select `paper-architect` from the dropdown
4. Agent presents a menu with available workflows

**In OpenAI Codex:**
1. Type `/paper-architect` in your editor
2. Agent activates and shows options

### 3. Follow the Workflow Loop

```
Define Scope → Outline → Research → Draft → Refine → Validate Citations → Assemble PDF
```

Each agent handles one phase. See the routing guide below.

---

## 🧭 Agent Routing Guide

### Quick Reference Table

| Your Request | Use This Agent | Output Location | When to Use |
|--------------|---------------|-----------------|-------------|
| "Brainstorm ideas for..." | **Brainstorm Coach** | `planning/YYYYMMDD-session/` | Exploring angles, hypotheses, and scope |
| "Outline the paper" | **Paper Architect** | `.paperkit/data/output-drafts/outlines/`<br>`latex/sections/` (skeleton) | After you know your topic and scope |
| "Find sources for..." | **Research Librarian** | `planning/YYYYMMDD-session/` | Need evidence with page numbers |
| "Consolidate research" | **Research Consolidator** | `.paperkit/data/output-refined/research/` | After gathering materials |
| "Draft [section name]" | **Section Drafter** | `latex/sections/` | Ready to write a specific section |
| "Refine this draft" | **Quality Refiner** | `latex/sections/` (in place) | After first draft; can repeat 2-3 times |
| "Review this section" | **Review Tutor** | `planning/YYYYMMDD-session/` | Want expert feedback on quality |
| "Validate citations" | **Reference Manager** | `latex/references/references.bib` | Before final assembly |
| "I'm stuck on..." | **Problem Solver** | `planning/YYYYMMDD-session/` | Troubleshooting blockers |
| "Assemble the paper" | **LaTeX Assembler** | `.paperkit/data/output-final/pdf/` | All sections refined and ready |

---

## 📁 Folder Structure You'll Use

```
PaperKit/
├── .paperkit/                      ← Core Framework (EDIT HERE)
│   ├── _cfg/                       ← Manifests, schemas, guides
│   │   ├── manifest.yaml           ← System version info
│   │   ├── agent-manifest.yaml     ← All agents catalog
│   │   ├── workflow-manifest.yaml  ← All workflows catalog
│   │   ├── tool-manifest.yaml      ← All tools catalog
│   │   ├── agents/                 ← Agent metadata (YAML)
│   │   ├── workflows/              ← Workflow definitions (YAML)
│   │   ├── tools/                  ← Tool metadata (YAML)
│   │   ├── guides/                 ← Harvard citation guide, style guides
│   │   └── schemas/                ← JSON Schemas for validation
│   │
│   ├── core/agents/                ← Core agent specifications (6)
│   │   ├── research-consolidator.md
│   │   ├── paper-architect.md
│   │   ├── section-drafter.md
│   │   ├── quality-refiner.md
│   │   ├── reference-manager.md
│   │   └── latex-assembler.md
│   │
│   ├── specialist/agents/          ← Specialist agent specifications (4)
│   │   ├── brainstorm.md
│   │   ├── problem-solver.md
│   │   ├── tutor.md
│   │   └── librarian.md
│   │
│   ├── tools/                      ← Tool implementations
│   │   ├── build-latex.sh
│   │   ├── lint-latex.sh
│   │   ├── extract-evidence.sh
│   │   ├── validate-structure.py
│   │   └── format-references.py
│   │
│   ├── docs/                       ← IDE-specific instructions
│   │   ├── github-copilot-instructions.md
│   │   └── codex-instructions.md
│   │
│   └── data/                       ← Agent outputs (DO NOT EDIT)
│       ├── output-drafts/          ← First drafts
│       │   └── outlines/
│       ├── output-refined/         ← Iterated versions
│       │   ├── research/
│       │   └── references/
│       └── output-final/           ← Created on build
│           └── pdf/
│
├── latex/                          ← Publication document
│   ├── main.tex                    ← Main document (integrates all)
│   ├── preamble.tex                ← Packages and configuration
│   ├── metadata.tex                ← Title, author, abstract
│   ├── settings.tex                ← Customization and macros
│   │
│   ├── sections/                   ← 12 atomic section files
│   │   ├── ...
│   │
│   ├── appendices/                 ← Supplementary material
│   │   ├── ...
│   │
│   └── references/
│       └── references.bib          ← BibTeX database (Harvard style)
│
├── .github/agents/                 ← Generated Copilot chat modes
│   └── paper-*.agent.md            ← One file per agent (DO NOT EDIT)
│
├── .codex/prompts/                 ← Generated Codex prompts
│   └── paper-*.md                  ← One file per agent (DO NOT EDIT)
│
├── AGENTS.md                       ← Generated quick reference (DO NOT EDIT)
├── COPILOT.md                      ← Generated integration guide (DO NOT EDIT)
│
├── planning/                       ← Session outputs from specialist agents
│   └── YYYYMMDD-session-name/      ← Planning sessions, brainstorms, feedback
│
└── open-agents/                    ← Legacy system (kept for reference)
```

---

## 🎓 Typical Workflow Example

### Scenario: Writing a Specification Paper on Color Science

**Step 1: Brainstorm and Scope** (Brainstorm Coach)
```
User: "I want to write about mathematical color perception models."
→ Agent explores: What angle? Who's the audience? What's novel?
→ Output: Session notes in planning/20251219-color-perception/
```

**Step 2: Create Structure** (Paper Architect)
```
User: "Outline a paper on color perception for researchers. 10,000 words."
→ Agent creates 12-section outline with research requirements
→ Output: .paperkit/data/output-drafts/outlines/color-perception-outline.md
→ Also creates: latex/sections/*.tex skeleton files
```

**Step 3: Find Evidence** (Research Librarian)
```
User: "Find sources on cone cell responses. Extract key quotes with page numbers."
→ Agent searches, extracts evidence with context
→ Output: planning/20251219-color-perception/evidence-cone-cells.md
```

**Step 4: Consolidate Research** (Research Consolidator)
```
User: "Synthesize the evidence on color theory foundations."
→ Agent creates coherent research document with citations
→ Output: .paperkit/data/output-refined/research/color-theory-foundations.md
```

**Step 5: Draft Introduction** (Section Drafter)
```
User: "Draft §01 Introduction. Motivate color perception modeling."
→ Agent writes 2000-word introduction with citations, logical flow
→ Output: latex/sections/01_introduction.tex
```

**Step 6: Refine Introduction** (Quality Refiner)
```
User: "Refine §01. The transitions feel rushed."
→ Agent improves transitions, strengthens arguments, polishes prose
→ Output: latex/sections/01_introduction.tex (refined in place)
```

**Step 7: Get Feedback** (Review Tutor, optional)
```
User: "Review §01 for academic quality."
→ Agent provides constructive critique and suggestions
→ Output: planning/20251219-color-perception/feedback-intro.md
```

**Repeat Steps 5-7** for each section (§02-§12)

**Step 8: Validate Citations** (Reference Manager)
```
User: "Validate all citations and format bibliography."
→ Agent checks citations, validates BibTeX, formats Harvard style
→ Output: latex/references/references.bib (validated)
→ Also: .paperkit/data/output-refined/references/citation-report.md
```

**Step 9: Final Assembly** (LaTeX Assembler)
```
User: "Assemble the paper. Build the document."
→ Agent integrates all sections, validates syntax, compiles PDF
→ Output: .paperkit/data/output-final/pdf/main.pdf
```

**Result:** Publication-ready PDF with 10,000 words, 12 sections, proper citations

---

## 🛠️ Available Tools

You can run these scripts from the terminal:

```bash
# Build the LaTeX document (compile to PDF with proper BibTeX handling)
./.paperkit/tools/build-latex.sh [--clean] [--final]

# Check LaTeX syntax before compilation
./.paperkit/tools/lint-latex.sh

# Extract evidence from PDFs with page numbers (forensic audit)
./.paperkit/tools/extract-evidence.sh <pdf_dir> <output_md> [search_terms...]

# Validate paper structure
python3 ./.paperkit/tools/validate-structure.py

# Format and validate bibliography (Harvard style)
python3 ./.paperkit/tools/format-references.py --validate latex/references/references.bib
```

---

## 🎯 Essential Commands

### System Management
```bash
./paperkit init                           # Initialize/repair generated assets
./paperkit generate                       # Regenerate all IDE files
./paperkit generate --check               # Check what's out of sync
./paperkit generate --target=copilot      # Regenerate Copilot only
./paperkit generate --target=codex        # Regenerate Codex only
./paperkit validate                       # Validate schemas & structure
./paperkit version                        # Show version
./paperkit help                           # Show help
```

### Build & Validation
```bash
# Build PDF (3-pass LaTeX + BibTeX)
./.paperkit/tools/build-latex.sh

# Build with cleanup
./.paperkit/tools/build-latex.sh --clean

# Build final version (cleanup + optimize)
./.paperkit/tools/build-latex.sh --final

# Check syntax before building
./.paperkit/tools/lint-latex.sh

# Validate structure
python3 ./.paperkit/tools/validate-structure.py

# Check bibliography
python3 ./.paperkit/tools/format-references.py --validate latex/references/references.bib
```

---

## 🎓 Academic Standards

This system enforces:

- **Harvard referencing** (Cite Them Right, 11th edition) for all citations
- **Proper LaTeX semantics** (equations, cross-references, figures, tables)
- **Academic tone** (formal, objective, well-reasoned)
- **Logical structure** (introduction → foundations → methods → results → conclusion)
- **Iterative improvement** (draft → refine → feedback → redraft → polish)
- **Citation integrity** (every claim is cited or clearly original)
- **Page numbers** for all direct quotes
- **Open access** sources preferred
- **Never fabricate** - flag uncertainties for verification

---

## 🚨 Important Notes

### Start with Scope
Don't start writing immediately. Start with **goal definition** and **brainstorming**.

Ask **Brainstorm Coach** to explore ideas, then **Paper Architect** to outline FIRST. This prevents rework and false starts.

### Use Agents in Order
Don't skip steps:
```
Brainstorm → Architect → Librarian → Consolidator → Drafter → Refiner → References → Assembler
```

Jumping steps creates quality problems and requires more rework.

### Iterate Responsibly
It's normal and healthy to refine sections 2-3 times:
```
Draft → Refine → Get Feedback → Refine Again → Done
```

Multiple refinement passes produce better results than trying to write perfect first drafts.

### Keep Files Organized
- **Edit only in** `.paperkit/` (source of truth)
- **Let agents write to** `latex/sections/` (drafts and refinements)
- **Planning outputs** go to `planning/YYYYMMDD-session/`
- **Never edit** `.github/agents/`, `.codex/prompts/`, AGENTS.md, COPILOT.md

This keeps your work clean, trackable, and regenerable.

### Regenerate After Changes
Whenever you edit `.paperkit/`, regenerate:
```bash
./paperkit generate
./paperkit validate
git add .paperkit/ .github/ .codex/ AGENTS.md COPILOT.md
git commit -m "Update agent definitions"
```

---

## 💡 Pro Tips

- **Save often:** Git commit after each agent completes a task
- **Ask questions:** Agents will ask you to clarify if uncertain
- **Iterate freely:** Early drafts don't have to be perfect
- **Trust the process:** Multiple refinement passes produce better results
- **Use the tools:** Run `lint-latex.sh` before assembly to catch issues early
- **Get feedback:** Use Review Tutor to identify improvement opportunities
- **Extract evidence first:** Use Research Librarian to get quotes with page numbers before writing
- **Check citations early:** Validate references throughout, not just at the end
- **Read agent menus:** Each agent presents a menu of workflows when activated

---

## 🤝 Need Help?

### Quick Questions
- **Understanding the system?** Read [Docs/ARCHITECTURE.md](ARCHITECTURE.md)
- **Which agent to use?** Check routing table above
- **How to cite?** See `.paperkit/_cfg/guides/harvard-citation-guide.md`
- **How to draft?** See `.paperkit/core/agents/section-drafter.md`
- **How to compile?** Run `./.paperkit/tools/build-latex.sh`

### Documentation
- **[README.md](../README.md)** — Main system overview
- **[AGENTS.md](../AGENTS.md)** — Quick reference for all agents
- **[COPILOT.md](../COPILOT.md)** — GitHub Copilot integration
- **[Docs/ARCHITECTURE.md](ARCHITECTURE.md)** — System architecture
- **[Docs/SETUP_COMPLETE.md](SETUP_COMPLETE.md)** — Setup checklist

### IDE-Specific
- **GitHub Copilot:** `.paperkit/docs/github-copilot-instructions.md`
- **OpenAI Codex:** `.paperkit/docs/codex-instructions.md`

---

## 🎉 You're Ready!

Your PaperKit system is fully set up and ready to use.

**Begin by running:**
```bash
./paperkit init
```

Then open your IDE, activate the **Brainstorm Coach** or **Paper Architect**, and tell them what you want to write.

The agents will guide you through the entire process from idea to publication-ready PDF.

---

**Happy writing! 📝**

Remember: Edit in `.paperkit/`, regenerate with `./paperkit generate`, and let the agents handle the rest.
