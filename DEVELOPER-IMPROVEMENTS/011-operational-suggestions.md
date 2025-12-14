# Smaller/Operational Suggestions

**Document ID:** 011-operational-suggestions  
**Date:** 2024-12-13  
**Status:** Reference  
**Category:** Operations

---

## Overview

This document captures smaller operational suggestions that don't warrant full specification documents but should be tracked for future implementation.

---

## Manifest Format Migration

### Suggestion
Prefer YAML/JSON manifests over CSV for agent/workflow/tool manifests for better extensibility.

### Current State
- `agent-manifest.csv`
- `workflow-manifest.csv`
- `tool-manifest.csv`

### Proposed
- Migrate to YAML format
- Single structured file or per-item YAML files
- JSON Schema validation

### Priority
Medium

### Related Specs
- [001-agent-metadata.md](001-agent-metadata.md)

---

## Repository Governance Files

### Suggestion
Include a CONTRIBUTING.md, CODE_OF_CONDUCT, and LICENSE in the repo root.

### Current State
- CONTRIBUTING.md exists ✓
- LICENSE exists ✓
- CODE_OF_CONDUCT missing

### Action
Create CODE_OF_CONDUCT.md following Contributor Covenant

### Priority
Low

---

## Agent-to-Agent Orchestration

### Suggestion
Add examples of agent-to-agent orchestration (if one agent should call another, specify patterns).

### Current State
Workflow defines agent sequence but no explicit inter-agent communication pattern documented.

### Proposed
- Document orchestration patterns
- Add example: "Architect calls Researcher for source suggestions"
- Define message passing format

### Priority
Medium

### Related Specs
- [002-workflow-agent-contract.md](002-workflow-agent-contract.md)

---

## Human-in-the-Loop Approval

### Suggestion
Provide a human-in-the-loop approval step for final manuscript assembly/publishing.

### Current State
LaTeX Assembler builds without explicit approval step.

### Proposed
- Add "review and approve" stage before final build
- Show diff of all changes since last approved version
- Require explicit user confirmation

### Priority
Medium

### Related Specs
- [003-consent-sandboxing.md](003-consent-sandboxing.md)
- [009-state-management.md](009-state-management.md)

---

## Retry and Rate Limiting

### Suggestion
Add retry/backoff semantics for external calls and rate-limit awareness for APIs used to fetch sources.

### Current State
No documented retry policy or rate limit handling.

### Proposed
```yaml
retryPolicy:
  maxRetries: 3
  backoff:
    initial: 1s
    multiplier: 2
    max: 30s
  retryableErrors:
    - timeout
    - rate_limit
    - server_error

rateLimits:
  crossref:
    requestsPerSecond: 50
    burstSize: 100
  semanticScholar:
    requestsPerSecond: 10
```

### Priority
Medium

### Related Specs
- [004-security-governance.md](004-security-governance.md)
- [007-citation-validation.md](007-citation-validation.md)

---

## Docker LaTeX Environment

### Suggestion
Consider bundling a Docker image that contains a known-good LaTeX toolchain to make builds reproducible across environments.

### Current State
Users must install their own LaTeX distribution.

### Proposed
```dockerfile
FROM texlive/texlive:latest

# Add Paper Kit tools
COPY tools/ /paperkit/tools/
COPY latex/ /paperkit/latex/

# Standard build command
CMD ["./tools/build-latex.sh"]
```

### Priority
High

### Related Specs
- [005-testing-ci.md](005-testing-ci.md)

---

## Expanded Tool Manifest

### Suggestion
Expand tool-manifest to include security impact levels and expected runtime/resource usage.

### Current State
Tool manifest only includes: name, displayName, description, path, requiresConsent

### Proposed Additional Fields
```yaml
tool:
  name: build-latex
  
  # Existing fields
  displayName: Build LaTeX
  description: Compile LaTeX to PDF
  path: tools/build-latex.sh
  requiresConsent: true
  
  # New fields
  securityImpact: medium  # low | medium | high | critical
  expectedRuntime: "30-60s"
  resourceUsage:
    cpu: medium
    memory: "256MB"
    disk: "50MB"
  networkRequired: false
  modifiesFiles: true
  modifiedPaths:
    - "output-final/pdf/"
    - "latex/*.aux"
```

### Priority
Low

### Related Specs
- [003-consent-sandboxing.md](003-consent-sandboxing.md)

---

## Implementation Priority Matrix

| Suggestion | Priority | Effort | Impact |
|------------|----------|--------|--------|
| Docker LaTeX Environment | High | Medium | High |
| Retry/Rate Limiting | Medium | Low | Medium |
| Human-in-the-Loop | Medium | Medium | High |
| Agent Orchestration Examples | Medium | Low | Medium |
| Manifest Format Migration | Medium | High | Medium |
| Tool Manifest Expansion | Low | Low | Low |
| CODE_OF_CONDUCT | Low | Low | Low |

---

## Quick Wins (< 2 hours each)

1. Add CODE_OF_CONDUCT.md
2. Document retry policy in README
3. Add rate limit notes to citation validation docs
4. Create basic Dockerfile for builds

---

## Next Steps

1. Prioritize based on user feedback
2. Create issues for tracking
3. Assign to appropriate milestones
4. Consider bundling with related spec implementations
