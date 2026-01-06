# Agent System Unification Decision

Generated: 2026-01-06

## Decision

**Canonical Agent Definition System**: Markdown files with YAML frontmatter at `.paperkit/{core,specialist}/agents/*.md`

**YAML files at `.paperkit/_cfg/agents/*.yaml`**: Retained as supplementary metadata index (NOT deprecated)

## Rationale

### Evidence from Repository

1. **Schema Design**:
   - `agent-schema.json` path regex: `^\\.paperkit/(core|specialist)/agents/[a-z][a-z0-9-]*\\.md$`
   - This explicitly expects MD files, not YAML

2. **Runtime Loader**:
   - `generate.sh` reads from `.paperkit/{core,specialist}/agents/*.md`
   - Generated IDE files reference the MD locations

3. **Existing Pattern**:
   - All 11 MD agent files have YAML frontmatter with schema-compliant metadata
   - The `orchestrator.md` file is fully compliant with the schema
   - MD files contain both metadata AND operational instructions

4. **YAML Files Purpose**:
   - Each YAML file has a `path` property pointing to the corresponding MD file
   - They provide a machine-readable index without parsing frontmatter
   - Used by CI validation workflow

### Why Not Retire YAML Files?

1. **They serve a purpose**: Quick lookup of agent metadata without parsing MD
2. **CI workflow uses them**: `validate-agent-metadata.yml` validates the YAML files
3. **Manifest references them**: `agent-manifest.yaml` points to YAML files
4. **No duplication of instructions**: YAML files don't contain operational prompts

### The Real Problem

The issue isn't that YAML files exist—it's that:
1. `orchestrator.yaml` is non-compliant with the schema
2. `validate.py` has hardcoded wrong paths (`.paper/` instead of `.paperkit/`)
3. orchestrator is missing from `agent-manifest.yaml`

## Implementation Plan

### Phase 1: Fix Schema Compliance
- [ ] Update `orchestrator.yaml` to be schema-compliant
- [ ] Verify all YAML files pass validation

### Phase 2: Fix Validation Scripts
- [ ] Update `validate.py` to use `.paperkit/` paths

### Phase 3: Update Manifest
- [ ] Add orchestrator to `agent-manifest.yaml`

### Phase 4: Add Unified Check
- [ ] Create `tools/check-agents.sh` that:
  - Validates all YAML files against schema
  - Validates all MD frontmatter against schema
  - Checks for name mismatches
  - Ensures path references exist
  - Detects duplicate agent names

### Phase 5: Documentation
- [ ] Create "How agents are structured" guide

## Compatibility Layer

**Not needed.** The dual system is intentional:
- MD files = canonical definitions (metadata + instructions)
- YAML files = supplementary metadata index

Both should reference the same MD paths and pass schema validation.
