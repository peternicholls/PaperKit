# Scope, Use Cases, and Presets

## Overview

This document establishes the **explicit boundaries** of the Color Journey Engine: what it does, what it deliberately does not do, who it serves, and how presets encode design expertise into accessible defaults. This scope statement is essential for setting expectations and guiding both implementation and usage.

**Relevance to Paper Goal:** This foundational section frames the entire system, preventing misunderstandings about the engine's purpose and capabilities.

---

## What the Engine Does

### Core Function

The Color Journey Engine produces **ordered sequences of discrete color swatches** by constructing perceptually-aware paths through color space.

Given:
- **1–5 anchor colors** (user-specified key colors)
- **Style parameters** (temperature, intensity, smoothness, etc.)
- **Configuration options** (loop mode, variation settings)

It generates:
- **N swatches** such that adjacent colors are perceptually distinguishable but smoothly related
- A sequence that follows a **coherent trajectory** in perceptual space
- An ordering that has **narrative/structural meaning**

### Key Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Perceptually uniform** | Uses OKLab color space where distance ≈ perceived difference |
| **Constructive** | Builds paths through color space, not random selection |
| **Deterministic** | Same inputs always produce same outputs |
| **Discrete output** | Produces finite swatch lists, not continuous functions |
| **Constrained** | Enforces perceptual bounds (Δ_min, Δ_max) |

---

## What the Engine Does NOT Do

### Explicitly Out of Scope

> **Design Decision:** The engine should do only what the caller cannot do themselves. Complexity belongs in construction, not in the public interface.

| Not This | Why Not |
|----------|---------|
| **Continuous curve evaluation** | The curve is a construction device, not an exposed API |
| **Animation/interpolation logic** | Consumers handle temporal concerns |
| **Automatic aesthetic optimization** | Provides foundation, not taste |
| **Accessibility compliance checking** | Caller's responsibility to verify contrast |
| **Color naming** | Separate knowledge domain |
| **Image processing** | Different problem space |
| **Design system generation** | Higher-level abstraction built on top |

### The Discrete Nature

> **Design Decision:** The engine produces ordered lists of discrete swatches, not continuous curves that get sampled at runtime. The curve mathematics is an *internal construction device*, not an exposed API.

This means:
- No need for curve evaluation functions in the public interface
- Looping strategies produce extended discrete lists, not continuous wrapping
- Temporal/animation concerns are the consumer's responsibility

---

## Primary Use Cases

### 1. UI Timelines and State Sequences

**Scenario:** A music player needs colors for different playback states or timeline segments.

**Why the engine fits:**
- Ordered swatches map naturally to sequential states
- Perceptual coherence ensures smooth visual transitions
- Anchor colors can represent key moments (start, climax, end)

### 2. Data Visualization with Ordered Categories

**Scenario:** A chart needs colors for sequential data (time series, rankings, progress).

**Why the engine fits:**
- Sequential data maps to journey ordering
- Perceptual uniformity ensures equal visual weight
- Constraints prevent confusingly similar adjacent colors

### 3. Generative Palette Expansion

**Scenario:** A designer has one brand color and needs a harmonious palette.

**Why the engine fits:**
- Single-anchor "mood expansion" generates variations
- Style controls tune the character (warm, cool, vibrant, subdued)
- Deterministic generation allows reproducible results

### 4. Creative/Generative Applications

**Scenario:** An artist wants to explore color combinations from seed colors.

**Why the engine fits:**
- Multiple anchors define key color relationships
- Variation layer adds controlled randomness
- Loop strategies enable continuous/cycling effects

### 5. Animation Color Sequences

**Scenario:** A loading animation needs smoothly cycling colors.

**Why the engine fits:**
- Closed loop ensures seamless wrap
- Perceptual constraints prevent jarring jumps
- Ping-pong mode enables breathing/pulsing effects

---

## Design Principles

### 1. Perceptual Uniformity as Foundation

All decisions are grounded in perceptual color science. OKLab provides the uniform space where mathematical operations correspond to visual experience.

### 2. Aesthetic Expression via Anchors and Controls

The engine separates **what colors** (anchors) from **how they relate** (style controls). Users specify the "what"; the engine computes the "how" within perceptual constraints.

### 3. Graceful Handling of Edge Cases

Rather than failing on unusual inputs, the engine adapts:
- Gray anchors use lightness variation instead of hue
- Extreme colors adapt direction to available gamut space
- Pathological inputs produce documented fallback behavior

### 4. Discrete Output, Continuous Thinking

The journey metaphor describes *construction*, not *consumption*. Internally, the engine thinks in continuous curves; externally, it delivers discrete swatches.

### 5. Caller Responsibility for Context

The engine cannot know how swatches will be used. Callers must:
- Test palettes in their actual context
- Verify accessibility requirements
- Handle edge cases specific to their application

---

## The Preset Philosophy

### Presets as Encoded Expertise

> **Design Decision:** Presets aren't "dumbing down" the interface—they're *encoding expertise*. A well-designed preset captures knowledge about which parameter combinations work well together for specific aesthetic goals.

### The Hybrid Approach

The engine supports two modes of configuration:

| Approach | Who It Serves | Characteristics |
|----------|---------------|-----------------|
| **Presets** | Designers, quick exploration | Curated combinations, named intentions |
| **Parameters** | Power users, fine control | Direct access to all dynamics |

> **Design Decision:** The engine exposes bias operators directly. Higher-level "preset" systems can be built on top by callers who want simplified interfaces, but the engine itself remains low-level and transparent.

### What Presets Encode

A preset bundles:
- **Temperature** — warm/cool bias direction
- **Intensity** — chromatic drama level
- **Smoothness** — transition character
- **Loop preference** — suggested topology for cycling

### Example Presets

| Preset | τ (temp) | ι (intensity) | σ (smooth) | Loop Mode | Character |
|--------|----------|---------------|------------|-----------|-----------|
| **Minimal** | 0 | 0.2 | 0.8 | Tile | Subtle, professional, restrained |
| **Cinematic** | -0.3 | 0.6 | 0.7 | Phased | Dramatic, evolving, atmospheric |
| **Energetic** | 0.4 | 0.8 | 0.3 | Möbius | Vibrant, dynamic, punchy |
| **Corporate** | 0 | 0.3 | 0.9 | Ping-Pong | Clean, reliable, conservative |
| **Retro** | 0.2 | 0.5 | 0.5 | Tile | Warm, nostalgic, balanced |

### Preset Semantics

**Minimal:**
- Near-zero temperature (neutral)
- Low intensity (subtle curves)
- High smoothness (gentle transitions)
- Result: Professional palettes that don't call attention to themselves

**Cinematic:**
- Slight cool bias (atmospheric)
- Medium-high intensity (dramatic arcs)
- Good smoothness (flowing transitions)
- Phased looping (evolving over cycles)
- Result: Movie-poster aesthetics, mood-driven sequences

**Energetic:**
- Warm bias (active, exciting)
- High intensity (pronounced chromatic swings)
- Lower smoothness (punchier transitions)
- Möbius looping (interesting twist patterns)
- Result: Dynamic, attention-grabbing palettes

**Corporate:**
- Neutral temperature
- Low-medium intensity (not distracting)
- Very high smoothness (professional feel)
- Ping-pong (stable, predictable)
- Result: Safe, reliable, boardroom-appropriate

---

## Preset Implementation Notes

### Presets as Starting Points

> **Design Decision:** Presets are suggestions, not constraints. Users can select a preset and then adjust individual parameters to fine-tune.

```c
// Conceptual: preset as parameter bundle
JourneyConfig applyPreset(Preset preset) {
    switch (preset) {
        case MINIMAL:
            return { .temperature = 0, .intensity = 0.2, .smoothness = 0.8 };
        case CINEMATIC:
            return { .temperature = -0.3, .intensity = 0.6, .smoothness = 0.7 };
        case ENERGETIC:
            return { .temperature = 0.4, .intensity = 0.8, .smoothness = 0.3 };
        // ...
    }
}

// User can override after preset application
config = applyPreset(CINEMATIC);
config.temperature = 0.1;  // Make it warmer than default cinematic
```

### Hidden Topology Selection

> **Design Decision:** The user never sees "MÖBIUS MODE!!!"; they just choose "Style: Cinematic, Intensity: High" and the engine quietly picks the interesting topology.

Internally, preset + parameter combinations influence loop strategy selection:

```c
LoopStrategy selectLoopStrategy(JourneyConfig config, Preset preset) {
    if (preset == CINEMATIC && config.intensity > 0.5) {
        return PHASED;  // Evolving cycles for dramatic effect
    }
    if (preset == ENERGETIC && config.intensity > 0.7) {
        return MOBIUS;  // Half-twist for extra interest
    }
    return TILE;  // Safe default
}
```

---

## User-Facing Configuration

### Conceptual API

```c
struct JourneyStyleConfig {
    float temperature;   // -1.0 ... +1.0
    float intensity;     // 0.0 subtle ... 1.0 vivid
    float smoothness;    // 0.0 punchy ... 1.0 smooth
    bool loopEnabled;
    Preset preset;       // Optional: MINIMAL, CINEMATIC, etc.
};

// Usage
JourneyStyleConfig config = {
    .temperature = 0.4,   // slightly warm
    .intensity = 0.8,     // pretty vivid
    .smoothness = 0.7,    // mostly smooth
    .loopEnabled = true,
    .preset = NONE        // custom, not using preset
};

Journey journey = createJourney(anchors, config);
Swatch[] swatches = generateSwatches(journey, 64);
```

### Meaningful Creative Control

This approach gives users **meaningful creative control** without exposing any of the tensor/metric/Bézier/loop-topology machinery. The three floats (temperature, intensity, smoothness) plus optional preset feed directly into:
- Bézier control point generation
- Segment joining behavior
- Extension & looping strategy selection
- Arc-length sampling logic

---

## Constraints and Validation

### Input Constraints

The engine enforces minimal input constraints to avoid pathological cases:

| Parameter | Valid Range | Out-of-Range Behavior |
|-----------|-------------|----------------------|
| Anchor count | 1–5 | Clamp to range |
| Temperature | -1.0 to +1.0 | Clamp |
| Intensity | 0.0 to 1.0 | Clamp |
| Smoothness | 0.0 to 1.0 | Clamp |
| Δ_min | > 0 | Use default |
| Δ_max | > Δ_min | Use default |

### User Responsibility

> **Design Decision:** The user is expected to **check, test, and integrate responsibly**, not just crank random parameters and assume anything the engine produces is "correct".

The engine:
- Provides a well-structured, perceptually-aware starting point
- Deliberately narrows the input space to avoid obvious nonsense
- Documents edge case behavior

The caller must:
- Check the palette against the actual context
- Handle edge cases (extreme anchors, accessibility contrast)
- Decide if the result is appropriate for the specific application

---

## Related Documents

- [04_dynamic_controls.md](04_dynamic_controls.md) — Detailed parameter specifications
- [05_loop_strategies.md](05_loop_strategies.md) — Loop topology details
- [07_api_design_philosophy.md](07_api_design_philosophy.md) — API contract
- [09_diagnostics_validation.md](09_diagnostics_validation.md) — Error handling
