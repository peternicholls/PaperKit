# ⚠️ DEPRECATED LOCATION

**Tools have moved to `.paperkit/tools/`**

The canonical tool implementations are now at:
```
.paperkit/tools/
├── build-latex.sh
├── check-dependencies.sh
├── extract-evidence.sh
├── format-references.py
├── lint-latex.sh
├── validate-structure.py
└── requirements.txt
```

Tool metadata/definitions are at:
```
.paperkit/_cfg/tools/
├── build-latex.yaml
├── extract-evidence.yaml
├── format-references.yaml
├── lint-latex.yaml
└── validate-structure.yaml
```

## Migration

Update any scripts or documentation that reference tools:

| Old Path | New Path |
|----------|----------|
| `open-agents/tools/build-latex.sh` | `.paperkit/tools/build-latex.sh` |
| `open-agents/tools/lint-latex.sh` | `.paperkit/tools/lint-latex.sh` |
| `open-agents/tools/extract-evidence.sh` | `.paperkit/tools/extract-evidence.sh` |
| `open-agents/tools/format-references.py` | `.paperkit/tools/format-references.py` |
| `open-agents/tools/validate-structure.py` | `.paperkit/tools/validate-structure.py` |
| `open-agents/tools/check-dependencies.sh` | `.paperkit/tools/check-dependencies.sh` |

## Why?

`.paperkit/` is now the **single source of truth** for:
- Agent definitions (`.paperkit/core/agents/`, `.paperkit/specialist/agents/`)
- Workflow definitions (`.paperkit/_cfg/workflows/`)
- Tool definitions and implementations (`.paperkit/_cfg/tools/`, `.paperkit/tools/`)
- Configuration and schemas (`.paperkit/_cfg/`)

This consolidation simplifies maintenance and ensures consistency.

---

*Files in this directory are kept temporarily for backward compatibility but will be removed in a future version.*
