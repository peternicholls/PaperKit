# Agent Instruction Code Duplication Report

**Generated**: 2026-01-20 16:49:05
**Purpose**: Baseline measurement for Phase 2 Skills Framework (SC-007)

---

## Summary

| Metric | Value |
|--------|-------|
| Total Agent Files | 11 |
| Total Words | 7,520 |
| Estimated Duplication | 22.7% |
| Similar File Pairs | 9 |
| Common Sections | 5 |
| Skill Candidates | 14 |

## File Analysis

| File | Words |
|------|-------|
| reference-manager.md | 1,115 |
| paper-architect.md | 832 |
| research-consolidator.md | 796 |
| section-drafter.md | 795 |
| quality-refiner.md | 732 |
| librarian.md | 689 |
| latex-assembler.md | 595 |
| tutor.md | 589 |
| problem-solver.md | 489 |
| brainstorm.md | 472 |
| orchestrator.md | 416 |

## File Similarity

Files with >30% word overlap (Jaccard similarity):

| File 1 | File 2 | Similarity |
|--------|--------|------------|
| research-consolidator.md | section-drafter.md | 36.8% |
| research-consolidator.md | librarian.md | 34.6% |
| quality-refiner.md | section-drafter.md | 34.2% |
| problem-solver.md | tutor.md | 32.6% |
| section-drafter.md | librarian.md | 32.0% |
| quality-refiner.md | research-consolidator.md | 32.0% |
| librarian.md | tutor.md | 31.9% |
| brainstorm.md | problem-solver.md | 31.1% |
| reference-manager.md | research-consolidator.md | 30.1% |

## Common Section Names

Section names appearing in multiple agents:

| Section | # Files | Files |
|---------|---------|-------|
| preamble | 10 | latex-assembler.md, paper-architect.md, quality-refiner.md, +7 more |
| purpose | 10 | latex-assembler.md, paper-architect.md, quality-refiner.md, +7 more |
| when to use | 10 | latex-assembler.md, paper-architect.md, quality-refiner.md, +7 more |
| core behaviors | 10 | latex-assembler.md, paper-architect.md, quality-refiner.md, +7 more |
| output format | 9 | latex-assembler.md, paper-architect.md, quality-refiner.md, +6 more |

## Recommended Skill Extractions

Patterns that could be extracted into reusable skills:

### 1. purpose
- **Type**: section
- **Occurrences**: 10
- **Recommendation**: Extract 'purpose' into a reusable skill

### 2. when to use
- **Type**: section
- **Occurrences**: 10
- **Recommendation**: Extract 'when to use' into a reusable skill

### 3. core behaviors
- **Type**: section
- **Occurrences**: 10
- **Recommendation**: Extract 'core behaviors' into a reusable skill

### 4. output format
- **Type**: section
- **Occurrences**: 9
- **Recommendation**: Extract 'output format' into a reusable skill

### 5. agent" --- you must fully
- **Type**: phrase
- **Occurrences**: 10
- **Recommendation**: Extract common phrase pattern into skill

### 6. --- you must fully embody
- **Type**: phrase
- **Occurrences**: 10
- **Recommendation**: Extract common phrase pattern into skill

### 7. you must fully embody this
- **Type**: phrase
- **Occurrences**: 10
- **Recommendation**: Extract common phrase pattern into skill

### 8. must fully embody this agent's
- **Type**: phrase
- **Occurrences**: 10
- **Recommendation**: Extract common phrase pattern into skill

### 9. fully embody this agent's persona
- **Type**: phrase
- **Occurrences**: 10
- **Recommendation**: Extract common phrase pattern into skill

### 10. embody this agent's persona and
- **Type**: phrase
- **Occurrences**: 10
- **Recommendation**: Extract common phrase pattern into skill

## Next Steps for Phase 2

1. Review common sections for skill extraction candidates
2. Create skill definitions in `.paperkit/_cfg/skills/`
3. Refactor agent instructions to reference skills
4. Re-measure duplication after skill implementation

---

*This baseline report will be compared against Phase 2 results to measure improvement.*