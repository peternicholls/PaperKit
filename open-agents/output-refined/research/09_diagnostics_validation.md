# Diagnostics, Validation, and Error Handling

> **Design Rationale Document** — Color Journey Engine  
> **Theme**: Input validation, diagnostic output, caller responsibilities  
> **Audience**: API implementers, integration developers, QA teams

---

## 1. Overview

The Color Journey Engine provides a rich diagnostic layer alongside its palette output. This document specifies:

- What inputs the engine validates and how
- What diagnostic information the engine provides
- What the engine explicitly does NOT guarantee
- How callers should integrate with the engine responsibly

---

## 2. The Diagnostic Philosophy

The engine follows a principle of **responsible flexibility**:

> The engine assists, but does not prevent, the user from exploring unusual or risky color configurations.

This means:
- Invalid inputs are clamped or corrected, not rejected
- Warnings appear in diagnostics, not as errors
- The caller retains full responsibility for semantic appropriateness

---
```
┌─────────────────────────────────────────────────────┐
│              DESIGN DECISION                        │
├─────────────────────────────────────────────────────┤
│  The engine should NEVER silently fail.             │
│                                                     │
│  Every correction, clamping, or constraint          │
│  enforcement must be visible in diagnostics.        │
│                                                     │
│  Callers can then decide: accept, adjust, or retry. │
└─────────────────────────────────────────────────────┘
```
---

## 3. Input Validation

### 3.1 Validated Parameters

The engine enforces basic sanity on all inputs:

| Parameter | Valid Range | Behavior if Invalid |
|-----------|-------------|---------------------|
| Anchor count | $1 \le k \le 5$ | Clamp to range |
| $\Delta_{\min}$ | $> 0$ | Use default (~2) |
| $\Delta_{\max}$ | $> \Delta_{\min}$ | Use default (~5) |
| `lightness` | $[-1, 1]$ | Clamp to range |
| `chroma` | $[0, 2]$ | Clamp to range |
| `contrast` | $[0, 1]$ | Clamp to range |
| `vibrancy` | $[0, 1]$ | Clamp to range |
| `warmth` | $[-1, 1]$ | Clamp to range |
| `numColors` | $\ge 1$ | Minimum 1 |
| `seed` | Any integer | Use as-is |

### 3.2 Anchor Validation

For each anchor color:

1. **Parse color format** — Accept hex (#RRGGBB), RGB object, or OKLab
2. **Validate sRGB range** — RGB values must be in [0, 255] or [0, 1]
3. **Convert to OKLab** — Use standard conversion pipeline
4. **Check gamut** — Flag if anchor is at gamut boundary

Invalid anchors are:
- Corrected if possible (e.g., clamp RGB values)
- Flagged in diagnostics
- Never silently ignored

### 3.3 Anchor Count Limits

The 5-anchor maximum is a UX clarity constraint, not a technical limit:

```
if anchors.length > 5:
    // Don't expose as an "error"
    // Simply don't allow adding the 6th in UI
    diagnostics.warning = "Maximum 5 anchors supported"
    anchors = anchors.slice(0, 5)
```

---
```
┌─────────────────────────────────────────────────────┐
│              DESIGN DECISION                        │
├─────────────────────────────────────────────────────┤
│  "Anchor limit reached" should NOT be an error.     │
│                                                     │
│  The UI should simply prevent adding a 6th anchor.  │
│  If the API receives 6+, it silently truncates      │
│  and notes this in diagnostics.                     │
│                                                     │
│  The engine accommodates, it doesn't punish.        │
└─────────────────────────────────────────────────────┘
```
---

## 4. Diagnostic Output Structure

### 4.1 Standard Diagnostics Object

Every engine response includes:

```json
{
  "diagnostics": {
    "minDeltaE": 2.34,
    "maxDeltaE": 4.87,
    "avgDeltaE": 3.21,
    "contrastViolations": 0,
    "wcagMinRatio": 4.52,
    "wcagViolations": 0,
    "enforcementIters": 2,
    "traversalStrategy": "perceptual",
    "gamutCorrections": 0,
    "warnings": []
  }
}
```

### 4.2 Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `minDeltaE` | float | Smallest perceptual distance between adjacent swatches |
| `maxDeltaE` | float | Largest perceptual distance between adjacent swatches |
| `avgDeltaE` | float | Mean perceptual distance across journey |
| `contrastViolations` | int | Number of adjacent pairs below $\Delta_{\min}$ |
| `wcagMinRatio` | float | Minimum contrast ratio found (for accessibility) |
| `wcagViolations` | int | Count of pairs failing WCAG thresholds |
| `enforcementIters` | int | How many passes to satisfy constraints |
| `traversalStrategy` | string | Algorithm used: "perceptual", "linear", "hybrid" |
| `gamutCorrections` | int | Number of colors that required gamut mapping |
| `warnings` | array | Human-readable warning messages |

### 4.3 Extended Diagnostics (Debug Mode)

For development/debugging, additional fields may be included:

```json
{
  "diagnostics": {
    // ... standard fields ...
    "controlPoints": [...],
    "arcLengthTotal": 47.3,
    "segmentLengths": [12.1, 15.4, 19.8],
    "executionTimeMs": 4.2,
    "cacheHit": false
  }
}
```

---

## 5. Constraint Satisfaction Reporting

### 5.1 Distance Constraints

The engine reports whether perceptual constraints were met:

```json
{
  "diagnostics": {
    "constraintsMet": {
      "deltaMin": true,
      "deltaMax": true,
      "gamut": true,
      "continuity": true
    },
    "constraintDetails": {
      "deltaMinTarget": 2.0,
      "deltaMinActual": 2.34,
      "deltaMaxTarget": 5.0,
      "deltaMaxActual": 4.87
    }
  }
}
```

### 5.2 When Constraints Cannot Be Fully Satisfied

Some anchor configurations make constraints impossible:

- Two anchors very close together → can't achieve $\Delta_{\min}$ steps
- Request for more swatches than perceptually distinguishable
- Gamut-constrained regions limiting path options

In these cases:

```json
{
  "diagnostics": {
    "constraintsMet": {
      "deltaMin": false
    },
    "warnings": [
      "Requested 20 swatches but only 12 perceptually distinct steps possible",
      "Consider using loop strategy or reducing swatch count"
    ]
  }
}
```

---

## 6. What the Engine Does NOT Guarantee

### 6.1 Explicit Non-Guarantees

The engine cannot and does not guarantee:

| Aspect | Why Not |
|--------|---------|
| **Aesthetic success** | Perceptual uniformity ≠ beauty |
| **Accessibility compliance** | Caller must verify contrast for their context |
| **Cultural appropriateness** | Emotional/cultural color meanings vary |
| **Context suitability** | What works for data viz may not work for branding |
| **Extreme input handling** | Pathological configurations may produce minimal results |

### 6.2 Documented Behavior

These non-guarantees are **features, not bugs**:

> The engine provides sophisticated defaults and perceptual foundation, but cannot replace human judgment about whether results serve the specific application.

---
```
┌─────────────────────────────────────────────────────┐
│              DESIGN DECISION                        │
├─────────────────────────────────────────────────────┤
│  The engine makes colors that are perceptually      │
│  coherent. Making them "good" for a specific        │
│  purpose is the caller's job.                       │
│                                                     │
│  We optimize for technical correctness and          │
│  provide tools for evaluation — but final           │
│  aesthetic judgment belongs to the human.           │
└─────────────────────────────────────────────────────┘
```
---

## 7. Expected Usage Pattern

The engine is designed for this workflow:

1. **Provide semantically meaningful anchors** — Colors with intent
2. **Choose appropriate loop mode** — Open, closed, möbius, etc.
3. **Select preset or tune dynamics** — Start with presets, refine
4. **Review diagnostics** — Check constraint satisfaction
5. **Test output in actual context** — Does it work visually?
6. **Iterate if needed** — Adjust parameters and repeat

The engine supports rapid iteration, not one-shot perfection.

---

## 8. Caller Responsibilities

### 8.1 Input Quality

Callers should provide:
- **Valid color values** — Well-formed hex or RGB
- **Meaningful anchor choices** — Colors with purpose
- **Reasonable swatch counts** — Aligned with use case

### 8.2 Accessibility Verification

The engine reports WCAG metrics but **does not enforce** accessibility:

```
// Caller responsibility:
if (diagnostics.wcagViolations > 0) {
    // Decide: adjust colors, change context, or accept
}
```

### 8.3 Semantic Appropriateness

Color meanings are context-dependent:
- Red for "stop" in traffic UI
- Red for "positive" in financial charts (some cultures)
- Red for "celebration" in festive contexts

The engine doesn't know context. The caller does.

---

## 9. Warning Categories

### 9.1 Warning Types

| Category | Example |
|----------|---------|
| `input_clamped` | "Chroma value 2.5 clamped to 2.0" |
| `anchor_adjusted` | "Anchor #ff0000 at gamut boundary" |
| `constraint_partial` | "Delta_min not achievable for all pairs" |
| `loop_limited` | "Möbius loop requires at least 6 swatches" |
| `performance` | "Large swatch count may impact performance" |

### 9.2 Warning vs Error

The engine has **warnings only, never errors** (except for catastrophic failures):

- Invalid input → clamped + warning
- Impossible constraint → best effort + warning
- Unusual configuration → proceed + warning

This keeps the engine usable in exploration scenarios.

---

## 10. Determinism and Reproducibility

### 10.1 The Determinism Guarantee

Given identical inputs, the engine produces **identical outputs**:

```
same anchors + same dynamics + same seed 
    → same palette (within floating-point tolerance)
```

Tolerance: ~0.2% in OKLab coordinates (imperceptible).

### 10.2 Seed Behavior

The variation seed controls all pseudo-random behavior:

- Same seed → same variation pattern
- No seed provided → engine uses deterministic default (not random)
- Explicit randomization requires caller to generate seed

---
```
┌─────────────────────────────────────────────────────┐
│              DESIGN DECISION                        │
├─────────────────────────────────────────────────────┤
│  Determinism is MANDATORY.                          │
│                                                     │
│  The engine must never produce different outputs    │
│  for the same inputs. This is essential for:        │
│    - Testing and QA                                 │
│    - Reproducible design systems                    │
│    - Caching and optimization                       │
│    - User trust and predictability                  │
│                                                     │
│  If you want randomness, YOU provide the seed.      │
└─────────────────────────────────────────────────────┘
```
---

## 11. Error Recovery

### 11.1 Graceful Degradation

When the engine encounters problems:

1. **Never crash** — Return best-effort result
2. **Always produce output** — Even if suboptimal
3. **Document everything** — Fill diagnostics completely
4. **Suggest alternatives** — Via warnings when appropriate

### 11.2 Fallback Behaviors

| Situation | Fallback |
|-----------|----------|
| All anchors identical | Return single color, replicated |
| Invalid color format | Use fallback color (#808080) + warning |
| Zero swatches requested | Return empty array + warning |
| Pathological dynamics | Clamp all values, proceed |

---

## 12. Summary

The diagnostic and validation system follows these principles:

1. **Transparency** — Every decision visible in diagnostics
2. **Flexibility** — Accept unusual inputs, document behavior
3. **Responsibility** — Caller owns semantic meaning
4. **Determinism** — Same inputs, same outputs, always
5. **Graceful degradation** — Never fail completely

The engine is a tool, not a judge. It provides perceptually coherent colors and complete information about how they were generated. What the caller does with them is their domain.

---

## Cross-References

- [07_api_design_philosophy.md](07_api_design_philosophy.md) — API boundaries
- [03_perceptual_constraints.md](03_perceptual_constraints.md) — Distance constraints
- [08_gamut_management.md](08_gamut_management.md) — Gamut handling
- [06_variation_determinism.md](06_variation_determinism.md) — Reproducibility
