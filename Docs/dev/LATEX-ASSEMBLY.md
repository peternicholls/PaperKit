# LaTeX Document Assembly in PaperKit

This document explains how PaperKit assembles the final LaTeX document from modular components and compiles it to PDF.

> **Quick Reference**: For a one-page overview, see [latex-assembly-quickref.txt](latex-assembly-quickref.txt)

## Table of Contents

1. [Overview](#overview)
2. [File Structure](#file-structure)
3. [Assembly Process](#assembly-process)
4. [Build Process](#build-process)
5. [Commands](#commands)
6. [Customization](#customization)

---

## Overview

PaperKit uses a **modular LaTeX architecture** where the final document is assembled from multiple small, focused files. This approach provides:

- **Clean version control**: Small section files create readable diffs
- **Parallel editing**: Multiple authors can work on different sections simultaneously
- **Easier maintenance**: Changes are localized to specific files
- **Progressive refinement**: Each section can be drafted and refined independently

The final PDF is generated through a **3-pass compilation process** that resolves cross-references, integrates bibliography citations, and produces a complete document with table of contents, references, and all formatting.

---

## File Structure

### Core LaTeX Files

The document structure is defined in `latex/` directory:

```
latex/
├── main.tex              # Main document - integrates all components
├── preamble.tex          # LaTeX packages, document class, formatting
├── metadata.tex          # Title, author, abstract, keywords
├── settings.tex          # Fine-tuning, custom commands, styling
├── sections/             # Individual section files
│   ├── 01_introduction.tex
│   ├── 02_perceptual_foundations.tex
│   ├── 03_journey_construction.tex
│   └── ...
├── appendices/           # Appendix files
│   ├── A_presets.tex
│   ├── B_notation.tex
│   └── ...
└── references/
    └── references.bib    # Bibliography database
```

### File Responsibilities

#### 1. **main.tex** - Document Integration

The main document file (`latex/main.tex`) is the entry point that:

- Inputs the preamble, settings, and metadata
- Defines the document structure
- Inputs all section files in order
- Generates front matter (title, abstract, table of contents)
- Inputs appendices
- Prints the bibliography

**Structure:**
```tex
\input{preamble}          % Packages and formatting
\input{settings}          % Custom settings
\input{metadata}          % Title, author, abstract

\begin{document}

\maketitle                % Title page
\begin{abstract}          % Abstract section
  \abstracttext
\end{abstract}

\tableofcontents          % Table of contents

% Main chapters
\chapter{Introduction and Scope}
\input{sections/01_introduction}

\chapter{Perceptual Color Foundations}
\input{sections/02_perceptual_foundations}

% ... more chapters ...

% Appendices
\appendix
\chapter{Preset Reference}
\input{appendices/A_presets}

% Bibliography
\printbibliography[title={References}]

\end{document}
```

#### 2. **preamble.tex** - LaTeX Configuration

The preamble (`latex/preamble.tex`) configures the entire document:

- **Document class**: `\documentclass[12pt,a4paper,twoside,openany]{report}`
- **Essential packages**: 
  - Character encoding and fonts (`fontenc`, `lmodern`, `babel`)
  - Mathematics (`amsmath`, `amssymb`, `amsthm`, `mathtools`, `physics`)
  - Graphics (`graphicx`, `xcolor`, `tikz`)
  - Page layout (`geometry`, `setspace`)
  - Bibliography (`biblatex` with Harvard/author-year style)
  - Cross-references (`hyperref`, `cleveref`)
  - Headers/footers (`fancyhdr`)
  - Tables and lists (`booktabs`, `array`, `longtable`, `enumitem`)
  - Code listings (`listings`)
  
- **Custom environments**: Design decision boxes, theorem environments
- **Custom macros**: Mathematical notations, operators, abbreviations

**Key Configuration:**
```tex
% Page geometry
\usepackage[left=1in, right=1in, top=1in, bottom=1in]{geometry}

% Bibliography (Harvard style)
\usepackage[backend=bibtex,style=authoryear,natbib=true]{biblatex}
\addbibresource{references/references.bib}

% Hyperlinks
\usepackage{hyperref}
\hypersetup{colorlinks=true, linkcolor=blue, citecolor=blue}

% Custom environments
\newtcolorbox{designdecision}[1][]{
  colback=blue!5!white,
  colframe=blue!75!black,
  title={Design Decision: #1}
}
```

#### 3. **metadata.tex** - Document Metadata

Defines the paper's identifying information (`latex/metadata.tex`):

```tex
\title{Color Journey Engine: A Perceptually-Uniform Palette Generation Specification}
\author{Peter Nicholls}
\date{\today}

\newcommand{\abstracttext}{
  This paper specifies the Color Journey Engine...
}

\newcommand{\keywords}{
  color palette generation, OKLab, perceptual uniformity, 
  Bézier curves, gamut mapping, deterministic algorithms
}
```

#### 4. **settings.tex** - Custom Settings

Fine-tuning and customizations (`latex/settings.tex`):

- Title formatting (`titlesec`)
- Custom colors for highlighting
- Figure and table configuration
- Caption formatting
- Custom environments (key insights, notes)
- PDF metadata

#### 5. **Section Files** - Content

Each section file (`latex/sections/*.tex`) contains:

- Section content with LaTeX markup
- Subsections and subsubsections
- Citations using `\cite{key}` or `\citep{key}`
- Cross-references using `\ref{}` or `\cref{}`
- Figures, tables, equations
- Custom environments (design decisions, examples)

**Example section structure:**
```tex
% ==============================================================================
% Section 1: Introduction and Scope
% ==============================================================================
% Primary Source: 10_scope_use_cases_presets.md
% Target Length: 500-1,000 words
% ==============================================================================

\section{Motivation}
\label{sec:motivation}

Every domain that works with color requires coherent color palettes...

\subsection*{Audience and Purpose}

This document serves as an internal technical reference...

\section{Scope Definition}
\label{sec:scope}

The Color Journey Engine produces \textbf{ordered sequences}...
```

#### 6. **references.bib** - Bibliography Database

BibTeX database file (`latex/references/references.bib`) containing all citations:

```bibtex
@article{oklab2020,
  author = {Ottosson, Björn},
  title = {A perceptual color space for image processing},
  year = {2020},
  journal = {Blog post}
}

@book{fairchild2013,
  author = {Fairchild, Mark D.},
  title = {Color Appearance Models},
  year = {2013},
  publisher = {Wiley}
}
```

---

## Assembly Process

### How Files Are Combined

The LaTeX assembly process follows this sequence:

```
┌─────────────────────────────────────────────────────────────┐
│                      main.tex (Entry Point)                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Input Configuration Files                           │
│   \input{preamble}   → Load all packages & formatting       │
│   \input{settings}   → Load custom settings                 │
│   \input{metadata}   → Load title, author, abstract         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Begin Document                                       │
│   \begin{document}                                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Generate Front Matter                               │
│   \maketitle         → Title page                           │
│   \abstracttext      → Abstract                             │
│   \keywords          → Keywords                             │
│   \tableofcontents   → Table of contents (from sections)    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Input Main Content Sections                         │
│   \chapter{Introduction and Scope}                          │
│   \input{sections/01_introduction}                          │
│   \chapter{Perceptual Color Foundations}                    │
│   \input{sections/02_perceptual_foundations}                │
│   ... (all 12 chapters)                                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Input Appendices                                    │
│   \appendix                                                  │
│   \chapter{Preset Reference}                                │
│   \input{appendices/A_presets}                              │
│   ... (all appendices)                                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 6: Generate Bibliography                               │
│   \printbibliography[title={References}]                    │
│   → Reads references.bib                                    │
│   → Includes only cited works                               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 7: End Document                                         │
│   \end{document}                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Points

1. **\input{} command**: Includes external files inline (no extra formatting)
2. **\chapter{} wrapper**: Each section file is wrapped in a chapter declaration in main.tex
3. **Labels and references**: Cross-references like `\ref{sec:motivation}` work across files
4. **Bibliography**: Only cited works from references.bib are included in the final document

---

## Build Process

The LaTeX document requires a **3-pass compilation** to properly resolve all references and citations.

### Why 3 Passes?

1. **First Pass**: Processes document structure, creates `.aux` files with label definitions
2. **BibTeX**: Reads citations from `.aux`, extracts entries from `.bib`, creates `.bbl`
3. **Second Pass**: Incorporates bibliography, updates references
4. **Third Pass**: Resolves any remaining cross-references

### Build Script

The build process is automated in `.paperkit/tools/build-latex.sh`:

```bash
#!/bin/bash
# Simplified view of the build process

cd latex/

# Pass 1: Initial compilation
pdflatex -interaction=nonstopmode main.tex

# BibTeX: Generate bibliography
bibtex main

# Pass 2: Incorporate bibliography
pdflatex -interaction=nonstopmode main.tex

# Pass 3: Resolve cross-references
pdflatex -interaction=nonstopmode main.tex

# Copy to output directory
cp main.pdf ../open-agents/output-final/pdf/main.pdf
```

### Build Artifacts

The compilation creates several intermediate files:

```
latex/
├── main.pdf           # Final PDF output
├── main.aux           # Auxiliary file (labels, references)
├── main.toc           # Table of contents data
├── main.bbl           # Formatted bibliography
├── main.blg           # BibTeX log
├── main.log           # Compilation log
├── main.out           # Hyperref bookmarks
└── main.run.xml       # Biblatex run data
```

**Output Location**: The final PDF is copied to `open-agents/output-final/pdf/main.pdf`

### Build Flow Diagram

```
┌──────────────┐
│  main.tex    │
│  preamble    │
│  metadata    │
│  settings    │
│  sections/*  │
│  appendices/*│
└──────┬───────┘
       │
       ↓ pdflatex (Pass 1)
┌──────────────┐
│  main.aux    │ ← Contains citation keys
│  main.log    │
└──────┬───────┘
       │
       ↓ bibtex
┌──────────────┐       ┌─────────────────┐
│  main.bbl    │ ←───  │ references.bib  │
│  main.blg    │       └─────────────────┘
└──────┬───────┘
       │
       ↓ pdflatex (Pass 2)
┌──────────────┐
│  main.pdf    │ ← Bibliography included
│  main.aux    │ ← Updated with biblio refs
│  main.toc    │ ← Table of contents
└──────┬───────┘
       │
       ↓ pdflatex (Pass 3)
┌──────────────┐
│  main.pdf    │ ← Final document with all refs resolved
└──────┬───────┘
       │
       ↓ copy
┌──────────────────────────────┐
│ open-agents/output-final/    │
│   pdf/main.pdf               │
└──────────────────────────────┘
```

---

## Commands

PaperKit provides CLI commands for working with LaTeX documents via the `./paperkit` script.

### Build the PDF

Compile the complete document:

```bash
./paperkit latex build
```

**What it does:**
1. Validates required files exist
2. Runs 3-pass compilation (pdflatex → bibtex → pdflatex → pdflatex)
3. Copies PDF to output directory
4. Generates build report
5. Shows summary (file size, page count)

**Output:**
- PDF: `open-agents/output-final/pdf/main.pdf`
- Build log: `latex/build.log`
- Build report: `open-agents/output-final/build_report.md`

### Lint LaTeX

Check for syntax errors before building:

```bash
./paperkit latex lint
```

**What it checks:**
- Unmatched braces `{}`
- Unmatched math delimiters `$`
- Unclosed environments (`\begin{...}` without `\end{...}`)
- Missing citation keys (references not in .bib file)
- Missing section files

**Example output:**
```
LaTeX Syntax Validation
======================

Checking for unmatched braces...
Checking for unmatched math delimiters...
Checking for unclosed environments...
Checking for citation references...
Checking for missing section files...

======================
Validation Summary
======================
Errors: 0
Warnings: 2

✓ Validation complete. Safe to compile.
```

### Open the PDF

View the compiled PDF:

```bash
./paperkit latex open
```

**What it does:**
- Opens `latex/main.pdf` (if it exists) using system default PDF viewer
- On macOS: Uses `open`
- On Linux: Uses `xdg-open`
- On Windows: Uses `start`

If the PDF doesn't exist, suggests running `./paperkit latex build` first.

### Help

Get help on LaTeX commands:

```bash
./paperkit latex --help
```

---

## Customization

### Adding a New Section

1. **Create the section file**: `latex/sections/13_new_section.tex`
   
   ```tex
   % ==============================================================================
   % Section 13: New Section
   % ==============================================================================
   
   \section{First Topic}
   \label{sec:new-topic}
   
   Content goes here...
   ```

2. **Add to main.tex**: Edit `latex/main.tex` to include the new section
   
   ```tex
   \chapter{New Section Title}
   \input{sections/13_new_section}
   ```

3. **Rebuild**: Run `./paperkit latex build`

### Adding Citations

1. **Add to bibliography**: Edit `latex/references/references.bib`
   
   ```bibtex
   @article{newpaper2024,
     author = {Smith, John},
     title = {A New Approach},
     journal = {Journal Name},
     year = {2024},
     volume = {10},
     pages = {1--20}
   }
   ```

2. **Cite in text**: Use in any section file
   
   ```tex
   According to \citet{newpaper2024}, the approach works well.
   The results are promising \citep{newpaper2024}.
   ```

3. **Rebuild**: The citation will appear in the bibliography automatically

### Changing Document Style

Edit `latex/preamble.tex` or `latex/settings.tex`:

- **Page margins**: Modify `\usepackage[...]{geometry}`
- **Font size**: Change `\documentclass[12pt,...]`
- **Line spacing**: Use `\singlespacing`, `\onehalfspacing`, or `\doublespacing`
- **Citation style**: Modify `\usepackage[style=...]{biblatex}`
- **Colors**: Define in `settings.tex` with `\definecolor{name}{RGB}{r,g,b}`

### Custom Commands

Add project-specific macros to `latex/settings.tex`:

```tex
% Custom abbreviation
\newcommand{\oklab}{\textsc{OkLab}}

% Custom notation
\newcommand{\colorspace}[1]{\mathcal{#1}}

% Usage in sections
The \oklab{} color space is defined as \colorspace{C}...
```

---

## Validation and Quality Checks

### Pre-build Validation

Always run lint before building:

```bash
./paperkit latex lint && ./paperkit latex build
```

This catches common errors before the lengthy compilation process.

### Build Logs

If compilation fails, check:

1. **Terminal output**: Shows last 20 lines of errors
2. **Full log**: `latex/build.log` contains complete compilation output
3. **BibTeX log**: `latex/main.blg` shows bibliography issues

### Common Issues

**"Undefined control sequence"**
- You used a command without loading the required package
- Check preamble.tex for the appropriate `\usepackage{}`

**"Citation undefined"**
- Citation key not found in references.bib
- Run lint to identify missing citations

**"Missing number, treated as zero"**
- Often caused by unescaped special characters (%, &, #, _)
- Escape with backslash: `\%`, `\&`, `\#`, `\_`

**"Overfull hbox"** (warnings)
- Line is too wide for margins
- Usually acceptable; check PDF to see if it looks okay
- Fix by rewording or adding hyphenation hints

---

## Summary

The PaperKit LaTeX assembly process:

1. **Modular Architecture**: Separate files for configuration, metadata, and content
2. **\input{} Assembly**: Main.tex pulls everything together
3. **3-Pass Compilation**: Resolves references and citations completely
4. **Automated Build**: Single command handles entire process
5. **Quality Checks**: Linting catches errors before compilation
6. **Clean Output**: Final PDF placed in designated output directory

This design enables collaborative editing, version control, and progressive refinement while maintaining a professional, publication-ready final document.

**Quick Reference:**

```bash
# Check syntax
./paperkit latex lint

# Build PDF
./paperkit latex build

# View result
./paperkit latex open

# All-in-one
./paperkit latex lint && ./paperkit latex build && ./paperkit latex open
```

For more information:
- LaTeX build script: `.paperkit/tools/build-latex.sh`
- Lint script: `.paperkit/tools/lint-latex.sh`
- CLI implementation: `paperkit` (lines 286-353)
- Commands reference: `Docs/COMMANDS.md`
