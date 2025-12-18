### 007-references-citationAudit

**Agent:** 📚 Reference Manager (Harper)  
**Phase:** 2 (Core)  
**Estimated Time:** 45 minutes  
**Dependencies:** 001-librarian-foundationalReferences  
**Output Location:** `latex/references/references.bib`, `open-agents/output-refined/references/citation_audit.md`

#### Task Brief

Audit and fix citation issues identified by tutors:

1. **CSS Color 4 citation** — Verify specificity (Candidate Recommendation Snapshot)
2. **Moosbauer & Poole (2025)** — Evaluate relevance or remove
3. **Levien (2021)** — Label as blog post/technical analysis
4. **Add foundational references** — MacAdam (1942), Wyszecki & Stiles (1982)

#### Specific Actions

**Citation 1: CSS Color 4 (W3C)**
- [ ] Verify citation is for "Candidate Recommendation Snapshot" specifically
- [ ] Add publication date and snapshot version
- [ ] Note that CSS Color 4 is still evolving

**Citation 2: Moosbauer & Poole (2025)**
- [ ] Locate in paper (§12.3 Future Directions?)
- [ ] Evaluate: Is symmetry-constrained search relevant to color harmony?
- [ ] **If tenuous:** Remove citation and find more relevant symmetry reference, OR
- [ ] **If defensible:** Add 1-2 sentence explanation connecting it to paper

**Citation 3: Levien (2021)**
- [ ] Verify BibTeX entry type is `@misc` or `@online`, not `@article`
- [ ] Add note field: `Independent technical analysis; not peer-reviewed`
- [ ] Ensure in-text citations reflect informal status

**Citation 4: Add foundational references**
- [ ] Add MacAdam (1942) BibTeX entry (from 001-librarian task)
- [ ] Add Wyszecki & Stiles (1982) BibTeX entry
- [ ] Verify keys are consistent with paper citations

#### Output: Citation Audit Report

```markdown
## Citation Audit Report

### Changes Made

1. **CSS Color 4**
   - Updated to reference Candidate Recommendation Snapshot [date]
   - Added note about evolving specification status

2. **Moosbauer & Poole (2025)**
   - [Removed / Clarified relevance with additional sentence]

3. **Levien (2021)**
   - Reclassified as @online entry
   - Added non-peer-reviewed note

4. **New References Added**
   - macadam_visual_1942
   - wyszecki_color_1982

### Validation Status
- Total citations in paper: [N]
- Total BibTeX entries: [N]
- All citations resolved: [Yes/No]
- Missing entries: [List]
```

#### Success Criteria

- [ ] All citation issues from tutors addressed
- [ ] BibTeX entries formatted correctly (Harvard style)
- [ ] New foundational references added
- [ ] Citation audit report created
- [ ] LaTeX compiles with valid bibliography
