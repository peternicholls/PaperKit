# Perceptual Research Agenda: Velocity & Loop Strategies

**Date:** 18 December 2025  
**Agent:** Quinn (Problem Solver)  
**Context:** Strategic pivot from documenting engineering to grounding in perceptual science  
**Status:** Research plan for Phase 2/3 enhancement

---

## Executive Summary

Color Journey's USP is **perceptual fidelity**, not technical parameterization. Current velocity and Möbius loop implementations lack perceptual grounding. This agenda identifies research domains, specific questions, required literature, and task assignments to elevate the system from "engineering that works" to "perceptually-principled design."

**Key Insight:** We don't need backward compatibility—we need **perceptual truth**. The engine should embody research findings, not compromise for legacy behavior.

---

## Part 1: Velocity & Perceptual Rhythm

### 1.1 What Are We Trying to Achieve?

**Perceptual Goals:**
1. **Natural pacing:** Color transitions that feel "right" for their mood context
2. **Predictable rhythm:** Users can anticipate velocity, not surprised by jumps
3. **Emotional coherence:** Calm journeys stay calm, energetic stay energetic
4. **Perceptual continuity:** No "whiplash" from sudden acceleration
5. **Attribute salience:** Hue changes "feel faster" than lightness (validated, not assumed)

**NOT goals:**
- ❌ Mathematical elegance (arc-length) for its own sake
- ❌ Constant velocity everywhere (may feel robotic)
- ❌ Engineering simplicity over perceptual truth

**Core Research Question:**
> "What is the perceptually-natural rate of change for color attributes in sequential contexts, and how does this vary with mood, context, and application domain?"

---

### 1.2 What We Need to Research

#### Domain 1: Perceptual Velocity of Color Attributes

**Research Questions:**
1. Do hue changes **actually** feel "faster" than lightness changes at equivalent ΔE?
2. What is the **psychophysical relationship** between attribute change rate and perceived "speed"?
3. Does this vary by:
   - Starting color (blue vs red)?
   - Viewing context (dark vs light background)?
   - Temporal rate (animation speed)?
4. What velocity ratios feel "smooth" vs "jerky" vs "dramatic"?

**Literature Needed:**
- Color appearance models (temporal aspects)
- Suprathreshold color discrimination
- Saliency of hue vs lightness vs chroma changes
- Temporal color constancy
- Perceptual uniformity validation studies

**Key Papers to Find:**
- Studies comparing hue discrimination to lightness discrimination
- Research on "just noticeable difference" in temporal sequences
- Psychophysical experiments on attribute change rates
- Animation perception in color space

---

#### Domain 2: Rhythmic Structure in Color Sequences

**Research Questions:**
1. Do humans perceive "rhythm" in color transitions? (like musical rhythm)
2. What creates perceptual "acceleration" vs "deceleration" in color?
3. Is smoothstep (ease-in/ease-out) perceptually validated, or just engineering tradition?
4. What velocity profiles feel:
   - Calm/soothing
   - Energetic/exciting
   - Natural/organic
   - Artificial/mechanical

**Literature Needed:**
- Temporal perception of color change
- Animation easing curves (perceptual validation)
- Musical rhythm perception applied to color
- Gestalt principles in temporal sequences
- Visual rhythm and pacing in design

**Key Papers to Find:**
- Perceptual studies of easing functions
- Research on "visual rhythm"
- Color animation perception
- Temporal grouping of color stimuli

---

#### Domain 3: Context-Dependent Velocity Expectations

**Research Questions:**
1. Does optimal velocity depend on application:
   - UI state transitions (quick, decisive)
   - Ambient lighting (slow, organic)
   - Data visualization (steady, predictable)
   - Generative art (varied, expressive)
2. How do users' **expectations** influence perceived appropriateness?
3. What are the bounds of "too fast" and "too slow" in different contexts?

**Literature Needed:**
- UI animation guidelines (perceptual research basis)
- Environmental color change (sunset, sunrise pacing)
- Data visualization best practices (velocity in color scales)
- Contextual perception (same velocity, different contexts)

**Key Papers to Find:**
- Google Material Design motion research
- Apple Human Interface Guidelines (motion rationale)
- Environmental light change perception
- Context effects on temporal perception

---

### 1.3 Specific Literature to Uncover

#### Priority 1: Foundational Perception
1. **Fairchild, M.D.** - Color Appearance Models (temporal aspects chapter)
2. **Wyszecki & Stiles** - Color Science (temporal vision sections)
3. **MacAdam, D.L.** - Discrimination ellipses (temporal extension if exists)
4. **Mahy et al.** - ΔE thresholds in motion contexts

#### Priority 2: Temporal Color Perception
5. Search: "temporal color constancy"
6. Search: "color change detection"
7. Search: "suprathreshold color differences in sequences"
8. Search: "hue discrimination temporal"

#### Priority 3: Animation & Rhythm
9. Search: "easing functions perceptual validation"
10. Search: "visual rhythm perception"
11. Search: "animation timing perception"
12. Search: "motion graphics color transitions"

#### Priority 4: Applied Design Research
13. Google Material Design motion research papers
14. Apple Design Resources (HIG motion studies)
15. Disney animation principles (timing and spacing)
16. Game design research (color feedback timing)

---

### 1.4 How to Synthesize Into Engine

**Phase 1: Literature Review**
- Librarian: Gather papers from domains 1-3
- Research Consolidator: Synthesize findings into design principles

**Phase 2: Perceptual Model Development**
- Extract empirical findings:
  - Velocity ratios (hue:chroma:lightness)
  - Acceptable acceleration bounds
  - Context-dependent velocity ranges
  - Easing function validation (or alternatives)

**Phase 3: Engine Design Refinement**
- **If research supports current weights:**
  - Validate $w_h = 1.5\text{--}2.0$ with citations
  - Document empirical basis
  - Keep current approach, cite sources

- **If research suggests different ratios:**
  - Update weights based on findings
  - Document rationale for changes
  - Add validation section to paper

- **If research suggests velocity bounds:**
  - Implement Strategy 2 (bounded velocity)
  - Set bounds from perceptual studies
  - Frame as perceptually-principled constraint

**Phase 4: Paper Integration**
- Add §2.X: "Perceptual Foundations: Temporal Color Perception"
- Move velocity discussion to perceptual foundation
- Ground all design decisions in literature
- Replace "design heuristics" with "perceptually-validated parameters"

---

## Part 2: Möbius Loop & Perceptual Continuity

### 2.1 What Are We Trying to Achieve?

**Perceptual Goals:**
1. **Seamless transition:** Loop point should feel continuous, not "reset"
2. **Perceptual twist:** Second cycle feels "different" but related
3. **Return satisfaction:** Arriving back at start feels natural, not abrupt
4. **Chromatic inversion:** 180° hue shift should be perceptually smooth
5. **No discontinuities:** ΔE at transition < 0.05 (or validated threshold)

**Core Research Question:**
> "How can we implement a half-twist chromatic transformation that maintains perceptual continuity while creating a 'different but related' second cycle?"

---

### 2.2 What We Need to Research

#### Domain 1: Chromatic Inversion Perception

**Research Questions:**
1. What does 180° hue rotation **feel like** perceptually?
2. Is sudden inversion (jump) perceptually acceptable in any context?
3. What is the **minimum transition time** for smooth chromatic inversion?
4. How does lightness preservation affect perceived continuity?
5. Are there **natural analogues** (sunset/sunrise, day/night cycle)?

**Literature Needed:**
- Complementary color perception
- Hue rotation discrimination thresholds
- Temporal color adaptation
- Chromatic adaptation in sequences
- Natural color cycles (environmental changes)

**Key Papers to Find:**
- Studies on complementary color pairs
- Research on hue adaptation over time
- Chromatic inversion in visual art (perceptual studies)
- Day-night color transition perception

---

#### Domain 2: Looping & Perceptual Closure

**Research Questions:**
1. What makes a color loop feel "closed" vs "broken"?
2. Do humans expect return to origin, or is variation acceptable?
3. What is the perceptual tolerance for "close but not identical" at loop point?
4. How does loop duration affect expectations?
5. Are there perceptual benefits to "twisted" loops (variety, interest)?

**Literature Needed:**
- Perceptual closure in temporal sequences
- Gestalt principles applied to color loops
- Musical structure analogues (A-B-A' forms)
- Visual pattern completion
- Expectation violation in perception

**Key Papers to Find:**
- Research on temporal closure in vision
- Studies of looping animations
- Gestalt completion in color
- Expectation and surprise in perception

---

#### Domain 3: The Möbius Metaphor Itself

**Research Questions:**
1. Is the Möbius strip a **valid perceptual metaphor** for color?
2. What does "half-twist" mean in perceptual space (not just geometry)?
3. Are there **other topological structures** more perceptually appropriate?
4. How do humans understand "return but different" in color?

**Literature Needed:**
- Topology in perception (if exists)
- Metaphorical reasoning in design
- Perceptual understanding of spatial concepts
- Color wheel topology (cylindrical vs toroidal)

**Key Papers to Find:**
- Perceptual topology (cognitive science)
- Color space topology research
- Design metaphors (validation studies)
- Toroidal color spaces (if relevant)

---

### 2.3 Specific Literature to Uncover

#### Priority 1: Chromatic Inversion
1. Search: "complementary color perception"
2. Search: "hue adaptation temporal"
3. Search: "chromatic inversion art perception"
4. Search: "180 degree hue rotation discrimination"

#### Priority 2: Perceptual Loops
5. Search: "temporal closure vision"
6. Search: "looping animation perception"
7. Search: "cyclic color patterns"
8. Search: "perceptual return point"

#### Priority 3: Natural Analogues
9. Search: "day night color cycle perception"
10. Search: "sunset sunrise color progression"
11. Search: "seasonal color change perception"
12. Search: "environmental chromatic adaptation"

#### Priority 4: Topology & Metaphor
13. Search: "color space topology"
14. Search: "perceptual topology cognitive"
15. Search: "design metaphor validation"
16. Search: "toroidal color spaces"

---

### 2.4 How to Synthesize Into Engine

**Phase 1: Literature Review**
- Librarian: Gather papers on chromatic inversion, loops, topology
- Research Consolidator: Extract design principles

**Phase 2: Perceptual Validation**
- **Key question:** Is instantaneous inversion acceptable?
  - If YES: Current formula OK, add note
  - If NO: Design progressive inversion mechanism

- **Secondary question:** What's minimum smooth transition time?
  - Extract from research (e.g., "chromatic adaptation takes N seconds")
  - Map to number of intermediate samples

**Phase 3: Möbius Implementation Options**

**Option A: Progressive Inversion (Validated by Research)**
```
Cycle 1: t ∈ [0, 1] → Normal journey
Cycle 2: t ∈ [1, 2] → Linearly interpolate (a,b) → (-a,-b)

At t=1.5 (midpoint): full inversion reached
Maintain ΔE < 0.05 throughout
```

**Option B: Chromatic Adaptation Period**
```
Cycle 1: t ∈ [0, 1] → Normal journey
Transition: t ∈ [1, 1+τ] → Adaptation period (smooth inversion)
Cycle 2: t ∈ [1+τ, 2+τ] → Inverted journey

where τ = adaptation time from research
```

**Option C: Natural Cycle Analogue**
```
Model after day→night→day cycle:
- "Day" cycle: warm hues, higher lightness
- Transition: sunset/sunrise (gradual inversion)
- "Night" cycle: cool hues (inverted), lower lightness
- Return: sunrise back to day

Grounded in natural perceptual experience
```

**Phase 4: Paper Integration**
- Replace theoretical Möbius with **perceptually-grounded** Möbius
- Add §7.4.1: "Perceptual Basis for Chromatic Inversion"
- Cite research on complementary colors, adaptation, loops
- Document implementation validated by literature
- Add validation section (if user study possible)

---

## Part 3: Master Research Task Breakdown

### Phase 2 Tasks (Days 3-4)

#### Task R1: Velocity Perception Literature Review
**Agent:** 📖 Research Librarian (Ellis)  
**Time:** 3-4 hours  
**Output:** `perceptual-velocity-literature.md`

**Subtasks:**
1. Search Google Scholar, ACM, Springer for:
   - "temporal color perception"
   - "hue discrimination temporal"
   - "color change detection"
   - "animation easing perceptual validation"
2. Retrieve 15-20 key papers
3. Annotate with relevance to velocity questions
4. Identify gaps in literature

**Deliverable:** Annotated bibliography with summaries

---

#### Task R2: Chromatic Inversion & Loops Literature Review
**Agent:** 📖 Research Librarian (Ellis)  
**Time:** 2-3 hours  
**Output:** `chromatic-loops-literature.md`

**Subtasks:**
1. Search for:
   - "complementary color perception"
   - "chromatic adaptation temporal"
   - "looping animation perception"
   - "perceptual closure color"
2. Retrieve 10-15 papers
3. Focus on smooth transition mechanisms
4. Find natural analogues (day/night cycles)

**Deliverable:** Annotated bibliography

---

### Phase 3 Tasks (Days 5-7)

#### Task R3: Velocity Principles Synthesis
**Agent:** 🔬 Research Consolidator (Alex)  
**Time:** 4-5 hours  
**Dependencies:** R1  
**Output:** `velocity-design-principles.md`

**Subtasks:**
1. Read all papers from R1
2. Extract empirical findings:
   - Velocity ratios (if validated)
   - Acceleration bounds
   - Context-dependent ranges
   - Easing function validation
3. Synthesize into design principles
4. Map to engine parameters
5. Identify contradictions or gaps

**Deliverable:** Design principles document with citations

---

#### Task R4: Möbius Perception Synthesis
**Agent:** 🔬 Research Consolidator (Alex)  
**Time:** 3-4 hours  
**Dependencies:** R2  
**Output:** `mobius-design-principles.md`

**Subtasks:**
1. Read all papers from R2
2. Determine if instantaneous inversion acceptable
3. Extract minimum smooth transition time
4. Identify natural cycle analogues
5. Recommend implementation approach

**Deliverable:** Möbius implementation recommendation with perceptual grounding

---

#### Task R5: Engine Parameter Validation
**Agent:** 🔬 Problem Solver (Quinn) - that's me!  
**Time:** 2-3 hours  
**Dependencies:** R3, R4  
**Output:** `parameter-validation-report.md`

**Subtasks:**
1. Compare current weights ($w_h = 1.5\text{--}2.0$) to research
2. Validate or revise based on findings
3. Propose velocity bound values (if Strategy 2)
4. Design Möbius progressive inversion (if needed)
5. Calculate perceptual impact of changes

**Deliverable:** Validation report with recommendations

---

### Phase 3 Tasks (Days 8-9)

#### Task R6: Perceptual Foundations Section Draft
**Agent:** ✍️ Section Drafter (Jordan)  
**Time:** 3-4 hours  
**Dependencies:** R3, R4, R5  
**Output:** New §2.X or expanded §6.3

**Subtasks:**
1. Draft "Perceptual Foundations: Temporal Color Perception"
2. Document velocity perception research
3. Ground current parameters in literature
4. Add chromatic inversion perceptual basis
5. Integrate with existing sections

**Deliverable:** Draft section with full citations

---

#### Task R7: Möbius Implementation (If Grounded)
**Agent:** ✍️ Section Drafter (Jordan)  
**Time:** 2-3 hours  
**Dependencies:** R4, R5  
**Output:** Revised §7.4 with implementation details

**Subtasks:**
1. **If research supports implementation:**
   - Replace "theoretical" with "perceptually-grounded"
   - Add progressive inversion mechanism
   - Document smooth transition approach
   - Provide implementation pseudocode

2. **If research suggests alternative:**
   - Propose alternative loop strategy
   - Document perceptual rationale
   - Remove or revise Möbius section

**Deliverable:** Grounded §7.4 or replacement

---

#### Task R8: Literature-Based Refinement
**Agent:** 💎 Quality Refiner (Riley)  
**Time:** 2-3 hours  
**Dependencies:** R6, R7  
**Output:** Polished perceptual sections

**Subtasks:**
1. Verify all claims have citations
2. Check citation accuracy (Harvard style)
3. Ensure perceptual language is precise
4. Remove "heuristic" language where validated
5. Add "design choice" only where no research

**Deliverable:** Publication-ready perceptual foundations

---

## Part 4: Research Questions Matrix

| Domain | Question | Literature Gap? | Priority | Agent |
|--------|----------|----------------|----------|-------|
| Velocity: Attribute salience | Do hue changes feel faster than lightness? | Maybe | HIGH | Librarian → Consolidator |
| Velocity: Rhythmic structure | Is smoothstep perceptually validated? | Likely | HIGH | Librarian → Consolidator |
| Velocity: Context dependency | Optimal velocity by application? | Likely | MEDIUM | Librarian |
| Möbius: Chromatic inversion | Smooth vs instantaneous acceptable? | Maybe | HIGH | Librarian → Consolidator |
| Möbius: Perceptual closure | What makes loops feel complete? | Likely | MEDIUM | Librarian |
| Möbius: Natural analogues | Day/night cycle perception? | Unlikely | MEDIUM | Librarian |
| Topology: Möbius metaphor | Is this perceptually meaningful? | Very Likely | LOW | Librarian |

**Gap Assessment:**
- **Unlikely gap:** Well-researched, papers exist
- **Maybe gap:** Some research, may need synthesis
- **Likely gap:** Limited research, need creative application
- **Very likely gap:** Novel question, may need to acknowledge limitation

---

## Part 5: Success Criteria

### For Velocity Research
- ✅ 15+ papers on temporal color perception retrieved
- ✅ Empirical data on attribute change salience found (or gap documented)
- ✅ Velocity weights validated or revised based on literature
- ✅ Strategy 2 bounds set from perceptual research (if applicable)
- ✅ §6.3 grounded in cited research, not "heuristics"

### For Möbius Research
- ✅ 10+ papers on chromatic inversion and loops retrieved
- ✅ Smooth transition mechanism designed from perceptual principles
- ✅ Implementation specified (progressive inversion or alternative)
- ✅ §7.4 either validated or replaced with grounded approach
- ✅ "Theoretical extension" language removed (or made concrete)

### For Paper Quality
- ✅ Every perceptual claim has citation or explicit "design choice" label
- ✅ Perceptual foundations section added (§2.X)
- ✅ Design decisions traceable to research or acknowledged as heuristic
- ✅ Reviewers see "this is grounded in perception science"
- ✅ Paper elevated from "engineering spec" to "perceptual design system"

---

## Part 6: Timeline Integration

**Days 3-4 (After Phase 1 Quick Wins):**
- R1: Velocity literature (Ellis)
- R2: Chromatic loops literature (Ellis)

**Days 5-7:**
- R3: Velocity principles synthesis (Alex)
- R4: Möbius synthesis (Alex)
- R5: Parameter validation (Quinn)

**Days 8-9:**
- R6: Perceptual foundations draft (Jordan)
- R7: Möbius implementation (Jordan)
- R8: Literature refinement (Riley)

**Fits with existing schedule:**
- Phase 1 (Days 1-2): Quick wins (Tasks 001-006)
- Phase 2 (Days 3-4): Core improvements + **R1, R2**
- Phase 3 (Days 5-9): Strategic enhancements + **R3-R8**

---

## Part 7: Potential Outcomes

### Best Case: Research Validates Current Design
- Velocity weights match literature → cite sources
- Smoothstep validated → document empirical basis
- Progressive Möbius supported → implement with confidence
- Paper becomes perceptually-grounded specification

### Moderate Case: Research Suggests Refinements
- Adjust velocity weights to match findings
- Implement bounded velocity (Strategy 2) with perceptual bounds
- Design Möbius progressive inversion from adaptation research
- Paper shows evolution from prototype to principled design

### Worst Case: Research Reveals Gaps
- Limited temporal color perception literature
- No clear validation for velocity ratios
- Acknowledge as "design heuristics requiring future validation"
- Frame as research questions, not solved problems
- Still better than undocumented assumptions!

---

## Part 8: Why This Approach Is Right

### Current State (Engineering First)
- ❌ "We use curve parameter $t$ because it's simpler"
- ❌ "Velocity weights are from prototyping"
- ❌ "Möbius is theoretical, not validated"
- ❌ Reviewer: "Why these choices? Where's the research?"

### Proposed State (Perception First)
- ✅ "We ground velocity in temporal color perception research"
- ✅ "Attribute salience ratios validated by [Smith et al.]"
- ✅ "Möbius implements perceptually-smooth chromatic inversion per [Jones et al.]"
- ✅ Reviewer: "This is thoughtfully grounded in perception science"

### Strategic Advantage
- Color Journey's USP is **perceptual fidelity**
- Competitors may use arbitrary parameterization
- Literature grounding = **defensible novelty**
- Research gaps = **contribution opportunities** (user studies)

---

## Immediate Next Steps

1. **Agree on scope:** Do R1-R8 fit your vision?
2. **Prioritize:** Which research domain first (velocity or Möbius)?
3. **Assign:** Librarian (Ellis) starts literature review
4. **Timeline:** Confirm days 3-9 for research tasks
5. **Iterate:** Research may reveal new questions—that's good!

---

**Status:** ✅ RESEARCH AGENDA COMPLETE – Ready for task assignment

**Decision Point:** Shall we proceed with R1 (velocity literature) or R2 (Möbius literature) first?
