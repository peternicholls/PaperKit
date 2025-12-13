# /paper.refine — Quality Refiner

Purpose: improve an existing draft section for clarity, coherence, and academic tone.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/quality_refiner.md](../../../open-agents/agents/quality_refiner.md).

Inputs to collect:
- Target section draft path in [open-agents/output-drafts/sections](../../../open-agents/output-drafts/sections) or [open-agents/output-refined/sections](../../../open-agents/output-refined/sections)
- Desired focus areas (clarity, concision, argument strength, etc.)
- Standards flexibility and gap priorities from [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md)

Outputs:
- Refined draft to [open-agents/output-refined/sections](../../../open-agents/output-refined/sections)
- Change summary; update [open-agents/memory/section-status.yaml](../../../open-agents/memory/section-status.yaml)
- Update [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with what changed, remaining gaps, and next steps.

Behavior notes:
- Preserve LaTeX structure and citation placeholders.
- Keep edits scoped to the target section.
- No build tools needed; skip consent gate unless a tool is requested.
