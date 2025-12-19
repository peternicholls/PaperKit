# PaperKit Validation Resources

This folder contains documentation about validation processes used by PaperKit agents.

> **Note:** The citation validation rules now live at `.paperkit/_cfg/resources/citation-rules.yaml`.

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

- [.paperkit/_cfg/resources/citation-rules.yaml](../resources/citation-rules.yaml) - Citation validation rules
- [.paperkit/_cfg/guides/harvard-citation-guide.md](../guides/harvard-citation-guide.md) - Style guide
- [.paperkit/_cfg/agents/reference-manager.yaml](../agents/reference-manager.yaml) - Agent definition
- [.paperkit/_cfg/workflows/validate-citations.yaml](../workflows/validate-citations.yaml) - Validation workflow

---

**Version:** 2.0.0  
**Last Updated:** December 2025
