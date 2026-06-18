# Mechanical Fixes Protocol for Locked Chapters

When a chapter is locked for conceptual edits, mechanical fixes are still permitted. This guide defines what qualifies as "mechanical" and the commit protocol to follow.

---

## ✅ Permitted Mechanical Fixes

### 1. Typos and Spelling
**What qualifies:**
- Misspelled words
- Incorrect punctuation
- Grammar errors (subject-verb agreement, tense consistency)
- Capitalization mistakes

**Examples:**
```diff
- ...perceptual uniformity (\S\ref{sec:topology-impossibility}) means
+ ...perceptual uniformity (\S\ref{sec:topology-impossibility}) mean

- The engine uses OKLab, a preceptually uniform space
+ The engine uses OKLab, a perceptually uniform space
```

**Commit format:**
```bash
git commit -m "fix(ch2): correct typo in section 2.3"
```

---

### 2. LaTeX Build Issues
**What qualifies:**
- Missing packages
- Broken compilation
- Undefined references (at first build)
- Label conflicts
- Figure path errors

**Examples:**
```diff
- \includegraphics{temporal-weights.pdf}
+ \includegraphics{figures/temporal-weights.pdf}

- \ref{sec:oklab}  % undefined
+ \ref{sec:oklab-implementation}  % correct label
```

**Commit format:**
```bash
git commit -m "fix(ch2): resolve undefined reference in eq. 2.4"
```

---

### 3. Reference Formatting
**What qualifies:**
- Harvard citation style compliance
- Page number additions
- Citation command corrections (`\cite` vs `\citep` vs `\citet`)
- Bibliography entry formatting
- Broken .bib entries

**Examples:**
```diff
- \cite{kong2021}
+ \citep[p.~3]{kong2021}

- as Kong found \citep{kong2021}
+ as \citet{kong2021} found

- (see \citeauthor{hong2024})
+ \citep{hong2024}
```

**Commit format:**
```bash
git commit -m "fix(ch2): add page numbers to Sekulovski citations"
```

---

### 4. Cross-Reference Updates
**What qualifies:**
- Section/equation/figure reference updates when targets are renumbered
- Label updates to match new section names
- Forward references to later chapters

**Examples:**
```diff
- Section~\ref{sec:gamut} discusses...
+ Section~\ref{sec:gamut-correction} discusses...

- as derived in Chapter 5
+ as derived in \S\ref{sec:bezier-construction}
```

**Commit format:**
```bash
git commit -m "fix(ch2): update cross-refs after chapter 3 restructure"
```

---

## ❌ Prohibited Changes (Not Mechanical)

These require unlocking the chapter:

### 1. Conceptual Rewrites
- Changing argument structure
- Reordering sections
- Altering conclusions
- Adding new concepts

### 2. Content Additions
- New subsections
- Additional paragraphs
- New examples
- Extra figures/tables

### 3. Structural Changes
- Section hierarchy modifications
- Merging/splitting sections
- Reorganizing content flow

### 4. Substantive Edits
- Rewriting for clarity (if meaning changes)
- Changing mathematical derivations
- Altering experimental interpretations

**If you need to make these changes:**
1. Document the reason
2. Get explicit approval
3. Create a new tag (e.g., `paper-v0.2.1-ch2-revised`)
4. Update the lock status

---

## 🔄 Mechanical Fix Workflow

### For Small Fixes (1-3 changes)

```bash
# Make the fix
vim latex/sections/02_perceptual_foundations.tex

# Test build
./paperkit latex build

# Commit with descriptive message
git add latex/sections/02_perceptual_foundations.tex
git commit -m "fix(ch2): correct typo in equation 2.3 caption"

# No new tag needed - original tag still valid
```

### For Multiple Fixes (4+ changes)

```bash
# Make all fixes
vim latex/sections/02_perceptual_foundations.tex

# Test build
./paperkit latex build

# Commit with detailed message
git add latex/sections/02_perceptual_foundations.tex
git commit -m "fix(ch2): multiple mechanical fixes

- Corrected 3 typos in section 2.4
- Added page numbers to Hong citations
- Fixed broken cross-reference to fig:metric-ellipses
- Resolved LaTeX warning about overfull hbox"

# No new tag needed
```

### For Fixes That Affect PDF Output Significantly

If mechanical fixes change pagination or figure placement:

```bash
# Make fixes
vim latex/sections/02_perceptual_foundations.tex

# Test build
./paperkit latex build

# Commit
git commit -m "fix(ch2): correct citation formatting (affects pagination)"

# Optional: create maintenance snapshot
cp latex/main.pdf "open-agents/output-final/snapshots/paper-v0.2-ch2-maintenance_$(date +%Y%m%d).pdf"

# Document in snapshot README
echo "- paper-v0.2-ch2-maintenance_YYYYMMDD.pdf - Post-citation-fix state" >> open-agents/output-final/snapshots/README.md
```

---

## 📝 Commit Message Convention

**Format:** `fix(chN): <description>`

**Good examples:**
```
fix(ch2): correct equation numbering in section 2.3
fix(ch2): add missing page numbers to Nölle citations
fix(ch2): resolve LaTeX compilation error in table 2.1
fix(ch2): update cross-reference after chapter 5 merge
```

**Bad examples (too vague):**
```
fix typo
updated ch2
fixed references
```

**For multiple related fixes:**
```
fix(ch2): improve citation formatting

- Add page numbers to all direct quotes
- Convert \cite to \citep for parenthetical citations
- Fix Ottosson year display in section 2.3.4
```

---

## 🧪 Testing Requirements

**Before committing any mechanical fix:**

1. **Build test:**
   ```bash
   ./paperkit latex build
   # Must complete without errors
   ```

2. **Visual check:**
   - Open `latex/main.pdf`
   - Navigate to the fixed section
   - Verify fix appears correctly
   - Check for layout issues

3. **Cross-reference check:**
   If fixing refs, verify they resolve:
   ```bash
   grep "??" latex/main.log  # Should return nothing
   ```

4. **Citation check:**
   If fixing citations:
   ```bash
   grep "Warning" latex/main.blg  # Check for citation warnings
   ```

---

## 📊 Tracking Mechanical Fixes

### In Commit History

All fixes are tracked in Git:

```bash
# List all fixes to Chapter 2 since sign-off
git log --oneline --grep="fix(ch2)" paper-v0.2-ch2-signedoff..HEAD

# Show detailed fix history
git log -p --grep="fix(ch2)" paper-v0.2-ch2-signedoff..HEAD
```

### In Chapter Header Block

**Do NOT update** the version number in the LaTeX header for mechanical fixes:

```latex
% ==============================================================================
% Section 2: Perceptual Foundations
% ==============================================================================
% VERSION: 3 (Refined - 30 Dec 2025)  ← Keep this unchanged
% Research Integration: Hong (2024), Nölle (2012), Braun (2017), Sekulovski (2007)
% Refinement: Implemented tutor feedback - citation page numbers, transitions
% Target Length: 3,000–3,500 words
% Dependencies: None (foundational section)
% ==============================================================================
```

Version bumps are for **conceptual** changes only.

### Audit Trail

```bash
# See all changes to Chapter 2 since lock
git diff paper-v0.2-ch2-signedoff..HEAD -- latex/sections/02_perceptual_foundations.tex

# Count mechanical fixes
git log --oneline --grep="fix(ch2)" paper-v0.2-ch2-signedoff..HEAD | wc -l
```

---

## ⚖️ When in Doubt

**Ask these questions:**

1. **Does this change the argument?** → Conceptual, not mechanical
2. **Does this add new content?** → Conceptual, not mechanical
3. **Does this fix a mistake?** → Probably mechanical
4. **Would a reader notice the change?** → Consider carefully

**Conservative rule:**  
If you're unsure whether it's mechanical, treat it as conceptual and document the need for unlocking.

**Escalation path:**
1. Document the proposed change
2. Note why it's needed
3. Get approval from Paper Architect or Review Tutor
4. If approved, unlock chapter temporarily
5. Make change with full documentation
6. Re-lock with new minor version tag

---

## 📋 Quick Reference

| Fix Type | Example | Allowed? | Version Bump? |
|----------|---------|----------|---------------|
| Typo | "perceptula" → "perceptual" | ✅ Yes | ❌ No |
| Missing page # | `\citep{source}` → `\citep[p.~5]{source}` | ✅ Yes | ❌ No |
| Broken ref | `\ref{sec:old}` → `\ref{sec:new}` | ✅ Yes | ❌ No |
| Build error | Missing package | ✅ Yes | ❌ No |
| New paragraph | Add context | ❌ No | ✅ Yes (if permitted) |
| Rewrite | Clarify argument | ❌ No | ✅ Yes (if permitted) |
| Reorganize | Move subsection | ❌ No | ✅ Yes (if permitted) |

---

**Last updated:** 30 Dec 2025  
**Applies to:** All locked chapters  
**Current locked chapters:** Chapter 2 (paper-v0.2-ch2-signedoff)
