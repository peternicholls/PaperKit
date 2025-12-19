# Implementation Plan: Incomplete/Fragmented Agent Metadata

**Branch**: `[001-agent-metadata]` | **Date**: 2025-12-14 | **Spec**: DEVELOPER-IMPROVEMENTS/001-agent-metadata.md
**Input**: Feature specification from `/specs/001-agent-metadata/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Migrate agent metadata from truncated CSV entries to structured YAML (or per-agent YAML files) with JSON Schema validation and richer fields (capabilities, constraints, example prompts, input/output schemas), backed by validation tooling and CI gating.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: NEEDS CLARIFICATION  
**Primary Dependencies**: NEEDS CLARIFICATION  
**Storage**: N/A  
**Testing**: NEEDS CLARIFICATION  
**Target Platform**: NEEDS CLARIFICATION  
**Project Type**: NEEDS CLARIFICATION  
**Performance Goals**: NEEDS CLARIFICATION  
**Constraints**: NEEDS CLARIFICATION  
**Scale/Scope**: NEEDS CLARIFICATION

## Constitution Check

- Reviewed `DEVELOPER-IMPROVEMENTS/011-operational-suggestions.md` for related migration guidance (YAML preference and validation focus).
- Reviewed `DEVELOPER-IMPROVEMENTS/012-open-questions.md` for blocking decisions (manifest file structure, validation strictness, YAML vs JSON support).
- Reviewed `DEVELOPER-IMPROVEMENTS/README.md` for dependencies, priority, and implementation sequencing.

## Project Structure

### Documentation (this feature)
- Plan: `DEVELOPER-IMPROVEMENTS/001-agent-metadata-plan.md`
- Spec: `DEVELOPER-IMPROVEMENTS/001-agent-metadata.md`
- Related references: `DEVELOPER-IMPROVEMENTS/011-operational-suggestions.md`, `DEVELOPER-IMPROVEMENTS/012-open-questions.md`, `DEVELOPER-IMPROVEMENTS/README.md`

### Source Code (repository root)

**Structure Decision**: Maintain existing repository layout while introducing new agent manifest artifacts under a dedicated structured format path (e.g., `.paper/_cfg/agents/` or similar), aligning with future YAML/JSON schema validation tooling alongside existing scripts.

## Complexity Tracking

> **Fill ONLY if there are open questions and inconsistencies that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| — | — | — |

## Milestones & Timeline

- **Milestone 1:** Define JSON Schema and YAML template for agents; select manifest organization (single vs per-agent) and document decisions. 
- **Milestone 2:** Convert initial agents to YAML and implement schema validation tooling; integrate into local developer workflow. 
- **Milestone 3:** Migrate remaining agents, update references, and wire validation into CI gates; deprecate CSV manifest. 
- **Milestone 4:** Update documentation and governance materials to reflect new manifest format and validation policies.

## Risks & Mitigations

- **Blocking decisions unresolved (manifest structure, strictness, JSON support):** Track Q1.1–Q1.3 and secure stakeholder decisions before tooling lock-in; design schema to accommodate a hybrid model if needed.
- **Backward compatibility with existing CSV consumers:** Provide transitional loaders or dual-read paths until migration completes; communicate deprecation timeline.
- **Validation friction for long-form fields:** Start with progressive strictness (warnings where possible) and tighten after initial adoption.

## Stakeholders & Approvals

- **Owners:** Core architecture maintainers (agent metadata owners).
- **Reviewers:** Workflow and governance leads (due to dependencies on contract validation and versioning).
- **Approvals Required:** Sign-off on schema strictness level, manifest layout, and CI enforcement timing.

## Definition of Done

- All agent definitions authored in YAML (or equivalent structured format) with full, untruncated fields.
- JSON Schema validated locally and in CI, blocking invalid metadata.
- Documentation updated to describe manifest format, migration path, and validation workflow.
- Deprecated CSV manifest removed or clearly marked and scheduled for removal.

## Assumptions

- Team agrees to adopt YAML as the primary authoring format with JSON Schema for validation.
- Existing tooling can be adapted or replaced to consume YAML manifests without major refactors.
- CI environment can run schema validation without new platform constraints.

## Dependencies & Alignments

- Ties directly to workflow contract work (spec 002) and governance (spec 010) for versioning and validation policies.
- Aligns with operational suggestions promoting YAML manifests and validation (doc 011).
- Must resolve open questions outlined in doc 012 before locking the schema.
