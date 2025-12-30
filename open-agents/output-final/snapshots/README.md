# Paper Snapshots

This directory contains timestamped PDF snapshots corresponding to signed-off Git tags.

## Purpose

When a chapter is locked for conceptual edits, we:
1. Create an annotated Git tag (e.g., `paper-v0.2-ch2-signedoff`)
2. Copy the compiled PDF here with matching timestamp
3. Preserve source + output together for reproducibility

## Naming Convention

Format: `paper-v[major].[minor]-ch[N]-signedoff_YYYYMMDD.pdf`

**Examples:**
- `paper-v0.2-ch2-signedoff_20241230.pdf` ← Chapter 2 locked
- `paper-v0.3-ch3-signedoff_20250105.pdf` ← Chapter 3 locked (future)
- `paper-v1.0-complete_20250201.pdf` ← Final submission (future)

## Current Snapshots

| Tag | Date | Chapter | File |
|-----|------|---------|------|
| `paper-v0.2-ch2-signedoff` | 2024-12-30 | Perceptual Foundations | `paper-v0.2-ch2-signedoff_20241230.pdf` |

## Retrieving Historical State

To rebuild the paper at a specific snapshot state:

```bash
# Checkout the tag
git checkout paper-v0.2-ch2-signedoff

# Rebuild
./paperkit latex build

# Verify output matches snapshot
diff latex/main.pdf open-agents/output-final/snapshots/paper-v0.2-ch2-signedoff_20241230.pdf

# Return to current state
git checkout master
```

## Relationship to Version Control

- **Git tags** preserve the exact source code state
- **PDF snapshots** preserve the compiled output at that moment
- **Together** they provide complete reproducibility

This is especially important for LaTeX where:
- Package versions may change
- Citation styles may evolve
- Figure generation may vary

## Storage Notes

- PDFs are binary files, so Git doesn't track diffs efficiently
- Keep snapshots for major milestones only
- Consider `.gitattributes` configuration for LFS if repository grows large

---

**Last updated:** 30 Dec 2025
