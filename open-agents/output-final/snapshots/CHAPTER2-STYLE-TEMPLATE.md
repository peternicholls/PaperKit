# Chapter 2 Style Template & Structural Checklist

**Status:** Chapter 2 (Perceptual Foundations) signed off as of commit `paper-v0.2-ch2-signedoff`  
**Purpose:** This checklist defines the structural conventions, citation discipline, and formatting standards established in Chapter 2 that should be replicated in all subsequent chapters.

---

## 🔒 Read-Only Policy for Chapter 2

**LOCKED FOR CONCEPTUAL EDITS** as of tag `paper-v0.2-ch2-signedoff`

**Permitted modifications:**
- ✅ Typo corrections
- ✅ LaTeX build fixes
- ✅ Reference formatting updates
- ✅ Cross-reference fixes (e.g., broken `\ref{}` commands)

**Prohibited modifications:**
- ❌ Conceptual rewrites
- ❌ Structural reorganization
- ❌ Adding new subsections
- ❌ Changing argument flow

---

## 📐 Structural Template

### Header Block Format
```latex
% ==============================================================================
% Section X: [Chapter Title]
% ==============================================================================
% VERSION: [number] ([status] - [date])
% Research Integration: [key citations]
% Refinement: [what was improved]
% Target Length: [word count range]
% Dependencies: [other sections, or "None"]
% ==============================================================================
```

**Chapter 2 Example:**
```latex
% VERSION: 3 (Refined - 30 Dec 2025)
% Research Integration: Hong (2024), Nölle (2012), Braun (2017), Sekulovski (2007)
% Refinement: Implemented tutor feedback - citation page numbers, transitions, definitions
% Target Length: 3,000–3,500 words
% Dependencies: None (foundational section)
```

### Section Hierarchy

**Chapter 2 structure (use as template):**

1. **Top-level section** (`\section{}`) — Chapter title
   - Brief introductory paragraph (3-5 sentences) establishing scope
   
2. **Major subsections** (`\section{}`) — Conceptual blocks
   - Each major idea gets its own numbered section
   - Example: "Color Space as Riemannian Manifold"
   
3. **Thematic subsections** (`\subsection{}`) — Detailed development
   - Theoretical Framework
   - Practical Implications
   - Computational Approximation
   - Design Implications
   - Summary sections
   
4. **Unnumbered subsections** (`\subsubsection*{}`) — Technical details
   - Mathematical derivations
   - Specific technical points
   - Implementation notes

**Depth discipline:**
- Maximum 3 levels of nesting (section → subsection → subsubsection)
- Use unnumbered `\subsubsection*{}` for minor technical points
- Avoid orphaned subsections (don't have just one subsection under a section)

---

## 📚 Citation Discipline

### Page Number Requirements

**Chapter 2 standard:**  
Every quotation and specific factual claim MUST include page numbers.

**Format examples:**
```latex
% Direct quote
\citep[p.~3]{kong2021}

% Page range
\citep[pp.~113--114]{sekulovski2007}

% Multiple references with pages
\citep[p.~2]{nolle2012} ... \citep[p.~9]{nolle2012}

% Year only for general attribution
\citeyearpar{hong2024}
```

### Citation Context Requirements

1. **First mention:** Full context with what the study measured
   - ❌ "Hong et al. found that..."
   - ✅ "Hong et al. \citeyearpar{hong2024} characterized this structure empirically through approximately 6,000 discrimination threshold trials per participant, mapping elliptical contours of equal perceptual distance across color space."

2. **Methodological notes:** Use footnotes for methodology details
   ```latex
   \footnote{Hong et al.'s study employed the Bayesian Wishart Process 
   Psychophysical Model (WPPM) within a Riemannian manifold framework...}
   ```

3. **Quote integration:** Blockquote format for substantial quotes
   ```latex
   \begin{quote}
   ``The visibility threshold of smoothness... is about ten times smaller 
   for lightness changes than for chroma or hue changes in CIELAB'' 
   \citep[p.~3]{kong2021}.
   \end{quote}
   ```

### Footnote Usage

**Chapter 2 conventions:**

1. **Methodological details** — Study design that would disrupt flow
2. **Historical context** — Background on theories/concepts
3. **Implementation notes** — Technical details for implementers
4. **Caveats** — Scope limitations or assumptions
5. **Source code attribution** — License and URL for code references

**Example:**
```latex
\footnote{Sekulovski's research at Philips Research introduced the 
Delta-E-ab per second metric for temporal color transitions, establishing 
that smoothness thresholds are approximately 10 times smaller for luminance 
than for chroma/hue changes in CIELAB.}
```

---

## 🎯 Figure Integration

### Figure Placement Strategy

**Chapter 2 standard:**  
Figures referenced **before** they appear, with justification in running text.

**Pattern:**
1. Textual explanation of the concept
2. In-text reference: "...as Figure X illustrates"
3. Figure placement immediately after paragraph or logical section break
4. Figure includes fallback placeholder for missing PDFs

**Example pattern:**
```latex
% Text references figure
...visualization. Figure~\ref{fig:temporal-weights} visualizes the 
intuition: small changes in lightness are typically more salient...

% Figure appears after paragraph
\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\linewidth]{figures/temporal-weights.pdf}
\caption{Temporal channel weighting for perceived smoothness...}
\label{fig:temporal-weights}
\end{figure}
```

### Caption Format

**Chapter 2 standard:**

1. **Declarative first sentence** — What the figure shows
2. **Interpretation** — What it means/implies
3. **Citation** — Source if applicable

**Example:**
```latex
\caption{Temporal channel weighting for perceived smoothness. Lightness 
is upweighted relative to chroma based on Sekulovski's measured 10:1 
temporal sensitivity asymmetry, while hue receives a moderate heuristic 
weight pending dedicated calibration \citep{sekulovski2007}.}
```

### Placeholder Discipline

For figures not yet generated, use consistent placeholder format:

```latex
\IfFileExists{figures/filename.pdf}{%
  \includegraphics[width=0.95\linewidth]{figures/filename.pdf}%
}{%
  \fbox{\parbox{0.95\linewidth}{\centering\vspace{0.75em}%
  Figure placeholder: [description of intended figure]\vspace{0.75em}}}%
}
```

---

## 📊 Tables

### Table Format

**Chapter 2 standard:**

1. Use `booktabs` package style (toprule, midrule, bottomrule)
2. Caption explains interpretation, not just content
3. Italics for column descriptions in caption
4. Clear column headers with units where applicable

**Example:**
```latex
\begin{table}[htbp]
\centering
\caption{Color space comparison... \textit{Uniformity} refers to how 
closely Euclidean distances match perceived differences...; \textit{Cost} 
measures computational complexity...}
\label{tab:color-space-comparison}
\begin{tabular}{lcccc}
\toprule
\textbf{Column 1} & \textbf{Column 2} & ... \\
\midrule
Row 1 data & ... \\
\bottomrule
\end{tabular}
\end{table}
```

---

## ✍️ Writing Style

### Mathematical Notation

**Chapter 2 conventions:**

1. **Inline equations** for simple expressions: $\Delta E$, $(L, a, b)$
2. **Display equations** for important relationships:
   ```latex
   \begin{equation}
   ds^2 = d\mathbf{x}^\top g(\mathbf{x})\, d\mathbf{x}
   \label{eq:line-element}
   \end{equation}
   ```
3. **Align environment** for multi-step derivations
4. **Labels** for all numbered equations using semantic names

### List Formatting

**Enumerate** for sequences/steps:
```latex
\begin{enumerate}
    \item First step
    \item Second step
\end{enumerate}
```

**Itemize** for unordered points:
```latex
\begin{itemize}
    \item Point one
    \item Point two
\end{itemize}
```

**Description** for term definitions:
```latex
\begin{description}
    \item[$L$ --- Lightness] explanation
    \item[$a$ --- Green–red] explanation
\end{description}
```

### Transition Quality

**Chapter 2 standard:**  
Every major section transition includes bridging text.

**Pattern:**
1. Summary sentence of previous section
2. Preview of next section's contribution
3. Logical connection explaining why the next topic follows

**Example:**
```latex
Having established both the Riemannian curvature (\S\ref{sec:riemannian-color}) 
and the topological impossibility of perfect uniformity 
(\S\ref{sec:topology-impossibility}), we now face a practical engineering 
question: which color space provides the best computational approximation? 
The answer lies in strategic compromise rather than theoretical perfection.
```

### Emphasis & Formatting

**Italics** (`\emph{}`) for:
- First use of technical terms
- Emphasis on key concepts
- Latin phrases (e.g., *i.e.*, *e.g.*)

**Bold** (`\textbf{}`) for:
- Emphasized list items
- Key takeaway points
- Table/figure highlights

**Small caps** (`\textsc{}`) — not used in Chapter 2, avoid unless needed

**Code/symbols** (`\texttt{}`) — only for actual code or filenames

---

## 🔗 Cross-Referencing

### Reference Format

**Chapter 2 standard:**

- Sections: `\S\ref{sec:label}` or `(\S\ref{sec:label})`
- Equations: `Eq.~\ref{eq:label}` or `Eq.~(\ref{eq:label})`
- Figures: `Figure~\ref{fig:label}` or `Fig.~\ref{fig:label}` in parenthetical
- Tables: `Table~\ref{tab:label}`

**Multiple references:**
```latex
\S\ref{sec:loop-open}--\ref{sec:loop-phased}  % Section range
Eqs.~\ref{eq:first}--\ref{eq:last}           % Equation range
```

---

## 🎓 Academic Integrity Markers

### Caveat Statements

**Chapter 2 established pattern:**  
Clearly mark limitations and open questions.

**Examples:**
```latex
\subsubsection*{Caveat on global structure and suprathreshold perception}

While a Riemannian metric is an effective model of \emph{local} 
discrimination structure, evidence suggests that suprathreshold 
dissimilarity judgements may be nonadditive...
```

```latex
\emph{Important caveat:} This connection should be understood as a 
\emph{design heuristic and analogy} rather than a formally derived theorem.
```

### Empirical Claims

**Pattern for statistical findings:**
1. State the methodology
2. Report specific numbers with citations
3. Interpret with appropriate confidence
4. Flag assumptions

**Example from Chapter 2:**
```latex
The ANOVA revealed a highly significant main effect of direction of change 
($p < 0.01$) \citep[p.~113]{sekulovski2007}. Post hoc tests demonstrated 
that mean threshold values for lightness changes were approximately 
\textbf{10 times smaller} than those for chroma and hue changes 
\citep[p.~113]{sekulovski2007}.
```

---

## 📦 Summary Section Pattern

**Every major chapter should end with:**

1. **Numbered list** of key constraints/findings
2. **Description list** of algorithmic implications
3. **Forward reference** to next chapter

**Chapter 2 template:**
```latex
\section{Summary: [Topic] Determine [Outcome]}
\label{sec:summary-label}

The [topic] established in this section impose X practical constraints 
on [application]:

\begin{enumerate}
    \item \textbf{Constraint 1:} Explanation
    \item \textbf{Constraint 2:} Explanation
\end{enumerate}

\subsection{Implications for [Application]}

These constraints translate directly into algorithmic requirements:

\begin{description}
    \item[Requirement 1:] Explanation
    \item[Requirement 2:] Explanation
\end{description}

With these foundations established, we now turn to [next chapter topic]...
```

---

## 🧪 Quality Checklist (Use Before Finalizing Each Chapter)

### Pre-Sign-Off Checklist

- [ ] **Header block complete** with version, sources, dependencies
- [ ] **All citations include page numbers** for quotes and specific claims
- [ ] **Figures referenced before appearing** with textual justification
- [ ] **Figure captions explain interpretation**, not just content
- [ ] **Transitions between sections** include bridging text
- [ ] **Mathematical notation consistent** with Chapter 2 conventions
- [ ] **Cross-references use correct format** (`\S`, `Fig.`, `Eq.`, `Table`)
- [ ] **Footnotes used appropriately** for methodology and caveats
- [ ] **Summary section follows template** with constraints and implications
- [ ] **Forward reference to next chapter** at end
- [ ] **No orphaned subsections** (single subsection under section)
- [ ] **Maximum 3 levels of heading depth**
- [ ] **Caveats and limitations clearly marked**
- [ ] **All claims either cited or marked as design decisions**
- [ ] **LaTeX builds without errors**
- [ ] **No TODO or FIXME comments remaining**

---

## 📏 Length Guidelines

**Chapter 2 target:** 3,000–3,500 words

**Recommended ranges by chapter type:**

- **Foundational chapters** (like Ch. 2): 3,000–3,500 words
- **Technical implementation chapters**: 2,500–3,500 words
- **Application/results chapters**: 2,000–3,000 words
- **Conclusion chapters**: 1,500–2,500 words

**Balance:**
- Don't sacrifice depth for brevity
- Remove redundancy, not rigor
- Use footnotes for tangential details
- Appendices for extensive derivations

---

## 🔄 Version Control Integration

### Commit Pattern for Chapter Sign-Off

```bash
# 1. Final edits complete
git add latex/sections/XX_chapter_name.tex

# 2. Commit with descriptive message
git commit -m "Chapter X sign-off: [chapter name] locked for conceptual edits"

# 3. Create annotated tag
git tag -a paper-vX.X-chX-signedoff -m "Chapter X ([Title]) signed off - locked for conceptual edits. Only mechanical fixes permitted."

# 4. Snapshot PDF
cp latex/main.pdf "open-agents/output-final/snapshots/paper-vX.X-chX-signedoff_$(date +%Y%m%d).pdf"

# 5. Update this checklist with chapter-specific notes if needed
```

### Tag Naming Convention

Format: `paper-v[major].[minor]-ch[N]-signedoff`

**Examples:**
- `paper-v0.2-ch2-signedoff` ← Chapter 2
- `paper-v0.3-ch3-signedoff` ← Chapter 3
- `paper-v1.0-complete` ← Full paper

---

## 📋 Chapter-Specific Notes

### Chapter 2: Perceptual Foundations

**Signed off:** 30 Dec 2025  
**Tag:** `paper-v0.2-ch2-signedoff`  
**PDF snapshot:** `open-agents/output-final/snapshots/paper-v0.2-ch2-signedoff_20241230.pdf`

**Key structural features:**
- Strong emphasis on citation page numbers (tutor feedback implemented)
- Extensive footnotes for methodological context
- Clear caveats for design heuristics vs. empirical findings
- Transition quality between major sections
- Mathematical rigor balanced with practical interpretation

**Metrics:**
- Word count: ~3,200 words
- Citations: 23 unique sources
- Figures: 3 (2 placeholders, 1 generated)
- Tables: 1
- Equations: 8 numbered
- Sections: 5 major + 1 summary

---

## 🎯 Next Steps for Later Chapters

1. **Before drafting:** Review this checklist
2. **During drafting:** Follow header block, citation, and structure conventions
3. **Before refining:** Check figure integration and transitions
4. **After refining:** Run pre-sign-off checklist
5. **At sign-off:** Execute version control pattern above

---

**Document version:** 1.0  
**Last updated:** 30 Dec 2025  
**Maintained by:** Paper Architect agent  
**Source of truth:** Chapter 2 at commit `paper-v0.2-ch2-signedoff`
