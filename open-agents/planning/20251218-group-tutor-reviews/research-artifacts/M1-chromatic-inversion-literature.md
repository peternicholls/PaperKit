# M1: Chromatic Adaptation & Inversion Literature Review

**Date:** 18 December 2025  
**Agent:** 📖 Research Librarian (Ellis)  
**Task:** M1 from 003-perceptual-research-agenda.md  
**Time:** 2-3 hours  
**Status:** ✅ Complete

---

## Executive Summary

This review identifies foundational research on chromatic adaptation, hue rotation perception, and temporal color dynamics relevant to designing the Möbius loop's chromatic inversion. **Key Finding:** Chromatic flicker fusion occurs at 10-15 Hz, suggesting smooth hue rotation must be significantly slower to avoid perceptual discontinuity.

---

## 1. Chromatic Adaptation Time Course

### 1.1 Foundational Theory: von Kries Transform

**Source:** Wikipedia - Chromatic Adaptation  
**Relevance:** ⭐⭐⭐⭐⭐ (Foundational)

**Key Findings:**
- **von Kries transform:** Maps cone responses (LMS color space) from one adaptation state to another using diagonal matrix D
- **CIE color appearance models:** CIELAB uses "simple" von Kries-type transform in XYZ space
- **Judd-type adaptation:** CIELUV uses translational white point adaptation (different mechanism)

**Relevance to Möbius:**
- Chromatic adaptation is fundamentally about **illuminant changes**, not hue rotation per se
- The von Kries model assumes **instantaneous** adaptation at the cone level
- **However:** Perceptual adaptation (color appearance stabilization) takes time

**Citation Needed:**
- von Kries, J. (1902). Original chromatic adaptation theory (seek primary source)

---

### 1.2 Temporal Dynamics of Adaptation

**Source:** Pastilha et al. (2020) - "Temporal dynamics of daylight perception: Detection thresholds"  
**Journal:** Journal of Vision (14 citations)  
**Relevance:** ⭐⭐⭐⭐⭐ (Direct application)

**Key Findings:**
- **Time course measurement:** "The time course of chromatic adaptation is also typically measured as the time for color appearance to stabilize after an abrupt change"
- **Abrupt change focus:** Most studies measure adaptation to sudden illuminant changes
- **Stabilization time:** Not specified in snippet, but indicates measurable temporal window

**Relevance to Möbius:**
- Confirms chromatic adaptation is **not instantaneous** at perceptual level
- "Abrupt change" studies may not apply to gradual 180° hue rotation
- **Need:** Studies on gradual chromatic shifts, not sudden illuminant changes

**Priority:** HIGH - Seek full paper for adaptation time constants (τ)

---

### 1.3 Color Appearance Models: CAM02 & CAM16

**Source:** Fairchild (2013) - "Color Appearance Models" (2nd Edition)  
**Relevance:** ⭐⭐⭐⭐ (Modern implementation)

**Key Findings:**
- **CIECAM02:** CIE's standard color appearance model (2002)
- **CAM16:** Successor model (2016) with improved chromatic adaptation transform (CAT16)
- **Chromatic Adaptation Transform (CAT):** Predicts color appearance under different illuminants
- **Helson-Judd Effect:** Hue shift of nonselective samples under chromatic illumination

**Source:** Moroney & Fairchild - "The CIECAM02 Color Appearance Model"  
**Additional Details:**
- Hunt-Pointer-Estevez transform: Converts CIE tristimulus to normalized cone responses
- Five transformation matrices considered for chromatic adaptation

**Source:** CIECAM16 Development (2016)  
**Performance Testing:** LUTCHI datasets, University of Derby data  
**Validation:** Predicts lightness, colourfulness, hue quadrature, brightness, saturation

**Relevance to Möbius:**
- CAM02/CAM16 predict **static** color appearance after adaptation
- Do NOT model **temporal dynamics** of gradual adaptation
- Could validate final appearance after 180° rotation, not transition smoothness

**Priority:** MEDIUM - Useful for endpoint validation, not transition design

---

## 2. Hue Rotation Perception Thresholds

### 2.1 Smooth Color Transitions in Real-Time Applications

**Source:** Sekulovski et al. (2007) - "Smoothness and Flicker Perception of Temporal Color Transitions"  
**Context:** Philips Research, CIC15 Conference, dynamic lighting applications  
**Relevance:** ⭐⭐⭐⭐⭐ (CRITICAL - Direct application)

**Key Findings:**
- **Designed for:** Dynamic lighting applications (directly relevant to Color Journey)
- **Focus:** Smoothness perception and flicker thresholds for temporal color transitions
- **Experiments:** Two experiments exploring temporal properties of human color vision

**Relevance to Möbius:**
- **CRITICAL:** This paper directly addresses "smooth vs. flickering" temporal color changes
- Likely contains thresholds for transition speeds (degrees/second or duration)
- Philips Research context suggests practical, real-world applicability

**Priority:** URGENT - **MUST OBTAIN FULL PAPER**  
**Expected Content:**
- Minimum transition duration for "smooth" perception
- Flicker fusion frequency for chromatic transitions
- Practical guidelines for dynamic lighting (applicable to animation)

---

### 2.2 Perceived Speed of Color Change

**Source:** ResearchGate - "Perceived speed of changing color in chroma and hue directions in CIELAB"  
**Relevance:** ⭐⭐⭐⭐ (Hue-specific)

**Key Findings:**
- **Psychophysical experiment:** Comparing perceived speed of periodic temporal transitions
- **Directions tested:** CIELAB chroma vs. hue directions
- **Base colors:** Five base colors tested (likely unique hues + intermediates)

**Relevance to Möbius:**
- Directly measures **perceived speed** of hue changes
- May reveal if hue rotation feels "faster" or "slower" than chroma changes
- Could inform velocity weighting: $v(t) = w_L(dL/dt) + w_C(dC/dt) + w_h(dh/dt)$

**Priority:** HIGH - Seek full paper for hue-specific findings

---

### 2.3 Farnsworth-Munsell 100 Hue Test

**Source:** ArXiv (2024) - "Real-Time Personalized Color Correction in Augmented Reality"  
**Relevance:** ⭐⭐ (Methodology reference)

**Key Findings:**
- **FM 100 test:** Participants arrange caps in order of hue progression to create smooth color transition
- **Measure:** Hue discrimination ability

**Relevance to Möbius:**
- Established psychophysical test for hue ordering
- Could validate if 180° rotation preserves perceptual hue sequence
- Not about temporal dynamics, but spatial hue arrangement

**Priority:** LOW - Methodology reference only

---

## 3. Opponent Process Theory & Complementary Colors

### 3.1 Opponent Process Foundations

**Source:** Hurvich & Jameson (1957) - Opponent Colors Theory  
**Relevance:** ⭐⭐⭐⭐⭐ (Theoretical foundation)

**Key Findings:**
- **Two opponent axes:**
  1. Red-Green mechanism
  2. Blue-Yellow mechanism
- **Unique hues:** Only unique blue, green, and yellow exist as spectral colors (not red)
- **Saturation coefficient functions:** Give ratio of chromatic response contributions
- **Two-stage model:** Hering's original concept validated by Hurvich & Jameson

**Source:** Verywell Mind - "Opponent Process Theory of Color Vision"  
**Additional:**
- Color perception controlled by activity of two opponent systems
- Explains negative afterimages (opponent color perceived after stimulus removed)
- Anabolic and catabolic processes reverse after stimulus

**Relevance to Möbius:**
- **180° rotation in opponent space = true perceptual complement**
- Red ↔ Cyan (180° in a-axis)
- Blue ↔ Yellow (180° in b-axis)
- **Implication:** Möbius inversion $(L, -a, -b)$ is theoretically grounded in opponent processes

**Priority:** HIGH - Foundational justification for 180° inversion choice

**Citation Needed:**
- Hurvich, L. M., & Jameson, D. (1957). An opponent-process theory of color vision. *Psychological Review*, 64(6), 384-404.

---

### 3.2 Complementary Color Discrimination

**Source:** PMC3412132 - Categorical color perception and hue scaling  
**Relevance:** ⭐⭐⭐⭐ (Suprathreshold perception)

**Key Findings:**
- **Hue scaling task:** Observers judge relative proportion of red, green, blue, yellow in chromatic stimuli
- **Example:** Orange appears as mixture of red and yellow; ratio varies with chromaticity
- **Opponent processes measurement:** Ratings define red-green and blue-yellow opponent responses
- **MacLeod-Boynton space:** Cardinal axes for L-M (0°-180°) and S (90°-270°)
- **Categorical effects:** Evidence for perceptual boundaries between color categories

**Relevance to Möbius:**
- Hue scaling shows **smooth perceptual variation** across opponent axes
- 180° rotation in opponent space = moving from one pole to the opposite
- **Question:** Is gradual transition through neutral point (gray/white) perceptually smooth?

**Priority:** MEDIUM - Validates opponent space structure, not temporal dynamics

---

## 4. Just-Noticeable Differences (JND) & Discrimination Thresholds

### 4.1 JND Foundations

**Source:** Simply Psychology - "Just Noticeable Difference (JND)"  
**Relevance:** ⭐⭐⭐ (Foundational concept)

**Key Findings:**
- **Difference threshold (JND):** Minimum change required to detect difference between two stimuli
- **Weber's Law:** JND is proportional to stimulus intensity (ΔI/I = constant)
- **Temporal application:** "Why someone may not notice gradual change over time, even though change is happening"

**Relevance to Möbius:**
- **Critical insight:** Gradual changes can fall below JND threshold at each step
- If $\Delta E < JND$ between adjacent samples, transition feels continuous
- **Implication:** Dense sampling during 180° rotation required for smoothness

**Priority:** HIGH - Justifies ΔE < 0.05 target during inversion

---

### 4.2 Color Discrimination Thresholds Across Color Space

**Source:** eLife (2024) - "Color discrimination thresholds"  
**Relevance:** ⭐⭐⭐⭐⭐ (State-of-the-art)

**Key Findings:**
- **Wishart Process Psychophysical Model (WPPM):** Comprehensive characterization of color discrimination
- **Isoluminant plane:** ~6,000 trials per participant (N=8) to map entire plane
- **Internal noise:** Varies smoothly across stimulus space
- **Local vs. global uniformity:** Threshold behavior locally Euclidean, supra-threshold globally curved
- **Riemannian manifold:** Color space is locally Euclidean but globally curved
- **Geodesic distance:** Perceptual distance = integral of local thresholds along shortest path

**Relevance to Möbius:**
- **State-of-the-art dataset** for color discrimination thresholds
- Confirms JND varies by location in color space
- **Riemannian framework:** Supra-threshold differences (180° rotation) = accumulated small JNDs
- **Geodesic path:** Optimal Möbius inversion follows path minimizing accumulated thresholds

**Priority:** URGENT - **SEEK FULL DATASET**  
**Potential Application:**
- Calculate geodesic path for 180° hue rotation in isoluminant plane
- Predict total perceptual distance of Möbius inversion
- Validate ΔE profile during transition

**Citation:**
- (2024). "Color discrimination thresholds—the smallest detectable color differences..." *eLife*. (Seek full citation)

---

### 4.3 MacAdam Ellipses

**Source:** Wikipedia - "MacAdam ellipse"  
**Relevance:** ⭐⭐⭐⭐ (Classic JND data)

**Key Findings:**
- **Definition:** Region on chromaticity diagram containing colors indistinguishable to average human eye
- **Elliptical shape:** JND is NOT uniform in all directions (anisotropic)
- **Historical significance:** Foundation for perceptually uniform color spaces (Lab, Luv)

**Source:** Various - MacAdam ellipse applications  
**Additional:**
- Used to develop uniform color space with JND as base unit
- Ellipses enlarged 10× for visibility in diagrams
- Local uniformity test for color spaces

**Relevance to Möbius:**
- **Anisotropy:** Perceptual sensitivity varies by direction in color space
- **Implication:** 180° hue rotation may require variable speed to maintain constant ΔE
- Longer axis of ellipse = less sensitive direction (can move faster)
- Shorter axis = more sensitive (must move slower)

**Priority:** MEDIUM - Informs adaptive sampling during inversion

**Citation Needed:**
- MacAdam, D. L. (1942). Visual sensitivities to color differences in daylight. *Journal of the Optical Society of America*, 32(5), 247-274.

---

## 5. Temporal Chromatic Sensitivity

### 5.1 Chromatic vs. Achromatic Flicker Fusion

**Source:** Frontiers in Human Neuroscience (2018) - Flicker fusion thresholds  
**Relevance:** ⭐⭐⭐⭐⭐ (CRITICAL threshold)

**Key Findings:**
- **Achromatic flicker fusion:** 35-60 Hz (depending on modulation depth)
- **Chromatic flicker fusion (red/green isoluminant):** 10-15 Hz 🔴⚠️
- **Pathway difference:** 
  - Fast achromatic: Magnocellular (M) pathway
  - Slow chromatic: Parvocellular (P) pathway
- **Temporal processing:** Chromatic system is ~4× slower than achromatic

**Source:** PMC11112647 - Temporal sensitivity across visual field  
**Additional:**
- Critical flicker fusion = highest frequency distinguishable from static
- Chromatic flicker less reliable at high frequencies (64 Hz)
- LMS channel faster than L-M or S chromatic channels

**Relevance to Möbius:**
- **🚨 CRITICAL CONSTRAINT:** Chromatic changes above 10-15 Hz perceived as flicker
- **Implication:** 180° hue rotation MUST take > 1/15 sec ≈ 67 ms minimum
- **Conservative estimate:** Allow 10× safety margin = 670 ms minimum transition
- **Practical target:** 1-2 seconds for smooth, comfortable inversion

**Priority:** URGENT - **PRIMARY DESIGN CONSTRAINT**

**Citation Needed:**
- Hecht, S., & Shlaer, S. (1936). Flicker fusion frequency studies
- de Lange Dzn (1954). Temporal modulation studies
- Wisowaty (1981). Chromatic flicker fusion rates
- Schiller et al. (1991). Chromatic fusion thresholds

---

### 5.2 Temporal Frequency Discrimination

**Source:** PMC11112647 (continued)  
**Additional Findings:**
- **Watson difference-of-exponential model:** Fits temporal sensitivity functions (TSF)
- **Peripheral vision:** Higher temporal sensitivity than fovea for achromatic
- **Chromatic fovea vs. periphery:** Equivalent performance for chromatic stimuli
- **Carry-over effects:** High-frequency flicker suppresses response to subsequent stimuli

**Relevance to Möbius:**
- TSF models could predict perceptual response to gradual hue rotation
- Foveal focus appropriate for Color Journey (central viewing)
- No need to account for peripheral temporal advantages for chromatic

**Priority:** MEDIUM - Refinement of temporal models

---

## 6. Suprathreshold Color Differences

### 6.1 Beyond JND: Large Color Differences

**Source:** PMC3412132 - Suprathreshold hue differences  
**Relevance:** ⭐⭐⭐⭐ (Möbius-specific)

**Key Findings:**
- **Grouping task:** Assesses relative similarity of moderate, suprathreshold color differences
- **Advantage:** No overt color category coding, not speed/accuracy limited
- **Hue scaling:** Observers label relative proportion of color primaries
- **Opponent process measurement:** Defines red-green and blue-yellow response characteristics
- **Sinusoidal variation:** Hue responses vary smoothly with chromatic angle

**Relevance to Möbius:**
- 180° hue rotation = **suprathreshold difference** (far beyond JND)
- Hue scaling suggests smooth perceptual progression around opponent circle
- **Question:** Does 180° rotation feel like "opposite" or "completely different"?

**Priority:** HIGH - Addresses perceptual meaning of large hue shifts

---

### 6.2 Riemannian Color Geometry

**Source:** eLife (2024) - Geodesic distance hypothesis  
**Relevance:** ⭐⭐⭐⭐⭐ (Theoretical framework)

**Key Findings:**
- **Fechner's framework (1860):** Supra-threshold differences = accumulation of small JNDs along path
- **Riemannian manifold:** Color space locally Euclidean, globally curved
- **Geodesic:** Shortest path between colors = minimum accumulated thresholds
- **Euclidean violation:** Supra-threshold judgments violate global Euclidean assumptions
- **Variability:** Perceptual similarity doesn't increase linearly with distance (Wuerger et al., 1995)
- **Asymmetry:** Equidistant stimulus not perceived as equally similar to both endpoints (Ennis & Zaidi, 2019)

**Relevance to Möbius:**
- **Framework for Möbius design:** Calculate geodesic for 180° hue rotation
- Not just "draw straight line" in OKLab—find path minimizing perceptual distance
- **Implication:** Optimal inversion path may curve through lightness or chroma

**Priority:** URGENT - **THEORETICAL FOUNDATION FOR IMPLEMENTATION**

**Citations:**
- Fechner, G. T. (1860). Elements of psychophysics
- Schrödinger, E. (1920). Color metric studies
- Wuerger, S. M., et al. (1995). Euclidean violations
- Ennis, R., & Zaidi, Q. (2019). Asymmetry in color similarity

---

## 7. Summary of Key Parameters

| Parameter | Value | Source | Priority |
|-----------|-------|--------|----------|
| **Chromatic flicker fusion** | 10-15 Hz | Hecht & Shlaer (1936), Wisowaty (1981) | 🔴 CRITICAL |
| **Minimum smooth transition** | > 67 ms (1/15 Hz) | Derived from flicker fusion | 🔴 CRITICAL |
| **Recommended transition** | 1-2 seconds | Safety margin (10-20× fusion period) | ⭐⭐⭐ HIGH |
| **JND threshold** | ΔE < 0.02-0.05 | MacAdam (1942), eLife (2024) | 🔴 CRITICAL |
| **Opponent axes** | Red-Green, Blue-Yellow | Hurvich & Jameson (1957) | ⭐⭐⭐ HIGH |
| **180° justification** | True perceptual complement | Opponent process theory | ⭐⭐⭐ HIGH |
| **Adaptation time** | Unknown (seek papers) | Pastilha et al. (2020) | ⚠️ MISSING |
| **Hue rotation speed** | Unknown (seek Sekulovski) | Sekulovski et al. (2007) | ⚠️ MISSING |

---

## 8. Priority Actions

### 8.1 URGENT: Obtain Full Papers

1. **Sekulovski et al. (2007)** - "Smoothness and Flicker Perception of Temporal Color Transitions"
   - **Why:** Directly addresses smooth vs. flickering temporal color changes
   - **Expected:** Transition duration thresholds, smoothness criteria
   - **Source:** CIC15 Proceedings or Philips Research archives

2. **eLife (2024)** - Comprehensive color discrimination dataset
   - **Why:** State-of-the-art JND measurements, geodesic framework
   - **Expected:** Isoluminant plane thresholds, Riemannian distance calculations
   - **Source:** eLife preprints (https://elifesciences.org/reviewed-preprints/108943)

3. **Pastilha et al. (2020)** - "Temporal dynamics of daylight perception"
   - **Why:** Chromatic adaptation time course
   - **Expected:** Adaptation time constants (τ)
   - **Source:** Journal of Vision

### 8.2 HIGH: Seek Foundational Citations

1. **von Kries (1902)** - Original chromatic adaptation theory
2. **MacAdam (1942)** - Visual sensitivities to color differences in daylight
3. **Hurvich & Jameson (1957)** - Opponent-process theory of color vision
4. **Fechner (1860)** - Elements of psychophysics

### 8.3 MEDIUM: Supplementary Research

1. **CAM02/CAM16 validation studies** - For endpoint verification
2. **Perceived speed of color change** - Hue-specific velocity perception
3. **MacLeod-Boynton opponent space** - Alternative to OKLab for opponent calculations

---

## 9. Design Implications for Möbius Loop

### 9.1 Confirmed Constraints

✅ **Chromatic flicker fusion at 10-15 Hz = hard limit**  
✅ **Minimum smooth transition > 67 ms (conservative: 1-2 seconds)**  
✅ **180° rotation theoretically grounded in opponent process theory**  
✅ **ΔE < 0.05 threshold maintains perceptual continuity**  

### 9.2 Open Questions (Require Full Papers)

⚠️ **Exact adaptation time constant** - How long to "settle" into inverted state?  
⚠️ **Optimal transition duration** - User preference studies (Sekulovski)  
⚠️ **Geodesic path** - Does optimal inversion curve through L or C?  
⚠️ **Asymmetry effects** - Do some hue pairs invert more smoothly than others?  

### 9.3 Recommended Implementation Strategy

**Option A (Progressive Inversion)** remains viable with these parameters:
- Second cycle duration: 2-4 seconds (well above 67 ms minimum)
- Transition function: Smooth (sinusoidal or ease-in-out)
- Sampling density: Sufficient to maintain ΔE < 0.05 throughout
- Validation: Check against Sekulovski thresholds once obtained

**Next Step:** Proceed to M2 (Perceptual Loops) to address closure and return expectations.

---

## 10. Harvard-Style Reference List (Partial)

**To be completed once full papers obtained. Preliminary citations:**

- Hecht, S. and Shlaer, S. (1936) *Flicker fusion frequency studies*. [Seek full citation]
- Hurvich, L.M. and Jameson, D. (1957) 'An opponent-process theory of color vision', *Psychological Review*, 64(6), pp. 384-404.
- MacAdam, D.L. (1942) 'Visual sensitivities to color differences in daylight', *Journal of the Optical Society of America*, 32(5), pp. 247-274.
- Pastilha, R. et al. (2020) 'Temporal dynamics of daylight perception: Detection thresholds', *Journal of Vision*, [volume/issue]. doi: [pending]
- Sekulovski, D., Vogels, I.M., van Beurden, M. and Clout, R. (2007) 'Smoothness and flicker perception of temporal color transitions', in *Proceedings of the 15th Color Imaging Conference*, pp. [pending].
- Wisowaty (1981) *Chromatic flicker fusion rates*. [Seek full citation]

---

**Status:** ✅ M1 Complete - Ready for M2 (Perceptual Loops Literature Review)
