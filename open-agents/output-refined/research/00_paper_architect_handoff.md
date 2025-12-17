# Paper Architect Handoff: Color Journey Engine Specification

## Overview

This document provides a comprehensive handoff from the Research Consolidator to the Paper Architect for structuring the Color Journey Engine specification paper. It summarizes all available research materials, recommends a paper structure, and identifies key themes for each section.

---

## Available Research Documents

### Complete Document Inventory (11 documents)

| # | Document | Key Themes | LaTeX Section Candidate |
|---|----------|------------|-------------------------|
| 01 | `01_perceptual_color_foundations.md` | OKLab, perceptual uniformity, mathematics | §2 Perceptual Foundations |
| 02 | `02_journey_construction.md` | Anchors, Bézier curves, mood expansion | §3 Journey Construction |
| 03 | `03_perceptual_constraints.md` | JND, Δ_min/Δ_max, adaptive sampling | §4 Perceptual Constraints |
| 04 | `04_dynamic_controls.md` | Temperature, intensity, smoothness, warmth | §5 Style Controls |
| 05 | `05_loop_strategies.md` | Open, closed, pingpong, möbius, phased | §6 Loop Strategies |
| 06 | `06_variation_determinism.md` | Seeds, PRNG, reproducibility | §8 Variation Layer |
| 07 | `07_api_design_philosophy.md` | Engine boundaries, output format | §9 API Design |
| 08 | `08_gamut_management.md` | sRGB boundaries, soft correction | §7 Gamut Management |
| 09 | `09_diagnostics_validation.md` | Error handling, caller responsibilities | §10 Responsibilities |
| 10 | `10_scope_use_cases_presets.md` | Scope, use cases, presets philosophy | §1 Introduction/Scope |
| 11 | `11_modes_of_operation.md` | Journey vs categorical mode, velocity | §5b Modes of Operation |

### Source Materials

- **Primary Source**: `open-agents/source/ideas/Reasoning.md` (~9000 lines of design discussions)
- **Key Insights**: `open-agents/source/ideas/key-insights.md` (synthesis document with structure recommendations)

---

## Recommended Paper Structure

Based on analysis of source materials and key-insights.md recommendations:

```
1. Introduction and Scope
   - What the engine does / doesn't do
   - Primary use cases
   - Design principles
   
2. Perceptual Color Foundations
   - OKLab color space
   - Why perceptual uniformity matters
   - Coordinate systems (OKLab vs OKLCh)
   
3. Journey Construction
   - The "journey" metaphor
   - Anchor system (1-5 colors)
   - Cubic Bézier curves
   - Single-anchor mood expansion
   - Multi-anchor path construction
   
4. Perceptual Constraints
   - Just-noticeable difference (JND)
   - Δ_min and Δ_max bounds
   - Adaptive sampling
   - Constraint enforcement
   
5. User-Facing Style Controls
   - Temperature (warm/cool bias)
   - Intensity (curve drama)
   - Smoothness (transition character)
   - Other dynamics (lightness, chroma, contrast, vibrancy)
   
6. Modes of Operation
   - Journey Mode (smooth transitions)
   - Categorical Mode (maximum distinction)
   - Perceptual velocity concept
   - Mode selection guidelines
   
7. Loop Strategies
   - Open paths
   - Closed loops
   - Ping-pong oscillation
   - Möbius half-twist
   - Phased evolution
   
8. Gamut Management
   - The sRGB boundary problem
   - Two-layer strategy (construction + correction)
   - Hue preservation
   
9. Variation and Determinism
   - Core determinism requirement
   - Controlled variation layer
   - Seed handling
   
10. API Design and Output Structure
    - Discrete palette output
    - Output format (hex + OKLab)
    - Diagnostics
    
11. Caller Responsibilities
    - Input validation
    - What the engine cannot guarantee
    - Expected usage patterns
    
12. Future Directions
    - Potential enhancements
    - Open questions
```

---

## Section-by-Document Mapping

### Section 1: Introduction and Scope
**Primary source**: [10_scope_use_cases_presets.md](open-agents/output-refined/research/10_scope_use_cases_presets.md)

Key content:
- Explicit "what the engine does / doesn't do" statements
- Primary use cases (timelines, data viz, generative palettes, animation)
- Design principles (perceptual uniformity, discrete output)
- Preset philosophy introduction

### Section 2: Perceptual Color Foundations
**Primary source**: [01_perceptual_color_foundations.md](open-agents/output-refined/research/01_perceptual_color_foundations.md)

Key content:
- OKLab derivation and properties
- L, a, b coordinate meanings
- OKLCh cylindrical form
- Conversion pipeline (sRGB → linear → OKLab)

### Section 3: Journey Construction
**Primary source**: [02_journey_construction.md](open-agents/output-refined/research/02_journey_construction.md)

Key content:
- Journey metaphor (constructive, not prescriptive)
- Anchor system (1-5 anchors, guaranteed appearance)
- Single-anchor "mood expansion" (critical concept)
- Cubic Bézier segments with C¹ continuity
- Arc-length parameterization

### Section 4: Perceptual Constraints
**Primary source**: [03_perceptual_constraints.md](open-agents/output-refined/research/03_perceptual_constraints.md)

Key content:
- JND threshold (~2 OKLab units)
- Δ_min (~2) and Δ_max (~5) rationale
- Adaptive sampling algorithm
- Constraint violation handling

### Section 5: Style Controls
**Primary source**: [04_dynamic_controls.md](open-agents/output-refined/research/04_dynamic_controls.md)

Key content:
- Temperature: direction blending formula
- Intensity: control point scaling
- Smoothness: continuity enforcement
- Other parameters: lightness, chroma, contrast, vibrancy, warmth

### Section 6: Modes of Operation
**Primary source**: [11_modes_of_operation.md](open-agents/output-refined/research/11_modes_of_operation.md)

Key content:
- Journey Mode vs Categorical Mode distinction
- When to use each
- Perceptual velocity concept
- Mode selection decision tree

### Section 7: Loop Strategies
**Primary source**: [05_loop_strategies.md](open-agents/output-refined/research/05_loop_strategies.md)

Key content:
- Five loop strategies (open, closed, pingpong, möbius, phased)
- Output semantics for each
- Internal vs exposed strategies
- Non-repetition rules

### Section 8: Gamut Management
**Primary source**: [08_gamut_management.md](open-agents/output-refined/research/08_gamut_management.md)

Key content:
- Two-layer approach (design-time + sample-time)
- Soft correction philosophy
- Hue preservation priority
- Gamut-aware control point placement

### Section 9: Variation and Determinism
**Primary source**: [06_variation_determinism.md](open-agents/output-refined/research/06_variation_determinism.md)

Key content:
- Core determinism requirement
- Controlled variation layer
- PRNG with explicit seeds
- Reproducibility guarantees

### Section 10: API Design
**Primary source**: [07_api_design_philosophy.md](open-agents/output-refined/research/07_api_design_philosophy.md)

Key content:
- Pure function model
- Discrete output (not continuous curves)
- Output structure (palette array, config echo, diagnostics)
- What's explicitly out of scope

### Section 11: Caller Responsibilities
**Primary sources**: 
- [09_diagnostics_validation.md](open-agents/output-refined/research/09_diagnostics_validation.md)
- [10_scope_use_cases_presets.md](open-agents/output-refined/research/10_scope_use_cases_presets.md)

Key content:
- Input validation rules
- What the engine cannot guarantee
- User responsibility for context testing
- Graceful degradation behavior

---

## Key Themes to Emphasize

### 1. "Discrete Output, Continuous Thinking"
The engine thinks in continuous curves internally but outputs discrete swatches. This is a construction device, not an exposed API.

### 2. "Perceptual Uniformity as Foundation"
Every decision is grounded in the perceptual uniformity of OKLab. Mathematical operations correspond to visual experience.

### 3. "The Journey Is Constructive, Not Prescriptive"
Colors are generated "as if" traveling a perceptual path—this gives coherence and order, but users can use them however they want.

### 4. "Presets Encode Expertise"
Presets aren't dumbing-down; they capture knowledge about which parameter combinations work well for specific goals.

### 5. "Graceful Edge Case Handling"
Rather than failing on unusual inputs, the engine adapts (gray anchors use lightness, extreme colors adapt direction).

---

## Open Questions for Paper Architect

From key-insights.md (refinement questions):

### A. Loop Output Semantics
When a loop strategy is active and N >> one cycle capacity, does output:
- Contain N discrete swatches (loops unrolled into list)?
- Or return one cycle with metadata saying "loops with strategy X"?

**Recommendation**: Document the former (unrolled list).

### B. Preset Specification
Should the paper include a formal presets table? Example in [10_scope_use_cases_presets.md](open-agents/output-refined/research/10_scope_use_cases_presets.md).

**Recommendation**: Yes, include as an appendix or example table.

### C. Categorical Mode Detail
How much algorithmic detail for categorical mode? Full section or note as variant?

**Recommendation**: Full section in [11_modes_of_operation.md](open-agents/output-refined/research/11_modes_of_operation.md) is sufficient; paper can summarize.

---

## Estimated Paper Length

Based on research document lengths and typical academic paper formatting:

| Section | Estimated Pages |
|---------|-----------------|
| Introduction/Scope | 0.5–1 |
| Perceptual Foundations | 1–1.5 |
| Journey Construction | 1.5–2 |
| Perceptual Constraints | 0.5–1 |
| Style Controls | 1–1.5 |
| Modes of Operation | 0.5–1 |
| Loop Strategies | 1–1.5 |
| Gamut Management | 0.5–1 |
| Variation/Determinism | 0.5 |
| API Design | 0.5–1 |
| Caller Responsibilities | 0.5 |
| **Total** | **8–12 pages** |

---

## Ready for Paper Architect

All research materials are consolidated and organized. The Paper Architect can:

1. Use the recommended structure as a starting point
2. Refer to specific documents for each section's content
3. Apply the key themes throughout
4. Address open questions as needed

**Files location**: `open-agents/output-refined/research/`

**Index**: `open-agents/memory/research-index.yaml`
