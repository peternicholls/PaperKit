# Tasks: Agent System Upgrade - 5-Phase Enhancement

**Input**: Design documents from `/specs/001-agent-system-upgrade/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are included where validation and CI integration are required per spec.md

**Organization**: Tasks are organized by phase and user story to enable independent implementation.

## Format: `- [ ] [ID] [P?] [US?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[US#]**: Which user story this task belongs to

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and validation framework

- [ ] T001 Create `docs/dev/PATHS.md` documenting all canonical paths per FR-008
- [ ] T002 [P] Create `.paperkit/_cfg/schemas/` directory if not exists
- [ ] T003 [P] Verify `agent-schema.json` exists and is valid in `.paperkit/_cfg/schemas/`

**Status**: ✅ COMPLETE (2026-01-20)

---

## Phase 2: Foundational - System Consolidation (US1: P1)

**Goal**: All agent metadata in single authoritative location (User Story 1)

**Independent Test**: Run `python .paperkit/tools/check-agents.py --ci` with zero errors

**⚠️ CRITICAL**: Must complete before Phase 2a-5 can begin

### Validation Scripts

- [ ] T004 [US1] Update `check-agents.py` to detect YAML frontmatter in MD files per FR-004
- [ ] T005 [US1] Update all validation script path references from `.paper/` to `.paperkit/` per FR-003
- [ ] T006 [US1] Add manifest completeness validation in `check-agents.py` per FR-005
- [ ] T007 [US1] Implement clear, actionable error messages for all validation failures per FR-007

### Agent Migration

- [ ] T008 [P] [US1] Remove YAML frontmatter from `.paperkit/core/agents/*.md` files per FR-001
- [ ] T009 [P] [US1] Remove YAML frontmatter from `.paperkit/specialist/agents/*.md` files per FR-001
- [ ] T010 [US1] Verify all agent metadata exists exclusively in `.paperkit/_cfg/agents/*.yaml` per FR-002

### CI Integration

- [ ] T011 [US1] Update GitHub Actions workflow to run validation on PR per FR-006
- [ ] T012 [US1] Test CI workflow blocks merge when duplicates or path errors exist

**Status**: ✅ COMPLETE (2026-01-20)

**Checkpoint**: SC-001 through SC-005 verified - agent metadata consolidated

---

## Phase 2a: Agent Skills Framework (US2: P2)

**Goal**: Industry-standard Agent Skills in SKILL.md format (User Story 2 - Skills)

**Independent Test**: Validate all SKILL.md files pass `skill-frontmatter-schema.json`

### Schema and Structure

- [X] T013 [US2] Create `.paperkit/_cfg/skills/` directory structure per FR-2A-01
- [X] T014 [US2] Move `skill-frontmatter-schema.json` from `contracts/` to `.paperkit/_cfg/schemas/` per FR-2A-02
- [X] T015 [US2] Implement SKILL.md frontmatter validator in Python per FR-2A-08

### Skill Migration

- [X] T016 [P] [US2] Create `skills/humanizer/SKILL.md` from existing `humanizer.md` per FR-2A-09
- [X] T017 [P] [US2] Create `skills/academic-writing/SKILL.md` with academic writing instructions
- [X] T018 [P] [US2] Create `skills/latex-best-practices/SKILL.md` with LaTeX guidelines
- [X] T019 [P] [US2] Create `skills/harvard-citations/SKILL.md` with citation instructions

### Agent Integration

- [X] T020 [US2] Add `suggestedSkills` field to `agent-schema.json` per FR-2A-07
- [X] T021 [US2] Implement skill discovery registry (metadata only, <50ms) per FR-2A-06
- [X] T022 [US2] Implement progressive disclosure loading per FR-2A-04

### CI Integration

- [X] T023 [US2] Add SKILL.md validation to CI workflow per FR-2A-08

**Status**: ✅ COMPLETE (2026-01-20) - All 11 Phase 2a tasks done

**Checkpoint**: SC-2A-01 through SC-2A-05 verified - Agent Skills operational

---

## Phase 2b: Compositional Workflows Framework (US2: P2)

**Goal**: YAML workflow orchestration distinct from Agent Skills (User Story 2 - Workflows)

**Independent Test**: Validate all workflow files pass `workflow-schema.json`

### Schema and Structure

- [X] T024 [US2] Create `.paperkit/_cfg/workflows/` directory per FR-009
- [X] T025 [US2] Move `workflow-schema.json` from `contracts/` to `.paperkit/_cfg/schemas/`
- [X] T026 [US2] Update workflow-schema.json to include `skill` field in steps per FR-2B-01

### Workflow Migration

- [X] T027 [P] [US2] Migrate `cite-source.yaml` to `workflows/cite-source.yaml`
- [X] T028 [P] [US2] Migrate `validate-citation.yaml` to `workflows/validate-citation.yaml`
- [X] T029 [P] [US2] Migrate `draft-section.yaml` to `workflows/draft-section.yaml`
- [X] T030 [P] [US2] Migrate `research-topic.yaml` to `workflows/research-topic.yaml`
- [X] T031 [P] [US2] Migrate `compile-latex.yaml` to `workflows/compile-latex.yaml`

### Workflow Registry

- [X] T032 [US2] Implement workflow validator with skill reference support per FR-016
- [X] T033 [US2] Implement workflow registry for agent discovery per FR-014
- [X] T034 [US2] Validate workflow depth limit (5 levels) per FR-013

### CI Integration

- [X] T035 [US2] Add workflow validation to CI workflow per FR-017

**Status**: ✅ COMPLETE (2026-01-20)

**Checkpoint**: SC-006 through SC-010 verified - Workflows operational

---

## Phase 3: Enhanced Orchestration (US3: P2)

**Goal**: Intelligent multi-step task routing (User Story 3)

**Independent Test**: Submit 10 diverse requests, verify correct intent classification

### Intent Classification

- [X] T036 [US3] Implement intent parser extracting goals from requests per FR-018
- [X] T037 [US3] Implement confidence scoring for agent routing per FR-020
- [X] T038 [US3] Implement top-3 fallback when confidence < 0.7 per FR-021
- [X] T039 [US3] Implement tie-break rules for equal scores per FR-022

### Workflow Generation

- [X] T040 [US3] Implement multi-step workflow generator per FR-019
- [X] T041 [US3] Implement dependency resolver for workflow steps
- [X] T042 [US3] Implement workflow presentation for user approval per FR-023
- [X] T043 [US3] Implement step output passing as input per FR-026

### State Management

- [X] T044 [US3] Implement workflow state checkpoint after each step per FR-024
- [X] T045 [US3] Implement workflow resumption from checkpoint per FR-025
- [X] T046 [US3] Create checkpoint storage in `.paperkit/data/checkpoints/`

### Performance

- [X] T047 [US3] Verify <100ms routing for single-intent, <500ms for multi-intent per FR-020

**Checkpoint**: SC-011 through SC-016 verified - Orchestration operational

**Status**: ✅ COMPLETE (2026-01-20)

---

## Phase 4: Tool Integration Layer (US4: P3)

**Goal**: Programmatic tool discovery and invocation (User Story 4)

**Independent Test**: Agent queries registry, gets consent, invokes tool successfully

### Tool Registry

- [ ] T048 [US4] Implement tool registry with discovery API per FR-028
- [ ] T049 [US4] Create tool input/output schema validation per FR-032
- [ ] T050 [US4] Implement tool timeout enforcement per FR-035

### Consent Management

- [ ] T051 [US4] Implement user consent workflow per FR-030
- [ ] T052 [US4] Create consent registry storage per FR-031
- [ ] T053 [US4] Implement session-scoped consent (default) per FR-031
- [ ] T054 [US4] Implement persistent consent opt-in per FR-031

### Execution & Logging

- [ ] T055 [US4] Implement tool invocation in agent runtime
- [ ] T056 [US4] Create audit logging system per FR-033
- [ ] T057 [US4] Implement structured error context per FR-036
- [ ] T058 [US4] Implement fallback strategies per FR-034

**Checkpoint**: SC-017 through SC-021 verified - Tool integration operational

---

## Phase 5: Advanced Features (US5: P3)

**Goal**: Production observability and safe experimentation (User Story 5)

**Independent Test**: Collect metrics from 100 invocations, generate performance report

### Metrics Collection

- [ ] T059 [US5] Create SQLite metrics database per research.md section 5
- [ ] T060 [US5] Implement 90-day retention with auto-cleanup
- [ ] T061 [US5] Implement metrics collection hooks per FR-037
- [ ] T062 [US5] Create metrics dashboard per FR-043

### Agent Versioning

- [ ] T063 [US5] Implement agent versioning with semver per FR-038
- [ ] T064 [US5] Implement compatibility validation per FR-039

### A/B Testing

- [ ] T065 [US5] Implement A/B test traffic split per FR-040
- [ ] T066 [US5] Enforce minimum sample size (30 per variant) per FR-041
- [ ] T067 [US5] Implement gradual rollout per FR-044

### Reporting

- [ ] T068 [US5] Implement performance reports with trends per FR-042
- [ ] T069 [US5] Complete 30-day stability monitoring per SC-026

**Checkpoint**: SC-022 through SC-026 verified - Advanced features operational

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cleanup, final validation

- [ ] T070 [P] Update `docs/dev/SKILLS.md` to document dual architecture
- [ ] T071 [P] Update agent instructions to reference new skill/workflow locations
- [ ] T072 [P] Create migration guide in `docs/dev/MIGRATION.md`
- [ ] T073 Update `workflow-manifest.yaml` with new workflow locations
- [ ] T074 Update `agent-manifest.yaml` with `suggestedSkills` references
- [ ] T075 Run full validation suite against all success criteria
- [ ] T076 Run quickstart.md validation scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (US1) ← BLOCKS ALL BELOW
    ↓
┌───┴───┐
↓       ↓
Phase 2a  Phase 2b  (can run in parallel)
(Skills)  (Workflows)
└───┬───┘
    ↓
Phase 3: Orchestration (US3)
    ↓
Phase 4: Tools (US4)
    ↓
Phase 5: Advanced (US5)
    ↓
Phase 6: Polish
```

### Critical Path

`T001 → T004 → T011 → T013 → T024 → T036 → T048 → T059 → T075`

### User Story Dependencies

| User Story | Can Start After | Can Run Parallel With |
|------------|-----------------|----------------------|
| US1 (Consolidation) | Phase 1 | None (blocking) |
| US2 (Skills/Workflows) | US1 complete | Phase 2a ↔ Phase 2b |
| US3 (Orchestration) | US2 complete | None |
| US4 (Tools) | US3 complete | None |
| US5 (Advanced) | US4 complete | None |

### Parallel Opportunities

**Phase 2 (Foundational)**:
```bash
# T008 and T009 can run in parallel:
"Remove frontmatter from core agents"
"Remove frontmatter from specialist agents"
```

**Phase 2a (Skills)**:
```bash
# T016-T019 can run in parallel:
"Create humanizer SKILL.md"
"Create academic-writing SKILL.md"
"Create latex-best-practices SKILL.md"
"Create harvard-citations SKILL.md"
```

**Phase 2b (Workflows)**:
```bash
# T027-T031 can run in parallel:
"Migrate cite-source.yaml"
"Migrate validate-citation.yaml"
"Migrate draft-section.yaml"
"Migrate research-topic.yaml"
"Migrate compile-latex.yaml"
```

---

## Implementation Strategy

### MVP (Phases 1-2a Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T012)
3. Complete Phase 2a: Agent Skills (T013-T023)
4. **STOP and VALIDATE**: Test skill discovery and validation
5. Usable system with consolidated agents + skills

### Full Implementation

1. MVP + Phase 2b (Workflows)
2. Add Phase 3 (Orchestration)
3. Add Phase 4 (Tools)
4. Add Phase 5 (Advanced)
5. Polish and documentation

---

## Summary

| Phase | Tasks | Estimated Time |
|-------|-------|----------------|
| Phase 1: Setup | 3 | 0.5 day |
| Phase 2: Foundational | 9 | 1.5 days |
| Phase 2a: Agent Skills | 11 | 2 days |
| Phase 2b: Workflows | 12 | 2 days |
| Phase 3: Orchestration | 12 | 3 days |
| Phase 4: Tools | 11 | 2.5 days |
| Phase 5: Advanced | 11 | 3 days |
| Phase 6: Polish | 7 | 1.5 days |
| **Total** | **76** | **~16 days** |

---

## Notes

- [P] tasks can run in parallel (different files, no dependencies)
- [US#] label maps task to specific user story for traceability
- All FR-### references map to spec.md requirements
- All SC-### references map to spec.md success criteria
- Commit after each task or logical group
- Stop at any checkpoint to validate progress
