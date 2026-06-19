# PaperKit Canonical Paths Reference

**Version**: 1.0.0
**Created**: 2026-01-20
**Status**: Active

This document defines the canonical paths for all PaperKit agent system components. All tools, scripts, and documentation should reference these paths.

---

## Quick Reference

| Component | Canonical Path |
|-----------|---------------|
| PaperKit Root | `.paperkit/` |
| Agent Metadata | `.paperkit/_cfg/agents/` |
| Agent Instructions | `.paperkit/{core,specialist}/agents/` |
| Workflows | `.paperkit/_cfg/workflows/` |
| Tools Metadata | `.paperkit/_cfg/tools/` |
| Tool Scripts | `.paperkit/tools/` |
| Schemas | `.paperkit/_cfg/schemas/` |
| Skills (NEW) | `.paperkit/_cfg/skills/` |
| Data Output | `.paperkit/data/` |
| Metrics DB | `.paperkit/data/metrics.db` |
| Checkpoints | `.paperkit/data/checkpoints/` |
| Consent Registry | `.paperkit/_cfg/consent.registry.yaml` |
| Routing Registry | `.paperkit/_cfg/routing.registry.yaml` |

---

## Directory Structure

```text
.paperkit/                              # Root agent system directory
├── _cfg/                               # Configuration and metadata
│   ├── agents/                         # Agent YAML metadata files
│   │   ├── paper-architect.yaml
│   │   ├── section-drafter.yaml
│   │   └── ...
│   ├── workflows/                      # Workflow definitions
│   │   └── *.yaml
│   ├── tools/                          # Tool metadata (YAML)
│   │   └── *.yaml
│   ├── skills/                         # Skill definitions (NEW)
│   │   └── *.yaml
│   ├── schemas/                        # JSON Schema files
│   │   ├── agent-schema.json
│   │   ├── workflow-schema.json
│   │   ├── tool-schema.json
│   │   └── skill-schema.json           # NEW
│   ├── guides/                         # Reference guides
│   │   └── harvard-citation-guide.md
│   ├── routing.registry.yaml           # Intent-to-agent routing
│   ├── consent.registry.yaml           # Tool consent records (NEW)
│   ├── agent-manifest.yaml             # Agent catalog
│   ├── workflow-manifest.yaml          # Workflow catalog
│   └── tool-manifest.yaml              # Tool catalog
│
├── core/                               # Core paper writing module
│   ├── agents/                         # Core agent instructions (MD)
│   │   ├── latex-assembler.md
│   │   ├── orchestrator.md
│   │   ├── paper-architect.md
│   │   ├── quality-refiner.md
│   │   ├── reference-manager.md
│   │   ├── research-consolidator.md
│   │   └── section-drafter.md
│   └── config.yaml
│
├── specialist/                         # Specialist support module
│   ├── agents/                         # Specialist agent instructions (MD)
│   │   ├── brainstorm.md
│   │   ├── librarian.md
│   │   ├── problem-solver.md
│   │   └── tutor.md
│   └── config.yaml
│
├── tools/                              # Executable scripts
│   ├── check-agents.py                 # Agent validation
│   ├── validate.py                     # Schema validation
│   ├── validate-skills.py              # Skill validation (NEW)
│   ├── validate-workflow-schema.py     # Workflow validation
│   ├── validate-tool-schema.py         # Tool validation
│   ├── build-latex.sh                  # LaTeX compilation
│   ├── lint-latex.sh                   # LaTeX linting
│   └── ...
│
├── data/                               # Runtime data
│   ├── metrics.db                      # SQLite metrics (NEW)
│   ├── checkpoints/                    # Workflow state (NEW)
│   ├── output-drafts/                  # Draft outputs
│   ├── output-refined/                 # Refined outputs
│   └── output-final/                   # Final outputs
│
└── docs/                               # Documentation
    ├── github-copilot-instructions.md
    └── codex-instructions.md
```

---

## Path Conventions

### 1. Agent Metadata vs Instructions

**Metadata** (machine-readable, schema-validated):
```
.paperkit/_cfg/agents/{agent-name}.yaml
```

**Instructions** (human-readable prompts, no frontmatter):
```
.paperkit/core/agents/{agent-name}.md      # Core agents
.paperkit/specialist/agents/{agent-name}.md # Specialist agents
```

### 2. Tool Metadata vs Scripts

**Metadata** (YAML definition):
```
.paperkit/_cfg/tools/{tool-name}.yaml
```

**Executable Script** (shell/python):
```
.paperkit/tools/{tool-name}.{sh,py}
```

### 3. Schema Files

All JSON Schema files live in:
```
.paperkit/_cfg/schemas/{entity}-schema.json
```

Available schemas:
- `agent-schema.json` - Agent metadata validation
- `workflow-schema.json` - Workflow definition validation
- `tool-schema.json` - Tool definition validation
- `skill-schema.json` - Skill definition validation (NEW)
- `routing-schema.json` - Routing registry validation
- `metrics-schema.json` - Metrics record validation (NEW)

### 4. Manifests

All manifests live in `_cfg/`:
```
.paperkit/_cfg/agent-manifest.yaml
.paperkit/_cfg/workflow-manifest.yaml
.paperkit/_cfg/tool-manifest.yaml
```

---

## Deprecated Paths

The following paths are **deprecated** and should NOT be used:

| Deprecated Path | Canonical Replacement |
|-----------------|----------------------|
| `.paper/` | `.paperkit/` |
| `.paper/_cfg/` | `.paperkit/_cfg/` |
| `open-agents/` | `.paperkit/` |

If you encounter references to deprecated paths, update them to use canonical paths.

---

## Environment Variables

For scripts that need path flexibility:

| Variable | Default | Purpose |
|----------|---------|---------|
| `PAPERKIT_ROOT` | `.paperkit/` | Override agent system root |
| `PAPERKIT_AGENT_SCHEMA_PATH` | `.paperkit/_cfg/schemas/agent-schema.json` | Override agent schema |
| `PAPERKIT_WORKFLOW_SCHEMA_PATH` | `.paperkit/_cfg/schemas/workflow-schema.json` | Override workflow schema |
| `PAPERKIT_TOOL_SCHEMA_PATH` | `.paperkit/_cfg/schemas/tool-schema.json` | Override tool schema |
| `PAPERKIT_AGENTS_DIR` | `.paperkit/_cfg/agents/` | Override agents directory |
| `PAPERKIT_WORKFLOWS_DIR` | `.paperkit/_cfg/workflows/` | Override workflows directory |
| `PAPERKIT_TOOLS_DIR` | `.paperkit/_cfg/tools/` | Override tools directory |

---

## Path Resolution in Code

### Python

```python
from pathlib import Path

def find_project_root() -> Path:
    """Find the project root by looking for .paperkit/ directory."""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / ".paperkit").is_dir():
            return path
    raise FileNotFoundError("Could not find PaperKit project root")

# Canonical paths
project_root = find_project_root()
agents_dir = project_root / ".paperkit/_cfg/agents"
schemas_dir = project_root / ".paperkit/_cfg/schemas"
tools_dir = project_root / ".paperkit/tools"
```

### Shell

```bash
#!/bin/bash

# Find project root
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.paperkit" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

PROJECT_ROOT=$(find_project_root)
AGENTS_DIR="$PROJECT_ROOT/.paperkit/_cfg/agents"
SCHEMAS_DIR="$PROJECT_ROOT/.paperkit/_cfg/schemas"
TOOLS_DIR="$PROJECT_ROOT/.paperkit/tools"
```

---

## Validation

To verify all paths are correctly configured:

```bash
# Run unified agent checker
python3 .paperkit/tools/check-agents.py --verbose

# Validate specific component
python3 .paperkit/tools/validate.py --agents-only
```

---

## Migration Notes

### From `.paper/` to `.paperkit/`

If you have scripts referencing `.paper/`:

```bash
# Find all references
grep -r "\.paper/" --include="*.py" --include="*.sh"

# Update references (manual review recommended)
sed -i '' 's/\.paper\//\.paperkit\//g' <file>
```

### From MD Frontmatter to YAML Files

Agent metadata should ONLY exist in:
```
.paperkit/_cfg/agents/{agent-name}.yaml
```

NOT in frontmatter within:
```
.paperkit/{core,specialist}/agents/{agent-name}.md
```

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-01-20 | 1.0.0 | Initial canonical paths document |
