# Color Journey Engine: Paper Outline

**Status**: Draft Structure  
**Created**: 2024-12-17  
**Author**: Paper Architect (Morgan)  
**Target Length**: 8,000–12,000 words (~8–12 pages)

---

## Document Overview

This specification paper describes the **Color Journey Engine**, a deterministic algorithm for generating perceptually-uniform color palettes. The paper serves as both a formal specification and implementation guide.

### Audience
- Software engineers implementing color systems
- Color scientists and researchers
- UI/UX designers working with programmatic palettes
- Graphics programmers in visualization and generative art

### Key Themes
1. **Discrete Output, Continuous Thinking** — Internal Bézier curves, discrete swatch output
2. **Perceptual Uniformity as Foundation** — OKLab grounds all design decisions
3. **The Journey Is Constructive, Not Prescriptive** — Coherence without usage prescription
4. **Presets Encode Expertise** — Knowledge capture, not simplification
5. **Graceful Edge Case Handling** — Adapt rather than fail

---

## Section Structure

### §1 Introduction and Scope
**File**: `sections/01_introduction.tex`  
**Source**: `10_scope_use_cases_presets.md`  
**Length**: 500–1,000 words

#### Purpose
Establish what the Color Journey Engine does and doesn't do, primary use cases, and design philosophy.

#### Content
- Problem statement: need for perceptually-coherent, deterministic palettes
- What the engine is (palette generator) vs. isn't (color picker, real-time renderer)
- Primary use cases: timelines, data visualization, generative palettes, animation
- Design principles overview
- Paper roadmap

#### Subsections
- 1.1 Motivation
- 1.2 Scope Definition
- 1.3 Design Principles
- 1.4 Paper Organization

---

### §2 Perceptual Color Foundations
**File**: `sections/02_perceptual_foundations.tex`  
**Source**: `01_perceptual_color_foundations.md`  
**Length**: 1,000–1,500 words

#### Purpose
Establish the mathematical and perceptual foundation that underlies all engine decisions.

#### Content
- Why perceptual uniformity matters for palette generation
- OKLab color space: derivation, properties, coordinate meanings (L, a, b)
- OKLCh cylindrical form: lightness, chroma, hue
- Conversion pipeline: sRGB → linear RGB → OKLab
- Mathematical notation conventions for the paper

#### Subsections
- 2.1 The Perceptual Uniformity Requirement
- 2.2 OKLab Color Space
- 2.3 Cartesian vs. Cylindrical Coordinates
- 2.4 Color Space Conversion

#### Dependencies
- None (foundational section)

---

### §3 Journey Construction
**File**: `sections/03_journey_construction.tex`  
**Source**: `02_journey_construction.md`  
**Length**: 1,500–2,000 words

#### Purpose
Define the central "journey" metaphor and how palettes are constructed from anchor colors.

#### Content
- The journey metaphor: constructive device for coherence
- Anchor system: 1–5 colors, guaranteed appearance in output
- Single-anchor "mood expansion" (critical innovation)
- Multi-anchor path construction
- Cubic Bézier curves with C¹ continuity
- Arc-length parameterization for uniform sampling

#### Subsections
- 3.1 The Journey Metaphor
- 3.2 Anchor Colors
- 3.3 Single-Anchor Expansion
- 3.4 Multi-Anchor Paths
- 3.5 Bézier Curve Construction
- 3.6 Arc-Length Parameterization

#### Dependencies
- §2 (OKLab coordinates for path construction)

---

### §4 Perceptual Constraints
**File**: `sections/04_perceptual_constraints.tex`  
**Source**: `03_perceptual_constraints.md`  
**Length**: 500–1,000 words

#### Purpose
Define the constraints that ensure output colors are distinguishable yet harmonious.

#### Content
- Just-noticeable difference (JND) threshold (~2 OKLab units)
- Δ_min constraint: minimum perceptual distance between adjacent colors
- Δ_max constraint: maximum perceptual distance for smooth transitions
- Adaptive sampling algorithm
- Constraint violation handling and fallback behaviors

#### Subsections
- 4.1 Just-Noticeable Difference
- 4.2 Minimum Distance Constraint (Δ_min)
- 4.3 Maximum Distance Constraint (Δ_max)
- 4.4 Adaptive Sampling
- 4.5 Constraint Enforcement

#### Dependencies
- §2 (perceptual distance calculations)
- §3 (path sampling)

---

### §5 User-Facing Style Controls
**File**: `sections/05_style_controls.tex`  
**Source**: `04_dynamic_controls.md`  
**Length**: 1,000–1,500 words

#### Purpose
Document the parameters users can adjust to control palette character.

#### Content
- Temperature: warm/cool bias via direction blending
- Intensity: control point scaling for curve drama
- Smoothness: transition character and continuity
- Additional dynamics: lightness, chroma, contrast, vibrancy, warmth
- Parameter interaction and valid ranges
- Default values and rationale

#### Subsections
- 5.1 Temperature Control
- 5.2 Intensity Control
- 5.3 Smoothness Control
- 5.4 Secondary Parameters
- 5.5 Parameter Interactions

#### Dependencies
- §3 (Bézier control point manipulation)

---

### §6 Modes of Operation
**File**: `sections/06_modes_of_operation.tex`  
**Source**: `11_modes_of_operation.md`  
**Length**: 500–1,000 words

#### Purpose
Distinguish between Journey Mode and Categorical Mode, and when to use each.

#### Content
- Journey Mode: smooth perceptual transitions
- Categorical Mode: maximum distinction between colors
- Perceptual velocity concept
- Mode selection guidelines and decision tree
- Output differences between modes

#### Subsections
- 6.1 Journey Mode
- 6.2 Categorical Mode
- 6.3 Perceptual Velocity
- 6.4 Mode Selection Guidelines

#### Dependencies
- §3 (journey construction)
- §4 (distance constraints)

---

### §7 Loop Strategies
**File**: `sections/07_loop_strategies.tex`  
**Source**: `05_loop_strategies.md`  
**Length**: 1,000–1,500 words

#### Purpose
Define strategies for extending palettes beyond a single path traversal.

#### Content
- Open paths (default, no return)
- Closed loops (return to start color)
- Ping-pong oscillation (reverse at endpoints)
- Möbius half-twist (return with perceptual shift)
- Phased evolution (progressive transformation)
- Output semantics: unrolled lists
- Non-repetition rules

#### Subsections
- 7.1 Open Strategy
- 7.2 Closed Strategy
- 7.3 Ping-Pong Strategy
- 7.4 Möbius Strategy
- 7.5 Phased Strategy
- 7.6 Output Semantics

#### Dependencies
- §3 (path construction)
- §4 (spacing constraints)

---

### §8 Gamut Management
**File**: `sections/08_gamut_management.tex`  
**Source**: `08_gamut_management.md`  
**Length**: 500–1,000 words

#### Purpose
Define how the engine handles colors that fall outside the sRGB gamut.

#### Content
- The sRGB boundary problem in perceptual spaces
- Two-layer strategy: design-time awareness + sample-time correction
- Soft correction philosophy
- Hue preservation priority
- Gamut-aware control point placement

#### Subsections
- 8.1 The Gamut Boundary Problem
- 8.2 Design-Time Gamut Awareness
- 8.3 Sample-Time Correction
- 8.4 Hue Preservation

#### Dependencies
- §2 (color space boundaries)
- §3 (control point placement)

---

### §9 Variation and Determinism
**File**: `sections/09_variation_determinism.tex`  
**Source**: `06_variation_determinism.md`  
**Length**: 400–600 words

#### Purpose
Explain how the engine maintains determinism while supporting controlled variation.

#### Content
- Core determinism requirement: same inputs → same outputs
- Controlled variation layer
- PRNG with explicit seeds
- Reproducibility guarantees
- Version stability considerations

#### Subsections
- 9.1 Determinism Requirement
- 9.2 Controlled Variation
- 9.3 Seed Handling
- 9.4 Reproducibility

#### Dependencies
- None (cross-cutting concern)

---

### §10 API Design and Output Structure
**File**: `sections/10_api_design.tex`  
**Source**: `07_api_design_philosophy.md`  
**Length**: 500–1,000 words

#### Purpose
Define the engine's interface and output format.

#### Content
- Pure function model
- Discrete output: array of swatches, not continuous curves
- Output structure: palette array, config echo, diagnostics
- Format: hex strings + OKLab coordinates
- What's explicitly out of scope

#### Subsections
- 10.1 API Philosophy
- 10.2 Input Parameters
- 10.3 Output Structure
- 10.4 Diagnostic Information
- 10.5 Scope Boundaries

#### Dependencies
- §5 (parameter documentation)

---

### §11 Caller Responsibilities
**File**: `sections/11_caller_responsibilities.tex`  
**Source**: `09_diagnostics_validation.md`, `10_scope_use_cases_presets.md`  
**Length**: 400–600 words

#### Purpose
Define what the engine guarantees and what callers must handle.

#### Content
- Input validation rules
- What the engine cannot guarantee
- User responsibility for context testing (accessibility, contrast)
- Graceful degradation behavior
- Error states and handling

#### Subsections
- 11.1 Input Validation
- 11.2 Engine Guarantees
- 11.3 Caller Responsibilities
- 11.4 Error Handling

#### Dependencies
- §10 (API contract)

---

### §12 Conclusion and Future Directions
**File**: `sections/12_conclusion.tex`  
**Source**: Research synthesis  
**Length**: 400–600 words

#### Purpose
Summarize key contributions and identify areas for future work.

#### Content
- Summary of specification contributions
- Key design decisions recap
- Implementation considerations
- Potential enhancements
- Open questions for future research

#### Subsections
- 12.1 Summary
- 12.2 Key Contributions
- 12.3 Future Directions

#### Dependencies
- All previous sections

---

## Appendices

### Appendix A: Preset Reference
**File**: `appendices/A_presets.tex`  
**Content**: Table of recommended presets with parameter values

### Appendix B: Mathematical Notation
**File**: `appendices/B_notation.tex`  
**Content**: Complete notation reference for the paper

### Appendix C: Implementation Examples
**File**: `appendices/C_examples.tex`  
**Content**: Code examples and usage patterns

---

## Cross-Reference Plan

### Forward References
- §1 → §2: "foundations detailed in §2"
- §3 → §4: "constraints governing sampling (§4)"
- §5 → §3: "parameters affect Bézier construction (§3)"

### Backward References
- §4 → §2: "perceptual distance as defined in §2"
- §6 → §3, §4: "building on journey construction and constraints"
- §12 → all: summary references

### Key Term Definitions
| Term | Defined In | First Used |
|------|------------|------------|
| Perceptual uniformity | §2.1 | §1.1 |
| OKLab | §2.2 | §1.3 |
| Anchor | §3.2 | §1.2 |
| Journey | §3.1 | §1.1 |
| JND | §4.1 | §2.1 |
| Δ_min / Δ_max | §4.2–4.3 | §4.1 |

---

## Section Dependencies Graph

```
§1 Introduction
    ↓
§2 Perceptual Foundations
    ↓
§3 Journey Construction ←──────────────┐
    ↓                                   │
§4 Perceptual Constraints              │
    ↓                                   │
§5 Style Controls ─────────────────────┘
    ↓
§6 Modes of Operation
    ↓
§7 Loop Strategies
    ↓
§8 Gamut Management
    ↓
§9 Variation & Determinism (cross-cutting)
    ↓
§10 API Design
    ↓
§11 Caller Responsibilities
    ↓
§12 Conclusion
```

---

## Writing Order Recommendation

Based on dependencies and logical flow:

1. **Phase 1 - Foundations**: §1, §2
2. **Phase 2 - Core Mechanics**: §3, §4
3. **Phase 3 - User Interface**: §5, §6
4. **Phase 4 - Advanced Features**: §7, §8, §9
5. **Phase 5 - Integration**: §10, §11
6. **Phase 6 - Wrap-up**: §12, Appendices

---

## Research Document Mapping

| Section | Primary Research Document |
|---------|--------------------------|
| §1 | `10_scope_use_cases_presets.md` |
| §2 | `01_perceptual_color_foundations.md` |
| §3 | `02_journey_construction.md` |
| §4 | `03_perceptual_constraints.md` |
| §5 | `04_dynamic_controls.md` |
| §6 | `11_modes_of_operation.md` |
| §7 | `05_loop_strategies.md` |
| §8 | `08_gamut_management.md` |
| §9 | `06_variation_determinism.md` |
| §10 | `07_api_design_philosophy.md` |
| §11 | `09_diagnostics_validation.md` |
| §12 | Synthesis of all documents |

---

*Outline generated by Paper Architect. Ready for Section Drafter to begin writing.*
