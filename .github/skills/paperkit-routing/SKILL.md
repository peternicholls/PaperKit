---
name: paperkit-routing
description: Route PaperKit requests to the right agent module using the orchestrator tie-break rules.
---

## Purpose
Use this skill when a request needs routing to a single PaperKit agent.

## Routing rules
Select exactly one agent and do not perform the task yourself. Use these tie-break rules:

- "peer reviewed / cited by / discredited / provenance / credibility" -> librarian
- "help me understand / explain / distil / teach" -> tutor
- "derive / implement / debug / algorithm / model" -> problem-solver
- "harvard / bibtex / biblatex / biber / citations / doi" -> reference-manager
- "latex compile / .tex error / package / build log" -> latex-assembler
- "outline / structure / argument flow" -> paper-architect
- "draft section / write introduction/methods/related work" -> section-drafter
- "polish / rewrite / tighten" -> quality-refiner
- otherwise: research-consolidator (if synthesis) or brainstorm (if ideation)

## Output requirements
When routing:
- Choose exactly one agent.
- Ask a clarifying question only when required inputs are missing.
- Do not fabricate citations, sources, quotes, or attribution.
