# Implementation Plan: Agent System Upgrade - 5-Phase Enhancement

**Branch**: `001-agent-system-upgrade` | **Date**: 2026-01-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-agent-system-upgrade/spec.md`

## Summary

Transform PaperKit's agent system from a fragmented 3-part architecture (YAML metadata, MD frontmatter, legacy paths) into a unified, composable platform with:
1. **Single source of truth** for agent metadata (Phase 1)
2. **Reusable skills framework** for capability composition (Phase 2)
3. **Intelligent orchestration** with intent classification and workflow generation (Phase 3)
4. **Programmatic tool integration** with consent management (Phase 4)
5. **Production observability** with metrics, versioning, and A/B testing (Phase 5)

## Technical Context

**Language/Version**: Python 3.8+ (compatible with existing tooling)  
**Primary Dependencies**: PyYAML >=6.0, jsonschema >=4.0, pytest (testing), sqlite3 (stdlib)  
**Storage**: SQLite for metrics (90-day retention), YAML files for definitions, JSON schemas for validation  
**Testing**: pytest with 80% minimum coverage target  
**Target Platform**: macOS/Linux CLI, GitHub Copilot Chat, VS Code integration  
**Project Type**: Single project with modular architecture  
**Performance Goals**: <100ms routing (single intent), <500ms workflow generation (multi-intent), <2s response time (95th percentile)  
**Constraints**: Backward compatible during 2-week migration, per-tool session-scoped consent, 5-level skill depth limit  
**Scale/Scope**: 10 agents, 16 workflows, 5-10 initial skills, ~50 tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Library-First | ✅ PASS | Skills framework creates reusable, testable units |
| CLI Interface | ✅ PASS | All validation tools expose CLI; JSON + human output |
| Test-First | ✅ PASS | 80% coverage required; acceptance scenarios defined |
| Integration Testing | ✅ PASS | Multi-component workflows tested end-to-end |
| Observability | ✅ PASS | Phase 5 adds comprehensive metrics and logging |
| Simplicity | ✅ PASS | Phased rollout; skills limited to 5 depth levels |

**Gate Decision**: ✅ PROCEED - No violations

## Project Structure

### Documentation (this feature)

```text
specs/001-agent-system-upgrade/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file
├── research.md          # Phase 0: Technical research findings
├── data-model.md        # Phase 1: Entity definitions
├── quickstart.md        # Phase 1: Developer onboarding
├── contracts/           # Phase 1: API contracts
│   ├── skill-schema.json
│   ├── metrics-api.yaml
│   └── tool-registry-api.yaml
└── tasks.md             # Phase 2: Task breakdown (via /speckit.tasks)
```

### Source Code (repository root)

```text
.paperkit/
├── _cfg/
│   ├── agents/*.yaml           # Agent metadata (single source of truth)
│   ├── skills/                 # NEW: Skill definitions
│   │   ├── cite-source.yaml
│   │   ├── validate-citation.yaml
│   │   ├── draft-section.yaml
│   │   ├── research-topic.yaml
│   │   └── compile-latex.yaml
│   ├── schemas/
│   │   ├── agent-schema.json   # Existing
│   │   ├── skill-schema.json   # NEW
│   │   └── metrics-schema.json # NEW
│   ├── routing.registry.yaml   # Enhanced with confidence thresholds
│   └── consent.registry.yaml   # NEW: Tool consent preferences
├── core/agents/*.md            # Instructions only (no frontmatter)
├── specialist/agents/*.md      # Instructions only (no frontmatter)
├── tools/
│   ├── check-agents.py         # Updated: duplicate detection, path fixes
│   ├── validate-skills.py      # NEW
│   ├── skill-executor.py       # NEW
│   ├── tool-registry.py        # NEW
│   ├── consent-manager.py      # NEW
│   └── metrics-collector.py    # NEW
└── data/
    └── metrics.db              # NEW: SQLite metrics storage

docs/dev/
├── PATHS.md                    # NEW: Canonical path reference
├── SKILLS.md                   # NEW: Skills framework guide
└── MIGRATION.md                # NEW: Migration playbook

tests/
├── unit/
│   ├── test_skill_loader.py
│   ├── test_orchestrator_router.py
│   └── test_tool_registry.py
├── integration/
│   ├── test_skill_execution.py
│   ├── test_workflow_generation.py
│   └── test_consent_flow.py
└── contract/
    ├── test_agent_schema.py
    └── test_skill_schema.py
```

**Structure Decision**: Single project extending existing `.paperkit/` structure. New directories for skills, metrics, and consent management. All validation tools remain in `.paperkit/tools/`.

## Complexity Tracking

> No constitution violations requiring justification.

| Aspect | Complexity Level | Justification |
|--------|------------------|---------------|
| Skills Framework | Medium | Required for capability composition; limited to 5 depth levels |
| Orchestration | Medium | Multi-intent detection adds value; <500ms constraint keeps it simple |
| Tool Consent | Low | Session-scoped default minimizes storage complexity |
| Metrics | Low | SQLite with 90-day auto-cleanup; no external dependencies |
