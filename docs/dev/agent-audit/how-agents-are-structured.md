# How Agents Are Structured

This document explains the PaperKit agent system structure and how the dual-file approach works.

## Overview

PaperKit uses a dual-file approach for agent definitions:

1. **YAML Metadata Files** (`.paperkit/_cfg/agents/*.yaml`) - Machine-readable metadata index
2. **Markdown Agent Files** (`.paperkit/{core,specialist}/agents/*.md`) - Full agent definitions with operational instructions

## Directory Structure

```
.paperkit/
├── _cfg/
│   ├── agents/                    # YAML metadata files
│   │   ├── orchestrator.yaml
│   │   ├── paper-architect.yaml
│   │   └── ...
│   ├── schemas/
│   │   └── agent-schema.json      # JSON Schema for validation
│   └── agent-manifest.yaml        # Index of all agents
├── core/
│   └── agents/                    # Core agent definitions (MD)
│       ├── orchestrator.md
│       ├── paper-architect.md
│       └── ...
└── specialist/
    └── agents/                    # Specialist agent definitions (MD)
        ├── brainstorm.md
        ├── tutor.md
        └── ...
```

## YAML Metadata Files

Location: `.paperkit/_cfg/agents/`

These files contain structured metadata about each agent, including:

- `name` - Machine identifier (kebab-case)
- `displayName` - Human persona name
- `title` - Functional title
- `icon` - Emoji representation
- `module` - Either "core" or "specialist"
- `identity` - Role, description, and communication style
- `capabilities` - What the agent can do
- `constraints` - Limitations and boundaries
- `principles` - Guiding behaviors
- `inputSchema` / `outputSchema` - Expected data formats
- `examplePrompts` - Usage examples
- `path` - Reference to the MD file

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
  - Generate LaTeX scaffolding

constraints:
  - Cannot start writing content (delegates to Section Drafter)
  - Requires clear paper scope before structuring

path: .paperkit/core/agents/paper-architect.md
```

## Markdown Agent Files

Location: `.paperkit/{core,specialist}/agents/`

These files contain the full agent definition with:

1. YAML frontmatter (optional but recommended)
2. Operational instructions, prompts, and persona details
3. Menu systems and workflows

The runtime (`generate.sh`) reads from these files to generate IDE-specific agent files.

### Why Both?

| Feature | YAML Files | MD Files |
|---------|------------|----------|
| Schema validation | ✅ Primary | Optional frontmatter |
| Machine-readable metadata | ✅ Easy to parse | Requires frontmatter extraction |
| Operational instructions | ❌ None | ✅ Full agent prompts |
| IDE generation source | ❌ Metadata only | ✅ Used by generate.sh |
| CI validation | ✅ Primary target | Secondary |

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

2. **Create the MD file**:
   ```
   .paperkit/{core|specialist}/agents/{agent-name}.md
   ```

3. **Create the YAML metadata file**:
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
