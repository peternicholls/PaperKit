# Perceptual Color Foundations

## Overview

This document establishes the mathematical and perceptual foundations of the Color Journey Engine's approach to color representation. The choice of color space is not incidental—it is the foundational decision that determines whether color transitions appear smooth, natural, and uniform to human observers. This section covers the rationale for adopting OKLab, its mathematical structure, and the implications for all downstream computations.

**Relevance to Paper Goal:** This forms the theoretical bedrock for the entire engine. Every other component—journey construction, distance constraints, dynamic controls—depends on the properties of the chosen color space.

---

## Why Perceptual Uniformity Matters

### The Problem with Traditional Color Spaces

Human vision perceives color differences nonlinearly. A simple linear blend of RGB values does not correspond to a linear perceptual transition:

> **Design Decision:** Interpolating between saturated blue and yellow in raw RGB produces washed-out grays or unexpected hues in the middle, because the intermediate points travel through an unsaturated region of color space.

Similarly, equal numerical changes in hue or lightness in naive HSV/HSL models often result in uneven perceptual changes—some hues appear brighter or more intense than others for the same numeric step.

### The Perceptual Uniformity Requirement

To address this, scientists have developed *perceptually uniform* color spaces where Euclidean distances correspond more closely to perceived color differences. In such spaces, moving a given distance in any direction produces a change that observers judge to be of similar magnitude.

> **Design Decision:** The engine must work in a perceptually uniform space so that equal steps in the journey correspond to equal perceived differences. This is non-negotiable for achieving smooth, natural color transitions.

---

## OKLab: The Chosen Color Model

### Rationale for OKLab

**OKLab** (Ottosson 2020) is a modern perceptual color space designed to predict human color perception accurately while being computationally efficient.

Compared to alternatives:

| Color Space | Uniformity | Computational Cost | Stability | Chosen? |
|-------------|-----------|-------------------|-----------|---------|
| sRGB | Poor | Low | Good | ✗ |
| HSV/HSL | Poor | Low | Poor (hue discontinuities) | ✗ |
| CIELAB (1976) | Moderate | Moderate | Poor at extremes | ✗ |
| CAM16-UCS | Excellent | High (iterative) | Good | ✗ |
| JzAzBz | Excellent | Moderate | Good | ✗ |
| **OKLab** | **Excellent** | **Low** | **Excellent** | ✓ |

> **Design Decision:** OKLab was selected because it "ensures that equal steps in its coordinate space correspond to equal steps in perceived colour difference" while having an analytical forward and inverse transform (no iterative solvers required). This balances perceptual fidelity with computational practicality.

### OKLab Coordinate System

A color in OKLab is represented by three coordinates $(L, a, b)$:

- **L** — Perceived lightness
  - Range: 0 (perceptual black) to 1 (brightest white under reference illumination)
  - Correlates with how light or dark a color appears
  - Equal differences in L aim to correspond to equal steps in perceived brightness

- **a** — Green–Red opponent axis
  - Positive values: magenta/reddish tints
  - Negative values: greenish tints
  - Zero: achromatic along this axis

- **b** — Blue–Yellow opponent axis  
  - Positive values: yellowish tints
  - Negative values: bluish tints
  - Zero: achromatic along this axis

> **Key Property:** The L, a, b axes in OKLab are designed to be *approximately orthogonal in perception*. Altering L alone should not significantly change the perceived hue or chroma; altering a or b primarily changes hue or chroma without affecting perceived lightness.

### Polar Form: OKLCh

For certain operations (particularly hue manipulation), the polar form is more convenient:

- **L** — Same as OKLab (lightness)
- **C** — Chroma: $C = \sqrt{a^2 + b^2}$ (distance from neutral axis, representing saturation)
- **h** — Hue angle: $h = \text{atan2}(b, a)$ (angle around the a–b plane)

> **Design Decision:** The engine uses OKLab for distance calculations and interpolation, but converts to OKLCh when manipulating hue-related parameters (warmth bias, hue direction). This separation allows clean reasoning about lightness dynamics versus chromatic dynamics.

---

## Mathematical Foundation

### Conversion Pipeline: sRGB → OKLab

The transformation from sRGB to OKLab follows this pipeline:

1. **Linearize sRGB** — Remove gamma encoding to get linear RGB
2. **RGB to XYZ** — Apply standard matrix transformation
3. **XYZ to LMS** — Apply matrix $M_1$ to approximate cone responses
4. **Nonlinear compression** — Apply cube-root: $(l', m', s') = (l^{1/3}, m^{1/3}, s^{1/3})$
5. **LMS to Lab** — Apply matrix $M_2$ to get final $(L, a, b)$

The matrices:

$$
M_1 = \begin{pmatrix}
0.8189330101 & 0.3618667424 & -0.1288597137 \\
0.0329845436 & 0.9293118715 & 0.0361456387 \\
0.0482003018 & 0.2643662691 & 0.6338517070
\end{pmatrix}
$$

$$
M_2 = \begin{pmatrix}
0.2104542553 & 0.7936177850 & -0.0040720468 \\
1.9779984951 & -2.4285922050 & 0.4505937099 \\
0.0259040371 & 0.7827717662 & -0.8086757660
\end{pmatrix}
$$

### Why This Structure?

Each step mimics aspects of human vision:

1. **Matrix $M_1$** approximates **L, M, S cone responses** from XYZ
2. **Cube root** models the **nonlinear perceptual compression** (similar to gamma but biologically aligned)
3. **Matrix $M_2$** extracts:
   - L: weighted average of cone signals (luminance)
   - a: difference between long and medium cones (red-green)
   - b: difference between medium and short cones (yellow-blue)

> **Design Decision:** The cube root (rather than square root or other powers) was chosen because it approximates actual cone response compression while being computationally cheap. This is "hello world" level matrix math—extremely efficient on modern hardware.

### Perceptual Distance Metric

The Euclidean distance in OKLab serves as the perceptual distance metric:

$$
\Delta E_{AB} = \sqrt{(L_B - L_A)^2 + (a_B - a_A)^2 + (b_B - b_A)^2}
$$

> **Design Decision:** A $\Delta E$ of approximately 1.0 in OKLab corresponds to a just-noticeable difference (JND) for an average observer. This metric is used throughout the engine for spacing calculations and constraint enforcement.

---

## Computational Efficiency

### Performance Characteristics

The OKLab conversion is computationally trivial:

- **Per conversion:** ~50–100 CPU cycles
- **Operations:** 18 multiplications + 12 additions + 3 cube roots
- **Memory:** No allocations, all register operations
- **Parallelization:** Trivially vectorizable with SIMD

> **Design Decision:** OKLab was explicitly chosen for its computational simplicity. The entire forward/inverse pipeline uses fixed, known constant matrices—no iterative solving, no conditionals, no special cases. This enables real-time palette generation even on constrained devices.

### Optimized Cube Root

For performance-critical applications, the cube root can be approximated using bit manipulation:

```
Bit-hack + Newton iteration:
- Standard cbrtf: ~35-60 cycles
- Optimized version: ~5-10 cycles
- Error: < 0.1%
```

> **Design Decision:** For palette generation and UI applications, the Newton-refined bit-hack cube root is "plenty accurate" while being 5-10× faster. Scientific color reproduction can use the standard library function if needed.

---

## Implications for the Engine

### Why OKLab Properties Matter

The choice of OKLab has cascading implications:

1. **Linear interpolation works** — A straight line between two colors in OKLab space produces a perceptually smooth gradient

2. **Distance calculations are meaningful** — We can enforce $\Delta_{\min}$ and $\Delta_{\max}$ constraints knowing they correspond to actual perceived differences

3. **Dynamics are separable** — The orthogonality of L, a, b means we can adjust lightness independently of chromaticity without unexpected side effects

4. **Hue interpolation is stable** — Unlike HSV where interpolating across 0°/360° boundary causes problems, OKLab's Cartesian representation avoids discontinuities

### Gamut Considerations

OKLab itself has no inherent bounds—it can represent colors outside any physical display gamut:

> **Design Decision:** Because OKLab is unbounded, the engine must include explicit gamut mapping. Any color that falls outside sRGB when converted back must be projected to the nearest in-gamut color, typically by reducing chroma while preserving hue and lightness.

---

## Key Insights

1. **Perceptual uniformity is foundational** — Without it, no amount of clever interpolation can produce visually smooth transitions

2. **OKLab balances fidelity and efficiency** — It achieves near-CAM16 perceptual quality with CIELAB-level computational cost

3. **The coordinate system enables clean separation of concerns** — Lightness, chroma, and hue can be reasoned about and manipulated independently

4. **Computational simplicity enables real-time use** — The engine can generate palettes instantly, enabling interactive design tools

---

## Bibliography

Ottosson, B. (2020). *A perceptual color space for image processing*. Retrieved from https://bottosson.github.io/posts/oklab/

CIE (1976). *Recommendations on Uniform Color Spaces, Color-Difference Equations, Psychometric Color Terms*. CIE Publication No. 15.

Fairchild, M. D. (2013). *Color Appearance Models* (3rd ed.). Wiley.

Safdar, M., Cui, G., Kim, Y. J., & Luo, M. R. (2017). Perceptually uniform color space for image signals including high dynamic range and wide gamut. *Optics Express*, 25(13), 15131-15151.
