# Requirements & Technical Specifications

**Status:** Active  
**Last updated:** 2024-12-17  
**Author:** Peter Nicholls

## Document Style & Formatting

### Academic Standards
- **Harvard referencing**: Yes
- **Formal academic tone**: Pragmatic (formal where needed, accessible otherwise)
- **Peer review ready**: Yes (structure and rigor suitable for review)
- **Target venue**: Technical specification / reference document (not journal submission)

### Format and Structure
- **Target length**: 8,000–12,000 words
- **Number of sections**: 12 main sections + 3 appendices
- **Figures/tables required**: Yes
  - Gamut boundary diagram
  - Loop strategy output examples
  - Parameter interaction table
  - Preset reference table
- **Code/examples**: Yes (illustrative, language-agnostic pseudocode + JavaScript examples)
- **Appendices**: Yes
  - A: Preset Reference
  - B: Mathematical Notation
  - C: Implementation Examples

### Visual and Layout Requirements
 - **Structural aids for reference use**:
   - Decision rationale boxes for key architectural choices
   - Liberal cross-references (forward and backward)
   - Quick-reference appendix mapping topics to sections

## Content Technical Requirements
- **Notation conventions**:
  - OKLab coordinates: $L$, $a$, $b$ (italic)
  - OKLCh coordinates: $L$, $C$, $h$
 - **Source accessibility**: Open sources only (team must be able to access all citations)
   - Prefer: W3C specs, public blogs (Ottosson), technical reports
   - Avoid: Paywalled academic journals
 - **Citation strategy**: Strategic over comprehensive
   - Foundational (establish credibility): 5-8 citations
   - Comparative (justify choices): 3-5 citations
   - Validating (ground claims): 2-3 citations
  - Bézier parameter: $t \in [0, 1]$
  - Arc-length parameter: $s$
- **Data/evidence standards**: Theoretical specification; empirical values (JND ~2) cited from literature
- **Reproducibility expectations**: Yes—specification must enable deterministic reproduction

### Research and Citations
- **Minimum citation density**: Light (specification paper, not literature review)
- **Source types acceptable**: 
 - **Code examples**: Minimal in main text (extensive technical docs exist)
 - **Focus**: Design rationale and "why" over implementation "how"
 - **Performance notes**: Brief mentions of C-core characteristics where relevant (microsecond-range, production-ready)
- **Recency requirements**: Flexible (foundational work may be older)
- **Coverage breadth**: Selective (cite what's directly relevant)

## Quality Standards

### Baseline Expectations
- **Clarity**: Explain concepts so a competent engineer can implement
- **Rigor**: Mathematically precise where needed; pragmatic for concepts
- **Completeness**: Sufficient for implementation (no critical gaps)
- **Polish**: Review-ready; suitable for technical documentation

### Known Constraints or Flexibility
- **If gaps in research**: Note as "implementation-defined" or "future work"
- **If sources incomplete**: Acceptable for original specification content
- **Standards flexibility**: 
  - Mathematical precision: strict
  - Prose style: pragmatic (clear > formal)
  - Citation density: light is acceptable

## Specific Technical Decisions

### Mathematical Precision
- All formulas must be implementable (no hand-waving)
- Pseudocode for key algorithms (adaptive sampling, gamut correction)
- Units and ranges specified for all parameters

### API Specification
- Input parameters with types, ranges, defaults
- Output structure with field descriptions
- Error states and handling behavior
- Diagnostic information format

### Implementation Guidance
- Language-agnostic where possible
- JavaScript examples in appendix (illustrative)
- Note implementation choices vs. specification requirements

---

*This document drives agent behavior. Agents check here when unsure whether to be strict or pragmatic.* Return to this when requirements change.
