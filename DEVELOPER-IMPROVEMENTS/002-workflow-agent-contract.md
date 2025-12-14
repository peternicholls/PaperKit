# Specification: Workflow and Agent Linking Formal Contract

**Spec ID:** 002-workflow-agent-contract  
**Date:** 2024-12-13  
**Status:** Draft  
**Priority:** High  
**Category:** Core Architecture

---

## Problem Statement

The manifests list workflows and agents, but there is no explicit schema defining how workflows call agents, what inputs each agent expects, and how state is passed between steps. This creates ambiguity in workflow execution and makes debugging difficult.

### Current State

- `workflow-manifest.csv` lists workflows with basic metadata
- Workflow definitions reference agents loosely
- No formal input/output contracts between workflow steps
- State passing between agents is implicit
- Error handling and fallback behavior undefined

### Impact

- Workflow orchestration relies on implicit conventions
- Difficult to validate workflow correctness before execution
- State passing errors silently propagate
- No clear error recovery semantics
- Testing workflows requires end-to-end execution

---

## Proposed Solution

### Overview

Define a formal "agent contract" specification for each workflow step, with explicit schemas for inputs, outputs, side effects, and error handling.

### Technical Requirements

1. **Agent Contract Schema**
   ```yaml
   # Schema for agent contract in workflow context
   contractVersion: "1.0.0"
   
   agentId: section-drafter
   workflowStep: write-section
   
   input:
     schema:
       type: object
       required: [sectionName, outline, research]
       properties:
         sectionName:
           type: string
           description: Name of section to draft
         outline:
           type: object
           description: Section outline from Paper Architect
         research:
           type: array
           items:
             type: object
             properties:
               source: { type: string }
               citations: { type: array }
         context:
           type: object
           description: Optional context from previous steps
     
   output:
     schema:
       type: object
       properties:
         draftContent:
           type: string
           description: LaTeX-formatted section content
         citations:
           type: array
           description: Citations used in draft
         uncertainAreas:
           type: array
           description: Areas flagged for review
         completionStatus:
           type: string
           enum: [complete, partial, blocked]
     required: [draftContent, completionStatus]
   
   sideEffects:
     filesWritten:
       - path: output-drafts/sections/{sectionName}.tex
         description: Draft section file
       - path: memory/section-status.yaml
         description: Updated status tracking
     filesRead:
       - path: output-refined/research/*.md
       - path: output-drafts/outlines/*.md
     externalCalls: []
   
   resources:
     estimatedTime: "5-15 minutes"
     tokenBudget: 8000
     memoryRequired: "standard"
   
   errorHandling:
     onInputValidationFailure:
       action: reject
       message: "Invalid input: {validationErrors}"
     onPartialCompletion:
       action: return_partial
       requiresFlags: [uncertainAreas]
     onTimeout:
       action: checkpoint_and_retry
       maxRetries: 2
     onAgentFailure:
       action: escalate_to_user
       fallbackAgent: null
   
   compatibility:
     minAgentVersion: "1.0.0"
     requiresContext: [outline, research]
     providesContext: [draftContent, citations]
   ```

2. **Workflow State Schema**
   ```yaml
   # Schema for workflow state passed between steps
   workflowState:
     id: "wf-{uuid}"
     name: "write-paper"
     startedAt: "2024-12-13T10:00:00Z"
     currentStep: "draft-introduction"
     status: in_progress
     
     context:
       paperMetadata:
         title: "Color Perception Modeling"
         targetLength: 10000
       
       completedSteps:
         - stepId: outline
           agentId: paper-architect
           completedAt: "2024-12-13T10:05:00Z"
           outputs:
             outline: { $ref: "memory/outline.yaml" }
       
       artifacts:
         outline: "output-drafts/outlines/paper-outline.md"
         researchDoc: "output-refined/research/consolidated.md"
     
     nextSteps:
       - stepId: draft-introduction
         agentId: section-drafter
         inputs:
           sectionName: introduction
           outline: { $ref: "context.artifacts.outline" }
   ```

3. **Contract Validation Tool**
   - `tools/validate-workflow-contracts.py`
   - Verify all workflow steps have valid contracts
   - Check input/output schema compatibility between steps
   - Validate side effect declarations

4. **State Management**
   - Define state serialization format
   - Implement checkpoint/restore for long workflows
   - Track provenance of all artifacts

### Workflow Integration Pattern

```yaml
# Example workflow definition with contracts
workflow:
  name: write-paper
  version: "1.0.0"
  
  steps:
    - id: consolidate
      agent: research-consolidator
      contract: contracts/research-consolidator.yaml
      inputs:
        topic: { $input: "topic" }
        sources: { $input: "sources" }
      outputs:
        researchDoc: { $store: "artifacts.researchDoc" }
    
    - id: outline
      agent: paper-architect
      contract: contracts/paper-architect.yaml
      dependsOn: [consolidate]
      inputs:
        topic: { $input: "topic" }
        research: { $ref: "artifacts.researchDoc" }
      outputs:
        outline: { $store: "artifacts.outline" }
    
    - id: draft-sections
      forEach: { $ref: "artifacts.outline.sections" }
      agent: section-drafter
      contract: contracts/section-drafter.yaml
      dependsOn: [outline]
      inputs:
        sectionName: { $item: "name" }
        outline: { $item: "outline" }
        research: { $ref: "artifacts.researchDoc" }
      outputs:
        draft: { $store: "artifacts.drafts.{$item.name}" }
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Define contract schema specification | 6 hours |
| 2 | Define workflow state schema | 4 hours |
| 3 | Create contract templates for all agents | 8 hours |
| 4 | Build contract validation tool | 6 hours |
| 5 | Implement state serialization | 4 hours |
| 6 | Update workflow definitions with contracts | 6 hours |
| 7 | Add CI validation | 2 hours |
| 8 | Documentation and examples | 4 hours |

**Total Estimated Effort:** 40 hours

---

## Success Criteria

- [ ] Every agent has a formal contract definition
- [ ] Workflow definitions explicitly reference contracts
- [ ] Input/output schema validation passes for all workflows
- [ ] State passing between steps is explicit and validated
- [ ] Error handling semantics defined for all failure modes
- [ ] Contract compatibility checked between workflow steps

---

## Dependencies

- [001-agent-metadata.md](001-agent-metadata.md) - Agent schema provides base for contracts

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Over-specification reduces flexibility | Medium | Start with loose schemas, tighten based on usage |
| Contract maintenance burden | Medium | Auto-generate contract stubs from agent definitions |
| Breaking existing workflows | High | Implement contracts incrementally, validate compatibility |

---

## Related Specifications

- [001-agent-metadata.md](001-agent-metadata.md) - Agent definitions
- [009-state-management.md](009-state-management.md) - Session state management
- [005-testing-ci.md](005-testing-ci.md) - Contract testing in CI

---

## Open Questions

1. How strict should input validation be (fail-fast vs lenient)?
2. Should contracts be versioned independently of agents?
3. How to handle dynamic workflows where steps are determined at runtime?
4. Should we support contract inheritance for common patterns?

---

## References

- Current: `.paper/_cfg/workflow-manifest.csv`
- OpenAPI: https://spec.openapis.org/
- AsyncAPI: https://www.asyncapi.com/
