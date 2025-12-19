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
.paperkit/        ← Core Framework (edit here)
    _cfg/           ← manifests, schemas, guides
    core/agents/    ← core agent specs (6)
    specialist/agents/ ← specialist agent specs (4)
    tools/          ← build, lint, validate, evidence, refs
    data/           ← agent outputs (drafts/refined)

latex/            ← publication document
    main.tex, preamble.tex, metadata.tex, settings.tex
    sections/01..12 *.tex, appendices A–D, references/references.bib

.github/agents/   ← generated Copilot chat modes
.codex/prompts/   ← generated Codex prompts
open-agents/      ← legacy reference (do not edit)
```

## Typical Workflow (condensed)

1) **Plan** — Tell `paper-architect`: topic, scope, audience, target length. Review the outline.
2) **Evidence** — Ask `paper-librarian` to locate sources and extract quotes (with page numbers).
3) **Synthesize** — Ask `paper-research-consolidator` to structure notes in `.paperkit/data/output-refined/research/`.
4) **Draft** — Ask `paper-section-drafter` to write one section at a time into `latex/sections/`.
5) **Refine** — Use `paper-quality-refiner` (and `paper-tutor` if you want feedback) to polish.
6) **References** — Run `paper-reference-manager` to validate citations and format bibliography.
7) **Assemble** — Run `./.paperkit/tools/build-latex.sh` (creates `.paperkit/data/output-final/`).

## Essential Commands

- `./paperkit init` — install/repair generated assets.
- `./paperkit generate [--check]` — sync `.paperkit/` → `.github/agents/` + `.codex/prompts/`.
- `./paperkit validate` — schema + sync checks.
- `./.paperkit/tools/build-latex.sh [--clean] [--final]` — build PDF.
- `./.paperkit/tools/lint-latex.sh` — LaTeX preflight.
- `python3 ./.paperkit/tools/validate-structure.py` — structure check.
- `python3 ./.paperkit/tools/format-references.py --validate latex/references/references.bib` — bibliography check.

## Academic Integrity (always on)

- Cite every claim; include quote text and page numbers for direct quotes.
- Prefer open-access sources; never fabricate citations.
- Maintain Harvard style (Cite Them Right, 11th ed.).

## If You Get Stuck

- Rerun `./paperkit init` to repair generated files.
- Run `./paperkit generate --check` to see drift.
- Validate with `./paperkit validate` before builds/commits.
- Check `.paperkit/docs/github-copilot-instructions.md` or `.paperkit/docs/codex-instructions.md` for IDE usage.

Happy writing—keep edits in `.paperkit/`, regenerate often, and use the agents to stay in the loop.
