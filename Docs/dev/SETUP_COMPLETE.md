# Setup and Readiness Checklist

This checklist tracks the current PaperKit installation status. PaperKit is driven from `.paperkit/`; generated files live in `.github/agents/`, `.codex/prompts/`, AGENTS.md, and COPILOT.md.

## Core Framework

- [x] `.paperkit/` present with `_cfg/`, `core/`, `specialist/`, `tools/`, `docs/`, and `data/`.
- [x] CLI entrypoints `paperkit`, `paperkit-generate*.sh`, `paperkit-validate.py` available.
- [x] Generated references (AGENTS.md, COPILOT.md) present; regenerated via `./paperkit generate`.

## Agents (10)

- [x] Core agents defined: research-consolidator, paper-architect, section-drafter, quality-refiner, reference-manager, latex-assembler.
- [x] Specialist agents defined: brainstorm, problem-solver, tutor, librarian.
- [x] Copilot/Codex chat modes generated in `.github/agents/` and `.codex/prompts/`.

## Documentation

- [x] Docs refreshed: [Docs/ARCHITECTURE.md](ARCHITECTURE.md), [Docs/SYSTEM_GUIDE.md](SYSTEM_GUIDE.md), [Docs/README_SYSTEM.md](README_SYSTEM.md).
- [x] IDE usage guides: `.paperkit/docs/github-copilot-instructions.md`, `.paperkit/docs/codex-instructions.md`.
- [x] Legacy reference retained: `open-agents/`.

## LaTeX Infrastructure

- [x] `latex/main.tex`, `preamble.tex`, `metadata.tex`, `settings.tex`.
- [x] 12 section files under `latex/sections/` and appendices A–D under `latex/appendices/`.
- [x] `latex/references/references.bib` present.

## Outputs & Data Staging

- [x] `.paperkit/data/output-drafts/outlines/` created.
- [x] `.paperkit/data/output-refined/research/` and `references/` created.
- [ ] `.paperkit/data/output-final/` (created automatically on first build).

## Tooling

- [x] Build: `./.paperkit/tools/build-latex.sh`.
- [x] Lint: `./.paperkit/tools/lint-latex.sh`.
- [x] Evidence: `./.paperkit/tools/extract-evidence.sh`.
- [x] Validation: `./.paperkit/tools/validate-structure.py`, `./.paperkit/tools/format-references.py`.

## Validation & Sync

- [x] `./paperkit generate --check` runs to detect drift between `.paperkit/` and generated files.
- [x] `./paperkit validate` available for schema/structure checks.

## Ready Status

- Overall: **Ready** once `output-final/` is produced by a build.

## Next Steps

1) Run `./paperkit init` (safe to rerun) to ensure generated assets match `.paperkit/`.
2) Use Copilot Chat → select `paper-architect` → request an outline for your topic.
3) Build with `./.paperkit/tools/build-latex.sh` after sections and references are in place.
