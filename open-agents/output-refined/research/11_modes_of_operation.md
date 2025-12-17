# Modes of Operation and Perceptual Velocity

## Overview

This document distinguishes between the two fundamental modes of operation in the Color Journey Engine—**Journey Mode** and **Categorical Mode**—and introduces the concept of **perceptual velocity** as a higher-order consideration for temporal and rhythmic applications. These concepts address the tension between smooth color transitions and maximum distinguishability.

**Relevance to Paper Goal:** Understanding when to use each mode, and how perceptual velocity affects aesthetic outcomes, is essential for applying the engine appropriately to different use cases.

---

## The Data Viz Tension

### Two Competing Goals

Color sequence generation faces a fundamental tension between two valid but incompatible objectives:

| Goal | Optimizes For | Sacrifices |
|------|---------------|------------|
| **Smooth journeys** | Perceptual continuity, narrative flow | Maximum contrast |
| **Categorical distinction** | Maximum distinguishability | Smooth transitions |

> **Design Decision:** Rather than trying to serve two masters poorly, the engine provides two distinct modes with different objectives. Users choose the mode appropriate for their use case.

### Why Not One Universal Mode?

A single mode that tries to balance both goals:
- Produces mediocre results for both use cases
- Creates unpredictable behavior as parameters change
- Forces users to fight against the algorithm

Better to be explicit: "Do you want smooth flow or maximum contrast?"

---

## Journey Mode (Default)

### Purpose

Journey Mode optimizes for **smooth, ordered sequences** suitable for:
- Timelines and narratives
- Gradients and transitions
- Contexts where perceptual continuity matters
- Animation and cycling effects

### Characteristics

| Aspect | Behavior |
|--------|----------|
| **Adjacency constraint** | Enforces Δ_min ≤ Δ(Cᵢ, Cᵢ₊₁) ≤ Δ_max |
| **Path construction** | Smooth Bézier curves through anchors |
| **Continuity** | C¹ continuity at anchor junctions |
| **Sampling** | Arc-length parameterized for perceptual uniformity |

### Mathematical Formulation

For adjacent swatches $C_i$ and $C_{i+1}$:

$$\Delta_{\min} \leq \|C_i - C_{i+1}\|_{OKLab} \leq \Delta_{\max}$$

Where:
- $\Delta_{\min} \approx 2$ (just-noticeable difference threshold)
- $\Delta_{\max} \approx 5$ (perceptual comfort limit)

### When to Use Journey Mode

- Timeline visualizations (progress, history)
- State transitions (hover, active, disabled)
- Mood-based palettes (warm sunset, cool ocean)
- Animation color cycling
- Any context where "flow" matters

### When NOT to Use Journey Mode

- Categorical data where each color represents a distinct entity
- Maximum contrast requirements
- Semantic color mapping (red=danger, green=safe)

---

## Categorical Mode

### Purpose

Categorical Mode optimizes for **maximum distinguishability** between swatches, suitable for:
- Discrete data categories
- Maximum contrast requirements
- Semantic color mapping
- Accessibility-critical applications

### Characteristics

| Aspect | Behavior |
|--------|----------|
| **Distance goal** | Maximize perceptual distance between all pairs |
| **Path construction** | May use hue maximization, not smooth curves |
| **Continuity** | Not prioritized |
| **Semantic awareness** | Can preserve warm/cool associations |

### Mathematical Formulation

Instead of constraining adjacency, categorical mode maximizes minimum pairwise distance:

$$\max \min_{i \neq j} \|C_i - C_j\|_{OKLab}$$

Subject to:
- Staying within displayable gamut
- Respecting any semantic constraints (e.g., "keep this category warm")

### Algorithmic Differences

| Aspect | Journey Mode | Categorical Mode |
|--------|--------------|------------------|
| **Curve type** | Smooth Bézier | May use angular paths |
| **Sampling** | Sequential along path | Optimized spacing in color space |
| **Anchor role** | Waypoints on path | Fixed category colors |
| **Output order** | Meaningful sequence | Order less important |

### When to Use Categorical Mode

- Pie charts, bar charts with distinct categories
- Legend colors in data visualization
- Status indicators (error, warning, success, info)
- Any context where "this is different from that" matters

### Implementation Notes

> **Design Decision:** Categorical mode is recognized as a genuinely different goal from smooth journeys. The engine may use different algorithms internally rather than just relaxing journey constraints.

Potential approaches:
- Hue wheel spacing (maximize hue angle differences)
- OKLab sphere packing (place colors at maximum distances)
- Constraint satisfaction (ensure minimum ΔE between all pairs)

---

## Perceptual Velocity

### The Concept

Beyond perceptual *distance* (how different two colors are), **perceptual velocity** addresses how *fast* color change feels along a sequence.

> **Key Insight:** Fast hue swings feel "faster" or more noticeable than the same ΔE spent on subtle lightness shifts. The *type* of change affects perceived speed, not just the magnitude.

### Why Velocity Matters

For timelines and animations:
- Color rhythm should align with temporal/narrative rhythm
- "Calm" sequences should feel slow even with consistent ΔE
- "Energetic" sequences should feel fast and dynamic

### Velocity Components

Perceptual velocity $v$ can be modeled as a weighted sum of change rates in different dimensions:

$$v = w_L \cdot \frac{dL}{dt} + w_C \cdot \frac{dC}{dt} + w_h \cdot \frac{dh}{dt}$$

Where:
- $w_L$ = weight for lightness change (lower perceived velocity)
- $w_C$ = weight for chroma change (medium perceived velocity)
- $w_h$ = weight for hue change (higher perceived velocity)

### Heuristic Weights

Based on perceptual research, hue changes tend to feel more dramatic:

| Dimension | Relative Weight | Perceptual Effect |
|-----------|-----------------|-------------------|
| Lightness (L) | 1.0 | Subtle, gradual feel |
| Chroma (C) | 1.2 | Moderate drama |
| Hue (h) | 1.5–2.0 | High impact, "fast" feel |

> **Design Decision:** These weights are heuristic and may be tuned based on empirical testing. The exact values matter less than recognizing that velocity is multidimensional.

### Applications of Velocity

#### Non-Uniform Sampling

Instead of equal arc-length sampling, sample more densely where change feels fast:

$$n_i \propto \int_{t_i}^{t_{i+1}} v(t) \, dt$$

More samples in high-velocity regions creates smoother perceived transitions.

#### Style Presets

Velocity informs preset character:

| Preset | Velocity Profile | How Achieved |
|--------|------------------|--------------|
| **Calm** | Low perceived velocity | Prefer L/C changes over hue |
| **Thriller** | High perceived velocity | More hue swings, angular paths |
| **Corporate** | Uniform velocity | Balanced changes, no surprises |

#### Rhythm Encoding

For temporal applications, velocity can create rhythmic patterns:

- **Accelerando** — Increasing velocity toward climax
- **Ritardando** — Decreasing velocity toward resolution
- **Pulse** — Alternating high/low velocity

---

## Mode Selection Guidelines

### Decision Tree

```
Is the output for discrete categories?
├── YES → Use Categorical Mode
│   ├── Need maximum contrast? → Categorical with high separation
│   └── Need semantic mapping? → Categorical with constraints
│
└── NO → Use Journey Mode
    ├── Need smooth animation? → Journey + closed/pingpong loop
    ├── Need timeline colors? → Journey + open path
    └── Need mood palette? → Journey + single anchor expansion
```

### Hybrid Approaches

Some applications may benefit from combining modes:

1. **Categorical anchors, journey fill** — Use categorical mode to select maximally distinct anchors, then journey mode to create smooth transitions between them.

2. **Journey with velocity control** — Use journey mode but adjust sampling based on velocity for rhythmic effects.

3. **Mode switching** — Different parts of an application use different modes (categorical for legend, journey for timeline).

---

## Interaction with Style Controls

### How Mode Affects Controls

| Control | Journey Mode Effect | Categorical Mode Effect |
|---------|---------------------|------------------------|
| **Temperature** | Biases curve direction | Biases category placement |
| **Intensity** | Chromatic arc drama | May be ignored |
| **Smoothness** | Transition character | N/A (no transitions) |
| **Loop mode** | Affects cycling topology | N/A (no cycling) |

### Velocity and Style Interaction

The style controls implicitly affect perceived velocity:

| Setting | Velocity Tendency |
|---------|-------------------|
| High intensity | Higher velocity (more hue movement) |
| Low intensity | Lower velocity (subtle changes) |
| High smoothness | More uniform velocity |
| Low smoothness | Variable velocity (punchy) |

---

## Future Directions

### Explicit Velocity Control

A potential enhancement would expose velocity as a first-class control:

```c
struct JourneyConfig {
    // ... existing controls ...
    VelocityProfile velocityProfile;  // UNIFORM, ACCELERATING, PULSING
    float targetVelocity;             // Desired perceived speed
};
```

### Rhythm Specification

For temporal applications, users could specify rhythmic patterns:

```c
struct RhythmSpec {
    float[] beats;      // Relative timing of emphasis points
    float intensity;    // How pronounced the rhythm is
};
```

### Adaptive Mode Selection

The engine could automatically suggest modes based on input analysis:
- Many similar anchors → suggest categorical mode
- Wide hue range → suggest journey mode
- Accessibility flag → force categorical mode constraints

---

## Summary

| Mode | Optimizes For | Key Constraint | Best For |
|------|---------------|----------------|----------|
| **Journey** | Smooth transitions | Δ_min ≤ Δ ≤ Δ_max | Timelines, animation, mood |
| **Categorical** | Maximum distinction | Max min pairwise Δ | Charts, legends, categories |

| Velocity Aspect | Description | Application |
|-----------------|-------------|-------------|
| **Definition** | Perceived rate of color change | Rhythmic control |
| **Components** | L, C, h weighted changes | Non-uniform sampling |
| **Presets** | Encode velocity profiles | Calm vs. energetic |

---

## Related Documents

- [03_perceptual_constraints.md](03_perceptual_constraints.md) — Δ_min, Δ_max details
- [04_dynamic_controls.md](04_dynamic_controls.md) — Style parameter specifications
- [05_loop_strategies.md](05_loop_strategies.md) — Loop topology for cycling
- [10_scope_use_cases_presets.md](10_scope_use_cases_presets.md) — Preset definitions
