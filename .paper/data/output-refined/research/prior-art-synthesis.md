# Prior Art Synthesis: Color Journey Engine Positioning

**Status:** Complete  
**Last Updated:** 2025-12-17  
**Purpose:** Consolidated research findings to prevent reinvention and position novelty

---

## Executive Summary

This document synthesizes external research across eight areas to ensure the Color Journey Engine specification:
1. **Does not reinvent** established solutions
2. **Aligns with** industry standards where appropriate
3. **Clearly positions** novel contributions
4. **Captures methodological influences** that shape implementation approach

**Key Finding:** The combination of continuous Bézier path construction + discrete sampling with perceptual constraints + single-anchor mood expansion appears to be novel. Individual components are well-established; the architecture combining them is the contribution.

**Methodological Insight:** The symmetry-constrained search approach from Moosbauer & Poole (2025) provides a mental model for journey curve optimization—constraining to symmetric/well-behaved curve families dramatically reduces search complexity.

---

## 1. OKLab Color Space (Foundational)

### Industry Adoption Status

| Platform | Status | Notes |
|----------|--------|-------|
| CSS (browsers) | ✅ Standard | Color Level 4/5, `color-mix()` defaults to OKLab |
| Adobe Photoshop | ✅ Default for gradients | As of 2024+ |
| Adobe Illustrator | ⚠️ Partial | Gradient Blender script supports OKHSL/OKLAB |
| Figma | ❌ No native support | Community plugins available (OK Palette, OkColor) |
| Unity | ✅ Supported | Gradients use OKLab |
| Godot | ✅ Supported | Color picker uses OKLab |

### Key Citations

- **Ottosson (2020)**: Primary source. "Oklab was designed with the goal of [...] having the property that the perceived color difference between two colors is approximately proportional to their Euclidean distance in the color space."
- **W3C CSS Color 4 (2022)**: Official web standard adoption
- **Levien (2021)**: Independent validation for gradients and color manipulation

### Implication for Paper

**Do not argue for OKLab.** Team already values it; industry is adopting. Document *how* we leverage it, not *why* it's good.

---

## 2. Palette Generation Approaches

### Landscape Analysis

| Approach | Tools | Method | Perceptual? | Discrete? |
|----------|-------|--------|-------------|-----------|
| Harmony rules | Adobe Color, Paletton | Geometric relationships (complementary, analogous) | ❌ HSL/HSV | ✅ Yes |
| Interpolation | Chroma.js, CSS gradients | Linear interpolation between colors | ⚠️ Optional | ❌ Continuous |
| Data-driven | Some academic tools | ML/clustering from images | Varies | ✅ Yes |
| Contrast-based | Adobe Leonardo | Target contrast ratios | ✅ CIELAB | ✅ Yes |
| **Journey Engine** | This project | Bézier path + discrete sampling | ✅ OKLab | ✅ Yes |

### Gap Identified

No existing tool combines:
- Continuous path construction (Bézier curves)
- Discrete output with perceptual constraints (Δ_min, Δ_max)
- Single-anchor mood expansion
- Arc-length parameterization for uniform perceptual spacing

### Key Citations

- **IxDF Color Harmony**: Traditional geometric rules
- **Programming Design Systems**: Why perceptual uniformity matters for code
- **Liu et al. (IEEE TVCG)**: Academic image-driven approach (contrast to our deterministic method)

---

## 3. Bézier Curves in Color

### Standard Usage

- **Gradients**: CSS, SVG use Bézier for smooth transitions (continuous output)
- **Animation**: Easing curves
- **Graphics**: Path construction

### Our Differentiation

| Aspect | Standard (gradients) | Color Journey Engine |
|--------|---------------------|---------------------|
| Output | Continuous | Discrete swatches |
| Parameterization | t ∈ [0,1] (non-uniform) | Arc-length (uniform perceptual) |
| Constraints | None | Δ_min, Δ_max, anchor guarantees |
| Space | Often sRGB | Always OKLab |

### Arc-Length Parameterization

This is a known technique but not standard for palette generation:
- **Kamermans**: Comprehensive treatment in "A Primer on Bézier Curves" §14
- **Levien (2018)**: Practical algorithms ("How long is that Bézier?")
- **Observable**: Interactive demonstrations of uniform vs. non-uniform sampling

### Implication for Paper

Arc-length parameterization is well-documented; cite Kamermans. Novel application to discrete palette sampling with constraints.

---

## 4. Gamut Mapping

### CSS Standard Approach (W3C)

The CSS Color Level 4 gamut mapping algorithm:
1. Uses OKLCH space
2. Reduces chroma via binary search
3. Preserves hue and lightness
4. Clips when ΔE < 0.02 (OKLab scale)

**This aligns with our approach.** We are not reinventing; we are implementing established best practice.

### Key Insight from Research

> "Changes in Hue are particularly objectionable; changes in Chroma are more tolerable." — W3C Color Workshop (Lilley)

### Our Two-Layer Approach

| Layer | Standard? | Description |
|-------|-----------|-------------|
| Prevention | ✅ Novel architecture | Gamut-aware path construction |
| Correction | ✅ Standard | Soft chroma reduction with hue preservation |

### Key Citations

- **W3C CSS Color 4 §12**: Standard algorithm
- **Color.js**: Reference implementation
- **ICC Profile Format**: Four rendering intents (background context)

---

## 5. Perceptual Spacing (JND)

### Established Values

| Observer Type | JND (ΔE) | Source |
|---------------|----------|--------|
| Trained observers | ~1 | Standard literature |
| Average viewers | ~2-3 | Standard literature |
| CSS gamut mapping threshold | 0.02 (OKLab 0-1 scale) | W3C |

### Our Δ_min ≈ 2 OKLab Units

This is a **conservative, well-justified choice**:
- Provides safety margin above trained-observer JND
- Aligns with average viewer distinguishability
- Similar threshold concept used in CSS gamut mapping

### Implication for Paper

Cite Ottosson's design goal ("Euclidean distance ≈ perceptual difference") and Wikipedia for JND background. Note our threshold choice is conservative.

---

## 6. Determinism and PRNG

### Established Practice

Seed-based determinism is standard in:
- Procedural generation (games, graphics)
- Avatar generators
- Testing frameworks
- Reproducible data generation

### Industry-Standard Algorithms

| Algorithm | Source | Notes |
|-----------|--------|-------|
| xoshiro128** | Vigna & Blackman (2018/2021) | Fast, passes PractRand |
| xoshiro256++ | Vigna & Blackman (2018/2021) | 256-bit state version |
| JSF | Bob Jenkins (2007) | Alternative, passes PractRand |
| Mulberry32 | Community | Simple 32-bit state |

### Implication for Paper

Our determinism approach follows established patterns. No novel claim here; just document that we use standard PRNG practices for reproducibility.

---

## 7. Symmetry-Constrained Search (Methodological Influence)

### Source

**Moosbauer & Poole (2025)**: "Flip Graphs with Symmetry and New Matrix Multiplication Schemes"  
arXiv:2502.04514v1 [cs.SC]

### Why This Matters (Not Direct Prior Art)

This paper isn't about color—it's about finding optimal matrix multiplication algorithms. However, the **methodological approach** directly informs how we think about journey curve optimization.

### Key Insight: Symmetry Reduces Search Space

The authors faced a problem: searching all possible matrix multiplication schemes is computationally intractable. Their solution:

- Impose **group symmetry constraints** (C₃ cyclic, Z₂ reflection)
- Search only among **symmetric schemes**
- Result: search space reduced by orders of magnitude

This is the same principle we use:

| Their Domain | Our Domain |
|--------------|------------|
| Matrix multiplication tensor decompositions | Bézier curves through OKLab |
| Symmetry group: C₃ × Z₂ | Symmetry: cyclic palettes, mirror gradients |
| "Flip graph" of valid schemes | Space of valid journey curves |
| Orbit operations (modify whole symmetry class) | Modify curve families, not individual points |

### The "Flip Graph" Mental Model

Their algorithm walks a graph where:
- **Nodes** = valid matrix multiplication schemes
- **Edges** = small modifications ("flips") that preserve validity

For Color Journey, we can think similarly:
- **Nodes** = valid Bézier curves in OKLab (in-gamut, smooth)
- **Edges** = nudging control points while maintaining constraints

Finding the "longest perceptual journey" between two anchors is a search over this implicit graph.

### Implementation Implications

1. **Don't search all possible curves** — constrain to symmetric / well-behaved families
2. **Looping strategies** (tile, ping-pong, Möbius) are symmetry operations on the base journey
3. **Multi-anchor journeys** compose from 2-anchor primitives, like their tensor decompositions compose from rank-1 primitives
4. **Orbit-based extension**: when extending a journey past its natural endpoint, we're performing something like their "orbit flip" — modifying a whole class of related curves, not just one point

### Citation (Internal Reference)

```
@article{moosbauer2025flip,
  title={Flip Graphs with Symmetry and New Matrix Multiplication Schemes},
  author={Moosbauer, Jakob and Poole, Michael J.},
  journal={arXiv preprint arXiv:2502.04514},
  year={2025}
}
```

Located at: `open-agents/source/reference-materials/FLIP GRAPHS WITH SYMMETRY AND NEW MATRIX MULTIPLICATION SCHEMES JAKOB MOOSBAUER∗ AND MICHAEL POOLE.pdf`

---

## 8. Color Harmony Theory

### Traditional Approach

Geometric relationships on color wheel:
- Complementary (180° apart)
- Analogous (adjacent)
- Triadic (120° apart)
- Split-complementary

**Limitations:**
- Based on position, not perceptual distance
- No guarantee of distinguishability
- Works in HSL/HSV (not perceptually uniform)

### Our Approach

Replace geometric rules with perceptual constraints:
- Δ_min ensures distinguishability
- Δ_max ensures coherence
- Journey path provides implicit harmony through smooth transitions

### Implication for Paper

Position as "perceptual constraints replace geometric rules." Not claiming harmony theory is wrong; claiming we achieve harmony through different means.

---

## Novelty Statement

### What We're NOT Claiming First

- ❌ First use of OKLab (industry adopting)
- ❌ First use of Bézier in color (gradients use them)
- ❌ First palette generator (obviously)
- ❌ First deterministic color generation (standard practice)
- ❌ First gamut mapping with hue preservation (CSS standard)

### What We ARE Claiming

✅ **Novel combination of:**
1. Continuous Bézier path construction through OKLab
2. Arc-length parameterization for uniform perceptual sampling
3. Discrete output with JND-based constraints (Δ_min, Δ_max)
4. Guaranteed anchor appearance (not approximate)
5. Single-anchor mood expansion using lightness direction

✅ **Novel architectural approach:**
- "Journey metaphor" as construction device
- Two-layer gamut management (prevention + correction)
- Presets as encoded expertise
- Symmetry-constrained curve families for efficient path optimization (cf. Moosbauer & Poole)

✅ **Methodological influence:**
- Search over well-constrained curve families rather than arbitrary paths
- Looping/continuation strategies as symmetry operations on base journey
- Multi-anchor journeys as composition of 2-anchor primitives

---

## Recommendations for Paper

### Citations to Include

| Section | Citation | Purpose |
|---------|----------|---------|
| §2 Perceptual Foundations | Ottosson (2020) | OKLab derivation |
| §2 Perceptual Foundations | W3C CSS Color 4 | Industry validation |
| §3 Journey Construction | Kamermans | Bézier mathematics |
| §3 Journey Construction | W3C SVG 2 | Path definitions |
| §4 Perceptual Constraints | Wikipedia Color Difference | JND background |
| §8 Gamut Management | W3C CSS Color 4 §12 | Standard algorithm |
| §8 Gamut Management | Color.js | Implementation reference |
| §1.4 Positioning | Levien (2021) | Independent OKLab validation |

### Contrast Statements

Use these to position our work:

> "Unlike traditional palette generators that use predefined geometric relationships (complementary, analogous) or simple linear interpolation, the Color Journey Engine constructs continuous Bézier paths through perceptually-uniform OKLab space, then samples discretely with JND-based constraints ensuring distinguishability and coherence."

> "While gamut mapping algorithms like CSS Color 4 §12 reduce chroma to fit colors within gamut, our two-layer approach prevents out-of-gamut samples during path construction and corrects remaining edge cases with hue-preserving soft clipping."

---

## Open Items

1. **Performance benchmarking**: Document C-core method (hardware, test code) for internal reference
2. **Mood expansion survey**: No academic paper found on single-anchor lightness-direction expansion; this strengthens novelty claim

---

*End of synthesis. Use this document when drafting §1.4 (Positioning) and ensuring citations are strategic, not comprehensive.*
