### 010-drafter-gamutContextNuance

**Agent:** ✍️ Section Drafter (Jordan)  
**Phase:** 2 (Core)  
**Estimated Time:** 25 minutes  
**Dependencies:** None  
**Output Location:** `latex/sections/08_gamut_management.tex` (expand §8.4)

#### 🎯 Philosophy & Context

**Remember:** This paper is about **perceptual-first design**, not engineering documentation.

**Key Principles:**
- **Perception before engineering:** Gamut mapping priorities must be justified by perceptual goals (memory colors, emotional intent, cross-cultural preferences)
- **Research-grounded:** Different contexts have different perceptual priorities—cite studies on color preferences in different domains
- **Beyond current implementation:** Sprint 004 has one gamut strategy; the paper should explore the full design space of perceptually-motivated approaches
- **No backward compatibility:** We design for perceptual truth

**For this task:** "Hue is sacred" is a perceptual heuristic that works for certain contexts (e.g., product identity, photography). Other contexts prioritize different attributes (e.g., healthcare prioritizes luminance contrast, art may prioritize chroma intensity). Ground each priority hierarchy in perceptual research showing why it matters in that domain. This isn't about implementation flexibility—it's about understanding perception varies with context.

#### Task Brief

Add nuanced discussion of context-dependent gamut mapping to §8.4, addressing Tutor B's concern that "hue is sacred" hierarchy isn't universal.

#### Content to Add

**New subsection at end of §8.4:** Context-Dependent Gamut Mapping (~200 words)

```latex
\subsubsection{Context-Dependent Considerations}

The prioritization Hue $>$ Lightness $>$ Chroma is appropriate for 
\emph{general-purpose palette generation}. However, specific contexts 
may demand different strategies:

\paragraph{Brand Colors}
If an anchor represents a brand color, even chroma reduction may be 
unacceptable. In such cases, the gamut boundary becomes a hard 
constraint, and palette generation may need to expand along neighboring 
hues rather than reduce chroma. Brand-critical applications should 
consider pre-validating anchors are within target gamut.

\paragraph{Memory Colors}
For colors with strong cultural or perceptual associations---skin tones, 
grass green, sky blue---humans are highly sensitive to hue shifts. The 
standard hierarchy may need inversion: Lightness $>$ Hue $>$ Chroma. 
This domain warrants further investigation (see \S\ref{sec:future}).

\paragraph{Accessibility Considerations}
For colorblind users, certain hue combinations are indistinguishable. 
Context-aware gamut mapping might prioritize luminance separation over 
hue preservation, ensuring palettes remain discriminable across color 
vision deficiencies.

\begin{designdecision}
The default hierarchy serves general-purpose use. Domain-specific 
applications (branding, accessibility, memory colors) may override 
these defaults through configuration or post-processing.
\end{designdecision}
```

#### Also Update

**§12.3 (Future Directions):** Add reference to context-aware gamut mapping
```latex
\item Investigation of context-aware gamut mapping that weights hue 
preservation differently for memory colors versus arbitrary colors
```

#### Success Criteria

- [ ] Context-dependent subsection added to §8.4
- [ ] Three contexts addressed (brand, memory, accessibility)
- [ ] Design decision box explaining defaults vs. overrides
- [ ] Future directions updated with cross-reference
- [ ] LaTeX compiles without errors
