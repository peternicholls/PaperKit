### 017-assembler-finalBuild

**Agent:** 🔧 LaTeX Assembler (Taylor)  
**Phase:** 3 (Final)  
**Estimated Time:** 30 minutes  
**Dependencies:** All previous tasks  
**Output Location:** `open-agents/output-final/pdf/main.pdf`, build report

#### Task Brief

Perform final assembly and validation after all improvements are complete.

#### Pre-Assembly Checklist

- [ ] All section files present and updated
- [ ] All figures created and placed
- [ ] Bibliography updated with new references
- [ ] Table of contents will generate correctly
- [ ] Cross-references are valid

#### Build Process

1. **Clean previous build artifacts:**
   ```bash
   cd latex/
   rm -f *.aux *.bbl *.blg *.log *.toc *.out
   ```

2. **Run full compilation:**
   ```bash
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex
   ```

3. **Check for errors and warnings:**
   - Errors: Must fix before proceeding
   - Warnings: Document but continue if non-critical

4. **Validate output:**
   - [ ] PDF generated
   - [ ] All pages present
   - [ ] Table of contents correct
   - [ ] Figures render
   - [ ] Bibliography complete
   - [ ] No undefined references (??)
   - [ ] No missing citations

#### Build Report

```markdown
## Final Build Report

### Build Status: [SUCCESS / FAILED]

### Document Statistics
- Total pages: [N]
- Total words: [N] (estimated)
- Figures: [N]
- Tables: [N]
- Bibliography entries: [N]
- Citations in text: [N]

### Changes Since Last Build
- New section: §1.6 (Limitations)
- New subsection: §2.2.1 (OKLab Recency)
- New figures: 4
- Updated references: [N]
- Spelling/notation standardization: Complete

### Validation Results
- [ ] All citations resolved
- [ ] All cross-references valid
- [ ] All figures render
- [ ] No LaTeX errors
- [ ] Warnings: [list if any]

### Quality Assessment
[Brief assessment of document quality]

### Remaining Issues (if any)
[List any non-critical issues for future attention]
```

#### Success Criteria

- [ ] PDF compiles without errors
- [ ] All tutor-identified issues addressed
- [ ] Build report complete
- [ ] Document ready for distribution
