# Perceptual Distance Constraints

## Overview

This document defines the perceptual constraints that govern how the Color Journey Engine spaces colors along a journey. The engine enforces minimum and maximum perceptual distances between adjacent swatches, ensuring that transitions are neither imperceptibly subtle nor jarringly abrupt. These constraints transform the abstract notion of "smooth color transition" into quantifiable, enforceable rules.

**Relevance to Paper Goal:** These constraints are the mechanism by which the engine guarantees perceptual quality. They operationalize the design goal of "smooth transitions" into specific mathematical bounds.

---

## The Perceptual Distance Problem

### Why Constraints Are Needed

Without constraints, color sequences can fail in two ways:

1. **Too Similar** — Adjacent colors are so close that the difference is imperceptible. This wastes palette slots on redundant colors.

2. **Too Different** — Adjacent colors jump abruptly, breaking the sense of smooth transition. The eye perceives a "step" rather than a flow.

> **Design Decision:** The engine must enforce both a minimum and maximum perceptual distance between consecutive swatches. This ensures every step is noticeable but not jarring.

### The Distance Metric

All distance calculations use Euclidean distance in OKLab:

$$\Delta E = \sqrt{(L_2 - L_1)^2 + (a_2 - a_1)^2 + (b_2 - b_1)^2}$$

Because OKLab is perceptually uniform, this metric approximates perceived color difference.

---

## Just Noticeable Difference (JND)

### Defining the Threshold

The **Just Noticeable Difference (JND)** is the smallest color change that an average human observer can detect under standard viewing conditions.

In OKLab:
- JND ≈ **1.0 units** (theoretical threshold)
- Practical threshold ≈ **2.0 units** (accounting for viewing conditions, observer variability)

> **Design Decision:** A $\Delta E$ of approximately 2 units is treated as the Just Noticeable Difference threshold. Colors closer than this may be indistinguishable to many observers under typical conditions.

### JND Implications

| $\Delta E$ Range | Perceptual Interpretation |
|------------------|--------------------------|
| < 1.0 | Imperceptible to most observers |
| 1.0 – 2.0 | Barely perceptible, subtle |
| 2.0 – 3.0 | Noticeable, clear difference |
| 3.0 – 5.0 | Obvious difference, still smooth |
| > 5.0 | Pronounced difference, may feel like a "step" |

---

## The $\Delta_{\min}$ Constraint

### Definition

$$\Delta_{\min} \approx 2.0$$

This is the **minimum allowed perceptual distance** between any two adjacent swatches.

### Rationale

> **Design Decision:** Setting $\Delta_{\min}$ at the JND threshold (≈2) ensures that every color step is perceptible. There's no point generating colors that viewers cannot distinguish—it wastes palette capacity and creates the illusion of redundancy.

### Enforcement

If two anchors are closer than $\Delta_{\min}$:

1. **Collapse case:** The engine may treat them as essentially the same anchor, producing no intermediate swatches
2. **Skip intermediates:** No interpolation is performed; the journey jumps directly from one to the other

> **Design Decision:** When anchors are extremely close ($\Delta < \Delta_{\min}$), the engine does not attempt to create meaningless intermediate colors. It either collapses them or produces a direct transition.

---

## The $\Delta_{\max}$ Constraint

### Definition

$$\Delta_{\max} \approx 5.0$$

This is the **maximum allowed perceptual distance** between any two adjacent swatches.

### Rationale

> **Design Decision:** Setting $\Delta_{\max}$ at approximately 5 units ensures that no single step is so large that it feels like an abrupt jump. Differences above ~5 are readily noticeable and can break the sense of smooth progression.

### Enforcement

If a segment between anchors has total distance $D > \Delta_{\max}$:

1. **Subdivide:** The segment is divided into $n$ sub-segments where:
   $$n = \left\lceil \frac{D}{\Delta_{\max}} \right\rceil$$

2. **Insert intermediates:** $n-1$ intermediate swatches are inserted

3. **Cap subdivisions:** $n \leq 5$ to prevent excessive palette length

> **Design Decision:** At most 5 segments (4 intermediate swatches) are created between any two anchors. This keeps palettes manageable in length and prevents over-refinement. If anchors are extremely far apart, each step will approach $\Delta_{\max}$.

---

## Adaptive Sampling

### The Algorithm

Given anchors $A$ and $B$ with perceptual distance $D$:

```
if D < Δ_min:
    # Colors nearly identical
    append only B to output (skip intermediates)
else:
    n = min(5, ceil(D / Δ_max))
    for i in 1 to n:
        t = i / n
        interpolated_color = interpolate(A, B, t)
        append interpolated_color to output
```

### Resulting Swatch Spacing

Each segment has length $D/n$, guaranteeing:
- Each step ≤ $\Delta_{\max}$
- Each step ≥ $\Delta_{\min}$ (approximately, given the constraints)

### Example Calculation

| Total Distance D | Segments n | Step Size D/n |
|-----------------|------------|---------------|
| 3.0 | 1 | 3.0 |
| 7.0 | 2 | 3.5 |
| 12.0 | 3 | 4.0 |
| 20.0 | 4 | 5.0 |
| 30.0 | 5 (capped) | 6.0 |

Note: When D is very large and capped at n=5, step sizes may exceed $\Delta_{\max}$. This is a trade-off for palette manageability.

---

## Granularity Control

### User-Specified Swatch Count

The engine can also accept a requested number of swatches $N$ rather than relying purely on adaptive sampling:

> **Design Decision:** If the user specifies $N$ swatches, the engine distributes them along the journey. The $\Delta_{\min}$ and $\Delta_{\max}$ constraints become advisory warnings rather than hard limits—the user's explicit request takes precedence.

### Granularity Modes

| Mode | Behavior |
|------|----------|
| **Adaptive** | Engine determines count based on distance constraints |
| **Fixed N** | User specifies exact count; constraints become advisory |
| **Minimum N** | At least N swatches; may add more for long segments |

---

## Constraint Interaction with Dynamics

### Dynamics Can Affect Distance

Dynamic parameters (lightness bias, chroma boost, warmth) can alter the effective path length. A curved path in OKLab space is longer than a straight path between the same anchors.

> **Design Decision:** Distance constraints are evaluated on the actual path (after dynamics are applied), not the straight-line distance between anchors. If dynamics increase path length, more intermediate swatches may be needed.

### Gamut Clipping and Distance

Gamut mapping can also affect distances. If a color is clipped to remain in gamut, the actual step size may differ from the theoretical calculation.

> **Design Decision:** Constraint checking occurs after gamut mapping to ensure the final output meets the perceptual distance requirements.

---

## Diagnostics Output

### Reporting Distance Metrics

The engine can report actual distance statistics in its output:

```json
{
  "diagnostics": {
    "minDeltaE": 2.34,
    "maxDeltaE": 4.87,
    "meanDeltaE": 3.42,
    "constraintViolations": 0
  }
}
```

> **Design Decision:** The engine reports actual perceptual distances in the palette, allowing callers to verify that constraints were met or understand how the palette was constructed.

### Constraint Violation Handling

When constraints cannot be met (e.g., user requests 100 swatches between two close colors):

1. **Warning:** Report the constraint violation in diagnostics
2. **Best effort:** Produce the requested output anyway
3. **No hard failure:** The engine does not refuse to produce output

> **Design Decision:** The engine prioritizes producing output over strict constraint enforcement. Callers who need hard guarantees should check the diagnostics.

---

## Perceptual Comfort Zone

### The "Sweet Spot"

Based on the constraints, the ideal step size falls in the range:

$$2.0 \leq \Delta E \leq 5.0$$

This is the **perceptual comfort zone**—steps are clearly distinguishable but not jarring.

### Visual Interpretation

| Step Size | Visual Quality |
|-----------|----------------|
| < 2.0 | Too subtle, may seem redundant |
| 2.0 – 3.0 | Gentle, subtle transitions |
| 3.0 – 4.0 | Clear, pleasant transitions |
| 4.0 – 5.0 | Noticeable, but smooth |
| > 5.0 | Feels like a "jump" or distinct step |

---

## Key Design Decisions Summary

| Decision | Value | Rationale |
|----------|-------|-----------|
| $\Delta_{\min}$ | ~2.0 | JND threshold; avoid imperceptible steps |
| $\Delta_{\max}$ | ~5.0 | Comfort limit; avoid jarring jumps |
| Max subdivisions | 5 | Keep palettes manageable |
| Constraint enforcement | Soft | Best-effort; diagnostics report violations |
| Evaluation point | After dynamics + gamut mapping | Actual path, not theoretical |

---

## Key Insights

1. **Constraints operationalize "smooth"** — Without quantified bounds, "smooth transition" is subjective. These constraints make it measurable.

2. **JND is the floor** — There's no benefit to colors below the perceptual threshold.

3. **The comfort zone is 2–5** — This range balances distinguishability with continuity.

4. **Adaptive sampling is intelligent** — The engine automatically determines how many colors are needed based on the perceptual distance.

5. **User intent trumps constraints** — When users specify explicit counts, constraints become advisory.

---

## Bibliography

Mahy, M., Van Eycken, L., & Oosterlinck, A. (1994). Evaluation of uniform color spaces developed after the adoption of CIELAB and CIELUV. *Color Research & Application*, 19(2), 105-121.

Luo, M. R., Cui, G., & Rigg, B. (2001). The development of the CIE 2000 colour-difference formula: CIEDE2000. *Color Research & Application*, 26(5), 340-350.

Ottosson, B. (2020). *A perceptual color space for image processing*. Retrieved from https://bottosson.github.io/posts/oklab/
