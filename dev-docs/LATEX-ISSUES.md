# LaTeX Issues Tracking

This document tracks known LaTeX compilation issues, undefined references, and cross-reference problems that need to be resolved.

**Last Updated:** 30 December 2025

---

## Active Issues

### Undefined Section References

**Status:** 🔴 ACTIVE  
**Priority:** HIGH  
**Discovered:** 30 Dec 2025  
**Impact:** References render as `??` in compiled PDF instead of section numbers

#### Remaining Undefined Labels

The following section labels are referenced but not defined anywhere in the document:

| Referenced Label | Referenced In | Line | Expected Location | Action Needed |
|-----------------|---------------|------|-------------------|---------------|
| `sec:oklch` | Section 5 (style_controls.tex) | ~15 | Section 2 or 3 | Add label or fix reference |
| `sec:oklab` | Section 12 (conclusion.tex) | ~13 | Section 2 | Add `\label{sec:oklab}` near OKLab intro |
| `sec:oklch` | Section 12 (conclusion.tex) | ~14 | Section 2 | Add `\label{sec:oklch}` near OKLCh intro |
| `sec:caller-responsibilities` | Section 10 (api_design.tex) | ~120 | Section 11 | Verify label exists or create it |

#### Detection Method

```bash
cd latex/
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep "Reference.*undefined"
```

#### Notes

- Section 2 references were fixed on 30 Dec 2025 (7 fixes)
- These 4 references remain across sections 5, 10, and 12
- Some may be simple typos (e.g., `sec:oklab-implementation` exists but `sec:oklab` doesn't)
- Some may require creating new labels at appropriate subsections

---

## Recently Resolved

### Section 2 Cross-References (FIXED)

**Resolved:** 30 Dec 2025  
**Issue:** Section 2 had 7 undefined cross-references causing `§??` in output

**Fixes Applied:**

| Original Reference | Fixed To | Section |
|-------------------|----------|---------|
| `sec:warmth-bias` | `sec:temperature` | §5 |
| `sec:palette-modes` | `sec:categorical-mode` | §6 |
| `sec:gamut-management` (×3) | `sec:gamut-correction`, `sec:gamut-problem` | §8 |
| `sec:loop-strategies` | `sec:loop-open--sec:loop-phased` (range) | §7 |
| `sec:mobius-mathematical` | `sec:loop-mobius` | §7 |
| `sec:journey-construction` | `sec:bezier` | §3 |
| `sec:velocity-weights` | `sec:perceptual-velocity` | §6 |

**Additional Fix:** Corrected LaTeX syntax: `\item[Gamut management:}` → `\item[Gamut management:]`

---

## Investigation Checklist

When investigating undefined references:

- [ ] Run `pdflatex` to identify all undefined references
- [ ] Extract unique undefined labels: `grep -o "\\ref{sec:[^}]*}" file.tex | sort -u`
- [ ] Check if labels exist: `grep "\\label{sec:label-name}" latex/sections/*.tex`
- [ ] Determine correct mapping:
  - Search for related content in target sections
  - Check for similar label names (typos)
  - Verify label naming conventions
- [ ] Apply fixes using `multi_replace_string_in_file` for efficiency
- [ ] Verify with `pdflatex` compilation
- [ ] Document in this file

---

## Future Work

### Suggested Improvements

1. **Automated Reference Validation**
   - Create script to validate all `\ref{}` have corresponding `\label{}`
   - Add to CI/CD pipeline
   - Run before each commit

2. **Label Inventory**
   - Generate complete list of all section labels
   - Document in reference file
   - Update when sections are added/renamed

3. **Naming Convention**
   - Standardize label naming: `sec:section-name-kebab-case`
   - Ensure consistency across all sections
   - Add to style guide

4. **Cross-Reference Map**
   - Visual diagram of section dependencies
   - Identify circular references
   - Optimize document flow

---

## Quick Reference

### All Defined Section Labels (as of 30 Dec 2025)

Generated with: `grep -h "\\label{sec:" latex/sections/*.tex | sort`

```
\label{sec:adaptive-sampling}
\label{sec:anchors}
\label{sec:api-diagnostics}
\label{sec:api-input}
\label{sec:api-output}
\label{sec:api-philosophy}
\label{sec:api-scope}
\label{sec:arc-length}
\label{sec:bezier}
\label{sec:caller-duties}
\label{sec:categorical-mode}
\label{sec:constraint-conflicts}
\label{sec:constraint-enforcement}
\label{sec:contributions}
\label{sec:delta-max}
\label{sec:delta-min}
\label{sec:design-principles}
\label{sec:determinism}
\label{sec:error-handling}
\label{sec:future}
\label{sec:gamut-correction}
\label{sec:gamut-design}
\label{sec:gamut-problem}
\label{sec:guarantees}
\label{sec:hue-preservation}
\label{sec:input-validation}
\label{sec:intensity}
\label{sec:jnd}
\label{sec:journey-metaphor}
\label{sec:journey-mode}
\label{sec:loop-closed}
\label{sec:loop-mobius}
\label{sec:loop-open}
\label{sec:loop-output}
\label{sec:loop-phased}
\label{sec:loop-pingpong}
\label{sec:mode-selection}
\label{sec:motivation}
\label{sec:multi-anchor}
\label{sec:oklab-implementation}
\label{sec:param-interactions}
\label{sec:perceptual-foundations}
\label{sec:perceptual-velocity}
\label{sec:riemannian-color}
\label{sec:secondary-params}
\label{sec:single-anchor}
\label{sec:smoothness}
\label{sec:temperature}
\label{sec:temporal-spatial}
\label{sec:topology-impossibility}
```

*Note: Regenerate this list when sections are modified.*
