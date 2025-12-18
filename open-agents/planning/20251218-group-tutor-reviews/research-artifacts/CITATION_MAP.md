# Citation Map & Section Relevance Index

This document maps the rigorous "PhD-level" citations to the specific sections of the report where they provide critical evidence. It serves as a bridge between the Research Artifacts (M1-M4) and the LaTeX Report Sections.

> **Last Updated:** Session continuation - comprehensive extraction from all 10 collected sources

---

## 📚 Section 02: Perceptual Foundations
*Establishing the mathematical and psychophysical basis for the engine.*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Hong et al. (2024)** | **Riemannian Manifold:** Color space is curved, not Euclidean. Geodesics (shortest paths) are curved lines. Discrimination ellipses are radially oriented toward the achromatic axis. | M1 | Validates that linear interpolation in RGB is perceptually incorrect; justifies complex pathing. |
| **Nölle et al. (2012)** | **720° Topology:** Hue circle circumference is $\approx 4\pi$ (12.65), not $2\pi$. Requires 720° rotation to return to origin. Judd's result: "hue is of superimportant importance." | M4 | **CRITICAL PROOF** for the "twisted" Möbius topology of the engine. |
| **Sekulovski et al. (2007)** | **10:1 Asymmetry:** Temporal sensitivity to Lightness changes is 10x higher than to Chroma changes. | M1 | Justifies separating Lightness and Chroma into different "tracks" or frequencies. |
| **Kong (2021)** | **No Temporal Uniformity:** "CIELAB... is not a useful space to predict the perception of dynamic colored light. Today, no color spaces are available that accurately predict the visibility of color differences over time." | M1 | **CRITICAL FINDING** - validates the paper's novel contribution to temporal color perception. |
| **Roberti & Peruzzi (2023)** | **Schrödinger's Color Metrics:** "Lower color metrics" (threshold discrimination) vs "higher color metrics" (large differences). Line element: $ds^2 = g_{ij} dx^i dx^j$ | M1 | Historical foundation for Riemannian approach; validates mathematical framework choice. |
| **Fairchild (2013)** | **Hunt & Stevens Effects:** Colorfulness increases with luminance (Hunt); brightness/lightness follow power law (Stevens). Observer variability is significant. | M1 | Justifies dynamic adaptation algorithms; explains why static color spaces fail. |
| **Fechner (1860)** | **Logarithmic Scaling:** Sensation scales logarithmically with stimulus. | General | Foundation for all perceptual mapping. |
| **Stevens (1957)** | **Power Laws:** Refinement of Fechner's law for specific modalities. | General | Fine-tuning the perceptual curves. |

## 🔄 Section 03: Journey Construction
*Building the paths through color space.*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Walmsley et al. (2015)** | **Natural Variance:** 78.5% of daylight variance is along the Blue-Yellow axis (color), vs 75.8% for irradiance. "The spectral composition of twilight is... remarkably consistent across seasons and locations." | M3 | Proves that color temperature cycles are the dominant feature of natural light, justifying the "Daylight Locus" strategy. |
| **Spitschan (2017)** | **Melanopsin Pathway:** Peak sensitivity at 480nm (blue). "Melanopsin-expressing retinal ganglion cells... drive circadian photoentrainment." Separated from image-forming vision. | M3 | **CRITICAL** for understanding non-visual pathways; justifies separate treatment of circadian-relevant wavelengths. |
| **Foster & Nascimento (1994)** | **Cone Excitation:** Ratios remain stable under illuminant changes. | M3 | Biological basis for color constancy in journey construction. |
| **Süsstrunk (2005)** | **Sharp Sensors:** "Sensors designed with sharp transition at ~550nm" improve spectral recovery for chromatic adaptation. | M3 | Design guidance for spectral handling in the engine. |

## 🚧 Section 04: Perceptual Constraints
*Limits and boundaries of the system.*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Kong (2021)** | **Temporal Thresholds:** "The threshold for L\* was found to be approximately 10 times smaller than for the chromaticity indices a\* and b\*." Confirmed across all experimental conditions. | M1 | **QUANTITATIVE BASIS** for the 10:1 L\*/Chroma asymmetry; justifies differential rate limiting. |
| **Sekulovski et al. (2007)** | **Speed-Sensitive Perception:** Transition rates affect perceived color difference. "Visual system... integrates color information over time." | M1 | Foundational work that Kong (2021) extended; establishes temporal perception as key constraint. |
| **Gao et al. (2020)** | **von Kries Properties:** The von Kries transform satisfies symmetry and transitivity—"if A adapts to B, then B adapts to A" (symmetry), and "if A→B→C, then A→C directly" (transitivity). | M1 | Validates chromatic adaptation model choice; ensures reversible color journeys. |
| **Hong et al. (2024)** | **Ellipse Orientation:** Discrimination ellipses are "radially oriented toward the achromatic axis." | M1 | Gamut boundary behavior; justifies radial compression strategies. |
| **Atkins et al. (1994)** | **Dynamic Range:** Human vision compresses dynamic range non-linearly. | General | Justifies the "soft-clipping" and compression algorithms. |
| **Tan & ISO (2018)** | **HDR Standards:** Modern standards for high dynamic range imaging. | General | Benchmarks for the engine's output capabilities. |

## 🎛️ Section 07: Loop Strategies
*Closing the circle (or Möbius strip).*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Nölle et al. (2012)** | **Möbius Connection:** The 720° requirement mathematically implies a Möbius-like structure for continuous hue loops. "The double covering of the circle group SO(2) by Spin(2)." | M4 | **THEORETICAL VALIDATION** for the "Möbius Loop" strategy. |
| **Webster et al. (2012)** | **Category Boundaries:** "Large individual differences in the loci of color term boundaries." Focal colors (best examples) are more stable than boundaries. | M4 | Helps define perceptual "landmarks" along the loop while acknowledging boundary fluidity. |
| **Troost & de Weert (1992)** | **Naming Categories:** Categorical perception of color. | M4 | Helps define "landmarks" along the loop (e.g., "Red", "Blue"). |
| **Fairchild (2013)** | **Observer Variability:** Individual differences in color perception are significant and must be accommodated. | M4 | Justifies flexible/adaptive loop strategies rather than fixed hue positions. |

## 🎨 Section 08: Gamut Management
*Handling out-of-bounds colors.*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Hong et al. (2024)** | **Geodesic Paths:** In curved perceptual space, shortest paths (geodesics) are not straight lines. "The metric describes the local geometry." | M1 | Gamut compression should follow geodesics, not linear projections. |
| **Gao et al. (2020)** | **Generalized von Kries:** Extends classical von Kries to arbitrary transforms while preserving key properties. | M1 | Framework for gamut-aware adaptation transforms. |
| **Braun & Fairchild (2017)** | **Gamut Mapping:** Techniques for preserving perceptual intent when reducing gamut. | General | Algorithms for the "Gamut Compression" module. |
| **Wang et al. (2022)** | **Gamut Volume:** Methods for calculating the volume of reproducible colors. | General | Metrics for evaluating the engine's performance. |

---

## 🌡️ Section 05: Style Controls (Circadian Context)
*Adapting to time-of-day and biological rhythms.*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Spitschan (2017)** | **Melanopsin-Melatonin Pathway:** "Circadian disruption by light at night has been associated with increased risk for breast cancer, metabolic dysfunction, and mood disorders." | M3 | Establishes health implications; justifies careful blue-light handling at night. |
| **Walmsley et al. (2015)** | **Twilight Consistency:** "The spectral composition of twilight is, perhaps surprisingly, remarkably consistent across seasons and locations." | M3 | Enables predictable circadian-aligned color journeys. |

## ⚙️ Section 09: Variation & Determinism
*Balancing predictability with organic variation.*

| Citation | Key Finding | Artifact | Relevance |
|----------|-------------|----------|-----------|
| **Fairchild (2013)** | **Observer Variability:** "Because of individual differences in color matching functions, no single set of color matching functions can be used to predict the color perceptions of all observers." | M1 | Justifies incorporating variation to accommodate observer differences. |
| **Kong (2021)** | **Temporal Integration:** Visual system integrates color information over time; rapid changes may be imperceptible. | M1 | Variation rate must respect temporal integration limits. |

---

## 📂 Artifact Index

| Artifact | Focus Area | Key Citations |
|----------|------------|---------------|
| **M1** | Chromatic Inversion, Temporal Perception, Mathematical Framework | Hong (2024), Sekulovski (2007), Kong (2021), Gao (2020), Roberti (2023), Fairchild (2013) |
| **M2** | Gestalt Principles, Apparent Motion, Perceptual Continuity | Wertheimer (1923), Kolers (1972), Gestalt literature |
| **M3** | Natural Cycles, Daylight Locus, Circadian Biology | Walmsley (2015), Spitschan (2017), Foster (1994), Süsstrunk (2005) |
| **M4** | Topology, Möbius Structure, Categorical Perception | Nölle (2012), Webster (2012), Troost (1992) |

---

## 📖 Complete Source Bibliography

### Primary Sources (Extracted & Analyzed)

| Author(s) | Year | Title | Type | Key Contribution |
|-----------|------|-------|------|------------------|
| **Hong, Huang & Luo** | 2024 | The geometry of color perception | Article | Riemannian manifold framework, geodesics, ellipse orientation |
| **Nölle, Fah, Schaefer & Hardeberg** | 2012 | Euclidean Spectral Colour Metric | Conference | 720° topology proof, $4\pi$ circumference |
| **Kong** | 2021 | Temporal Color Perception (PhD Thesis) | Thesis | 10:1 asymmetry confirmation, "no temporally uniform space exists" |
| **Sekulovski, Seuntiens & Heynderickx** | 2007 | Perception of the smoothness of colour transitions | Conference | Original 10:1 finding, temporal color integration |
| **Walmsley et al.** | 2015 | Colour as a Signal for Entraining the Mammalian Circadian Clock | Article | 78.5% blue-yellow variance, twilight consistency |
| **Spitschan** | 2017 | Melanopsin Contributions to Non-Visual and Visual Function | Review | Melanopsin pathway, 480nm peak, circadian photoentrainment |
| **Fairchild** | 2013 | Color Appearance Models (3rd ed.) | Book | Hunt/Stevens effects, observer variability |
| **Gao, Ling, Kwok & Luo** | 2020 | Generalised Structure of von Kries | Article | Symmetry/transitivity properties of chromatic adaptation |
| **Roberti & Peruzzi** | 2023 | Schrödinger's color theory | Article | Historical lower/higher metrics, Riemannian line element |
| **Süsstrunk** | 2005 | Chromatic Adaptation (PhD Thesis) | Thesis | Sharp sensor design for spectral recovery |

### Secondary Sources (Referenced)

| Author(s) | Year | Key Contribution |
|-----------|------|------------------|
| **Webster, Miyahara, Malkoc & Raker** | 2012 | Color category boundaries vary across observers |
| **Foster & Nascimento** | 1994 | Cone excitation ratios and color constancy |
| **Troost & de Weert** | 1992 | Categorical color perception |
| **Braun & Fairchild** | 2017 | Gamut mapping techniques |
| **Fechner** | 1860 | Logarithmic psychophysical scaling |
| **Stevens** | 1957 | Power law refinement |
