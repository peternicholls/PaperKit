# Content Specification

**Status:** Active  
**Last updated:** 2024-12-17  
**Author:** Peter Nicholls

## Paper Direction & Themes

### Core Thesis/Argument

The Color Journey Engine provides a principled approach to color palette generation by grounding all operations in perceptual uniformity (OKLab color space) and using the "journey" metaphor—colors are generated as if traveling along a smooth path through perceptual color space, producing palettes that are both mathematically rigorous and visually coherent.

### Key Themes

1. **Discrete Output, Continuous Thinking** — The engine constructs smooth Bézier curves internally but outputs discrete color swatches. The journey is a construction device, not an exposed API concept.

2. **Perceptual Uniformity as Foundation** — Every design decision is grounded in OKLab's perceptual uniformity. Mathematical operations correspond to visual experience.

3. **The Journey Is Constructive, Not Prescriptive** — Colors are generated "as if" traveling a path—this gives coherence and order, but users can apply colors however they want.

4. **Presets Encode Expertise** — Presets aren't dumbing-down; they capture knowledge about which parameter combinations work well for specific goals.

5. **Graceful Edge Case Handling** — Rather than failing on unusual inputs, the engine adapts (gray anchors use lightness expansion, extreme colors adapt direction).

## Proposed Structure

### Section Overview (12 Sections)

| § | Title | Purpose | Source |
|---|-------|---------|--------|
| 1 | Introduction and Scope | Problem, scope, design philosophy | `10_scope_use_cases_presets.md` |
| 2 | Perceptual Color Foundations | OKLab, coordinates, conversion | `01_perceptual_color_foundations.md` |
| 3 | Journey Construction | Anchors, Bézier curves, arc-length | `02_journey_construction.md` |
| 4 | Perceptual Constraints | JND, Δ_min, Δ_max, adaptive sampling | `03_perceptual_constraints.md` |
| 5 | User-Facing Style Controls | Temperature, intensity, smoothness | `04_dynamic_controls.md` |
| 6 | Modes of Operation | Journey vs Categorical mode | `11_modes_of_operation.md` |
| 7 | Loop Strategies | Open, closed, pingpong, möbius, phased | `05_loop_strategies.md` |
| 8 | Gamut Management | sRGB boundaries, correction | `08_gamut_management.md` |
| 9 | Variation and Determinism | Seeds, reproducibility | `06_variation_determinism.md` |
| 10 | API Design and Output | Input/output structure | `07_api_design_philosophy.md` |
| 11 | Caller Responsibilities | Validation, guarantees, errors | `09_diagnostics_validation.md` |
| 12 | Conclusion | Summary, future directions | Synthesis |

## Content Scope & Priorities

### Must-Have Content (Critical)
- OKLab color space explanation and rationale
- Anchor system (1–5 colors, guaranteed appearance)
- Single-anchor "mood expansion" algorithm
- Cubic Bézier curve construction in OKLab
- Arc-length parameterization for uniform sampling
- JND-based constraints (Δ_min, Δ_max)
- Style parameter definitions and ranges
- Journey vs Categorical mode distinction
- Loop strategy definitions and output semantics
- Gamut correction algorithm
- Determinism guarantees
- Complete API specification

### Nice-to-Have Content
- Detailed preset table (can be appendix)
- Mathematical notation appendix
- Extended code examples
- Visual diagrams of gamut boundaries
- Perceptual velocity analysis

### Out of Scope
- Color naming systems
- WCAG accessibility checking
- Color blindness simulation
- Real-time performance optimization
- Comparison benchmarks with other tools
- Implementation in specific languages (beyond illustrative examples)

## Known Gaps & Research Directions

### Research Gaps

| Gap | Importance | Resolution |
|-----|------------|------------|
| Loop output semantics (N >> cycle) | Critical | **Resolved**: unrolled list |
| Formal preset specification | Nice-to-have | Include in Appendix A |
| Categorical mode algorithm detail | Nice-to-have | Summarize from `11_modes_of_operation.md` |

### Open Questions (from research phase)

1. **Loop Output Semantics** — When N >> one cycle capacity, output is unrolled list (not nested/metadata). ✓ Resolved
2. **Preset Table** — Include formal table in Appendix A. ✓ Planned
3. **Categorical Mode Detail** — Section 6 covers adequately; no separate deep-dive needed.

## Known Sources & Foundation

### Primary Research Documents

All consolidated research is in `open-agents/output-refined/research/`:

| Document | Key Content |
|----------|-------------|
| `01_perceptual_color_foundations.md` | OKLab derivation, coordinates, conversion |
| `02_journey_construction.md` | Anchors, Bézier curves, mood expansion |
| `03_perceptual_constraints.md` | JND, Δ_min/Δ_max, adaptive sampling |
| `04_dynamic_controls.md` | Temperature, intensity, smoothness params |
| `05_loop_strategies.md` | Five loop strategies, output semantics |
| `06_variation_determinism.md` | Seeds, PRNG, reproducibility |
| `07_api_design_philosophy.md` | Engine boundaries, output format |
| `08_gamut_management.md` | sRGB boundaries, soft correction |
| `09_diagnostics_validation.md` | Error handling, caller responsibilities |
| `10_scope_use_cases_presets.md` | Scope, use cases, presets philosophy |
| `11_modes_of_operation.md` | Journey vs categorical, velocity |

### Original Source Materials

- **Primary**: `open-agents/source/ideas/Reasoning.md` (~9000 lines of design discussions)
- **Synthesis**: `open-agents/source/ideas/key-insights.md` (structure recommendations)

### External References to Cite

- Björn Ottosson (2020) — OKLab color space
- Standard Bézier curve mathematics
- Just-noticeable difference literature (perceptual thresholds)

---

*This document evolves as drafting progresses. Update when discovering new themes, changing priorities, or resolving gaps.*
