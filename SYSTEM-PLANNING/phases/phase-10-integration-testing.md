# Phase 10: Integration & Testing

### Wire Copilot Extension

The `paper-system.yaml` agent (router) must:
1. Read from master registries (agents, commands, workflows)
2. Route commands based on registry metadata
3. Load agent YAML specs instead of hardcoding
4. Support workflow orchestration

### Create Validation Script

**File:** `.copilot/tools/validate-system.sh` (shell) or `.copilot/tools/validate.py` (Python)

Checks:
- YAML syntax for all registries and specs
- All referenced files exist
- Agent/command completeness (required fields present)
- No missing prerequisites
- Workflow consistency

### Run End-to-End Tests

1. **Test Setup Workflow:**
   - Run `/paper.init`
   - Verify canonical docs created
   - Check working reference updated

2. **Test Sprint Workflow:**
   - Run `/paper.sprint-plan`
   - Create tasks
   - Run `/paper.review`

3. **Test Writing Workflow:**
   - Run `/paper.plan` (outline)
   - Run `/paper.research` (research)
   - Run `/paper.draft` (draft section)
   - Run `/paper.refine` (refine)
   - Run `/paper.assemble` (build)

---

## Timeline & Dependencies

### Tier 1: Critical Foundation (Weeks 1–2)
- [ ] Create registries (agents.yaml, commands.yaml, workflows.yaml)
- [ ] Create configuration files (settings.yaml, consent.yaml, tools.yaml)
- [ ] Create folder structure
- [ ] Move memory files

### Tier 2: Refactoring Agents (Weeks 2–3)
- [ ] Convert agent specs to YAML
- [ ] Create agent registry metadata
- [ ] Link YAML specs to markdown docs

### Tier 3: Workflow System (Weeks 3–4)
- [ ] Define setup workflow (YAML)
- [ ] Define sprint workflow (YAML)
- [ ] Define writing workflow (YAML)

### Tier 4: Configuration System (Weeks 4–5)
- [ ] Finalize consent policy
- [ ] Finalize system settings
- [ ] Finalize tool registry

### Tier 5: Documentation & Integration (Weeks 5–6)
- [ ] Create all README files
- [ ] Create migration guide
- [ ] Wire up Copilot extension
- [ ] Create validation script

### Tier 6: Testing & Polish (Weeks 6+)
- [ ] End-to-end testing
- [ ] User feedback
- [ ] Refinements

---

## Success Criteria

- [x] Plan completed and documented
- [ ] All agents accessible via registry
- [ ] All commands accessible via registry
- [ ] Workflows explicitly defined
- [ ] Memory protected in `.copilot/`
- [ ] Structure mirrors BMAD's modular approach
- [ ] Configuration-driven (easy to extend)
- [ ] Documentation clear and complete
- [ ] End-to-end workflows functional
- [ ] User can't accidentally edit system configs
- [ ] Validation script passing
- [ ] End-to-end tests passing

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| YAML for config + Markdown for docs | YAML is parseable; markdown is readable. Both together = best of both. |
| Central registries | Single source of truth; easier discovery; better tooling. |
| Move memory to `.copilot/` | Keeps system data separate from user content; prevents accidental corruption. |
| Declarative workflows | Workflows are visible, testable, independent of agent implementations. |
| No XML, use YAML/JSON/CSV | Simpler, more readable, better for human collaboration. |
| BMAD-inspired architecture | Proven pattern; scales from simple to enterprise. |

---

## What Stays the Same

- ✓ `open-agents/INSTRUCTIONS.md` (master guide, still authoritative)
- ✓ `open-agents/agents/*.md` (documentation reference)
- ✓ `open-agents/tools/` (scripts themselves)
- ✓ `latex/` (source files)
- ✓ `planning/` (user documents)
- ✓ Core agent behaviors and capabilities

---

## What Moves/Changes

- ✓ System configuration → `.copilot/` (out of user directories)
- ✓ Memory → `.copilot/memory/` (protected)
- ✓ Agent specs → YAML in `.copilot/agents/` (machine-readable)
- ✓ Command specs → YAML in `.copilot/commands/` (machine-readable)
- ✓ Workflows → Declarative YAML in `.copilot/workflows/` (orchestrated)
- ✓ Agent naming → Dashes instead of underscores (consistency)


