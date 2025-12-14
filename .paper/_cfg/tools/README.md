# PaperKit Tools Directory

This directory contains individual tool definition files in YAML format.

## Purpose

Each file defines a tool used in the PaperKit system with complete metadata, capabilities, constraints, and input/output schemas.

## Structure

```
.paper/_cfg/tools/
├── README.md                    ← This file
├── build-latex.yaml            ← LaTeX compilation tool
├── lint-latex.yaml             ← LaTeX syntax checker
├── validate-structure.yaml     ← Paper structure validator
└── format-references.yaml      ← Reference formatter
```

## Tool Definition Format

Each tool YAML file follows this structure:

```yaml
name: tool-name                 # Machine identifier (kebab-case)
displayName: Tool Display Name  # Human-readable name
description: What the tool does # Full description
version: 1.0.0                  # Semantic version
path: tools/tool-name.sh        # Path to executable
requiresConsent: true           # Whether consent is required

capabilities:                   # What the tool can do
  - Capability 1
  - Capability 2

constraints:                    # Limitations and requirements
  - Constraint 1
  - Constraint 2

dependencies:                   # External dependencies
  - dependency1
  - dependency2

inputSchema:                    # JSON Schema for inputs
  type: object
  properties:
    param1:
      type: string

outputSchema:                   # JSON Schema for outputs
  type: object
  properties:
    result:
      type: string

exampleUsage:                   # Example command lines
  - "./tools/tool-name.sh"
  - "./tools/tool-name.sh --option"

owner: team-name                # Responsible team/person
```

## Schema Validation

All tool definitions must conform to the JSON Schema at:
`.paper/_cfg/schemas/tool-schema.json`

### Validate Tools

```bash
# Validate all tools
python3 open-agents/tools/validate-tool-schema.py

# Validate specific tool
python3 open-agents/tools/validate-tool-schema.py --tool build-latex

# Verbose output
python3 open-agents/tools/validate-tool-schema.py --verbose
```

## Creating a New Tool

1. **Create tool YAML file**: `.paper/_cfg/tools/my-tool.yaml`

2. **Follow the schema structure** (see example above)

3. **Validate the tool**:
   ```bash
   python3 open-agents/tools/validate-tool-schema.py --tool my-tool
   ```

4. **Add to manifest**: Edit `.paper/_cfg/tool-manifest.yaml`
   ```yaml
   tools:
     - name: my-tool
       path: .paper/_cfg/tools/my-tool.yaml
       displayName: My Tool
       description: What my tool does
       requiresConsent: true
       status: active
   ```

5. **Create the actual tool**: Implement `tools/my-tool.sh` or `tools/my-tool.py`

## Loading Tools in Code

### Python

```python
import yaml
from pathlib import Path

def load_tool(tool_name: str) -> dict:
    path = Path(f'.paper/_cfg/tools/{tool_name}.yaml')
    with open(path) as f:
        return yaml.safe_load(f)

tool = load_tool('build-latex')
print(tool['displayName'])
print(tool['capabilities'])
print(tool['requiresConsent'])
```

### JavaScript

```javascript
const fs = require('fs');
const yaml = require('js-yaml');

function loadTool(toolName) {
  const path = `.paper/_cfg/tools/${toolName}.yaml`;
  const content = fs.readFileSync(path, 'utf8');
  return yaml.load(content);
}

const tool = loadTool('build-latex');
console.log(tool.displayName);
console.log(tool.capabilities);
```

## Required Fields

Every tool definition **must** include:
- `name` - Machine identifier (kebab-case)
- `displayName` - Human-readable name
- `description` - What the tool does
- `path` - Path to tool executable
- `requiresConsent` - Boolean indicating if consent required

## Optional Fields

- `version` - Semantic version (defaults to 1.0.0)
- `capabilities` - Array of capabilities
- `constraints` - Array of constraints
- `dependencies` - Array of external dependencies
- `inputSchema` - JSON Schema for input validation
- `outputSchema` - JSON Schema for output validation
- `exampleUsage` - Array of example commands
- `owner` - Team or person responsible

## Consent and Security

All tools that execute scripts or modify files **must** have `requiresConsent: true`. This ensures users can review what tools do before execution.

See `DEVELOPER-IMPROVEMENTS/003-consent-sandboxing.md` for the full consent and sandboxing specification.

## Migration from CSV

The old CSV format (`tool-manifest.csv`) has been deprecated. See `.paper/_cfg/TOOL-MANIFEST-CSV-DEPRECATED.md` for migration details.

## References

- **Schema**: `.paper/_cfg/schemas/tool-schema.json`
- **Manifest**: `.paper/_cfg/tool-manifest.yaml`
- **Deprecation Notice**: `.paper/_cfg/TOOL-MANIFEST-CSV-DEPRECATED.md`
- **Consent Spec**: `DEVELOPER-IMPROVEMENTS/003-consent-sandboxing.md`
