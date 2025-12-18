# Handover: Reference Manager Integration

Agent: Harper (📚 Reference Manager)
Date: 2025-12-18
Upstream: Ellis (📖 Research Librarian)

## Inputs
- Deliverable: open-agents/planning/20251218-group-tutor-reviews/tasks-artifacts/foundational-references.md
- Target BibTeX database: latex/references/references.bib
- Relevant LaTeX sections:
  - latex/sections/02_perceptual_foundations.tex
  - latex/sections/03_journey_construction.tex
  - latex/sections/04_perceptual_constraints.tex
  - latex/sections/08_gamut_management.tex

## Keys and Entries
- macadam_visual_1942 (article): DOI 10.1364/JOSA.32.000247
- wyszecki_color_1982 (book): 2nd ed., Wiley-Interscience, ISBN 0471021067

The BibTeX blocks are included verbatim in foundational-references.md.

## Tasks
1. Insert BibTeX entries
   - Add the two entries to latex/references/references.bib.
   - Check for duplicates (key and metadata). If a prior entry exists, harmonize under a single canonical key.
2. Validate citations
   - Run workflow: extract-citations → validate-citations → citation-completeness → format-bibliography.
   - Confirm fields: author(s), year, title, venue/publisher, volume/issue/pages (MacAdam), DOI (MacAdam), edition/address/isbn (W&S).
3. Add inline citations at recommended locations
   - 02_perceptual_foundations: introduce JND/discrimination ellipses → cite macadam_visual_1942.
   - 04_perceptual_constraints: threshold-aware steps/uniformity → cite macadam_visual_1942 and, where definitions are invoked, wyszecki_color_1982.
   - 03_journey_construction: colorimetric transforms/observer data → cite wyszecki_color_1982.
   - 08_gamut_management: perceptual error metrics and tolerance framing → cite macadam_visual_1942 when discussing sensitivity contours.
   - Use the project’s citation command (e.g., \parencite or \cite) consistent with preamble; if uncertain, prefer \parencite{key} and align with existing usage.
4. Rebuild and check
   - Compile the LaTeX document and ensure both citations appear and bibliography entries render correctly.

## Acceptance Checklist
- [ ] Both BibTeX entries present (or deduplicated) in latex/references/references.bib
- [ ] No validation errors from citation workflows
- [ ] Citations added in the four sections listed above
- [ ] PDF builds without citation/bibliography warnings

## Notes
- MacAdam (1942) supports JND thresholds and anisotropic discrimination ellipses in CIE 1931 (x,y), critical for threshold-aware stepping.
- Wyszecki & Stiles (1982) is the canonical reference for colorimetric definitions, observer functions, difference formulae, and psychophysical methods.
