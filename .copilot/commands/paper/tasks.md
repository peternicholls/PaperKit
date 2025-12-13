# /paper.tasks — Sprint Task Tracking

Purpose: track user requests and agent progress within a sprint.

Load order:
1) Read [open-agents/INSTRUCTIONS.md](../../../open-agents/INSTRUCTIONS.md).
2) Identify the active sprint folder (latest in `planning/YYYYMMDD-[name]/`).

Inputs to collect:
- New task description (what the user is asking for)?
- Priority (critical / high / medium / low)?
- Is this a new task or an update to an existing one?

Outputs:
- Updated `planning/YYYYMMDD-[name]/tasks.md` with new task (or progress update on existing task).
- Task entry includes: task ID, description, status (not-started / in-progress / blocked / completed), assignee (user / agent), due date if relevant, notes/blockers.
- Updated [open-agents/memory/working-reference.md](../../../open-agents/memory/working-reference.md) with latest task status.

Behavior notes:
- Keep task descriptions clear and actionable.
- Track progress; update status as work completes.
- Flag blockers early (e.g., missing research, unclear requirements).
- This command is called frequently during a sprint to add or update tasks.
- No build tools needed; skip consent gate.
