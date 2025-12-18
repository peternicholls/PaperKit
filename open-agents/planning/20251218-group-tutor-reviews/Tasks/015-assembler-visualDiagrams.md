### 015-assembler-visualDiagrams

**Agent:** 🔧 LaTeX Assembler (Taylor)  
**Phase:** 3 (Strategic)  
**Estimated Time:** 3-4 hours  
**Dependencies:** 002-refiner-spellingNotation (ensures consistent terminology)  
**Output Location:** `latex/figures/`, relevant section files

#### 🎯 Philosophy & Context

**Remember:** This paper is about **perceptual-first design**, not engineering documentation.

**Key Principles:**
- **Perception before engineering:** Diagrams should illustrate perceptual concepts (JND regions, temporal transitions, color space topology) not system architecture
- **Research-grounded:** Visual representations should clarify perceptual principles from research literature
- **Beyond current implementation:** Show the design space, not just Sprint 004's implementation
- **No backward compatibility:** We design for perceptual truth

**For this task:** Create diagrams that help readers understand perceptual concepts: (1) OKLab perceptual uniformity vs RGB, (2) temporal color transition showing ΔE thresholds, (3) journey construction in 3D color space, (4) gamut mapping preserving perceptual intent. Avoid flowcharts/UML—use perceptual visualizations (color gradients with ΔE markers, 3D color space plots, time-series showing smooth transitions). Think "Nature/Science figures" not "software documentation."

#### Task Brief

Create visual diagrams to enhance comprehension of key concepts. Both tutors noted the absence of figures.

#### Diagrams to Create

**Figure 2.1: RGB vs OKLab Interpolation**
- Location: §2.2 (Perceptual Foundations)
- Content: Side-by-side gradient showing:
  - Linear RGB interpolation (shows muddy middle)
  - OKLab interpolation (perceptually uniform)
- Purpose: Visually justify OKLab choice
- Method: TikZ or imported PNG from implementation

**Figure 3.1: Bézier Control Point Placement**
- Location: §3.2-3.3 (Journey Construction)
- Content: Diagram showing:
  - Anchor points
  - Control points determining curve shape
  - Resulting trajectory in abstract 2D space
- Purpose: Illustrate mood trajectory construction
- Method: TikZ path diagram

**Figure 4.1: Constraint Visualization**
- Location: §4.3 (Perceptual Constraints)
- Content: OKLab space slice showing:
  - ∆_min boundary (minimum separation)
  - ∆_max boundary (maximum separation)
  - Valid region between constraints
- Purpose: Make abstract constraints tangible
- Method: TikZ with shaded regions

**Figure 7.1: Loop Strategies Comparison**
- Location: §7 (Loop Strategies)
- Content: Three sub-figures showing:
  - Linear loop progression
  - Sinusoidal (oscillating) loop
  - Möbius (twisted) loop
- Purpose: Show how loop shape affects palette
- Method: TikZ curves or imported diagrams

#### LaTeX Integration

For each figure:

```latex
\begin{figure}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{figures/figure_name.pdf}
% OR TikZ inline:
% \begin{tikzpicture}
% ...
% \end{tikzpicture}
\caption{Caption text explaining the figure}
\label{fig:figure-label}
\end{figure}
```

Add references in text:
```latex
As illustrated in Figure~\ref{fig:oklab-comparison}, OKLab interpolation 
maintains perceptual uniformity...
```

#### Success Criteria

- [ ] All four figures created
- [ ] Consistent visual style across figures
- [ ] Proper LaTeX figure environments
- [ ] Captions and labels included
- [ ] References added in relevant sections
- [ ] LaTeX compiles without errors
- [ ] Figures render correctly in PDF
