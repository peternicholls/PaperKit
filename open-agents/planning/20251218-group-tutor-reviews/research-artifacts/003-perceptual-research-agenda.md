# Perceptual Research Agenda: Möbius Loops & Chromatic Inversion

**Date:** 18 December 2025  
**Agent:** Quinn (Problem Solver)  
**Task:** 003-solver-mobiusVerification  
**Context:** Strategic pivot from "theoretical extension" to perceptually-grounded implementation  
**Status:** Research plan for Möbius loop design

---

## Executive Summary

The Möbius loop strategy (§7.4) is currently marked as "theoretical extension not implemented." Rather than simply documenting this gap, we should ask: **What does perceptual science tell us about chromatic inversion and loop closure?** This agenda identifies research domains, specific questions, and implementation pathways to create a **perceptually-principled half-twist loop** grounded in literature.

**Key Insight:** The Möbius strip is a geometric metaphor—but what's the **perceptual truth** behind "return with difference"? We need to discover what makes chromatic transitions feel continuous, what inversion rates are acceptable, and whether natural cycles provide better models than abstract topology.

---

## Part 1: The Core Möbius Challenge

### 1.1 What Are We Trying to Achieve?

**Perceptual Goals:**
1. **Seamless chromatic inversion:** 180° hue rotation that feels smooth, not jarring
2. **Perceptual twist sensation:** Second cycle feels "different but related"
3. **Satisfying return:** Arriving back at origin feels natural after two cycles
4. **No perceptual discontinuities:** ΔE maintained < 0.05 throughout
5. **Mood preservation:** "Calm" stays calm through inversion, "energetic" stays energetic

**NOT goals:**
- ❌ Mathematical elegance of topology for its own sake
- ❌ Literal geometric Möbius strip (color space isn't a physical surface)
- ❌ Instantaneous jumps that violate perceptual continuity

**Core Research Question:**
> "How can we implement a chromatic half-twist that maintains perceptual continuity while creating a satisfying 'return with difference' experience grounded in human color perception?"

---

### 1.2 Current Understanding: What We Don't Know

**The Tutor's Concern:**
> "You invert chromatic components: $(L, -a, -b)$. This results in the mathematical complement (180° rotation). Ensure the text clarifies that the twist happens over the course of the second loop, not as a jump."

**Our Gap in Knowledge:**
1. **Is instantaneous inversion ever acceptable?**
   - Medical studies show flash rate limits
   - What about gradual chromatic shifts?
   
2. **What's the minimum smooth transition time?**
   - How long does chromatic adaptation take?
   - Does it vary by starting color?

3. **What does "180° hue rotation" feel like?**
   - Red → Cyan: Is this perceptually smooth?
   - Blue → Yellow: Different perceptual distance?
   - Context-dependent?

4. **Are there natural analogues we should follow?**
   - Day → Night cycle (gradual chromatic inversion)
   - Seasonal color shifts (slow complementary transitions)
   - Atmospheric phenomena (auroras, twilight)

---

## Part 2: Research Domains

### Domain 1: Chromatic Adaptation & Inversion

#### 1.1 Core Questions

**Primary:**
1. **What is the perceptual threshold for "sudden" vs "smooth" hue change?**
   - At what rate (degrees/second) does hue rotation feel continuous?
   - Does this vary by hue (red vs blue vs green)?
   - Context effects: background, illumination, surround

2. **How long does chromatic adaptation take?**
   - Classic studies: von Kries, Helson-Judd
   - Modern findings: cortical adaptation time constants
   - Relevant to Möbius transition duration

3. **What makes complementary colors feel "related"?**
   - Are complementary pairs perceptually special?
   - Do they share perceptual structure beyond geometry?
   - Cultural/learned associations vs hardwired

4. **Is 180° rotation the "right" amount of twist?**
   - Why not 90° (quarter-twist) or 270° (three-quarter)?
   - What does perceptual "opposite" mean?
   - Color opponent theory implications

#### 1.2 Literature to Find

**Foundational Papers:**
- **von Kries (1902):** Chromatic adaptation theory
- **Helson & Judd (1936):** Chromatic adaptation time course
- **Hurvich & Jameson (1957):** Opponent process theory
- **Fairchild (2013):** Modern color appearance models (CAM02, CAM16)

**Temporal Aspects:**
- Search: "chromatic adaptation temporal dynamics"
- Search: "hue rotation perception threshold"
- Search: "complementary color discrimination"
- Search: "opponent color temporal processing"

**Perceptual Continuity:**
- Search: "color change detection temporal"
- Search: "suprathreshold hue differences"
- Search: "chromatic flicker fusion"
- Search: "color constancy temporal windows"

**Critical Findings Needed:**
1. **Adaptation time constant (τ):** How long for 180° hue shift to feel "settled"?
2. **Rotation rate threshold:** Max degrees/second for smooth perception
3. **ΔE during inversion:** Can we maintain < 0.05 during 180° rotation?
4. **Complementary pair salience:** Are red↔cyan, blue↔yellow special cases?

---

### Domain 2: Perceptual Loops & Closure

#### 2.1 Core Questions

**Primary:**
1. **What makes a color sequence feel "complete"?**
   - Gestalt closure principles in temporal color
   - Role of return to origin vs near-origin
   - Expectation fulfillment

2. **Is exact return necessary, or is "close enough" acceptable?**
   - Just-noticeable-difference at loop point
   - Perceptual tolerance for ΔE at closure
   - Context: animation speed, viewing distance

3. **What is the perceptual effect of "twisted return"?**
   - Return to complementary vs return to origin
   - Surprise/interest vs satisfaction/closure
   - Novelty seeking vs pattern completion

4. **How does loop duration affect expectations?**
   - Short loops (< 1s): expect exact return
   - Long loops (> 5s): tolerate variation
   - Memory effects in color sequences

#### 2.2 Literature to Find

**Temporal Gestalt:**
- **Wertheimer (1923):** Gestalt principles of organization
- **Kubovy & Van Valkenburg (2001):** Auditory and visual continuity
- **Bregman (1990):** Auditory scene analysis (applicable to color sequences?)

**Perceptual Closure:**
- Search: "perceptual closure temporal sequences"
- Search: "Gestalt completion in vision"
- Search: "temporal grouping color stimuli"
- Search: "expectation violation visual perception"

**Looping Perception:**
- Search: "looping animation perception"
- Search: "cyclic visual patterns"
- Search: "return point detection"
- Search: "seamless loop perception"

**Memory & Expectation:**
- Search: "color memory short-term"
- Search: "perceptual expectations temporal"
- Search: "pattern completion vision"
- Search: "temporal predictive coding color"

**Critical Findings Needed:**
1. **Closure threshold:** Maximum ΔE at loop point for "seamless" feel
2. **Expectation window:** How precisely do viewers remember starting color?
3. **Twisted return acceptability:** Is complementary return "satisfying"?
4. **Duration effects:** Optimal loop length for Möbius effect

---

### Domain 3: Natural Chromatic Cycles

#### 3.1 Core Questions

**Primary:**
1. **What natural phenomena exhibit chromatic inversion?**
   - Day → Night cycle: warm → cool
   - Sunrise/Sunset: orange → blue
   - Seasonal changes: summer warm → winter cool
   - Atmospheric optics: sky color variations

2. **How fast are natural chromatic transitions?**
   - Twilight duration: ~30-60 minutes
   - Seasonal shift: months
   - Weather changes: minutes to hours
   - Relevant to Möbius transition rate

3. **Do natural cycles provide perceptual "templates"?**
   - Evolutionary adaptation to natural color changes
   - Ecological validity of smooth inversion
   - Cultural universals vs learned patterns

4. **What makes natural transitions feel "right"?**
   - Gradual vs sudden changes
   - Predictable pacing (circadian, seasonal)
   - Perceptual satisfaction from familiar patterns

#### 3.2 Literature to Find

**Environmental Color:**
- **Lynch & Livingston (2001):** Color and Light in Nature
- **Minnaert (1954):** The Nature of Light and Color in the Open Air
- **Nassau (2001):** The Physics and Chemistry of Color

**Twilight & Atmospheric Color:**
- Search: "twilight color perception"
- Search: "sunset sunrise color progression"
- Search: "atmospheric color change rate"
- Search: "sky color temporal dynamics"

**Seasonal & Circadian:**
- Search: "seasonal color change perception"
- Search: "circadian color sensitivity"
- Search: "environmental chromatic adaptation"
- Search: "ecological color perception"

**Perceptual Ecology:**
- Search: "natural scene statistics color"
- Search: "ecological validity color perception"
- Search: "evolutionary color vision"
- Search: "color constancy natural environments"

**Critical Findings Needed:**
1. **Natural inversion rates:** Typical degrees/minute in nature
2. **Perceptual anchors:** Blue sky, warm sun as reference points
3. **Smooth transition models:** Twilight as template for Möbius
4. **Cultural universals:** Cross-cultural recognition of natural cycles

---

### Domain 4: Topological Metaphors in Perception

#### 4.1 Core Questions

**Primary:**
1. **Is the Möbius strip a valid perceptual metaphor?**
   - Do non-experts understand "half-twist" in color?
   - Cognitive load of topological concepts
   - Alternative metaphors (day/night, seasonal)

2. **What does "twisted" mean in perceptual color space?**
   - Opponent process axis inversion
   - Cylindrical (LCh) vs Cartesian (Lab) implications
   - Perceptual vs geometric twist

3. **Are there better topological models?**
   - Torus (donut): continuous both ways
   - Klein bottle: non-orientable surface
   - Sphere: no edges, but different topology
   - Which matches perceptual experience?

4. **How do users conceptualize "return with difference"?**
   - Mental models of color loops
   - Expectations from UI/animation experience
   - Educational background effects

#### 4.2 Literature to Find

**Perceptual Topology:**
- **Shepard (1964):** Circularity in judgments of relative pitch (applicable to hue?)
- **Marr (1982):** Vision (computational topology of perception)
- **Palmer (1999):** Vision Science (perceptual organization)

**Cognitive Metaphors:**
- Search: "spatial metaphors perception"
- Search: "topological concepts cognition"
- Search: "perceptual geometry color"
- Search: "mental models color space"

**Color Space Topology:**
- Search: "color space topology"
- Search: "hue circle perception"
- Search: "cylindrical color space perception"
- Search: "toroidal color spaces"

**Alternative Models:**
- Search: "color solid topology"
- Search: "non-Euclidean color spaces"
- Search: "perceptual color manifolds"
- Search: "color appearance model topology"

**Critical Findings Needed:**
1. **Metaphor validity:** Do users understand Möbius analogy?
2. **Perceptual topology:** What's the "shape" of perceptual color space?
3. **Alternative structures:** Better models than Möbius strip?
4. **User mental models:** How do designers think about color loops?

---

## Part 3: Implementation Pathways

### Option A: Progressive Inversion (Research-Grounded)

**Hypothesis:** Smooth chromatic inversion over second cycle maintains perceptual continuity.

#### Implementation Design

**Mathematical Formulation:**
```
Cycle 1: t ∈ [0, 1]
    J(t) = path from A₁ to Aₘ (normal journey)
    
Cycle 2: t ∈ [1, 2]
    τ = (t - 1)  // Progress through second cycle
    inversion_factor = smoothstep(τ)  // 0 → 1 smoothly
    
    a(t) = a_base(t) · (1 - 2·inversion_factor)
    b(t) = b_base(t) · (1 - 2·inversion_factor)
    L(t) = L_base(t)  // Preserve lightness
    
    At τ=0.0 (t=1.0): a,b unchanged
    At τ=0.5 (t=1.5): a,b → -a,-b (full inversion)
    At τ=1.0 (t=2.0): return to original a,b
```

**Perceptual Validation Needed:**
1. **ΔE profile during inversion:**
   - Calculate ΔE between adjacent samples
   - Ensure < 0.05 throughout
   - May require denser sampling during inversion

2. **Inversion rate check:**
   - If literature says max N degrees/second
   - Map to number of samples per 180° rotation
   - Adjust second cycle duration if needed

3. **Perceptual testing:**
   - Does this feel "smooth"?
   - Is complementary color recognizable at midpoint?
   - Does return feel satisfying?

#### Research Questions to Resolve

**From Domain 1 (Chromatic Adaptation):**
- Q: What's the minimum transition time for 180° hue rotation?
- A: Extract from adaptation studies → set second cycle duration

**From Domain 2 (Closure):**
- Q: Is exact return to origin necessary?
- A: If yes, ensure $J(2.0) = J(0.0)$ precisely
- A: If no, tolerance band determines acceptable ΔE

**From Domain 3 (Natural Cycles):**
- Q: Should we model after twilight (30-60 min)?
- A: Translate real-time to animation time (proportional scaling)

---

### Option B: Adaptation Period (Natural Cycle Model)

**Hypothesis:** Mimic natural day→night transition with explicit adaptation period.

#### Implementation Design

**Mathematical Formulation:**
```
Phase 1 (Day): t ∈ [0, 1]
    J(t) = normal journey (warm bias)
    
Phase 2 (Twilight): t ∈ [1, 1+τ]
    Gradual chromatic inversion
    Lightness reduction (sun setting)
    τ = adaptation time from research
    
Phase 3 (Night): t ∈ [1+τ, 2+τ]
    Inverted journey (cool bias)
    Reduced lightness
    
Phase 4 (Dawn): t ∈ [2+τ, 3+τ]
    Reverse inversion
    Lightness increase
    
Return: t = 3+τ → back to t=0
```

**Advantages:**
- ✅ Grounded in natural perceptual experience
- ✅ Explicit adaptation period (no confusion)
- ✅ Can match natural twilight durations
- ✅ Culturally/evolutionarily familiar

**Disadvantages:**
- ⚠️ Longer total cycle (3+2τ instead of 2)
- ⚠️ More complex than pure Möbius
- ⚠️ May not feel like "twist" (just slow cycle)

#### Research Questions to Resolve

**From Domain 3 (Natural Cycles):**
- Q: What's the typical twilight duration perception?
- A: Scale to animation context (e.g., 5% of total cycle)

**From Domain 1 (Chromatic Adaptation):**
- Q: How long for adaptation to complementary?
- A: Use τ = adaptation constant from literature

**From Domain 2 (Closure):**
- Q: Does longer cycle reduce closure expectation?
- A: If yes, four-phase structure may be acceptable

---

### Option C: Opponent Axis Rotation (Perceptual Twist)

**Hypothesis:** Rotate around opponent axes rather than simple negation.

#### Implementation Design

**Mathematical Formulation:**
```
Opponent space representation:
    Red-Green axis: a
    Yellow-Blue axis: b
    
Cycle 1: t ∈ [0, 1]
    Normal journey in opponent space
    
Cycle 2: t ∈ [1, 2]
    Rotate opponent axes:
        a → b, b → -a (90° CCW rotation)
    OR:
        a → -a, b → -b (180° rotation, original)
    OR:
        a → -b, b → a (90° CW rotation)
        
Test different rotations for perceptual effect
```

**Advantages:**
- ✅ Grounded in opponent process theory
- ✅ Multiple rotation options to explore
- ✅ May feel more "perceptually natural"
- ✅ Could validate against neural mechanisms

**Disadvantages:**
- ⚠️ More complex to explain
- ⚠️ Requires opponent process literature
- ⚠️ May not match geometric Möbius metaphor

#### Research Questions to Resolve

**From Domain 1 (Chromatic Adaptation):**
- Q: Are opponent axes perceptually independent?
- A: Can we rotate one without affecting the other?

**From Domain 4 (Topology):**
- Q: What's the perceptual meaning of "axis rotation"?
- A: User testing needed

---

### Option D: Pulsed Inversion (Rhythmic Approach)

**Hypothesis:** Oscillate between original and inverted rather than smooth transition.

#### Implementation Design

**Mathematical Formulation:**
```
Inversion wave:
    inv(t) = 0.5 * (1 + sin(π * (t - 1)))
    
    For t ∈ [1, 2]:
        a(t) = a_base(t) · (1 - 2·inv(t))
        b(t) = b_base(t) · (1 - 2·inv(t))
        
    Creates sinusoidal oscillation:
        t=1.0: inv=0 (original)
        t=1.5: inv=1 (fully inverted)
        t=2.0: inv=0 (back to original)
```

**Advantages:**
- ✅ Smooth, continuous (sine wave)
- ✅ Symmetric acceleration/deceleration
- ✅ Natural oscillation pattern
- ✅ Clear maximum inversion point

**Disadvantages:**
- ⚠️ May feel like "breathing" rather than "twist"
- ⚠️ Doesn't match Möbius metaphor closely

#### Research Questions to Resolve

**From Domain 2 (Perceptual Loops):**
- Q: Do rhythmic patterns feel different from linear transitions?
- A: Animation perception literature

---

## Part 4: Research Task Breakdown

### Task M1: Chromatic Inversion Literature Review
**Agent:** 📖 Research Librarian (Ellis)  
**Time:** 2-3 hours  
**Output:** `chromatic-inversion-literature.md`

**Specific Searches:**
1. "chromatic adaptation temporal dynamics"
2. "hue rotation perception threshold"
3. "complementary color perception"
4. "opponent process temporal"
5. "color change detection threshold"
6. "suprathreshold hue discrimination"

**Key Papers to Prioritize:**
- von Kries, Helson-Judd (foundational adaptation)
- Fairchild 2013 (modern CAM)
- Any studies on 180° hue rotation
- Temporal chromatic sensitivity

**Deliverable:** 10-15 annotated papers with:
- Adaptation time constants
- Rotation rate thresholds
- Complementary pair findings
- Relevance to Möbius design

---

### Task M2: Perceptual Loops Literature Review
**Agent:** 📖 Research Librarian (Ellis)  
**Time:** 2 hours  
**Output:** `perceptual-loops-literature.md`

**Specific Searches:**
1. "perceptual closure temporal"
2. "Gestalt completion color"
3. "looping animation perception"
4. "cyclic visual patterns"
5. "return point detection"
6. "temporal grouping color"

**Key Papers to Prioritize:**
- Gestalt psychologists (Wertheimer et al.)
- Modern closure studies
- Animation perception research
- Pattern completion studies

**Deliverable:** 8-12 annotated papers with:
- Closure thresholds
- Loop duration effects
- Expectation findings
- Relevance to Möbius return

---

### Task M3: Natural Chromatic Cycles Research
**Agent:** 📖 Research Librarian (Ellis)  
**Time:** 1-2 hours  
**Output:** `natural-cycles-literature.md`

**Specific Searches:**
1. "twilight color perception"
2. "sunset sunrise progression"
3. "atmospheric color temporal"
4. "circadian color sensitivity"
5. "seasonal chromatic adaptation"
6. "natural scene color statistics"

**Key Papers to Prioritize:**
- Environmental color perception
- Ecological vision research
- Twilight/atmospheric optics
- Circadian studies with color

**Deliverable:** 5-10 annotated papers/sources with:
- Natural transition rates
- Perceptual anchors (blue sky, warm sun)
- Twilight duration perception
- Ecological validity findings

---

### Task M4: Topology & Metaphor Research
**Agent:** 📖 Research Librarian (Ellis)  
**Time:** 1-2 hours  
**Output:** `topology-metaphor-literature.md`

**Specific Searches:**
1. "color space topology"
2. "perceptual geometry color"
3. "hue circle perception"
4. "mental models color space"
5. "spatial metaphors cognition"
6. "toroidal color spaces"

**Key Papers to Prioritize:**
- Shepard (circularity research)
- Palmer (Vision Science)
- Color space structure studies
- Cognitive metaphor research

**Deliverable:** 5-8 annotated papers with:
- Perceptual color space structure
- Alternative topological models
- Metaphor validity findings
- User conceptualization studies

---

### Task M5: Möbius Design Synthesis
**Agent:** 🔬 Research Consolidator (Alex)  
**Time:** 3-4 hours  
**Dependencies:** M1, M2, M3, M4  
**Output:** `mobius-design-principles.md`

**Synthesis Objectives:**
1. **Determine feasibility:** Is perceptually-smooth Möbius possible?
2. **Extract parameters:**
   - Minimum inversion time
   - Maximum rotation rate
   - Closure threshold (ΔE)
   - Optimal cycle duration

3. **Recommend implementation:**
   - Option A, B, C, or D?
   - Or hybrid approach?
   - Or alternative structure?

4. **Design validation approach:**
   - What needs user testing?
   - What's grounded in literature?
   - What are design choices?

**Deliverable:** Design principles document with:
- Implementation recommendation
- Parameter specifications (with citations)
- Perceptual rationale
- Validation requirements
- Alternative options if primary fails

---

### Task M6: Möbius Parameter Specification
**Agent:** 🔬 Problem Solver (Quinn)  
**Time:** 2-3 hours  
**Dependencies:** M5  
**Output:** `mobius-parameter-specification.md`

**Specification Objectives:**
1. **Mathematical formulation:**
   - Exact equations for chosen option
   - Sample density calculations
   - ΔE profile predictions

2. **Perceptual validation:**
   - Check against research thresholds
   - Calculate transition rates
   - Verify closure conditions

3. **Implementation details:**
   - Pseudocode for engine
   - Edge case handling
   - Performance considerations

4. **Test scenarios:**
   - Example journeys (red→cyan, blue→yellow)
   - Edge cases (near-gray, saturated colors)
   - Different cycle durations

**Deliverable:** Complete specification with:
- Equations (LaTeX)
- Pseudocode (C-style)
- Test case definitions
- Expected ΔE profiles
- Validation criteria

---

### Task M7: Section 7.4 Revision
**Agent:** ✍️ Section Drafter (Jordan)  
**Time:** 2-3 hours  
**Dependencies:** M5, M6  
**Output:** Revised `latex/sections/07_loop_strategies.tex` §7.4

**Drafting Objectives:**
1. **Replace "theoretical" with "perceptually-grounded"**
2. **Add perceptual rationale section:**
   - Cite chromatic adaptation research
   - Reference natural cycle analogues
   - Explain smooth inversion mechanism

3. **Specify implementation:**
   - Mathematical formulation (from M6)
   - Progressive inversion description
   - ΔE maintenance guarantee

4. **Add validation note:**
   - What's literature-grounded
   - What requires user testing
   - Future work acknowledgment

**Deliverable:** Publication-ready §7.4 with:
- Perceptual foundations subsection
- Implementation details
- Full citations (Harvard style)
- Design decision boxes
- No "theoretical extension" language

---

### Task M8: Möbius Section Refinement
**Agent:** 💎 Quality Refiner (Riley)  
**Time:** 1-2 hours  
**Dependencies:** M7  
**Output:** Polished §7.4

**Refinement Objectives:**
1. Verify all perceptual claims have citations
2. Check mathematical notation consistency
3. Ensure smooth integration with §7.1-7.3
4. Polish language (clear, precise, academic)
5. Add cross-references (§2, §4, §6)

**Deliverable:** Publication-ready §7.4

---

## Part 5: Success Criteria

### Literature Review Success (M1-M4)
- ✅ 25-40 papers total across four domains
- ✅ Adaptation time constants found (or gap documented)
- ✅ Hue rotation thresholds identified
- ✅ Natural cycle rates documented
- ✅ Topological alternatives explored

### Design Synthesis Success (M5-M6)
- ✅ Clear implementation recommendation (Option A/B/C/D or hybrid)
- ✅ All parameters grounded in literature or marked as design choice
- ✅ ΔE profile validated against perceptual thresholds
- ✅ Mathematical formulation complete and testable

### Paper Integration Success (M7-M8)
- ✅ §7.4 transforms from "theoretical" to "perceptually-grounded"
- ✅ Every claim has citation or explicit design choice label
- ✅ Implementation specified with enough detail for reproduction
- ✅ Perceptual rationale clear to interdisciplinary readers
- ✅ Reviewers see this as principled, not arbitrary

---

## Part 6: Potential Outcomes & Contingencies

### Best Case: Progressive Inversion Validated
**Findings:**
- Literature supports smooth chromatic inversion
- Adaptation time constant found: τ ≈ X seconds
- 180° rotation acceptable at ≤ Y degrees/second
- Complementary pairs perceptually special

**Implementation:**
- Option A (Progressive Inversion) with parameters from research
- Second cycle duration set to 2τ (full adaptation + return)
- ΔE profile maintained < 0.05
- §7.4 becomes showcase of perceptual grounding

---

### Moderate Case: Natural Cycle Model Better
**Findings:**
- Literature suggests explicit adaptation period needed
- Twilight model more perceptually natural than geometric twist
- Four-phase structure (day/twilight/night/dawn) validated
- Users prefer ecological validity over topological elegance

**Implementation:**
- Option B (Adaptation Period / Natural Cycle)
- Longer total cycle (3+2τ) but more familiar
- Ground in ecological perception literature
- Rename from "Möbius" to "Circadian" or "Twilight Cycle"

---

### Alternative Case: Opponent Rotation Better
**Findings:**
- Opponent process literature suggests axis rotation
- 90° rotations feel more natural than 180°
- Red-Green and Yellow-Blue axes show independence
- Neural mechanisms support this approach

**Implementation:**
- Option C (Opponent Axis Rotation)
- Multiple rotation variants possible
- Ground in opponent process theory
- Require more extensive explanation in paper

---

### Challenging Case: Limited Literature
**Findings:**
- Few studies on temporal chromatic inversion
- No clear adaptation time constants for 180° rotation
- Mostly static color perception research
- Gap in temporal suprathreshold literature

**Implementation:**
- Acknowledge literature gap honestly
- Propose implementation based on first principles
- Frame as "design hypothesis requiring validation"
- Specify exactly what user study would test
- Turn limitation into contribution opportunity

**Paper Language:**
```latex
\begin{note}
While extensive research exists on chromatic adaptation 
in static contexts, we found limited literature on the 
perceptual effects of gradual 180° hue rotation in 
sequential color presentations. Our proposed progressive 
inversion mechanism (Eq. X) is designed to maintain 
perceptual continuity by ensuring $\Delta E < 0.05$ 
throughout the transition. Formal perceptual validation 
through user studies remains future work (§12.3).
\end{note}
```

---

## Part 7: Timeline Integration

**Days 3-4 (Phase 2):**
- M1-M4: All literature reviews (Ellis) - 6-9 hours total
- Parallel with velocity research (R1-R2)

**Days 5-6 (Phase 3):**
- M5: Design synthesis (Alex) - 3-4 hours
- M6: Parameter specification (Quinn) - 2-3 hours

**Days 7-8:**
- M7: Section drafting (Jordan) - 2-3 hours
- M8: Refinement (Riley) - 1-2 hours

**Total Effort:** ~15-20 hours across tasks
**Calendar Days:** 6 days (overlapping with other work)

---

## Part 8: Why This Matters

### Current State
- ❌ "Möbius is theoretical, not implemented"
- ❌ Tutor concern about discontinuous jump unresolved
- ❌ No perceptual grounding for chromatic inversion
- ❌ Geometric metaphor without perceptual validation

### Proposed State
- ✅ "Möbius implements perceptually-smooth chromatic inversion"
- ✅ Tutor concern resolved with progressive mechanism
- ✅ Grounded in chromatic adaptation and natural cycle research
- ✅ Implementation specified with perceptual parameters

### Strategic Value
- **Novelty:** Perceptually-principled half-twist loop (may be first)
- **Rigor:** Every parameter traceable to research
- **Contribution:** If literature gap exists, we define the problem
- **Defensibility:** Reviewers can't claim arbitrary design
- **USP:** Reinforces Color Journey as perception-first system

---

## Immediate Next Steps

1. **Approve scope:** Do M1-M8 address the Möbius challenge?
2. **Prioritize:** Start with M1 (chromatic inversion) or M3 (natural cycles)?
3. **Assign:** Librarian begins literature search
4. **Iterate:** Findings may suggest new questions or approaches
5. **Integrate:** Coordinate with velocity research (R1-R8)

---

**Status:** ✅ MÖBIUS RESEARCH AGENDA COMPLETE – Ready for task execution

**Decision Point:** Proceed with M1-M8 or refine research questions first?
