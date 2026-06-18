# Comprehensive Citation Audit Report
## LaTeX Section Files Analysis
**Generated:** 2025-12-30
**Scope:** All `.tex` files in `latex/sections/`

---

## Executive Summary

- **Total Citations Found:** 93
- **Citations WITH Page Numbers:** 3 (3.2%)
- **Citations WITHOUT Page Numbers:** 90 (96.8%)
- **Unique Cite Keys:** 38

### Critical Finding
⚠️ **96.8% of citations are missing page numbers**, which is below academic standards for a technical specification paper. Harvard citation style strongly recommends page numbers for all citations, especially for direct quotes and specific claims.

---

## Summary by Citation Type

| Citation Command | Count | With Page Numbers | Without Page Numbers |
|-----------------|-------|-------------------|---------------------|
| `\citep{}` | 73 | 2 | 71 |
| `\cite{}` | 10 | 0 | 10 |
| `\citeyearpar{}` | 6 | 0 | 6 |
| `\citet{}` | 1 | 0 | 1 |
| `\citealt{}` | 1 | 1 | 0 |
| **TOTAL** | **91** | **3** | **88** |

---

## Citations WITH Page Numbers (3 total)

### ✅ Section 02 - Perceptual Foundations

1. **Line 77** - `\citep[p.~11]{judd1940}`
   ```latex
   This is not a limitation of current measurement techniques—it is a
   mathematical constraint arising from the ``super-importance of hue''
   first identified by Judd \citep[p.~11]{judd1940}.
   ```

2. **Line 106** - `\citep[p.~3]{kong2021}`
   ```latex
   Kong \citeyearpar{kong2021} notes explicitly: ``CIELAB is not a useful space
   to predict the perception of dynamic colored light. Today, no color spaces
   are available that accurately predict the visibility of color differences
   over time'' \citep[p.~3]{kong2021}.
   ```

3. **Line 219** - `\citealt{fairchild2013}, Chapter~3`
   ```latex
   the cube root models nonlinear perceptual compression—a principle dating
   to Fechner's seminal psychophysical work (as discussed in
   \citealt{fairchild2013}, Chapter~3) and refined through modern
   understanding of cone response functions \citep{ottosson2020};
   ```

---

## Citations WITHOUT Page Numbers (90 total)

Organized by cite key with all occurrences listed.

### blackman2018
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 09_variation_determinism.tex | 82 | `\citep{blackman2018}` | Implementation uses documented algorithm (e.g., xoshiro256** \citep{blackman2018}) |

---

### bloch2008
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 10_api_design.tex | 15 | `\citep{bloch2008}` | The engine is a \textbf{pure function} that transforms configuration into palette \citep{bloch2008}: |

---

### braun2017
**Occurrences:** 3

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 287 | `\citeyearpar{braun2017}` | Human color perception differs fundamentally between static spatial patterns and dynamic temporal transitions. Braun et al.\ \citeyearpar{braun2017} measured chromatic sensitivity |
| 02_perceptual_foundations.tex | 290 | `\citep{braun2017}` | When tracking a moving object with smooth eye movements, chromatic sensitivity \emph{increases} by approximately 12\% \citep{braun2017}. |
| 02_perceptual_foundations.tex | 294 | `\citep{braun2017}` | During rapid eye movements (saccades), chromatic sensitivity \emph{decreases} by approximately 58\% \citep{braun2017}. |

---

### cie1976
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 99 | `\cite{cie1976}` | CIELAB~\cite{cie1976} was the first widely-used perceptual space but exhibits known uniformity issues |

---

### colorjs2025
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 112 | `\cite{colorjs2025}` | Two-layer gamut management~\cite{morovic2008} preventing and correcting out-of-gamut colors while preserving hue, aligned with CSS Color Level 4 practices~\cite{colorjs2025} |
| 08_gamut_management.tex | 64 | `\citep{colorjs2025}` | Our approach aligns with the CSS Color Level 4 gamut mapping algorithm \citep{csscolor4}, which has been implemented in reference libraries such as Color.js \citep{colorjs2025}. |

---

### cowan2001
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 03_journey_construction.tex | 50 | `\citep{cowan2001}` | Research on working memory suggests humans can reliably track 4±1 items simultaneously \citep{cowan2001}; |

---

### csscolor4
**Occurrences:** 5

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 101 | `\cite{csscolor4}` | OKLab has achieved rapid industry adoption, appearing in CSS Color Level 4~\cite{csscolor4}, Adobe Photoshop |
| 02_perceptual_foundations.tex | 142 | `\citep{csscolor4}` | It has gained rapid adoption in web standards (CSS Color Level 4) \citep{csscolor4}, creative software |
| 02_perceptual_foundations.tex | 217 | `\citep{csscolor4}` | These values are standardized in CSS Color Level 4 \citep{csscolor4} and match the reference implementation. |
| 04_perceptual_constraints.tex | 25 | `\citep{csscolor4}` | the CSS Color Level 4 gamut mapping algorithm uses a similar threshold concept: colors are considered ``close enough'' to clip when $\Delta E < 0.02$ on OKLab's 0--1 scale \citep{csscolor4} |
| 08_gamut_management.tex | 74 | `\citep{csscolor4}` | The CSS standard specifies terminating the search when $\Delta E < 0.02$ (on OKLab's 0--1 scale), indicating the corrected color is perceptually indistinguishable from the gamut boundary \citep{csscolor4}. |

---

### fairchild2013
**Occurrences:** 8 (1 with page, 7 without)

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 219 | `\citealt{fairchild2013}, Chapter~3` | ✅ **HAS PAGE** - (as discussed in \citealt{fairchild2013}, Chapter~3) and refined through modern understanding |
| 04_perceptual_constraints.tex | 15 | `\citep{fairchild2013}` | This concept originates from Weber's and Fechner's foundational psychophysics work and has been extensively studied in color science \citep{fairchild2013}. |
| 04_perceptual_constraints.tex | 23 | `\citep{fairchild2013,luo2001}` | Color science literature consistently shows that laboratory JND values [...] underestimate the threshold needed for reliable discrimination in real applications \citep{fairchild2013,luo2001}. |
| 04_perceptual_constraints.tex | 41 | `\cite{fairchild2013}` | \textit{Note: This table represents design guidance derived from Fairchild~\cite{fairchild2013} and practical experience} |
| 04_perceptual_constraints.tex | 55 | `\citep{fairchild2013}` | the 2.0 threshold provides margin for the variability inherent in real-world color perception \citep{fairchild2013}. |
| 06_modes_of_operation.tex | 47 | `\citep{fairchild2013}` | Categorical Mode optimizes for \textbf{maximum distinguishability} between swatches, suitable for discrete data categories, legends, and accessibility-critical applications \citep{fairchild2013}. |
| 06_modes_of_operation.tex | 92 | `\citep{fairchild2013}` | This observation is consistent with color appearance research showing that hue changes are more salient than equivalent lightness or chroma changes \citep{fairchild2013}. |
| 08_gamut_management.tex | 106 | `\citep{morovic2008,fairchild2013}` | research on gamut mapping algorithms shows that hue shifts are perceptually more objectionable than chroma reductions \citep{morovic2008,fairchild2013}. |
| 12_conclusion.tex | 34 | `\citep{fairchild2013}` | The specific threshold values ($\Delta_{\min} \approx 2.0$, $\Delta_{\max} \approx 5.0$) are design heuristics informed by color science literature \citep{fairchild2013} |

---

### farin2002
**Occurrences:** 5

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 108 | `\cite{farin2002}` | Continuous Bézier paths through OKLab space~\cite{farin2002}, providing flexible curve shapes |
| 03_journey_construction.tex | 50 | `\citep{farin2002}` | Additionally, cubic Bézier curves between consecutive anchors provide $C^1$ continuity guarantees \citep{farin2002} |
| 03_journey_construction.tex | 125 | `\cite{farin2002}` | Each segment is represented as a \textbf{cubic Bézier curve} in OKLab space \cite{farin2002} |
| 07_loop_strategies.tex | 38 | `\citep{farin2002}` | The \textbf{closed} strategy forms a complete cycle, returning smoothly from the last anchor back to the first \citep{farin2002}: |
| 12_conclusion.tex | 17 | `\cite{farin2002}` | Second, the journey metaphor---implemented through cubic Bézier curves \cite{farin2002} with arc-length parameterisation |

---

### gamma1994
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 10_api_design.tex | 29 | `\citep{gamma1994}` | The guiding principle: the engine should do only what the caller cannot do themselves. Complexity belongs in construction, not in the public interface \citep{gamma1994}. |

---

### hong2024
**Occurrences:** 9

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 24 | `\citep{hong2024}` | Recent comprehensive measurements of human color discrimination thresholds confirm that color space must be modeled as a \emph{Riemannian manifold}—a space that is locally Euclidean but globally curved \citep{hong2024}. |
| 02_perceptual_foundations.tex | 26 | `\citep{hong2024}` (×2) | In a Riemannian manifold, the shortest path is a \emph{geodesic}—a curve that follows the intrinsic geometry of the space \citep{hong2024}. The perceptual distance between two colors corresponds to the geodesic distance [...] \citep{hong2024}. |
| 02_perceptual_foundations.tex | 28 | `\citeyearpar{hong2024}` | Hong et al.\ \citeyearpar{hong2024} characterized this structure empirically |
| 02_perceptual_foundations.tex | 42 | `\citep{hong2024}` | \textbf{Radial orientation:} Major axes of threshold ellipses are consistently oriented toward the achromatic center \citep{hong2024} |
| 02_perceptual_foundations.tex | 56 | `\citep{hong2024}` | Hong et al.'s ellipse measurements \citep{hong2024} provide the data needed to construct position-dependent distance corrections. |
| 02_perceptual_foundations.tex | 58 | `\citep{hong2024}` | Hong et al.'s finding that discrimination ellipses orient radially toward the achromatic center \citep{hong2024} justifies reducing saturation |
| 02_perceptual_foundations.tex | 65 | `\citep{hong2024}` (×2) | The approximation is not perfect—local curvature remains \citep{hong2024}—but the error is small enough [...] |

---

### hunt2004
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 05_style_controls.tex | 15 | `\citep{hunt2004}` | Temperature biases the journey's hue path toward warm or cool colors \citep{hunt2004}. |
| 08_gamut_management.tex | 108 | `\citep{hunt2004}` | This preserves the journey's ``character'' (its hue story) even when display limitations require desaturation \citep{hunt2004}. |

---

### itten1961
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 89 | `\citep{itten1961}` | Traditional \emph{color harmony rules}---complementary, triadic, analogous, split-complementary---define geometric relationships on the color wheel \citep{itten1961}. |

---

### judd1940
**Occurrences:** 1 (WITH PAGE NUMBER)

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 77 | `\citep[p.~11]{judd1940}` | ✅ **HAS PAGE** - it is a mathematical constraint arising from the ``super-importance of hue'' first identified by Judd \citep[p.~11]{judd1940}. |

---

### kamermans2023
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 109 | `\cite{kamermans2023}` | Arc-length parameterisation~\cite{piegl1997,kamermans2023} for perceptually uniform sampling |
| 03_journey_construction.tex | 188 | `\citep{kamermans2023}` | For efficiency, the engine uses numerical approximation following established techniques \citep{kamermans2023}: |

---

### knuth1997
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 09_variation_determinism.tex | 76 | `\citep{knuth1997}` | The variation layer uses a \textbf{pseudo-random number generator (PRNG)} with these properties \citep{knuth1997}: |

---

### kong2021
**Occurrences:** 3 (1 with page, 2 without)

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 103 | `\citep{kong2021}` | This result explains why even carefully designed spaces like CIELAB exhibit perceptual nonuniformities \citep{kong2021}: |
| 02_perceptual_foundations.tex | 106 | `\citeyearpar{kong2021}` | \textbf{CIELAB (1976):} Achieves approximate uniformity in spatial discrimination tasks but fails for temporal transitions. Kong \citeyearpar{kong2021} notes explicitly |
| 02_perceptual_foundations.tex | 106 | `\citep[p.~3]{kong2021}` | ✅ **HAS PAGE** - ``CIELAB is not a useful space to predict the perception of dynamic colored light [...] \citep[p.~3]{kong2021}. |
| 02_perceptual_foundations.tex | 304 | `\citep[p.~3]{kong2021}` | ``The visibility threshold of smoothness [...] is about ten times smaller for lightness changes than for chroma or hue changes in CIELAB'' \citep[p.~3]{kong2021} |

---

### levien2018arclength
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 03_journey_construction.tex | 176 | `\citep{levien2018arclength}` | The engine estimates total arc length and samples at equal arc-length intervals \citep{levien2018arclength}: |

---

### levien2021oklab
**Occurrences:** 3

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 101 | `\cite{levien2021oklab}` | Independent analysis has validated OKLab's perceptual uniformity claims for gradient and color manipulation applications~\cite{levien2021oklab}. |
| 02_perceptual_foundations.tex | 142 | `\citep{levien2021oklab}` | It has gained rapid adoption in web standards (CSS Color Level 4) \citep{csscolor4}, creative software, and independent validation for gradient quality \citep{levien2021oklab}. |

---

### liu2013palette
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 95 | `\citep{liu2013palette}` | More recent academic work has explored \emph{data-driven approaches} that learn palette patterns from images or existing designs. Liu et al.\ \citep{liu2013palette} demonstrate image-driven harmonious color extraction |

---

### luo2001
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 99 | `\cite{luo2001}` | CIEDE2000~\cite{luo2001} improved color difference calculation but remains computationally complex. |
| 04_perceptual_constraints.tex | 23 | `\citep{fairchild2013,luo2001}` | Color science literature consistently shows that laboratory JND values [...] underestimate the threshold needed for reliable discrimination in real applications \citep{fairchild2013,luo2001}. |

---

### mahy1994
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 99 | `\cite{mahy1994}` | CIELAB~\cite{cie1976} was the first widely-used perceptual space but exhibits known uniformity issues, particularly in blue-violet regions~\cite{mahy1994}. |

---

### moosbauer2025
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 12_conclusion.tex | 65 | `\citep{moosbauer2025}` | Recent work on symmetry-constrained search in combinatorial domains \citep{moosbauer2025} suggests that constraining search to symmetric or well-behaved curve families |

---

### morovic2008
**Occurrences:** 5

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 112 | `\cite{morovic2008}` | Two-layer gamut management~\cite{morovic2008} preventing and correcting out-of-gamut colors |
| 08_gamut_management.tex | 20 | `\citep{morovic2008}` | OKLab is a perceptually uniform color space, but it encompasses colors that lie outside any real display's capabilities \citep{morovic2008}: |
| 08_gamut_management.tex | 79 | `\citep{morovic2008}` | This approach follows established best practices in color management \citep{morovic2008}. |
| 08_gamut_management.tex | 98 | `\citep{morovic2008}` | When gamut mapping is required, the engine follows a strict priority hierarchy rooted in established gamut mapping practice \citep{morovic2008}: |
| 12_conclusion.tex | 36 | `\citep{morovic2008}` | Two-Layer Gamut Management. A prevention-then-correction strategy following established gamut mapping principles \citep{morovic2008} |

---

### nolle2012
**Occurrences:** 6

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 77 | `\citep{nolle2012}` | A fundamental result in perceptual color theory is that no single global 3D Euclidean coordinate system can make perceptual distance everywhere equal to Euclidean distance without distortion \citep{nolle2012}. |
| 02_perceptual_foundations.tex | 79 | `\citeyearpar{nolle2012}` | Nölle et al.\ \citeyearpar{nolle2012} provide a rigorous derivation. |
| 02_perceptual_foundations.tex | 86 | `\citep{nolle2012}` | Empirical measurements of color discrimination thresholds yield \citep{nolle2012}: |
| 02_perceptual_foundations.tex | 93 | `\citep{nolle2012}` | Color space requires approximately \emph{twice} this value—the hue circle has an effective ``circumference'' of 720° rather than 360° \citep{nolle2012}. |
| 02_perceptual_foundations.tex | 99 | `\citep{nolle2012,roberti2023}` | This ``extra length'' cannot be accommodated in three-dimensional Euclidean geometry. It implies that color space has intrinsic curvature: the space is \emph{non-Euclidean} \citep{nolle2012,roberti2023}. |
| 02_perceptual_foundations.tex | 119 | `\citep{nolle2012}` | A Möbius strip—a surface with a single half-twist—also requires traversing 720° to return to the original orientation \citep{nolle2012}. |

---

### ottosson2020
**Occurrences:** 9

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 64 | `\cite{ottosson2020}` | All design decisions rest on the perceptual uniformity of OKLab color space \cite{ottosson2020}. |
| 01_introduction.tex | 101 | `\cite{ottosson2020}` | OKLab, introduced by Björn Ottosson in 2020~\cite{ottosson2020}, represents a significant advance |
| 02_perceptual_foundations.tex | 65 | `\citep{ottosson2020,safdar2017}` | Modern perceptually uniform color spaces (OKLab, CAM16-UCS) are designed such that Euclidean distance $\Delta E$ in the coordinate representation approximates geodesic distance in the underlying perceptual manifold \citep{ottosson2020,safdar2017}. |
| 02_perceptual_foundations.tex | 142 | `\citep{ottosson2020}` | OKLab, introduced by Björn Ottosson in 2020 \citep{ottosson2020}, achieves an excellent balance |
| 02_perceptual_foundations.tex | 175 | `\citep{ottosson2020}` | altering $a$ or $b$ primarily affects hue and saturation without changing perceived lightness \citep{ottosson2020}. |
| 02_perceptual_foundations.tex | 197 | `\citep{ottosson2020}` | The transformation matrices are \citep{ottosson2020}: |
| 02_perceptual_foundations.tex | 219 | `\citep{ottosson2020}` | the cube root models nonlinear perceptual compression [...] and refined through modern understanding of cone response functions \citep{ottosson2020}; |
| 04_perceptual_constraints.tex | 19 | `\citep{ottosson2020}` | Theoretical JND threshold: $\Delta E \approx 1.0$ unit (OKLab's design target \citep{ottosson2020}) |
| 12_conclusion.tex | 47 | `\citep{ottosson2020}` | OKLab's JND correspondence ($\Delta E \approx 1.0$) is a design target \citep{ottosson2020}; |

---

### piegl1997
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 109 | `\cite{piegl1997,kamermans2023}` | Arc-length parameterisation~\cite{piegl1997,kamermans2023} for perceptually uniform sampling |
| 03_journey_construction.tex | 170 | `\citep{piegl1997,kamermans2023}` | The Bézier parameter $t$ does not correspond to distance along the curve \citep{piegl1997,kamermans2023}. |

---

### poynton2012
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 05_style_controls.tex | 131 | `\citep{poynton2012}` | Range $0.0$ to $2.0$, default $1.0$. Selectively boosts chroma of less-saturated colors while leaving already-vibrant colors unchanged \citep{poynton2012}. |
| 11_caller_responsibilities.tex | 52 | `\citep{poynton2012}` | \paragraph{Context Suitability.} Print and screen have different requirements \citep{poynton2012}. |

---

### programmingdesignsystems2017
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 92 | `\citep{programmingdesignsystems2017}` | Even when tools support perceptual spaces, they typically output continuous gradients rather than discrete palettes with distinguishability guarantees \citep{programmingdesignsystems2017}. |

---

### roberti2023
**Occurrences:** 3

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 47 | `\citep{roberti2023}` | This Riemannian framework has historical foundations extending to Schrödinger's extension of Helmholtz's line element \citep{roberti2023}. |
| 02_perceptual_foundations.tex | 47 | `\citeyearpar{roberti2023}` | Roberti and Peruzzi \citeyearpar{roberti2023} note that Schrödinger distinguished between \emph{lower color metrics} |
| 02_perceptual_foundations.tex | 99 | `\citep{nolle2012,roberti2023}` | This ``extra length'' cannot be accommodated in three-dimensional Euclidean geometry. It implies that color space has intrinsic curvature: the space is \emph{non-Euclidean} \citep{nolle2012,roberti2023}. |

---

### safdar2017
**Occurrences:** 2

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 101 | `\cite{safdar2017}` | OKLab, introduced by Björn Ottosson in 2020~\cite{ottosson2020}, represents a significant advance: CAM16-level perceptual uniformity~\cite{safdar2017} |
| 02_perceptual_foundations.tex | 65 | `\citep{ottosson2020,safdar2017}` | Modern perceptually uniform color spaces (OKLab, CAM16-UCS) are designed such that Euclidean distance $\Delta E$ in the coordinate representation approximates geodesic distance in the underlying perceptual manifold \citep{ottosson2020,safdar2017}. |

---

### sekulovski2007
**Occurrences:** 5

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 301 | `\citeyearpar{sekulovski2007}` | Beyond eye movement effects, the visual system exhibits channel-specific temporal sensitivities. Sekulovski et al.\ \citeyearpar{sekulovski2007} measured smoothness thresholds |
| 02_perceptual_foundations.tex | 304 | `\citet{sekulovski2007}` | ``The visibility threshold of smoothness [...] \citep[p.~3]{kong2021}, citing \citet{sekulovski2007}. |
| 02_perceptual_foundations.tex | 307 | `\citep{sekulovski2007}` | In other words, observers are approximately \textbf{10 times more sensitive} to temporal changes in lightness than to changes in chromatic attributes \citep{sekulovski2007}. |
| 02_perceptual_foundations.tex | 309 | `\citeyearpar{sekulovski2007}` | Importantly, Sekulovski et al.\ \citeyearpar{sekulovski2007} found that lightness thresholds are \emph{independent} of base chromaticity: |
| 02_perceptual_foundations.tex | 312 | `\citep{sekulovski2007}` | ``No main effect of the base color point on the thresholds for lightness changes was found [...] \citep{sekulovski2007}. |
| 02_perceptual_foundations.tex | 324 | `\citep{sekulovski2007}` | \textbf{Lightness velocity weight:} $w_L = 10.0$ reflects the heightened temporal sensitivity \citep{sekulovski2007} |
| 02_perceptual_foundations.tex | 329 | `\citep{sekulovski2007}` | The 10:1 ratio for $w_L : w_C$ is empirically validated \citep{sekulovski2007}. |

---

### stone2014
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 01_introduction.tex | 92 | `\citep{stone2014}` | Most creative tools (CSS gradients, design software) use linear interpolation in RGB or HSL space, producing results that can appear perceptually uneven---muddy midpoints, abrupt hue shifts through grey regions, and inconsistent step sizes \citep{stone2014}. |

---

### wang2022
**Occurrences:** 1

| File | Line | Citation | Context |
|------|------|----------|---------|
| 02_perceptual_foundations.tex | 329 | `\citep{wang2022}` | Future work should employ psychometric methods (e.g., two-alternative forced-choice paradigms \citep{wang2022}) to measure hue temporal sensitivity rigorously. |

---

## File-by-File Breakdown

### 01_introduction.tex
**Total Citations:** 20
**With Page Numbers:** 0
**Without Page Numbers:** 20

| Line | Citation | Cite Key |
|------|----------|----------|
| 64 | `\cite{ottosson2020}` | ottosson2020 |
| 89 | `\citep{itten1961}` | itten1961 |
| 92 | `\citep{stone2014}` | stone2014 |
| 92 | `\citep{programmingdesignsystems2017}` | programmingdesignsystems2017 |
| 95 | `\citep{liu2013palette}` | liu2013palette |
| 99 | `\cite{cie1976}` | cie1976 |
| 99 | `\cite{mahy1994}` | mahy1994 |
| 99 | `\cite{luo2001}` | luo2001 |
| 101 | `\cite{ottosson2020}` | ottosson2020 |
| 101 | `\cite{safdar2017}` | safdar2017 |
| 101 | `\cite{levien2021oklab}` | levien2021oklab |
| 101 | `\cite{csscolor4}` | csscolor4 |
| 108 | `\cite{farin2002}` | farin2002 |
| 109 | `\cite{piegl1997,kamermans2023}` | piegl1997, kamermans2023 |
| 112 | `\cite{morovic2008}` | morovic2008 |
| 112 | `\cite{colorjs2025}` | colorjs2025 |

---

### 02_perceptual_foundations.tex
**Total Citations:** 44
**With Page Numbers:** 3
**Without Page Numbers:** 41

| Line | Citation | Cite Key | Has Page? |
|------|----------|----------|-----------|
| 24 | `\citep{hong2024}` | hong2024 | ❌ |
| 26 | `\citep{hong2024}` (×2) | hong2024 | ❌ |
| 28 | `\citeyearpar{hong2024}` | hong2024 | ❌ |
| 42 | `\citep{hong2024}` | hong2024 | ❌ |
| 47 | `\citep{roberti2023}` | roberti2023 | ❌ |
| 47 | `\citeyearpar{roberti2023}` | roberti2023 | ❌ |
| 56 | `\citep{hong2024}` | hong2024 | ❌ |
| 58 | `\citep{hong2024}` | hong2024 | ❌ |
| 65 | `\citep{ottosson2020,safdar2017}` | ottosson2020, safdar2017 | ❌ |
| 65 | `\citep{hong2024}` | hong2024 | ❌ |
| 77 | `\citep{nolle2012}` | nolle2012 | ❌ |
| 77 | `\citep[p.~11]{judd1940}` | judd1940 | ✅ |
| 79 | `\citeyearpar{nolle2012}` | nolle2012 | ❌ |
| 86 | `\citep{nolle2012}` | nolle2012 | ❌ |
| 93 | `\citep{nolle2012}` | nolle2012 | ❌ |
| 99 | `\citep{nolle2012,roberti2023}` | nolle2012, roberti2023 | ❌ |
| 103 | `\citep{kong2021}` | kong2021 | ❌ |
| 106 | `\citeyearpar{kong2021}` | kong2021 | ❌ |
| 106 | `\citep[p.~3]{kong2021}` | kong2021 | ✅ |
| 119 | `\citep{nolle2012}` | nolle2012 | ❌ |
| 142 | `\citep{ottosson2020}` | ottosson2020 | ❌ |
| 142 | `\citep{csscolor4}` | csscolor4 | ❌ |
| 142 | `\citep{levien2021oklab}` | levien2021oklab | ❌ |
| 175 | `\citep{ottosson2020}` | ottosson2020 | ❌ |
| 197 | `\citep{ottosson2020}` | ottosson2020 | ❌ |
| 217 | `\citep{csscolor4}` | csscolor4 | ❌ |
| 219 | `\citealt{fairchild2013}, Chapter~3` | fairchild2013 | ✅ |
| 219 | `\citep{ottosson2020}` | ottosson2020 | ❌ |
| 287 | `\citeyearpar{braun2017}` | braun2017 | ❌ |
| 290 | `\citep{braun2017}` | braun2017 | ❌ |
| 294 | `\citep{braun2017}` | braun2017 | ❌ |
| 301 | `\citeyearpar{sekulovski2007}` | sekulovski2007 | ❌ |
| 304 | `\citep[p.~3]{kong2021}` | kong2021 | ✅ |
| 304 | `\citet{sekulovski2007}` | sekulovski2007 | ❌ |
| 307 | `\citep{sekulovski2007}` | sekulovski2007 | ❌ |
| 309 | `\citeyearpar{sekulovski2007}` | sekulovski2007 | ❌ |
| 312 | `\citep{sekulovski2007}` | sekulovski2007 | ❌ |
| 324 | `\citep{sekulovski2007}` | sekulovski2007 | ❌ |
| 329 | `\citep{sekulovski2007}` | sekulovski2007 | ❌ |
| 329 | `\citep{wang2022}` | wang2022 | ❌ |

---

### 03_journey_construction.tex
**Total Citations:** 5
**With Page Numbers:** 0
**Without Page Numbers:** 5

| Line | Citation | Cite Key |
|------|----------|----------|
| 50 | `\citep{cowan2001}` | cowan2001 |
| 50 | `\citep{farin2002}` | farin2002 |
| 125 | `\cite{farin2002}` | farin2002 |
| 170 | `\citep{piegl1997,kamermans2023}` | piegl1997, kamermans2023 |
| 176 | `\citep{levien2018arclength}` | levien2018arclength |
| 188 | `\citep{kamermans2023}` | kamermans2023 |

---

### 04_perceptual_constraints.tex
**Total Citations:** 6
**With Page Numbers:** 0
**Without Page Numbers:** 6

| Line | Citation | Cite Key |
|------|----------|----------|
| 15 | `\citep{fairchild2013}` | fairchild2013 |
| 19 | `\citep{ottosson2020}` | ottosson2020 |
| 23 | `\citep{fairchild2013,luo2001}` | fairchild2013, luo2001 |
| 25 | `\citep{csscolor4}` | csscolor4 |
| 41 | `\cite{fairchild2013}` | fairchild2013 |
| 55 | `\citep{fairchild2013}` | fairchild2013 |

---

### 05_style_controls.tex
**Total Citations:** 2
**With Page Numbers:** 0
**Without Page Numbers:** 2

| Line | Citation | Cite Key |
|------|----------|----------|
| 15 | `\citep{hunt2004}` | hunt2004 |
| 131 | `\citep{poynton2012}` | poynton2012 |

---

### 06_modes_of_operation.tex
**Total Citations:** 2
**With Page Numbers:** 0
**Without Page Numbers:** 2

| Line | Citation | Cite Key |
|------|----------|----------|
| 47 | `\citep{fairchild2013}` | fairchild2013 |
| 92 | `\citep{fairchild2013}` | fairchild2013 |

---

### 07_loop_strategies.tex
**Total Citations:** 1
**With Page Numbers:** 0
**Without Page Numbers:** 1

| Line | Citation | Cite Key |
|------|----------|----------|
| 38 | `\citep{farin2002}` | farin2002 |

---

### 08_gamut_management.tex
**Total Citations:** 7
**With Page Numbers:** 0
**Without Page Numbers:** 7

| Line | Citation | Cite Key |
|------|----------|----------|
| 20 | `\citep{morovic2008}` | morovic2008 |
| 64 | `\citep{csscolor4}` | csscolor4 |
| 64 | `\citep{colorjs2025}` | colorjs2025 |
| 74 | `\citep{csscolor4}` | csscolor4 |
| 79 | `\citep{morovic2008}` | morovic2008 |
| 98 | `\citep{morovic2008}` | morovic2008 |
| 106 | `\citep{morovic2008,fairchild2013}` | morovic2008, fairchild2013 |
| 108 | `\citep{hunt2004}` | hunt2004 |

---

### 09_variation_determinism.tex
**Total Citations:** 2
**With Page Numbers:** 0
**Without Page Numbers:** 2

| Line | Citation | Cite Key |
|------|----------|----------|
| 76 | `\citep{knuth1997}` | knuth1997 |
| 82 | `\citep{blackman2018}` | blackman2018 |

---

### 10_api_design.tex
**Total Citations:** 2
**With Page Numbers:** 0
**Without Page Numbers:** 2

| Line | Citation | Cite Key |
|------|----------|----------|
| 15 | `\citep{bloch2008}` | bloch2008 |
| 29 | `\citep{gamma1994}` | gamma1994 |

---

### 11_caller_responsibilities.tex
**Total Citations:** 1
**With Page Numbers:** 0
**Without Page Numbers:** 1

| Line | Citation | Cite Key |
|------|----------|----------|
| 52 | `\citep{poynton2012}` | poynton2012 |

---

### 12_conclusion.tex
**Total Citations:** 5
**With Page Numbers:** 0
**Without Page Numbers:** 5

| Line | Citation | Cite Key |
|------|----------|----------|
| 17 | `\cite{ottosson2020}` | ottosson2020 |
| 17 | `\cite{farin2002}` | farin2002 |
| 34 | `\citep{fairchild2013}` | fairchild2013 |
| 36 | `\citep{morovic2008}` | morovic2008 |
| 47 | `\citep{ottosson2020}` | ottosson2020 |
| 65 | `\citep{moosbauer2025}` | moosbauer2025 |

---

## Recommendations for Page Number Addition

### High Priority (Direct Quotes)
These citations contain direct quotes and MUST have page numbers per Harvard style:

1. **kong2021** - Line 106, 304 (already has p.~3, but verify quote accuracy)
2. **sekulovski2007** - Line 304, 312 (direct quotes, NEEDS page numbers)
3. **fairchild2013** - Line 219 (already has "Chapter~3", but could be more specific)

### Medium Priority (Specific Claims/Data)
These citations make specific quantitative or empirical claims that would benefit from page numbers:

1. **braun2017** - Lines 290, 294 (specific percentages: 12%, 58%)
2. **hong2024** - All 9 occurrences (specific empirical findings)
3. **nolle2012** - Lines 86, 93 (specific mathematical results)
4. **sekulovski2007** - Lines 307, 324, 329 (10:1 ratio claim)
5. **ottosson2020** - Lines 19, 197, 219 (specific technical details)
6. **csscolor4** - Lines 25, 74 (specific threshold values)

### Lower Priority (General References)
These could remain as general citations but would be strengthened with page numbers:

- All other citations to **fairchild2013** (general color science principles)
- Citations to **morovic2008** (established practices)
- Citations to **farin2002** (standard Bézier curve mathematics)

---

## Next Steps

1. **Locate Source Documents** - Gather PDFs for all cited works
2. **Extract Page Numbers** - For each citation, find the specific page(s) where the claim/quote appears
3. **Update LaTeX Files** - Add page numbers using format: `\citep[p.~XX]{key}` or `\citep[pp.~XX--YY]{key}`
4. **Verify Quotes** - Ensure all quoted text matches source exactly
5. **Document in Bibliography** - Verify all cite keys exist in `references.bib`

---

## Citation Style Guidelines

**Harvard Style (Cite Them Right) Recommendations:**

- **Direct quotes:** ALWAYS include page number(s)
- **Specific data/figures:** STRONGLY RECOMMENDED to include page number(s)
- **General concepts:** Page numbers optional but recommended
- **Multiple pages:** Use `pp.~XX--YY` format
- **Single page:** Use `p.~XX` format
- **Chapter reference:** Use `Chapter~X` or combine with pages

**LaTeX Syntax:**
```latex
\citep[p.~42]{author2024}           % Single page
\citep[pp.~42--45]{author2024}      % Page range
\citep[Chapter~3, p.~42]{author2024} % Chapter and page
```

---

**Report Generated:** 2025-12-30
**Total Files Analyzed:** 12
**Total Citations:** 93 (91 unique command instances)
**Missing Page Numbers:** 90 (96.8%)
