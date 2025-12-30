# Agent Metadata Migration Guide

**Date:** 2025-12-14  
**Spec:** DEVELOPER-IMPROVEMENTS/001-agent-metadata.md  
**Status:** Complete

## Overview

This guide documents the successful migration of agent metadata from CSV format to structured YAML with JSON Schema validation.

## What Changed

### Before (CSV Format)

```csv
name,displayName,title,icon,role,identity,communicationStyle,principles,module,path
"research-consolidator","Alex","Research Consolidator","🔬","Research Synthesizer","Transforms scattered research materials into polished, synthesized research documents with proper citations and clear narrative structure.","Academic but accessible. Precise terminology with clear explanations.","Synthesize into narrative; Every claim needs citation; Flag gaps; Never fabricate","core",".paper/core/agents/research-consolidator.md"
```

**Problems:**
- Fields truncated with semicolons instead of full arrays
- Limited structure (flat CSV rows)
- No validation
- Hard to extend with new fields
- Poor version control diffs

### After (YAML Format)

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

constraints:
  - Never fabricate citations or attributes
  - Always flag uncertain claims with qualifiers
  - Require source verification for factual claims

principles:
  - Synthesize information into coherent narrative, not lists of facts
  - Every factual claim should have a citation
  - Never make up citations or attributes

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

**Benefits:**
- ✅ Full-length fields (no truncation)
- ✅ Hierarchical structure (nested objects and arrays)
- ✅ JSON Schema validation
- ✅ Better diffs in version control
- ✅ Easy to extend with new fields
- ✅ Input/output schemas for better tooling

## Files Created

### Schema and Validation

| File | Purpose |
|------|---------|
| `.paper/_cfg/schemas/agent-schema.json` | JSON Schema definition |
| `open-agents/tools/validate-agent-schema.py` | Validation tool |
| `.github/workflows/validate-agent-metadata.yml` | CI workflow |

### Agent Definitions

| File | Agent |
|------|-------|
| `.paper/_cfg/agents/research-consolidator.yaml` | Research Consolidator (Alex) |
| `.paper/_cfg/agents/paper-architect.yaml` | Paper Architect (Morgan) |
| `.paper/_cfg/agents/section-drafter.yaml` | Section Drafter (Jordan) |
| `.paper/_cfg/agents/quality-refiner.yaml` | Quality Refiner (Riley) |
| `.paper/_cfg/agents/reference-manager.yaml` | Reference Manager (Harper) |
| `.paper/_cfg/agents/latex-assembler.yaml` | LaTeX Assembler (Taylor) |
| `.paper/_cfg/agents/brainstorm.yaml` | Brainstorm Coach (Carson) |
| `.paper/_cfg/agents/problem-solver.yaml` | Problem Solver (Quinn) |
| `.paper/_cfg/agents/tutor.yaml` | Review Tutor (Sage) |
| `.paper/_cfg/agents/librarian.yaml` | Research Librarian (Ellis) |

### Manifests and Documentation

| File | Purpose |
|------|---------|
| `.paper/_cfg/agent-manifest.yaml` | Master agent index |
| `.paper/_cfg/AGENT-MANIFEST-CSV-DEPRECATED.md` | Deprecation notice |
| `.paper/_cfg/agents/README.md` | Agent directory documentation |
| `.paper/_cfg/schemas/README.md` | Schema documentation |

### Deprecated

| File | Status |
|------|--------|
| `.paper/_cfg/agent-manifest.csv.deprecated` | Kept for backward compatibility |

## Using the New Format

### Validation

```bash
# Validate all agents
python3 open-agents/tools/validate-agent-schema.py

# Validate specific agent
python3 open-agents/tools/validate-agent-schema.py --agent research-consolidator

# Verbose output
python3 open-agents/tools/validate-agent-schema.py --verbose

# CI mode (exits with error on failure)
python3 open-agents/tools/validate-agent-schema.py --ci
```

### Loading Agents in Code

**Python:**
```python
import yaml
from pathlib import Path

# Load single agent
def load_agent(agent_name: str) -> dict:
    path = Path(f'.paper/_cfg/agents/{agent_name}.yaml')
    with open(path) as f:
        return yaml.safe_load(f)

agent = load_agent('research-consolidator')
print(agent['displayName'])  # "Alex"
print(agent['identity']['role'])  # "Research Synthesizer"
```

**JavaScript:**
```javascript
const fs = require('fs');
const yaml = require('js-yaml');

function loadAgent(agentName) {
  const path = `.paper/_cfg/agents/${agentName}.yaml`;
  const content = fs.readFileSync(path, 'utf8');
  return yaml.load(content);
}

const agent = loadAgent('research-consolidator');
console.log(agent.displayName);  // "Alex"
console.log(agent.identity.role);  // "Research Synthesizer"
```

### Creating New Agents

1. **Create YAML file**: `.paper/_cfg/agents/my-agent.yaml`

```yaml
name: my-agent
displayName: PersonaName
title: Agent Title
icon: 🎯
version: 1.0.0
module: core  # or specialist

identity:
  role: Primary Role
  description: >
    Full description of what this agent does.
  communicationStyle: How the agent communicates.

capabilities:
  - Capability 1
  - Capability 2

constraints:
  - Constraint 1
  - Constraint 2

principles:
  - Principle 1
  - Principle 2

owner: team-name
path: .paper/core/agents/my-agent.md
```

2. **Validate**:
```bash
python3 open-agents/tools/validate-agent-schema.py --agent my-agent
```

3. **Add to manifest**: Edit `.paper/_cfg/agent-manifest.yaml`

```yaml
agents:
  - name: my-agent
    module: core
    path: .paper/_cfg/agents/my-agent.yaml
    displayName: PersonaName
    title: Agent Title
    icon: 🎯
    status: active
```

4. **Create agent file**: `.paper/core/agents/my-agent.md`

## CI Integration

The GitHub Actions workflow automatically validates:

- ✅ All agent YAML files against JSON Schema
- ✅ Agent manifest consistency
- ✅ Referenced files exist

**Triggers on:**
- Push to agent files
- Pull requests affecting agent metadata
- Changes to schema or validation tool

**Validation runs:**
- On every commit affecting agent metadata
- Blocks merge if validation fails

## Migration Checklist

- [x] JSON Schema created and documented
- [x] All 10 agents converted to YAML
- [x] Validation tool implemented
- [x] CI workflow configured
- [x] Documentation created
- [x] CSV deprecated (kept for backward compatibility)
- [x] All agents validated successfully

## Success Metrics

| Metric | Before | After |
|--------|--------|-------|
| Field truncation | Yes (ellipses visible) | No (full text) |
| Schema validation | None | JSON Schema + CI |
| Extensibility | Limited (flat CSV) | High (nested YAML) |
| Version control | Poor (CSV diffs) | Good (YAML diffs) |
| Machine parseable | Partial | Full |
| Input/output schemas | None | Defined for all agents |

## Next Steps

### For Developers

1. **Use YAML format** for all new agents
2. **Validate before committing**:
   ```bash
   python3 open-agents/tools/validate-agent-schema.py --ci
   ```
3. **Add full metadata** including capabilities, constraints, and schemas
4. **Update manifest** when adding new agents

### For Tool Developers

1. **Migrate to YAML readers** - Update tools to read from `.paper/_cfg/agents/*.yaml`
2. **Use manifest** - Read `.paper/_cfg/agent-manifest.yaml` for agent discovery
3. **Leverage schemas** - Use input/output schemas for type checking and validation

### Future Enhancements

- [ ] Add workflow contract validation (spec 002)
- [ ] Add agent versioning and governance (spec 010)
- [ ] Extend schema for additional fields as needed
- [ ] Create agent definition templates
- [ ] Build agent metadata API/SDK

## References

- **Specification**: `DEVELOPER-IMPROVEMENTS/001-agent-metadata.md`
- **Implementation Plan**: `DEVELOPER-IMPROVEMENTS/001-agent-metadata-plan.md`
- **Schema**: `.paper/_cfg/schemas/agent-schema.json`
- **Validation Tool**: `open-agents/tools/validate-agent-schema.py`
- **JSON Schema Docs**: https://json-schema.org/

## Questions?

See documentation in:
- `.paper/_cfg/agents/README.md` - Agent definitions guide
- `.paper/_cfg/schemas/README.md` - Schema reference
- `.paper/_cfg/AGENT-MANIFEST-CSV-DEPRECATED.md` - CSV deprecation details
