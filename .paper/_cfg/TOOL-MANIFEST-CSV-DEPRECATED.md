# Tool Manifest CSV Format Deprecated

**Date:** 2024-12-14  
**Status:** Deprecated  
**Migration Complete:** Yes

## Notice

The CSV format for tool metadata (`tool-manifest.csv`) has been **deprecated** in favor of structured YAML format with JSON Schema validation.

## Why This Change?

The CSV format had several limitations:
- ❌ Limited structure (flat rows)
- ❌ No validation
- ❌ Hard to extend with new fields
- ❌ Poor version control diffs
- ❌ No input/output schemas

## New Format: YAML

Tool definitions are now stored as individual YAML files with full metadata, validation, and extensibility.

### Location

- **Individual Definitions**: `.paper/_cfg/tools/*.yaml`
- **Master Index**: `.paper/_cfg/tool-manifest.yaml`
- **Schema**: `.paper/_cfg/schemas/tool-schema.json`

### Example

```yaml
name: build-latex
displayName: Build LaTeX
description: Compile LaTeX document to PDF
version: 1.0.0
path: tools/build-latex.sh
requiresConsent: true

capabilities:
  - Compile LaTeX source files to PDF format
  - Resolve references and citations

dependencies:
  - pdflatex or xelatex
  - bibtex or biber

inputSchema:
  type: object
  properties:
    file:
      type: string
      description: Path to main LaTeX file

outputSchema:
  type: object
  properties:
    pdfPath:
      type: string
    success:
      type: boolean
```

## Migration Guide

### For Developers

1. **Read YAML instead of CSV**
   ```python
   import yaml
   
   # Old: Reading CSV
   # import csv
   # with open('.paper/_cfg/tool-manifest.csv') as f:
   #     reader = csv.DictReader(f)
   
   # New: Reading YAML
   with open('.paper/_cfg/tool-manifest.yaml') as f:
       manifest = yaml.safe_load(f)
       tools = manifest['tools']
   ```

2. **Use individual tool files for detailed metadata**
   ```python
   def load_tool(tool_name: str) -> dict:
       path = f'.paper/_cfg/tools/{tool_name}.yaml'
       with open(path) as f:
           return yaml.safe_load(f)
   
   tool = load_tool('build-latex')
   print(tool['capabilities'])
   ```

### For Tool Authors

1. Create new tool definition: `.paper/_cfg/tools/my-tool.yaml`
2. Follow the JSON Schema: `.paper/_cfg/schemas/tool-schema.json`
3. Add to manifest: `.paper/_cfg/tool-manifest.yaml`
4. Validate: `python3 open-agents/tools/validate-tool-schema.py`

## Validation

```bash
# Validate all tools
python3 open-agents/tools/validate-tool-schema.py

# Validate specific tool
python3 open-agents/tools/validate-tool-schema.py --tool build-latex
```

## Benefits of New Format

- ✅ Full metadata (no truncation)
- ✅ Hierarchical structure
- ✅ JSON Schema validation
- ✅ Better version control diffs
- ✅ Easy to extend
- ✅ Input/output schemas for tooling
- ✅ Capabilities and constraints explicitly defined

## Backward Compatibility

The old CSV file has been renamed to `tool-manifest.csv.deprecated` and is kept for reference only. All new development should use the YAML format.

## Questions?

See documentation:
- `.paper/_cfg/tools/README.md` - Tool definitions guide
- `.paper/_cfg/schemas/README.md` - Schema reference
- `DEVELOPER-IMPROVEMENTS/001-agent-metadata-migration-guide.md` - Migration patterns

## Related Changes

This deprecation follows the same pattern as:
- Agent metadata migration (completed 2024-12-14)
- Workflow metadata migration (completed 2024-12-14)

All manifest files in PaperKit now use YAML format with JSON Schema validation.
