# Specification: Incomplete/Fragmented Agent Metadata

**Spec ID:** 001-agent-metadata  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** High  
**Category:** Core Architecture

---

## Problem Statement

Agent-manifest.csv entries are truncated (ellipses visible in source), making it unclear whether agent instructions/principles are fully specified and machine-parseable. CSV format is inherently limited for complex, hierarchical agent definitions with long text fields.

### Current State

- Agent definitions stored in `agent-manifest.csv` format
- Fields include: name, displayName, title, icon, role, identity, communicationStyle, principles, module, path
- Long text fields are truncated or abbreviated
- No schema validation for agent definitions
- Limited extensibility for new fields (capabilities, constraints, example prompts, input/output schema)

### Impact

- Machine parsing unreliable due to CSV escaping issues with complex text
- Agent definitions incomplete or ambiguous
- Difficult to extend with new fields
- No formal validation of agent specifications
- Hard to version or diff agent changes effectively

---

## Proposed Solution

### Overview

Migrate from CSV to YAML/JSON format for agent manifests with full schema validation.

### Technical Requirements

1. **Convert to YAML Format**
   - Create new `agent-manifest.yaml` or individual agent YAML files
   - Support hierarchical data structures
   - Enable full-length descriptions and principles without truncation

2. **Define JSON Schema for Validation**
   - Create `schemas/agent-schema.json` with OpenAPI-compatible format
   - Validate all required fields: name, displayName, role, identity, etc.
   - Support optional extended fields: capabilities[], constraints[], examplePrompts[]

3. **Extended Agent Fields**
   ```yaml
   # Naming Convention:
   # - name: Machine identifier (kebab-case, used in code/configs)
   # - displayName: Human persona name (used in UI for personality)
   # - title: Functional title (used in UI for capability description)
   
   name: research-consolidator       # Machine identifier
   displayName: Alex                 # Persona name shown in UI
   title: Research Consolidator      # Functional title/role in UI
   version: 1.0.0
   module: core
   
   identity:
     role: Research Synthesizer
     description: >
       Transforms scattered research materials into polished, 
       synthesized research documents with proper citations
     communicationStyle: Academic but accessible
   
   capabilities:
     - Synthesize research materials
     - Extract and organize citations
     - Identify research gaps
   
   constraints:
     - Never fabricate citations
     - Always flag uncertain claims
     - Require source verification
   
   principles:
     - Synthesize into narrative
     - Every claim needs citation
     - Flag gaps proactively
   
   inputSchema:
     type: object
     properties:
       topic: { type: string }
       sources: { type: array }
       depth: { type: string, enum: [shallow, moderate, deep] }
   
   outputSchema:
     type: object
     properties:
       document: { type: string }
       citations: { type: array }
       gaps: { type: array }
   
   examplePrompts:
     - "Research color theory foundations from these 5 papers"
     - "Consolidate my notes on machine learning into a coherent summary"
   
   owner: core-team
   path: .paper/core/agents/research-consolidator.md
   ```

4. **Schema Validation Tool**
   - Add validation script: `tools/validate-agent-schema.py`
   - Integrate with CI pipeline
   - Report clear error messages for schema violations

### Migration Strategy

1. Create new YAML agent definitions alongside existing CSV
2. Build validation tooling
3. Update all agent references to use YAML source
4. Deprecate and remove CSV after migration complete
5. Document new format in developer docs

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define JSON Schema for agent definitions | 4 hours |
| 2 | Create YAML template and convert first agent | 2 hours |
| 3 | Convert remaining agents to YAML | 4 hours |
| 4 | Build validation script | 4 hours |
| 5 | Update manifest registry references | 2 hours |
| 6 | Add CI validation job | 2 hours |
| 7 | Update documentation | 2 hours |
| 8 | Remove deprecated CSV | 1 hour |

**Total Estimated Effort:** 21 hours

---

## Success Criteria

- [ ] All agents defined in YAML with full fields (no truncation)
- [ ] JSON Schema exists and validates all agent definitions
- [ ] Validation runs in CI and blocks invalid changes
- [ ] Agent definitions include: capabilities, constraints, input/output schemas
- [ ] Documentation updated with new agent specification format
- [ ] Old CSV format deprecated and removed

---

## Dependencies

- None (foundational change)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Breaking existing references | Medium | Phased migration with backward compatibility |
| Schema too restrictive | Low | Start with flexible schema, tighten over time |
| Complex nested YAML parsing | Low | Use established YAML libraries |

---

## Related Specifications

- [002-workflow-agent-contract.md](002-workflow-agent-contract.md) - Uses agent schema for workflow contracts
- [010-agent-governance.md](010-agent-governance.md) - Agent versioning depends on structured metadata

---

## Open Questions

1. Should agents be defined in individual YAML files or a single manifest file?
2. What validation strictness level is appropriate for v1?
3. Should we support JSON alongside YAML for tooling compatibility?

---

## References

- Current: `.paper/_cfg/agent-manifest.csv`
- OpenAPI Specification: https://spec.openapis.org/
- JSON Schema: https://json-schema.org/
