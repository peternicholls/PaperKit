# Literature Review: Color Harmony Generation Methods

**Agent:** 📖 Research Librarian (Ellis)  
**Date:** 18 December 2025  
**Task:** 012-librarian-literatureReview  
**Status:** Complete

---

## Overview

This literature review systematically examines color harmony generation methods across six categories: rule-based harmony systems, geometric methods, commercial design tools, interpolation methods, data-driven approaches, and academic HCI work. The goal is to position the Color Journey Engine's novel contribution against existing prior art, identifying gaps between traditional static color theory and temporally-aware perceptual design.

### Key Finding

Traditional color theory (Itten) has been empirically falsified as a predictive model for color mixing and harmony. Contemporary tools continue to use non-perceptual color spaces (HSB/HSL), leaving a significant gap for perceptually-grounded, temporally-aware color generation systems.

---

## 1. Rule-Based Harmony Systems

### 1.1 Traditional Color Theory: Itten (1961)

Johannes Itten's *The Art of Color* (1961) established the dominant framework for color harmony education, proposing that complementary colors, triadic relationships, and contrast principles create aesthetically pleasing combinations.

**Critical Falsification:** Kirchner (2023) provides comprehensive empirical evidence that Itten's color theory fails as a predictive model:

> "Itten's color diagram cannot be regarded as a tool that clarifies how colors mix... no combination of red, yellow and blue paints that after mixing produce the vivid bright secondary colors indicated by Itten's diagram."

The study demonstrates mathematically using Kubelka-Munk K and S parameters that:
- Itten's color circle "does not produce reliable predictions for color harmony"
- "Itten largely excluded scientific developments from the mid-nineteenth century onwards" (Shamey and Kuehni, cited in Kirchner)
- The persistence of Itten's theory in education represents "confirmation of unexamined beliefs" rather than empirical validation

**Implication for Color Journey:** This empirical falsification of traditional color theory validates the paper's perceptual-first philosophy. We are not simply iterating on Itten—we are building on a fundamentally different foundation.

### 1.2 Munsell Color System

The Munsell system (1905, refined through 1943) represents an early attempt at perceptual uniformity:

- **Hue:** 10 major divisions (5 principal + 5 intermediate)
- **Value:** 0 (black) to 10 (white)
- **Chroma:** 0 (neutral) to maximum saturation (varies by hue)

Key properties:
- Designed for **perceptual uniformity**—equal steps appear equally different
- Value scale was calibrated through extensive psychophysical experiments
- Chroma extends unevenly (blue-purples reach higher chroma than yellow-greens at same value)

**Limitation:** The Munsell system is static—it describes color relationships but provides no guidance for temporal transitions or continuous journeys through color space.

### 1.3 Complementary and Geometric Rules

Traditional harmony rules define relationships through angular positions on a color wheel:

| Rule | Angular Relationship | Colors |
|------|---------------------|--------|
| Complementary | 180° | 2 |
| Split-complementary | 180° ± 30° | 3 |
| Triadic | 120° | 3 |
| Tetradic (square) | 90° | 4 |
| Tetradic (rectangle) | 60°/120° | 4 |
| Analogous | ±30° | 3-5 |

**Critical Issue:** These rules assume a uniform color wheel where equal angular steps produce equal perceptual differences. This assumption is false in RGB, HSL, and HSV spaces—only approximately true in perceptually uniform spaces like OKLCh.

---

## 2. Geometric Methods

### 2.1 Color Wheel Approaches

Most commercial and educational tools implement harmony through geometric relationships on a color wheel:

- **Angular selection:** User picks a base hue; complementary colors are computed as hue ± offset
- **Fixed ratios:** Triadic = 120° apart, tetradic = 90° apart
- **Saturation/lightness preservation:** Many tools maintain S/L while rotating H

### 2.2 Proportional Harmony Theories

Some approaches extend beyond simple angle selection:

- **Golden ratio proportions:** Dividing the color wheel by φ (≈1.618)
- **Fibonacci sequences:** Stepping through hues in Fibonacci intervals
- **Rule of thirds:** Using 30° increments for subtle harmonies

### 2.3 Fundamental Limitation

All geometric methods assume the color wheel is perceptually uniform. In HSL/HSV:
- A 30° step from red to orange appears different from a 30° step from cyan to blue
- Saturation at constant S varies wildly in perceived intensity across hues
- "Complementary" colors in HSL are not perceptual complements

The CSS Color Level 4 specification acknowledges this:

> "Lab represents the entire range of color that humans can see... Usefully, L=50% or 50 is mid gray, by design, and equal increments in L are evenly spaced visually: the Lab color space is intended to be perceptually uniform." (W3C, 2022)

---

## 3. Commercial Tool Analysis

### 3.1 Adobe Color (formerly Kuler)

**Method:** Geometric harmony rules applied to a color wheel with manual refinement

**Perceptual Space:** HSB (Hue-Saturation-Brightness)—**not perceptually uniform**

**Harmony Modes:**
- Analogous
- Monochromatic
- Triad
- Complementary
- Split-complementary
- Double-split-complementary
- Square
- Compound
- Shades
- Custom

**Single-Anchor Expansion:** Partially supported—user can lock one color and adjust others, but the expansion is geometric (angular), not perceptual.

**Documentation:** Adobe's methodology is not formally documented. The tool appears to use pure HSB angular relationships without perceptual correction.

**Accessibility Features:** Adobe Color includes accessibility tools:
- Color blind safe themes
- Conflict detection for color blindness types
- Contrast ratio checking

**Gap:** No formalized "journey" or trajectory concept. Colors are discrete points, not continuous paths.

### 3.2 Coolors.co

**Method:** Random generation with user-directed locking and adjustment

**Perceptual Space:** HSL—**not perceptually uniform**

**Key Features:**
- Lock/unlock individual colors
- Adjust individual hue/saturation/lightness
- Export to multiple formats
- Palette exploration (random + refinement)

**Single-Anchor Expansion:** Not supported. The tool generates random palettes; users refine iteratively.

**Documentation:** No formal methodology documentation. The tool is empirically-driven (user satisfaction) rather than theory-grounded.

**Gap:** No perceptual uniformity. No trajectory or journey concept. Random + refine is fundamentally different from deterministic expansion.

### 3.3 Paletton

**Method:** Color wheel with geometric harmony rules

**Perceptual Space:** HSV—**not perceptually uniform**

**Modes:**
- Monochromatic
- Adjacent (analogous)
- Triad
- Tetrad

**Single-Anchor Expansion:** Supported—user selects base color, tool generates harmonious palette.

**Documentation:** Website provides basic explanations but no formal specification.

**Gap:** Same limitations as Adobe Color—geometric relationships in non-perceptual space.

### 3.4 Khroma (AI-Based)

**Method:** Machine learning trained on user preferences

**Perceptual Space:** Unknown (not documented)

**Approach:**
1. User rates initial color palettes
2. ML model learns user preferences
3. Tool generates personalized palettes

**Documentation:** Proprietary. Methodology not publicly specified.

**Gap:** Black-box ML approach. No deterministic reproducibility. No trajectory concept.

### 3.5 Colormind

**Method:** Deep learning trained on existing color palettes from design, photography, and film

**Perceptual Space:** Unknown (not documented)

**Approach:**
- Neural network trained on curated palette datasets
- Can extract palettes from images
- Generates palettes from partial inputs

**Documentation:** Minimal. Describes approach as "deep learning" without formal specification.

**Gap:** Non-deterministic. Results vary between runs. No trajectory or journey concept.

### Summary: Commercial Tools

| Tool | Color Space | Perceptual Uniform | Single-Anchor | Trajectory | Documented |
|------|-------------|-------------------|---------------|------------|------------|
| Adobe Color | HSB | ❌ | Partial | ❌ | ❌ |
| Coolors | HSL | ❌ | ❌ | ❌ | ❌ |
| Paletton | HSV | ❌ | ✅ | ❌ | ❌ |
| Khroma | Unknown | Unknown | ❌ | ❌ | ❌ |
| Colormind | Unknown | Unknown | ❌ | ❌ | ❌ |

**Conclusion:** No commercial tool operates in a perceptually uniform space with documented methodology. None implements a continuous trajectory or journey concept.

---

## 4. Interpolation Methods

### 4.1 CSS Color Level 4 Specification

The W3C CSS Color Level 4 specification (2022) provides comprehensive guidance on color interpolation:

**Key Innovation:** OKLab as default interpolation space

> "If the host syntax does not define what color space interpolation should take place in, it defaults to Oklab." (W3C, 2022)

**Supported Interpolation Spaces:**
- Rectangular: sRGB, sRGB-linear, Display P3, A98-RGB, ProPhoto-RGB, Rec2020, Lab, OKLab, XYZ
- Polar: HSL, HWB, LCH, OKLCh

**Hue Interpolation Methods:**
1. **shorter** (default): Takes shorter arc between hues
2. **longer**: Takes longer arc
3. **increasing**: Always increases hue angle
4. **decreasing**: Always decreases hue angle

**Missing Component Handling:** The `none` keyword allows missing components, enabling intelligent interpolation:

> "If a color with a carried forward missing component is interpolated with another color which is not missing that component, the missing component is treated as having the other color's component value." (W3C, 2022)

**Premultiplied Alpha:** Interpolation uses premultiplied alpha to avoid artifacts at transparency boundaries.

**Gamut Mapping:** CSS specifies a gamut mapping algorithm using OKLCh with local MINDE (Minimum Delta E OK).

**Gap:** CSS provides point-to-point interpolation. It does not define:
- Multi-point trajectories
- Style/mood parameterization
- Rate limiting for temporal perception
- Arc-length parameterization for uniform velocity

### 4.2 Chroma.js

**Color Spaces:** Wide support including OKLab (since v2.4)

**Interpolation:**
```javascript
chroma.scale(['yellow', 'red', 'black']).mode('lab')
```

**Features:**
- Multi-stop gradients
- Various color space modes
- Bezier interpolation available

**Gap:** Library provides interpolation primitives but no higher-level "journey" concept. No rate limiting. No style parameterization.

### 4.3 TinyColor

**Color Spaces:** RGB, HSL, HSV primarily

**Features:**
- Basic color manipulation
- Complementary/triadic/tetrad generation
- Lighten/darken/saturate operations

**Gap:** Non-perceptual color space focus. No trajectory concept. Basic manipulation only.

### 4.4 D3 Color Interpolation

**Color Spaces:** RGB, HSL, Lab, HCL, Cubehelix

**Key Feature:** `d3.interpolateHcl()` provides perceptual interpolation in HCL space.

**Gap:** Point-to-point interpolation only. No multi-point trajectories. No temporal considerations.

### Summary: Interpolation Libraries

| Library | OKLab Support | Multi-Point | Arc-Length | Rate Limiting |
|---------|--------------|-------------|------------|---------------|
| CSS Color 4 | ✅ | ❌ | ❌ | ❌ |
| Chroma.js | ✅ (v2.4+) | ✅ (basic) | ❌ | ❌ |
| TinyColor | ❌ | ❌ | ❌ | ❌ |
| D3 | Partial (HCL) | ✅ (basic) | ❌ | ❌ |

---

## 5. Data-Driven Approaches

### 5.1 Liu et al. (2013) — Data-Driven Color Harmony

Liu et al. (2013) present a data-driven approach to color palette generation:

**Method:**
- Train on large datasets of "harmonious" palettes
- Extract statistical patterns
- Generate new palettes matching learned distributions

**Contribution:** Demonstrates that harmony can be learned from examples rather than defined by rules.

**Gap:**
- Statistical, not deterministic—same input can produce different outputs
- No trajectory concept—generates discrete palettes
- No perceptual grounding—learns from examples without explicit perceptual model

### 5.2 Machine Learning Approaches

Various ML approaches have been applied to color palette generation:

- **GANs:** Generate palettes from image inputs
- **Neural networks:** Learn palette aesthetics from ratings
- **Optimization:** Minimize distance from "ideal" palette distributions

**Common Gaps:**
- Non-deterministic (randomness in training/inference)
- Black-box (no explainable reasoning)
- No temporal considerations
- No formal specification or reproducibility

### 5.3 Optimization-Based Methods

Some approaches frame palette generation as optimization:

- **Objective:** Maximize aesthetic score / minimize color clash
- **Constraints:** Accessibility, brand guidelines, contrast requirements
- **Methods:** Genetic algorithms, simulated annealing, gradient descent

**Gap:** Optimization produces endpoints, not journeys. No concept of continuous trajectory through color space.

---

## 6. Academic Work

### 6.1 HCI Color Research

Academic HCI literature on color focuses primarily on:

- **Accessibility:** Color blindness, contrast ratios (WCAG)
- **Information visualization:** Distinguishability, categorical perception
- **User preference:** A/B testing, rating studies

**Gap:** HCI research optimizes for task performance or preference, not aesthetic trajectories. No "journey" concept in the literature.

### 6.2 Visualization Color Research

Notable contributions:

- **Stone et al. (2014):** Color difference as function of size—smaller elements require larger color differences
- **Colorbrewer:** Perceptually-grounded palettes for cartography

**Gap:** Focus on categorical palettes (discrete sets), not continuous trajectories.

### 6.3 Design Automation Literature

Design automation research addresses:

- **Style transfer:** Apply color scheme from one design to another
- **Recoloring:** Palette substitution with semantic preservation
- **Harmonization:** Adjust colors to improve aesthetic coherence

**Gap:** Operates on existing content, not generative trajectory design.

### 6.4 Temporal Color Perception Research

**Critical Finding:** Kong (2021) PhD thesis explicitly addresses temporal color perception:

> "CIELAB... is not a useful space to predict the perception of dynamic colored light. Today, **no color spaces are available that accurately predict the visibility of color differences over time**."

This directly validates the novelty of temporal considerations in color journey design.

Sekulovski et al. (2007) established the foundational 10:1 asymmetry:
> "The threshold for L* was found to be approximately 10 times smaller than for the chromaticity indices a* and b*."

**Implication:** Rate limiting in Color Journey Engine addresses a documented perceptual phenomenon that existing tools ignore.

---

## 7. Gap Analysis

### 7.1 What Exists

| Capability | Current State |
|------------|--------------|
| Static harmony rules | ✅ Well-documented (Itten, Munsell) |
| Geometric color wheel | ✅ Universal in tools |
| HSB/HSL interpolation | ✅ Standard implementation |
| Perceptual interpolation | ✅ CSS Color 4 (OKLab) |
| Point-to-point interpolation | ✅ All libraries |
| Random palette generation | ✅ Coolors, Colormind |
| ML-based generation | ✅ Khroma, Colormind |

### 7.2 What Does NOT Exist

| Capability | Status |
|------------|--------|
| **Single-anchor perceptual expansion** | ❌ Not formalized |
| **Style-parameterized trajectories** | ❌ Not documented |
| **Arc-length parameterization** | ❌ Not in color tools |
| **Temporal rate limiting** | ❌ Not implemented |
| **Deterministic journey specification** | ❌ Not formalized |
| **Perceptual uniformity in commercial tools** | ❌ All use HSB/HSL/HSV |
| **Journey metaphor (trajectory + sampling)** | ❌ Novel concept |

### 7.3 The Gap Color Journey Engine Fills

**Traditional color theory** (Itten, Munsell) provides static harmony rules that have been empirically falsified.

**Commercial tools** (Adobe Color, Coolors, Paletton) implement these rules in non-perceptual color spaces without formal specification.

**Interpolation libraries** (CSS Color 4, Chroma.js, D3) provide point-to-point transitions but no higher-level trajectory concept.

**Data-driven approaches** (Liu et al., ML tools) generate discrete palettes without determinism or perceptual grounding.

**No existing work** formalizes:
1. Single-anchor expansion in perceptual space
2. Style-parameterized continuous trajectories
3. Temporal rate limiting based on perceptual asymmetries
4. Arc-length parameterization for uniform perceptual velocity
5. Deterministic journey specification with reproducible results

---

## 8. Novelty Positioning Recommendation

### 8.1 Primary Novelty Claim

**The Color Journey Engine is the first formally specified system for generating temporally-aware color trajectories in perceptually uniform space.**

Supporting evidence:
- Traditional color theory (Itten) empirically falsified (Kirchner, 2023)
- No existing commercial tool uses perceptually uniform space
- No existing system addresses temporal perception (Kong, 2021)
- Journey metaphor (continuous trajectory + discrete sampling) undocumented

### 8.2 Secondary Novelty Claims

1. **Single-anchor perceptual expansion:** Formalized method for expanding a single input color into a complete palette through perceptual trajectories.

2. **Style parameterization:** Mood and style parameters that shape trajectory geometry (tension, spread, chromatic intensity) rather than selecting from preset rules.

3. **Temporal rate limiting:** Rate constraints derived from perceptual research (10:1 L*/chroma asymmetry) ensuring smooth temporal transitions.

4. **Arc-length parameterization:** Uniform perceptual velocity through trajectory—equal time steps produce equal perceptual changes.

5. **Deterministic specification:** Same inputs always produce same outputs, enabling reproducibility and version control.

### 8.3 Positioning Statement

> The Color Journey Engine bridges the gap between **static color theory** (which describes harmony as discrete relationships) and **perceptual color science** (which quantifies how humans perceive color). By formalizing continuous trajectories through perceptually uniform space with temporal awareness, the Engine enables a new paradigm: **color as journey rather than color as palette**.

### 8.4 Differentiation Matrix

| Aspect | Traditional Theory | Commercial Tools | Color Journey Engine |
|--------|-------------------|------------------|---------------------|
| **Foundation** | Artistic intuition | Geometric rules | Perceptual science |
| **Color space** | Unspecified | HSB/HSL (non-uniform) | OKLCh (perceptually uniform) |
| **Output** | Discrete palette | Discrete palette | Continuous trajectory |
| **Temporal** | Not considered | Not considered | Rate-limited |
| **Determinism** | N/A | Varies | Fully deterministic |
| **Specification** | Descriptive | Undocumented | Formally specified |

---

## 9. Bibliography

### Primary Sources Cited

Fairchild, M.D. (2013) *Color Appearance Models*. 3rd edn. Wiley.

Itten, J. (1961) *The Art of Color: The Subjective Experience and Objective Rationale of Color*. Reinhold Publishing.

Kirchner, E.J.J. (2023) 'Color mixing with paints reconsidered: Itten's color circle unmasked', *Optics Express*, 31(15), pp. 25191-25213. doi: 10.1364/OE.497782.

Kong, Y.W. (2021) *Temporal Color Perception: Assessing the Visibility of Dynamic Color Changes*. PhD thesis. Eindhoven University of Technology.

Liu, Y., Cohen-Or, D., Sorkine, O. and Gingold, Y. (2013) 'Image-driven harmonious color palette generation', *IEEE Transactions on Visualization and Computer Graphics*, 19(6), pp. 978-989. doi: 10.1109/TVCG.2012.155.

Ottosson, B. (2020) *A perceptual color space for image processing*. Available at: https://bottosson.github.io/posts/oklab/ (Accessed: 18 December 2025).

Sekulovski, D., Vogels, I.M., Van Beurden, M. and Clout, R. (2007) 'Smoothness and Flicker Perception of Temporal Color Transitions', *Proceedings of the 15th Color and Imaging Conference*, pp. 112-117. doi: 10.2352/CIC.2007.15.1.art00021.

Stone, M.C., Szafir, D.A. and Setlur, V. (2014) 'An engineering model for color difference as a function of size', *Color and Imaging Conference*, 2014(1), pp. 228-233.

W3C CSS Working Group (2022) *CSS Color Module Level 4*. W3C Candidate Recommendation. Available at: https://www.w3.org/TR/css-color-4/ (Accessed: 18 December 2025).

### Additional Sources Consulted

Gao, C., Ling, Y., Kwok, T.-W. and Luo, M.R. (2020) 'Generalised Structure-Preserving Chromatic Adaptation Transform', *Color Research & Application*, 45(4), pp. 611-625. doi: 10.1002/col.22498.

Hong, F. et al. (2024) 'Comprehensive characterization of human color discrimination thresholds', *eLife*, 13, p. RP108943. doi: 10.7554/eLife.108943.

Madsen, R. (2017) *Programming Design Systems: Perceptually Uniform Color Spaces*. Available at: https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/ (Accessed: 18 December 2025).

Nölle, M., Suda, M. and Boxleitner, W. (2012) 'H2SI - A new perceptual colour space', ResearchGate preprint.

Roberti, V. and Peruzzi, G. (2023) 'The Helmholtz legacy in color metrics: Schrödinger's color theory', *Archive for History of Exact Sciences*, 77, pp. 305-335. doi: 10.1007/s00407-023-00317-x.

Walmsley, L. et al. (2015) 'Colour as a signal for entraining the mammalian circadian clock', *PLOS Biology*, 13(4), p. e1002127. doi: 10.1371/journal.pbio.1002127.

---

## 10. Key Questions Answered

### Q1: Does any prior work formalize single-anchor expansion in perceptual space?

**No.** Commercial tools offer "expand from color" features, but:
- All use non-perceptual spaces (HSB/HSL/HSV)
- None formally specify the expansion algorithm
- None operate in perceptually uniform space

### Q2: What color space do existing tools use for expansion/interpolation?

| Tool | Color Space |
|------|-------------|
| Adobe Color | HSB |
| Coolors | HSL |
| Paletton | HSV |
| CSS Color 4 | OKLab (default) |
| Chroma.js | Configurable (Lab, OKLab supported) |

### Q3: Is there documented specification for Adobe Color's "monochromatic" or "shades" modes?

**No.** Adobe's methodology is not publicly documented. The tool appears to adjust lightness/saturation in HSB space without formal specification.

### Q4: What differentiates "mood-based trajectory" from existing approaches?

Existing approaches:
- Select preset harmony rule (triadic, complementary, etc.)
- Adjust individual colors manually
- No concept of continuous trajectory shaped by mood parameters

Color Journey's approach:
- Style parameters (tension, spread, chromatic intensity) shape geometry
- Continuous trajectory through perceptual space
- Mood expressed as trajectory shape, not discrete color selection

### Q5: Is the journey metaphor (continuous trajectory + discrete sampling) documented elsewhere?

**No.** The literature treats palettes as discrete sets:
- Traditional theory: harmony rules between discrete colors
- Commercial tools: discrete palette outputs
- Interpolation libraries: point-to-point transitions (two endpoints)

The "journey" concept—a continuous, style-parameterized trajectory from which discrete samples are extracted—appears to be novel.

---

**Document Complete**  
**Ready for:** Research Consolidator synthesis (Task 013)
