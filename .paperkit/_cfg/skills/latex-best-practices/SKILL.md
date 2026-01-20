---
name: latex-best-practices
description: Best practices for writing LaTeX documents including structure, formatting, and common patterns. Use when creating or editing LaTeX files, troubleshooting compilation errors, or improving document organization.
metadata:
  author: core-team
  version: "1.0.0"
  category: formatting
---

# LaTeX Best Practices: Document Composition Guide

You are a LaTeX expert helping authors create well-structured, maintainable LaTeX documents. This skill provides guidance on document organization, common patterns, and error prevention.

## When to Use

Use this skill when:
- Creating or structuring LaTeX documents
- Troubleshooting compilation errors
- Improving document organization
- Writing mathematical notation
- Managing bibliographies and cross-references

## Document Structure

### Modular Organization

Split large documents into separate files:

```latex
% main.tex
\documentclass{article}
\input{preamble}           % Package imports and settings
\input{metadata}           % Title, author, date
\begin{document}
\maketitle
\input{sections/01_introduction}
\input{sections/02_background}
\input{sections/03_methodology}
\bibliography{references}
\end{document}
```

### Preamble Organization

Group package imports by function:

```latex
% preamble.tex

% === Document Class Settings ===
\usepackage[margin=1in]{geometry}

% === Typography ===
\usepackage[T1]{fontenc}
\usepackage{microtype}

% === Mathematics ===
\usepackage{amsmath,amssymb,amsthm}

% === Graphics and Figures ===
\usepackage{graphicx}
\usepackage{tikz}

% === Tables ===
\usepackage{booktabs}
\usepackage{tabularx}

% === References ===
\usepackage[style=authoryear]{biblatex}
\usepackage{hyperref}
\usepackage{cleveref}
```

## Common Patterns

### Figures

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/diagram.pdf}
  \caption{Description of the figure. Note the period at the end.}
  \label{fig:diagram}
\end{figure}
```

Reference with: `\Cref{fig:diagram}` or `Figure~\ref{fig:diagram}`

### Tables

```latex
\begin{table}[htbp]
  \centering
  \caption{Comparison of methods. Caption goes above tables.}
  \label{tab:comparison}
  \begin{tabular}{lcc}
    \toprule
    Method & Accuracy & Speed \\
    \midrule
    Baseline & 0.75 & 100ms \\
    Proposed & 0.92 & 85ms \\
    \bottomrule
  \end{tabular}
\end{table}
```

Use `booktabs` for professional tables - never use vertical lines.

### Equations

**Numbered equation:**
```latex
\begin{equation}
  E = mc^2
  \label{eq:einstein}
\end{equation}
```

**Unnumbered equation:**
```latex
\begin{equation*}
  E = mc^2
\end{equation*}
```

**Aligned equations:**
```latex
\begin{align}
  f(x) &= ax^2 + bx + c \\
  g(x) &= \frac{df}{dx} = 2ax + b
\end{align}
```

### Lists

**Itemized:**
```latex
\begin{itemize}
  \item First item
  \item Second item
\end{itemize}
```

**Enumerated:**
```latex
\begin{enumerate}
  \item First step
  \item Second step
\end{enumerate}
```

**Description:**
```latex
\begin{description}
  \item[Term] Definition of the term
  \item[Another] Its definition
\end{description}
```

### Cross-References

Use `cleveref` for automatic formatting:

```latex
\usepackage{cleveref}

% In text:
\Cref{fig:diagram}     % "Figure 1"
\cref{fig:diagram}     % "figure 1"
\Cref{eq:einstein}     % "Equation 1"
\Cref{sec:intro}       % "Section 1"
```

### Citations

**With biblatex:**
```latex
\textcite{Smith_2020} argues that...    % Smith (2020) argues that...
\parencite{Smith_2020}                  % (Smith, 2020)
\parencite[p.~45]{Smith_2020}           % (Smith, 2020, p. 45)
```

**With natbib:**
```latex
\citet{Smith_2020}                      % Smith (2020)
\citep{Smith_2020}                      % (Smith, 2020)
\citep[p.~45]{Smith_2020}               % (Smith, 2020, p. 45)
```

## Spacing and Typography

### Non-Breaking Spaces

Use `~` to prevent line breaks:

```latex
Figure~\ref{fig:diagram}
Section~\ref{sec:intro}
Dr.~Smith
100~km
```

### Dashes

- Hyphen: `-` for compound words (well-known)
- En-dash: `--` for ranges (pages 1--10, 2020--2023)
- Em-dash: `---` for punctuation---like this

### Quotation Marks

```latex
``Double quotes''
`Single quotes'
```

### Ellipsis

Use `\ldots` not `...`:
```latex
The data shows that\ldots
```

## Error Prevention

### Common Mistakes

**1. Missing braces:**
```latex
% Wrong:
\textbf{bold text    % Missing closing brace

% Right:
\textbf{bold text}
```

**2. Unescaped special characters:**
```latex
% Wrong:
50% of users          % % starts a comment

% Right:
50\% of users
```

Special characters requiring escape: `# $ % & _ { } ~ ^`

**3. Missing label before caption:**
```latex
% Wrong (label after caption may not work):
\caption{Description}
\label{fig:example}

% Right:
\caption{Description}\label{fig:example}
% Or:
\label{fig:example}
\caption{Description}
```

**4. Hardcoded formatting:**
```latex
% Wrong:
\textbf{Theorem 1.} Let $x$ be...

% Right:
\begin{theorem}
  Let $x$ be...
\end{theorem}
```

### Compilation Issues

**Undefined control sequence:**
- Check package is loaded
- Check spelling of command
- Check command is used in correct context

**Missing $ inserted:**
- Math mode characters outside math: `_`, `^`, `\alpha`
- Use `$...$` or `\(...\)` for inline math

**Overfull hbox:**
- Text extends past margins
- Try `\sloppy` locally or rephrase
- Check URLs with `\url{}` command

**Missing \item:**
- Forgot `\item` in list environment
- Content outside `\item` in list

## Mathematical Notation

### Common Symbols

```latex
% Greek letters
\alpha, \beta, \gamma, \Gamma

% Operators
\sum, \prod, \int, \partial

% Relations
\leq, \geq, \neq, \approx, \equiv

% Sets
\in, \subset, \cup, \cap, \emptyset

% Arrows
\rightarrow, \leftarrow, \Rightarrow, \iff
```

### Formatting

```latex
% Vectors (bold)
\mathbf{v}, \vec{v}

% Matrices
\begin{pmatrix} a & b \\ c & d \end{pmatrix}
\begin{bmatrix} a & b \\ c & d \end{bmatrix}

% Text in math
$x = 5 \text{ where } x > 0$

% Functions
\sin, \cos, \log, \exp
\operatorname{argmax}  % Custom operators
```

## File Organization

```
project/
├── main.tex              # Main document
├── preamble.tex          # Package imports
├── metadata.tex          # Title, author
├── settings.tex          # Custom commands
├── sections/
│   ├── 01_introduction.tex
│   ├── 02_background.tex
│   └── ...
├── figures/
│   ├── diagram.pdf
│   └── chart.pdf
├── tables/               # Optional: external tables
├── appendices/
│   └── A_supplementary.tex
└── references/
    └── references.bib
```

## Custom Commands

Define shortcuts for repeated patterns:

```latex
% In preamble or settings.tex:

% Abbreviations
\newcommand{\eg}{e.g.,\xspace}
\newcommand{\ie}{i.e.,\xspace}
\newcommand{\cf}{cf.\xspace}

% Math shortcuts
\newcommand{\R}{\mathbb{R}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\E}{\mathbb{E}}
\newcommand{\norm}[1]{\left\lVert #1 \right\rVert}

% Color space (example)
\newcommand{\oklab}{\textsc{Oklab}\xspace}
```

## Build Process

### Basic compilation

```bash
pdflatex main.tex
bibtex main          # or biber main for biblatex
pdflatex main.tex
pdflatex main.tex    # Run twice for references
```

### With latexmk (recommended)

```bash
latexmk -pdf main.tex
```

### Cleaning auxiliary files

```bash
latexmk -c           # Clean auxiliary files
latexmk -C           # Clean all generated files
```

## Process

When helping with LaTeX:

1. **Identify the issue**: Compilation error, structure, formatting
2. **Check basics**: Package imports, braces, special characters
3. **Apply best practices**: Modular structure, semantic commands
4. **Verify compilation**: Ensure document builds cleanly
5. **Optimize**: Remove redundancy, improve readability

## Output Format

When providing LaTeX guidance:
1. Show the corrected/improved code
2. Explain what was changed and why
3. Note any dependencies (packages) required
4. Highlight common pitfalls to avoid
