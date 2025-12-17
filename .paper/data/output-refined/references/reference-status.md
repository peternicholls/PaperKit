# Reference Status Tracking
**Paper:** Color Journey Engine Specification  
**Last Updated:** 17 December 2025  
**Citation Style:** Harvard (BibTeX)

---

## Summary

| Category | Count | Status |
|----------|-------|--------|
| **Currently Cited** | 18 | ✅ In use |
| **Available (not yet cited)** | 2 | 📦 Ready |
| **Commented (future use)** | 1 | 💤 Reserved |
| **Total Active Entries** | 19 | — |

---

## Currently Cited in Paper

These references have `\cite{}` commands in the LaTeX sections:

| Key | Author(s) | Year | Section(s) Used |
|-----|-----------|------|-----------------|
| `ottosson2020` | Ottosson, B. | 2020 | §1, §2, §12 |
| `csscolor4` | W3C CSS Working Group | 2022 | §1, §2 |
| `cie1976` | CIE | 1976 | §2 |
| `fairchild2013` | Fairchild, M. D. | 2013 | §2, §6 |
| `mahy1994` | Mahy, Van Eycken, Oosterlinck | 1994 | §2, §4 |
| `safdar2017` | Safdar et al. | 2017 | §2 |
| `luo2001` | Luo, Cui, Rigg | 2001 | §2, §4 |
| `farin2002` | Farin, G. | 2002 | §3, §7, §12 |
| `piegl1997` | Piegl, Tiller | 1997 | §3 |
| `hunt2004` | Hunt, R. W. G. | 2004 | §5, §8 |
| `poynton2012` | Poynton, C. | 2012 | §5, §11 |
| `foley1990` | Foley, van Dam, et al. | 1990 | §6 |
| `morovic2008` | Morovič, J. | 2008 | §8 |
| `knuth1997` | Knuth, D. E. | 1997 | §9 |
| `blackman2018` | Blackman & Vigna | 2018/2021 | §9 |
| `bloch2008` | Bloch, J. | 2008 | §10 |
| `gamma1994` | Gamma, Helm, et al. | 1994 | §10 |

---

## Available References (Not Yet Cited)

These entries are in `references.bib` and ready to cite if needed:

### Computational Geometry

| Key | Citation | Potential Use |
|-----|----------|---------------|
| `deboor1978` | de Boor (1978) | Spline theory foundations (if detailed math needed) |

### Matrix Multiplication (Research Interest)

| Key | Citation | Potential Use |
|-----|----------|---------------|
| `moosbauer2025` | Moosbauer & Poole (2025) | Flip graphs (if relevant to color journey) |
| `strassen1969` | Strassen (1969) | Matrix multiplication efficiency |

---

## Commented References (Future Use)

These are commented out in `references.bib` but can be uncommented if needed:

| Key | Citation | Topic |
|-----|----------|-------|
| `berlin1969` | Berlin & Kay (1969) | Color naming/semantics |

---

## Citation Coverage by Section

### §1 Introduction and Scope ✅
- `ottosson2020` — OKLab introduction
- `csscolor4` — Industry adoption

### §2 Perceptual Color Foundations ✅
- `ottosson2020` — OKLab details
- `fairchild2013` — Color appearance models comparison
- `cie1976` — Historical CIELAB context
- `safdar2017` — JzAzBz comparison
- `mahy1994` — Uniform color space evaluation
- `luo2001` — CIEDE2000

### §3 Journey Construction ✅
- `farin2002` — Primary Bézier reference
- `piegl1997` — Arc-length parameterization

### §4 Perceptual Constraints ✅
- `luo2001` — CIEDE2000, JND thresholds
- `mahy1994` — Uniform color space evaluation

### §5 Style Controls ✅
- `hunt2004` — Color reproduction theory
- `poynton2012` — Digital video/display

### §6 Modes of Operation ✅
- `fairchild2013` — Distinguishability in categorical mode
- `foley1990` — Perceptual velocity, animation

### §7 Loop Strategies ✅
- `farin2002` — Closed curve continuity

### §8 Gamut Management ✅
- `morovic2008` — Gamut mapping techniques
- `hunt2004` — Hue preservation

### §9 Variation and Determinism ✅
- `knuth1997` — PRNG foundations
- `blackman2018` — xoshiro256** algorithm

### §10 API Design ✅
- `bloch2008` — API design principles
- `gamma1994` — Design patterns

### §11 Caller Responsibilities ✅
- `poynton2012` — Print vs screen contexts

### §12 Conclusion ✅
- `ottosson2020`, `farin2002` — Summary references

---

## All Sections Now Have Citations

✅ §1 Introduction — 2 citations  
✅ §2 Perceptual Foundations — 6 citations  
✅ §3 Journey Construction — 2 citations  
✅ §4 Perceptual Constraints — 2 citations  
✅ §5 Style Controls — 2 citations  
✅ §6 Modes of Operation — 2 citations  
✅ §7 Loop Strategies — 1 citation  
✅ §8 Gamut Management — 2 citations  
✅ §9 Determinism — 2 citations  
✅ §10 API Design — 2 citations  
✅ §11 Caller Responsibilities — 1 citation  
✅ §12 Conclusion — 2 citations

---

## Harvard Style Quick Reference

**In-text citation:** `\cite{key}` → (Author, Year)  
**Multiple citations:** `\cite{key1,key2}` → (Author1, Year1; Author2, Year2)  
**Textual citation:** `\citet{key}` → Author (Year) [if supported]

---

*Document maintained by Reference Manager Agent (Harper)*
