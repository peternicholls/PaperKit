# Agent Manifest CSV Format - DEPRECATED

**Date:** 2024-12-14  
**Status:** Deprecated  
**Replacement:** YAML format with JSON Schema validation

## Summary

The CSV format for agent manifests (`agent-manifest.csv`) has been **deprecated** in favor of structured YAML files with JSON Schema validation.

## Why the Change?

The CSV format had several limitations:

1. **Truncation Issues**: Long text fields were truncated with ellipses, making agent definitions incomplete
2. **Limited Structure**: CSV cannot represent hierarchical data (capabilities, constraints, input/output schemas)
3. **No Validation**: No schema validation to ensure agent definitions are complete and consistent
4. **Hard to Extend**: Adding new fields requires changing all consumers
5. **Poor Diff Support**: CSV changes are hard to review in version control

## New Format

Agent definitions are now stored as individual YAML files in `.paper/_cfg/agents/` with:

- **Full-length fields**: No truncation of descriptions or principles
- **Hierarchical structure**: Supports nested data like capabilities, constraints, schemas
- **JSON Schema validation**: Automated validation ensures completeness
- **Better diffs**: YAML changes are easier to review in Git
- **Extensibility**: Easy to add new fields without breaking existing tools

## Migration Path

### Old Format (CSV)
```csv
name,displayName,title,icon,role,identity,communicationStyle,principles,module,path
"research-consolidator","Alex","Research Consolidator","🔬","Research Synthesizer","Transforms scattered research materials...","Academic but accessible...","Synthesize into narrative; Every claim...","core",".paper/core/agents/research-consolidator.md"
```

### New Format (YAML)
```yaml
name: research-consolidator
displayName: Alex
title: Research Consolidator
icon: 🔬
version: 1.0.0
module: core

identity:
  role: Research Synthesizer
  description: >
    Transforms scattered research materials into polished, synthesized research 
    documents with proper citations and clear narrative structure.
  communicationStyle: Academic but accessible. Precise terminology with clear explanations.

capabilities:
  - Synthesize research materials into coherent narratives
  - Extract and organize citations from multiple sources
  - Identify research gaps and areas needing more investigation

principles:
  - Synthesize information into coherent narrative, not lists of facts
  - Every factual claim should have a citation
  - Never make up citations or attributes

# ... plus input/output schemas, example prompts, etc.
```

## How to Use New Format

### Validation
```bash
# Validate all agents
python3 open-agents/tools/validate-agent-schema.py

# Validate specific agent
python3 open-agents/tools/validate-agent-schema.py --agent research-consolidator

# CI mode (exit with error on failure)
python3 open-agents/tools/validate-agent-schema.py --ci
```

### Loading Agents
```python
import yaml
from pathlib import Path

# Load single agent
with open('.paper/_cfg/agents/research-consolidator.yaml') as f:
    agent = yaml.safe_load(f)

# Load all agents from manifest
with open('.paper/_cfg/agent-manifest.yaml') as f:
    manifest = yaml.safe_load(f)
    for agent_ref in manifest['agents']:
        agent_path = Path(agent_ref['path'])
        with open(agent_path) as af:
            agent_data = yaml.safe_load(af)
```

## Files

- **Schema**: `.paper/_cfg/schemas/agent-schema.json`
- **Manifest**: `.paper/_cfg/agent-manifest.yaml`
- **Individual Agents**: `.paper/_cfg/agents/*.yaml`
- **Validation Tool**: `open-agents/tools/validate-agent-schema.py`
- **Old CSV (deprecated)**: `.paper/_cfg/agent-manifest.csv.deprecated`

## Timeline

- **2024-12-14**: YAML format introduced, CSV marked deprecated
- **Future**: CSV file will be removed after all tools migrate to YAML

## Questions?

See documentation:
- `DEVELOPER-IMPROVEMENTS/001-agent-metadata.md` - Full specification
- `DEVELOPER-IMPROVEMENTS/001-agent-metadata-plan.md` - Implementation plan
