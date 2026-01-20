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

**All NEEDS CLARIFICATION items resolved.** Ready for Phase 1: Design & Contracts.
