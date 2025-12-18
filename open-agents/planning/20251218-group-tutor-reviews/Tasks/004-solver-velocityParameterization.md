### 004-solver-velocityParameterization

**Agent:** 🔬 Problem Solver (Quinn)  
**Phase:** 1 (Quick Win)  
**Estimated Time:** 30 minutes  
**Dependencies:** None  
**Output Location:** `open-agents/planning/20251218-group-tutor-reviews/velocity-analysis.md`

#### Task Brief

Tutor A identified ambiguity in the perceptual velocity formula (§6.3):

> "The formula $v = w_L \frac{dL}{dt} + w_a \frac{da}{dt} + w_b \frac{db}{dt}$ is ambiguous. Clarify if the derivative is with respect to parameter $t$ or arc-length $s$."

Your task is to determine the correct parameterization and propose clarifying text.

**✅ IMPLEMENTATION EVIDENCE FOUND:** Research consolidation provides concrete answer.

**Evidence:** See `.paper/data/output-refined/research/technical-documentation-consolidated.md` §1.2:

From PRD.md §3.3:
> "The route can be expressed as: A continuous function t ∈ [0, 1] → OKLab"

From Architecture.md:
> "Journey sampling: Waypoint interpolation in LCh space. Smoothstep easing (cubic polynomial, not transcendental)"

**Conclusion:** Parameter is **curve parameter t**, not arc-length s.
- The implementation uses smoothstep easing for pacing
- Derivatives are with respect to curve parameter t
- Perceptual velocity varies with Bézier control point placement

#### Analysis Required

1. **Read §6.3** (Perceptual Velocity) and understand current specification

2. **Determine parameterization:**
   - **If parameter $t$ (curve parameter):** Velocity varies with Bézier control point placement; "acceleration" occurs at inflection points
   - **If arc-length $s$:** Rate of attribute change is constant per unit distance traveled; "velocity" = attribute change per perceptual distance

3. **Consider implementation intent:**
   - What makes more sense for "mood dynamics"?
   - What's more computationally tractable?
   - What do existing implementations use?

4. **Document findings:**
   ```markdown
   ## Perceptual Velocity Parameterization Analysis
   
   ### Current Formula
   $v = w_L \frac{dL}{dt} + w_a \frac{da}{dt} + w_b \frac{db}{dt}$
   
   ### Parameterization Assessment
   - **Most likely intent:** [t / s]
   - **Reasoning:** [explanation]
   
   ### Implications
   - If using $t$: [what this means for velocity behavior]
   - If using $s$: [what this means for velocity behavior]
   
   ### Recommended Clarification
   
   **Add to §6.3 (before or after formula):**
   > "Note: Derivatives are taken with respect to the curve parameter $t \in [0,1]$, not arc-length $s$. As a consequence, perceptual velocity varies with the placement of Bézier control points—regions with tighter curvature exhibit higher perceptual acceleration. This allows mood dynamics to emphasize certain hue ranges through geometric path design."
   
   **Add to Appendix B (Notation):**
   ```latex
   $t$ & Curve parameter, $t \in [0,1]$ & Parameterizes the journey path \\
   $s$ & Arc-length parameter & Not used in this specification \\
   $\frac{dL}{dt}$, $\frac{da}{dt}$, $\frac{db}{dt}$ & Perceptual derivatives & With respect to curve parameter $t$ \\
   ```
   
   **Reference Implementation:**
   - See Sprint 004 spec.md for position calculation: `t = fmodf((float)index * 0.05f, 1.0f)`
   - Smoothstep easing documented in Architecture.md
   ```

#### Success Criteria

- [ ] Parameterization determined (t vs s)
- [ ] Implications documented
- [ ] Clarifying text proposed for §6.3
- [ ] Notation addition proposed for Appendix B
- [ ] Ready for Section Drafter to implement
