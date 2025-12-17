# Dynamic Controls: Perceptual Operators

## Overview

This document specifies the **dynamics layer**—a set of high-level parameters that allow users to shape the character of a color journey without directly manipulating individual colors. These controls operate as **perceptual bias operators**, shifting the journey's behavior along dimensions like lightness, chroma, warmth, and smoothness. The dynamics system is what transforms the engine from a simple interpolator into a sophisticated design tool.

**Relevance to Paper Goal:** The dynamics layer is the primary interface for creative control. Understanding how each parameter affects the journey is essential for both implementers and users.

---

## Design Philosophy

### Bias Operators, Not Presets

> **Design Decision:** Dynamics are implemented as **bias operators** rather than preset configurations. Each parameter adjusts a specific perceptual dimension independently. Users compose effects by combining multiple biases, rather than selecting from a menu of fixed options.

This approach provides:
- **Composability** — Effects can be layered
- **Predictability** — Each control has one clear effect
- **Fine-grained control** — Users adjust exactly what they want
- **No hidden behavior** — No unexpected interactions

### Dynamics vs. Presets

| Approach | Characteristics |
|----------|-----------------|
| **Presets** ("sunset", "ocean") | Opaque, fixed combinations; easy but inflexible |
| **Bias operators** | Transparent, composable; more control but requires understanding |

> **Design Decision:** The engine exposes bias operators directly. Higher-level "preset" systems can be built on top by callers who want simplified interfaces, but the engine itself remains low-level and transparent.

---

## The Dynamics Parameters

### Parameter Summary

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| `lightness` | -1.0 to +1.0 | 0 | Shifts L values darker or lighter |
| `chroma` | 0.0 to 2.0 | 1.0 | Scales saturation (1.0 = no change) |
| `contrast` | 0.0 to 2.0 | 1.0 | Expands/compresses L range |
| `vibrancy` | 0.0 to 2.0 | 1.0 | Boosts chroma of less saturated colors |
| `intensity` | 0.0 to 1.0 | 0.5 | Controls curve drama / chromatic arcs |
| `warmth` | -1.0 to +1.0 | 0 | Biases hue direction (warm/cool) |
| `curveStyle` | enum | "linear" | Easing function for interpolation |
| `smoothness` | 0.0 to 1.0 | 0.5 | $C^1$ continuity strength at anchors |

---

## Lightness Dynamics

### Purpose

Controls the overall brightness bias of the journey.

### Behavior

The lightness parameter applies a bias to all L values:

- **Positive values** (+0.1 to +1.0): Shift all colors lighter
- **Negative values** (-0.1 to -1.0): Shift all colors darker
- **Zero**: No bias, use interpolated values directly

### Mathematical Model

For a color with lightness $L$:

$$L' = L + \lambda \cdot (1 - L) \quad \text{if } \lambda > 0$$
$$L' = L + \lambda \cdot L \quad \text{if } \lambda < 0$$

Where $\lambda$ is the lightness parameter. This ensures:
- Positive bias pushes toward white (L=1) proportionally
- Negative bias pushes toward black (L=0) proportionally
- Anchors at L=0 or L=1 remain unmoved

> **Design Decision:** Lightness bias is applied proportionally, not additively. This prevents clipping at extremes and ensures already-light colors don't become blown out.

---

## Chroma Dynamics

### Purpose

Controls the overall saturation/colorfulness of the journey.

### Behavior

The chroma parameter scales the C value in OKLCh:

- **Values > 1.0**: Increase saturation
- **Values < 1.0**: Decrease saturation (toward grayscale)
- **Value = 1.0**: No change

### Mathematical Model

$$C' = C \cdot \kappa$$

Where $\kappa$ is the chroma parameter.

> **Design Decision:** Chroma is a simple multiplier because saturation scales naturally. Unlike lightness, there's no "maximum" chroma to push toward—the gamut boundary handles limits.

### Gamut Interaction

Increasing chroma can push colors outside the sRGB gamut. The engine clamps these back into gamut after all dynamics are applied.

---

## Contrast Dynamics

### Purpose

Controls the lightness range of the palette—the difference between darkest and lightest colors.

### Behavior

Contrast expands or compresses the L values around the midpoint:

- **Values > 1.0**: Darken darks, lighten lights (more contrast)
- **Values < 1.0**: Push toward mid-gray (less contrast)
- **Value = 1.0**: No change

### Mathematical Model

Using an S-curve function $f_L$:

$$f_L(\alpha) = \frac{\alpha^p}{\alpha^p + (1-\alpha)^p}$$

Where $p$ is derived from the contrast parameter:
- $p > 1$: High contrast (S-curve)
- $p = 1$: Linear (no change)
- $p < 1$: Inverse S-curve (reduced contrast)

### Application

For a color at position $\alpha$ along the journey:

$$L(\alpha) = L_{\text{start}} + f_L(\alpha) \cdot (L_{\text{end}} - L_{\text{start}})$$

> **Design Decision:** Contrast uses an S-curve rather than simple scaling because it preserves endpoint values while redistributing intermediate lightness. This is perceptually more natural than additive contrast.

---

## Vibrancy Dynamics

### Purpose

Boosts saturation of less-saturated colors while leaving already-vibrant colors alone.

### Behavior

Unlike uniform chroma scaling, vibrancy is **selective**:

- Low-chroma colors get significant boost
- High-chroma colors get minimal or no boost
- This prevents already-saturated colors from becoming garish

### Mathematical Model

$$C' = C \cdot \left(1 + v \cdot \left(1 - \frac{C}{C_{\max}}\right)\right)$$

Where:
- $v$ is the vibrancy parameter
- $C_{\max}$ is the maximum chroma in the palette

> **Design Decision:** Vibrancy mimics the "vibrance" control in photo editing software, which is universally understood. It's distinct from chroma because it intelligently targets dull colors.

### Use Case

When interpolating between complementary colors (e.g., blue to yellow), the middle can become desaturated gray. Vibrancy counteracts this by boosting the mid-journey chroma without affecting the saturated anchors.

---

## Intensity (Curve Drama)

### Purpose

Controls the chromatic drama of the journey—how far control points deviate from straight-line interpolation between anchors.

### Behavior

- **Value = 0.0**: Subtle, nearly linear paths; control points close to the line
- **Value = 0.5**: Moderate curves with balanced chromatic excursions
- **Value = 1.0**: Maximum drama; pronounced arcs through color space

### Mathematical Model

Intensity scales how far Bézier control points move away from the straight segment:

$$P_1 = \text{lerp}(P_0, P_3, \tfrac{1}{3}) + \iota \cdot \vec{s}_1$$
$$P_2 = \text{lerp}(P_0, P_3, \tfrac{2}{3}) + \iota \cdot \vec{s}_2$$

Where:
- $\iota$ is the intensity parameter
- $\vec{s}_1, \vec{s}_2$ are style-determined offset vectors (typically into higher-chroma regions)

Equivalently, scaling the base offset:

$$s_k = s_k^{\text{base}} \cdot (1 + c_\iota \cdot \iota)$$

Where $c_\iota$ is a tuning constant (typically 1.0–2.0).

### Effect

| Intensity | Journey Character | Visual Result |
|-----------|-------------------|---------------|
| Low (0.0–0.3) | Subtle, minimal | Nearly linear interpolation |
| Medium (0.4–0.6) | Balanced | Gentle chromatic arcs |
| High (0.7–1.0) | Dramatic, energetic | Pronounced curves, vivid paths |

> **Design Decision:** Intensity controls path geometry, not endpoint colors. The anchors remain unchanged; only the route between them becomes more or less dramatic.

### Interaction with Extensions

For extension segments, intensity affects how adventurous the continuation is:
- Low intensity: Extension mostly follows existing direction
- High intensity: Extension can spiral more in hue or push into higher chroma

---

## Warmth (Hue Bias)

### Purpose

Biases the hue interpolation path toward warm or cool colors.

### Behavior

- **Positive values** (+0.1 to +1.0): Bias toward warm hues (reds, oranges, yellows)
- **Negative values** (-0.1 to -1.0): Bias toward cool hues (blues, greens, purples)
- **Zero**: Take the shortest hue path (default)

### The Hue Path Problem

When interpolating hue in OKLCh, there are always two possible paths around the color wheel:

```
Purple (280°) → Green (140°)

Shortest path: 280° → 240° → 200° → 160° → 140°  (through blue, COOL)
Longer path:   280° → 320° → 360° → 40° → 80° → 140°  (through red/yellow, WARM)
```

> **Design Decision:** By default, the engine takes the shortest hue path. The warmth parameter overrides this, forcing the journey through the warm or cool side of the wheel.

### Mathematical Model

Let $\Delta h = h_{\text{end}} - h_{\text{start}}$ (normalized to $[-180°, 180°]$ for shortest path).

With warmth bias $w$:
- If $w > 0$ and $\Delta h < 0$: Add $360°$ to go the warm way
- If $w < 0$ and $\Delta h > 0$: Subtract $360°$ to go the cool way
- If $w = 0$: Use $\Delta h$ as-is (shortest)

### Implementation: Direction Blending

Even at extreme values ($|w| = 1$), the starting color identity is preserved via blending:

$$\vec{v} = (1 - \alpha|w|) \cdot \hat{v}_{\text{base}} + \alpha|w| \cdot \hat{v}_{\text{warm/cool}}$$

Where:
- $\hat{v}_{\text{base}}$ is the default (shortest path) direction
- $\hat{v}_{\text{warm/cool}}$ is the target warm (≈30–60°) or cool (≈200–240°) hue direction
- $\alpha < 1$ ensures partial preservation of the base direction

This prevents a jarring "snap" to pure warm/cool when the user adjusts the parameter.

### Visual Effect

The same anchor pair can produce vastly different palettes:

| Anchors | Warmth | Path | Character |
|---------|--------|------|-----------|
| Purple → Green | 0 | Blue | Cool, oceanic |
| Purple → Green | +1 | Red/Yellow | Warm, sunset-like |

---

## Curve Style

### Purpose

Defines the easing function for how color attributes change along the journey.

### Options

| Style | Function | Effect |
|-------|----------|--------|
| `linear` | $f(t) = t$ | Uniform change |
| `ease-in` | $f(t) = t^2$ | Start slow, end fast |
| `ease-out` | $f(t) = 1-(1-t)^2$ | Start fast, end slow |
| `ease-in-out` | $f(t) = 3t^2 - 2t^3$ | Slow at both ends |

### Application

The curve style is applied to the interpolation parameter $t$ before computing color values:

$$t_{\text{eased}} = f(t)$$
$$\text{color} = \text{interpolate}(A, B, t_{\text{eased}})$$

> **Design Decision:** Curve style applies globally to all dimensions (L, a, b). For per-dimension control, users would need to make multiple engine calls with different anchors.

---

## Smoothness

### Purpose

Controls the strength of $C^1$ continuity enforcement at anchor junctions.

### Behavior

- **Value = 1.0**: Maximum smoothing; tangents fully matched at anchors
- **Value = 0.5**: Moderate smoothing (default)
- **Value = 0.0**: No smoothing; sharp corners allowed at anchors

### Effect

| Smoothness | Junction Behavior | Visual Result |
|------------|-------------------|---------------|
| 0.0 | Control points at anchors | Sharp "corner" in color space |
| 0.5 | Partial tangent matching | Gentle rounding |
| 1.0 | Full tangent matching | Smooth flow through anchors |

> **Design Decision:** Smoothness controls how "flowy" the journey feels through anchors. High smoothness is better for gradients; low smoothness might be preferred when anchors represent distinct states.

---

## Parameter Interaction

### Independence

Dynamics parameters are designed to be **largely independent**:

- Lightness affects only L
- Chroma affects only C
- Warmth affects only hue path
- Contrast affects L distribution (not absolute values)

### Potential Conflicts

Some combinations can conflict:

| Combination | Potential Issue |
|-------------|-----------------|
| High chroma + low lightness | May exceed gamut |
| High contrast + extreme anchors | May clip at black/white |
| High warmth + cool anchors | Long hue path, more colors needed |

> **Design Decision:** The engine applies all dynamics as specified, then performs gamut mapping. Conflicts are resolved by clamping to valid values, not by preventing the combination.

---

## Key Design Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Bias operators, not presets | Composability, transparency |
| Proportional lightness bias | Prevents clipping |
| Simple chroma multiplier | Natural scaling |
| S-curve contrast | Preserves endpoints |
| Selective vibrancy | Matches user expectations |
| Hue path override | Creative control over mood |
| Global curve style | Simplicity; per-dimension would add complexity |
| Adjustable smoothness | Different use cases need different junction behavior |

---

## Key Insights

1. **Dynamics are compositional** — Each parameter has one clear effect that can be combined with others

2. **Defaults produce neutral behavior** — With all defaults, the engine does simple linear interpolation

3. **Perceptual language, not math** — Users think "warmer", "more contrast", not "shift hue angle by 30°"

4. **Gamut is the final arbiter** — Dynamics can request impossible colors; gamut mapping resolves them

5. **Anchors are preserved** — Dynamics affect the path between anchors, not the anchor colors themselves

---

## Bibliography

Adobe Systems. (2006). *Digital Negative (DNG) Specification*. [Vibrance processing description]

Poynton, C. (2012). *Digital Video and HD: Algorithms and Interfaces* (2nd ed.). Morgan Kaufmann.

Hunt, R. W. G. (2004). *The Reproduction of Colour* (6th ed.). Wiley.
