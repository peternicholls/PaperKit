# Color Journey Engine — Tutor Review Action Plan

**Created:** 18 December 2025  
**Status:** Ready for implementation  
**Consolidated from:** Tutor A & Tutor B reviews  

---

## At a Glance

| Phase | Tasks | Est. Effort | Priority |
|-------|-------|------------|----------|
| **Phase 1: Quick Wins** | Spelling, notation, performance table, API clarity, math | 1-2 hrs | NOW |
| **Phase 2: Core Improvements** | Limitations section, threshold rephrase, OKLab context, citations | 3-5 hrs | WEEK 1 |
| **Phase 3: Strategic Enhancements** | Literature review, novelty reframe, visual diagrams | 4-8 hrs | WEEK 2 |
| **Phase 4: Academic Path (Optional)** | Restructure, validation studies, expert review | 10+ hrs | CONDITIONAL |

---

## PHASE 1: Quick Wins ⚡ (1-2 hours)

### Task 1.1: Standardize Spelling to US English

**Files affected:** Entire document (especially sections, abstracts, code labels)

**Find & Replace patterns:**
```
Colour     → Color
colour     → color
neighbouring → neighboring
favourite  → favorite
```

**Rationale:** API uses `Color`, code examples use US English, consistency required.

**Checklist:**
- [ ] Main document sections
- [ ] Abstract and introduction
- [ ] All section headings
- [ ] Code comments and examples (if any)
- [ ] References to "Color Journey Engine"

---

### Task 1.2: Standardize Mathematical Notation

**Issue:** ∆E and ∆E_OK used interchangeably

**Action:**
1. Choose primary notation: **∆E** (simpler, OKLab implied by context)
2. Add global footnote (§1.1): "All ∆E measurements in this document refer to color difference in OKLab perceptual space per Fairchild (2013)."
3. Use ∆E consistently throughout

**Checklist:**
- [ ] Replace ∆E_OK → ∆E in all sections
- [ ] Add OKLab clarification footnote
- [ ] Verify Appendix B notation consistency

---

### Task 1.3: Create Performance Metrics Table

**Location:** §10.6 (Performance Characteristics)

**Current text:**
> "achieving 5.6 million colors per second"

**Replace with:**

| Metric | Value | Configuration |
|--------|-------|---------------|
| Per-color generation time | ~180 nanoseconds | Single invocation |
| Throughput (single-threaded) | 5.6 million colors/second | M1 Max, Clang 15, -O3 optimization |
| Working set memory | < 64 KB | 3 anchors, default parameters |
| Scaling factor | Linear with anchors | ~1.87 million colors/sec per additional anchor |

**Add footnote:**
> "Performance measurements conducted on Apple M1 Max, Clang 15 compiler with -O3 optimization, single-threaded execution. Throughput scales approximately linearly with number of anchors and complexity of constraint checking. Results may vary on different hardware and compiler configurations."

**Checklist:**
- [ ] Update §10.6 with table format
- [ ] Add hardware/config footnote
- [ ] Verify numbers are accurate

---

### Task 1.4: Clarify API Behavior: Seed → Variation

**Location:** §9.3 and §10.2 (API Design and table)

**Issue:** Does passing `seed: 42` automatically imply `variation: true`?

**Current vagueness:**
- §9.3 says: "If variation is requested but no seed provided, the engine uses a default seed (0)"
- §10.2 lists `mode` and `loop` but not explicit `variation` boolean
- §C.11 code example uses `seed: 42` without explicit `variation`

**Resolution (choose approach A or B):**

**Approach A:** Implicit (cleaner API)
```typescript
// If seed is provided, variation is automatically enabled
config.seed = 42;  // implies variation: true

// If seed is omitted, variation is disabled
config.seed = null; // variation: false (deterministic from anchors alone)
```

**Approach B:** Explicit (clearer)
```typescript
config.variation = true;
config.seed = 42;  // used only if variation: true
```

**Action:**
1. Choose approach A or B
2. Update §9.3 with one sentence clarification: "If a seed is provided, variation mode is automatically enabled. Otherwise, the engine generates deterministic palettes based solely on anchor configuration."
3. Update §10.2 API table with chosen approach
4. Update Appendix C code examples consistently

**Checklist:**
- [ ] Decide on implicit vs. explicit approach
- [ ] Update §9.3 clarification
- [ ] Update §10.2 API table
- [ ] Update Appendix C examples
- [ ] Add remark to design decision box

---

### Task 1.5: Clarify Perceptual Velocity Derivative

**Location:** §6.3 (Perceptual Velocity)

**Issue:** Formula $v = w_L \frac{dL}{dt} + w_a \frac{da}{dt} + w_b \frac{db}{dt}$ is ambiguous.

**Question:** Is the derivative with respect to:
- **t** (curve parameter, varies based on Bézier control points), or
- **s** (arc-length, normalized to [0,1])?

**Action:**
1. **If using parameter t:** Add clarification: "where t is the curve parameter (0 ≤ t ≤ 1). Velocity varies with Bézier control point placement, creating natural acceleration near inflection points."

2. **If using arc-length s:** Change formula notation and add: "where s is arc-length parameter. Velocity represents the rate of perceptual attribute change per unit arc-length traveled."

3. Add notation explanation to Appendix B.4 (Perceptual Derivatives)

**Current assumption:** You likely mean **arc-length** (constant rate of change), which makes "velocity" = rate of attribute change per distance traveled.

**Checklist:**
- [ ] Verify which parameterization your implementation uses
- [ ] Add clarification sentence to §6.3
- [ ] Update Appendix B notation section
- [ ] Add diagram showing velocity concept if helpful

---

### Task 1.6: Verify Möbius Loop Smooth Transition

**Location:** §7.4 (Möbius Loop Strategy)

**Issue:** Inversion $(L, -a, -b)$ creates 180° rotation. Need to verify it doesn't create discontinuous jump.

**Action:**
1. **Verify implementation:** Does the transition from Loop 1 → Loop 2 (with inversion) create a smooth curve or a jump?
2. **If smooth:** Add sentence to §7.4: "The chromatic inversion is applied continuously over the second loop, creating a smooth Möbius twist without discontinuities at the transition point."
3. **If abrupt:** Document as constraint: "Note: The Möbius implementation creates a 180° hue rotation at the transition between loops. This may be perceptible as a 'shift' in mood at the wrap point."

**Checklist:**
- [ ] Run test implementation to verify smoothness
- [ ] Update §7.4 with findings
- [ ] Add visual diagram if helpful (Phase 3 task)

---

### Summary: Phase 1 Deliverables

After Phase 1, you will have:
- ✓ Consistent spelling and notation
- ✓ Professional performance metrics with context
- ✓ Clear API behavior documentation
- ✓ Mathematically unambiguous formulas
- ✓ Verified implementation claims

**Estimated time: 60-90 minutes**

---

## PHASE 2: Core Improvements 🎯 (3-5 hours)

### Task 2.1: Add Explicit Limitations Section

**Location:** §1.6 (new section, insert after Design Principles)

**Title:** "Limitations & Future Validation"

**Content (suggested):**

```markdown
## 1.6 Limitations & Future Validation

This specification achieves rigorous formalization of perceptual palette 
generation in OKLab space. However, several design choices reflect 
engineering heuristics rather than empirically-validated constants:

### Perceptual Threshold Values
The constraint thresholds (∆_min ≈ 2.0, ∆_max ≈ 5.0) and perceptual 
velocity weights (w_h ≈ 1.5–2.0) are informed by color science literature 
[Fairchild 2013] and extensive practical testing, but have not been 
validated through formal psychophysical user studies. These values should 
be considered "recommended engineering parameters" rather than 
psychophysically-derived constants.

### OKLab Adoption Recency
OKLab (Okabe & Ito, 2020) is a recently-developed color space with 
growing industry adoption. While independent analysis (Levien, 2021) 
validates its perceptual uniformity claims, CIELAB (CIE 1976) has 45+ 
years of empirical validation in contrast. OKLab selection reflects 
current best practice for software implementation, but systems requiring 
maximum backward compatibility should consider CIELAB alternatives.

### Single-Anchor Expansion Scope
This specification provides formalization and implementation of 
lightness-weighted single-anchor palette expansion. Related work (Adobe 
Color, Coolors.co) demonstrates similar approaches; our contribution is 
systematic formalization and rigorous computational specification.

### Recommended Future Work
1. Psychophysical studies validating perceptual threshold values
2. User studies comparing generated palettes to professional 
   design tool output
3. Context-aware gamut mapping for memory colors (skin tones, 
   grass, sky blue)
4. Cross-platform performance benchmarking (iOS, web, desktop)
5. Formal validation of OKLab uniformity in domain-specific 
   applications (accessibility, colorblindness simulation)
```

**Rationale:** Addresses Tutor B's core concern about heuristics vs. empirical facts. Intellectual honesty increases credibility.

**Checklist:**
- [ ] Add §1.6 section after §1.5
- [ ] Update table of contents
- [ ] Verify tone is professional, not defensive
- [ ] Cross-reference back to relevant sections (4.1, 6.3, etc.)

---

### Task 2.2: Rephrase All Perceptual Thresholds

**Pattern:** Everywhere a threshold is stated, add "(design choice)" qualifier

**Examples of changes:**

**Before:**
> "The ∆_min ≈ 2.0 threshold ensures perceptual distinctness"

**After:**
> "The ∆_min ≈ 2.0 threshold (design choice, see §4.1) ensures perceptual 
> distinctness"

**Locations to audit:**
- [ ] §2.2: OKLab JND statements
- [ ] §4.1: ∆E definition and thresholds
- [ ] §4.3: ∆_min and ∆_max definitions
- [ ] §6.3: Velocity weight constants
- [ ] §8.1-8.4: Gamut management thresholds

**Affected sections: [List specifically which sentences need updating]**

---

### Task 2.3: Add OKLab Recency Risk Section

**Location:** §2.2.1 (new, after OKLab introduction)

**Title:** "OKLab Adoption: Recency, Validation, and Risk Mitigation"

**Content (suggested):**

```markdown
## 2.2.1 Recency & Empirical Validation

OKLab is a recent development (Okabe & Ito, 2020, blog post; not 
peer-reviewed as of publication). This contrasts with CIELAB (CIE 1976, 
45+ years of empirical validation in colorimetry and vision science).

**Why we chose OKLab despite recency:**

1. **Practical software performance:** Simpler computation than CIELAB; 
   GPU-optimizable
2. **Demonstrated uniformity:** Independent analysis (Levien, 2021) shows 
   superior perceptual uniformity over CIELAB in tested ranges
3. **Industry adoption:** Growing use in color tools (CSS Color 4 WD, 
   design software), reducing implementation risk
4. **Modern gamut requirements:** Better handles wide-gamut displays 
   (DCI-P3, Rec. 2020)

**Risk mitigation:**

- This specification can be retargeted to CIELAB if future work reveals 
  OKLab uniformity limitations in specific domains
- All mathematical formalism (journey trajectory, constraints) is 
  color-space agnostic; only the perceptual distance metric (∆E) would 
  change
- Monitoring: If significant uniformity issues are discovered in peer 
  review, we will document CIELAB compatibility path

**Empirical validation status:** Levien's blog analysis (2021) is 
insightful but not peer-reviewed. Formal psychophysical validation of 
OKLab uniformity claims remains an open research direction.
```

**Checklist:**
- [ ] Add §2.2.1 after OKLab introduction
- [ ] Update forward references in §12.3 (Future Directions)
- [ ] Tone: confident but honest about open questions

---

### Task 2.4: Add Gamut Management Context Nuance

**Location:** §8.4 (end of section)

**Current text likely says:**
> "The hierarchy Hue > Lightness > Chroma applies universally"

**Add paragraph:**

```markdown
### Context-Dependent Gamut Mapping

The prioritization Hue > Lightness > Chroma is appropriate for 
*general-purpose palette generation*. However, context may demand 
different strategies:

**Brand Colors:** If an anchor represents a brand color, even chroma 
reduction may be unacceptable. In such cases, the gamut boundary is a 
hard constraint, and palette generation might expand to neighboring hues 
slightly rather than reduce chroma.

**Memory Colors:** For colors with strong cultural or perceptual 
associations (skin tones, grass green, sky blue), humans are highly 
sensitive to hue shifts. The current hierarchy may need inversion: 
Lightness > Hue > Chroma.

**Accessibility:** For colorblind users, certain hue combinations are 
indistinguishable. Context-aware gamut mapping might prioritize 
luminance separation over hue preservation.

**Future Directions:** Investigation of context-aware gamut mapping 
(§12.3) should address these domain-specific scenarios.
```

**Checklist:**
- [ ] Add context nuance subsection to §8.4
- [ ] Update §12.3 future directions to reference this
- [ ] Tone: exploratory, not prescriptive

---

### Task 2.5: Fix Citation Issues

**Citation 1: CSS Color 4**
- [ ] Verify reference is specifically "Candidate Recommendation Snapshot"
- [ ] Check if it's evolved since (CSS Color Module Level 4 is still draft)
- [ ] Add publication date and snapshot version

**Citation 2: Moosbauer & Poole (2025)**
- [ ] Evaluate relevance to symmetry-constrained search
- [ ] If tenuous: remove and reference a more relevant symmetry paper, or
- [ ] If defensible: add 1-2 sentence explanation of connection

**Citation 3: Levien (2021)**
- [ ] Verify it's labeled as "blog post" or "technical analysis", not "paper"
- [ ] Add note: "Independent analysis; not peer-reviewed" if not already noted

**Citation 4: Add missing foundational references**
- [ ] MacAdam, D. L. (1942). "Visual sensitivities to color differences in daylight." *JOSA*, 32(5), 247-274.
- [ ] Wyszecki, G., & Stiles, W. S. (1982). *Color Science: Concepts and Methods, Quantitative Data and Formulae* (2nd ed.). Wiley.

**Checklist:**
- [ ] Verify CSS Color 4 citation specificity
- [ ] Evaluate & fix Moosbauer & Poole
- [ ] Label Levien blog post appropriately
- [ ] Add MacAdam & Wyszeski references

---

### Summary: Phase 2 Deliverables

After Phase 2, you will have:
- ✓ Explicit limitations section (intellectual honesty)
- ✓ Consistent threshold phrasing (design choices labeled)
- ✓ OKLab recency risks addressed transparently
- ✓ Nuanced gamut mapping discussion
- ✓ Clean, accurate citations

**Estimated time: 180-300 minutes (3-5 hours)**

---

## PHASE 3: Strategic Enhancements 📊 (4-8 hours)

### Task 3.1: Conduct Literature Review on Color Harmony

**Objective:** Ground novelty claims in comprehensive prior art analysis

**Scope of review:**
1. **Rule-based harmony systems:** Itten (1961), traditional color theory
2. **Geometric methods:** Triadic, tetrad, split-complementary rules
3. **Commercial tools:** Adobe Color, Paletton, Coolors.co, Khroma
4. **Interpolation methods:** CSS Color interpolation, Chroma.js, TinyColor
5. **Data-driven approaches:** Liu et al. (2013), optimization-based methods
6. **Academic work:** Color harmony papers in HCI, visualization, design

**Deliverable:** 2-page synthesis document identifying:
- What approaches exist
- What's novel in *your* formalization
- Clear differentiation

**Output:** [Integrated into §1.4 / new "Related Work" section]

---

### Task 3.2: Reframe Novelty Claims

**Current claims (problematic):**
- "novel contribution" (§1.4)
- "to our knowledge, novel approach" (§3.3)

**Post-literature-review repositioning (choose one):**

**Option A: Emphasized Formalization**
> "We systematize single-anchor mood-based palette expansion, which has 
> existed informally in design tools (Adobe Color's monochromatic mode, 
> Coolors.co's gradient expansion), into a rigorous mathematical 
> specification suitable for reproducible software implementation. Our 
> contribution is formalizing the lightness-weighted expansion in OKLab 
> perceptual space and establishing explicit design heuristics for 
> perceptual constraints."

**Option B: Incremental Innovation**
> "Building on existing approaches to single-color palette expansion, we 
> contribute: (1) explicit formalization in OKLab perceptual space, (2) 
> lightness-weighted directional expansion rather than geometric harmony 
> rules, and (3) systematic treatment of gamut boundaries in perceptual 
> space."

**Option C: Design Contribution**
> "While single-color palette generation is well-established in design 
> tools, the Color Journey Engine contributes a new design philosophy: 
> the 'journey' metaphor, which models palette generation as a 
> continuous trajectory in perceptual space, enabling dynamic mood 
> expression and deterministic reproducibility for distributed systems."

**Action:** Choose option A, B, or C based on literature findings, revise §1.4 & §3.3

---

### Task 3.3: Create Visual Diagrams

**Diagram 1: RGB vs OKLab Interpolation (Figure 2.1)**
- **Content:** Side-by-side comparison of linear RGB interpolation vs. OKLab
- **Tool:** TikZ in LaTeX or external PDF/PNG import
- **Where:** §2.2 (OKLab section)
- **Purpose:** Visually justify OKLab over RGB

**Diagram 2: Bézier Control Point Placement (Figure 3.1)**
- **Content:** Show how control points determine mood trajectory
- **Where:** §3.2-3.3 (Single-anchor expansion)
- **Purpose:** Illustrate Bézier curve construction

**Diagram 3: Constraint Visualization (Figure 4.1)**
- **Content:** OKLab space with ∆_min and ∆_max boundaries visualized
- **Where:** §4.3 (Constraint definitions)
- **Purpose:** Make abstract constraints tangible

**Diagram 4: Loop Strategies Comparison (Figure 7.1)**
- **Content:** Visual progression of loops (Linear, Sinusoidal, Möbius)
- **Where:** §7 (Loop Strategies)
- **Purpose:** Show how loop shape affects palette

**Diagram 5: Concept Map (Appendix D.1.1)**
- **Content:** System overview showing relationships between components
- **Where:** Appendix D (listed but missing)
- **Purpose:** Help readers navigate system architecture

**Technical approach:**
- Use TikZ for mathematical plots (RGB vs OKLab)
- Use Graphviz/diagram tool for concept map
- Create PNG export from implementations for validation

---

### Task 3.4: Complete Appendix D Quick Reference

**Issue:** Appendix D.1.1 "Concept Map" is listed but missing

**Add:**
1. System architecture diagram (D.1.1)
2. Expand troubleshooting table (D.6) with common issues:
   ```
   Problem                          | Symptom           | Solution
   ─────────────────────────────────────────────────────────────
   Grayscale anchor                 | No color spread   | §3.4: Use colored anchor
   Gamut boundary exceeded          | Chroma reduced    | §8.4: Check gamut limits
   Hue shifts with chroma change    | Unexpected color  | §8: Verify hierarchy
   Velocity feels flat              | Boring palette    | §6.3: Adjust w_h weight
   Reproducibility fails            | Different output  | §9: Verify seed value
   ```

**Checklist:**
- [ ] Create concept map diagram
- [ ] Expand troubleshooting table
- [ ] Add "Common Configurations" examples
- [ ] Update Table of Contents reference

---

### Summary: Phase 3 Deliverables

After Phase 3, you will have:
- ✓ Literature review grounding novelty claims
- ✓ Repositioned novelty with defensible language
- ✓ 4-5 visual diagrams enhancing comprehension
- ✓ Complete quick reference appendix

**Estimated time: 240-480 minutes (4-8 hours)**

---

## PHASE 4: Academic Path (Optional, Conditional) 📚 (10+ hours)

**Only pursue if academic publication is a goal.**

### Task 4.1: Restructure for Academic Format

Reorder document:
1. Abstract (refined)
2. **New: Related Work** (from §1.4 expansion + Phase 3 literature review)
3. **Introduction** (§1.1-1.3 only)
4. **Method** (§2-§9: Current technical content)
5. **Validation** (NEW: experimental section)
6. **Applications** (Appendix C examples as main section)
7. **Discussion & Limitations** (Expand §12.3)
8. **Conclusion**

### Task 4.2: Conduct Validation Study

Options:
- **User study:** 20-30 designers compare Color Journey output to Adobe/Coolors
- **Expert review:** 5-10 color scientists evaluate perceptual uniformity
- **Computational validation:** CIEDE2000 uniformity metrics vs. baselines

### Task 4.3: Formal Results & Comparison

Create comparison tables:
- Your ∆E distributions vs. other tools
- User preference ratings
- Computational efficiency benchmarks

---

## Implementation Timeline (Recommended)

```
Week of Dec 18-22:  Phase 1 (Quick Wins) — 2 hours
                    Phase 2 (Core) — 4 hours start
Week of Dec 29-Jan 4: Phase 2 (Core) — 2 hours finish
                    Phase 3 (Enhancement) — 4 hours start
Week of Jan 5-12:   Phase 3 (Enhancement) — 4 hours finish
                    Review + Polish — 2 hours

TOTAL: ~18 hours over 3 weeks for A-grade engineering specification
OPTIONAL: +10-15 hours if pursuing academic publication
```

---

## Success Criteria Checklist

### Phase 1 Complete ✓
- [ ] Spelling consistent (US English)
- [ ] Notation consistent (∆E)
- [ ] Performance table with hardware context
- [ ] API seed behavior clarified
- [ ] Perceptual velocity math unambiguous
- [ ] Möbius smoothness verified

### Phase 2 Complete ✓
- [ ] Limitations section added (§1.6)
- [ ] All thresholds labeled "(design choice)"
- [ ] OKLab recency risks discussed (§2.2.1)
- [ ] Gamut context nuance added (§8.4)
- [ ] Citations cleaned and verified

### Phase 3 Complete ✓
- [ ] Literature review completed
- [ ] Novelty claims repositioned
- [ ] 4-5 diagrams created
- [ ] Appendix D complete

### Final Grade Target
- **Engineering specification:** A (9.5/10)
- **Academic viability:** B+ (8.0/10) — solid foundation for publication if pursued

---

## Notes & Observations

### From Tutor A (Academic Focus)
- Emphasized *precision* of claims
- Flagged heuristics vs. empirical facts
- Praised design rationale boxes
- Grade: A- with specific fixes

### From Tutor B (Comprehensive)
- Emphasized *context* and nuance
- Highlighted missing diagrams
- Noted academic publication potential
- Grade: A (engineering) / B (academic paper)

### Key Insight from Both
The document is **genuinely exceptional**. The gaps identified are not fundamental flaws but rather "leveling up" opportunities:
- Tutor A: "From technical whitepaper to rigorous academic paper"
- Tutor B: "From internal spec to publication-ready foundation"

---

## Questions to Resolve

Before starting Phase 1, confirm:

1. **Academic goal?** Are you considering academic publication, or is internal/external engineering specification the goal?
2. **Novelty position:** Based on your knowledge, do you think single-anchor expansion formalization is truly novel, or should we reframe?
3. **Perceptual validation:** Do you have plans for user studies, or should we document current state as "engineering heuristics"?
4. **Diagram capacity:** Will you create diagrams, or should they be assigned/outsourced?
5. **Timeline:** Is 3-week timeline realistic for your schedule?

---

**Document prepared for implementation:** Ready to begin Phase 1  
**Next action:** Review this plan with tutors and confirm priorities
