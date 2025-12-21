# PaperKit Agent Definitions

This directory contains structured YAML definitions for all PaperKit agents.

## Overview

Each agent has a dedicated YAML file with complete metadata including:

- **Identity**: Role, description, communication style
- **Capabilities**: What the agent can do
- **Constraints**: What the agent cannot or will not do
- **Principles**: Core guidelines for agent behavior
- **Input/Output Schemas**: Expected data formats
- **Example Prompts**: Sample use cases

## Files

- `research-consolidator.yaml` - Research synthesis agent
- `paper-architect.yaml` - Paper structure design agent
- `section-drafter.yaml` - Section writing agent
- `quality-refiner.yaml` - Draft refinement agent
- `reference-manager.yaml` - Citation management agent
- `latex-assembler.yaml` - Document compilation agent
- `brainstorm.yaml` - Brainstorming facilitation agent
- `problem-solver.yaml` - Problem analysis agent
- `tutor.yaml` - Review and feedback agent
- `librarian.yaml` - Research curation agent

## Schema

All agent definitions conform to JSON Schema: `.paperkit/_cfg/schemas/agent-schema.json`

### Required Fields

```yaml
name: agent-identifier         # kebab-case machine identifier
displayName: PersonaName        # Human-friendly persona name
title: Functional Title         # Role description
icon: 🔬                        # Emoji icon
module: core                    # Module: core or specialist
identity:                       # Identity object
  role: Role Title              # Primary role
  description: |                # Full description
    Multi-line description
path: .paperkit/module/agents/name.md  # Path to agent file
```

### Optional Fields

```yaml
capabilities: []                # List of capabilities
constraints: []                 # List of constraints
principles: []                  # Core principles
communicationStyle: ""          # How agent communicates
inputSchema: {}                 # JSON Schema for input
outputSchema: {}                # JSON Schema for output
examplePrompts: []              # Example use cases
owner: team-name                # Owning team
```

## Validation

Validate agent definitions before committing:

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

## Creating a New Agent

1. Create new YAML file: `.paper/_cfg/agents/your-agent.yaml`
2. Follow the schema structure (see examples above)
3. Add entry to `.paper/_cfg/agent-manifest.yaml`
4. Validate: `python3 open-agents/tools/validate-agent-schema.py --agent your-agent`
5. Create agent definition file: `.paper/{module}/agents/your-agent.md`

## Loading Agents Programmatically

### Python

```python
import yaml
from pathlib import Path

# Load single agent
def load_agent(agent_name: str) -> dict:
    agent_path = Path(f'.paper/_cfg/agents/{agent_name}.yaml')
    with open(agent_path) as f:
        return yaml.safe_load(f)

# Load all agents
def load_all_agents() -> list:
    agents_dir = Path('.paper/_cfg/agents')
    agents = []
    for agent_file in agents_dir.glob('*.yaml'):
        if agent_file.name != 'README.md':
            with open(agent_file) as f:
                agents.append(yaml.safe_load(f))
    return agents
```

### JavaScript

```javascript
const fs = require('fs');
const yaml = require('js-yaml');

// Load single agent
function loadAgent(agentName) {
  const agentPath = `.paper/_cfg/agents/${agentName}.yaml`;
  const content = fs.readFileSync(agentPath, 'utf8');
  return yaml.load(content);
}

// Load all agents
function loadAllAgents() {
  const agentsDir = '.paper/_cfg/agents';
  const files = fs.readdirSync(agentsDir)
    .filter(f => f.endsWith('.yaml'));
  
  return files.map(file => {
    const content = fs.readFileSync(`${agentsDir}/${file}`, 'utf8');
    return yaml.load(content);
  });
}
```

## Migration from CSV

The old CSV format (`agent-manifest.csv`) has been deprecated. See `.paper/_cfg/AGENT-MANIFEST-CSV-DEPRECATED.md` for migration details.

### Key Improvements

- ✅ No field truncation
- ✅ Hierarchical data structure
- ✅ JSON Schema validation
- ✅ Better version control diffs
- ✅ Extensible for new fields
- ✅ Machine and human readable

## Related Documentation

- **Schema**: `.paper/_cfg/schemas/agent-schema.json`
- **Manifest**: `.paper/_cfg/agent-manifest.yaml`
- **Specification**: `DEVELOPER-IMPROVEMENTS/001-agent-metadata.md`
- **Implementation Plan**: `DEVELOPER-IMPROVEMENTS/001-agent-metadata-plan.md`
