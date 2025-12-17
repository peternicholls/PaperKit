# Journey Construction and Anchor System

## Overview

This document describes how the Color Journey Engine constructs paths through perceptual color space. The core abstraction is the **journey**—a continuous path defined by user-specified **anchor colors** that serve as waypoints. The engine's role is to construct a smooth, perceptually coherent curve connecting these anchors, then sample discrete colors from that curve.

**Relevance to Paper Goal:** This defines the geometric and mathematical framework for how color sequences are generated. The anchor system and curve construction are central to the engine's flexibility and power.

---

## The "Journey" Metaphor

### Conceptual Framework

> **Design Decision:** The term "journey" was deliberately chosen over "gradient" or "palette" because it emphasizes the *constructive process*—a path through color space—rather than the static result. The journey is a construction device; the output is a discrete set of swatches.

The journey metaphor captures several key ideas:

1. **Directionality** — There is a start and end (or a cycle)
2. **Waypoints** — Anchors are places the journey must pass through
3. **Path flexibility** — The route between waypoints can vary
4. **Temporal progression** — Colors are ordered, with a sense of "before" and "after"

### What the Journey Is NOT

> **Design Decision:** The journey is NOT a continuous function that callers should sample arbitrarily. The engine outputs discrete swatches only. The continuous curve is an internal construction mechanism—the caller receives N specific colors, not an interpolation function.

This distinction matters because:
- Callers should not expect to query "color at t=0.347"
- The engine can optimize internal representation freely
- Simple behaviors (like ping-pong playback) become caller responsibility

---

## Anchor System

### Definition and Purpose

**Anchors** are user-specified key colors that define the skeleton of the journey. They are guaranteed to appear in the output and serve as fixed boundary conditions for the path construction.

| Property | Specification |
|----------|---------------|
| Minimum anchors | 1 |
| Maximum anchors | 5 |
| Format | Any standard color format (hex, RGB, etc.) |
| Internal representation | OKLab coordinates |
| Guarantee | Each anchor appears exactly in the output |

### Why Maximum 5 Anchors?

> **Design Decision:** The 5-anchor limit is a deliberate constraint for UX clarity and perceptual coherence. With more than 5 anchors:
> - The journey becomes difficult to reason about
> - The perceptual "story" of the color sequence fragments
> - UI complexity increases substantially
> - Most practical use cases (timelines, UI states, data visualization) need ≤5 key colors

This is a *design choice*, not a technical limitation. The mathematics would work for any number of anchors.

### Anchor Ordering

Anchors are processed in the order provided:

$$A_1 \rightarrow A_2 \rightarrow ... \rightarrow A_m$$

The journey visits each anchor in sequence. For closed loops, it then returns to $A_1$.

---

## Single-Anchor Journeys: Mood Expansion

### The Special Case

When only one anchor is provided, the engine cannot construct a traditional "transition between colors." Instead, it performs **mood expansion**—creating a set of harmonious colors centered on the single anchor.

> **Design Decision:** Single-anchor mode generates colors that vary the anchor in multiple dimensions (lightness, slight hue shifts, chroma variations) to create a cohesive palette anchored on that color. This is analogous to "variations on a theme."

### Mood Expansion Behavior

With one anchor $A_1$, the engine:

1. Uses the anchor as the palette's conceptual center
2. Generates variations along multiple axes:
   - Lighter and darker variants (L axis)
   - Slight hue rotations (h in OKLCh)
   - Chroma variations (C in OKLCh)
3. Forms a closed loop returning to the anchor

The exact variations depend on dynamic parameters (covered in the Dynamic Controls document).

### Use Cases

Single-anchor journeys are useful for:
- Generating a monochromatic palette with depth
- Creating UI state variations (hover, active, disabled) from a brand color
- Animating a "breathing" or "pulsing" color effect

---

## Multi-Anchor Journeys

### Segment Construction

For $m$ anchors ($m \geq 2$), the journey is composed of $m-1$ segments:

$$\gamma_0: A_1 \rightarrow A_2$$
$$\gamma_1: A_2 \rightarrow A_3$$
$$...$$
$$\gamma_{m-2}: A_{m-1} \rightarrow A_m$$

Each segment is constructed independently but with continuity constraints at the junction points.

### Continuity at Anchors

**$C^0$ Continuity (position):** The end of segment $\gamma_i$ must equal the start of segment $\gamma_{i+1}$. This is automatically satisfied since both meet at anchor $A_{i+1}$.

**$C^1$ Continuity (tangent):** For smooth transitions, the engine can match the direction of approach and departure at each anchor. This prevents "corners" in the color path.

> **Design Decision:** By default, the engine applies smoothing at anchor junctions to achieve $C^1$ continuity. This makes the journey feel fluid rather than segmented. However, if sharp transitions are desired at an anchor, this can be disabled.

---

## Curve Construction: Bézier Representation

### Why Bézier Curves?

The engine represents each segment as a **cubic Bézier curve** in OKLab space. This provides:

1. **Flexibility** — Control points can shape the path beyond straight lines
2. **Mathematical elegance** — Well-understood properties
3. **Continuity control** — Easy to enforce $C^1$ at junctions
4. **Efficiency** — Fast evaluation

### Cubic Bézier Definition

A cubic Bézier curve with endpoints $P_0$, $P_3$ and control points $P_1$, $P_2$:

$$\gamma(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$$

For $0 \leq t \leq 1$:
- $\gamma(0) = P_0$ (start anchor)
- $\gamma(1) = P_3$ (end anchor)

### Tangent Vectors

The tangent (derivative) at endpoints:
- $\gamma'(0) = 3(P_1 - P_0)$ — direction leaving start
- $\gamma'(1) = 3(P_3 - P_2)$ — direction arriving at end

### Control Point Placement

By default, control points are placed on the line between anchors (making the Bézier equivalent to linear interpolation). Dynamic parameters then "nudge" these control points to shape the curve:

> **Design Decision:** The default is a straight-line path (control points on the line). Dynamic parameters introduce curvature by moving control points off-line. This means with no dynamics, you get simple linear interpolation—the most predictable baseline.

### Ensuring $C^1$ Continuity

To match tangents at anchor $A_{i+1}$, the control point $Q_1$ of the next segment is placed such that:

$$Q_1 = A_{i+1} + (A_{i+1} - P_2)$$

This mirrors $P_2$ across the anchor, ensuring the outgoing direction matches the incoming direction.

---

## Arc-Length Parameterization

### The Problem with Parameter $t$

The Bézier parameter $t$ does not correspond to distance along the curve. Equal increments in $t$ produce unequal distances in OKLab space, leading to uneven perceptual steps.

### Arc-Length Solution

The engine estimates total arc length and samples at equal arc-length intervals:

1. **Estimate total arc length** — Numerically integrate $|\gamma'(t)|$ over $[0,1]$
2. **Distribute sample points** — Place $N$ samples at equal arc-length intervals
3. **Map back to $t$** — Find the $t$ value corresponding to each arc-length position

> **Design Decision:** Arc-length parameterization ensures that the output swatches are perceptually equidistant (in terms of path distance in OKLab), not just parametrically equidistant. This is essential for uniform visual stepping.

### Practical Implementation

For efficiency, the engine uses numerical approximation:
- Subdivide curve into many small segments
- Sum Euclidean distances of segments
- Use binary search or Newton iteration to find $t$ for target arc lengths

---

## Output: From Journey to Swatches

### Sampling the Journey

After constructing the continuous journey $J(t)$, the engine samples $N$ discrete colors:

1. **Determine sample positions** — Based on requested count and arc-length distribution
2. **Evaluate curve** — Compute OKLab coordinates at each position
3. **Apply variations** — If variation is enabled, perturb colors slightly
4. **Gamut map** — Ensure all colors are within sRGB
5. **Convert to output format** — Hex, RGB, etc.

### Anchor Preservation

> **Design Decision:** Anchors always appear exactly in the output sequence. They are not approximated or averaged. This ensures the user's specified key colors are honored precisely.

If the user provides anchors A, B, C and requests 7 swatches, the output will include A at position 0, C at position 6, and B at approximately the middle, with interpolated colors filling the gaps.

---

## Key Design Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Journey as construction metaphor | Emphasizes process over static result |
| Discrete output only | Simplifies caller responsibility; engine controls sampling |
| Maximum 5 anchors | UX clarity, perceptual coherence |
| Single-anchor = mood expansion | Graceful handling of edge case |
| Cubic Bézier representation | Flexibility with mathematical elegance |
| Default to linear path | Predictable baseline; dynamics add curvature |
| $C^1$ continuity at anchors | Smooth transitions by default |
| Arc-length parameterization | Uniform perceptual stepping |
| Anchor preservation | User's key colors are never altered |

---

## Key Insights

1. **The journey is a construction device, not the output** — Callers receive discrete swatches, not a continuous function

2. **Anchors are sacred** — They define the constraints; the engine fills in between them

3. **Curve flexibility enables dynamics** — By representing paths as Bézier curves, we gain control points that dynamic parameters can manipulate

4. **Arc-length matters for perception** — Without it, swatches would cluster in curved regions

5. **Single-anchor is valid and useful** — The engine gracefully handles this as "mood expansion"

---

## Bibliography

Farin, G. (2002). *Curves and Surfaces for CAGD: A Practical Guide* (5th ed.). Morgan Kaufmann.

De Boor, C. (1978). *A Practical Guide to Splines*. Springer-Verlag.

Piegl, L., & Tiller, W. (1997). *The NURBS Book* (2nd ed.). Springer.
