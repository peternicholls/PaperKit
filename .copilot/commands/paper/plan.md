# /paper.plan — Paper Architect

Purpose: design the paper structure. Follow the pointer pattern and keep context small.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/paper_architect.md](../../../open-agents/agents/paper_architect.md).

Inputs to collect:
- Paper topic and scope
- Audience and target length
- Deadlines or constraints
- Standards flexibility (strict academic vs pragmatic) and known gaps/constraints from [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md)

Outputs:
- Outline to [open-agents/output-drafts/outlines](../../../open-agents/output-drafts/outlines)
- LaTeX section skeletons in [latex/sections](../../../latex/sections) if requested
- Update [open-agents/memory/paper-metadata.yaml](../../../open-agents/memory/paper-metadata.yaml)
- Update working handoff at [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with goals, constraints, gaps, next steps.

Behavior notes:
- Ask clarifying questions when scope is vague.
- Do not preload other agent specs.
- No build tools needed; skip consent gate unless a tool is requested.
