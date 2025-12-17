# API Design Philosophy and Caller Responsibilities

## Overview

This document articulates the **design philosophy** underpinning the Color Journey Engine's API. It defines the boundary between what the engine handles and what callers are responsible for, the principles guiding interface design, and the output structure. Understanding these decisions helps both implementers and users work effectively with the engine.

**Relevance to Paper Goal:** This is the "contract" between the engine and its users. It ensures consistent expectations and clean separation of concerns.

---

## Core Design Philosophy

### The Guiding Principle

> **Design Decision:** The engine should do only what the caller cannot do themselves. Complexity belongs in construction, not in the public interface.

This principle drives all API decisions:

| Engine's Job | Caller's Job |
|--------------|--------------|
| Perceptual color math | Choosing anchor colors |
| Curve construction | Deciding when to use the palette |
| Constraint enforcement | Animation timing |
| Gamut mapping | UI presentation |
| Deterministic generation | Storage/caching strategy |

### Minimalism Over Feature Accumulation

> **Design Decision:** When in doubt, leave it out. Features that can be implemented by callers using the core output should not be built into the engine.

Examples of **rejected features**:
- "Play animation at 30fps" — caller can control timing
- "Apply palette to image" — separate concern
- "Generate complementary palette" — call engine twice with different anchors
- "Export to Photoshop swatch file" — format conversion is caller's job

---

## What the Engine Is

### Core Capability

The engine is a **pure function** that transforms:

```
(anchors, config) → palette
```

Where:
- **anchors**: 1-5 key colors
- **config**: dynamics, loop mode, variation settings
- **palette**: ordered array of color swatches

### Characteristics

- **Stateless** — No memory between calls
- **Deterministic** — Same inputs → same outputs
- **Focused** — Does one thing well (color journey generation)

---

## What the Engine Is NOT

### Explicitly Out of Scope

| Not This | Why Not |
|----------|---------|
| Color picker UI | Presentation concern |
| Animation framework | Timing is caller's domain |
| Image processing library | Different problem space |
| Design system generator | Higher-level abstraction |
| Color naming service | Separate knowledge domain |
| Accessibility checker | Post-processing concern |

> **Design Decision:** The engine produces colors. Everything else—display, application, validation—is external.

---

## Output Structure

### Discrete Palette Only

> **Design Decision:** The engine outputs **discrete swatches only**, not a continuous interpolation function. The "journey" is a construction metaphor; the output is a finite list of colors.

Rationale:
- Callers receive exactly what they need (N colors)
- No ambiguity about sampling
- Engine can optimize internal representation freely
- Simpler mental model

### What Callers Receive

```json
{
  "config": { ... },      // Echo of input config
  "palette": [            // Array of swatches
    { "hex": "#...", "ok": { "L": ..., "a": ..., "b": ... } },
    ...
  ],
  "diagnostics": { ... }  // Quality metrics
}
```

### Swatch Structure

Each swatch contains:

| Field | Type | Description |
|-------|------|-------------|
| `hex` | string | sRGB hex code (`#RRGGBB`) |
| `ok` | object | OKLab coordinates (`{L, a, b}`) |

> **Design Decision:** Both sRGB (for immediate use) and OKLab (for further computation) are provided. Callers can choose which to use.

### Config Echo

The output includes the effective configuration used:

```json
{
  "config": {
    "anchors": ["#FF0000", "#0000FF"],
    "numColors": 8,
    "loop": "open",
    "dynamics": { "warmth": 0.3, "vibrancy": 1.0, ... },
    "variation": { "mode": "off", "seed": null }
  }
}
```

> **Design Decision:** Echoing config enables reproducibility. Callers can log, store, or transmit the config to regenerate the same palette later.

---

## Diagnostics

### Purpose

The diagnostics object reports quality metrics and constraint status:

```json
{
  "diagnostics": {
    "minDeltaE": 2.34,
    "maxDeltaE": 4.87,
    "meanDeltaE": 3.42,
    "contrastViolations": 0,
    "gamutClips": 2,
    "wcagMinRatio": 4.5,
    "traversalStrategy": "arc-length"
  }
}
```

### Available Metrics

| Metric | Description |
|--------|-------------|
| `minDeltaE` | Smallest perceptual distance between adjacent swatches |
| `maxDeltaE` | Largest perceptual distance between adjacent swatches |
| `meanDeltaE` | Average distance |
| `contrastViolations` | Count of constraint violations |
| `gamutClips` | Count of colors that required gamut mapping |
| `wcagMinRatio` | Minimum WCAG contrast ratio in palette |
| `traversalStrategy` | Algorithm used (e.g., "arc-length") |

> **Design Decision:** Diagnostics are informational, not prescriptive. The engine doesn't fail on constraint violations—it reports them and produces output anyway.

---

## CSS Export Format

### Custom Properties

For web usage, palettes can be formatted as CSS custom properties:

```css
:root {
  --cj-1: #FF8040;
  --cj-2: #FFA060;
  --cj-3: #FFC080;
  ...
}
```

> **Design Decision:** The naming convention `--cj-N` (color journey) is stable and independent of anchors or curve shape. This makes integration into design systems straightforward.

### Why Not Gradient Syntax?

The engine outputs discrete swatches, not CSS gradients. Callers can construct gradients from the output if needed:

```css
background: linear-gradient(to right, var(--cj-1), var(--cj-2), var(--cj-3), ...);
```

> **Design Decision:** Gradient construction is caller's responsibility because gradient direction, type (linear/radial/conic), and color stop positions are application-specific.

---

## Caller Responsibilities

### What Callers Must Handle

| Responsibility | Examples |
|----------------|----------|
| **Input validation** | Ensure anchors are valid colors |
| **Parameter bounds** | Keep dynamics values in range |
| **Output application** | Apply colors to UI, charts, etc. |
| **Animation control** | Timing, playback, looping behavior |
| **Accessibility compliance** | Check contrast ratios for specific uses |
| **Storage strategy** | Cache, persist, or regenerate as needed |
| **Error handling** | Respond to invalid configs |

### Simple Behaviors Left to Callers

> **Design Decision:** Simple behaviors that callers can implement trivially are explicitly NOT engine features.

Examples:
- **Ping-pong playback**: Just traverse array forward then backward
- **Restart from index N**: Just start iteration at index N
- **Reverse palette**: Just reverse the array
- **Skip every other color**: Just filter the array

These are array operations, not color operations.

---

## Error Handling Philosophy

### No Hard Failures for Valid Input

> **Design Decision:** If input is syntactically valid, the engine ALWAYS produces output. Constraint violations result in diagnostics, not errors.

| Scenario | Engine Response |
|----------|-----------------|
| Anchors too close | Collapse to fewer colors + diagnostic |
| Impossible contrast | Best effort + diagnostic |
| Out-of-gamut anchor | Clamp to gamut + diagnostic |
| Invalid hex format | Error (invalid input) |

### Error Categories

| Category | Engine Behavior |
|----------|-----------------|
| Invalid syntax | Return error, no output |
| Unsatisfiable constraints | Return output + warning diagnostics |
| Edge cases | Return output (possibly degenerate) |

---

## Extensibility Philosophy

### Open for Composition

The engine is designed to be **composed** with other systems:

```
Engine → Accessibility Checker → Filter → UI
Engine → Persistence Layer
Engine → Export Formatter (Figma, Sketch, etc.)
```

> **Design Decision:** The engine provides a clean interface that external tools can wrap, filter, or extend. It does not try to be a complete design system.

### Closed for Modification

The core algorithm is not designed to be pluggable:

- No custom interpolation functions
- No user-defined color spaces
- No plugin architecture

> **Design Decision:** Stability and predictability are more valuable than infinite configurability. The engine does specific things well; if different behavior is needed, use a different tool.

---

## Versioning Contract

### Semantic Versioning

The engine follows semantic versioning:

- **Major**: Breaking changes to output (different colors from same input)
- **Minor**: New features, parameters, diagnostic fields
- **Patch**: Bug fixes that don't change output for valid input

> **Design Decision:** Determinism extends to versioning. Within a major version, the same input MUST produce the same output. Users can lock to a major version for stability.

### What Counts as Breaking

| Change | Breaking? |
|--------|-----------|
| Different output for same input | YES |
| New parameter with default | NO |
| New diagnostic field | NO |
| Performance improvement | NO |
| Bug fix changing wrong output | MAYBE (documented) |

---

## Key Design Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Do only what callers can't | Focus; avoid feature creep |
| Discrete output only | Clarity; no sampling ambiguity |
| Echo config in output | Reproducibility |
| Diagnostics not errors | Always produce output |
| Simple behaviors = caller | Arrays are easy to manipulate |
| No plugin architecture | Stability over flexibility |
| Semantic versioning | Predictable upgrades |

---

## Key Insights

1. **Less is more** — A focused engine is more useful than a kitchen sink

2. **The boundary matters** — Clear caller responsibilities prevent scope creep

3. **Output is data** — Callers can do anything with an array of colors

4. **Diagnostics enable trust** — Users can verify quality without black-box faith

5. **Composition beats integration** — The engine works well with other tools

---

## Example API Usage Pattern

### Basic Usage

```javascript
const palette = colorJourney({
  anchors: ['#FF0000', '#0000FF'],
  numColors: 8,
  dynamics: { warmth: 0.3 }
});

// palette.palette[0].hex → '#FF0000'
// palette.diagnostics.maxDeltaE → 4.2
```

### With Variation

```javascript
const variant = colorJourney({
  anchors: ['#FF0000', '#0000FF'],
  numColors: 8,
  variation: { mode: 'subtle', seed: 42 }
});
```

### Looped Animation (Caller Code)

```javascript
const palette = colorJourney({ ..., loop: 'closed' });
const colors = palette.palette.map(s => s.hex);

let index = 0;
setInterval(() => {
  applyColor(colors[index]);
  index = (index + 1) % colors.length;  // Caller handles looping
}, 100);
```

---

## Bibliography

Bloch, J. (2008). *Effective Java* (2nd ed.). Addison-Wesley. [API design principles]

Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.

Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
