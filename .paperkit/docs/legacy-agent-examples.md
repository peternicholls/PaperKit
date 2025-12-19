# Legacy Agent Examples & Reference Material

This document preserves detailed examples, templates, and troubleshooting guidance from the legacy `open-agents/agents/` definitions. These examples supplement the canonical agent definitions in `.paperkit/core/agents/` and `.paperkit/specialist/agents/`.

---

## LaTeX Assembler Examples

### preamble.tex Template

```tex
\documentclass[12pt,a4paper,twoside]{article}

% Core packages
\usepackage[utf-8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}

% Content packages
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}

% Bibliography
\usepackage[style=authoryear,backend=bibtex]{biblatex}
\addbibresource{references/references.bib}

% Formatting
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{setspace}
\onehalfspacing

% Cross-references
\usepackage{hyperref}
\hypersetup{colorlinks=true,linkcolor=blue}
```

### metadata.tex Template

```tex
\title{Paper Title Here}
\author{Author Name}
\date{\today}

\begin{abstract}
[Abstract text here]
\end{abstract}
```

### settings.tex Template

```tex
% Custom spacing
\setlength{\parindent}{0.5in}
\setlength{\parskip}{0.1in}

% Custom macros for this paper
\newcommand{\colorspace}{color space}
\newcommand{\rgb}{RGB}

% Custom theorem styles (if needed)
\newtheorem{theorem}{Theorem}[section]
\newtheorem{definition}{Definition}[section]
```

### Common LaTeX Issues and Solutions

| Issue | Solution |
|-------|----------|
| `! Undefined control sequence` | Find the undefined command. Check spelling, ensure package is loaded, ask author. |
| Bibliography incomplete / `[?]` refs | Check that bibtex ran and all `\cite{}` keys exist in .bib file. Run full rebuild. |
| Cross-references show as `??` | Normal after first compile. Run pdflatex 2-3 times to resolve all cross-references. |
| Text overlaps / formatting broken | Usually due to oversized content. Check section for overfull boxes. Manual adjustment may be needed. |
| Missing/incorrect title page metadata | Check metadata.tex has correct title, author, date, abstract. |
| Last-minute section changes | No problem. Update section file, rebuild. Takes seconds. |
| PDF is too large | Usually OK for academic papers. If needed, compress with `gs` command (quality trade-off). |

---

## Paper Architect Examples

### Non-Standard Paper Structures

**Experimental papers:**
```
Introduction → Methods → Results → Discussion → Conclusion
```

**Theory papers:**
```
Introduction → Foundations → Main Results → Implications → Conclusion
```

**Survey papers:**
```
Introduction → Topic 1 → Topic 2 → Comparison → Future Directions → Conclusion
```

**Position papers:**
```
Introduction → Problem Statement → Proposed Solution → Counterarguments → Defense → Conclusion
```

### Example Workflow Narrative

**User Provides:**
- Paper goal: "A mathematical specification for a color-based algorithm for X"
- Audience: "Researchers and practitioners in color science"
- Length: "8000-10000 words"
- Key constraint: "Must include worked examples"

**Architect Response:**

1. **Clarify:** Ask if they want historical context, how much theory vs. application, whether appendices should include proof sketches

2. **Propose structure:**
   ```
   I. Introduction (Motivation & Scope)
   II. Mathematical Foundations (Color models, notation)
   III. Core Algorithm (Main contribution)
   IV. Implementation Considerations (Practical aspects)
   V. Validation and Results (Testing and examples)
   VI. Comparison to Prior Work (Context)
   VII. Conclusion and Future Directions
   
   Appendices:
   A. Detailed Mathematical Proofs
   B. Worked Examples
   C. Computational Complexity
   ```

3. **Create outline** with detailed section briefs
4. **Generate LaTeX skeleton** with numbered section files
5. **Update memory** with metadata and structure

---

## Quality Refiner Examples

### Before/After Refinement Samples

**Clarity Improvement:**
```
Original: "The algorithm, based on fundamental principles derived from 
color science research and mathematical models, demonstrates efficiency 
across several metrics related to computational speed and accuracy."

Refined: "The algorithm, grounded in color science principles and 
mathematical models, achieves two key metrics: computational speed and 
accuracy."
```

**Logical Connection Improvement:**
```
Original: "Color spaces vary. The RGB model is commonly used. The LAB 
model is used in perceptual work."

Refined: "Color spaces vary fundamentally in their organization. The RGB 
model, commonly used in digital displays, encodes color as additive 
light mixtures. In contrast, the LAB model, employed in perceptual work, 
separates lightness from chromatic dimensions—a structure better suited 
to human vision."
```

**Academic Tone Improvement:**
```
Original: "Interestingly, we found that the algorithm is really quite 
efficient when processing large datasets."

Refined: "Efficiency gains become pronounced with larger datasets, 
suggesting the algorithm scales well \cite{...}."
```

### Refinement Level Definitions

| Level | Scope | When to Use |
|-------|-------|-------------|
| **Light** | Grammar, typos, specific awkward sentences | Final polish before submission |
| **Moderate** | Restructure paragraphs, strengthen connections, tone consistency | After initial draft review |
| **Deep** | Potentially reorganize, rewrite paragraphs, comprehensive polish | Major revision requested |

---

## Reference Manager Examples

### BibTeX Entry Templates

**Journal Article:**
```bibtex
@article{author_keyword_year,
  author = {Author, A. A. and Author, B. B.},
  title = {Article title in sentence case},
  journal = {Journal Name},
  year = {2020},
  volume = {30},
  number = {3},
  pages = {171--179},
  doi = {10.1234/example.2020.12345}
}
```

**Book:**
```bibtex
@book{author_keyword_year,
  author = {Author, A. A.},
  title = {Book Title in Title Case},
  publisher = {Publisher Name},
  year = {2020},
  address = {City},
  edition = {2nd}
}
```

**Conference Paper:**
```bibtex
@inproceedings{author_conference_2020,
  author = {Author, A. A.},
  title = {Paper title},
  booktitle = {Proceedings of Conference Name},
  year = {2020},
  pages = {100--110},
  publisher = {Publisher}
}
```

**Web Source:**
```bibtex
@misc{author_web_2021,
  author = {Author, A. A.},
  title = {Page or article title},
  year = {2021},
  howpublished = {\url{https://url.example.com}},
  note = {Accessed: 2021-06-15}
}
```

**Thesis:**
```bibtex
@phdthesis{author_thesis_2020,
  author = {Author, A. A.},
  title = {Thesis title},
  school = {University Name},
  year = {2020},
  type = {PhD thesis}
}
```

### Harvard Style Quick Reference

**In-text citations:**
- Single author: (Smith, 2020)
- Two authors: (Smith and Jones, 2020)
- Three authors: (Smith, Jones and Brown, 2020)
- Four+ authors: (Smith et al., 2020)
- With page number: (Smith, 2020, p. 45)
- Multiple sources: (Brown, 2018; Smith, 2020)
- Direct quote: Smith states, "exact quote" (2020, p. 45)

**Special cases:**
- Multiple authors same year: `smith_2020a`, `smith_2020b`
- No author: Use organization name or "Anonymous"
- No publication date: Use `(n.d.)` [no date]
- Secondary citation: "As cited in Smith (2020), the original finding..."

---

## Section Drafter Examples

### LaTeX Semantic Markup

```tex
\subsection{Mathematical Foundations}

In this section, we establish notation and foundational concepts 
\cite{author_year}.

\subsubsection{Color Space Definitions}

A color space is formally defined as \cite{cite_key}:

\begin{equation}
C = (L^*, a^*, b^*)
\end{equation}

where $L^*$ represents lightness, and $a^*$, $b^*$ represent 
chromatic dimensions.

Key insight here: \cite{another_source}.
```

### Word Count Targets by Section Type

| Section Type | Target Words | Notes |
|--------------|--------------|-------|
| Introduction | 2000-2500 | Motivation, scope, contribution preview |
| Methods/Background | 2000-3000 | Technical foundation, prior work |
| Core content sections | 2000-3000 each | Main contribution, analysis |
| Conclusion | 1000-1500 | Summary, future work |

### Citation Frequency Guidelines

- Aim for citations every 3-5 sentences when presenting established facts
- New concepts or ideas from other work: always cite
- Your paper's novel contributions: no citation needed
- Well-known general knowledge: no citation needed
- Methodological approaches from prior work: cite

---

## Research Librarian Examples

### Extraction Commands

```bash
# Convert PDF to searchable text and search with context
pdftotext "source.pdf" - 2>/dev/null | grep -A 10 -B 3 "search_term"

# Multi-term search with context
pdftotext "source.pdf" - | grep -E "term1|term2|term3" -A 5 -B 3

# Page-specific extraction (when page numbers visible)
pdftotext "source.pdf" - | grep -n "key phrase"
```

### Document Search Protocol

- **Timeouts:** Set maximum search iterations; avoid infinite loops
- **Boundaries:** Cap attempts; escalate to manual retrieval when exceeded
- **Terminal downloads:** Prefer `wget`/`curl` for retries and integrity checks
- **Verify content:** Confirm file format/integrity before inventory inclusion

### Search Efficiency Guidelines

- **Pre-filter targets:** Academic databases (arXiv, institutional repos)
- **Log queries:** Record search terms and failures to prevent duplicate effort
- **Cache successes:** Save source locations for rapid re-access
- **Escalate blocks:** Flag unlocatable sources after three attempts
- **Check access:** Confirm open-access or institutional availability before extraction

### Quality Checklist

- [ ] Inventory all sources before extraction
- [ ] Use exact quotes; include page numbers where available
- [ ] Map findings to sections (§02–§12)
- [ ] Maintain Harvard citation format throughout
- [ ] Note gaps explicitly; do not hide missing evidence
- [ ] Add/validate BibTeX entries as you go
- [ ] Update citation map with each new finding
- [ ] Produce handoff document for next agent

---

## Integration Points

### Agent Handoff Patterns

```
Research Librarian → Research Consolidator
  Handoff: COMPREHENSIVE_EVIDENCE_EXTRACTION.md, CITATION_MAP.md
  
Research Consolidator → Section Drafter
  Handoff: [topic]_synthesis.md with citations

Section Drafter → Quality Refiner
  Handoff: [section_name].tex draft

Quality Refiner → Reference Manager
  Handoff: [section_name].tex with [VERIFY] flags

Reference Manager → LaTeX Assembler
  Handoff: Validated references.bib, citation_validation.md
```

### Success Criteria by Agent

| Agent | Success Criteria |
|-------|------------------|
| Paper Architect | Structure reflects goals, sections appropriately sized, LaTeX skeleton ready |
| Research Consolidator | Sources synthesized into narrative, citations complete, gaps flagged |
| Section Drafter | Purpose accomplished, proper citations, correct LaTeX format |
| Quality Refiner | Noticeably clearer, author intent preserved, changes documented |
| Reference Manager | All citations validated, Harvard format consistent, no orphans |
| LaTeX Assembler | PDF compiles cleanly, all references resolve, no warnings |

---

*This document is a reference companion to the canonical agent definitions in `.paperkit/`. For behavioral specifications and activation protocols, see the agent files directly.*
