# Variation Layer and Deterministic Behavior

## Overview

This document specifies the **variation layer** and the engine's **determinism guarantees**. The variation layer provides controlled randomness for generating palette alternatives, while the determinism requirement ensures that the engine remains predictable and reproducible. These seemingly opposing goals are reconciled through **pseudo-random determinism**—randomness that is completely reproducible given a known seed.

**Relevance to Paper Goal:** Determinism is a core non-negotiable requirement. The variation layer adds creative flexibility without compromising reproducibility.

---

## The Core Determinism Requirement

### Absolute Reproducibility

> **Design Decision:** The Color Journey Engine MUST be **programmatically deterministic**. Given the same inputs, it MUST produce the same outputs, up to small numerical differences arising from floating-point arithmetic and platform differences.

This is not a preference—it is a hard requirement.

### What "Same Inputs" Means

For identical output, the following must match:

| Input | Requirement |
|-------|-------------|
| Anchor colors | Same colors, same order, same representation |
| Configuration | All dynamics, loop mode, UI fields identical |
| Variation config | Same mode and seed (if used) |
| Implementation version | Same engine version |

### Tolerance for Numerical Precision

> **Design Decision:** Outputs must be identical modulo a small tolerance (on the order of ~0.2% in channel values or $\Delta E$) attributable solely to floating-point precision. This accounts for platform differences in math library implementations.

Example acceptable variance:
- Color `#FF8040` vs `#FF8041` — acceptable (1/255 ≈ 0.4%)
- Color `#FF8040` vs `#FF9050` — NOT acceptable (visible difference)

---

## Why Determinism Matters

### Practical Requirements

1. **Debugging** — Developers must be able to reproduce bugs
2. **Testing** — Automated tests need predictable outputs
3. **Sharing** — Configurations can be shared as compact seeds/parameters
4. **Version control** — Generated assets can be diffed meaningfully
5. **Caching** — Identical inputs can be cached without recomputation

### The "Config as ID" Pattern

With determinism, a configuration object (anchors + parameters + seed) serves as a **unique identifier** for a specific palette:

```json
{
  "anchors": ["#FF0000", "#00FF00"],
  "dynamics": { "warmth": 0.3 },
  "variation": { "seed": 42 }
}
```

This config will **always** produce the same palette. It can be:
- Stored instead of storing the full palette
- Transmitted compactly
- Regenerated on any conforming implementation

---

## Prohibited Non-Determinism Sources

### What MUST NOT Affect Output

> **Design Decision:** No source of non-determinism may affect palette generation.

Prohibited:
| Source | Why Prohibited |
|--------|---------------|
| System time | Would vary between runs |
| Thread scheduling | Race conditions cause variance |
| External state | Uncontrolled dependencies |
| True random numbers | Unreproducible |
| Hash table iteration order | Implementation-dependent |
| Uninitialized memory | Undefined behavior |

### Implementation Implications

- Random number generation MUST use seeded PRNG
- Floating-point operations MUST use consistent rounding
- Iteration order MUST be deterministic (arrays, not unordered sets)
- No side effects from or to external state

---

## The Variation Layer

### Purpose

While determinism is required, users may want to:
- Generate **alternatives** to a base palette
- Add **organic texture** to transitions
- Explore **nearby** palettes without manual anchor adjustment

The variation layer provides this through **controlled, seeded perturbations**.

### Variation Modes

| Mode | Effect |
|------|--------|
| `off` | No variation; pure interpolation |
| `subtle` | Small perturbations; ΔE < 1 |
| `noticeable` | Moderate perturbations; ΔE 1-2 |
| `extreme` | Large perturbations; ΔE 2-4 |

> **Design Decision:** Variation modes are categorical rather than continuous (no slider from 0 to 100). This prevents the paralysis of infinite choice and provides meaningful distinct options.

### Variation Parameters

```json
{
  "variation": {
    "mode": "subtle|noticeable|extreme|off",
    "seed": <integer>
  }
}
```

- **mode**: Categorical strength
- **seed**: Integer seed for PRNG

---

## Pseudo-Random Number Generation

### PRNG Requirements

The variation layer uses a **pseudo-random number generator (PRNG)** with these properties:

1. **Seeded** — Initialized from user-provided seed
2. **Deterministic** — Same seed produces same sequence
3. **Well-distributed** — Numbers uniformly distributed
4. **Specified algorithm** — Implementation must use documented algorithm

> **Design Decision:** The PRNG algorithm must be specified in the engine documentation so that implementations can guarantee cross-platform reproducibility. Suggested: xoshiro256** or similar.

### Seed Handling

| Seed Value | Behavior |
|------------|----------|
| Explicit integer | Use that seed |
| `null` or omitted | Default seed (e.g., 0) or variation disabled |

> **Design Decision:** If variation is requested but no seed provided, the engine uses a **default seed (0)**, NOT a random seed. This preserves determinism.

### PRNG Advancement Order

The order in which random numbers are consumed must be **fixed and documented**:

1. Per-color L perturbation
2. Per-color a perturbation
3. Per-color b perturbation
4. (Or whatever order is chosen—but it must be specified)

> **Design Decision:** PRNG advancement order is part of the specification. Changing it would change outputs for existing seeds.

---

## How Variation Is Applied

### Perturbation Approach

Variation adds small offsets to interpolated colors in OKLab space:

$$L' = L + \delta_L$$
$$a' = a + \delta_a$$
$$b' = b + \delta_b$$

Where $\delta_L$, $\delta_a$, $\delta_b$ are drawn from the PRNG.

### Distribution of Perturbations

Perturbations are typically:
- Drawn from normal (Gaussian) distribution
- Centered at 0
- Scaled by mode (subtle = small σ, extreme = large σ)

| Mode | Approximate σ |
|------|---------------|
| subtle | 0.01-0.02 |
| noticeable | 0.03-0.05 |
| extreme | 0.08-0.15 |

### Anchor Preservation

> **Design Decision:** Anchors are NEVER perturbed. Variation applies only to interpolated colors, not to user-specified anchor colors.

This ensures anchors remain exactly as specified. Variation affects the *journey between* anchors, not the waypoints themselves.

### Tapering Near Anchors

To ensure smooth transitions into/out of anchors:

$$\text{perturbation\_scale}(t) = \sin(\pi \cdot t)$$

This yields zero perturbation at $t=0$ and $t=1$ (anchors), maximum at $t=0.5$ (midpoint).

---

## Variation and Constraints Interaction

### Constraint Enforcement After Variation

Variation is applied **before** constraint checking:

1. Compute base interpolated colors
2. Apply perturbations
3. Check/enforce gamut
4. Check/enforce distance constraints
5. Output

### Handling Constraint Violations

If perturbation pushes a color out of bounds:
- Gamut: Clamp/map back to sRGB
- Distance: Report in diagnostics (perturbations may affect spacing)

> **Design Decision:** Variation does not guarantee distance constraints are still met exactly. Diagnostics should report actual post-variation metrics.

---

## Reproducibility Verification

### Cross-Implementation Testing

Implementations can verify determinism by:

1. Define reference test cases (anchors, params, seed)
2. Compute expected outputs
3. Assert new implementation matches to tolerance

### Test Case Format

```json
{
  "test_id": "determinism_001",
  "input": {
    "anchors": ["#FF0000", "#0000FF"],
    "dynamics": { "warmth": 0 },
    "variation": { "mode": "subtle", "seed": 12345 },
    "numColors": 5
  },
  "expected_output": [
    {"hex": "#FF0000", "ok": {"L": 0.628, "a": 0.225, "b": 0.126}},
    ...
  ],
  "tolerance": 0.002
}
```

---

## Seed as Palette Identifier

### Exploration Pattern

Users can explore alternatives by iterating seeds:

```
seed=1: Palette variant A
seed=2: Palette variant B
seed=3: Palette variant C
...
```

Each seed deterministically produces a unique (but related) palette.

### Sharing Pattern

Instead of sharing a full palette, users can share:
- Anchors
- Configuration
- Seed

Recipients regenerate the exact same palette locally.

---

## Key Design Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Determinism is mandatory | Debugging, testing, sharing, caching |
| ~0.2% tolerance | Floating-point variance is acceptable |
| No true randomness | Would break reproducibility |
| Seeded PRNG only | Controlled randomness |
| Categorical variation modes | Avoids choice paralysis |
| Default seed if omitted | Preserves determinism |
| Specified PRNG algorithm | Cross-platform reproducibility |
| Fixed PRNG advancement order | Seed stability |
| Anchors never perturbed | User intent preserved |
| Tapering near anchors | Smooth anchor transitions |

---

## Key Insights

1. **Determinism and variation are compatible** — Pseudo-randomness provides both

2. **Seed is powerful** — A single integer unlocks infinite reproducible variants

3. **Tolerance handles reality** — Floating-point variance is unavoidable but bounded

4. **Order matters** — PRNG sequence is part of specification

5. **Anchors are sacred** — Even with variation, user-specified colors are exact

---

## Bibliography

Marsaglia, G. (2003). Xorshift RNGs. *Journal of Statistical Software*, 8(14), 1-6.

Blackman, D., & Vigna, S. (2018). Scrambled linear pseudorandom number generators. *arXiv preprint arXiv:1805.01407*.

Knuth, D. E. (1997). *The Art of Computer Programming, Volume 2: Seminumerical Algorithms* (3rd ed.). Addison-Wesley.
