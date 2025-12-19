# PaperKit JSON Schemas

This directory contains JSON Schema definitions for validating PaperKit configuration and metadata files.

## Schemas

### agent-schema.json

JSON Schema for validating agent definition files.

**Purpose**: Ensures all agent YAML files have complete, consistent metadata.

**Validates**:
- Required fields (name, displayName, title, icon, identity, module, path)
- Field formats (kebab-case names, semantic versions, valid paths)
- Data types and structure
- Enum constraints (module must be 'core' or 'specialist')

**Usage**:
```bash
python3 open-agents/tools/validate-agent-schema.py
```

**Schema Version**: 1.0.0  
**JSON Schema Draft**: Draft-07  
**Schema ID**: https://paperkit.dev/schemas/agent-schema.json

### tool-schema.json

JSON Schema for validating tool definition files.

**Purpose**: Ensures all tool YAML files have complete, consistent metadata.

**Validates**:
- Required fields (name, displayName, description, path, requiresConsent)
- Field formats (kebab-case names, semantic versions, tool paths)
- Data types and structure
- Tool capabilities, constraints, and dependencies

**Usage**:
```bash
python3 open-agents/tools/validate-tool-schema.py
```

**Schema Version**: 1.0.0  
**JSON Schema Draft**: Draft-07  
**Schema ID**: https://paperkit.dev/schemas/tool-schema.json

### workflow-schema.json

JSON Schema for validating workflow definition files.

**Purpose**: Ensures all workflow YAML files have complete, consistent metadata.

**Validates**:
- Required fields (name, displayName, description, module, path)
- Field formats (kebab-case names, semantic versions, workflow paths)
- Data types and structure
- Enum constraints (module, category)
- Workflow steps and agent relationships

**Usage**:
```bash
python3 open-agents/tools/validate-workflow-schema.py
```

**Schema Version**: 1.0.0  
**JSON Schema Draft**: Draft-07  
**Schema ID**: https://paperkit.dev/schemas/workflow-schema.json

## JSON Schema Reference

### Core Fields

```json
{
  "name": "agent-identifier",          // kebab-case, pattern: ^[a-z][a-z0-9-]*$
  "displayName": "Persona Name",       // Human-friendly name
  "title": "Functional Title",         // Role description
  "icon": "🔬",                        // Emoji icon
  "version": "1.0.0",                  // Optional, pattern: ^\d+\.\d+\.\d+$
  "module": "core",                    // Enum: [core, specialist]
  "identity": {                        // Required object
    "role": "Role Title",              // Required
    "description": "Full description", // Required
    "communicationStyle": "Style"      // Optional
  },
  "path": ".paperkit/module/agents/name.md"  // Required, validated pattern
}
```

### Extended Fields

```json
{
  "capabilities": [                    // Optional array
    "Capability 1",
    "Capability 2"
  ],
  "constraints": [                     // Optional array
    "Constraint 1",
    "Constraint 2"
  ],
  "principles": [                      // Optional array
    "Principle 1",
    "Principle 2"
  ],
  "inputSchema": {                     // Optional JSON Schema object
    "type": "object",
    "properties": { /* ... */ }
  },
  "outputSchema": {                    // Optional JSON Schema object
    "type": "object",
    "properties": { /* ... */ }
  },
  "examplePrompts": [                  // Optional array
    "Example prompt 1",
    "Example prompt 2"
  ],
  "owner": "team-name"                 // Optional string
}
```

## Validation Rules

### Pattern Validations

- `name`: Must match `^[a-z][a-z0-9-]*$` (lowercase, kebab-case)
- `version`: Must match `^\d+\.\d+\.\d+$` (semantic versioning)
- `path`: Must match `^\.paperkit/(core|specialist)/agents/[a-z][a-z0-9-]*\.md$`

### Enum Validations

- `module`: Must be one of `["core", "specialist"]`

### Type Validations

- `identity`: Must be an object with required `role` and `description`
- `capabilities`, `constraints`, `principles`, `examplePrompts`: Must be arrays of strings
- `inputSchema`, `outputSchema`: Must be valid JSON Schema objects

### Custom Validations

The validation tool (`validate-agent-schema.py`) adds custom checks:

1. **Name consistency**: Agent name must match filename
2. **Path existence**: Referenced agent file must exist

## Adding New Schemas

When adding new schemas:

1. Create schema file: `.paper/_cfg/schemas/your-schema.json`
2. Follow JSON Schema Draft-07 specification
3. Add schema reference to `.paper/_cfg/manifest.yaml`
4. Create validation tool if needed
5. Document schema in this README

## Schema Evolution

### Versioning

Schemas follow semantic versioning:
- **Major**: Breaking changes (removed/renamed required fields)
- **Minor**: Backwards-compatible additions (new optional fields)
- **Patch**: Non-functional changes (descriptions, examples)

### Deprecation Process

1. Mark field as deprecated in schema description
2. Add migration guide to documentation
3. Announce deprecation with timeline
4. Remove field in next major version

### Extending Schemas

When adding new fields:
- Make them optional initially
- Provide clear descriptions
- Add examples in documentation
- Update validation tools

## Tooling

### Python

```python
import json
from jsonschema import validate, ValidationError

# Load schema
with open('.paperkit/_cfg/schemas/agent-schema.json') as f:
    schema = json.load(f)

# Validate data
try:
    validate(instance=agent_data, schema=schema)
    print("Valid!")
except ValidationError as e:
    print(f"Invalid: {e.message}")
```

### JavaScript

```javascript
const Ajv = require('ajv');
const fs = require('fs');

// Load schema
const schema = JSON.parse(
  fs.readFileSync('.paperkit/_cfg/schemas/agent-schema.json', 'utf8')
);

// Validate data
const ajv = new Ajv();
const validate = ajv.compile(schema);
const valid = validate(agentData);

if (!valid) {
  console.log('Invalid:', validate.errors);
}
```

## Related Documentation

- **Agent Definitions**: `.paperkit/_cfg/agents/`
- **Tool Definitions**: `.paperkit/_cfg/tools/`
- **Workflow Definitions**: `.paperkit/_cfg/workflows/`
- **Agent Validation Tool**: `open-agents/tools/validate-agent-schema.py`
- **Tool Validation Tool**: `open-agents/tools/validate-tool-schema.py`
- **Workflow Validation Tool**: `open-agents/tools/validate-workflow-schema.py`
- **Agent Specification**: `DEVELOPER-IMPROVEMENTS/001-agent-metadata.md`
- **Workflow Specification**: `DEVELOPER-IMPROVEMENTS/002-workflow-agent-contract.md`
- **Tool Specification**: `DEVELOPER-IMPROVEMENTS/003-consent-sandboxing.md`
- **JSON Schema Docs**: https://json-schema.org/
