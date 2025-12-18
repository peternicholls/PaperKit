# PaperKit Validation Resources

This folder contains documentation about validation processes used by PaperKit agents.

> **Note:** The citation validation rules have been moved to `.paper/_cfg/tools/citation-rules.yaml` 
> for consistency with the tools manifest structure.

## Validation Overview

PaperKit uses validation at multiple stages:

1. **Citation Validation** - Reference-manager agent validates citations
2. **Structure Validation** - LaTeX-assembler validates paper structure
3. **LaTeX Linting** - Syntax checking before compilation

## Severity Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| **Error** | Critical issue preventing valid output | Must fix before proceeding |
| **Warning** | Issue that should be addressed | Strongly recommended to fix |
| **Info** | Suggestion for improvement | Optional enhancement |

## Related Files

- [.paper/_cfg/tools/citation-rules.yaml](../tools/citation-rules.yaml) - Citation validation rules
- [.paper/_cfg/guides/harvard-citation-guide.md](../guides/harvard-citation-guide.md) - Style guide
- [.paper/_cfg/agents/reference-manager.yaml](../agents/reference-manager.yaml) - Agent definition
- [.paper/_cfg/workflows/validate-citations.yaml](../workflows/validate-citations.yaml) - Validation workflow

---

**Version:** 2.0.0  
**Last Updated:** December 2025
