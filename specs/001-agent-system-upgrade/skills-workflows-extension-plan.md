# Skills & Workflows Extension Plan

**Version**: 1.0.0
**Created**: 2026-01-20
**Status**: Proposed

---

## Executive Summary

This plan extends PaperKit's Agent Skills and Compositional Workflows to provide comprehensive coverage for all 11 agents across the complete academic paper writing lifecycle.

**Current State:**
- 4 Agent Skills (humanizer, academic-writing, harvard-citations, latex-best-practices)
- 20 Compositional Workflows (12 complete, 8 need schema updates)

**Proposed Additions:**
- 12 new Agent Skills (covering all agents)
- 8 new Compositional Workflows (filling gaps)
- 8 workflow schema updates (standardization)

---

## Part 1: New Agent Skills

### Priority 1: Core Agent Skills (High Impact)

These skills directly support the main paper writing workflow.

#### 1.1 `research-synthesis` (for Research Consolidator)

```yaml
name: research-synthesis
description: Transform scattered research materials into structured, synthesized documents. Use when consolidating notes, PDFs, and sources into coherent research summaries.
```

**Instructions cover:**
- Evidence extraction from PDFs
- Research gap identification
- Source quality evaluation
- Synthesis patterns (thematic, chronological, methodological)
- Citation tracking during synthesis
- Mapping evidence to paper sections

#### 1.2 `paper-structure` (for Paper Architect)

```yaml
name: paper-structure
description: Design effective academic paper structures with logical flow and hierarchy. Use when creating outlines, section plans, or LaTeX skeletons.
```

**Instructions cover:**
- Academic paper conventions by field
- Outline generation patterns
- Section dependency mapping
- Argument flow design
- LaTeX skeleton creation
- Structure validation checklist

#### 1.3 `section-writing` (for Section Drafter)

```yaml
name: section-writing
description: Write academic prose from outlines and research. Use when drafting paper sections with proper tone, citations, and structure.
```

**Instructions cover:**
- Academic writing patterns by section type
- Introduction writing (hooks, context, thesis)
- Literature review construction
- Methods section conventions
- Results presentation
- Discussion and conclusion patterns
- Citation integration techniques
- Handling uncertainty and limitations

#### 1.4 `text-refinement` (for Quality Refiner)

```yaml
name: text-refinement
description: Improve academic writing through systematic refinement. Use when polishing drafts for clarity, flow, coherence, and academic tone.
```

**Instructions cover:**
- Clarity improvement techniques
- Flow and transition enhancement
- Redundancy elimination
- Passive vs active voice
- Sentence variety
- Paragraph structure
- Academic tone calibration
- Consistency checking

#### 1.5 `bibtex-management` (for Reference Manager)

```yaml
name: bibtex-management
description: Parse, validate, and manage BibTeX entries and files. Use when working with bibliography databases, fixing entries, or extracting citations.
```

**Instructions cover:**
- BibTeX entry types and required fields
- Common BibTeX errors and fixes
- Entry deduplication
- Field normalization
- Key generation conventions
- Cross-reference handling
- Special character escaping

#### 1.6 `latex-troubleshooting` (for LaTeX Assembler)

```yaml
name: latex-troubleshooting
description: Diagnose and fix LaTeX compilation errors. Use when builds fail or produce unexpected output.
```

**Instructions cover:**
- Common LaTeX error patterns
- Package conflicts
- Missing file handling
- Bibliography errors (bibtex/biber)
- Float placement issues
- Font and encoding problems
- Cross-reference resolution
- Error message interpretation

---

### Priority 2: Specialist Agent Skills (Medium Impact)

These skills support specialized tasks and improve agent effectiveness.

#### 2.1 `brainstorming-techniques` (for Brainstorm Coach)

```yaml
name: brainstorming-techniques
description: Structured brainstorming techniques for academic ideation. Use when generating research questions, paper angles, or exploring topics.
```

**Instructions cover:**
- SCAMPER technique
- Mind mapping patterns
- Six Thinking Hats
- Concept clustering
- Assumption challenging
- Question laddering
- Idea categorization

#### 2.2 `problem-analysis` (for Problem Solver)

```yaml
name: problem-analysis
description: Systematic problem analysis and root cause identification. Use when stuck on research problems, writing blocks, or technical issues.
```

**Instructions cover:**
- Root cause analysis (5 Whys, Fishbone)
- Problem decomposition
- Assumption identification
- Solution evaluation criteria
- Risk assessment
- Decision matrices
- Iterative refinement

#### 2.3 `constructive-feedback` (for Review Tutor)

```yaml
name: constructive-feedback
description: Provide constructive academic feedback on drafts. Use when reviewing papers to identify strengths, weaknesses, and improvements.
```

**Instructions cover:**
- Feedback sandwich technique
- Argument assessment rubric
- Evidence quality evaluation
- Writing quality criteria
- Balancing critique and encouragement
- Actionable suggestion formulation
- Academic standards reference

#### 2.4 `source-evaluation` (for Research Librarian)

```yaml
name: source-evaluation
description: Evaluate research source quality and relevance. Use when assessing whether sources are credible, current, and appropriate for academic work.
```

**Instructions cover:**
- CRAAP test (Currency, Relevance, Authority, Accuracy, Purpose)
- Peer review indicators
- Publisher reputation
- Citation impact
- Primary vs secondary sources
- Source triangulation
- Bias identification

---

### Priority 3: Cross-Cutting Skills (Universal)

These skills benefit multiple agents.

#### 3.1 `evidence-extraction` (Universal)

```yaml
name: evidence-extraction
description: Extract and organize evidence from academic sources. Use when pulling quotes, data, and findings from PDFs and papers.
```

**Instructions cover:**
- Quote extraction with page numbers
- Paraphrasing vs direct quotation
- Evidence categorization
- Section mapping
- Context preservation
- Source tracking
- Evidence quality annotation

#### 3.2 `academic-integrity` (Universal)

```yaml
name: academic-integrity
description: Ensure academic integrity in all outputs. Use to verify proper attribution, avoid plagiarism, and maintain ethical standards.
```

**Instructions cover:**
- Attribution requirements
- Plagiarism types and avoidance
- Self-citation ethics
- Data integrity
- Fabrication vs honest uncertainty
- Common integrity violations
- Verification checklist

---

## Part 2: New Compositional Workflows

### 2.1 `full-paper-draft` (End-to-End)

```yaml
name: full-paper-draft
type: composite
description: Draft an entire paper from outline to complete first draft
agents: [paper-architect, research-consolidator, section-drafter, reference-manager]
steps:
  - finalize-outline (paper-architect)
  - gather-all-research (research-consolidator)
  - draft-introduction (section-drafter, skill: section-writing)
  - draft-body-sections (section-drafter, skill: section-writing) [loop]
  - draft-conclusion (section-drafter, skill: section-writing)
  - integrate-citations (reference-manager)
```

### 2.2 `research-to-synthesis` (Research Pipeline)

```yaml
name: research-to-synthesis
type: composite
description: Complete research pipeline from topic to synthesized notes
agents: [librarian, research-consolidator]
steps:
  - define-research-questions (librarian)
  - search-sources (librarian, skill: source-evaluation)
  - extract-evidence (research-consolidator, skill: evidence-extraction)
  - synthesize-findings (research-consolidator, skill: research-synthesis)
  - identify-gaps (research-consolidator)
```

### 2.3 `citation-audit` (Reference Validation)

```yaml
name: citation-audit
type: composite
description: Complete audit of all citations in a document
agents: [reference-manager]
steps:
  - extract-all-citations (reference-manager)
  - validate-each-citation (reference-manager, skill: harvard-citations) [loop]
  - check-bibtex-completeness (reference-manager, skill: bibtex-management)
  - generate-audit-report (reference-manager)
```

### 2.4 `iterative-refinement` (Quality Loop)

```yaml
name: iterative-refinement
type: composite
description: Multi-pass refinement with tutor feedback
agents: [quality-refiner, tutor]
steps:
  - initial-refinement (quality-refiner, skill: text-refinement)
  - tutor-review (tutor, skill: constructive-feedback)
  - address-feedback (quality-refiner)
  - final-polish (quality-refiner, skill: humanizer)
```

### 2.5 `latex-full-build` (Complete Build)

```yaml
name: latex-full-build
type: composite
description: Full LaTeX compilation with pre-checks and error handling
agents: [latex-assembler, reference-manager]
steps:
  - validate-structure (latex-assembler)
  - check-citations (reference-manager)
  - lint-latex (latex-assembler, skill: latex-best-practices)
  - compile-document (latex-assembler, tool: build-latex)
  - verify-output (latex-assembler, skill: latex-troubleshooting)
```

### 2.6 `problem-resolution` (Problem Solving)

```yaml
name: problem-resolution
type: composite
description: Systematic problem analysis with solution implementation
agents: [problem-solver, brainstorm]
steps:
  - define-problem (problem-solver, skill: problem-analysis)
  - brainstorm-solutions (brainstorm, skill: brainstorming-techniques)
  - evaluate-options (problem-solver)
  - implement-solution (problem-solver)
```

### 2.7 `paper-review` (Complete Review)

```yaml
name: paper-review
type: composite
description: Comprehensive paper review before submission
agents: [tutor, quality-refiner, reference-manager]
steps:
  - assess-structure (tutor)
  - assess-arguments (tutor, skill: constructive-feedback)
  - assess-writing (quality-refiner)
  - assess-citations (reference-manager)
  - generate-review-report (tutor)
```

### 2.8 `section-complete` (Section Pipeline)

```yaml
name: section-complete
type: composite
description: Complete a section from research to polished draft
agents: [research-consolidator, section-drafter, quality-refiner, reference-manager]
steps:
  - gather-section-research (research-consolidator, skill: research-synthesis)
  - draft-section (section-drafter, skill: section-writing)
  - refine-section (quality-refiner, skill: text-refinement)
  - add-citations (reference-manager, skill: harvard-citations)
  - humanize-text (quality-refiner, skill: humanizer)
```

---

## Part 3: Workflow Schema Updates

The following 8 workflows need schema standardization:

| Workflow | Changes Needed |
|----------|----------------|
| `outline.yaml` | Add `type`, `version`, update steps to new format |
| `refine-section.yaml` | Add `type`, `version`, update steps |
| `review-draft.yaml` | Add `type`, `version`, update steps |
| `search-sources.yaml` | Add `type`, `version`, update steps |
| `consolidate.yaml` | Add `type`, `version`, update steps |
| `generate-ideas.yaml` | Add `type`, `version`, update steps |
| `analyze-problem.yaml` | Add `type`, `version`, update steps |
| `build.yaml` | Review and align with compile-latex |

---

## Part 4: Skill-Agent Mapping

| Agent | Primary Skills | Secondary Skills |
|-------|---------------|------------------|
| **Research Consolidator** | research-synthesis, evidence-extraction | academic-integrity |
| **Paper Architect** | paper-structure | academic-writing |
| **Section Drafter** | section-writing, academic-writing | harvard-citations |
| **Quality Refiner** | text-refinement, humanizer | academic-writing |
| **Reference Manager** | harvard-citations, bibtex-management | academic-integrity |
| **LaTeX Assembler** | latex-best-practices, latex-troubleshooting | — |
| **Brainstorm Coach** | brainstorming-techniques | problem-analysis |
| **Problem Solver** | problem-analysis | — |
| **Review Tutor** | constructive-feedback | academic-writing |
| **Research Librarian** | source-evaluation, evidence-extraction | academic-integrity |
| **Orchestrator** | — (routes to other agents) | — |

---

## Part 5: Implementation Priority

### Phase 1: Foundation (Immediate)

1. Create 4 core skills:
   - `research-synthesis`
   - `section-writing`
   - `text-refinement`
   - `bibtex-management`

2. Update 4 workflows to new schema:
   - `outline.yaml`
   - `refine-section.yaml`
   - `consolidate.yaml`
   - `search-sources.yaml`

### Phase 2: Complete Core (Week 2)

3. Create remaining core skills:
   - `paper-structure`
   - `latex-troubleshooting`

4. Create cross-cutting skills:
   - `evidence-extraction`
   - `academic-integrity`

5. Update remaining workflows:
   - `review-draft.yaml`
   - `generate-ideas.yaml`
   - `analyze-problem.yaml`
   - `build.yaml`

### Phase 3: Specialist & Pipelines (Week 3)

6. Create specialist skills:
   - `brainstorming-techniques`
   - `problem-analysis`
   - `constructive-feedback`
   - `source-evaluation`

7. Create composite workflows:
   - `full-paper-draft`
   - `research-to-synthesis`
   - `citation-audit`
   - `iterative-refinement`
   - `latex-full-build`
   - `problem-resolution`
   - `paper-review`
   - `section-complete`

---

## Part 6: Success Metrics

| Metric | Target |
|--------|--------|
| Total Agent Skills | 16 (from 4) |
| Skills per agent | ≥1 primary skill |
| Workflow schema compliance | 100% |
| Skill registry load time | <50ms |
| All validations passing | ✓ |

---

## Part 7: Task Breakdown

### New Tasks to Add to tasks.md

```markdown
## Phase 2c: Skills & Workflows Extension

### New Agent Skills

- [ ] T080 [P] Create `research-synthesis/SKILL.md`
- [ ] T081 [P] Create `section-writing/SKILL.md`
- [ ] T082 [P] Create `text-refinement/SKILL.md`
- [ ] T083 [P] Create `bibtex-management/SKILL.md`
- [ ] T084 [P] Create `paper-structure/SKILL.md`
- [ ] T085 [P] Create `latex-troubleshooting/SKILL.md`
- [ ] T086 [P] Create `evidence-extraction/SKILL.md`
- [ ] T087 [P] Create `academic-integrity/SKILL.md`
- [ ] T088 [P] Create `brainstorming-techniques/SKILL.md`
- [ ] T089 [P] Create `problem-analysis/SKILL.md`
- [ ] T090 [P] Create `constructive-feedback/SKILL.md`
- [ ] T091 [P] Create `source-evaluation/SKILL.md`

### Workflow Schema Updates

- [ ] T092 Update `outline.yaml` to new schema
- [ ] T093 Update `refine-section.yaml` to new schema
- [ ] T094 Update `consolidate.yaml` to new schema
- [ ] T095 Update `search-sources.yaml` to new schema
- [ ] T096 Update `review-draft.yaml` to new schema
- [ ] T097 Update `generate-ideas.yaml` to new schema
- [ ] T098 Update `analyze-problem.yaml` to new schema
- [ ] T099 Update `build.yaml` to new schema

### New Composite Workflows

- [ ] T100 Create `full-paper-draft.yaml` workflow
- [ ] T101 Create `research-to-synthesis.yaml` workflow
- [ ] T102 Create `citation-audit.yaml` workflow
- [ ] T103 Create `iterative-refinement.yaml` workflow
- [ ] T104 Create `latex-full-build.yaml` workflow
- [ ] T105 Create `problem-resolution.yaml` workflow
- [ ] T106 Create `paper-review.yaml` workflow
- [ ] T107 Create `section-complete.yaml` workflow

### Integration

- [ ] T108 Update agent YAML files with `suggestedSkills`
- [ ] T109 Update agent-manifest.yaml with skill references
- [ ] T110 Update documentation with new skills/workflows
- [ ] T111 Run full validation suite
```

---

## Appendix: Skill Template

```markdown
---
name: skill-name
description: Brief description AND when to use it. Include trigger keywords.
metadata:
  author: core-team
  version: "1.0.0"
---

# Skill Display Name

## Your Task

When given [context], do:

1. First step
2. Second step
3. Final output

## Core Guidelines

### Section One

- Guideline
- Guideline
- Guideline

### Section Two

...

## Patterns & Examples

### Pattern: Name

**Use when**: Context
**Steps**: 1, 2, 3
**Example**: ...

### Pattern: Name

...

## Common Mistakes to Avoid

1. Mistake description
2. Mistake description

## Quick Reference

| Scenario | Do This |
|----------|---------|
| ... | ... |
```
