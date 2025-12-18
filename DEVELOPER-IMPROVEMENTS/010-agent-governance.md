# Specification: Governance of Agent Updates

**Spec ID:** 010-agent-governance  
**Date:** 2025-12-13  
**Status:** Draft  
**Priority:** Medium  
**Category:** Operations & Maintenance

---

## Problem Statement

How are agents maintained, versioned, and reviewed? The manifest contains installDate/version but no per-agent versioning policy. There's no formal process for agent changes, no changelogs, and no compatibility guarantees.

### Current State

- `manifest.yaml` has system version and installDate
- No per-agent version numbers
- No changelog for agent changes
- No PR-based review process specifically for agents
- No compatibility notes between versions
- No deprecation policy
- Agents can change without notice

### Impact

- Users unaware of agent behavior changes
- Breaking changes may surprise users
- No way to track what changed when
- Difficult to roll back problematic changes
- No audit trail for agent evolution

---

## Proposed Solution

### Overview

Implement formal agent governance with semantic versioning, PR-based review process, changelogs, and compatibility policies.

### Technical Requirements

#### 1. Agent Version Schema

```yaml
# Extended agent definition with versioning
agent:
  id: "section-drafter"
  name: "Section Drafter"
  displayName: "Jordan"
  
  versioning:
    version: "1.2.0"
    releaseDate: "2025-12-13"
    status: "stable"  # alpha | beta | stable | deprecated
    
    changelog:
      - version: "1.2.0"
        date: "2025-12-13"
        type: "minor"
        changes:
          - "Added support for multi-paragraph citations"
          - "Improved transition sentence generation"
        breaking: false
        
      - version: "1.1.0"
        date: "2025-11-15"
        type: "minor"
        changes:
          - "Added uncertainty flagging"
          - "Improved LaTeX formatting"
        breaking: false
        
      - version: "1.0.0"
        date: "2025-10-01"
        type: "major"
        changes:
          - "Initial release"
        breaking: false
        
    compatibility:
      minSystemVersion: "0.3.0"
      maxSystemVersion: null  # null = no upper limit
      requiredContracts: ["1.0.0"]
      
    deprecation:
      isDeprecated: false
      deprecatedDate: null
      removalDate: null
      replacementAgent: null
      migrationGuide: null
```

#### 2. Semantic Versioning Policy

```yaml
# .paper/_cfg/governance/versioning-policy.yaml
versioningPolicy:
  version: "1.0.0"
  
  semanticVersioning:
    # MAJOR.MINOR.PATCH
    
    major:
      triggers:
        - "Breaking changes to input/output schema"
        - "Removal of capabilities"
        - "Significant behavior changes"
      required:
        - migrationGuide: true
        - deprecationPeriod: "90d"
        - userNotification: true
        
    minor:
      triggers:
        - "New capabilities added"
        - "Non-breaking behavior improvements"
        - "New optional inputs/outputs"
      required:
        - changelog: true
        - documentation: true
        
    patch:
      triggers:
        - "Bug fixes"
        - "Documentation updates"
        - "Performance improvements"
      required:
        - changelog: true
        
  preRelease:
    alpha:
      description: "Early development, may change significantly"
      stability: "unstable"
      support: "none"
      
    beta:
      description: "Feature complete, testing phase"
      stability: "testing"
      support: "limited"
      
    rc:
      description: "Release candidate, final testing"
      stability: "stable"
      support: "full"
```

#### 3. Change Review Process

```yaml
# .paper/_cfg/governance/review-process.yaml
reviewProcess:
  version: "1.0.0"
  
  changeTypes:
    agent_definition:
      required:
        - prReview: true
        - minReviewers: 1
        - documentation: true
        - changelog: true
        - testCoverage: true
      labels:
        - "agent-change"
        
    agent_behavior:
      required:
        - prReview: true
        - minReviewers: 2
        - userImpactAssessment: true
        - regressionTests: true
      labels:
        - "agent-behavior"
        - "needs-review"
        
    breaking_change:
      required:
        - prReview: true
        - minReviewers: 2
        - migrationGuide: true
        - deprecationNotice: true
        - userNotification: true
      labels:
        - "breaking-change"
        - "needs-migration-guide"
        
  reviewChecklist:
    - item: "Version number updated"
      required: true
    - item: "Changelog entry added"
      required: true
    - item: "Documentation updated"
      required: true
    - item: "Tests pass"
      required: true
    - item: "Backward compatibility verified"
      required: false
    - item: "User impact documented"
      required: false
```

#### 4. Changelog Format

```markdown
# CHANGELOG.md

# Agent Changelog

All notable changes to agents are documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### section-drafter
- Improved handling of complex equations

## [2025-12-13] - v1.2.0

### section-drafter
#### Changed
- Improved transition sentence generation between paragraphs

#### Added
- Multi-paragraph citation support
- Better handling of in-text citations

### quality-refiner
#### Changed
- More specific feedback on paragraph flow

#### Fixed
- Issue with duplicate suggestions

## [2025-11-15] - v1.1.0

### section-drafter
#### Added
- Uncertainty flagging for unverified claims
- Improved LaTeX math formatting

### paper-architect
#### Changed
- Better section length estimation
```

#### 5. Per-Agent Changelog

```yaml
# .paper/core/agents/section-drafter.md (frontmatter)
---
id: section-drafter
version: 1.2.0
lastUpdated: 2025-12-13
status: stable

changelog:
  - version: 1.2.0
    date: 2025-12-13
    changes:
      added:
        - Multi-paragraph citation support
      changed:
        - Improved transition generation
      fixed: []
      deprecated: []
      removed: []
      security: []
    breaking: false
    
  - version: 1.1.0
    date: 2025-11-15
    changes:
      added:
        - Uncertainty flagging
        - Math formatting improvements
      changed: []
      fixed: []
    breaking: false
---

# Section Drafter Agent

...
```

#### 6. Deprecation Process

```yaml
# Deprecation lifecycle
deprecationProcess:
  phases:
    announce:
      duration: "30d"
      actions:
        - "Add deprecation notice to agent"
        - "Log deprecation warnings in usage"
        - "Notify users via changelog"
        - "Document migration path"
        
    soft_deprecation:
      duration: "60d"
      actions:
        - "Show deprecation warning on activation"
        - "Suggest replacement agent"
        - "Track usage for impact assessment"
        
    hard_deprecation:
      duration: "30d"
      actions:
        - "Require acknowledgment to use"
        - "Log all usage with warnings"
        - "Final migration reminders"
        
    removal:
      actions:
        - "Remove agent from registry"
        - "Keep documentation archived"
        - "Redirect to replacement"

# Example deprecation entry
deprecatedAgent:
  id: "old-research-agent"
  deprecatedDate: "2025-09-01"
  removalDate: "2025-12-01"
  reason: "Replaced by improved research-consolidator"
  replacementAgent: "research-consolidator"
  migrationGuide: "docs/migration/research-agent-migration.md"
```

#### 7. Compatibility Matrix

```yaml
# .paper/_cfg/governance/compatibility-matrix.yaml
compatibilityMatrix:
  lastUpdated: "2025-12-13"
  
  system:
    currentVersion: "0.4.0"
    
  agents:
    section-drafter:
      version: "1.2.0"
      compatible:
        - systemVersion: ">=0.3.0"
        - contracts: ["section-input-v1", "section-output-v1"]
      tested:
        - systemVersion: ["0.3.0", "0.3.1", "0.4.0"]
        
    paper-architect:
      version: "1.1.0"
      compatible:
        - systemVersion: ">=0.2.0"
        - contracts: ["outline-v1"]
      tested:
        - systemVersion: ["0.2.0", "0.3.0", "0.4.0"]
        
  contracts:
    section-input-v1:
      introducedIn: "0.3.0"
      deprecatedIn: null
      agents: ["section-drafter", "quality-refiner"]
      
    outline-v1:
      introducedIn: "0.2.0"
      deprecatedIn: null
      agents: ["paper-architect"]
```

#### 8. Governance Automation

```yaml
# .github/workflows/agent-governance.yaml
name: Agent Governance Checks

on:
  pull_request:
    paths:
      - '.paper/**/agents/**'
      - '.github/agents/**'

jobs:
  version-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Check version bump
        run: |
          python tools/governance/check-version-bump.py
          
      - name: Validate changelog
        run: |
          python tools/governance/validate-changelog.py
          
      - name: Check deprecation notices
        run: |
          python tools/governance/check-deprecations.py

  compatibility-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Verify compatibility matrix
        run: |
          python tools/governance/verify-compatibility.py
          
      - name: Run agent regression tests
        run: |
          pytest tests/agents/ -v
```

#### 9. Agent Registry

```yaml
# .paper/_cfg/agent-registry.yaml
agentRegistry:
  version: "1.0.0"
  lastUpdated: "2025-12-13"
  
  agents:
    # Core agents
    - id: "research-consolidator"
      version: "1.1.0"
      status: "stable"
      module: "core"
      
    - id: "paper-architect"
      version: "1.1.0"
      status: "stable"
      module: "core"
      
    - id: "section-drafter"
      version: "1.2.0"
      status: "stable"
      module: "core"
      
    - id: "quality-refiner"
      version: "1.0.1"
      status: "stable"
      module: "core"
      
    - id: "reference-manager"
      version: "1.0.0"
      status: "stable"
      module: "core"
      
    - id: "latex-assembler"
      version: "1.0.0"
      status: "stable"
      module: "core"
      
    # Specialist agents
    - id: "brainstorm"
      version: "1.0.0"
      status: "stable"
      module: "specialist"
      
    - id: "problem-solver"
      version: "1.0.0"
      status: "stable"
      module: "specialist"
      
    - id: "tutor"
      version: "1.0.0"
      status: "stable"
      module: "specialist"
      
    - id: "librarian"
      version: "1.0.0"
      status: "stable"
      module: "specialist"
      
  deprecated: []
  
  upcoming:
    - id: "peer-reviewer"
      expectedVersion: "0.1.0"
      expectedRelease: "2025-Q1"
      status: "planning"
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define versioning schema | 4 hours |
| 2 | Update agent manifests with versions | 4 hours |
| 3 | Create changelog format and templates | 2 hours |
| 4 | Define review process | 2 hours |
| 5 | Create deprecation policy | 2 hours |
| 6 | Build compatibility matrix | 4 hours |
| 7 | Create governance CI workflow | 6 hours |
| 8 | Build version bump tooling | 4 hours |
| 9 | Update existing agents with versions | 4 hours |
| 10 | Documentation | 2 hours |

**Total Estimated Effort:** 34 hours

---

## Success Criteria

- [ ] All agents have semantic version numbers
- [ ] Changelogs exist for all agents
- [ ] Review process enforced via CI
- [ ] Deprecation policy documented
- [ ] Compatibility matrix maintained
- [ ] Version bump required for agent changes
- [ ] CI validates governance requirements

---

## Dependencies

- [001-agent-metadata.md](001-agent-metadata.md) - Agent schema with version fields
- [005-testing-ci.md](005-testing-ci.md) - CI for governance checks

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Version fatigue | Low | Auto-increment for minor changes |
| Process overhead | Medium | Automate checks; templates |
| Breaking change missed | High | Regression tests; review checklist |
| Changelog not maintained | Medium | CI enforcement; templates |

---

## Related Specifications

- [001-agent-metadata.md](001-agent-metadata.md) - Agent definitions
- [002-workflow-agent-contract.md](002-workflow-agent-contract.md) - Contract versioning
- [005-testing-ci.md](005-testing-ci.md) - Governance CI

---

## Open Questions

1. How frequently should we release agent updates?
2. Should we support multiple agent versions simultaneously?
3. How to handle emergency fixes vs planned releases?
4. Should changelog be auto-generated from commits?

---

## References

- Semantic Versioning: https://semver.org/
- Keep a Changelog: https://keepachangelog.com/
- GitHub Releases: https://docs.github.com/en/repositories/releasing-projects-on-github
