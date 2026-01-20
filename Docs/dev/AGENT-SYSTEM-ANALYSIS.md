# Agent System Analysis & Upgrade Plan

**Date**: 2026-01-20  
**Analysis of**: PR #28 "Clean up agent system" changes  
**Status**: Completed analysis, recommendations proposed

---

## Executive Summary

PR #28 introduced a **dual-file agent architecture** separating schema-validated metadata (YAML) from behavioral instructions (Markdown), along with a comprehensive validation framework and routing registry. The changes represent a significant architectural improvement toward machine-readability, CI validation, and agent orchestration.

However, the implementation reveals **three parallel systems** that need reconciliation, and introduces opportunities for further enhancement including skills/capabilities expansion and tool integration.

---

## 1. What Changed: Detailed Analysis

### 1.1 Architectural Changes

**Before PR #28:**
- Single-file `.md` agents with YAML frontmatter
- Manual validation
- No automated routing system
- Inconsistent path references

**After PR #28:**
- **Dual-file architecture**:
  - `.paperkit/_cfg/agents/*.yaml` — Schema-validated metadata
  - `.paperkit/{core,specialist}/agents/*.md` — Behavioral instructions
- **Routing Registry** (`.paperkit/_cfg/routing.registry.yaml`)
- **Unified validation** (`check-agents.py`)
- **CI/CD integration** (`.github/workflows/validate-agent-metadata.yml`)
- **Comprehensive documentation** (5 new docs in `docs/dev/agent-audit/`)

### 1.2 Files Created (14 files, 1,281 lines added)

#### Core Infrastructure
1. **`routing.registry.yaml`** (74 lines) — Agent routing rules with:
   - `whenToUse` criteria
   - `keywords` for intent matching
   - `requiredInputs` validation
   - `hardExclusions` to prevent misrouting

2. **`check-agents.py`** (354 lines) — Unified validation covering:
   - Schema compliance (YAML files)
   - Duplicate name detection
   - Path reference integrity
   - Manifest consistency
   - Exit codes for CI/CD

3. **`validate-agent-metadata.yml`** (10 lines) — GitHub Actions workflow

#### Agent Files Updated
4. **`orchestrator.yaml`** (103 lines) — Now schema-compliant with:
   - Structured `inputSchema` and `outputSchema`
   - Machine-parseable decision format
   - `capabilities`, `constraints`, `principles` arrays

5. **`orchestrator.md`** (176 lines) — Refactored to contain **only instructions**:
   - Removed YAML frontmatter
   - Added explicit tie-break rules
   - Keyword-based routing table
   - JSON output schema

#### Documentation
6-13. **Agent audit docs** (588 lines total):
- `decision.md` — Design rationale for dual-file split
- `how-agents-are-structured.md` — Architecture guide
- `inventory.md` — Complete agent catalog
- `runtime-paths.md` — Path analysis & issues found
- `baseline.txt`, `paperkit-tree.txt` — Reference data

### 1.3 Key Architectural Decisions

#### Decision 1: Separation of Concerns
**Metadata (YAML)** vs. **Instructions (MD)**

| Aspect | YAML Files | MD Files |
|--------|------------|----------|
| **Purpose** | Machine-readable metadata | Human-readable instructions |
| **Validation** | JSON Schema (`agent-schema.json`) | None (free-form prompts) |
| **CI Check** | ✅ Automated | ❌ Manual |
| **Fields** | `name`, `displayName`, `icon`, `capabilities`, `constraints`, `inputSchema`, `outputSchema` | Agent persona, behavior rules, tie-breaks, output formats |
| **Used By** | Orchestrator, tooling, manifests | Runtime agent activation (GitHub Copilot/Codex) |

**Rationale**: Enables schema validation, prevents drift, supports machine orchestration while preserving prompt flexibility.

#### Decision 2: Routing Registry as First-Class Citizen
- Separate from agent definitions
- Centralized routing logic
- Enables intent classification
- Supports required input validation

#### Decision 3: CI-First Validation
- GitHub Actions workflow runs on every change
- Blocks merges if validation fails
- Two-layer validation: schema + system integrity

---

## 2. What We Learned: Key Insights

### 2.1 Architecture Patterns

#### Pattern 1: **Progressive Disclosure of Complexity**
The system reveals complexity only when needed:
- Users interact with simple MD files
- Orchestrator uses routing registry
- CI validates against strict schemas
- Tools reference YAML metadata

**Lesson**: Separation allows different stakeholders to work at appropriate abstraction levels.

#### Pattern 2: **Metadata-Driven Orchestration**
The orchestrator doesn't hardcode routing logic—it references:
- `routing.registry.yaml` for intent matching
- Agent YAML files for capabilities
- Input/output schemas for validation

**Lesson**: Data-driven systems are more maintainable and testable than code-driven ones.

#### Pattern 3: **Constraint-Based Agent Design**
Agents define what they **cannot** do as clearly as what they **can** do:
```yaml
constraints:
  - Cannot start writing content (delegates to Section Drafter)
  - Must not fabricate citations or sources
```

**Lesson**: Explicit constraints prevent scope creep and improve routing accuracy.

### 2.2 System Insights

#### Insight 1: **Three Parallel Systems Exist**
The analysis revealed three overlapping agent definition approaches:

1. **YAML metadata files** (`.paperkit/_cfg/agents/`)
2. **Markdown files with frontmatter** (`.paperkit/{core,specialist}/agents/`)
3. **Legacy `.paper/` paths** (in some validation scripts)

**Implication**: System needs consolidation—currently has redundancy and potential drift.

#### Insight 2: **Schema Pattern is Powerful**
The `agent-schema.json` provides:
- Contract enforcement
- Documentation-as-code
- IDE autocomplete (if tooling supports it)
- Version control of agent APIs

**Implication**: Extend schema pattern to workflows and tools.

#### Insight 3: **Routing Registry Enables Composability**
By externalizing routing rules, the system can:
- Add new agents without modifying orchestrator
- Test routing logic independently
- Support multiple routing strategies
- Enable user-defined agent priorities

**Implication**: This pattern should extend to workflows and tool selection.

### 2.3 Code Quality Observations

#### Strength 1: Explicit Error Handling
`check-agents.py` provides clear, actionable error messages:
```python
errors.append(f"  [{path}] {error.message}")
```

#### Strength 2: Documentation-First Approach
Changes included comprehensive docs **before** implementation questions arose.

#### Strength 3: CI Integration
Immediate validation feedback loop prevents drift.

#### Weakness 1: Path Inconsistency
`validate.py` still references `.paper/` instead of `.paperkit/`

#### Weakness 2: Duplication
Agent metadata exists in **both** YAML frontmatter (MD files) and YAML files—potential drift.

#### Weakness 3: No Runtime Validation
System validates at build time but not at agent invocation time.

---

## 3. Discovered: Skills & Capabilities Framework

### 3.1 Current State

The system already uses a **capabilities-based model** but hasn't formalized it:

```yaml
capabilities:
  - Design comprehensive paper structures
  - Create hierarchical section organization
  - Generate argument flow diagrams
```

This is **proto-skills** but lacks:
- Skill composition (skills built from other skills)
- Skill prerequisites
- Skill versioning
- Skill discovery/search

### 3.2 Skills vs. Capabilities

| Concept | Current Usage | Potential Enhancement |
|---------|---------------|----------------------|
| **Capabilities** | What an agent can do | Atomic abilities (read PDF, extract citation) |
| **Skills** | *(not formalized)* | Composed workflows (research → synthesize → write) |
| **Tools** | External executables | Invokable functions agents use to exercise skills |
| **Workflows** | YAML definitions in `_cfg/workflows/` | Multi-step skill orchestrations |

### 3.3 Skills Mentioned in System

Searching the codebase found **workflows** (16 defined) but no explicit "skills" framework:

**Core Workflows** (from `workflow-manifest.yaml`):
- Research: `consolidate.yaml`, `search-sources.yaml`
- Planning: `outline.yaml`, `skeleton.yaml`
- Drafting: `write-section.yaml`
- Refinement: `refine-section.yaml`
- References: `extract-citations.yaml`, `validate-citations.yaml`, `format-bibliography.yaml`

**Tools** (from `tool-manifest.yaml`):
- `build-latex`, `lint-latex`, `validate-structure`
- `format-references`, `extract-evidence`
- `lock-chapter`

**Implication**: The system has **workflow orchestration** and **tool execution** but no middle layer for **reusable skill composition**.

---

## 4. Upgrade Plan: Roadmap to Enhanced Agent System

### Phase 1: Consolidation (Weeks 1-2)

#### Goal: Eliminate redundancy and fix inconsistencies

**Tasks:**

1. **Fix Path References** (Priority: HIGH)
   - Update `validate.py` to use `.paperkit/` paths
   - Remove all `.paper/` references
   - Test all validation scripts

2. **Eliminate YAML Frontmatter in MD Files** (Priority: MEDIUM)
   - MD files should contain **only** instructions
   - All metadata should live in YAML files
   - Update `generate.sh` to read metadata from YAML

3. **Reconcile agent-manifest.yaml**
   - Ensure all agents listed
   - Verify path references
   - Add validation test for manifest completeness

4. **Document Canonical Paths**
   - Create `PATHS.md` documenting all official paths
   - Add path validation to CI

**Success Criteria:**
- ✅ All validation passes
- ✅ No duplicate metadata
- ✅ Single source of truth for each concept

---

### Phase 2: Skills Framework (Weeks 3-5)

#### Goal: Formalize reusable skill composition

**Design Proposal:**

Create `.paperkit/_cfg/skills/` directory with schema:

```yaml
# Example: .paperkit/_cfg/skills/cite-source.yaml
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
    pdf_path: { type: string }
  required: [pdf_path]

outputSchema:
  type: object
  properties:
    formatted_citation: { type: string }
    bibtex_entry: { type: string }
  required: [formatted_citation]
```

**Skills Types:**
1. **Atomic Skills** — Single agent, single action
2. **Composite Skills** — Multi-agent workflow
3. **Conditional Skills** — Branching logic based on inputs

**Implementation:**

1. **Create Schema** (`skill-schema.json`)
2. **Define 5-10 Core Skills**:
   - `cite-source`
   - `validate-citation`
   - `draft-section`
   - `research-topic`
   - `compile-latex`

3. **Extend Orchestrator**:
   - Add skill registry
   - Enable skill-based routing
   - Support skill chaining

4. **Create Skill Validator**:
   - Validate skill YAML files
   - Check prerequisite dependencies
   - Verify agent/tool availability

**Success Criteria:**
- ✅ Skills are reusable across workflows
- ✅ Skills can be composed into new skills
- ✅ CI validates skill definitions
- ✅ Agents can invoke skills declaratively

---

### Phase 3: Enhanced Orchestration (Weeks 6-8)

#### Goal: Intelligent multi-step task routing

**Capabilities to Add:**

1. **Intent Classification Improvements**
   - Machine learning for keyword extraction
   - Confidence thresholds with fallback
   - Multi-intent detection (task decomposition)

2. **Workflow Auto-Generation**
   - Orchestrator generates multi-step workflows from goals
   - Dynamic skill composition
   - Parallel execution planning

3. **Context Preservation**
   - Session state management
   - Inter-agent context passing
   - Workflow checkpointing

**Example Enhanced Flow:**

```
User: "Research color perception and draft Related Work"

Orchestrator analyzes:
├─ Intent 1: Research (librarian + research-consolidator)
├─ Intent 2: Draft section (section-drafter)
└─ Dependency: Intent 2 requires Intent 1 output

Orchestrator creates workflow:
1. [librarian] Search color perception sources
2. [research-consolidator] Synthesize findings
3. [section-drafter] Draft Related Work from synthesis
4. [quality-refiner] Polish draft

Orchestrator: "I've created a 4-step workflow. Proceed?"
```

**Implementation:**

1. **Add workflow generator to orchestrator**
2. **Create dependency resolver**
3. **Implement state machine for workflow execution**
4. **Add checkpoint/resume capability**

**Success Criteria:**
- ✅ Complex tasks decompose automatically
- ✅ Workflows execute reliably
- ✅ State persists across sessions
- ✅ Users can review/approve before execution

---

### Phase 4: Tool Integration Layer (Weeks 9-10)

#### Goal: Seamless agent-tool interaction

**Current State:**
- Tools exist (`tool-manifest.yaml`)
- Agents reference tools manually in instructions
- No programmatic tool invocation

**Proposed Architecture:**

```yaml
# agents invoke tools via tool registry
capabilities:
  - name: compile-latex
    requiresTool: build-latex
    inputs: [latex_dir]
    outputs: [pdf_path, error_log]
```

**Features:**

1. **Tool Discovery**
   - Agents query tool registry
   - Capability-to-tool mapping
   - Version compatibility checking

2. **Consent Management**
   - Tools marked `requiresConsent: true`
   - User approves tool execution
   - Audit log of tool invocations

3. **Error Handling**
   - Tool failures trigger fallback strategies
   - Retry logic with backoff
   - Error context passed to agents

**Implementation:**

1. **Create tool registry class**
2. **Add tool invocation to agent runtime**
3. **Implement consent workflow**
4. **Add tool execution logging**

**Success Criteria:**
- ✅ Agents invoke tools declaratively
- ✅ Users control tool permissions
- ✅ Tool failures don't crash workflows
- ✅ Full audit trail exists

---

### Phase 5: Advanced Features (Weeks 11-12)

#### Goal: Production-ready enhancements

**Features:**

1. **Agent Versioning & Compatibility**
   ```yaml
   version: 2.1.0
   compatibleWith:
     orchestrator: ">=1.0.0"
     tools:
       build-latex: "^3.0.0"
   ```

2. **Agent Performance Metrics**
   - Success/failure rates
   - Average completion time
   - User satisfaction ratings
   - Routing accuracy

3. **A/B Testing Framework**
   - Test multiple agent versions
   - Compare routing strategies
   - Gradual rollout capability

4. **Agent Marketplace**
   - Community-contributed agents
   - Agent discovery and installation
   - Rating and review system

**Success Criteria:**
- ✅ System tracks agent performance
- ✅ Multiple agent versions coexist
- ✅ Users can contribute agents
- ✅ Agents can be A/B tested

---

## 5. Immediate Next Steps (This Week)

### Priority 1: Fix Path Issues
```bash
# Update validate.py
sed -i 's/\.paper\//\.paperkit\//g' .paperkit/tools/validate.py
python .paperkit/tools/check-agents.py --ci
```

### Priority 2: Document Current State
```bash
# Create PATHS.md
cat > docs/dev/PATHS.md << 'EOF'
# Official Path Reference

## Agent Definitions
- YAML Metadata: `.paperkit/_cfg/agents/*.yaml`
- MD Instructions: `.paperkit/{core,specialist}/agents/*.md`
- Manifest: `.paperkit/_cfg/agent-manifest.yaml`

## Schemas
- Agent Schema: `.paperkit/_cfg/schemas/agent-schema.json`
- Workflow Schema: `.paperkit/_cfg/schemas/workflow-schema.json`
- Tool Schema: `.paperkit/_cfg/schemas/tool-schema.json`

## Validation
- Unified Check: `.paperkit/tools/check-agents.py`
- Schema Validation: `.paperkit/tools/validate-agent-schema.py`
EOF
```

### Priority 3: Run Full Validation
```bash
# Comprehensive system check
python .paperkit/tools/check-agents.py --verbose
python .paperkit/tools/validate-agent-schema.py --ci \
  --schema .paperkit/_cfg/schemas/agent-schema.json \
  --agents-dir .paperkit/_cfg/agents
```

### Priority 4: Create Skills Prototype
```bash
# Create skills directory and sample
mkdir -p .paperkit/_cfg/skills
cat > .paperkit/_cfg/skills/cite-source.yaml << 'EOF'
# Prototype skill definition
name: cite-source
displayName: Citation Skill
description: Extract and format citation from PDF source
version: 1.0.0
agents: [librarian, reference-manager]
tools: [pdftotext]
EOF
```

---

## 6. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking changes to agent API | HIGH | MEDIUM | Semantic versioning, deprecation warnings |
| Skill complexity explosion | MEDIUM | HIGH | Limit skill depth, require documentation |
| Performance degradation | MEDIUM | LOW | Benchmark, optimize hot paths |
| User confusion with new concepts | LOW | MEDIUM | Comprehensive docs, examples |
| Tool security vulnerabilities | HIGH | LOW | Sandboxing, consent management |

---

## 7. Success Metrics

### Technical Metrics
- ✅ 100% agent schema compliance
- ✅ <100ms orchestrator routing time
- ✅ Zero path reference errors
- ✅ 95%+ CI pass rate

### User Experience Metrics
- ✅ Reduced user input needed for routing
- ✅ Higher task completion rate
- ✅ Faster workflow execution
- ✅ Improved routing accuracy (user confirms agent choice)

### System Health Metrics
- ✅ No duplicate metadata
- ✅ All paths validated
- ✅ Complete documentation
- ✅ Active CI/CD monitoring

---

## 8. Conclusion

PR #28 represents a **foundational architectural shift** toward:
- **Machine-readable agent systems**
- **Automated validation and testing**
- **Intelligent orchestration**
- **Composable workflows**

The changes provide a **solid foundation** for the proposed **Skills Framework** and **Enhanced Orchestration** upgrades.

**Recommendation**: Proceed with **Phase 1 (Consolidation)** immediately, then evaluate resource allocation for **Phase 2 (Skills)** based on user demand and system stability.

---

**Next Review**: 2026-02-03 (2 weeks)  
**Owner**: System Architecture Team  
**Stakeholders**: Agent developers, CI/CD team, end users
