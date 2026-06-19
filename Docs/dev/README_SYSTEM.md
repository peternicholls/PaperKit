# 🎓 PaperKit: System Overview

PaperKit is a document-first, agentic workflow for writing academic papers in LaTeX with verifiable citations. `.paperkit/` is the source of truth for agents, workflows, tools, and schemas; `.github/agents/`, `.codex/prompts/`, AGENTS.md, and COPILOT.md are generated from it.

## What’s Included

- **10 agents** (6 core, 4 specialist) with light personas and menu-based workflows.
- **Core Framework** in `.paperkit/` with manifests, schemas, tools, and IDE guides.
- **LaTeX document** in `latex/` with 12 atomic sections and 4 appendices.
- **Build + validation tools** under `.paperkit/tools/` (build, lint, validate, evidence extraction, reference formatting).
- **Output staging** under `.paperkit/data/` (`output-drafts/`, `output-refined/`; `output-final/` is created on build).
- **Legacy** `open-agents/` directory retained for reference only.

## Start Here (5 minutes)

1) Run `./paperkit init` to set up the repo and regenerate IDE files.
2) Open Copilot Chat and pick an agent (e.g., `paper-architect`).
3) If using Codex, type `/paper-architect` to activate the same agent.
4) Keep `.paperkit/` as the edit point; rerun `./paperkit generate` after changes.

## Current Directory Highlights

- `.paperkit/_cfg/` — manifests, schemas, guides (Harvard citation guide).
- `.paperkit/core/agents/` — core agents: Research Consolidator, Paper Architect, Section Drafter, Quality Refiner, Reference Manager, LaTeX Assembler.
- `.paperkit/specialist/agents/` — Brainstorm Coach, Problem Solver, Review Tutor, Research Librarian.
- `.paperkit/tools/` — `build-latex.sh`, `lint-latex.sh`, `extract-evidence.sh`, `validate-structure.py`, `format-references.py`.
- `.paperkit/data/output-drafts/` — outlines; `.paperkit/data/output-refined/` — research, references.
- `latex/` — `main.tex`, `preamble.tex`, `metadata.tex`, `settings.tex`, 12 sections, appendices A–D, `references/references.bib`.

## Typical Workflow

1) **Scope & outline** — Paper Architect builds outline + section plan.
2) **Research** — Research Librarian finds evidence; Research Consolidator synthesizes notes.
3) **Draft** — Section Drafter writes each LaTeX section.
4) **Refine** — Quality Refiner polishes; Review Tutor optional.
5) **References** — Reference Manager validates citations and formats bibliography.
6) **Assemble** — LaTeX Assembler builds PDF via `.paperkit/tools/build-latex.sh` (creates `output-final/`).

## Commands You’ll Actually Use

- `./paperkit init` — install/repair generated assets.
- `./paperkit generate` — regenerate `.github/agents/`, `.codex/prompts/`, AGENTS.md, COPILOT.md.
- `./paperkit validate` — schema + IDE sync checks.
- `./.paperkit/tools/build-latex.sh [--clean] [--final]` — build PDF.
- `./.paperkit/tools/lint-latex.sh` — preflight LaTeX.
- `python3 ./.paperkit/tools/validate-structure.py` — structure check.
- `python3 ./.paperkit/tools/format-references.py --validate latex/references/references.bib` — bibliography check.

## Academic Integrity (always on)

- Cite everything; include quote text, page numbers, and full references.
- Prefer open-access sources; never fabricate citations.
- Maintain Harvard style (Cite Them Right, 11th ed.).

## Reading Order

1) [Docs/SYSTEM_GUIDE.md](Docs/SYSTEM_GUIDE.md) — quick start.
2) [Docs/ARCHITECTURE.md](Docs/ARCHITECTURE.md) — structure and paths.
3) `.paperkit/docs/github-copilot-instructions.md` or `.paperkit/docs/codex-instructions.md` — IDE usage.
4) AGENTS.md / COPILOT.md — generated references.

## If Something Breaks

- Rerun `./paperkit init` to repair generated assets.
- Run `./paperkit generate --check` to see what’s out of sync.
- Validate with `./paperkit validate` before committing.

Everything else lives in `.paperkit/`. Edit there, regenerate, and keep the LaTeX sections small and reviewable.
