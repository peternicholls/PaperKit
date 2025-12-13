# Phase 5: Move & Protect Memory

### Files to Migrate

**From:** `open-agents/memory/`  
**To:** `.copilot/memory/`

- `paper-metadata.yaml`
- `research-index.yaml`
- `section-status.yaml`
- `working-reference.md`
- `revision-log.md`

### Create Protection Layer

**New file:** `.copilot/memory/README.md`

```markdown
# Memory Files (System-Managed)

⚠️ These files are system-managed. Do not edit directly.

**Working Reference:** See [working-reference.md](working-reference.md) for a human-readable session handoff.

**System Memory Files:**
- `paper-metadata.yaml` — Project metadata (auto-updated by agents)
- `research-index.yaml` — Research tracking (auto-updated by Research Consolidator)
- `section-status.yaml` — Section progress (auto-updated by agents)
- `revision-log.md` — Change history (auto-updated by agents)

## Updating Memory

Agents update these files during their work. Do not edit manually.

## Questions About Progress?

Read `working-reference.md` — it's designed for human consumption and always kept current by agents.
```

---

