# PaperKit Agent Skills

PaperKit exposes Copilot Agent Skills to make routing and defaults discoverable in tools that support skill injection.

## Skills included

### paperkit-routing
Use for routing PaperKit requests to a single agent based on the orchestrator tie-break rules.

Source of truth:
- `.paperkit/core/agents/orchestrator.md`

### paperkit-defaults
Use to apply PaperKit workflow defaults like citation style, output folders, and document class.

Source of truth:
- `.paperkit/core/config.yaml`

## Locations
Project skills are located under `.github/skills/`.
