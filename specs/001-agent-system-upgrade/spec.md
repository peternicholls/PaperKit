# Feature Specification: Agent System Upgrade - 5-Phase Enhancement

**Feature Branch**: `001-agent-system-upgrade`  
**Created**: 2026-01-20  
**Status**: Draft  
**Input**: Comprehensive upgrade to the agent system implementing a 5-phase roadmap: consolidation of redundant systems, formalized skills framework for reusable capability composition, enhanced orchestration with intelligent multi-step task routing, seamless tool integration layer, and production-ready advanced features including versioning, metrics, and A/B testing

**Based On**: `docs/dev/AGENT-SYSTEM-ANALYSIS.md` — Analysis of PR #28 "Clean up agent system" changes

## User Scenarios & Testing *(mandatory)*

### User Story 1 - System Consolidation & Path Fixes (Priority: P1)

As a **system maintainer**, I need all agent metadata to exist in a single, authoritative location so that I can maintain consistency and avoid drift between redundant definitions.

**Why this priority**: Fixes critical architectural issues discovered in PR #28 analysis. Without this, the system has three parallel definition systems that can drift apart, causing validation failures and routing errors. This is the foundation for all other improvements.

**Independent Test**: Can be fully tested by running validation scripts (`check-agents.py`) and verifying that all path references are correct, no duplicate metadata exists, and all agents pass schema validation.

**Acceptance Scenarios**:

1. **Given** agent metadata exists in both YAML and Markdown frontmatter, **When** validation runs, **Then** system detects duplicate definitions and flags them as errors
2. **Given** validation scripts reference `.paper/` paths, **When** scripts execute, **Then** all references use `.paperkit/` paths consistently
3. **Given** an agent is defined in YAML, **When** querying agent metadata, **Then** system returns data from YAML files only (not MD frontmatter)
4. **Given** CI runs on a pull request, **When** agent files are modified, **Then** automated validation prevents merging if paths are incorrect or duplicates exist
5. **Given** `agent-manifest.yaml` exists, **When** new agents are added, **Then** manifest automatically includes them and validation ensures completeness

---

### User Story 2 - Skills Framework Creation (Priority: P2)

As an **agent developer**, I need to define reusable skills that agents can invoke so that I can build complex capabilities through composition rather than duplication.

**Why this priority**: Enables the core architectural shift toward composable agent behaviors. Currently, agents duplicate logic (e.g., citation extraction appears in multiple agents). Skills provide a middle layer between workflows and tools for reusable capability composition.

**Independent Test**: Can be tested by creating 3-5 core skills (e.g., `cite-source`, `validate-citation`, `draft-section`), validating their schema compliance, and demonstrating that an agent can invoke a skill declaratively.

**Acceptance Scenarios**:

1. **Given** a skill definition YAML file, **When** validation runs, **Then** skill passes schema validation and prerequisite dependencies are verified
2. **Given** an agent needs citation functionality, **When** agent invokes `cite-source` skill, **Then** skill executes multi-step workflow (extract metadata → format citation) and returns formatted output
3. **Given** a skill requires another skill, **When** skill is invoked, **Then** system automatically resolves and executes prerequisites in correct order
4. **Given** multiple agents need the same capability, **When** each agent invokes the shared skill, **Then** logic is executed consistently without duplication
5. **Given** a new skill is created, **When** added to skills directory, **Then** CI validates schema compliance and skill registry is automatically updated

---

### User Story 3 - Enhanced Orchestration with Intent Classification (Priority: P2)

As a **paper author**, I need the orchestrator to understand complex, multi-step requests so that I can describe my goal once and have the system decompose it into an optimal workflow.

**Why this priority**: Dramatically improves user experience by reducing manual agent selection and task decomposition. Users can state high-level goals (e.g., "Research color perception and draft Related Work") and the system handles routing.

**Independent Test**: Can be tested by submitting 10 diverse user requests, verifying that the orchestrator correctly identifies intents, selects appropriate agents, generates valid workflows, and presents them for user approval before execution.

**Acceptance Scenarios**:

1. **Given** user submits "Research X and draft section Y", **When** orchestrator analyzes request, **Then** system identifies two intents (research + drafting) and creates a 2-step workflow
2. **Given** orchestrator generates a workflow, **When** step 2 requires output from step 1, **Then** dependency is correctly identified and steps execute in order
3. **Given** user request matches multiple agents, **When** orchestrator evaluates routing rules, **Then** system calculates confidence scores and selects highest match or requests clarification
4. **Given** a multi-step workflow is generated, **When** presented to user, **Then** user can review/approve each step before execution begins
5. **Given** workflow execution begins, **When** a step completes, **Then** output is passed as input to dependent steps and state is checkpointed

---

### User Story 4 - Tool Integration Layer (Priority: P3)

As an **agent**, I need to discover and invoke tools programmatically so that I can execute concrete actions (build LaTeX, validate citations) without manual user intervention.

**Why this priority**: Enables agents to take autonomous actions while maintaining user control through consent management. Currently, tools exist but agents reference them manually in instructions without programmatic invocation.

**Independent Test**: Can be tested by having an agent query the tool registry, discover available tools, request user consent for tool execution, invoke a tool (e.g., `build-latex`), and handle success/failure outcomes.

**Acceptance Scenarios**:

1. **Given** an agent needs to compile LaTeX, **When** agent queries tool registry, **Then** system returns `build-latex` tool with input/output schema and consent requirements
2. **Given** a tool requires user consent, **When** agent attempts invocation, **Then** user is prompted for approval before execution
3. **Given** a tool execution fails, **When** error is returned, **Then** agent receives structured error context and can trigger fallback strategy
4. **Given** tool is invoked successfully, **When** execution completes, **Then** output conforms to declared schema and is logged to audit trail
5. **Given** user has previously approved a tool, **When** agent invokes same tool again, **Then** system remembers consent preference (session-based or persistent based on user choice)

---

### User Story 5 - Advanced Features & Production Readiness (Priority: P3)

As a **system administrator**, I need observability into agent performance and the ability to test improvements safely so that I can optimize routing accuracy and gradually roll out changes.

**Why this priority**: Provides production-grade operational capabilities. This is lower priority because basic functionality must work first, but becomes critical for long-term system health and continuous improvement.

**Independent Test**: Can be tested by collecting metrics from 100 agent invocations, generating a performance report, deploying two versions of an agent side-by-side, and demonstrating A/B test result comparison.

**Acceptance Scenarios**:

1. **Given** agents are invoked 100 times, **When** performance report is generated, **Then** metrics include success rate, average completion time, routing accuracy, and user satisfaction scores
2. **Given** two versions of an agent exist, **When** users trigger the agent, **Then** 50% are routed to v1 and 50% to v2 (or custom split ratio)
3. **Given** A/B test runs for defined period, **When** test concludes, **Then** system presents comparison metrics and recommends which version to promote
4. **Given** an agent declares version compatibility, **When** orchestrator evaluates agent, **Then** system verifies dependencies (tools, other agents) meet version requirements
5. **Given** system has run for 1 month, **When** admin reviews metrics dashboard, **Then** trends show routing accuracy improvements and agent performance over time

---

### Edge Cases

**System Consolidation (Phase 1)**:
- What happens when an agent is defined in YAML but missing corresponding MD file? → Validation fails with clear error message indicating orphaned metadata
- What happens when validation detects path references to non-existent files? → CI blocks merge and reports specific broken references
- What happens when two agents claim the same name? → Validation fails with conflict resolution guidance

**Agent Skills (Phase 2a)**:
- What happens when a SKILL.md file has invalid frontmatter? → Schema validation fails with clear error listing missing/invalid fields
- What happens when two skills declare the same name? → Validation fails with conflict resolution guidance
- What happens when an agent references a non-existent skill in `suggestedSkills`? → Warning logged, agent loads without skill suggestions
- What happens when skill instructions exceed 5000 token limit? → Validation warning, skill still loads but triggers progressive disclosure
- What happens when skill directory contains no SKILL.md? → Directory ignored, warning logged

**Compositional Workflows (Phase 2b)**:
- What happens when a workflow declares a prerequisite that doesn't exist? → Schema validation fails with dependency resolution error
- What happens when workflow execution reaches maximum depth (recursive workflows)? → System enforces depth limit (e.g., 5 levels) and returns error
- What happens when a workflow step fails mid-execution (e.g., step 2 of 5 fails)? → System checkpoints completed steps, then offers user choice to retry from failure point or rollback all changes
- What happens when a workflow step's output schema doesn't match next step's input schema? → Validation fails at workflow generation time before execution
- What happens when a workflow requires a tool that isn't installed? → System checks tool availability at workflow generation and prompts user to install missing tools
- What happens when a workflow step references a skill that doesn't exist? → Validation fails with clear error identifying missing skill

**Enhanced Orchestration (Phase 3)**:
- What happens when user request is completely ambiguous (no clear intent)? → Orchestrator returns clarifying questions with suggested interpretations
- What happens when workflow execution is interrupted mid-step? → System checkpoint allows resumption from last completed step
- What happens when confidence scores are tied between multiple agents? → Orchestrator applies explicit tie-break rules (documented in analysis) or requests user selection
- What happens when a workflow step fails? → System offers retry, skip, or abort options based on step criticality

**Tool Integration (Phase 4)**:
- What happens when a tool execution times out? → System applies timeout limit, terminates process, and returns timeout error to agent
- What happens when user denies tool consent? → Agent receives denial notification and must complete task without tool or request alternative approach
- What happens when a tool returns malformed output? → System validates against declared output schema and returns validation error

**Advanced Features (Phase 5)**:
- What happens when A/B test sample size is too small for statistical significance? → System requires minimum sample size (e.g., 30 invocations per variant) before allowing conclusions
- What happens when an agent version is incompatible with current orchestrator? → System logs compatibility error and falls back to last compatible version
- What happens when metric collection fails? → System continues operation but logs metric failure (non-blocking)


## Requirements *(mandatory)*

### Functional Requirements

**Phase 1: System Consolidation (Weeks 1-2)**

- **FR-001**: System MUST eliminate all YAML frontmatter from agent Markdown files, maintaining only behavioral instructions in MD files
- **FR-002**: System MUST store all agent metadata exclusively in `.paperkit/_cfg/agents/*.yaml` files validated against `agent-schema.json`
- **FR-003**: System MUST update all validation scripts to reference `.paperkit/` paths instead of legacy `.paper/` paths
- **FR-004**: System MUST detect and report duplicate agent metadata across YAML and MD files
- **FR-005**: System MUST validate `agent-manifest.yaml` completeness against actual agent files in directory
- **FR-006**: CI workflow MUST block merges when path references are incorrect or agent duplicates exist
- **FR-007**: System MUST provide clear, actionable error messages for all validation failures
- **FR-008**: System MUST document canonical paths in `docs/dev/PATHS.md`

**Phase 2a: Agent Skills (Weeks 3-4)**

- **FR-2A-01**: Agent Skills MUST be defined in `.paperkit/_cfg/skills/{name}/SKILL.md` files following agentskills.io specification
- **FR-2A-02**: SKILL.md files MUST contain YAML frontmatter validated against `skill-frontmatter-schema.json`
- **FR-2A-03**: Skill frontmatter MUST include: `name` (1-64 chars, lowercase+hyphens), `description` (1-1024 chars), and optional `license`, `compatibility`, `allowed-tools`, `metadata`
- **FR-2A-04**: System MUST support progressive disclosure: frontmatter loaded at startup (~100 tokens), full instructions loaded on activation (<5000 tokens)
- **FR-2A-05**: System MUST support three skill activation methods: description matching (automatic), explicit invocation (`/skill {name}`), and agent hints (`suggestedSkills` field)
- **FR-2A-06**: System MUST provide skill discovery registry returning skill metadata without loading full instructions
- **FR-2A-07**: Agents MUST be able to declare `suggestedSkills` array in their metadata referencing available skills
- **FR-2A-08**: CI workflow MUST validate all SKILL.md frontmatter on every commit
- **FR-2A-09**: System MUST migrate existing instruction files (e.g., `humanizer.md`) to `skills/{name}/SKILL.md` format
- **FR-2A-10**: Skill directories MAY contain additional resources (`examples/`, `templates/`) loaded on demand

**Phase 2b: Compositional Workflows (Weeks 5-6)**

- **FR-009**: System MUST define workflows in `.paperkit/_cfg/workflows/*.yaml` files with schema validation
- **FR-010**: System MUST validate workflow prerequisite dependencies at definition time
- **FR-011**: Workflows MUST declare input and output schemas using JSON Schema format
- **FR-012**: System MUST support three workflow types: atomic (single agent/action), composite (multi-step), and conditional (branching logic)
- **FR-013**: System MUST enforce maximum workflow composition depth of 5 levels to prevent infinite recursion
- **FR-014**: System MUST provide workflow registry for agent discovery of available capabilities
- **FR-015**: Workflows MUST specify required agents and tools with version constraints
- **FR-016**: System MUST validate that agents, skills, and tools referenced by workflows actually exist
- **FR-017**: CI workflow MUST validate all workflow definitions on every commit
- **FR-2B-01**: Workflow steps MAY include `skill` field to load Agent Skill context during execution

**Phase 3: Enhanced Orchestration (Weeks 6-8)**

- **FR-018**: Orchestrator MUST analyze user requests to identify single or multiple intents
- **FR-019**: Orchestrator MUST generate multi-step workflows with dependency resolution
- **FR-020**: Orchestrator MUST calculate confidence scores for agent routing using keyword matching and routing registry rules
- **FR-021**: System MUST request user clarification when confidence scores fall below threshold (< 0.7). When no agents meet minimum threshold, system presents top 3 agents with their confidence scores and asks user to select one or rephrase request
- **FR-022**: Orchestrator MUST apply explicit tie-break rules when multiple agents have equal scores
- **FR-023**: System MUST present generated workflows to users for review before execution
- **FR-024**: System MUST checkpoint workflow state after each completed step
- **FR-025**: System MUST support workflow resumption from last checkpoint after interruption
- **FR-026**: System MUST pass output from completed steps as input to dependent steps
- **FR-027**: Orchestrator MUST support parallel execution of independent workflow steps

**Phase 4: Tool Integration Layer (Weeks 9-10)**

- **FR-028**: System MUST provide tool registry with discovery API for agents
- **FR-029**: Tools MUST declare input/output schemas and consent requirements
- **FR-030**: System MUST enforce user consent workflow for tools marked `requiresConsent: true`
- **FR-031**: System MUST remember user consent preferences per-tool with session-scoped duration by default. Users can opt-in to persistent consent for specific tools, storing preferences in user-specific configuration file. Persistent consent can be revoked at any time through settings.
- **FR-032**: Tool invocations MUST validate outputs against declared schemas
- **FR-033**: System MUST log all tool invocations to audit trail with timestamp, agent, inputs, outputs, and status
- **FR-034**: System MUST support fallback strategies when tool execution fails
- **FR-035**: System MUST enforce tool execution timeouts to prevent hanging processes
- **FR-036**: System MUST return structured error context to agents when tools fail

**Phase 5: Advanced Features (Weeks 11-12)**

- **FR-037**: System MUST collect performance metrics: success rate, completion time, routing accuracy, user satisfaction
- **FR-038**: System MUST support agent versioning with semantic version constraints
- **FR-039**: System MUST validate compatibility between agent versions and dependencies (orchestrator, tools, other agents)
- **FR-040**: System MUST support A/B testing with configurable traffic split ratios
- **FR-041**: System MUST require minimum sample size (30 invocations per variant) before declaring A/B test results
- **FR-042**: System MUST generate performance reports with trend analysis over time
- **FR-043**: System MUST provide metrics dashboard showing routing accuracy, agent performance, and system health
- **FR-044**: System MUST support gradual rollout of new agent versions (e.g., 10% → 50% → 100%)
- **FR-045**: System MUST allow community-contributed agents with rating and review capability

**Cross-Cutting Requirements**

- **FR-046**: All YAML files MUST be validated against corresponding JSON schemas before merge
- **FR-047**: System MUST maintain backward compatibility with existing agent invocations during migration
- **FR-048**: Documentation MUST be updated for each phase before implementation begins
- **FR-049**: System MUST provide migration scripts to upgrade existing agents to new formats
- **FR-050**: All new features MUST include automated tests achieving minimum 80% code coverage

### Key Entities

- **Agent**: Represents a specialized AI persona with specific capabilities, constraints, and behavioral instructions. Defined by YAML metadata file (schema, capabilities, I/O contracts) and Markdown instruction file (behavioral prompts, examples, tie-breaks).

- **Agent Skill**: Industry-standard instruction file following agentskills.io specification. Defines HOW to perform a task through SKILL.md files containing YAML frontmatter (name, description, compatibility) and markdown instructions. Loaded via progressive disclosure: metadata at startup (~100 tokens), full instructions on activation (<5000 tokens). Activated by description matching, explicit invocation (`/skill {name}`), or agent hints (`suggestedSkills`). Location: `.paperkit/_cfg/skills/{name}/SKILL.md`. **Intent**: Provide reusable, portable behavioral instructions that work across AI coding agents (VS Code, Claude Code, Cursor, Gemini CLI).

- **Compositional Workflow**: PaperKit-internal YAML orchestration file defining WHAT steps to execute in sequence. Specifies agent assignments, inputs/outputs, and step dependencies. May reference Agent Skills via `skill` field to load contextual instructions during execution. Location: `.paperkit/_cfg/workflows/{name}.yaml`. **Intent**: Coordinate multi-agent, multi-step processes like "research → draft → refine → compile".

- **Workflow**: Multi-step orchestration generated dynamically or defined statically. Contains ordered steps with dependencies, checkpoint locations, and parallel execution groups.

- **Tool**: External executable (script, binary, API) that agents invoke to perform concrete actions. Declares input/output schemas, consent requirements, version, and timeout limits.

- **Routing Registry**: Centralized rules database mapping user intents (keywords, patterns, contexts) to appropriate agents. Includes confidence thresholds, tie-break rules, and hard exclusions.

- **Intent**: Parsed user goal extracted from natural language request. Can be single (one agent needed) or multiple (workflow required). Includes confidence score and matched keywords.

- **Checkpoint**: Workflow execution state snapshot enabling resumption after interruption. Contains completed steps, pending steps, intermediate outputs, and execution context.

- **Metric**: Performance measurement collected during system operation. Types include: success rate, completion time, routing accuracy, user satisfaction score, tool invocation count.

- **Schema**: JSON Schema definition that validates structure and content of YAML files (agents, skills, workflows, tools). Provides contract enforcement and documentation-as-code.

- **Manifest**: Authoritative catalog of system components (agents, workflows, tools, skills). Automatically generated from file system and validated for completeness.

### Assumptions

1. **Development Environment**: Assumes Python 3.8+ with support for YAML parsing, JSON Schema validation, and standard libraries (pathlib, subprocess). No external dependencies beyond existing `requirements.txt`.

2. **Git Workflow**: Assumes feature branch workflow with CI/CD pipeline (GitHub Actions). All changes must pass validation before merge to main branch.

3. **User Interaction Model**: Assumes conversational interface (GitHub Copilot Chat or similar) where users can approve/reject generated workflows and provide consent for tool execution.

4. **File System Structure**: Assumes existing `.paperkit/` directory structure is canonical and `.paper/` legacy paths will be completely removed.

5. **Backward Compatibility Window**: Migration period of 2 weeks where both old and new formats are supported. When both formats exist for the same agent, the new format (YAML metadata) takes precedence and old format (MD frontmatter) generates deprecation warnings but continues to function. After the 2-week period, old format support is completely removed and validation fails for any remaining frontmatter.

6. **Performance Targets**: Orchestrator routing decision must complete within 100ms for single-intent requests, 500ms for multi-intent workflow generation.

7. **Concurrency Model**: Initial implementation assumes single-user, serial workflow execution. Parallel step execution is best-effort (Phase 3 stretch goal).

8. **Metrics Storage**: Metrics stored in local SQLite database for first iteration with 90-day retention policy (automatic cleanup of older data). Future enhancement may use time-series database for production deployments.

9. **Security Model**: Tool consent is per-tool and session-scoped by default (consent expires when session ends). Users can opt-in to persistent consent for trusted tools on a per-tool basis. Persistent consent requires explicit user opt-in and stores preferences in user-specific configuration file with ability to revoke at any time.

10. **Documentation Standard**: All schemas, manifests, and configuration files include inline comments and link to comprehensive documentation in `docs/dev/`.


## Success Criteria *(mandatory)*

### Measurable Outcomes

**Phase 1: System Consolidation**

- **SC-001**: 100% of agent metadata exists in single authoritative location (zero duplicate definitions detected by validation)
- **SC-002**: All validation scripts execute successfully with zero path reference errors
- **SC-003**: CI validation workflow blocks 100% of pull requests with agent metadata violations
- **SC-004**: System documentation completeness score reaches 100% (all required docs exist and reference correct paths)
- **SC-005**: Agent manifest validation confirms all agents are listed (zero orphaned agent files)

**Phase 2a: Agent Skills**

- **SC-2A-01**: 100% of Agent Skills in `skills/` directory have valid SKILL.md frontmatter passing schema validation
- **SC-2A-02**: Skill discovery returns metadata for all registered skills in under 50ms
- **SC-2A-03**: At least 3 existing instruction files are migrated to SKILL.md format (humanizer, etc.)
- **SC-2A-04**: Progressive disclosure reduces initial load by 80% (frontmatter only vs full instructions)
- **SC-2A-05**: Agent `suggestedSkills` references resolve correctly 100% of the time

**Phase 2b: Compositional Workflows**

- **SC-006**: At least 5 core workflows are defined, validated, and invokable by agents
- **SC-007**: Workflows reduce code duplication by 40% (measured by eliminated duplicate logic in agent instructions)
- **SC-008**: 100% of workflow definitions pass schema validation and dependency checks
- **SC-009**: Workflow invocation success rate exceeds 95% when prerequisites are met
- **SC-010**: Agent developers can create new workflow in under 30 minutes using documented process

**Phase 3: Enhanced Orchestration**

- **SC-011**: Orchestrator correctly identifies intent for 90% of user requests (measured against test set of 100 diverse requests)
- **SC-012**: Multi-step workflow generation completes in under 500ms for requests with up to 5 intents
- **SC-013**: Routing accuracy improves by 30% compared to baseline (fewer incorrect agent selections)
- **SC-014**: 80% of generated workflows receive user approval without modification
- **SC-015**: Workflow state checkpoint/resume succeeds 100% of the time after interruption
- **SC-016**: Users can complete complex multi-agent tasks 50% faster compared to manual agent selection

**Phase 4: Tool Integration Layer**

- **SC-017**: Agents successfully discover and invoke tools with 95% success rate when tools are available
- **SC-018**: User consent workflow completes in under 10 seconds (from prompt to approval/denial)
- **SC-019**: Tool execution audit trail captures 100% of invocations with complete metadata
- **SC-020**: Tool failure fallback strategies execute successfully 90% of the time
- **SC-021**: Zero tool executions occur without explicit user consent for consent-required tools

**Phase 5: Advanced Features**

- **SC-022**: Metrics dashboard displays performance data for 100% of agent invocations
- **SC-023**: A/B test results achieve statistical significance within 100 total invocations (50 per variant minimum)
- **SC-024**: Agent version compatibility validation prevents 100% of incompatible combinations
- **SC-025**: Gradual rollout capability reduces deployment risk by catching issues before full release (measured by incident rate reduction)
- **SC-026**: System uptime exceeds 99.5% during 30-day observation period after Phase 5 completion

**Cross-Phase Success Criteria**

- **SC-027**: End-to-end user task completion rate improves by 40% from baseline
- **SC-028**: System response time (from user request to first agent action) under 2 seconds for 95th percentile
- **SC-029**: User satisfaction score (1-5 scale) averages 4.0 or higher after each phase
- **SC-030**: Zero regressions in existing functionality during migration (all existing agent invocations continue to work)
- **SC-031**: Documentation coverage reaches 100% (every feature has corresponding user and developer documentation)
- **SC-032**: Code review approval time reduces by 50% due to automated validation catching issues early
- **SC-033**: System supports 10 concurrent user sessions without performance degradation
- **SC-034**: Total number of user-reported bugs decreases by 60% compared to pre-upgrade baseline (measured 30 days post-launch)

### Quality Gates

Each phase must meet these criteria before proceeding to next phase:

**Phase 1 Exit Criteria**:
- All validation scripts pass ✓
- Zero path reference errors ✓
- Documentation updated ✓
- CI workflow operational ✓
- Stakeholder sign-off ✓

**Phase 2a Exit Criteria**:
- All SKILL.md files pass schema validation ✓
- Skill discovery registry operational ✓
- At least 3 skills migrated ✓
- Progressive disclosure verified ✓
- Documentation updated ✓

**Phase 2b Exit Criteria**:
- Minimum 5 workflows operational ✓
- Schema validation passing ✓
- Agent integration demonstrated ✓
- 80% test coverage achieved ✓
- Performance benchmarks met ✓

**Phase 3 Exit Criteria**:
- 90% routing accuracy achieved ✓
- Workflow generation tested with 100 diverse inputs ✓
- Checkpoint/resume verified ✓
- User acceptance testing passed ✓
- Performance SLA met (<500ms) ✓

**Phase 4 Exit Criteria**:
- Tool registry operational ✓
- Consent workflow tested ✓
- Audit logging verified ✓
- Security review completed ✓
- Error handling validated ✓

**Phase 5 Exit Criteria**:
- Metrics dashboard operational ✓
- A/B testing framework validated ✓
- Versioning system tested ✓
- Production readiness review passed ✓
- 30-day stability period completed ✓

---

## Implementation Notes

### Dependencies & Prerequisites

- **Existing Infrastructure**: PR #28 changes (dual-file architecture, routing registry, validation framework)
- **Python Environment**: Python 3.8+ with PyYAML, jsonschema, pytest libraries
- **CI/CD**: GitHub Actions workflow infrastructure
- **Documentation Tools**: Markdown, JSON Schema documentation generators

### Risk Mitigation Strategies

| Risk | Mitigation |
|------|------------|
| Breaking changes to agent API | Implement semantic versioning with 2-week deprecation warnings |
| Skill complexity explosion | Enforce maximum depth limit (5 levels), require comprehensive documentation |
| Performance degradation | Establish baseline benchmarks, continuous performance monitoring, optimization sprints |
| User confusion with new concepts | Create interactive tutorials, examples for each phase, gradual feature rollout |
| Tool security vulnerabilities | Implement sandboxing, mandatory consent for sensitive operations, audit logging |

### Testing Strategy

- **Unit Tests**: Each component (skill loader, orchestrator router, tool registry) has isolated tests
- **Integration Tests**: Multi-component workflows tested end-to-end
- **Validation Tests**: Schema compliance, path references, manifest completeness
- **Performance Tests**: Benchmarks for routing speed, workflow generation time, tool execution latency
- **User Acceptance Tests**: Real user scenarios with diverse request types
- **Security Tests**: Consent enforcement, audit trail completeness, sandboxing effectiveness

### Migration Path

**Week 1-2: Phase 1 Implementation**
1. Create `docs/dev/PATHS.md` documenting canonical paths
2. Update all validation scripts to use `.paperkit/` paths
3. Remove YAML frontmatter from agent MD files
4. Implement duplicate detection in `check-agents.py`
5. Add manifest completeness validation
6. Update CI workflow
7. Run full validation suite
8. Update all documentation

**Week 3-4: Phase 2a Implementation (Agent Skills)**
1. Create `skills/{name}/SKILL.md` directory structure
2. Design and document skill frontmatter schema (`skill-frontmatter-schema.json`)
3. Implement SKILL.md frontmatter validator
4. Migrate existing instruction files to SKILL.md format (humanizer, etc.)
5. Implement skill discovery registry (metadata only)
6. Add `suggestedSkills` support to agent schema
7. Implement progressive disclosure loading
8. Document skill creation process

**Week 5-6: Phase 2b Implementation (Compositional Workflows)**
1. Rename existing skill YAML files to workflows directory
2. Design and document workflow schema (`workflow-schema.json`)
3. Implement workflow validator with skill reference support
4. Create 5 prototype workflows (cite-source, validate-citation, draft-section, research-topic, compile-latex)
5. Extend orchestrator with workflow registry
6. Add skill-loading to workflow steps
7. Test workflow invocation from agents
8. Document workflow creation process

**Week 7-9: Phase 3 Implementation**
1. Enhance orchestrator intent classification
2. Implement dependency resolver
3. Create workflow state machine
4. Add checkpoint/resume capability
5. Build workflow presentation UI (conversational)
6. Test with 100 diverse user requests
7. Measure and optimize performance

**Week 9-10: Phase 4 Implementation**
1. Design tool registry API
2. Implement consent management workflow
3. Add tool invocation to agent runtime
4. Create audit logging system
5. Implement error handling and fallbacks
6. Test security and consent enforcement

**Week 11-12: Phase 5 Implementation**
1. Design metrics collection system
2. Implement agent versioning
3. Create A/B testing framework
4. Build metrics dashboard
5. Test gradual rollout capability
6. Conduct production readiness review
7. Complete 30-day stability monitoring

### Definition of Done (per Phase)

- [ ] All functional requirements implemented and tested
- [ ] Success criteria met (validated with metrics)
- [ ] Code review completed and approved
- [ ] Documentation updated (user guide, developer guide, API reference)
- [ ] CI/CD pipeline passing all checks
- [ ] Security review completed (where applicable)
- [ ] Performance benchmarks met
- [ ] User acceptance testing passed
- [ ] Migration scripts created and tested
- [ ] Release notes drafted
- [ ] Stakeholder sign-off obtained
- [ ] Phase exit criteria satisfied

---

## Appendices

### Appendix A: Reference Documents

- **`docs/dev/AGENT-SYSTEM-ANALYSIS.md`**: Comprehensive analysis of PR #28 changes, insights, and upgrade plan
- **`.paperkit/_cfg/schemas/agent-schema.json`**: JSON Schema for agent metadata validation
- **`.paperkit/_cfg/routing.registry.yaml`**: Routing rules for intent-to-agent mapping
- **`docs/dev/agent-audit/decision.md`**: Design rationale for dual-file architecture
- **`docs/dev/agent-audit/how-agents-are-structured.md`**: Agent architecture guide

### Appendix B: Example Skill Definition

```yaml
# .paperkit/_cfg/skills/cite-source.yaml
name: cite-source
displayName: Citation Skill
description: Extract citation from source and format in Harvard style
version: 1.0.0

prerequisites:
  - skill: extract-metadata
  - tool: pdftotext

steps:
  - action: extract_metadata
    agent: librarian
    inputs:
      - pdf_path
    outputs:
      - author
      - year
      - title
      - doi
  
  - action: format_citation
    agent: reference-manager
    inputs:
      - author
      - year
      - title
    outputs:
      - formatted_citation

inputSchema:
  type: object
  properties:
    pdf_path:
      type: string
      description: Absolute path to PDF file
  required: [pdf_path]

outputSchema:
  type: object
  properties:
    formatted_citation:
      type: string
      description: Harvard-style formatted citation
    bibtex_entry:
      type: string
      description: BibTeX database entry
  required: [formatted_citation]
```

### Appendix C: Validation Commands

```bash
# Phase 1: Consolidation validation
python .paperkit/tools/check-agents.py --ci --verbose

# Phase 2: Skills validation
python .paperkit/tools/validate-skills.py --schema .paperkit/_cfg/schemas/skill-schema.json

# Phase 3: Orchestration testing
python .paperkit/tools/test-orchestrator.py --requests test-requests.yaml

# Phase 4: Tool integration testing
python .paperkit/tools/test-tools.py --audit-log /tmp/tool-audit.log

# Phase 5: Performance benchmarking
python .paperkit/tools/benchmark.py --duration 300 --report metrics-report.html
```

### Appendix D: Glossary

- **Agent**: Specialized AI persona with defined capabilities and behavioral instructions
- **Atomic Skill**: Single-action skill executed by one agent
- **Composite Skill**: Multi-step skill orchestrating multiple agents/actions
- **Conditional Skill**: Skill with branching logic based on runtime conditions
- **Intent**: User goal extracted from natural language request
- **Orchestrator**: Central agent responsible for routing requests and generating workflows
- **Routing Registry**: Database of rules mapping intents to appropriate agents
- **Schema**: JSON Schema definition validating YAML structure and content
- **Skill**: Reusable capability that agents can invoke
- **Tool**: External executable invoked by agents to perform concrete actions
- **Workflow**: Multi-step orchestration of agents, skills, and tools

---

## Clarifications

### Session 2026-01-20

- Q: During the 2-week backward compatibility window (Assumption #5), when both old and new agent formats coexist, how should the system handle conflicts? → A: New format takes precedence; old format generates warnings but still works
- Q: How long should the system retain historical metrics data? → A: 90 days
- Q: What should happen when NO agents meet the minimum confidence threshold (< 0.7)? → A: Present top 3 agents with scores and ask user to select
- Q: When a skill execution fails mid-way through its multi-step workflow (e.g., step 2 of 5 fails), how should the system handle partial completion? → A: Checkpoint completed steps; offer retry from failure point or rollback
- Q: When a user grants consent for a tool like `build-latex`, what should be the scope of that consent? → A: Per-tool, session-scoped by default with opt-in for persistent
