# Section Drafter Handoff: Color Journey Engine Specification

## Overview

This document provides a comprehensive handoff from the Paper Architect to the Section Drafter for writing the Color Journey Engine specification paper. It summarizes the established structure, provides section-by-section writing guidance, and identifies key resources.

**Paper Title:** Color Journey Engine: A Perceptually-Uniform Palette Generation Specification  
**Target Length:** 8,000–12,000 words (~10,000 target)  
**Structure:** 12 main sections + 3 appendices  
**Status:** Structure complete, ready for drafting

---

## Project Foundation

### Canonical Documents

Before drafting, consult these documents in `open-agents/planning/0000-Project-Overview/`:

| Document | Purpose |
|----------|---------|
| `aims-and-objectives.md` | Vision, objectives, success criteria, scope boundaries |
| `requirements.md` | Technical specs, formatting, notation, quality standards |
| `content-specification.md` | Key themes, content priorities, source mapping |

### Five Key Themes

Weave these themes throughout the paper:

1. **Discrete Output, Continuous Thinking** — Internal Bézier curves produce discrete swatches
2. **Perceptual Uniformity as Foundation** — OKLab grounds all design decisions
3. **The Journey Is Constructive, Not Prescriptive** — Coherence without usage prescription
4. **Presets Encode Expertise** — Knowledge capture, not simplification
5. **Graceful Edge Case Handling** — Adapt rather than fail

---

## Section Writing Guide

### Phase 1: Foundations (Draft First)

#### §1 Introduction and Scope
**File:** `latex/sections/01_introduction.tex`  
**Source:** `open-agents/output-refined/research/10_scope_use_cases_presets.md`  
**Target:** ~900 words

**Subsections:**
- 1.1 Motivation (~200 words) — Why perceptually-coherent palettes matter
- 1.2 Scope Definition (~250 words) — What engine IS vs. ISN'T
- 1.3 Design Principles (~300 words) — The five key themes introduced
- 1.4 Paper Organization (~150 words) — Roadmap

**Key Points:**
- Hook: "Color palette generation is ubiquitous, but principled approaches are rare"
- Clearly state what's in/out of scope early
- Introduce "journey" metaphor without full explanation (deferred to §3)
- End with paper roadmap

---

#### §2 Perceptual Color Foundations
**File:** `latex/sections/02_perceptual_foundations.tex`  
**Source:** `open-agents/output-refined/research/01_perceptual_color_foundations.md`  
**Target:** ~1,250 words

**Subsections:**
- 2.1 Perceptual Uniformity Requirement (~300 words)
- 2.2 OKLab Color Space (~400 words)
- 2.3 Cartesian vs. Cylindrical Coordinates (~300 words)
- 2.4 Color Space Conversion (~250 words)

**Key Points:**
- Explain why RGB/HSL fail for palette generation
- Introduce OKLab (cite Björn Ottosson, 2020)
- Define L, a, b coordinates with meaning
- Show OKLCh cylindrical form
- Include distance formula: $\Delta E_{OK} = \sqrt{(L_2-L_1)^2 + (a_2-a_1)^2 + (b_2-b_1)^2}$
- Conversion pipeline (can be brief, point to implementation)

---

### Phase 2: Core Mechanics

#### §3 Journey Construction
**File:** `latex/sections/03_journey_construction.tex`  
**Source:** `open-agents/output-refined/research/02_journey_construction.md`  
**Target:** ~1,750 words (largest section)

**Subsections:**
- 3.1 The Journey Metaphor (~250 words)
- 3.2 Anchor Colors (~300 words)
- 3.3 Single-Anchor Expansion (~400 words) — **Critical innovation**
- 3.4 Multi-Anchor Paths (~300 words)
- 3.5 Bézier Curve Construction (~400 words)
- 3.6 Arc-Length Parameterization (~300 words)

**Key Points:**
- Journey = construction device, not exposed API
- Anchors guaranteed in output (not "close to")
- Single-anchor "mood expansion" is unique contribution
- Bézier formula: $B(t) = (1-t)^3 P_0 + 3(1-t)^2 t P_1 + 3(1-t) t^2 P_2 + t^3 P_3$
- Arc-length parameterization enables uniform sampling

---

#### §4 Perceptual Constraints
**File:** `latex/sections/04_perceptual_constraints.tex`  
**Source:** `open-agents/output-refined/research/03_perceptual_constraints.md`  
**Target:** ~750 words

**Subsections:**
- 4.1 Just-Noticeable Difference (~200 words)
- 4.2 Minimum Distance Constraint (~200 words)
- 4.3 Maximum Distance Constraint (~200 words)
- 4.4 Adaptive Sampling (~250 words)
- 4.5 Constraint Enforcement (~150 words)

**Key Points:**
- JND ≈ 2 OKLab units (cite perceptual research)
- Δ_min ensures distinguishability
- Δ_max ensures coherence (no jarring jumps)
- Adaptive sampling algorithm (pseudocode helpful)
- What happens when constraints conflict

---

### Phase 3: User Interface

#### §5 User-Facing Style Controls
**File:** `latex/sections/05_style_controls.tex`  
**Source:** `open-agents/output-refined/research/04_dynamic_controls.md`  
**Target:** ~1,250 words

**Subsections:**
- 5.1 Temperature Control (~300 words)
- 5.2 Intensity Control (~300 words)
- 5.3 Smoothness Control (~300 words)
- 5.4 Secondary Parameters (~250 words)
- 5.5 Parameter Interactions (~200 words)

**Key Points:**
- Each parameter: range, default, effect, formula if applicable
- Temperature: warm/cool bias via direction blending
- Intensity: control point scaling
- Smoothness: continuity enforcement
- Note parameter independence/interaction

---

#### §6 Modes of Operation
**File:** `latex/sections/06_modes_of_operation.tex`  
**Source:** `open-agents/output-refined/research/11_modes_of_operation.md`  
**Target:** ~750 words

**Subsections:**
- 6.1 Journey Mode (~250 words)
- 6.2 Categorical Mode (~250 words)
- 6.3 Perceptual Velocity (~200 words)
- 6.4 Mode Selection Guidelines (~200 words)

**Key Points:**
- Journey = smooth transitions (default)
- Categorical = maximum distinction
- Include decision table/flowchart for mode selection
- Perceptual velocity = rate of change along journey

---

### Phase 4: Advanced Features

#### §7 Loop Strategies
**File:** `latex/sections/07_loop_strategies.tex`  
**Source:** `open-agents/output-refined/research/05_loop_strategies.md`  
**Target:** ~1,250 words

**Subsections:**
- 7.1 Open Strategy (~200 words)
- 7.2 Closed Strategy (~200 words)
- 7.3 Ping-Pong Strategy (~200 words)
- 7.4 Möbius Strategy (~250 words)
- 7.5 Phased Strategy (~200 words)
- 7.6 Output Semantics (~250 words)

**Key Points:**
- All strategies output flat array (unrolled)
- Table showing example outputs for each strategy
- Möbius is interesting (half-twist return)
- Non-repetition rule: adjacent colors never identical

---

#### §8 Gamut Management
**File:** `latex/sections/08_gamut_management.tex`  
**Source:** `open-agents/output-refined/research/08_gamut_management.md`  
**Target:** ~750 words

**Subsections:**
- 8.1 Gamut Boundary Problem (~250 words)
- 8.2 Design-Time Gamut Awareness (~250 words)
- 8.3 Sample-Time Correction (~250 words)
- 8.4 Hue Preservation (~200 words)

**Key Points:**
- OKLab can represent colors outside sRGB
- Two-layer approach: prevention + correction
- Correction reduces chroma, preserves hue
- Diagram of sRGB boundary in OKLab would help

---

#### §9 Variation and Determinism
**File:** `latex/sections/09_variation_determinism.tex`  
**Source:** `open-agents/output-refined/research/06_variation_determinism.md`  
**Target:** ~500 words

**Subsections:**
- 9.1 Determinism Requirement (~150 words)
- 9.2 Controlled Variation (~150 words)
- 9.3 Seed Handling (~150 words)
- 9.4 Reproducibility (~150 words)

**Key Points:**
- Same inputs = same outputs (pure function)
- Variation only via explicit seed parameter
- Config echo in output enables reproduction

---

### Phase 5: Integration

#### §10 API Design and Output Structure
**File:** `latex/sections/10_api_design.tex`  
**Source:** `open-agents/output-refined/research/07_api_design_philosophy.md`  
**Target:** ~750 words

**Subsections:**
- 10.1 API Philosophy (~200 words)
- 10.2 Input Parameters (~200 words)
- 10.3 Output Structure (~200 words)
- 10.4 Diagnostic Information (~150 words)
- 10.5 Scope Boundaries (~150 words)

**Key Points:**
- Parameter table with types, ranges, defaults
- Output JSON structure example
- Diagnostics are informational, not errors
- Explicit out-of-scope list

---

#### §11 Caller Responsibilities
**File:** `latex/sections/11_caller_responsibilities.tex`  
**Source:** `open-agents/output-refined/research/09_diagnostics_validation.md`  
**Target:** ~500 words

**Subsections:**
- 11.1 Input Validation (~150 words)
- 11.2 Engine Guarantees (~150 words)
- 11.3 Caller Responsibilities (~200 words)
- 11.4 Error Handling (~100 words)

**Key Points:**
- Clear contract: what engine guarantees vs. caller must handle
- Accessibility is caller's responsibility
- No silent failures

---

### Phase 6: Wrap-up

#### §12 Conclusion and Future Directions
**File:** `latex/sections/12_conclusion.tex`  
**Source:** Synthesis of all research  
**Target:** ~500 words

**Subsections:**
- 12.1 Summary (~200 words)
- 12.2 Key Contributions (~200 words)
- 12.3 Future Directions (~200 words)

**Key Points:**
- Recap the specification's approach
- List concrete contributions (5-6 bullet points)
- Future: extended gamuts, accessibility integration, ML presets

---

## Appendices

### Appendix A: Preset Reference
**File:** `latex/appendices/A_presets.tex`  
**Content:** Table of recommended presets with all parameter values

### Appendix B: Mathematical Notation
**File:** `latex/appendices/B_notation.tex`  
**Content:** Complete notation reference (L, a, b, C, h, Δ, etc.)

### Appendix C: Implementation Examples
**File:** `latex/appendices/C_examples.tex`  
**Content:** JavaScript code examples (illustrative, not normative)

---

## Research Document Index

All source documents in `open-agents/output-refined/research/`:

| Document | Section(s) |
|----------|------------|
| `01_perceptual_color_foundations.md` | §2 |
| `02_journey_construction.md` | §3 |
| `03_perceptual_constraints.md` | §4 |
| `04_dynamic_controls.md` | §5 |
| `05_loop_strategies.md` | §7 |
| `06_variation_determinism.md` | §9 |
| `07_api_design_philosophy.md` | §10 |
| `08_gamut_management.md` | §8 |
| `09_diagnostics_validation.md` | §11 |
| `10_scope_use_cases_presets.md` | §1 |
| `11_modes_of_operation.md` | §6 |

---

## Writing Guidelines

### Tone
- Formal but accessible
- Explain concepts before using them
- Technical precision where needed, pragmatic elsewhere

### Mathematical Content
- Use LaTeX equation environments
- Number important equations
- Define all symbols at first use

### Cross-References
- Use `\label` and `\ref` for sections
- Forward reference sparingly ("as detailed in §X")
- Back reference freely ("recall from §X that...")

### Citations
- Harvard style (author, year)
- Light density (specification paper, not literature review)
- Key citations: Ottosson (2020) for OKLab, standard Bézier references

---

## Tracking

Update `open-agents/memory/section-status.yaml` as sections progress:
- `skeleton` → `drafted` → `refined` → `final`
- Track word counts
- Note any issues or deviations

---

## Ready for Section Drafter

**Recommended starting point:** §1 Introduction, then §2 Perceptual Foundations

Each section file contains detailed placeholders. Read the corresponding research document, then write content following the subsection structure.

**Questions?** Consult the canonical documents in `open-agents/planning/0000-Project-Overview/` or the detailed outline in `.paper/data/output-drafts/outlines/paper_outline.md`.
