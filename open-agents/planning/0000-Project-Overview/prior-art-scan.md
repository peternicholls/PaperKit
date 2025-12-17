# Prior Art & Positioning Scan

**Status:** In Progress  
**Last updated:** 2024-12-17  
**Purpose:** Map existing approaches to position Color Journey Engine novelty

## Scan Areas

### 1. Perceptual Color Spaces (OKLab)

**What We Need:**
- Industry adoption evidence (Adobe, CSS, etc.)
- Comparison with CIELAB, CIEDE2000
- Rationale for OKLab choice

**Open Sources:**
- [ ] Björn Ottosson's blog (https://bottosson.github.io/posts/oklab/)
- [ ] CSS Color Module Level 4 (W3C spec)
- [ ] Adobe Color documentation
- [ ] Figma engineering blog (if they mention OKLab)

**Key Points to Extract:**
- Why OKLab over predecessors
- Industry momentum (validation of choice)
- Perceptual uniformity metrics

---

### 2. Palette Generation Approaches

**What We Need:**
- Traditional methods (complementary, analogous, triadic)
- Modern tools and their approaches
- What makes journey metaphor different

**Open Sources:**
- [ ] Color theory documentation (public domain)
- [ ] Existing tool docs: Coolors, Adobe Color, Paletton
- [ ] CSS gradient specs (as comparison point)

**Key Points to Extract:**
- Most use predefined relationships or simple interpolation
- Few (if any) use continuous path construction with discrete sampling
- Positioning: "Unlike X which does Y, our approach Z"

---

### 3. Bézier Curves in Color

**What We Need:**
- Standard usage (gradients, transitions)
- What's different about our application

**Open Sources:**
- [ ] SVG spec (Bézier curve definitions)
- [ ] CSS gradient specs
- [ ] Standard computer graphics texts (if freely available)

**Key Points to Extract:**
- Bézier curves common in display (gradients)
- Less common in palette generation (discrete output)
- Arc-length parameterization for uniform sampling

---

### 4. Gamut Mapping

**What We Need:**
- Standard approaches to out-of-gamut colors
- Why hue preservation matters

**Open Sources:**
- [ ] CSS Color spec (gamut mapping section)
- [ ] ICC profile documentation (if public)
- [ ] W3C working group discussions (public)

**Key Points to Extract:**
- Common approaches: clipping, compression, hue shifting
- Our choice: soft clipping with hue preservation
- Two-layer approach (prevention + correction)

---

### 5. Perceptual Spacing (JND)

**What We Need:**
- Just-Noticeable Difference thresholds
- Validation for Δ_min ~2 ΔE units

**Open Sources:**
- [ ] Ottosson's OKLab paper/blog (if JND mentioned)
- [ ] Public perceptual research summaries
- [ ] W3C accessibility documentation

**Key Points to Extract:**
- Established JND threshold values
- Basis for minimum spacing constraint

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
