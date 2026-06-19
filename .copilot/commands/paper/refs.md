# /paper.refs — Reference Manager

Purpose: manage bibliography entries and citation formatting.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/reference_manager.md](../../../open-agents/agents/reference_manager.md).

Inputs to collect:
- New sources or citation keys
- Desired operations (add sources, validate bibliography, format references)

Outputs:
- Updated [latex/references/references.bib](../../../latex/references/references.bib)
- Reports to [open-agents/output-refined/references](../../../open-agents/output-refined/references)
- Update [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with bibliography changes, outstanding citation gaps, and next steps.

Behavior notes:
- Maintain Harvard style and consistent citation keys.
- Use [open-agents/tools/format-references.py](../../../open-agents/tools/format-references.py) when requested; gate with consent.
