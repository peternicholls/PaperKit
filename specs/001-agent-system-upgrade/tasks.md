# Task Breakdown: Agent System Upgrade - 5-Phase Enhancement

**Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)  
**Created**: 2026-01-20

---

## Phase 1: System Consolidation (Weeks 1-2)

**Goal**: Single source of truth for agent metadata; eliminate path inconsistencies

| Task | Description | Requirements | Exit Criteria | Status |
|------|-------------|--------------|---------------|--------|
| 1.1 | Create `docs/dev/PATHS.md` | FR-008 | Document exists with all canonical paths | ✅ Done |
| 1.2 | Update validation scripts to `.paperkit/` paths | FR-003 | All scripts use correct paths | ✅ Done |
| 1.3 | Remove YAML frontmatter from agent MD files | FR-001, FR-002 | No MD files contain frontmatter | ✅ Done (verified none exist) |
| 1.4 | Implement duplicate detection in `check-agents.py` | FR-004 | Duplicates detected and reported | ✅ Done (already implemented) |
| 1.5 | Add manifest completeness validation | FR-005 | Orphaned agents detected | ✅ Done (already implemented) |
| 1.6 | Update CI workflow | FR-006 | Validation blocks invalid PRs | ✅ Done (already configured) |
| 1.7 | Run full validation suite | FR-007 | Validation runs without crashes | ✅ Done (56/58 pass, 2 expected) |
| 1.8 | Update documentation | FR-048 | All docs reference correct paths | ✅ Done |
| 1.9 | Create migration scripts for agent format upgrade | FR-049 | Scripts convert frontmatter to YAML | ✅ Done |
| 1.10 | Measure baseline code duplication in agent instructions | SC-007 | Baseline report generated for Phase 2 comparison | ✅ Done (22.7% baseline) |

**Success Criteria**: SC-001 through SC-005
**Phase 1 Status**: ✅ COMPLETE (2026-01-20)

---

## Phase 2: Skills Framework (Weeks 3-5)

**Goal**: Reusable skill definitions for capability composition

| Task | Description | Requirements | Exit Criteria |
|------|-------------|--------------|---------------|
| 2.1 | Design `skill-schema.json` | FR-009, FR-011 | Schema validates skill YAML |
| 2.2 | Create `.paperkit/_cfg/skills/` structure | FR-009 | Directory structure exists |
| 2.3 | Implement skill validator (`validate-skills.py`) | FR-010, FR-016, FR-017 | Validates prerequisites/refs |
| 2.4 | Create 5 prototype skills | FR-012 | cite-source, validate-citation, draft-section, research-topic, compile-latex |
| 2.5 | Extend orchestrator with skill registry | FR-014 | Agents can discover skills |
| 2.6 | Test skill invocation from agents | FR-013, FR-015 | Skills execute correctly |
| 2.7 | Document skill creation process | FR-048 | `docs/dev/SKILLS.md` complete |

**Success Criteria**: SC-006 through SC-010

---

## Phase 3: Enhanced Orchestration (Weeks 6-8)

**Goal**: Intelligent multi-step task routing with workflow generation

| Task | Description | Requirements | Exit Criteria |
|------|-------------|--------------|---------------|
| 3.1 | Enhance orchestrator intent classification | FR-018, FR-020 | Single/multi-intent detection |
| 3.2 | Implement dependency resolver | FR-019 | Steps ordered by dependencies |
| 3.3 | Create workflow state machine | FR-024, FR-026 | State transitions work |
| 3.4 | Add checkpoint/resume capability | FR-025 | Resume after interruption |
| 3.5 | Build workflow presentation (conversational UI) | FR-023 | `.paperkit/tools/workflow-presenter.py` outputs step list; user can review/approve via CLI prompts |
| 3.6 | Test with 100 diverse user requests | FR-021, FR-022 | 90% routing accuracy |
| 3.7 | Measure and optimize performance | FR-027 | <500ms workflow generation |

**Success Criteria**: SC-011 through SC-016

---

## Phase 4: Tool Integration Layer (Weeks 9-10)

**Goal**: Programmatic tool discovery, invocation, and consent management

| Task | Description | Requirements | Exit Criteria |
|------|-------------|--------------|---------------|
| 4.1 | Design tool registry API (`tool-registry.py`) | FR-028, FR-029 | Discovery API functional |
| 4.2 | Implement consent management (`consent-manager.py`) | FR-030, FR-031 | Session/persistent consent |
| 4.3 | Add tool invocation to agent runtime | FR-032, FR-035 | Tools invokable with timeout |
| 4.4 | Create audit logging system | FR-033 | All invocations logged |
| 4.5 | Implement error handling and fallbacks | FR-034, FR-036 | Fallbacks execute on failure |
| 4.6 | Test security and consent enforcement | FR-030 | No unconsented executions |

**Success Criteria**: SC-017 through SC-021

---

## Phase 5: Advanced Features (Weeks 11-12)

**Goal**: Production observability with metrics, versioning, and A/B testing

| Task | Description | Requirements | Exit Criteria |
|------|-------------|--------------|---------------|
| 5.1 | Design metrics collection (`metrics-collector.py`) | FR-037 | Metrics stored in SQLite |
| 5.2 | Implement agent versioning | FR-038, FR-039 | Semantic versioning works |
| 5.3 | Create A/B testing framework | FR-040, FR-041 | Traffic split configurable |
| 5.4 | Build metrics dashboard | FR-042, FR-043 | Dashboard displays trends |
| 5.5 | Test gradual rollout capability | FR-044 | 10%→50%→100% rollout works |
| 5.6 | Conduct production readiness review | FR-045 | Checklist complete |
| 5.7 | Complete 30-day stability monitoring | SC-026 | 99.5% uptime achieved |

**Success Criteria**: SC-022 through SC-026

---

## Cross-Cutting Tasks (All Phases)

| Task | Description | Requirements | Phase |
|------|-------------|--------------|-------|
| X.1 | Schema validation for all YAML | FR-046 | All |
| X.2 | Backward compatibility testing (create test suite) | FR-047 | 1-2 |
| X.3 | Test coverage ≥80% | FR-050 | All |

---

## Task Dependencies

```
Phase 1 ─────────────────────────────┐
  └─► Phase 2 ───────────────────────┤
        └─► Phase 3 ─────────────────┤
              └─► Phase 4 ───────────┤
                    └─► Phase 5 ─────┘
```

**Critical Path**: 1.3 → 2.1 → 2.4 → 3.1 → 4.1 → 5.1

---

## Summary

| Phase | Tasks | Duration | Key Deliverables |
|-------|-------|----------|------------------|
| 1 | 10 | 2 weeks | PATHS.md, updated scripts, CI validation, migration scripts |
| 2 | 7 | 3 weeks | skill-schema.json, 5 skills, SKILLS.md |
| 3 | 7 | 3 weeks | Orchestrator, workflow engine, checkpoints |
| 4 | 6 | 2 weeks | Tool registry, consent manager, audit log |
| 5 | 7 | 2 weeks | Metrics, versioning, A/B testing |
| **Total** | **37** | **12 weeks** | Full agent system upgrade |
