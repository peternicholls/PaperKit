# Runtime Paths Analysis

Generated: 2026-01-06
**Updated**: 2026-01-20 (Issues resolved in Phase 1 Agent System Upgrade)

## Status: ✅ RESOLVED

All path issues identified in this audit have been resolved. See [PATHS.md](../PATHS.md) for canonical path reference.

## Runtime Agent Loading

### Primary Loader: `generate.sh`

**Location**: `.paperkit/tools/generate.sh`

**Code Path** (lines 196-235):
```bash
# Core agents
for agent_file in "${PAPERKIT_ROOT}"/.paperkit/core/agents/*.md; do
    [ -f "$agent_file" ] || continue
    if ! generate_copilot_agent "$agent_file"; then
        has_errors=true
    fi
done

# Specialist agents
for agent_file in "${PAPERKIT_ROOT}"/.paperkit/specialist/agents/*.md; do
    [ -f "$agent_file" ] || continue
    if ! generate_copilot_agent "$agent_file"; then
        has_errors=true
    fi
done
```

**Directories Scanned**:
- `.paperkit/core/agents/*.md`
- `.paperkit/specialist/agents/*.md`

**Expected File Format**: Markdown with YAML frontmatter

### Validation Script: `validate-agent-schema.py`

**Location**: `.paperkit/tools/validate-agent-schema.py`

**Default Paths** (lines 117-118, 127-134):
```python
parser.add_argument('--schema', help='Path to JSON Schema file (default: .paper/_cfg/schemas/agent-schema.json)')
parser.add_argument('--agents-dir', help='Path to agents directory (default: .paper/_cfg/agents)')
```

**Note**: The hardcoded defaults use `.paper/` NOT `.paperkit/`. This is overridden via CLI in the workflow.

**Directories Scanned**:
- `.paperkit/_cfg/agents/*.yaml` (when called with `--agents-dir`)

### Second Validator: `validate.py`

**Location**: `.paperkit/tools/validate.py`

**Hardcoded Paths** (lines 160, 175-176, 353):
```python
schema_path = project_root / ".paper/_cfg/schemas/agent-schema.json"
# ...
agent_dirs = [
    project_root / ".paper/core/agents",
    project_root / ".paper/specialist/agents"
]
```

**Issue**: This script uses `.paper/` paths which don't exist. It should use `.paperkit/`.

### CI Workflow: `validate-agent-metadata.yml`

**Location**: `.github/workflows/validate-agent-metadata.yml`

**Monitored Paths** (lines 7-10, 14-17):
```yaml
paths:
  - '.paperkit/_cfg/agents/**'
  - '.paperkit/_cfg/schemas/agent-schema.json'
  - '.paperkit/_cfg/agent-manifest.yaml'
  - '.paperkit/tools/validate-agent-schema.py'
```

**Execution** (lines 44-46):
```yaml
python .paperkit/tools/validate-agent-schema.py --ci \
  --schema .paperkit/_cfg/schemas/agent-schema.json \
  --agents-dir .paperkit/_cfg/agents
```

## Schema Path Pattern

From `agent-schema.json` (line 141):
```json
"path": {
  "pattern": "^\\.paperkit/(core|specialist)/agents/[a-z][a-z0-9-]*\\.md$"
}
```

**This expects**: `.paperkit/core/agents/*.md` or `.paperkit/specialist/agents/*.md`

## Summary

| Component | Reads From | Format |
|-----------|------------|--------|
| generate.sh (runtime) | `.paperkit/{core,specialist}/agents/` | `.md` |
| validate-agent-schema.py (CI) | `.paperkit/_cfg/agents/` | `.yaml` |
| validate.py | `.paper/{core,specialist}/agents/` (BROKEN) | `.md` frontmatter |
| agent-schema.json path regex | `.paperkit/{core,specialist}/agents/` | `.md` |

## Identified Issues

1. **validate.py uses wrong base path**: Uses `.paper/` instead of `.paperkit/`
2. **Two validation systems**: One for YAML, one for MD frontmatter
3. **Schema path regex mismatch**: Schema expects MD paths, but YAML files are validated
4. **YAML files act as metadata index**: They point to MD files but aren't the canonical source
