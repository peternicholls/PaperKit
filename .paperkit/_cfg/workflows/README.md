# PaperKit Workflows Directory

This directory contains individual workflow definition files in YAML format.

## Purpose

Each file defines a workflow used in the PaperKit system with complete metadata, step definitions, agent relationships, and input/output schemas.

## Structure

```
.paper/_cfg/workflows/
├── README.md                   ← This file
├── consolidate.yaml           ← Research consolidation workflow
├── outline.yaml               ← Paper outline creation workflow
├── skeleton.yaml              ← LaTeX skeleton generation workflow
├── write-section.yaml         ← Section drafting workflow
├── refine-section.yaml        ← Section refinement workflow
├── validate-citations.yaml    ← Citation validation workflow
├── build.yaml                 ← Document build workflow
├── generate-ideas.yaml        ← Idea generation workflow
├── analyze-problem.yaml       ← Problem analysis workflow
├── review-draft.yaml          ← Draft review workflow
└── search-sources.yaml        ← Source search workflow
```

## Workflow Definition Format

Each workflow YAML file follows this structure:

```yaml
name: workflow-name              # Machine identifier (kebab-case)
displayName: Workflow Name       # Human-readable name
description: What workflow does  # Full description
module: core                     # Module: core or specialist
category: drafting               # Workflow category
path: .paperkit/core/workflows/drafting/workflow-name.yaml

agents:                          # Agents used in workflow
  - agent-name-1
  - agent-name-2

steps:                           # Workflow steps
  - name: step-1
    agent: agent-name-1
    description: What this step does
  - name: step-2
    agent: agent-name-2
    description: What this step does

inputSchema:                     # JSON Schema for inputs
  type: object
  properties:
    param1:
      type: string

outputSchema:                    # JSON Schema for outputs
  type: object
  properties:
    result:
      type: string

exampleUsage:                    # Example invocations
  - "Run workflow with topic X"
  - "Execute workflow on section Y"

owner: team-name                 # Responsible team/person
```

## Categories

Workflows are organized by category:

**Core Categories:**
- `research` - Research consolidation and synthesis
- `planning` - Paper structuring and outlining
- `drafting` - Section writing
- `refinement` - Quality improvement
- `references` - Citation management
- `assembly` - Document compilation

**Specialist Categories:**
- `brainstorm` - Idea generation
- `problem-solving` - Problem analysis
- `tutor` - Draft review and feedback
- `librarian` - Source discovery

## Schema Validation

All workflow definitions must conform to the JSON Schema at:
`.paper/_cfg/schemas/workflow-schema.json`

### Validate Workflows

```bash
# Validate all workflows
python3 open-agents/tools/validate-workflow-schema.py

# Validate specific workflow
python3 open-agents/tools/validate-workflow-schema.py --workflow write-section

# Verbose output
python3 open-agents/tools/validate-workflow-schema.py --verbose
```

## Creating a New Workflow

1. **Create workflow YAML file**: `.paper/_cfg/workflows/my-workflow.yaml`

2. **Follow the schema structure** (see example above)

3. **Define agents and steps** clearly

4. **Validate the workflow**:
   ```bash
   python3 open-agents/tools/validate-workflow-schema.py --workflow my-workflow
   ```

5. **Add to manifest**: Edit `.paper/_cfg/workflow-manifest.yaml`
   ```yaml
   workflows:
     - name: my-workflow
       module: core
       category: drafting
       path: .paper/_cfg/workflows/my-workflow.yaml
       displayName: My Workflow
       description: What my workflow does
       status: active
   ```

6. **Create workflow definition file**: Create the actual workflow YAML at the path specified

## Loading Workflows in Code

### Python

```python
import yaml
from pathlib import Path

def load_workflow(workflow_name: str) -> dict:
    path = Path(f'.paper/_cfg/workflows/{workflow_name}.yaml')
    with open(path) as f:
        return yaml.safe_load(f)

workflow = load_workflow('write-section')
print(workflow['displayName'])
print(workflow['agents'])
print(workflow['steps'])
```

### JavaScript

```javascript
const fs = require('fs');
const yaml = require('js-yaml');

function loadWorkflow(workflowName) {
  const path = `.paper/_cfg/workflows/${workflowName}.yaml`;
  const content = fs.readFileSync(path, 'utf8');
  return yaml.load(content);
}

const workflow = loadWorkflow('write-section');
console.log(workflow.displayName);
console.log(workflow.agents);
console.log(workflow.steps);
```

## Required Fields

Every workflow definition **must** include:
- `name` - Machine identifier (kebab-case)
- `displayName` - Human-readable name
- `description` - What the workflow does
- `module` - Module (core or specialist)
- `path` - Path to workflow definition file

## Optional Fields

- `version` - Semantic version (defaults to 1.0.0)
- `category` - Workflow category
- `agents` - Array of agent names used
- `steps` - Array of workflow step objects
- `inputSchema` - JSON Schema for input validation
- `outputSchema` - JSON Schema for output validation
- `exampleUsage` - Array of example invocations
- `owner` - Team or person responsible

## Workflow Contracts

Workflows define formal contracts between agents and steps. See `DEVELOPER-IMPROVEMENTS/002-workflow-agent-contract.md` for the complete specification on:

- Input/output contracts
- State passing between steps
- Error handling
- Agent coordination

## Migration from CSV

The old CSV format (`workflow-manifest.csv`) has been deprecated. See `.paper/_cfg/WORKFLOW-MANIFEST-CSV-DEPRECATED.md` for migration details.

## References

- **Schema**: `.paper/_cfg/schemas/workflow-schema.json`
- **Manifest**: `.paper/_cfg/workflow-manifest.yaml`
- **Deprecation Notice**: `.paper/_cfg/WORKFLOW-MANIFEST-CSV-DEPRECATED.md`
- **Workflow Contract Spec**: `DEVELOPER-IMPROVEMENTS/002-workflow-agent-contract.md`
- **Agent Definitions**: `.paper/_cfg/agents/`
