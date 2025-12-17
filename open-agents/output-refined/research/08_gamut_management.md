# Gamut Management and Boundary Handling

> **Design Rationale Document** — Color Journey Engine  
> **Theme**: Gamut awareness, clipping strategies, and perceptual correction  
> **Audience**: Implementation teams, color scientists, rendering engineers

---

## 1. Overview

The Color Journey Engine operates primarily in OKLab/OKLCH space for perceptual uniformity, but must ultimately output colors within a displayable gamut (typically sRGB). This creates a fundamental tension: mathematically elegant paths in perceptual space may traverse colors that cannot be displayed.

This document specifies how the engine handles gamut boundaries through a **two-layer strategy** that prioritizes smooth appearance over mathematical purity.

---

## 2. The Gamut Problem

### 2.1 Why Gamut Matters

OKLab is a perceptually uniform color space, but it encompasses colors that lie outside any real display's capabilities:

- **High-chroma colors** at certain hue angles exceed sRGB
- **Very dark or very light saturated colors** clip
- **Certain hue regions** (cyan-blue, yellow-green) are particularly constrained

When constructing journeys:
- Naive Bézier curves may traverse impossible colors
- Hard clipping creates visible discontinuities
- Perceptual uniformity breaks down at gamut boundaries

### 2.2 The Constraint

All journey colors must satisfy:

$$
\gamma(t) \in G_{\text{sRGB}} \subset \text{OKLab} \quad \forall t
$$

where $G_{\text{sRGB}}$ represents the sRGB gamut volume mapped into OKLab space.

---

## 3. Two-Layer Gamut Strategy

The engine employs a **two-layer approach**: proactive construction and reactive correction.

### 3.1 Layer 1: Gamut-Aware Construction

When placing Bézier control points, the engine:

1. **Prefers moderate chroma levels** — Control points default to ~70-80% of maximum chroma at their hue/lightness
2. **Detects candidate out-of-gamut points** — Before finalizing control points, checks sRGB validity
3. **Pulls toward lower chroma** — If out-of-gamut detected, reduces chroma while preserving hue and lightness
4. **Uses gamut envelope models** — Employs OKLCH gamut boundary approximations (e.g., Björn Ottosson's gamut envelope)

### 3.2 Layer 2: Soft Correction at Sampling

When sampling the curve for final swatches:

1. **Check sRGB validity** — For each sampled OKLab point, test if RGB conversion produces values in [0,1]
2. **Apply perceptual gamut mapping** if invalid:
   - **Preserve hue** (highest priority)
   - **Preserve lightness** (second priority)
   - **Reduce chroma minimally** until valid
3. **Avoid hard clipping** — Never simply clamp RGB channels, as this creates visible discontinuities and hue shifts
4. **Log corrections** — Record in diagnostics when gamut mapping was applied

---
```
┌─────────────────────────────────────────────────────┐
│              DESIGN DECISION                        │
├─────────────────────────────────────────────────────┤
│  Philosophy: Smooth appearance trumps mathematical  │
│  purity. It is better to slightly compromise the    │
│  ideal curve than to produce obviously clipped      │
│  colors with visible discontinuities.               │
│                                                     │
│  The journey should "feel" continuous even if the   │
│  underlying geometry was adjusted for displayability.│
└─────────────────────────────────────────────────────┘
```
---

## 4. Gamut Mapping Algorithm

### 4.1 Per-Sample Correction

For a candidate color in OKLCH $(L, C, h)$:

```
function gamutMap(L, C, h):
    oklch = (L, C, h)
    rgb = oklchToSRGB(oklch)
    
    if isValidSRGB(rgb):
        return oklch
    
    // Binary search for maximum valid chroma
    C_low = 0
    C_high = C
    
    while (C_high - C_low) > epsilon:
        C_mid = (C_low + C_high) / 2
        rgb = oklchToSRGB(L, C_mid, h)
        
        if isValidSRGB(rgb):
            C_low = C_mid
        else:
            C_high = C_mid
    
    return (L, C_low, h)
```

### 4.2 Priority Hierarchy

When gamut mapping is required:

1. **Hue is sacred** — Never shift hue to fit gamut
2. **Lightness is strongly preserved** — Only adjust if absolutely necessary
3. **Chroma absorbs the compromise** — Reduce saturation to fit

This preserves the journey's "character" (its hue story) even when display limitations require desaturation.

---

## 5. Special Cases

### 5.1 Edge-Adjacent Anchors

When an anchor color sits at or near the gamut boundary:

- The engine detects this condition
- Extension strategies may be limited
- Certain loop modes (tangent continuation) may be discouraged

```
if (anchor.atGamutEdge && requestedSwatches > maxClearSteps):
    suggest: pingpong or mobius instead of tangent extension
```

### 5.2 Gray/Neutral Anchors

Achromatic colors (C ≈ 0) have no gamut constraints in chroma dimension:
- All lightness values from 0-1 are valid
- Gamut management focuses on lightness bounds only
- Journey expansion can use any hue direction freely

### 5.3 High-Contrast Journeys

When anchors span extreme lightness ranges:
- Mid-journey points may hit gamut boundaries at high chroma
- Engine automatically moderates chroma through the transition
- Resulting journey may appear less saturated than requested

---

## 6. Gamut-Aware Optimization

When the engine optimizes journey curves, gamut becomes a constraint in the objective function:

$$
J = \text{len}(\gamma) - \lambda \cdot \text{(gamut penalty)}
$$

Where:
- $\text{len}(\gamma)$ = perceptual arc length (to maximize)
- Gamut penalty = accumulated distance outside valid gamut
- $\lambda$ = large enough to ensure gamut compliance

---
```
┌─────────────────────────────────────────────────────┐
│              DESIGN DECISION                        │
├─────────────────────────────────────────────────────┤
│  Out-of-gamut points receive a "big negative" in    │
│  the optimization objective, effectively rejecting  │
│  curves that stray outside displayable colors.      │
│                                                     │
│  This happens at construction time, not just        │
│  sampling time — preventing bad curves rather       │
│  than just correcting bad samples.                  │
└─────────────────────────────────────────────────────┘
```
---

## 7. Chroma and Dynamics Interaction

Dynamic controls affect gamut behavior:

| Control | Gamut Implication |
|---------|-------------------|
| `chroma` > 1.0 | Increases gamut pressure; more mapping likely |
| `chroma` < 1.0 | Reduces gamut pressure; safer |
| `vibrancy` high | Pushes mid-journey toward gamut edges |
| `lightness` extreme | May limit available chroma range |
| `warmth` shift | Changes which hue regions are under pressure |

The engine considers these interactions when applying dynamics:
- If dynamics would push colors out of gamut, chroma is the first to be moderated
- Diagnostics report when dynamic settings caused gamut corrections

---

## 8. Diagnostics for Gamut Events

The engine reports gamut-related information:

```json
{
  "diagnostics": {
    "gamutCorrections": 3,
    "maxChromaReduction": 0.12,
    "constrainedAnchors": ["#ff0000"],
    "gamutStrategy": "chroma-preserve-hue"
  }
}
```

This allows callers to:
- Understand why output differs from theoretical ideal
- Adjust anchors or dynamics to avoid corrections
- Make informed decisions about color choices

---

## 9. Implementation Notes

### 9.1 Gamut Envelope Precomputation

For performance, the engine may precompute:
- Maximum chroma at discrete (L, h) grid points
- Interpolate for intermediate values
- Trade accuracy for speed in real-time applications

### 9.2 Color Space Precision

Gamut boundaries are defined in sRGB, which has specific primaries. The engine:
- Uses exact sRGB ↔ XYZ ↔ OKLab transformations
- Does not approximate or linearize gamut shape
- Handles the irregular boundary topology correctly

---

## 10. Summary

Gamut management in the Color Journey Engine follows these principles:

1. **Prevention over correction** — Build curves that stay in gamut
2. **Soft over hard** — When correction needed, preserve perceptual continuity
3. **Hue preservation** — Character of the journey is non-negotiable
4. **Transparency** — Report all gamut events in diagnostics
5. **Performance-aware** — Use precomputed envelopes for speed

The goal: every outputted palette contains **real, displayable colors** that maintain the perceptual coherence of the designed journey.

---

## Cross-References

- [01_perceptual_color_foundations.md](01_perceptual_color_foundations.md) — OKLab color space
- [02_journey_construction.md](02_journey_construction.md) — Curve construction
- [03_perceptual_constraints.md](03_perceptual_constraints.md) — Distance constraints
- [04_dynamic_controls.md](04_dynamic_controls.md) — Dynamics layer
