# ⚠️ DEPRECATED: Legacy Agent Definitions

**Deprecation Date:** December 19, 2025  
**Removal Date:** Next major version

## Notice

The agent definitions in this directory (`open-agents/agents/`) are **deprecated**.

### Source of Truth

All canonical agent definitions now live in `.paper/`:
- **Core agents:** `.paper/core/agents/`
- **Specialist agents:** `.paper/specialist/agents/`
- **YAML metadata:** `.paper/_cfg/agents/`

### Migration

If you have customizations in these legacy files:
1. Review the canonical agents in `.paper/`
2. Merge any unique content into the appropriate `.paper` agent
3. Update any scripts referencing `open-agents/agents/` to use `.paper/` paths

### Preserved Content

Unique content from legacy agents (detailed examples, troubleshooting tables, workflow narratives) has been documented in:
- `.paper/docs/legacy-agent-examples.md` (if created)
- Individual agent files in `.paper/core/agents/` and `.paper/specialist/agents/`

### Why This Change?

- **Single source of truth:** `.paper/` is now canonical
- **IDE-agnostic:** Derived layers (`.github/agents/`, `.codex/prompts/`) are generated from `.paper/`
- **Cleaner structure:** Reduces duplication and maintenance burden

### Questions?

See `AGENTS.md` for the current agent system overview.
