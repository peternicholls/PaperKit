# /paper.sprint-plan — Sprint Planning

Purpose: create a dated sprint folder and outline methodology, scope, and expected outcomes.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Consult [planning/0000-Project-Overview/](../../../planning/0000-Project-Overview/) canonical docs for context and constraints.

Inputs to collect:
- Sprint name/topic (will create dated folder: `YYYYMMDD-[name]`).
- Goals for this sprint (e.g., draft introduction, research background, refine sections)?
- Methodology (e.g., research first, then draft; or iterate on existing)?
- Expected deliverables and success criteria?
- Any blockers or dependencies?

Outputs:
- New dated sprint folder: `planning/YYYYMMDD-[name]/`
- Sprint plan document: `planning/YYYYMMDD-[name]/plan.md` with outline, methodology, scope, and process.
- Empty `planning/YYYYMMDD-[name]/tasks.md` for task tracking.
- Updated [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with sprint name and current plan.

Behavior notes:
- Help user think through realistic scope for a sprint.
- Plan should be actionable and clear.
- This command creates structure; tasks and review follow.
- No build tools needed; skip consent gate.
