# Chapter Locking System Guide

This guide explains the formal chapter locking system in PaperKit.

---

## 📚 Overview

The locking system provides reproducible snapshots of signed-off content, preventing conceptual drift while allowing mechanical fixes.

### Key Components

1. **Git Tags** — Immutable markers of locked state
2. **PDF Snapshots** — Compiled output at lock time
3. **Lock Documentation** — Policy and history
4. **Master Index** — Central registry of all locks

---

## 🔧 Tools and Workflows

### Lock Chapter Tool

**Location:** `.paperkit/tools/lock-chapter.sh`

**Purpose:** Execute complete locking protocol automatically

**Usage:**
```bash
# Lock a chapter
./.paperkit/tools/lock-chapter.sh \
  --target ch3 \
  --title "Journey Construction" \
  --type chapter

# Lock front matter
./.paperkit/tools/lock-chapter.sh \
  --target frontmatter \
  --title "Abstract and Metadata" \
  --type frontmatter

# Specify files explicitly
./.paperkit/tools/lock-chapter.sh \
  --target ch2 \
  --title "Perceptual Foundations" \
  --files "latex/sections/02_perceptual_foundations.tex"
```

### What the Tool Does

1. **Pre-flight checks**
   - Verifies git working directory
   - Warns if uncommitted changes exist

2. **Build validation**
   - Runs `./paperkit latex build`
   - Fails if build errors exist

3. **Git operations**
   - Commits current state
   - Creates annotated tag: `paper-v{major}.{minor}-{target}-signedoff`

4. **Snapshot creation**
   - Copies PDF to `open-agents/output-final/snapshots/`
   - Names with tag and datestamp

5. **Documentation**
   - Creates `{TARGET}-LOCK-SUMMARY.md`
   - Prompts to update master index

---

## 🎯 Lock Workflow

The `lock-chapter` workflow defines the canonical process:

**Location:** `.paperkit/_cfg/workflows/lock-chapter.yaml`

**Steps:**
1. Pre-lock validation
2. Create git commit
3. Create annotated tag
4. Create snapshot
5. Update documentation

**Agents:** Paper Architect, Quality Refiner

---

## 📋 Lock Policy

### ✅ Permitted (No Unlock Required)

- Typo corrections
- LaTeX formatting fixes (spacing, line breaks)
- Build error resolution
- Reference formatting (citation style)
- Cross-reference updates (if targets moved)

### ❌ Prohibited (Unlock Required)

- Conceptual changes to content
- Adding or removing sections
- Changing structure or argument flow
- Substantive rewording
- Adding/removing citations that change meaning

---

## 🔓 Unlock Protocol

If conceptual changes are needed to locked content:

1. **Document rationale**
   - Create issue or planning doc explaining why
   - Get approval from Paper Architect agent

2. **Create revision tag**
   - Format: `paper-v{major}.{minor}.{patch}-{target}-revised`
   - Example: `paper-v0.2.1-ch2-revised`

3. **Make changes**
   - Edit locked files
   - Document all changes in commit messages

4. **Re-lock**
   - Run lock tool again with incremented version
   - Creates new snapshot and documentation

---

## 📊 Verification and Auditing

### List all locks
```bash
git tag -l "paper-*-signedoff"
```

### Show lock details
```bash
git show paper-v0.2-ch2-signedoff
```

### Compare current to locked state
```bash
git diff paper-v0.2-ch2-signedoff..HEAD -- latex/sections/02_perceptual_foundations.tex
```

### Restore to locked state
```bash
git checkout paper-v0.2-ch2-signedoff -- latex/sections/02_perceptual_foundations.tex
```

### View all snapshots
```bash
ls -lh open-agents/output-final/snapshots/
```

---

## 🤖 Agent Integration

### Paper Architect

The Paper Architect agent understands the locking system and can:

- Execute lock protocol via workflow
- Determine when content is ready to lock
- Validate pre-lock conditions
- Guide unlock decisions

**Trigger phrases:**
- "Lock chapter 3"
- "Sign off front matter"
- "Create snapshot for chapter 2"

### Quality Refiner

The Quality Refiner participates in pre-lock validation:

- Checks citation completeness
- Verifies transition quality
- Validates heading hierarchy
- Confirms build success

---

## 📁 File Locations

### Configuration
```
.paperkit/_cfg/
├── workflows/lock-chapter.yaml      ← Workflow definition
└── tools/lock-chapter.yaml          ← Tool definition
```

### Implementation
```
.paperkit/tools/
└── lock-chapter.sh                  ← Executable script
```

### Documentation
```
dev-docs/
├── 00README-CHAPTER-LOCKS.md        ← Master index
├── FRONTMATTER-LOCK-SUMMARY.md      ← Per-lock summaries
├── CHAPTER2-LOCK-SUMMARY.md
└── .paperkit/_cfg/guides/
    └── locking-system.md            ← This file
```

### Snapshots
```
open-agents/output-final/snapshots/
├── paper-v0.2-ch2-signedoff_20241230.pdf
├── paper-v0.3-frontmatter-signedoff_20251231.pdf
└── README.md
```

---

## 🚀 Quick Reference

| Task | Command |
|------|---------|
| Lock a chapter | `./.paperkit/tools/lock-chapter.sh --target ch3 --title "Title"` |
| List locks | `git tag -l "paper-*-signedoff"` |
| Compare to lock | `git diff TAG..HEAD -- file.tex` |
| Restore lock state | `git checkout TAG -- file.tex` |
| View snapshots | `ls -lh open-agents/output-final/snapshots/` |

---

## 🎓 Best Practices

### When to Lock

- Chapter content is complete and reviewed
- All citations have page numbers
- Build succeeds without errors
- Transitions between sections are smooth
- No orphaned subsections exist

### When NOT to Lock

- Content is still in draft
- Awaiting review feedback
- Build has warnings or errors
- Citations incomplete
- Structure still evolving

### Mechanical Fixes

Mechanical fixes don't require unlock:

```bash
# Fix typo in locked chapter
vim latex/sections/02_perceptual_foundations.tex
# ... fix typo ...
git add latex/sections/02_perceptual_foundations.tex
git commit -m "fix(ch2): correct typo in section 2.3"
./paperkit latex build  # verify still builds
```

### Conceptual Changes

Conceptual changes require unlock and re-lock:

```bash
# 1. Document and get approval
# 2. Make changes
vim latex/sections/02_perceptual_foundations.tex
git add latex/sections/02_perceptual_foundations.tex
git commit -m "revise(ch2): expand discussion of temporal perception"

# 3. Re-lock with revision tag
./.paperkit/tools/lock-chapter.sh \
  --target ch2 \
  --title "Perceptual Foundations" \
  --major 0 \
  --minor 2 \
  --patch 1
```

---

**Last Updated:** 31 Dec 2025  
**Maintained by:** Paper Architect agent
