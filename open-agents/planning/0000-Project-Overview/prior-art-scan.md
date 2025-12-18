# Prior Art & Positioning Scan

**Status:** In Progress  
**Last updated:** 2025-12-17  
**Purpose:** Map existing approaches to position Color Journey Engine novelty

## Scan Areas

### 1. Perceptual Color Spaces (OKLab)

**What We Need:**
- Industry adoption evidence (Adobe, CSS, etc.)
- Comparison with CIELAB, CIEDE2000
- Rationale for OKLab choice

**Open Sources:**
- [x] **Björn Ottosson's blog** — https://bottosson.github.io/posts/oklab/
  - Primary source for OKLab derivation and rationale
  - Explains why CIELAB has hue linearity problems
  - Provides conversion formulas (sRGB ↔ OKLab)
  - **2025 Update:** Now industry standard—Photoshop default for gradients, CSS Color 4/5, Unity, Godot
  - *Cite as: Ottosson, B. (2020). A perceptual color space for image processing.*
  
- [x] **CSS Color Module Level 4** — https://www.w3.org/TR/css-color-4/
  - W3C Recommendation (official web standard)
  - §9 defines OKLab and OKLCH as standard CSS color spaces
  - §12 covers gamut mapping (relevant for §8)
  - *Cite as: W3C. (2022). CSS Color Module Level 4.*

- [x] **CSS Color Module Level 5** — https://www.w3.org/TR/css-color-5/
  - Working draft with color mixing in OKLab
  - `color-mix()` function uses OKLab by default
  - Validates industry direction
  
- [x] **Adobe Photoshop** — OKLab now default interpolation for gradients (as of 2024+)
  - No native OKLab picker yet, but gradient tool uses it
  - Adobe Exchange plugins: "Color Designer Pro" adds OKLCH support
  - *Evidence of adoption, not primary citation*

- [x] **Adobe Leonardo** — https://leonardocolor.io/
  - Open-source contrast-based color generator from Adobe Spectrum team
  - Uses perceptually uniform color spaces for accessible palette generation
  - *Cite as: Baldwin, N. Leonardo: an open source contrast-based color generator.*

- [x] **Figma** — No native OKLab support yet (as of 2025)
  - Community plugins: "OK Palette", "OkColor" enable OKLCH workflows
  - Feature requests show strong community demand
  - *Evidence of adoption gap + community workarounds*

- [x] **Raph Levien's OKLab critique** — https://raphlinus.github.io/color/2021/01/18/oklab-critique.html
  - Independent technical review of OKLab
  - Validates perceptual uniformity claims for gradients
  - *Cite as: Levien, R. (2021). An interactive review of Oklab.*

**Key Points to Extract:**
- ✅ OKLab designed specifically for perceptual uniformity
- ✅ CIELAB has hue shifts (blue→purple problem) that OKLab fixes
- ✅ W3C adoption = industry validation
- ✅ CSS default for mixing = momentum

**Quotable for Paper:**
> "OKLab was designed with the goal of [...] having the property that the perceived color difference between two colors is approximately proportional to their Euclidean distance in the color space." — Ottosson (2020)

---

### 2. Palette Generation Approaches

**What We Need:**
- Traditional methods (complementary, analogous, triadic)
- Modern tools and their approaches
- What makes journey metaphor different

**Open Sources:**
- [x] **Color theory (public domain)** — Johannes Itten, Josef Albers
  - Traditional harmony rules: complementary, analogous, triadic, split-complementary
  - Based on color wheel position, not perceptual distance
  - No guarantee of distinguishability or uniformity
  
- [x] **Coolors** — https://coolors.co/
  - Random generation + locking
  - No explicit perceptual model
  - "Explore" uses trending/popular palettes
  
- [x] **Adobe Color** — https://color.adobe.com/
  - Harmony rules (complementary, analogous, etc.)
  - Works in HSB, not perceptually uniform
  - Accessibility checker (separate from generation)
  
- [x] **Paletton** — https://paletton.com/
  - HSV-based color wheel
  - Geometric relationships
  - No perceptual uniformity
  
- [x] **Chroma.js** — https://gka.github.io/chroma.js/
  - Interpolation library (including OKLab since v2.4)
  - Scale/gradient generation
  - Linear interpolation, not path construction

- [x] **Programming Design Systems** — https://programmingdesignsystems.com/color/perceptually-uniform-color-spaces/
  - Free online book chapter on perceptually uniform color spaces
  - Explains why working with color in code differs from design tools
  - *Good for positioning our approach*

- [x] **Colormoo thesis** — Claremont scholarship
  - Academic thesis: "An Algorithmic Approach to Generating Color Palettes"
  - Implements three algorithms from starting color
  - *Potential comparator for single-anchor approaches*

- [x] **IEEE TVCG paper** — Liu et al. "Image-Driven Harmonious Color Palette Generation"
  - Uses saliency-hue clustering + harmony optimization in lightness-chroma plane
  - Academic approach to palette generation
  - *Contrast: data-driven vs. our deterministic path approach*

**Key Points to Extract:**
- ✅ Traditional tools use geometric relationships on color wheels
- ✅ Most work in HSL/HSV (not perceptually uniform)
- ✅ Interpolation tools create gradients, not discrete palettes with constraints
- ✅ None use continuous path construction + discrete constrained sampling
- ✅ None have "mood expansion" from single anchor
- ✅ Academic approaches tend toward data-driven/ML methods

**Positioning Statement:**
> Unlike traditional palette generators that use predefined geometric relationships (complementary, analogous) or simple linear interpolation, the Color Journey Engine constructs continuous Bézier paths through perceptually-uniform OKLab space, then samples discretely with JND-based constraints ensuring distinguishability and coherence.

---

### 3. Bézier Curves in Color

**What We Need:**
- Standard usage (gradients, transitions)
- What's different about our application
- Arc-length parameterization methods

**Open Sources:**
- [x] **SVG 2 Specification** — https://www.w3.org/TR/SVG2/paths.html
  - Cubic Bézier path commands (C, S)
  - Mathematical definition: $B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$
  - Standard reference for curve mathematics
  
- [x] **CSS Images Module Level 4** — https://www.w3.org/TR/css-images-4/
  - Gradient interpolation
  - `color-interpolation-method` (OKLab support)
  - Gradients are continuous output, not discrete sampling
  
- [x] **A Primer on Bézier Curves** — https://pomax.github.io/bezierinfo/
  - Free online book, comprehensive
  - Arc-length parameterization explained (§14)
  - *Cite as: Kamermans, M. A Primer on Bézier Curves.*

- [x] **Raph Levien on Bézier arc-length** — https://raphlinus.github.io/curves/2018/12/28/bezier-arclength.html
  - "How long is that Bézier?" — practical algorithms
  - Sample + sum distances approach
  - *Technical implementation reference*

- [x] **Observable: Bézier Segment Arclength** — https://observablehq.com/@jrus/bezier-segment-arclength
  - Interactive demonstration of arc-length vs. parameter-based sampling
  - Shows uniform speed (arc-length) vs. non-uniform (parameter)
  - *Visual teaching resource*

**Key Points to Extract:**
- ✅ Bézier curves standard for smooth paths in graphics
- ✅ Arc-length parameterization needed for uniform sampling (not default)
- ✅ Gradients output continuous color; we output discrete swatches
- ✅ Application to palette generation (discrete + constrained) is novel
- ✅ Standard algorithms exist for arc-length computation

---

### 4. Gamut Mapping

**What We Need:**
- Standard approaches to out-of-gamut colors
- Why hue preservation matters
- CSS and library implementations

**Open Sources:**
- [x] **CSS Color Level 4 §12** — https://www.w3.org/TR/css-color-4/#gamut-mapping
  - Defines CSS gamut mapping algorithm
  - Uses OKLCH, reduces chroma to fit gamut
  - Preserves hue and lightness (same as our approach!)
  - *Cite as: W3C. (2022). CSS Color Module Level 4, §12.*

- [x] **Color.js Gamut Mapping** — https://colorjs.io/docs/gamut-mapping.html
  - Library implementing CSS gamut mapping
  - Explains chroma reduction approach
  - Documents why hue preservation matters
  - Default "css" method: binary search in OKLCH with JND threshold
  - *Cite as: Verou, L. & Lilley, C. Color.js documentation.*

- [x] **W3C Color Workshop slides (Lilley)** — https://www.w3.org/Graphics/Color/Workshop/slides/talk/lilley
  - Chris Lilley's presentation on OKLCH gamut mapping
  - Explains why OKLab ΔE is simple Euclidean (fast)
  - References Morovič (2008) "Color Gamut Mapping" book
  - *Key background for gamut mapping design decisions*

- [x] **ColorAide gamut mapping** — https://facelessuser.github.io/coloraide/gamut/
  - Python library with multiple gamut mapping methods
  - Ray-tracing approach for RGB gamuts
  - Chroma reduction with JND thresholds
  - *Implementation reference*

- [x] **ICC profile documentation** — https://www.color.org/iccprofile.xalter
  - Four rendering intents (perceptual, saturation, relative/absolute colorimetric)
  - Industry standard for gamut mapping
  - *Cite as: ICC. Introduction to the ICC profile format.*

**Key Points to Extract:**
- ✅ CSS standard aligns with our approach (chroma reduction, hue preservation)
- ✅ Hard clipping destroys hue (well-documented problem)
- ✅ Two-layer approach (prevention + correction) is our specific contribution
- ✅ JND threshold (~2 ΔE) used in CSS algorithm for "close enough" clipping
- ✅ OKLab simplifies ΔE to Euclidean distance (performance benefit)

**Quotable for Paper:**
> "The CSS gamut mapping algorithm [...] reduces the chroma, while keeping the same hue and lightness." — CSS Color Level 4

---

### 5. Perceptual Spacing (JND)

**What We Need:**
- Just-Noticeable Difference thresholds
- Validation for Δ_min ~2 ΔE units

**Open Sources:**
- [x] **Ottosson OKLab post** — https://bottosson.github.io/posts/oklab/
  - States goal: "perceived color difference [...] proportional to Euclidean distance"
  - Implies JND ≈ 1 unit in OKLab for small differences
  - Our Δ_min ~2 provides safety margin
  
- [x] **W3C WCAG Techniques** — https://www.w3.org/WAI/WCAG21/Techniques/
  - Contrast ratios (different metric, but establishes "perceptible difference" matters)
  - G18: Ensuring contrast ratio of at least 4.5:1
  
- [x] **Color Difference (Wikipedia)** — https://en.wikipedia.org/wiki/Color_difference
  - Overview of ΔE metrics (CIE76, CIE94, CIEDE2000)
  - JND typically 1.0 ΔE for trained observers, 2-3 for average
  - *Use for background; cite primary sources where possible*

- [x] **Color.js JND in gamut mapping** — https://colorjs.io/docs/gamut-mapping.html
  - Uses deltaEOK (OKLab Euclidean) with threshold
  - Validates JND concept in practical implementation
  - CSS algorithm clips when ΔE < 0.02 (OKLab scale is 0-1, so ≈2 on 0-100 scale)

- [x] **Luo-Rigg dataset** — Referenced in Ottosson's blog
  - Experimental data on perceived color differences
  - Used to validate OKLab's uniformity claims
  - *Secondary reference through Ottosson*

**Key Points to Extract:**
- ✅ JND ~1 ΔE for trained observers, ~2-3 for average viewers
- ✅ Δ_min = 2 OKLab units provides reasonable distinguishability margin
- ✅ OKLab designed so Euclidean distance ≈ perceptual difference
- ✅ CSS gamut mapping uses similar threshold concept (ΔE < 0.02 in OKLab)

---

### 6. Determinism and PRNG (NEW)

**What We Need:**
- Standard approaches to deterministic randomness
- Seed-based reproducibility patterns
- Validation that our approach is standard practice

**Open Sources:**
- [x] **xoshiro/xoroshiro family** — Vigna & Blackman (2018)
  - Industry-standard fast PRNG algorithms
  - xoshiro128**, xoshiro256++ widely used
  - Passes PractRand tests
  - *Cite as: Blackman, D. & Vigna, S. (2021). Scrambled Linear Pseudorandom Number Generators.*

- [x] **Deterministic PRNG in games/graphics** — Common pattern
  - Procedural generation uses seeded PRNG for reproducibility
  - Avatar generators, map generation, etc.
  - *No single citation; established practice*

- [x] **JSF (Jenkins' Small Fast)** — Bob Jenkins (2007)
  - Alternative fast PRNG
  - Passes PractRand, used in many applications

**Key Points to Extract:**
- ✅ Seed-based determinism is standard practice for reproducibility
- ✅ Modern PRNGs (xoshiro, JSF) are fast and statistically robust
- ✅ Our approach follows established patterns

---

### 7. Color Harmony Theory (NEW)

**What We Need:**
- Traditional harmony rules for contrast
- Why we differ from geometric approaches

**Open Sources:**
- [x] **Interaction Design Foundation** — https://www.interaction-design.org/literature/topics/color-harmony
  - Overview of color harmony principles
  - Complementary, analogous, triadic, split-complementary
  - *Cite as: IxDF. Color Harmony.*

- [x] **Johannes Itten / Josef Albers** — Classic color theory (public domain)
  - Traditional harmony rules based on color wheel position
  - No perceptual distance guarantees
  - *Historical context*

- [x] **UX Matters: Color Theory for Digital Displays** — https://www.uxmatters.com/mt/archives/2006/01/color-theory-for-digital-displays-a-quick-reference-part-i.php
  - Practical application of harmony rules
  - Triadic, complementary definitions

**Key Points to Extract:**
- ✅ Traditional harmony = geometric relationships on color wheel
- ✅ No guarantee of distinguishability or perceptual uniformity
- ✅ Our approach: perceptual constraints replace geometric rules

---

## Positioning Statement (Draft)

**Our Contribution:**

The Color Journey Engine introduces a novel approach to palette generation:

1. **Journey Metaphor**: Construct continuous Bézier paths through perceptually-uniform color space (OKLab), then sample discretely with perceptual constraints.
2. **Mood Expansion**: Single-anchor case uses lightness direction to create coherent palettes from one color (unique contribution).
3. **Guaranteed Anchors**: Anchors always appear exactly in output, not "approximately" (differs from interpolation approaches).
4. **Perceptual Uniformity Throughout**: All operations in OKLab, arc-length parameterization ensures uniform perceptual spacing.

**Contrast With:**
- **Traditional harmony rules** (complementary, analogous): Predefined relationships
- **Simple interpolation**: No perceptual guarantees (RGB/HSL)
- **Data-driven approaches**: Require training data, less controllable
- **Gradient-based tools**: Continuous output, not discrete palette generation

**Not Claimed:**
- First use of OKLab (it's gaining adoption)
- First use of Bézier in color (gradients use them)
- First palette generator (obviously not)

**Claimed:**
- First (to our knowledge) to combine: continuous path construction + discrete sampling + perceptual constraints + single-anchor mood expansion
- Novel architectural approach (journey as construction device)

---

## Bibliography (Harvard Style)

### Primary Sources (Foundational)

1. **Ottosson, B.** (2020). *A perceptual color space for image processing*. https://bottosson.github.io/posts/oklab/

2. **W3C.** (2022). *CSS Color Module Level 4*. W3C Recommendation. https://www.w3.org/TR/css-color-4/

3. **W3C.** (2023). *CSS Color Module Level 5*. W3C Working Draft. https://www.w3.org/TR/css-color-5/

4. **Kamermans, M.** (n.d.). *A Primer on Bézier Curves*. https://pomax.github.io/bezierinfo/

5. **W3C.** (2024). *SVG 2 Specification*. https://www.w3.org/TR/SVG2/

### Secondary Sources (Comparative/Validating)

6. **Levien, R.** (2021). *An interactive review of Oklab*. https://raphlinus.github.io/color/2021/01/18/oklab-critique.html

7. **Levien, R.** (2018). *How long is that Bézier?* https://raphlinus.github.io/curves/2018/12/28/bezier-arclength.html

8. **Verou, L. & Lilley, C.** (n.d.). *Color.js documentation: Gamut mapping*. https://colorjs.io/docs/gamut-mapping.html

9. **Baldwin, N.** (n.d.). *Leonardo: an open source contrast-based color generator*. https://leonardocolor.io/

10. **ICC.** (n.d.). *Introduction to the ICC profile format*. https://www.color.org/iccprofile.xalter

### Tertiary Sources (Background)

11. **Wikipedia.** (n.d.). *Color difference*. https://en.wikipedia.org/wiki/Color_difference

12. **Interaction Design Foundation.** (n.d.). *Color Harmony*. https://www.interaction-design.org/literature/topics/color-harmony

13. **Blackman, D. & Vigna, S.** (2021). *Scrambled Linear Pseudorandom Number Generators*. ACM Transactions on Mathematical Software.

### Tools Surveyed (Not Cited, Positioning Only)

- Adobe Color — https://color.adobe.com/
- Coolors — https://coolors.co/
- Paletton — https://paletton.com/
- Chroma.js — https://gka.github.io/chroma.js/
- Figma plugins: OK Palette, OkColor

---

## Research Status Summary

| Area | Status | Open Items |
|------|--------|------------|
| OKLab foundations | ✅ Complete | None |
| Palette generation approaches | ✅ Complete | None |
| Bézier curves in color | ✅ Complete | None |
| Gamut mapping | ✅ Complete | None |
| Perceptual spacing (JND) | ✅ Complete | None |
| Determinism/PRNG | ✅ Complete | None |
| Color harmony theory | ✅ Complete | None |
| Performance benchmarking | ⚠️ Internal only | Document C-core method |

**Last Updated:** 2025-12-17
