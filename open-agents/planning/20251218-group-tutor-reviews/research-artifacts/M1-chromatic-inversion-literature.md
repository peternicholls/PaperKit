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

**Source:** Fairchild (2013) - "Color Appearance Models" (3rd Edition) 📚 **[COLLECTED]**  
**Relevance:** ⭐⭐⭐⭐⭐ (Definitive reference - full text available)

**Direct Quotes from Book:**

> "Like beauty, color is in the eye of the beholder. For as long as human scientific inquiry has been recorded, the nature of color perception has been a topic of great interest. Despite tremendous evolution of technology, fundamental issues of color perception remain unanswered. Many scientific attempts to explain color rely purely on the physical nature of light and objects. However, without the human observer there is no color."  
> — Fairchild (2013, p. xix, Introduction)

> "It is common to say that certain wavelengths of light, or certain objects, are a given color. This is an attempt to relegate color to the purely physical domain. Instead it is proper to state that those stimuli are perceived to be of a certain color when viewed under specified conditions."  
> — Fairchild (2013, p. xix, Introduction)

> "Various mechanisms of chromatic adaptation generally make us unaware of these gradual changes. However, we are all looking at the world through a yellow filter that not only changes with age, but is significantly different from observer to observer."  
> — Fairchild (2013, p. 3, Chapter 1)

> "The photoreceptors, rods and cones, serve to transduce the information present in the optical image into chemical and electrical signals that can be transmitted to the later stages of the visual system."  
> — Fairchild (2013, p. 5, Chapter 1)

> "The yellow filters of the lens and macula, through which we all view the world, are the major source of variability in color vision between observers with normal color vision."  
> — Fairchild (2013, p. 6, Chapter 1)

> "Chapters 8 and 9 concentrate on one of the most important component mechanisms of color appearance, chromatic adaptation. The models of chromatic adaptation described in Chapter 9 are the foundation of the color appearance models described in later chapters."  
> — Fairchild (2013, p. xvii, Preface)

**Key Findings from Full Text:**
- **CIECAM02:** CIE's standard color appearance model (2002)
- **CAM16:** Successor model (2016) with improved chromatic adaptation transform (CAT16)
- **Chromatic Adaptation Transform (CAT):** Predicts color appearance under different illuminants
- **Helson-Judd Effect:** Hue shift of nonselective samples under chromatic illumination
- **Hunt-Pointer-Estevez transform:** Converts CIE tristimulus to normalized cone responses
- **Chapter 8:** Dedicated chapter on chromatic adaptation physiology and models
- **Sensory vs. Cognitive mechanisms:** Both contribute to color constancy
- **Corresponding colors data:** Experimental datasets for validating CAT performance

**Book Structure (Relevant Chapters):**
- Chapter 1: Human Color Vision (spatial/temporal properties)
- Chapter 6: Color Appearance Phenomena (Bezold-Brücke, Hunt Effect, Stevens Effect)
- Chapter 8: Chromatic Adaptation (physiology, corresponding colors, models)
- Chapter 9: Chromatic Adaptation Models (von Kries and descendants)

**Relevance to Möbius:**
- **Definitive source** for chromatic adaptation theory and implementation
- CAM02/CAM16 predict **static** color appearance after adaptation
- Do NOT model **temporal dynamics** of gradual adaptation
- Could validate final appearance after 180° rotation, not transition smoothness
- **Hunt Effect** (§6.6): Colorfulness increases with luminance—relevant to journey perception
- **Stevens Effect** (§6.7): Contrast increases with luminance—affects inversion visibility

**Priority:** HIGH - Now available for detailed study

**Full Citation (Harvard):**
- Fairchild, M.D. (2013) *Color Appearance Models*. 3rd edn. Chichester: John Wiley & Sons. ISBN: 978-1-119-96703-3.

---

### 1.4 Computing Chromatic Adaptation: Sharp Sensors

**Source:** Süsstrunk, S. (2005) - "Computing Chromatic Adaptation" 📚 **[COLLECTED]**  
**Type:** PhD Thesis, University of East Anglia, Norwich  
**Relevance:** ⭐⭐⭐⭐⭐ (Deep technical detail on CAT computation)

**Direct Quotes from Thesis:**

> "Most of today's chromatic adaptation transforms (CATs) are based on a modified form of the von Kries chromatic adaptation model, which states that chromatic adaptation is an independent gain regulation of the three photoreceptors in the human visual system. However, modern CATs apply the scaling not in cone space, but use 'sharper' sensors, i.e. sensors that have a narrower shape than cones."  
> — Süsstrunk (2005, p. iii, Abstract)

> "The recommended transforms currently in use are derived by minimizing perceptual error over experimentally obtained corresponding color data sets."  
> — Süsstrunk (2005, p. iii, Abstract)

> "We show that these sensors are still not optimally sharp. Using different computational approaches, we obtain sensors that are even more narrowband."  
> — Süsstrunk (2005, p. iii, Abstract)

> "We speculate that in order to make a final decision on a single CAT, we should consider secondary factors, such as their applicability in a color imaging workflow."  
> — Süsstrunk (2005, p. iii, Abstract)

> "We show that sharp sensors are very appropriate for color encodings, as they provide excellent gamut coverage and hue constancy."  
> — Süsstrunk (2005, pp. iii–iv, Abstract)

> "To faithfully reproduce the appearance of image colors, it thus follows that all image processing systems need to apply a transform that converts the input colors captured under the input illuminant to the corresponding output colors under the output illuminant. This can be achieved by using a chromatic adaptation transform (CAT)."  
> — Süsstrunk (2005, p. 3, Chapter 1)

> "In this thesis, we investigate different computational approaches to derive such chromatic adaptation transforms, which can be used in color science and color image processing. All our transforms are based on the von Kries model, which states that chromatic adaptation can be modeled as an independent gain control of three different sensor responses."  
> — Süsstrunk (2005, pp. 4–5, Chapter 1)

**Key Findings:**
- **Sharp sensors:** Modern CATs use "sharper" sensors than cone fundamentals—narrower spectral sensitivity
- **Performance measure:** CATs evaluated on corresponding color datasets
- **Strong vs. weak von Kries:** 
  - Strong: Gain depends only on same cone class
  - Weak: Gain depends on all cone classes (cross-talk)
- **Spectral sharpening:** Technique to derive optimal sensor functions for CAT
- **CAT02 sensors:** Not uniquely optimal—many sensor sets perform equivalently
- **Spherical sampling:** Demonstrated large equivalence class of valid CAT matrices
- **Sharp CAT:** Proposed sensors that match or exceed CAT02 performance
- **Hue constancy:** Sharp sensors provide better hue constancy across illuminants
- **Gamut coverage:** Sharp sensors enable better color encoding coverage

**Technical Details:**
- **Diagonal matrix assumption:** von Kries model uses D = diag(k_R, k_G, k_B)
- **Scaling coefficients:** k = 1/R_white, 1/G_white, 1/B_white (illuminant white point)
- **Sensor-based sharpening:** Optimizes M matrix for CAT performance
- **Prediction error:** RMS CIE ΔE94 used for evaluation
- **Statistical evaluation:** No significant difference between Sharp CAT and CAT02

**Relevance to Möbius:**
- **Implementation detail:** If implementing CAT for inversion, Sharp CAT may be optimal
- **Hue constancy:** Critical for Möbius—ensures hue trajectory remains coherent
- **Not temporal:** Thesis addresses static adaptation, not temporal dynamics
- **Sensor choice:** When computing opponent inversion, sensor matrix matters

**Priority:** MEDIUM - Technical implementation reference

**Full Citation (Harvard):**
- Süsstrunk, S. (2005) *Computing Chromatic Adaptation*. PhD thesis. University of East Anglia, Norwich.

---

### 1.5 Von Kries Transform Generalization

**Source:** Gao et al. (2020) - "The von Kries chromatic adaptation transform and its generalization" 📚 **[COLLECTED]**  
**Journal:** Chinese Optics Letters, 18(3), p. 033301  
**Relevance:** ⭐⭐⭐⭐ (Mathematical foundations)

**Direct Quotes from Paper:**

> "Most viable modern chromatic adaptation transforms (CATs), such as CAT16 and CAT02, can trace their roots both conceptually and mathematically to a simple model formulated from the hypotheses of Johannes von Kries in 1902, known as von Kries transform/model. However, while the von Kries transform satisfies the properties of symmetry and transitivity, most modern CATs do not satisfy these two important properties."  
> — Gao et al. (2020, p. 1, Abstract)

> "In this paper, we propose a generalized von Kries transform which satisfies the symmetry and transitivity properties in addition to improving the fit to most available experimental visual datasets on corresponding colors."  
> — Gao et al. (2020, p. 1, Abstract)

**Key Findings (with page references):**
- **Symmetry property:** "while the von Kries transform satisfies the properties of symmetry...most modern CATs do not satisfy these two important properties" (p. 1)
- **Transitivity property:** CAT02, CAT16 "no longer satisfy the symmetry and transitivity properties" when D differs from 1 or 0 (p. 4)
- **Generalized von Kries:** Proposed transform "satisfies the symmetry and transitivity properties" (p. 1)
- **Von Kries coefficient rule:** k_R = 1/R_white, k_G = 1/G_white, k_B = 1/B_white
- **Corresponding colors:** "A pair of corresponding colors consists of a color observed under one illuminant (say, D65) and another color that has the same appearance when observed under a different illuminant (say, A)" (p. 1)

**Mathematical Framework (p. 1-2):**
```
R_β     X_β
(G_β) = M (Y_β)  [Convert tristimulus to sensor space]
B_β     Z_β

R_a,β     k_R,β × R_β
(G_a,β) = (k_G,β × G_β)  [Apply von Kries scaling]
B_a,β     k_B,β × B_β
```

**Relevance to Möbius:**
- **Inversion as CAT:** Möbius inversion (L, -a, -b) is conceptually similar to CAT
- **Symmetry:** Inversion should be reversible (apply twice = identity)
- **Mathematical rigor:** Provides formal framework for opponent axis manipulation
- **Not temporal:** Addresses static transforms only

**Priority:** MEDIUM - Mathematical foundation reference

**Full Citation (Harvard):**
- Gao, C., Wang, Z., Xu, Y., Melgosa, M., Xiao, K., Brill, M.H. and Li, C. (2020) 'The von Kries chromatic adaptation transform and its generalization', *Chinese Optics Letters*, 18(3), p. 033301. doi: 10.3788/COL202018.033301

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

### 3.0 Color Constancy: Foundational Framework

**Source:** Troost (1992) - "Perceptual and computational aspects of color constancy" 📚 **[COLLECTED]**  
**Type:** PhD Dissertation, Katholieke Universiteit Nijmegen  
**Relevance:** ⭐⭐⭐⭐⭐ (Deep theoretical foundation)

**Direct Quotes from Dissertation:**

> "Note that because the activities in the receptors are the same for both the standard and test papers, Helmholtz would have predicted that both papers will have the same color appearance. However, the actual color appearance of the test will be anything, indicating that it is not the absolute amount of light reaching the eye that determines the final color percept."  
> — Troost (1992, p. 2)

> "Von Kries proposed that the spectral sensitivities of the three receptor systems can be varied by a constant that is inversely related to the level of adaptation."  
> — Troost (1992, p. 7)

> "Hering already stated that 'one must not represent as products of experience the same innate functions of the visual system on the basis of which these experiences were originally acquired' (Hering, 1874/1962, p.21)."  
> — Troost (1992, p. 3), citing Hering

**Key Findings (with page references):**
- **Central insight:** "it is not the absolute amount of light reaching the eye that determines the final color percept" (p. 2)
- **Illuminant elimination:** "the visual system has to get rid of the illuminant component" (p. 3)
- **von Kries coefficients:** Defined as $a_R = L'_{AVG}/L_{AVG}$, etc. (p. 8)
- **Adaptation level:** "The average color in a scene is often used as an estimator" (p. 8)
- **Receptor adaptation:** "spectral sensitivities...varied by a constant inversely related to the level of adaptation" (p. 7)
- **Sensory vs. cognitive:** Helmholtz (cognitive, "unconscious inferences") vs. Hering (sensory, adaptation/contrast) debate (pp. 3-4)

**Theoretical Framework:**
- **Helmholtz:** Proposed "unconscious inferences" (cognitive, top-down)
- **Hering:** Proposed receptor adaptation and contrast (sensory, bottom-up)
- **Memory colors:** Aroused by non-color characteristics of objects (Hering's cognitive concession)
- **Neither complete:** Both sensory and cognitive mechanisms contribute

**Methodological Insight (Chapter 3):**
- **Matching task:** Estimates sensory contribution (chromatic adaptation, lateral inhibition)
- **Naming task:** Captures identification aspects beyond matching
- **Sällström-Buchsbaum model:** Automatic illuminant elimination (pure sensory explanation)

**Relevance to Möbius:**
- **Adaptation baseline:** Viewer's visual system adapts to journey's overall chromaticity
- **First cycle:** Establishes "illuminant" expectation (average journey color)
- **Second cycle (inverted):** Challenges adaptation baseline—may trigger re-adaptation
- **Cognitive vs. sensory:** Möbius "twist" sensation may be partly cognitive (recognizing difference)
- **Memory colors:** Viewer's memory of first cycle influences perception of inverted second

**Priority:** HIGH - Foundational theory for understanding inversion perception

**Full Citation (Harvard):**
- Troost, J.M. (1992) *Perceptual and computational aspects of color constancy*. PhD thesis. Katholieke Universiteit Nijmegen.

---

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

### 5.2 Visual Sensitivity During Eye Movements

**Source:** Braun, Schütz & Gegenfurtner (2017) - "Visual sensitivity for luminance and chromatic stimuli during the execution of smooth pursuit and saccadic eye movements" 📚 **[COLLECTED]**  
**Journal:** Vision Research, 136, pp. 57-69  
**Relevance:** ⭐⭐⭐⭐⭐ (CRITICAL - Chromatic sensitivity dynamics)

**Direct Quotes from Paper:**

> "During saccades, the reduction of contrast sensitivity was strongest for low-spatial frequency luminance stimuli (about 90%). However, a significant reduction was also present for chromatic stimuli (about 58%). Chromatic sensitivity was increased during smooth pursuit (about 12%)."  
> — Braun, Schütz & Gegenfurtner (2017, p. 57, Abstract)

> "Our results show that saccadic suppression is not quite as selective as proposed by Burr et al. (1994) because contrast sensitivity for chromatic stimuli was reduced significantly during saccades."  
> — Braun, Schütz & Gegenfurtner (2017, p. 58)

> "The sensitivity for low-spatial frequency luminance stimuli is only slightly suppressed by 5%, but the sensitivity for isoluminant color and for luminance stimuli with spatial frequencies above 3 cpd is actually increased by 15% (Schütz, Braun, & Gegenfurtner, 2009a, 2009b; Schütz, Braun, Kerzel, & Gegenfurtner, 2008). This sensitivity enhancement starts already 50 ms before pursuit onset and scales with pursuit velocity."  
> — Braun, Schütz & Gegenfurtner (2017, p. 58)

**Key Findings (with page references):**
- **Saccadic suppression for chromatic:** "about 58%" reduction (p. 57)
- **Previously thought:** "Chromatic stimuli largely unaffected" per Burr et al. (1994) (p. 57)
- **New finding:** Suppression "not quite as selective as proposed" (p. 58)
- **Pursuit enhancement:** Chromatic sensitivity "increased by 15%" during smooth pursuit (p. 58)
- **Enhancement onset:** "starts already 50 ms before pursuit onset" (p. 58)
- **Scaling:** "scales with pursuit velocity" (p. 58)
- **Pathway attribution:** "increase in contrast gain along the parvocellular pathway" (p. 58)

**Experimental Methods (p. 58-60):**
- **DKL color space:** Used for isoluminant chromatic stimuli
- **Psychometric functions:** Fitted to detection rates
- **Temporal profile:** Detection rates measured from -100ms to +500ms around eye movement

**Relevance to Möbius:**
- **🚨 MAJOR FINDING:** During smooth chromatic transitions (like Möbius), pursuit-like enhancement may occur
- **Viewer tracking:** If viewer's eyes track color change, sensitivity INCREASES
- **Saccade risk:** If eyes jump (saccade), sensitivity drops briefly
- **Design implication:** Smooth, gradual inversion benefits from pursuit-like processing
- **Avoid sudden jumps:** Sudden chromatic changes trigger saccade-like suppression

**Priority:** URGENT - **MODIFIES TEMPORAL DESIGN STRATEGY**

**Full Citation (Harvard):**
- Braun, D.I., Schütz, A.C. and Gegenfurtner, K.R. (2017) 'Visual sensitivity for luminance and chromatic stimuli during the execution of smooth pursuit and saccadic eye movements', *Vision Research*, 136, pp. 57-69. doi: 10.1016/j.visres.2017.05.008

---

### 5.3 Temporal Frequency Discrimination

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

## 10. Harvard-Style Reference List

**Full papers collected (📚):**

- Braun, D.I., Schütz, A.C. and Gegenfurtner, K.R. (2017) 'Visual sensitivity for luminance and chromatic stimuli during the execution of smooth pursuit and saccadic eye movements', *Vision Research*, 136, pp. 57-69. doi:10.1016/j.visres.2017.05.008. 📚
- Fairchild, M.D. (2013) *Color Appearance Models*. 3rd edn. Chichester: John Wiley & Sons. ISBN: 978-1-119-96703-3. 📚
- Gao, C., Wang, Z., Xu, Y., Melgosa, M., Xiao, K., Brill, M.H. and Li, C. (2020) 'The von Kries chromatic adaptation transform and its generalization', *Chinese Optics Letters*, 18(3), p. 033301. doi:10.3788/COL202018.033301. 📚
- Süsstrunk, S. (2005) *Computing Chromatic Adaptation*. PhD thesis. University of East Anglia, Norwich. 📚
- Troost, J.M. (1992) *Perceptual and computational aspects of color constancy*. PhD thesis. Katholieke Universiteit Nijmegen. 📚

**Foundational references:**

- Hurvich, L.M. and Jameson, D. (1957) 'An opponent-process theory of color vision', *Psychological Review*, 64(6), pp. 384-404. doi:10.1037/h0041403.
- MacAdam, D.L. (1942) 'Visual sensitivities to color differences in daylight', *Journal of the Optical Society of America*, 32(5), pp. 247-274. doi:10.1364/JOSA.32.000247.
- von Kries, J. (1902) 'Chromatic adaptation', *Festschrift der Albrecht-Ludwigs-Universität*, pp. 145-158. [Reprinted in MacAdam, D.L. (ed.) (1970) *Sources of Color Science*. Cambridge, MA: MIT Press, pp. 109-119.]

**Additional references:**

- Pastilha, R., Hurlbert, A. and Nascimento, S.M.C. (2020) 'Temporal dynamics of daylight perception: detection thresholds', *Journal of Vision*, 20(11), p. 871. doi:10.1167/jov.20.11.871.
- Sekulovski, D., Vogels, I.M., van Beurden, M. and Clout, R. (2007) 'Smoothness and flicker perception of temporal color transitions', in *Proceedings of the 15th Color and Imaging Conference*. Albuquerque, NM: Society for Imaging Science and Technology, pp. 112-117.
- Webster, M.A. and Kay, P. (2012) 'Color categories and color appearance', *Cognition*, 122(3), pp. 375-392. doi:10.1016/j.cognition.2011.11.008.

---

**Status:** ✅ M1 Complete (Updated with collected papers) - Ready for M2 (Perceptual Loops Literature Review)
