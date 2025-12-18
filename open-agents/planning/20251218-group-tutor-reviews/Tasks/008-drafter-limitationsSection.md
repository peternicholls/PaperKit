### 008-drafter-limitationsSection

**Agent:** ✍️ Section Drafter (Jordan)  
**Phase:** 2 (Core)  
**Estimated Time:** 45 minutes  
**Dependencies:** 001-librarian-foundationalReferences, 003-solver-mobiusVerification, 004-solver-velocityParameterization  
**Output Location:** `latex/sections/01_introduction.tex` (new §1.6)

---

#### 🎯 Philosophy & Context

**Remember:** This paper is about **perceptual-first design**. Honest limitations signal scientific integrity and point to perceptual research opportunities.

**Key Principles:**
- **Perception before engineering:** Focus on perceptual validation gaps, not implementation constraints
- **Research-grounded:** Frame as "what perceptual research is needed," not "what we couldn't implement"
- **Beyond current implementation:** Current limits are prototype boundaries; paper's limits are perceptual knowledge gaps

**For this task:** Transform limitations from apologies to "here's the perceptual research agenda this opens up."

---

#### Task Brief

Draft a new "Limitations & Future Validation" section to be inserted after §1.5 (Design Principles). This addresses Tutor B's core concern about making heuristics vs. empirical facts explicit.

#### Section Content

**Title:** Limitations \& Future Validation

**Subsections:**

1. **Perceptual Threshold Values** (~150 words)
   - Acknowledge ∆_min ≈ 2.0, ∆_max ≈ 5.0 are engineering heuristics
   - Note perceptual velocity weights are design-derived, not empirically validated
   - State they're "recommended engineering parameters" not psychophysically-derived constants
   - Reference Fairchild (2013) as informing source

2. **OKLab Adoption Recency** (~100 words)
   - Note OKLab (2020) vs CIELAB (1976) validation history
   - Acknowledge Levien (2021) is blog analysis, not peer-reviewed
   - State this reflects current best practice with awareness of recency risk

3. **Single-Anchor Expansion Scope** (~75 words)
   - Position as formalization and rigorous computational specification
   - Acknowledge related work in design tools
   - Don't overclaim novelty

4. **Technical Limitations** (~150 words)
   **✅ COMPREHENSIVE EVIDENCE:** See consolidated research §1.5 (Task 008)
   
   From RELEASENOTES.md (Known Issues L-001 to L-010):
   - Delta enforcement overhead (~6×) due to OKLab conversions
   - O(n) individual index access (must compute contrast chain)
   - Fixed delta parameters (0.02-0.05 range hardcoded in Sprint 004)
   - Maximum ΔE best-effort at boundaries (up to 5% may exceed)
   - Binary search monotonicity assumption (edge cases possible)
   - Index precision degradation beyond 1M colors (float limits)
   - Iterator not thread-safe (per-iterator, journey is thread-safe)
   
   From spec.md § Index Precision Guarantees:
   - 0 to 1M: Full precision guaranteed, perceptual error <0.02 ΔE
   - 1M to 10M: Warning range, perceptual error 0.02-0.10 ΔE
   - Beyond 10M: Not recommended

5. **Recommended Future Work** (~100 words as bullet list)
   - Psychophysical studies validating thresholds
   - User studies comparing output to professional tools
   - Context-aware gamut mapping for memory colors
   - Cross-platform performance benchmarking
   - Formal OKLab uniformity validation

#### LaTeX Structure

```latex
\section{Limitations \& Future Validation}
\label{sec:limitations}

This specification achieves rigorous formalization of perceptual palette 
generation in OKLab space, grounded in a working reference implementation 
(Sprint 004, December 2025). However, several design choices reflect 
engineering heuristics and first-implementation trade-offs rather than 
empirically-validated constants.

\subsection{Perceptual Threshold Values}
[Content per above]

\subsection{OKLab Adoption Recency}
[Content per above]

\subsection{Single-Anchor Expansion Scope}
[Content per above]

\subsection{Technical Limitations}
The reference implementation (Sprint 004) documents several known limitations:

\begin{itemize}
\item \textbf{Performance:} Delta enforcement overhead ($\sim$6×) due to OKLab conversions; O(n) individual index access requiring full contrast chain computation
\item \textbf{Precision:} Index precision guaranteed only to 1M colors; 1M–10M warning range with degraded accuracy; beyond 10M not recommended due to float precision limits
\item \textbf{Flexibility:} Delta parameters (0.02–0.05 ΔE) currently hardcoded; no API for override in Sprint 004
\item \textbf{Edge Cases:} Maximum ΔE best-effort at boundaries (up to 5\% may exceed threshold); binary search assumes monotonicity (edge cases possible in complex journeys)
\item \textbf{Concurrency:} Iterators not thread-safe (per-iterator state); journey handles are thread-safe for concurrent reads
\end{itemize}

See \texttt{RELEASENOTES.md} and \texttt{spec.md} (Sprint 004) for complete limitations catalog.

\subsection{Recommended Future Work}
\begin{itemize}
\item Psychophysical studies validating thresholds
\item User studies comparing output to professional tools
\item Context-aware gamut mapping for memory colors
\item Cross-platform benchmarking (ARM, x86, GPU)
\item Formal OKLab uniformity validation
\item API for runtime delta parameter overrides
\item Adaptive precision strategies for high-index generation
\end{itemize}
```

#### Tone Guidelines

- **Professional, not defensive:** This is standard academic practice
- **Confident but honest:** We know what we've validated and what we haven't
- **Forward-looking:** These are opportunities, not apologies

#### Success Criteria

- [ ] Section drafted with all four subsections
- [ ] Proper citations included (Fairchild, Levien, etc.)
- [ ] Cross-references to relevant sections (§4.1, §6.3, etc.)
- [ ] Inserted after §1.5 in introduction file
- [ ] Table of contents updated
- [ ] LaTeX compiles without errors
