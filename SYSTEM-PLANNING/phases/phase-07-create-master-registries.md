# Phase 7: Create Master Registries

Registries created in Phase 1 act as single source of truth.

**Usage example:** When user types `/paper.plan`, the system:
1. Looks up `/paper.plan` in `commands.yaml`
2. Finds routing: `agent: "paper-architect"`, `spec-file: "commands/paper/plan.yaml"`
3. Loads the command spec (inputs, outputs, workflow)
4. Loads the agent spec from `agents.yaml`: `spec-file: "agents/core/paper-architect.yaml"`
5. Invokes the agent with proper context

---

