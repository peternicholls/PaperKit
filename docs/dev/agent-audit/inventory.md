# Agent System Inventory

Generated: 2026-01-06

## Overview

This document inventories all agent definition files in PaperKit.

## Dual System Discovery

PaperKit has **two parallel agent definition systems**:

### System 1: YAML Metadata Files
Location: `.paperkit/_cfg/agents/`

| File | Schema-Compliant | Notes |
|------|------------------|-------|
| brainstorm.yaml | ✅ | Points to specialist/agents/brainstorm.md |
| latex-assembler.yaml | ✅ | Points to core/agents/latex-assembler.md |
| librarian.yaml | ✅ | Points to specialist/agents/librarian.md |
| orchestrator.yaml | ❌ | Missing: identity, path; Extra: decisionSchema, instructions, schemaVersion, status |
| paper-architect.yaml | ✅ | Points to core/agents/paper-architect.md |
| problem-solver.yaml | ✅ | Points to core/agents/problem-solver.md |
| quality-refiner.yaml | ✅ | Points to core/agents/quality-refiner.md |
| reference-manager.yaml | ✅ | Points to core/agents/reference-manager.md |
| research-consolidator.yaml | ✅ | Points to core/agents/research-consolidator.md |
| section-drafter.yaml | ✅ | Points to core/agents/section-drafter.md |
| tutor.yaml | ✅ | Points to specialist/agents/tutor.md |

### System 2: Markdown Agent Files (with YAML Frontmatter)
Location: `.paperkit/{core,specialist}/agents/`

#### Core Agents
| File | Has Frontmatter | Notes |
|------|-----------------|-------|
| latex-assembler.md | ✅ | Operational instructions |
| orchestrator.md | ✅ | Full schema-compliant metadata + instructions |
| paper-architect.md | ✅ | Operational instructions |
| quality-refiner.md | ✅ | Operational instructions |
| reference-manager.md | ✅ | Operational instructions |
| research-consolidator.md | ✅ | Operational instructions |
| section-drafter.md | ✅ | Operational instructions |

#### Specialist Agents
| File | Has Frontmatter | Notes |
|------|-----------------|-------|
| brainstorm.md | ✅ | Operational instructions |
| librarian.md | ✅ | Operational instructions |
| problem-solver.md | ✅ | Operational instructions |
| tutor.md | ✅ | Operational instructions |

## Manifest Files

| File | Location | Purpose |
|------|----------|---------|
| agent-manifest.yaml | `.paperkit/_cfg/` | Index of all agents with paths to YAML files |
| manifest.yaml | `.paperkit/_cfg/` | Master manifest pointing to schemas |

## Schema Files

| File | Location | Used By |
|------|----------|---------|
| agent-schema.json | `.paperkit/_cfg/schemas/` | validate-agent-schema.py |

## Key Findings

1. **Duplication exists**: Each agent has BOTH a `.yaml` metadata file AND a `.md` definition file
2. **Schema expects MD files**: The `path` property regex requires `.paperkit/(core|specialist)/agents/*.md`
3. **Runtime uses MD files**: `generate.sh` scans `.paperkit/{core,specialist}/agents/*.md`
4. **Validation checks YAML**: `validate-agent-schema.py` checks `.paperkit/_cfg/agents/*.yaml`
5. **YAML files reference MD files**: Each YAML file has a `path` field pointing to the MD file
6. **orchestrator.yaml is non-compliant**: Missing required fields and has extra properties
