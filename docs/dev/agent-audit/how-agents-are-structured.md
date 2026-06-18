# How Agents Are Structured

This document explains the PaperKit agent system structure and how the dual-file approach works.

## Overview

PaperKit uses a dual-file approach for agent definitions:

1. **YAML Metadata Files** (`.paperkit/_cfg/agents/*.yaml`) - Schema-validated metadata **ONLY**
2. **Markdown Agent Files** (`.paperkit/{core,specialist}/agents/*.md`) - Behavioural instructions and prompts

## Directory Structure

```
.paperkit/
├── _cfg/
│   ├── agents/                    # YAML metadata files (schema-validated)
│   │   ├── orchestrator.yaml
│   │   ├── paper-architect.yaml
│   │   └── ...
│   ├── schemas/
│   │   └── agent-schema.json      # JSON Schema for validation
│   └── agent-manifest.yaml        # Index of all agents
├── core/
│   └── agents/                    # Core agent instructions (MD)
│       ├── orchestrator.md
│       ├── paper-architect.md
│       └── ...
└── specialist/
    └── agents/                    # Specialist agent instructions (MD)
        ├── brainstorm.md
        ├── tutor.md
        └── ...
```

## YAML Metadata Files

Location: `.paperkit/_cfg/agents/`

These files contain **metadata only** — no instructions or prompts. They are validated against `agent-schema.json`.

### Required Fields

- `name` - Machine identifier (kebab-case)
- `displayName` - Human persona name
- `title` - Functional title
- `icon` - Emoji representation
- `module` - Either "core" or "specialist"
- `identity` - Object with `role` and `description`
- `path` - Reference to the MD file (must match pattern)

### Optional Fields

- `version` - Semantic version (e.g., "1.0.0")
- `capabilities` - Array of strings
- `constraints` - Array of strings
- `principles` - Array of strings
- `inputSchema` / `outputSchema` - JSON Schema objects
- `examplePrompts` - Array of example prompt strings
- `owner` - Maintainer name

### Example YAML File

```yaml
name: paper-architect
displayName: Morgan
title: Paper Architect
icon: 🏗️
module: core

identity:
  role: System Architect
  description: >
    Transforms paper scope and goals into comprehensive, hierarchical paper 
    structure with logical skeletons and LaTeX scaffolding.
  communicationStyle: Calm, pragmatic tones.

capabilities:
  - Design comprehensive paper structures
  - Create hierarchical section organization

constraints:
  - Cannot start writing content (delegates to Section Drafter)

path: .paperkit/core/agents/paper-architect.md
```

## Markdown Agent Files

Location: `.paperkit/{core,specialist}/agents/`

These files contain the **behavioural instructions** for the agent:

- Agent persona and role description
- How the agent should respond
- Specific rules and tie-break logic
- Output format requirements
- Menu systems and workflows (if applicable)

**Important**: MD files should NOT duplicate the YAML metadata. They contain only the instructions/prompts that define the agent's behavior.

The runtime (`generate.sh`) reads from these files to generate IDE-specific agent files.

## Why This Split?

| Concern | YAML Files | MD Files |
|---------|------------|----------|
| Schema validation | ✅ Validated by CI | Not validated |
| Structured metadata | ✅ Easy to parse | N/A |
| Agent instructions | ❌ None | ✅ Full prompts |
| IDE generation | Metadata reference | ✅ Used by generate.sh |
| Runtime loading | Metadata lookup | ✅ Behavior source |

## Validation

### Schema Compliance

All YAML files must comply with `.paperkit/_cfg/schemas/agent-schema.json`:

```bash
python .paperkit/tools/validate-agent-schema.py --ci
```

### Unified System Check

Run the comprehensive check to validate:
- Schema compliance
- No duplicate agent names
- Path references exist
- Manifest consistency
- MD file coverage

```bash
python .paperkit/tools/check-agents.py --ci
```

## Adding a New Agent

1. **Determine module**: `core` (paper writing) or `specialist` (support)

2. **Create the MD file** with instructions:
   ```
   .paperkit/{core|specialist}/agents/{agent-name}.md
   ```

3. **Create the YAML metadata file** (schema-compliant):
   ```
   .paperkit/_cfg/agents/{agent-name}.yaml
   ```

4. **Add to manifest**:
   Edit `.paperkit/_cfg/agent-manifest.yaml` to include the new agent

5. **Validate**:
   ```bash
   python .paperkit/tools/check-agents.py --ci
   ```

6. **Generate IDE files** (optional):
   ```bash
   .paperkit/tools/generate.sh
   ```

## Academic Integrity

All agents follow these critical principles:

- Academic integrity is paramount
- Proper attribution and Harvard-style citations required
- Never fabricate citations or sources
- Flag uncertainties for verification

These constraints are embedded in agent definitions and cannot be bypassed.
