# Project Aims & Objectives

**Status:** Active  
**Last updated:** 2024-12-17  
**Author:** Peter Nicholls

## Overall Vision

Create a **formal specification paper** for the Color Journey Engine—a deterministic algorithm that generates perceptually-uniform color palettes. The paper serves as both a technical specification and implementation guide, enabling software engineers and color scientists to understand, implement, and extend the engine.

**Audience:** This paper serves as an internal technical reference for the engineering team developing and maintaining the C-core Color Journey Engine implementation. It documents design rationale, mathematical foundations, and architectural decisions to enable team alignment and prevent knowledge loss.

The paper addresses a gap in existing color palette tools: most rely on ad-hoc heuristics or simple interpolation, producing palettes with inconsistent perceptual spacing. This specification grounds palette generation in color science (OKLab perceptual uniformity) while remaining practical for real-world implementation.

## Primary Objectives

1. **Specify the Core Algorithm** — Define how palettes are constructed from anchor colors using Bézier curves in OKLab space, with clear mathematical foundations
2. **Document Perceptual Constraints** — Establish formal constraints (JND, Δ_min, Δ_max) that ensure visually distinguishable and harmonious colors
3. **Define the Complete API Surface** — Specify inputs, outputs, parameters, modes, and diagnostics for deterministic, reproducible operation
4. **Provide Implementation Guidance** — Enable engineers to implement the specification correctly without ambiguity
5. **Establish Design Philosophy** — Communicate the "why" behind design decisions, not just the "what"

## Success Criteria

- [ ] All 12 sections drafted and refined
- [ ] Mathematical formulas are precise and implementable
- [ ] Key algorithms have pseudocode or formal description
- [ ] API contract is unambiguous (inputs, outputs, error cases)
- [ ] A competent engineer could implement from the spec alone
- [ ] Paper is internally consistent (no contradictions between sections)
- [ ] Terminology is defined before use and consistent throughout
- [ ] Target length achieved (8,000–12,000 words)
- [ ] Team can reference sections during design discussions
- [ ] Section titles are memorable and self-documenting
- [ ] Key decisions have explicit rationale documented
- [ ] Prior art is positioned relative to this approach

## Scope Boundaries

### IN Scope
- OKLab color space and perceptual uniformity foundations
- Journey construction (anchors, Bézier curves, arc-length parameterization)
- Perceptual constraints (JND, Δ_min, Δ_max, adaptive sampling)
- User-facing style controls (temperature, intensity, smoothness, etc.)
- Modes of operation (Journey vs Categorical)
- Loop strategies (open, closed, pingpong, möbius, phased)
- Gamut management (two-layer approach, hue preservation)
- Determinism and seed handling
- API design and output structure
- Caller responsibilities and error handling

### OUT of Scope
- Color naming systems
- Accessibility checking (WCAG contrast ratios)
- Color blindness simulation
- Real-time animation performance
- ICC color management / device profiles
- Comparison with competing tools (brief mention only)
- Implementation in specific languages (examples are illustrative)

## Key Constraints

- **Audience Level**: Assumes familiarity with basic color concepts; explains OKLab from scratch
- **Technical Precision**: Mathematical rigor where needed, but accessible prose for concepts
- **Length**: 8,000–12,000 words (8–12 pages typical academic format)
- **Format**: LaTeX, Harvard-style citations, formal but readable
- **No Deadline**: Quality over speed; iterate until complete
- **Working Reference**: Structure must support non-linear reading and conversational section references ("see mood expansion section")
- **Performance Context**: C-core achieves 5.6M colors/second (microsecond-range per-color), production-grade performance

## Assumptions

- Reader understands basic programming concepts
- Reader has encountered RGB/HSL color spaces before
- Reader may not know OKLab or perceptual color science
- Reader wants to either implement or deeply understand the engine
- Implementation examples are illustrative, not normative (any language acceptable)

---

*This document is the "constitution" of the paper. Return to it when making big decisions or when unsure of direction.*
