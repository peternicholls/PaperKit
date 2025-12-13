# Migration Guide

This document maps the old system structure to the new BMAD-inspired configuration-driven architecture.

## Overview

The system has been restructured from a flat markdown-based approach to a modular YAML-driven architecture. This enables:

- **Configuration-driven routing** — Commands map to agents via YAML registries
- **Declarative workflows** — Multi-phase operations defined in YAML
- **Protected memory** — System state isolated in `.copilot/memory/`
- **Modular agents** — Each agent has both spec (`.md`) and config (`.yaml`)

## Directory Mapping

### Agents

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `open-agents/agents/research_consolidator.md` | `.copilot/agents/core/research-consolidator.yaml` | YAML config; markdown kept for reference |
| `open-agents/agents/paper_architect.md` | `.copilot/agents/core/paper-architect.yaml` | Dashed naming convention |
| `open-agents/agents/section_drafter.md` | `.copilot/agents/core/section-drafter.yaml` | |
| `open-agents/agents/quality_refiner.md` | `.copilot/agents/core/quality-refiner.yaml` | |
| `open-agents/agents/reference_manager.md` | `.copilot/agents/core/reference-manager.yaml` | |
| `open-agents/agents/latex_assembler.md` | `.copilot/agents/core/latex-assembler.yaml` | |
| (new) | `.copilot/agents/specialist/brainstorm.yaml` | New specialist agent |
| (new) | `.copilot/agents/specialist/problem-solver.yaml` | New specialist agent |
| (new) | `.copilot/agents/specialist/tutor.yaml` | New specialist agent |
| (new) | `.copilot/agents/specialist/librarian.yaml` | New specialist agent |
| (new) | `.copilot/agents/paper-system.yaml` | System orchestrator |

### Memory

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `open-agents/memory/paper-metadata.yaml` | `.copilot/memory/paper-metadata.yaml` | Copied to protected location |
| `open-agents/memory/research-index.yaml` | `.copilot/memory/research-index.yaml` | |
| `open-agents/memory/section-status.yaml` | `.copilot/memory/section-status.yaml` | |
| `open-agents/memory/working-reference.md` | `.copilot/memory/working-reference.md` | |
| `open-agents/memory/revision-log.md` | `.copilot/memory/revision-log.md` | |

### Commands

Commands are now defined as YAML files in `.copilot/commands/paper/`:

| Command | YAML File |
|---------|-----------|
| `paper.init` | `.copilot/commands/paper/init.yaml` |
| `paper.objectives` | `.copilot/commands/paper/objectives.yaml` |
| `paper.requirements` | `.copilot/commands/paper/requirements.yaml` |
| `paper.spec` | `.copilot/commands/paper/spec.yaml` |
| `paper.plan` | `.copilot/commands/paper/plan.yaml` |
| `paper.sprint-plan` | `.copilot/commands/paper/sprint-plan.yaml` |
| `paper.tasks` | `.copilot/commands/paper/tasks.yaml` |
| `paper.review` | `.copilot/commands/paper/review.yaml` |
| `paper.research` | `.copilot/commands/paper/research.yaml` |
| `paper.draft` | `.copilot/commands/paper/draft.yaml` |
| `paper.refine` | `.copilot/commands/paper/refine.yaml` |
| `paper.refs` | `.copilot/commands/paper/refs.yaml` |
| `paper.assemble` | `.copilot/commands/paper/assemble.yaml` |

### Workflows

| Workflow | YAML File |
|----------|-----------|
| Initialization | `.copilot/workflows/setup/initialization.yaml` |
| Sprint | `.copilot/workflows/sprint/sprint.yaml` |
| Core Writing | `.copilot/workflows/paper/core-writing.yaml` |

### Configuration

| Purpose | File |
|---------|------|
| System settings | `.copilot/config/settings.yaml` |
| Consent policies | `.copilot/config/consent.yaml` |

### Tools

| Old Location | New Location | Notes |
|--------------|--------------|-------|
| `open-agents/tools/build-latex.sh` | Unchanged | Referenced in `.copilot/tools/tools.yaml` |
| `open-agents/tools/lint-latex.sh` | Unchanged | |
| `open-agents/tools/validate-structure.py` | Unchanged | |
| `open-agents/tools/format-references.py` | Unchanged | |

## Master Registries

All routing is controlled via master registry files:

- `.copilot/agents.yaml` — Agent registry (maps triggers to agents)
- `.copilot/commands.yaml` — Command registry (maps commands to agents)
- `.copilot/workflows.yaml` — Workflow registry (entry points to workflows)

## How Routing Works (New System)

1. **Command invocation**: User types `/paper.plan`
2. **Registry lookup**: System finds command in `commands.yaml`
3. **Agent resolution**: Loads agent config from `agents.yaml`
4. **Workflow check**: Determines if command triggers a workflow
5. **Execution**: Agent performs work with proper context

## What Changed and Why

### Change: Flat → Hierarchical Structure
**Why:** Better organization, clearer responsibility boundaries

### Change: Markdown → YAML Configuration
**Why:** Machine-readable, consistent parsing, easier validation

### Change: Implicit → Explicit Routing
**Why:** Clear command-to-agent mapping, extensibility

### Change: Open Memory → Protected Memory
**Why:** Prevent accidental edits, clear separation of concerns

### Change: Underscores → Dashes in Names
**Why:** Consistency, URL-friendly, YAML key-friendly

## Backward Compatibility

The old `open-agents/` directory structure is preserved. The new `.copilot/` structure runs alongside it. Original markdown specs remain for reference.

## Next Steps

After migration:
1. Run integration tests via Phase 10 procedures
2. Verify all commands route correctly
3. Test workflow execution end-to-end
4. Deprecate old structure once stable
