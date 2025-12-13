# Copilot Research Paper Assistant Kit — Copilot Integration

Former name: Academic Specification Paper Writing System.

This folder defines Copilot custom agents and slash commands that route into the Open Agent System.

## Agent
- paper-system: [.copilot/agents/paper-system.md](agents/paper-system.md)
  - Loads [open-agents/INSTRUCTIONS.md](../open-agents/INSTRUCTIONS.md) then the specific agent spec on demand (progressive disclosure).
  - Applies the consent gate before tool calls.

## Slash Commands — Setup (canonical docs)
- /paper.init → [.copilot/commands/paper/init.md](commands/paper/init.md)
- /paper.objectives → [.copilot/commands/paper/objectives.md](commands/paper/objectives.md)
- /paper.requirements → [.copilot/commands/paper/requirements.md](commands/paper/requirements.md)
- /paper.spec → [.copilot/commands/paper/spec.md](commands/paper/spec.md)

## Slash Commands — Core Workflow
- /paper.plan → [.copilot/commands/paper/plan.md](commands/paper/plan.md)
- /paper.research → [.copilot/commands/paper/research.md](commands/paper/research.md)
- /paper.draft → [.copilot/commands/paper/draft.md](commands/paper/draft.md)
- /paper.refine → [.copilot/commands/paper/refine.md](commands/paper/refine.md)
- /paper.refs → [.copilot/commands/paper/refs.md](commands/paper/refs.md)
- /paper.assemble → [.copilot/commands/paper/assemble.md](commands/paper/assemble.md)

## Slash Commands — Sprint Management
- /paper.sprint-plan → [.copilot/commands/paper/sprint-plan.md](commands/paper/sprint-plan.md)
- /paper.tasks → [.copilot/commands/paper/tasks.md](commands/paper/tasks.md)
- /paper.review → [.copilot/commands/paper/review.md](commands/paper/review.md)

## Specialist Agents
- Brainstorm → [.copilot/agents/brainstorm.md](agents/brainstorm.md) via `/paper.brainstorm [topic]`
- Problem-Solver → [.copilot/agents/problem-solver.md](agents/problem-solver.md) via `/paper.solve [problem]`
- Tutor → [.copilot/agents/tutor.md](agents/tutor.md) via `/paper.tutor-feedback [section]`
- Librarian → [.copilot/agents/librarian.md](agents/librarian.md) via `/paper.librarian-research [topic]`

## Consent Gate
- First tool run asks scope: Allow once / Allow for this session / Allow for this workspace / Always allow on this machine / Run all requested tools for this session.
- Store approvals in VS Code workspaceState/globalState; keep “once” in memory.
- Optional local log (gitignored): [.vscode/agent-consent.log](../.vscode/agent-consent.log). Do not write consent to tracked memory files.

## Tools to Bind (MCP/shell)
- Build: [open-agents/tools/build-latex.sh](../open-agents/tools/build-latex.sh)
- Lint: [open-agents/tools/lint-latex.sh](../open-agents/tools/lint-latex.sh)
- Validate: [open-agents/tools/validate-structure.py](../open-agents/tools/validate-structure.py)
- References: [open-agents/tools/format-references.py](../open-agents/tools/format-references.py)

## Outputs and Memory
- Drafts: [open-agents/output-drafts](../open-agents/output-drafts)
- Refined: [open-agents/output-refined](../open-agents/output-refined)
- Final/PDF: [open-agents/output-final](../open-agents/output-final)
- LaTeX sources: [latex](../latex)
- Memory: [open-agents/memory](../open-agents/memory)
