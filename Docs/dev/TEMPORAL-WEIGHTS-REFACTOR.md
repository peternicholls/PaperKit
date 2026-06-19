# Temporal Weights Figure Refactoring

## Overview
Refactored the "Channel weighting for temporal smoothness" diagram for both Python (matplotlib) and TikZ versions to improve code clarity, visual consistency, and maintainability.

## Improvements to Python Version (`scripts/create-figures.py`)

### Code Structure
- **Consolidated gradients**: Replaced three separate axes (L, C, H) with a unified, data-driven approach using a single swatch axis
- **Configuration-driven design**: Swatches defined in a single `swatches_config` list with (x_position, label, caption, colors) tuples
- **Cleaner rectangle generation**: Direct Rectangle patch creation in a loop instead of manual axis setup per swatch

### Visual Refinements
- Better gradient quality using 100-sample color arrays
- Improved label positioning and sizing hierarchy
- Cleaner arrow styling with consistent line widths
- Refined gridspec layout with better aspect ratios

### Code Metrics
- **Lines reduced**: From ~70 to ~55 lines in the main function
- **Readability**: Removed redundant axis transformations; all positioning now in absolute coordinates
- **Maintainability**: Single source of truth for swatch parameters

## Improvements to TikZ Version (`latex/figures/temporal-weights.tex`)

### Structure
- Added clear section comments (`===== TOP SECTION =====`, `===== BOTTOM SECTION =====`)
- Unified gradient colors with improved HSV parameters
- Better spacing and alignment of all elements

### Visual Enhancements
- Improved bar colors and edge styling
- Refined caption positioning and baseline alignment
- Better visual hierarchy with font weight and sizing
- Grid and axis lines now have explicit width specifications

### Typography
- Consistent use of `\bfseries` for emphasis
- Improved text alignment in node annotations
- Better baseline adjustment for multi-line labels

## Key Synergies

Both versions now:
- Use identical color schemes: red (#e63946), blue (#457b9d), teal (#2a9d8f)
- Follow the same spatial layout: swatches at top, bar chart at bottom
- Apply consistent typography and labeling hierarchies
- Emphasize source citations and validation status

## Usage

**Generate all figures (including temporal-weights-justified.pdf):**
```bash
cd latex/figures
source ../../.venv/bin/activate
python3 ../../scripts/create-figures.py
```

**Build TikZ version standalone:**
```bash
xelatex -interaction=nonstopmode temporal-weights.tex
```

Both approaches now provide professional, publication-ready output suitable for academic papers.
