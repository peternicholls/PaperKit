# Chapter Lock System - Quick Reference Index

This directory contains the infrastructure for locking chapters and maintaining stylistic consistency across the paper.

---

## 🔒 Currently Locked Chapters

| Chapter | Title | Tag | Snapshot | Locked Date |
|---------|-------|-----|----------|-------------|
| **Chapter 2** | Perceptual Foundations | `paper-v0.2-ch2-signedoff` | [PDF](../open-agents/output-final/snapshots/paper-v0.2-ch2-signedoff_20241230.pdf) | 30 Dec 2025 |

---

## 📚 Core Documentation

### For Understanding the Lock System
- **[CHAPTER2-LOCK-COMPLETE.md](CHAPTER2-LOCK-COMPLETE.md)** — Complete summary of what was done
- **[CHAPTER2-LOCK-SUMMARY.md](CHAPTER2-LOCK-SUMMARY.md)** — Quick reference for Chapter 2 status

### For Writing New Chapters
- **[CHAPTER2-STYLE-TEMPLATE.md](CHAPTER2-STYLE-TEMPLATE.md)** — Comprehensive checklist and structural guide
  - Header block format
  - Section hierarchy patterns
  - Citation disciplinee integration strategy
  - Pre-sign-off checklist

### For Maintaining Locked Chapters
- **[MECHANICAL-FIXES-PROTOCOL.md](MECHANICAL-FIXES-PROTOCOL.md)** — What's permitted vs. prohibited
  - Typo fixes ✅
  - Build issues ✅
  - Reference formatting ✅
  - Conceptual changes ❌

---

## 🚀 Quick Start Workflows

### I'm drafting a new chapter
1. Read: [CHAPTER2-STYLE-TEMPLATE.md](CHAPTER2-STYLE-TEMPLATE.md)
2. Follow: Header block format, citation patterns, figure integration
3. Before finalizing: Run the pre-sign-off checklist
4. When ready: Execute the lock protocol (see template)

### I- **[CHAPTER2-LOCK-SUMMARY.md](CHAPTER2-LOCK-SUMMARY.md)** — Quick ES-PROTOCOL.md)
2. Verify it's truly mechanical (typo, build error, ref format)
3. Make the fix
4. Test: `./paperkit latex build`
5. Commit: `git commit -m "fix(ch2): correct typo in section 2.X"`

### I need to make conceptual changes to Chapter 2
1. Read: [CHAPTER2-LOCK-SUMMARY.md](CHAPTER2-LOCK-SUMMARY.md) unlock protocol
2. Document: Why the change is needed
3. Get approval: From Paper Architect or Review Tutor
4. If approved: Create new minor version tag (e.g., `paper-v0.2.1-ch2-revised`)
5. Make changes with full documentation

### I want to restore Chapter 2 to its locked state
```bash
git checkout paper-v0.2-ch2-signedoff
./paperkit latex build
# Verify against snapshot if needed
git che2. Follow: Header block format, citation patterns, figure integr Statistics

**File:** `latex/sections/02_perceptual_foundations.tex`  
**Word Count:** ~3,200 words  
**Citations:** 23 unique sources  
**Quality Metrics:**
- ✅ All quotes have page numbers
- ✅ All sections have transitions
- ✅ Builds without errors
- ✅ No orphaned subsections
- ✅ Maximum 3 heading levels

---

## 🔄 The Lock Protocol (Step by Step)

When a chapter is ready to be locked:

### 1. Final Review
- Run pre-sign-off checklist from style template
- Verify all citations have page numbers
- Check all cross-references resolve
- Test LaTeX build

### 2. Create Git Tag
```bash
# Commit final state
git add latex/sections/XX_chapter.tex
git commit -m "Chapter X sign-off: [title] locked for conceptual edits"

# Create annotated tag
git tag -a paper-vX.X-chX-signedoff -m "Chapter X ([Title]) signed off - locked for conceptual edits. Only mechanical fixes permitted."
```

### 3. Snapshot PDF
```bash
cp latex/main.pdf "open-ag
**File:** `latex/sections/02_perceptual_foundations.tex`  f"
```

### 4. Update Documentation
```bash
# Add entry to this file's "Currently Locked Chapters" table
# Commit the snapshot
git add open-agents/output-final/snapshots/
git commit -m "Snapshot Chapter X signed-off state"
```

---

## 🎯 Why This System?

### Reproducibility
- Git tags preserve exact source state
- PDF snapshots preserve compiled output
- Together = complete reproducibility

### Convergence
- Style template ensures consistency
- Later chapters follow Chapter 2's patterns
- Paper reads as unified whole, not patchwork

### Discipline
- Lock policy prevents drift
- Mechanical fixes clearly defined
- Conceptual changes require explicit approval

### Confidence
- Signed-off chapters don't regress
- Can iterate on later chapters without fear
- Cl```

### 3. Snapshot PDF
```bash
cp latex/main.pdle Locations

### Documentation (this directory)
```
dev-docs/
├── 00README-CHAPTER-LOCKS.md          ← You are here
├── CHAPTER2-LOCK-COMPLETE.md          ← What was accomplished
├── CHAPTER2-LOCK-SUMMARY.md           ← Quick reference
├── CHAPTER2-STYLE-TEMPLATE.md         ← Template for new chapters
└── MECHANICAL-FIXES-PROTOCOL.md       ← Maintenance guidelines
```

### LaTeX Source
```
latex/sections/
├── 02_perceptual_foundations.tex      ← LOCKED ✅
├── 03_journey_metaphor.tex            ← Next target
├── 04_constraint_system.tex
└── ...
```

### Snapshots
```
open-agents/output-final/snapshots/
├── README.md
?### Discipline
- Lock policy pn Excellence
**Do this:**
```latex
\citep[p.~113]{sekulovski2007}
```

**Not this:**
```latex
\citep{sekulovski2007}  % Missing page number!
```

### Transition Quality
**Do this:**
> "Having established X and Y, we now face question Z..."

**Not this:**
> (Abrupt section break with no bridge)

### Figure Integration
**Do this:**
1. Explain concept in text
2. Reference figure: "...as Figure X shows..."
3. Place figure after paragraph
4. Caption interprets, doesn't just describe

**Not this:**
- Figure appears without prior reference
- Caption just says "Results are shown"

### Caveats
**Do this:**
> "Important caveat: This is a design heuristic, not a derived theorem."

**Not this:**
> (Claim presented as fact when it's actually a h├── 03_journ 🔍 Audit Commands

### List all locked chapters
```bash
git tag -l "paper-*-ch*-signedoff"
```

### Show mechanical fixes since lock
```bash
git log --oneline --grep="fix(ch2)" paper-v0.2-ch2-signedoff..HEAD
```

### Compare current state to locked state
```bash
git diff paper-v0.2-ch2-signedoff..HEAD -- latex/sections/02_perceptual_foundations.tex
```

### Verify snapshot integrity
```bash
ls -lh open-agents/output-final/snapshots/
```

---

## 📅 Timeline

| Date | Event | Artifact |
|------|-------|----------|
| 30 Dec 2025 | Chapter 2 locked | Tag: `paper-v0.2-ch2-signedoff` |
| 30 Dec 2025 | PDF snapshot | `paper-v0.2-ch2-signedoff_20241230.pdf` |
| 30 Dec 2025 | Lock system document
**Not this:**
- Figure appears without pries

- [ ] Chapter 3 draft (follow style template)
- [ ] Chapter 3 review
- [ ] Chapter 3 refinement
- [ ] Chapter 3 sign-off (execute lock protocol)
- [ ] Repeat for remaining chapters

**Goal:** All chapters locked by end of draft phase, ensuring stylistic unity.

---

**Last Updated:** 30 Dec 2025  
**Maintained by:** Paper Architect agent  
**Status:** System operational, Chapter 2 locked ✅
