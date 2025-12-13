## Copilot Research Paper Assistant Kit — GitHub Copilot Integration

Former name: Academic Specification Paper Writing System.

This repo includes Copilot agent and slash-command scaffolding that routes into the existing Open Agent System.

### Entry Points
- Agent role: see [.copilot/agents/paper-system.md](.copilot/agents/paper-system.md) (loads [open-agents/INSTRUCTIONS.md](open-agents/INSTRUCTIONS.md) then the specific agent spec on demand).
- Slash commands: located in [.copilot/commands/paper](.copilot/commands/paper) and map to the six paper agents.

### Commands
- /paper.init → init/intake and working reference update ([.copilot/commands/paper/init.md](.copilot/commands/paper/init.md))
- /paper.plan → Paper Architect ([.copilot/commands/paper/plan.md](.copilot/commands/paper/plan.md))
- /paper.research → Research Consolidator ([.copilot/commands/paper/research.md](.copilot/commands/paper/research.md))
- /paper.draft → Section Drafter ([.copilot/commands/paper/draft.md](.copilot/commands/paper/draft.md))
- /paper.refine → Quality Refiner ([.copilot/commands/paper/refine.md](.copilot/commands/paper/refine.md))
- /paper.refs → Reference Manager ([.copilot/commands/paper/refs.md](.copilot/commands/paper/refs.md))
- /paper.assemble → LaTeX Assembler ([.copilot/commands/paper/assemble.md](.copilot/commands/paper/assemble.md))

### Consent Gate (tools)
- Before first tool run, prompt for scope: Allow once / Allow for this session / Allow for this workspace / Always allow on this machine / Run all requested tools for this session.
- Remember scope in VS Code workspaceState/globalState; keep “once” in-memory. Prefer per-tool scopes to avoid over-granting.
- Optional local log (gitignored): [.vscode/agent-consent.log](.vscode/agent-consent.log). Do not write consent decisions into tracked memory files.

Implementation notes (extensions):
- Use `workspaceState.update` for session/workspace scopes; `globalState.update` for machine-wide.
- Run-all-this-session: store a session flag that expires at session end.
- Provide a palette action to clear stored approvals and optionally truncate the local log.

### Tools to Expose
- Build: [open-agents/tools/build-latex.sh](open-agents/tools/build-latex.sh)
- Lint: [open-agents/tools/lint-latex.sh](open-agents/tools/lint-latex.sh)
- Validate: [open-agents/tools/validate-structure.py](open-agents/tools/validate-structure.py)
- References: [open-agents/tools/format-references.py](open-agents/tools/format-references.py)

### Notes
- Respect progressive disclosure: load only the needed agent spec after [open-agents/INSTRUCTIONS.md](open-agents/INSTRUCTIONS.md).
- Keep outputs in existing folders (output-drafts, output-refined, output-final, latex).
- Maintain the handoff log at [open-agents/memory/working-reference.md](open-agents/memory/working-reference.md) so any agent can resume after interruptions.
