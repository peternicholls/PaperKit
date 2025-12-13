# /paper.research — Research Consolidator

Purpose: synthesize research inputs into structured reference docs.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/research_consolidator.md](../../../open-agents/agents/research_consolidator.md).

Inputs to collect:
- Topic or research question
- Available sources or notes locations (e.g., [open-agents/source/research-notes](../../../open-agents/source/research-notes))
- Depth/breadth preference

Outputs:
- Consolidation to [open-agents/output-refined/research](../../../open-agents/output-refined/research)
- Update [open-agents/memory/research-index.yaml](../../../open-agents/memory/research-index.yaml)
- Append/update handoff summary in [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) noting new research docs, gaps resolved/remaining, and next recommendations.

Behavior notes:
- Keep citations honest; use placeholders only when keys are known.
- Use markdown structure defined in the agent spec.
- No build tools needed; skip consent gate unless a tool is requested.
