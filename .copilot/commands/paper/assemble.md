# /paper.assemble — LaTeX Assembler

Purpose: integrate refined sections, validate, and build the PDF.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/latex_assembler.md](../../../open-agents/agents/latex_assembler.md).

Inputs to collect:
- Confirm refined sections are ready in [open-agents/output-refined/sections](../../../open-agents/output-refined/sections)
- Confirm bibliography is up to date in [latex/references/references.bib](../../../latex/references/references.bib)
- Any build flags (lint-only, build, validate-only)
- Standards flexibility and any user-marked-unimportant gaps from [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md)

Outputs:
- Integrated LaTeX in [latex](../../../latex)
- Compiled PDF to [open-agents/output-final/pdf](../../../open-agents/output-final/pdf)
- Build/validation logs in the same folder as appropriate
- Update [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with build results, remaining gaps, and final QA/preflight status.

Tools (consent required):
- [open-agents/tools/lint-latex.sh](../../../open-agents/tools/lint-latex.sh)
- [open-agents/tools/validate-structure.py](../../../open-agents/tools/validate-structure.py)
- [open-agents/tools/build-latex.sh](../../../open-agents/tools/build-latex.sh)

Consent gate protocol:
- Before first tool run, prompt: Allow once / Allow for this session / Allow for this workspace / Always allow on this machine / Run all requested tools for this session.
- Remember scope using VS Code workspaceState/globalState and in-memory for once; optionally log locally to [.vscode/agent-consent.log](../../../.vscode/agent-consent.log) (gitignored).
- If user declines, offer lint-only or skip execution.

QA/preflight:
- Offer a preflight checklist (structure validation, citation checks, reference formatting, lint) before final build.
- If gaps remain, surface them and ask if the user wants to proceed with placeholders or pause to address them.
