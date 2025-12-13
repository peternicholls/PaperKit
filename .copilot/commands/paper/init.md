# /paper.init — Session Initialization

Purpose: quickly initialize a session, capture goals, and set up state so any agent can resume seamlessly. Supports user typing `/paper.init`, `*init`, or running an init terminal command wired to this prompt.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Read [open-agents/agents/paper_architect.md](../../../open-agents/agents/paper_architect.md) for goal/structure intake guidance.

Core behaviors:
- Gather essentials without over-questioning: paper goal, audience, length/format, deadline, standards flexibility (strict academic vs. pragmatic), and current progress state.
- Detect user’s working style (brief prompts vs. detailed guidance) and adapt question depth accordingly.
- Record a concise working reference update in [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) summarizing goals, chosen standards, known gaps, next actions.
- If the user jumps straight into tasks without init, perform a lightweight inline intake (no bombardment) and update the working reference doc.

Gap handling:
- If user asks “complete paper” or similar, do not invent missing goals/content. Surface gaps, list options (research now, proceed with placeholders, or defer), and ask for confirmation.
- Respect user marking a gap as unimportant; propose a short plan to proceed, ask for confirmation, then continue.

Outputs:
- Updated working reference doc with current goal/constraints/state.
- Optionally seed outline or metadata when enough info is available (update [open-agents/memory/paper-metadata.yaml](../../../open-agents/memory/paper-metadata.yaml)).

Notes:
- Progressive questions only; avoid unnecessary prompts.
- This command should not run build tools; skip consent gate unless tools are explicitly requested.
