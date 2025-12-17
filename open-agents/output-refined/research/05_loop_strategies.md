# Loop Strategies and Path Topology

## Overview

This document specifies how the Color Journey Engine handles the **topology** of color paths—whether a journey is open-ended, forms a closed loop, oscillates back and forth, or has more exotic behaviors. Loop strategy determines how the beginning and end of a color sequence relate to each other, which is critical for applications like continuous animations, cycling palettes, and seamless transitions.

**Relevance to Paper Goal:** Loop topology is a distinguishing feature of the engine. Understanding these strategies is essential for applications that require repeating or continuous color sequences.

---

## Why Loop Topology Matters

### The Boundary Problem

In many applications, the color sequence must **repeat or cycle**:

- Animated color cycling
- Continuous timelines that loop
- Seamless palette wraps

Without explicit loop handling, the transition from the last color back to the first can be **jarring**—a visible discontinuity.

> **Design Decision:** The engine explicitly models loop topology rather than leaving it to callers. This ensures smooth boundaries are mathematically guaranteed, not approximated.

---

## Loop Strategy Options

### Summary

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `open` | Start → End, no closure | One-time transitions |
| `closed` | Start → End → Start (smooth) | Continuous cycling |
| `pingpong` | Start → End → Start (retracing) | Back-and-forth oscillation |
| `mobius` | Half-twist loop | Alternating cycle effects |
| `phased` | Progressive shift per cycle | Evolving animations |

---

## Open Path (`open`)

### Definition

The journey proceeds from the first anchor to the last anchor and **stops**. There is no attempt to connect the end back to the beginning.

### Behavior

$$J(t): t \in [0, 1] \quad \text{where } J(0) = A_1, J(1) = A_m$$

### Characteristics

- Default mode for $m \geq 2$ anchors
- Output is a finite sequence with no wrap consideration
- If looped externally, there will be a visible jump from $A_m$ back to $A_1$

### Use Cases

- One-time state transitions
- Linear progress indicators
- Categorical palettes (not intended to cycle)

> **Design Decision:** Open is the default because it makes no assumptions about how the output will be used. Callers who need cycling must explicitly request it.

---

## Closed Loop (`closed`)

### Definition

The journey forms a complete cycle, returning smoothly from the last anchor back to the first.

### Behavior

$$J(0) = J(1) = A_1$$

The engine adds a segment from $A_m$ back to $A_1$, creating a closed path.

### Output Semantics

> **Design Decision:** In closed loop mode, the output array **omits the duplicate final color**. The last swatch is adjacent to (but not identical to) $A_1$, because $A_1$ is already the first swatch. When looped, the sequence wraps seamlessly.

Example with anchors A, B, C:
- Path: A → B → C → A
- Output: `[A, ..., B, ..., C, ...]` (last element is close to A, but A not repeated)

### Continuity Requirement

The engine ensures $C^1$ continuity at the wrap point:
- The tangent leaving $A_m$ toward $A_1$ matches
- The tangent arriving at $A_1$ from $A_m$

This prevents a "corner" in color space at the loop boundary.

### Use Cases

- Continuous color cycling animations
- Hue wheels
- Looping ambient effects

---

## Ping-Pong (`pingpong`)

### Definition

The journey proceeds from start to end, then **reverses** back to start. This creates a back-and-forth oscillation.

### Behavior

For parameter $u \in [0, 2]$:

$$\tilde{t} = \begin{cases} u & 0 \leq u < 1 \\ 2 - u & 1 \leq u < 2 \end{cases}$$

Then $J(\tilde{t})$ gives the color.

### Characteristics

- No new colors generated in the reverse pass
- Path is exactly retraced
- Smooth reversal at the turning point ($A_m$)
- Smooth loop at the return point ($A_1$)

### Output Semantics

> **Design Decision:** Ping-pong output includes the forward sequence. The reverse pass is implicit—callers can traverse the array forward then backward, or the engine can output the full forward-and-back sequence explicitly.

Example output (explicit):
- Forward: `[A, X, Y, Z, B]`
- Full ping-pong: `[A, X, Y, Z, B, Z, Y, X, A]` or `[A, X, Y, Z, B, Z, Y, X]` (omitting duplicate A)

### Use Cases

- "Breathing" or "pulsing" color effects
- Bidirectional progress indicators
- Oscillating state visualizations

---

## Möbius Loop (`mobius`)

### Definition

A **half-twist** loop that requires **two complete traversals** to return to the starting color. Named after the Möbius strip, which has a 180° twist.

### Behavior

After one traversal ($t = 0 \to 1$), you arrive at a color related to the start but with some attribute **inverted**. After the second traversal ($t = 1 \to 2$), you return to the original color.

### Mathematical Interpretation

One approach: invert the chromatic components at the halfway point:

$$J_{\text{mobius}}(1) = (L, -a, -b) \quad \text{when } J_{\text{mobius}}(0) = (L, a, b)$$

This yields the **complementary color** (180° hue rotation) at the midpoint.

### Visual Effect

- Cycle 1: Journey from Red → ... → Cyan (complement)
- Cycle 2: Journey from Cyan → ... → Red (back to original)

The viewer perceives continuous change that takes two "laps" to truly repeat.

### Use Cases

- Complex animations with implicit alternation
- Effects that should vary between loops
- Artistic/generative applications

> **Design Decision:** Möbius is an advanced option. It requires careful understanding of the twist behavior. Most applications should use closed or pingpong instead.

---

## Phased Loop (`phased`)

### Definition

Each repetition of the loop applies a **systematic shift** to the colors, so the palette evolves over time rather than repeating exactly.

### Behavior

On cycle $k$:
- Hue shifted by $k \cdot \Delta h$
- Or lightness shifted by $k \cdot \Delta L$
- Or other progressive transformation

### Mathematical Interpretation

$$J_k(t) = J_0(t) + k \cdot \text{shift}$$

Where `shift` is a per-cycle offset in one or more dimensions.

### Visual Effect

- Cycle 1: Blue → Green
- Cycle 2: Blue+10° → Green+10° (slightly shifted hues)
- Cycle 3: Blue+20° → Green+20°
- ...eventually wraps around

### Use Cases

- Slowly evolving animations
- Generative art with progressive change
- Long-running visualizations that shouldn't feel static

> **Design Decision:** Phased loops are parameterized by the shift amount and dimension. This is the most complex loop type and should only be used when continuous evolution is specifically desired.

---

## Single-Anchor Loop Behavior

### Special Case

With only one anchor, certain loop strategies are degenerate:

| Strategy | Behavior with 1 Anchor |
|----------|----------------------|
| `open` | Single color output (trivial) |
| `closed` | Loop around the anchor (mood expansion) |
| `pingpong` | Same as closed (no forward/back distinction) |
| `mobius` | Half-twist to complement and back |
| `phased` | Progressive hue rotation around anchor |

> **Design Decision:** Single-anchor journeys default to `closed` behavior, creating a loop of variations around the anchor color.

---

## Output Array Conventions

### Non-Repetition Rule

> **Design Decision:** Loop outputs **omit duplicate colors** at boundaries. If the loop returns to the starting color, that color is NOT repeated at the end of the array.

Rationale:
- Prevents doubled colors when looping externally
- Reduces array length
- Caller can easily repeat if duplication is needed

### Example: Closed Loop with 5 Colors

Conceptual path: `A → B → C → D → E → A`

Output array: `[A, B, C, D, E]` (5 elements)

When looped: `A, B, C, D, E, A, B, C, D, E, ...` (A follows E naturally)

---

## Caller Responsibilities

### What the Engine Handles

- Constructing mathematically smooth loop paths
- Ensuring continuity at boundaries
- Outputting appropriate swatch sequences

### What Callers Handle

> **Design Decision:** Simple repetition behaviors are **caller responsibility**, not engine features.

| Behavior | Responsibility |
|----------|---------------|
| Smooth loop closure | Engine |
| "Play N times then stop" | Caller |
| "Restart from index 0" | Caller |
| Animation timing | Caller |
| Pause/resume | Caller |

The engine provides the colors; the caller controls playback.

---

## Loop Topology Summary

```
Open:      A ────────────── B     (no closure)

Closed:    A ────────────── B
           └────────────────┘     (smooth return)

Pingpong:  A ────────────── B
           ◄──────────────►       (oscillates)

Möbius:    A ───────┐  ┌──→ A     (two laps to repeat)
                    ↓  ↑
           A' ←─────┴──┘

Phased:    A₁ → B₁ → A₁'
           A₂ → B₂ → A₂'         (progressive shift)
           A₃ → B₃ → A₃'
```

---

## Key Design Decisions Summary

| Decision | Rationale |
|----------|-----------|
| Open as default | No assumptions about usage |
| Closed omits duplicate | Prevents doubled boundary colors |
| Pingpong retraces path | Simplicity; no new colors needed |
| Möbius uses half-twist | Provides two-period effect |
| Phased has configurable shift | Flexibility for evolution |
| Playback is caller responsibility | Engine stays focused on color |

---

## Key Insights

1. **Topology is explicit, not implicit** — The engine models loop behavior mathematically, guaranteeing smooth boundaries

2. **Non-repetition simplifies usage** — Callers can loop arrays without doubled boundary colors

3. **Most applications need only open/closed/pingpong** — Möbius and phased are specialized

4. **Playback timing is separate** — The engine produces colors; animation control is external

5. **Single-anchor loops are valid** — Mood expansion is the natural interpretation

---

## Bibliography

Lamport, L. (1994). *LaTeX: A Document Preparation System*. Addison-Wesley. [Möbius strip topology discussion]

Foley, J. D., van Dam, A., Feiner, S. K., & Hughes, J. F. (1990). *Computer Graphics: Principles and Practice* (2nd ed.). Addison-Wesley.
