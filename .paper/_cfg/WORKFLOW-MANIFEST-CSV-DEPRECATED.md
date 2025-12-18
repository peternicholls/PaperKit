# Workflow Manifest CSV Format Deprecated

**Date:** 2025-12-14  
**Status:** Deprecated  
**Migration Complete:** Yes

## Notice

The CSV format for workflow metadata (`workflow-manifest.csv`) has been **deprecated** in favor of structured YAML format with JSON Schema validation.

## Why This Change?

The CSV format had several limitations:
- ❌ Limited structure (flat rows)
- ❌ No validation
- ❌ Hard to extend with new fields
- ❌ Poor version control diffs
- ❌ No workflow steps or agent relationships

## New Format: YAML

Workflow definitions are now stored as individual YAML files with full metadata, step definitions, agent relationships, and validation.

### Location

- **Individual Definitions**: `.paper/_cfg/workflows/*.yaml`
- **Master Index**: `.paper/_cfg/workflow-manifest.yaml`
- **Schema**: `.paper/_cfg/schemas/workflow-schema.json`

### Example

```yaml
name: write-section
displayName: Write Section
description: Draft a complete section with academic rigor
version: 1.0.0
module: core
category: drafting
path: .paper/core/workflows/drafting/write-section.yaml

agents:
  - section-drafter

steps:
  - name: understand-context
    agent: section-drafter
    description: Review outline and surrounding sections
  - name: draft-content
    agent: section-drafter
    description: Write section content with academic tone

inputSchema:
  type: object
  properties:
    sectionName:
      type: string
      description: Name of section to write

outputSchema:
  type: object
  properties:
    content:
      type: string
      description: Drafted section content in LaTeX
```

## Migration Guide

### For Developers

1. **Read YAML instead of CSV**
   ```python
   import yaml
   
   # Old: Reading CSV
   # import csv
   # with open('.paper/_cfg/workflow-manifest.csv') as f:
   #     reader = csv.DictReader(f)
   
   # New: Reading YAML
   with open('.paper/_cfg/workflow-manifest.yaml') as f:
       manifest = yaml.safe_load(f)
       workflows = manifest['workflows']
   ```

2. **Use individual workflow files for detailed metadata**
   ```python
   def load_workflow(workflow_name: str) -> dict:
       path = f'.paper/_cfg/workflows/{workflow_name}.yaml'
       with open(path) as f:
           return yaml.safe_load(f)
   
   workflow = load_workflow('write-section')
   print(workflow['steps'])
   print(workflow['agents'])
   ```

### For Workflow Authors

1. Create new workflow definition: `.paper/_cfg/workflows/my-workflow.yaml`
2. Follow the JSON Schema: `.paper/_cfg/schemas/workflow-schema.json`
3. Add to manifest: `.paper/_cfg/workflow-manifest.yaml`
4. Validate: `python3 open-agents/tools/validate-workflow-schema.py`

## Validation

```bash
# Validate all workflows
python3 open-agents/tools/validate-workflow-schema.py

# Validate specific workflow
python3 open-agents/tools/validate-workflow-schema.py --workflow write-section
```

## Benefits of New Format

- ✅ Full metadata (no truncation)
- ✅ Hierarchical structure with steps
- ✅ JSON Schema validation
- ✅ Better version control diffs
- ✅ Easy to extend
- ✅ Input/output schemas for tooling
- ✅ Explicit agent relationships
- ✅ Workflow step definitions

## Backward Compatibility

The old CSV file has been renamed to `workflow-manifest.csv.deprecated` and is kept for reference only. All new development should use the YAML format.

## Workflow Categories

Workflows are now organized by category:

**Core Categories:**
- research
- planning
- drafting
- refinement
- references
- assembly

**Specialist Categories:**
- brainstorm
- problem-solving
- tutor
- librarian

## Questions?

See documentation:
- `.paper/_cfg/workflows/README.md` - Workflow definitions guide
- `.paper/_cfg/schemas/README.md` - Schema reference
- `DEVELOPER-IMPROVEMENTS/001-agent-metadata-migration-guide.md` - Migration patterns
- `DEVELOPER-IMPROVEMENTS/002-workflow-agent-contract.md` - Workflow contract specification

## Related Changes

This deprecation follows the same pattern as:
- Agent metadata migration (completed 2025-12-14)
- Tool metadata migration (completed 2025-12-14)

All manifest files in PaperKit now use YAML format with JSON Schema validation.
