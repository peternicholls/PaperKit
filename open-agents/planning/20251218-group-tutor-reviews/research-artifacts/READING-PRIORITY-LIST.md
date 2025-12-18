# Reading Priority List for Color Journey Paper

**Generated:** 2024-12-18  
**Purpose:** Prioritize which papers to read first for maximum research impact

---

## 🔴 CRITICAL - Read Immediately (Already Collected)

These papers are already downloaded and provide foundational support for the paper's core arguments.

### 1. Fairchild (2013) - Color Appearance Models 📚
**Location:** `color-perception/Color appearance models 3rd edition.pdf`  
**Why Critical:** 
- Definitive reference for chromatic adaptation (CAM02/CAM16)
- Already cited in Section 2 (Perceptual Foundations)
- Provides theoretical grounding for OKLab design choices

**Action:** Extract key quotes on:
- Perceptual uniformity definition
- JND thresholds across color space
- Chromatic adaptation time course

---

### 2. Walmsley et al. (2015) - Colour as Circadian Signal 📚
**Location:** `circadian-twilight/Colour as a Signal for Entraining the Mammalian Circadian Clock - Walmsley 2015.pdf`  
**Why Critical:**
- Direct support for twilight progression as natural chromatic cycle
- Blue-yellow opponent axis as circadian signal (78.5% vs 75.8% variance explained)
- Validates Möbius inversion design choice

**Action:** Extract specific data on:
- Twilight duration (90 minutes / 3 phases)
- Blue-yellow discrimination superiority
- Evolutionary significance of color vision for time-of-day

**Relevant to:** Section 7 (Loop Strategies), Section 3 (Natural cycles as design template)

---

### 3. Braun et al. (2017) - Visual Sensitivity During Eye Movements 📚
**Location:** `color-perception/Visual sensitivity for luminance and chromatic stimuli...pdf`  
**Why Critical:**
- Chromatic sensitivity INCREASES 15% during smooth pursuit
- Informs temporal dynamics of color journey perception
- 58% reduction during saccades (avoid sudden jumps)

**Action:** Extract findings on:
- Pursuit enhancement for chromatic stimuli (p. 58)
- Timeline: 50ms before pursuit onset
- Design implications for smooth transitions

**Relevant to:** Section 3 (Journey construction), temporal smoothness requirements

---

### 4. Süsstrunk (2005) - Computing Chromatic Adaptation (Thesis) 📚
**Location:** `color-perception/Computing Chromatic Adaptation (thesis).pdf`  
**Why Critical:**
- Technical implementation details for CAT
- Sharp sensors for hue constancy
- Optimization approaches for sensor matrices

**Action:** Technical reference for:
- Sensor-based sharpening
- Hue constancy across illuminants
- Sharp CAT implementation if needed

**Relevant to:** Section 8 (Gamut Management), technical appendices

---

### 5. Troost (1992) - Perceptual and Computational Aspects of Color Constancy 📚
**Location:** `color-perception/PERCEPTUAL AND COMPUTATIONAL ASPECTS OF COLOR CONSTANCY.pdf`  
**Why Critical:**
- Sensory vs. cognitive mechanisms debate
- von Kries adaptation foundations
- Memory colors and context effects

**Action:** Extract theory on:
- Illuminant elimination
- Adaptation baselines
- First cycle establishes expectation for second

**Relevant to:** Section 7 (Möbius loop perception), theoretical grounding

---

### 6. Wang et al. (2022) - Rotation Gains and Perceptual Limitations 📚
**Location:** `color-perception/Rotation Gains Within and Beyond Perceptual Limitations.pdf`  
**Why Critical:**
- Psychometric function methodology (2AFC design)
- PSE (Point of Subjective Equality) framework
- Detection threshold interpretation (25%-75% range)

**Action:** Adapt methodology for:
- Closure threshold experiments
- Chromatic return detection studies
- Individual variation quantification

**Relevant to:** Section 7 (Loop closure precision), Appendix (User studies)

---

### 7. Gao et al. (2020) - von Kries Transform Generalization 📚
**Location:** `color-perception/The von Kries chromatic adaptation transform and its generalization.pdf`  
**Why Critical:**
- Symmetry and transitivity properties of CAT
- Mathematical rigor for opponent axis manipulation
- Corresponding colors framework

**Action:** Mathematical foundation for:
- Inversion as CAT analogue
- Reversibility requirements (apply twice = identity)
- Formal framework for $(L, -a, -b)$ operation

**Relevant to:** Section 7 (Möbius mathematical foundations), Appendix (Mathematical proofs)

---

## 🟠 HIGH PRIORITY - Search and Download Next

### 8. eLife (2024/2025) - Comprehensive Color Discrimination Thresholds ⚠️ OPEN ACCESS
**DOI:** Not yet found  
**URL:** https://elifesciences.org/reviewed-preprints/108943  
**Why High Priority:**
- State-of-the-art JND measurements across isoluminant plane
- Riemannian manifold framework (geodesic distances)
- Wishart Process Psychophysical Model (WPPM)
- ~6,000 trials per participant

**Action:** 
1. Download preprint PDF
2. Extract threshold data
3. Compare with MacAdam ellipses

**Relevant to:** Section 2 (JND definition), Section 3 (ΔE < 0.05 justification), Section 7 (Geodesic path for inversion)

**Status:** ⏳ NEED TO DOWNLOAD

---

### 9. Schrödinger (1920) & Roberti/Peruzzi (2023) - Riemannian Color Metrics ✅ FOUND & EXTRACTED
**Original Citation:** Schrödinger, E. (1920) 'Grundlinien einer Theorie der Farbenmetrik im Tagessehen', *Annalen der Physik*, 63(20-21), pp. 397-426, 427-456, 481-520

**Modern Analysis:** Roberti, V. and Peruzzi, G. (2023) 'The Helmholtz legacy in color metrics: Schrödinger's color theory', *Archive for History of Exact Sciences*, 77, pp. 305-335. doi:10.1007/s00407-023-00317-x

**Status:** ✅ FOUND & EXTRACTED (via Roberti & Peruzzi 2023 open access analysis)

**Key Findings:**
- **Schrödinger's Critique of Helmholtz:** Identified computational errors and non-additivity of brightness in Helmholtz's original Riemannian metric
- **Lower vs. Higher Color Metric:** Distinguished color matching (Grassmann affine geometry) from perceptual distances (Riemannian geometry)
- **Reformulated Metric:** Established framework where brightness is additive (planar surfaces) while color space maintains Riemannian curvature
- **Spectral Cone Model:** 3D color space represented as cone with white direction; complementary colors lie on planes through white
- **Impact:** Founded all modern color metrics (CIELab, OKLab, CAM16); earned Haitinger Prize from Austrian Academy (1920)

**Direct Relevance to Möbius Loop:**
- **Geodesic Path Framework:** Schrödinger's Riemannian approach enables calculation of optimal (shortest perceptual) path for 180° hue inversion
- **Brightness Independence:** Additive brightness property justifies separate control of luminance vs. chromaticity
- **Local vs. Global Curvature:** Explains why MacAdam ellipses (local) are approximately Euclidean but global color space is curved
- **Modern Validation:** Hong et al. (2024) empirically validates Schrödinger's Riemannian framework with comprehensive JND measurements

**Citation for M1/M2:**
> "Schrödinger maintained a strong distinction between lower and higher color metrics...In the domain of lower color metrics, an affine space sufficed to describe the laws of color mixture. On the other hand, in the domain of higher color metrics, a Riemannian space was demonstrated to be necessary to translate color differences into color distances." (Roberti & Peruzzi 2023, p. 319)

> "The identification of these shortcomings by Helmholtz's pupils might have led to the suppression of the key passages related to higher color metrics in the third edition of the Handbuch, condemning his pioneering work to oblivion." (Roberti & Peruzzi 2023, on Schrödinger's critique)

**Priority:** ⭐⭐⭐⭐⭐ **ESSENTIAL MATHEMATICAL FOUNDATION**

**File Location:** `mathematics/The Helmholtz legacy in color metrics - Schrödinger's color theory - Roberti 2023.pdf` (1.0 MB, 21 pages)

---

### 10. Sekulovski et al. (2007) - Smoothness and Flicker of Temporal Color Transitions ✅ FOUND & EXTRACTED
**Conference:** CIC15 (15th Color and Imaging Conference)  
**Publication:** Proceedings, Albuquerque, NM, pp. 112-117  
**DOI:** 10.2352/CIC.2007.15.1.art00021  
**Status:** ✅ EXTRACTED VIA KONG (2021) THESIS - FULLY INTEGRATED

**Key Findings:**
- **10:1 Asymmetry:** Smoothness threshold for luminance ~10× smaller than for chroma/hue in CIELAB
- **ΔE*ab/s Metric:** Standard metric for temporal color transition speeds
- **Flicker-Smoothness Correlation:** High correlation between flicker perception and smoothness thresholds
- **Implication:** CIELAB not suitable for temporal color space

**Key Quote:**
> "The visibility threshold of smoothness...is about ten times smaller for lightness changes than for chroma or hue changes in CIELAB." (Sekulovski et al. 2007, cited in Kong 2021, p. 530)

**Application to Color Journey Möbius Loop:**
- Luminance transitions require fine temporal resolution
- Hue/Chroma transitions can tolerate ~10× coarser step sizes
- Design must respect this asymmetry for smooth appearance

**Relevant to:** Section 2.1 (Smooth color transitions), Section 7 (Animation timing)

---

## 🟡 MEDIUM PRIORITY - Library Access Required

### 11. Hurvich & Jameson (1957) - Opponent-Process Theory 📚 FOUNDATIONAL
**Citation:** *Psychological Review*, 64(6), pp. 384-404  
**DOI:** 10.1037/h0041403  
**Why Medium Priority:**
- Foundational for opponent axis theory
- Justifies $(L, -a, -b)$ inversion design
- Already well-cited in color science

**Access:** APA PsycNet subscription or university library  
**Action:** Request via library access  
**Relevant to:** Section 7 (Möbius theoretical foundation)

---

### 12. MacAdam (1942) - Visual Sensitivities to Color Differences 📚 CLASSIC
**Citation:** *Journal of the Optical Society of America*, 32(5), pp. 247-274  
**DOI:** 10.1364/JOSA.32.000247  
**Why Medium Priority:**
- Classic JND data (25,000 color matching trials)
- MacAdam ellipses define anisotropic thresholds
- Comparison baseline for modern studies

**Access:** OSA subscription or library  
**Action:** Request via library access  
**Relevant to:** Section 2 (JND definition), Appendix (Historical context)

---

### 13. Resnikoff (1974) - Differential Geometry and Color Perception
**Citation:** *Journal of Mathematical Biology*, 1(2), pp. 97-131  
**DOI:** 10.1007/BF00275798  
**Why Medium Priority:**
- Elegant geometric model for color space
- Homogeneous space structures
- Riemannian framework foundations

**Access:** Springer subscription or library  
**Action:** Request via library access  
**Relevant to:** Section 4 (Topology), Appendix (Geometric foundations)

---

### 14. Shepard (1964) - Circularity in Judgments of Relative Pitch
**Citation:** *Journal of the Acoustical Society of America*, 36(12), pp. 2346-2353  
**DOI:** 10.1121/1.1919362  
**Why Medium Priority:**
- Cross-modal analogy: hue = pitch class (circular)
- Shepard tone paradox applicable to chromatic Shepard analogue
- Validates circular dimension concept

**Access:** JASA subscription or library  
**Action:** Request via library access  
**Relevant to:** Section 4 (Circular topology), Section 7 (Infinite rotation illusion)

---

### 15. Hindy et al. (2016) - Pattern Completion and Predictive Coding
**Citation:** *Nature Neuroscience*, 19(5), pp. 665-667  
**DOI:** 10.1038/nn.4284  
**Why Medium Priority:**
- Memory-based expectations in visual cortex
- Pattern completion mechanism
- Explains "return with difference" perception

**Access:** Nature Neuroscience subscription  
**Action:** Request via library access  
**Relevant to:** Section 7 (Möbius perception), cognitive foundations

---

## 🟢 LOW PRIORITY - Supplementary Context

### 16. Wertheimer (1912) - Experimentelle Studien über das Sehen von Bewegung
**Citation:** *Zeitschrift für Psychologie*, 61, pp. 161-265  
**Why Low Priority:**
- Foundational Gestalt apparent motion
- Historical context for temporal perception
- Already well-understood concept

**Access:** Archive.org has related documents  
**Action:** Optional historical reference  
**Relevant to:** Section 2 (Temporal perception), historical context

---

### 17. Bregman (1990) - Auditory Scene Analysis
**Citation:** *MIT Press*, ISBN: 978-0-262-52195-6  
**Why Low Priority:**
- Cross-modal analogy (color streams vs. sound streams)
- Temporal segmentation principles
- Supplementary theoretical framework

**Access:** MIT Press (book purchase or library)  
**Action:** Optional if pursuing cross-modal analogies  
**Relevant to:** Section 7 (Journey as "color stream")

---

## 📊 Summary by Priority & Completion Status

| Priority | Papers | Status | Total | Completion |
|----------|--------|--------|-------|-----------|
| 🔴 Critical | 7 collected PDFs | ✅ ALL INTEGRATED | 7 | 100% |
| 🟠 High | 4 papers needed | ✅ ALL FOUND & INTEGRATED | 4 | 100% |
| 🟡 Medium | 5 classic papers | ⏳ Requires library access | 5 | 0% |
| 🟢 Low | 2 supplementary | ⏳ Optional reading | 2 | 0% |
| **TOTAL** | | | **18** | **61%** |

### 🎉 Completed Integration Summary

**CRITICAL (🔴) - 100% COMPLETE:**
- ✅ 1. Fairchild (2013) - *Color Appearance Models* - Section 1 (Chromatic Adaptation)
- ✅ 2. Walmsley et al. (2015) - *Colour as Circadian Signal* - Section 3 (Natural cycles)
- ✅ 3. Braun et al. (2017) - *Visual Sensitivity in Eye Movements* - Section 2 (Temporal dynamics)
- ✅ 4. Süsstrunk (2005) - *Computing Chromatic Adaptation* - Section 1 (CAT methodology)
- ✅ 5. Troost (1992) - *Color Constancy Theory* - Section 3 (Perceptual foundations)
- ✅ 6. Wang et al. (2022) - *Rotation Gains & Limitations* - Section 7 (Closure thresholds)
- ✅ 7. Gao et al. (2020) - *von Kries Transform Generalization* - Section 6 (Mathematical framework)

**HIGH PRIORITY (🟠) - 100% COMPLETE:**
- ✅ 8. Hong et al. (2024) - *Comprehensive Color Discrimination Thresholds* - Section 1A (State-of-art JND measurements)
- ✅ 9. Schrödinger (1920)/Roberti & Peruzzi (2023) - *Helmholtz Legacy in Color Metrics* - Section 6.2 (Riemannian geometry foundation)
- ✅ 10. Sekulovski et al. (2007) - *Smoothness & Flicker of Temporal Transitions* - Section 2.1 (10:1 asymmetry quantified)
- ✅ 11. Fechner (1860) - *Elements of Psychophysics* - Section 6.4 (Weber-Fechner law, fundamental/measurement formulas)

---

## 🎯 Recommended Reading Order - UPDATED

### ✅ COMPLETED (Already in M1-M4 artifacts)
1. ✅ Fairchild (2013), Chapter 8-9 (Chromatic Adaptation)
2. ✅ Walmsley et al. (2015) - Circadian twilight cycles
3. ✅ Braun et al. (2017) - Temporal dynamics during smooth pursuit
4. ✅ Gao et al. (2020) - Mathematical foundations of CAT
5. ✅ Süsstrunk (2005) - CAT implementation details
6. ✅ Wang et al. (2022) - Psychometric methodology for closure
7. ✅ Troost (1992) - Color constancy theory
8. ✅ Hong et al. (2024) - Comprehensive discrimination thresholds
9. ✅ Schrödinger (1920)/Roberti & Peruzzi (2023) - Riemannian color space geometry
10. ✅ Sekulovski et al. (2007) - Temporal transition smoothness (10:1 asymmetry)
11. ✅ Fechner (1860) - Weber-Fechner law, foundational psychophysics framework

### ⏳ PENDING (Library access required)
12. Hurvich & Jameson (1957) - Opponent-process theory (APA PsycNet)
13. MacAdam (1942) - JND ellipses (OSA subscription)
14. Resnikoff (1974) - Differential geometry of color (Springer)
15. Shepard (1964) - Pitch circularity analogy (JASA)
16. Hindy et al. (2016) - Pattern completion (Nature Neuroscience)

---

## 🔍 Outstanding Research Questions

Papers on this list should help answer:

1. **What is the minimum smooth transition duration for chromatic inversion?**  
   → ✅ Sekulovski et al. (2007) - **FOUND & EXTRACTED**: 10:1 asymmetry (luminance:chromaticity)

2. **What is the geodesic path for 180° hue rotation in OKLab?**  
   → eLife (2024) thresholds + Resnikoff (1974) geometry

3. **What is acceptable ΔE at loop closure for "seamless" perception?**  
   → MacAdam (1942) + eLife (2024) + User studies

4. **How does chromatic inversion affect color memory over 2-4 seconds?**  
   → Troost (1992) adaptation + Wang et al. (2022) methodology

5. **Is blue-yellow axis inversion more perceptually salient than red-green?**  
   → Walmsley et al. (2015) + Hurvich & Jameson (1957)

---

## 📝 Notes

- Papers marked 📚 are already downloaded
- Papers marked ⚠️ need immediate action
- Papers marked 🔴 are critical missing pieces
- DOIs provided for all papers where available
- File locations use relative paths from `open-agents/source/reference-materials/`

---

**Last Updated:** 2024-12-18  
**Maintained by:** Research Librarian Agent (Ellis)
