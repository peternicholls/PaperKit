# /paper.draft — Section Drafter

Purpose: draft an individual section in LaTeX with citations and clear flow.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/section_drafter.md](../../../open-agents/agents/section_drafter.md).

Inputs to collect:
- Section name (e.g., Introduction, Methodology)
- Outline context (from [open-agents/output-drafts/outlines](../../../open-agents/output-drafts/outlines))
- Relevant research docs (from [open-agents/output-refined/research](../../../open-agents/output-refined/research))
- Any specific claims or constraints
- Standards flexibility and gaps/priority notes from [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md)

Outputs:
- Draft to [open-agents/output-drafts/sections](../../../open-agents/output-drafts/sections)
- Update [open-agents/memory/section-status.yaml](../../../open-agents/memory/section-status.yaml)
- Update [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with progress, gaps, and next steps.

Behavior notes:
- Use LaTeX markup; include placeholder \cite{} where appropriate.
- Keep context minimal; do not load other agents.
- No build tools needed; skip consent gate unless a tool is requested.
