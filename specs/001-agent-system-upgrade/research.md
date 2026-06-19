# Research: Agent System Upgrade

**Feature**: 001-agent-system-upgrade
**Date**: 2026-01-20
**Status**: Complete

## Research Tasks

Based on Technical Context unknowns and dependencies, the following research was conducted.

---

## 1. Existing Agent System Architecture

### Decision: Dual-File Architecture (YAML + MD)

**Research**: Analysis of PR #28 changes and current `.paperkit/` structure.

**Findings**:
- **YAML files** (`.paperkit/_cfg/agents/*.yaml`): Machine-readable metadata validated against `agent-schema.json`
- **MD files** (`.paperkit/{core,specialist}/agents/*.md`): Behavioral instructions, prompts, examples
- **Routing Registry** (`.paperkit/_cfg/routing.registry.yaml`): Intent-to-agent mapping with keywords

**Current Issues Identified**:
1. Some MD files still contain YAML frontmatter (duplicate metadata)
2. Legacy `.paper/` path references in some validation scripts
3. No formal skill composition layer between agents and tools

**Rationale**: Dual-file separation is correct architecture; this upgrade consolidates and extends it.

**Alternatives Considered**:
- Single-file agents: Rejected because mixing schema-validated data with free-form prompts prevents CI validation
- Database storage: Rejected because YAML files are version-controllable and human-readable

---

## 2. Skills Framework Design Patterns

### Decision: Declarative YAML Skills with JSON Schema Validation

**Research**: Reviewed workflow definitions in `workflow-manifest.yaml` and agent capabilities patterns.

**Findings**:
- Current system has **workflows** (16 defined) but no **skills** layer
- Workflows are static sequences; skills should be composable units
- Existing patterns: `inputSchema`/`outputSchema` on agents provide foundation

**Best Practices for Skill Composition**:

| Pattern | Description | Applicability |
|---------|-------------|---------------|
| **Atomic Skills** | Single agent, single action | High - base building blocks |
| **Composite Skills** | Multi-step sequences | High - orchestrated workflows |
| **Conditional Skills** | Branching based on input | Medium - complex scenarios |
| **Parameterized Skills** | Template with variables | High - reusable patterns |

**Rationale**: YAML declarative format matches existing agent/workflow patterns; JSON Schema provides validation.

**Alternatives Considered**:
- Python-coded skills: Rejected because harder to validate, version, and understand for non-developers
- Graph-based skill DAGs: Rejected as over-engineering for initial 5-10 skills scope

---

## 3. Intent Classification Approaches

### Decision: Keyword Matching + Confidence Scoring + Top-3 Fallback

**Research**: Analyzed `routing.registry.yaml` structure and user interaction patterns.

**Findings**:
- Current routing uses `keywords` and `whenToUse` descriptions
- `hardExclusions` prevent misrouting
- No confidence scoring or fallback mechanism exists

**Classification Strategy**:

```
User Request → Tokenize → Match Keywords → Calculate Scores → Apply Exclusions → Route or Clarify
```

**Confidence Calculation**:
- Base score from keyword matches (TF-IDF style weighting)
- Bonus for `whenToUse` semantic match
- Penalty for `hardExclusions` partial match
- Threshold: 0.7 for auto-routing, below presents top 3 with scores

**Rationale**: Keyword matching is simple, interpretable, and fast (<100ms). Top-3 fallback provides transparency.

**Alternatives Considered**:
- ML-based classification: Rejected for V1 due to training data requirements and latency concerns
- Rule-based expert system: Considered as future enhancement; current keyword approach is simpler

---

## 4. Tool Consent Management Patterns

### Decision: Per-Tool Session-Scoped with Persistent Opt-In

**Research**: Security best practices for autonomous tool execution.

**Findings**:
- Tools vary in risk: `build-latex` (low risk) vs. `delete-file` (high risk)
- User trust varies by familiarity with tool
- Session-scoped consent balances security with usability

**Consent Model**:

| Consent Type | Scope | Storage | Use Case |
|--------------|-------|---------|----------|
| **None** | Per-invocation | N/A | Very dangerous tools |
| **Session** | Current session | Memory | Default for most tools |
| **Persistent** | Across sessions | YAML file | Trusted, frequently-used tools |

**Implementation**:
- Consent stored in `.paperkit/_cfg/consent.registry.yaml` (persistent)
- Session consent in memory (cleared on exit)
- Tools declare `requiresConsent: true/false` in definition

**Rationale**: Per-tool granularity gives users precise control; session-scope is secure default.

**Alternatives Considered**:
- Global consent (all or nothing): Rejected as too coarse-grained
- Per-invocation always: Rejected as too disruptive for common operations

---

## 5. Metrics Collection Strategy

### Decision: SQLite with 90-Day Retention and Auto-Cleanup

**Research**: Observability requirements and storage constraints.

**Findings**:
- Need to track: invocation count, success rate, completion time, routing accuracy
- 90-day window sufficient for trend analysis and debugging
- SQLite is zero-dependency, file-based, and sufficient for single-user scale

**Schema Design**:

```sql
-- Core metrics table
CREATE TABLE agent_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    agent_name TEXT NOT NULL,
    action TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    duration_ms INTEGER,
    confidence_score REAL,
    user_modified_workflow BOOLEAN,
    error_type TEXT
);

-- Index for common queries
CREATE INDEX idx_metrics_timestamp ON agent_metrics(timestamp);
CREATE INDEX idx_metrics_agent ON agent_metrics(agent_name);
```

**Cleanup Strategy**:
- Run on every write: `DELETE FROM agent_metrics WHERE timestamp < datetime('now', '-90 days')`
- Lightweight; SQLite handles this efficiently

**Rationale**: SQLite is stdlib, requires no server, and 90-day retention keeps database manageable.

**Alternatives Considered**:
- Time-series database (InfluxDB): Overkill for single-user; adds deployment complexity
- JSON log files: Harder to query for trend analysis

---

## 6. A/B Testing Framework

### Decision: Traffic Split via Routing Registry with Minimum Sample Size

**Research**: Statistical requirements for agent comparison.

**Findings**:
- Need minimum 30 invocations per variant for basic significance
- Traffic split configurable (default 50/50)
- Results stored in metrics DB; analysis via SQL queries

**A/B Test Definition**:

```yaml
# In routing.registry.yaml
abTests:
  - name: orchestrator-v2-test
    control: orchestrator-v1
    treatment: orchestrator-v2
    splitRatio: 0.5  # 50% to treatment
    minimumSampleSize: 30
    startDate: 2026-02-01
    endDate: 2026-02-15
    metrics:
      - routing_accuracy
      - user_modification_rate
      - completion_time
```

**Statistical Analysis**:
- Simple proportion test for success rate
- Mann-Whitney U for completion time (non-parametric)
- Report confidence intervals and effect size

**Rationale**: Lightweight implementation leveraging existing routing infrastructure.

**Alternatives Considered**:
- External A/B platform: Overkill for agent testing; adds complexity
- Manual version switching: Doesn't provide statistically valid comparisons

---

## 7. Backward Compatibility Strategy

### Decision: New Format Precedence with 2-Week Deprecation Warnings

**Research**: Migration patterns and user impact assessment.

**Findings**:
- Estimated 10 agents need frontmatter removal
- No external consumers depend on frontmatter format
- 2-week window provides buffer for edge cases

**Migration Process**:

| Week | Action | Behavior |
|------|--------|----------|
| 1 | Deploy dual-support | New format preferred; old format warns |
| 2 | Monitor warnings | Identify any missed migrations |
| 3+ | Remove old support | Validation fails on frontmatter |

**Warning Message**:
```
DEPRECATION WARNING: Agent '{name}' uses YAML frontmatter in MD file.
This format will stop working on {date}.
Migrate metadata to .paperkit/_cfg/agents/{name}.yaml
```

**Rationale**: Provides clear migration path with ample warning; automated detection prevents silent breakage.

**Alternatives Considered**:
- Hard cutoff (no warnings): Too risky; might miss edge cases
- Indefinite dual support: Accumulates technical debt; drift between formats

---

## 8. Skill Depth Limit Implementation

### Decision: 5-Level Maximum with Stack Tracking

**Research**: Recursion safety patterns in workflow systems.

**Findings**:
- Typical skill compositions are 2-3 levels deep
- 5 levels allows complex scenarios without risk of infinite loops
- Stack tracking enables clear error messages

**Implementation**:

```python
def execute_skill(skill_name: str, inputs: dict, _depth: int = 0) -> dict:
    if _depth > 5:
        raise SkillDepthExceeded(
            f"Skill '{skill_name}' exceeded maximum depth of 5. "
            f"Check for circular dependencies."
        )

    skill = load_skill(skill_name)

    # Execute prerequisites
    for prereq in skill.prerequisites:
        execute_skill(prereq.name, inputs, _depth + 1)

    # Execute main skill logic
    return skill.execute(inputs)
```

**Rationale**: 5 levels is generous for real use cases; stack tracking aids debugging.

**Alternatives Considered**:
- No limit: Risk of infinite loops in misconfigured skills
- 3-level limit: Might be too restrictive for complex compositions

---

---

## 9. Agent Skills vs Compositional Workflows (Phase 2a Addition)

### Decision: Dual-Concept Architecture - Skills (Instructions) + Workflows (Orchestration)

**Research**: Industry analysis of Agent Skills standard (agentskills.io), Claude Code implementation, existing PaperKit implementation.

**Critical Finding**: Phase 2 implementation conflates two distinct concepts:

| Concept | Purpose | Format | Standard |
|---------|---------|--------|----------|
| **Agent Skills** | Teach agents HOW to do something | SKILL.md (YAML frontmatter + markdown) | agentskills.io (VS Code, Claude Code, Cursor, Gemini CLI, Goose, Amp) |
| **Compositional Workflows** | Define WHAT steps to execute | YAML (steps, agents, I/O) | PaperKit-internal |

**Agent Skills Standard (agentskills.io)**:

Skills are folders containing instructions, scripts, and resources that agents load dynamically:

```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: additional docs
└── assets/           # Optional: templates, data
```

**SKILL.md Format**:

```yaml
---
name: skill-name                    # Required: 1-64 chars, lowercase, hyphens
description: What it does and when  # Required: 1-1024 chars
license: Apache-2.0                 # Optional
compatibility: Claude Code          # Optional
allowed-tools: Read Write Bash      # Optional: pre-approved tools
metadata:                           # Optional: arbitrary key-value
  author: example-org
  version: "1.0"
---

# Skill Instructions

[Markdown body with step-by-step instructions, examples, edge cases]
```

**Progressive Disclosure Pattern**:
1. **Metadata** (~100 tokens): `name` + `description` loaded at startup for ALL skills
2. **Instructions** (<5000 tokens): Full SKILL.md body loaded when skill ACTIVATED
3. **Resources** (as needed): scripts/, references/ loaded ON DEMAND

**Existing PaperKit Implementation**:

| File | Type | Current Location | Correct Classification |
|------|------|------------------|------------------------|
| `humanizer.md` | Agent Skill | `.paperkit/_cfg/skills/` | ✅ Correct |
| `cite-source.yaml` | Workflow | `.paperkit/_cfg/skills/` | ❌ Should be `workflows/` |
| `compile-latex.yaml` | Workflow | `.paperkit/_cfg/skills/` | ❌ Should be `workflows/` |
| `draft-section.yaml` | Workflow | `.paperkit/_cfg/skills/` | ❌ Should be `workflows/` |

**Rationale for Dual Architecture**:

Both concepts are valuable and serve different purposes:

- **Agent Skills** → Knowledge transfer, teaching agents domain expertise
- **Compositional Workflows** → Automation, orchestrating multi-step sequences

They can work together: A workflow step can invoke a skill, and a skill's instructions can reference workflows.

**Proposed Directory Structure**:

```
.paperkit/_cfg/
├── skills/                    # Agent Skills (SKILL.md format)
│   ├── humanizer/
│   │   └── SKILL.md
│   ├── academic-writing/
│   │   ├── SKILL.md
│   │   └── references/
│   │       └── harvard-guide.md
│   └── latex-best-practices/
│       ├── SKILL.md
│       └── scripts/
│           └── lint-latex.sh
├── workflows/                 # Compositional Workflows (YAML format)
│   ├── cite-source.yaml
│   ├── compile-latex.yaml
│   ├── draft-section.yaml
│   ├── research-topic.yaml
│   └── validate-citation.yaml
└── schemas/
    ├── skill-schema.json      # Validates SKILL.md frontmatter
    └── workflow-schema.json   # Validates workflow YAML
```

**Integration Points**:

1. **Skill → Workflow**: A skill's instructions can tell the agent to "run the cite-source workflow"
2. **Workflow → Skill**: A workflow step can specify `skill: academic-writing` to load context
3. **Agent → Both**: Agents can declare required skills AND participate in workflows

**Alternatives Considered**:

- Keep single "skills" concept: Rejected because it conflates fundamentally different purposes
- Abandon workflows: Rejected because orchestration automation is valuable
- Rename workflows to something else: Considered "procedures" or "sequences" but "workflows" is clearer

---

## 10. Skill Activation and Discovery

### Decision: Description Matching + Explicit Invocation + Agent Hints

**Research**: How Claude Code and other agent products handle skill activation.

**Activation Mechanisms**:

| Mechanism | Description | Example |
|-----------|-------------|---------|
| **Description Match** | Agent matches user request to skill descriptions | User: "humanize this text" → loads humanizer skill |
| **Explicit Command** | User or agent explicitly invokes skill | `/skill humanizer` or "use the humanizer skill" |
| **Agent Hint** | Agent definition suggests relevant skills | Agent declares `suggestedSkills: [humanizer]` |

**Skill Discovery Flow**:

```
1. System loads all skill metadata (name, description) at startup
2. User request arrives
3. For each skill:
   - Score description relevance to request
   - Check agent hints if agent already selected
4. If high-relevance skill found:
   - Load full SKILL.md into context
   - Continue with enriched instructions
5. Agent proceeds with task (may load additional references on demand)
```

**Rationale**: Multiple activation paths provide flexibility; description matching enables auto-discovery.

---

## Research Summary

| Topic | Decision | Confidence |
|-------|----------|------------|
| Agent Architecture | Dual-file (YAML + MD) | High |
| Skills Format | Declarative YAML with JSON Schema | High |
| Intent Classification | Keyword matching + confidence scoring | High |
| Tool Consent | Per-tool, session-scoped default | High |
| Metrics Storage | SQLite with 90-day retention | High |
| A/B Testing | Traffic split via routing registry | Medium |
| Migration | 2-week deprecation window | High |
| Skill Depth | 5-level maximum | High |
| **Agent Skills vs Workflows** | **Dual-concept: Skills (SKILL.md) + Workflows (YAML)** | **High** |
| **Skill Activation** | **Description matching + explicit + agent hints** | **High** |

**All NEEDS CLARIFICATION items resolved.** Ready for Phase 1: Design & Contracts.

---

## Phase 2a: Agent Skills Implementation (NEW)

Based on research findings, Phase 2 must be split:

- **Phase 2 (existing)**: Rename to "Compositional Workflows Framework"
- **Phase 2a (new)**: "Agent Skills Framework" - industry-standard SKILL.md format

### Phase 2a Requirements (to add to spec.md):

| ID | Requirement |
|----|-------------|
| FR-2A-01 | System MUST support Agent Skills in SKILL.md format per agentskills.io spec |
| FR-2A-02 | Skills MUST be stored in `.paperkit/_cfg/skills/{skill-name}/SKILL.md` |
| FR-2A-03 | SKILL.md MUST contain YAML frontmatter with `name` and `description` fields |
| FR-2A-04 | System MUST validate skill names (1-64 chars, lowercase, hyphens only) |
| FR-2A-05 | System MUST support optional `scripts/`, `references/`, `assets/` directories |
| FR-2A-06 | System MUST implement progressive disclosure (metadata → instructions → resources) |
| FR-2A-07 | System MUST support skill discovery via description matching |
| FR-2A-08 | System MUST support explicit skill invocation |
| FR-2A-09 | Agents MUST be able to declare `suggestedSkills` for automatic loading |
| FR-2A-10 | Existing workflow YAML files MUST be migrated to `.paperkit/_cfg/workflows/` |

### Phase 2a Tasks:

| Task | Description | Exit Criteria |
|------|-------------|---------------|
| 2a.1 | Create `skill-frontmatter-schema.json` | Validates SKILL.md frontmatter |
| 2a.2 | Create `.paperkit/_cfg/skills/` directory structure | Subdirectories per skill |
| 2a.3 | Migrate `humanizer.md` to `humanizer/SKILL.md` format | Passes validation |
| 2a.4 | Create 3 initial skills: `academic-writing`, `latex-best-practices`, `harvard-citations` | Skills operational |
| 2a.5 | Implement skill discovery in orchestrator | Description matching works |
| 2a.6 | Migrate workflow YAMLs to `.paperkit/_cfg/workflows/` | Clear separation |
| 2a.7 | Update `validate-skills.py` to handle both formats | Dual validation |
| 2a.8 | Update `docs/dev/SKILLS.md` to document dual architecture | Docs complete |
