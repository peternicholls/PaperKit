# PaperKit Implementation Guide
## Quick Start for Citation Management & Workflow Integration

**Version:** 1.0.0  
**Last Updated:** December 2025

---

## Overview

This guide shows how to use the improved PaperKit workflow system with enhanced citation management. The system now includes:

1. **Comprehensive Harvard Citation Guide** - Complete reference for agents
2. **Enhanced Workflow Manifest** - 25 workflows covering full paper writing lifecycle
3. **Detailed Workflow Definitions** - Step-by-step process specifications
4. **Improved Agent Definitions** - Clear roles, capabilities, and interaction patterns

---

## Quick Start

### 1. File Structure

Ensure your PaperKit directory has this structure:

```
.paper/
├── _cfg/
│   ├── guides/
│   │   └── harvard-citation-guide.md          ← NEW: Comprehensive style guide
│   ├── workflows/
│   │   ├── core/
│   │   │   ├── validate-citations.yaml        ← ENHANCED
│   │   │   ├── format-bibliography.yaml
│   │   │   ├── write-section.yaml
│   │   │   └── ...
│   │   └── specialist/
│   │       └── ...
│   ├── agents/
│   │   ├── reference-manager.yaml             ← ENHANCED
│   │   ├── academic-writer.yaml
│   │   └── ...
│   ├── schemas/
│   │   ├── workflow-schema.json
│   │   └── agent-schema.json
│   └── workflow-manifest.yaml                 ← ENHANCED
```

### 2. Using the Harvard Citation Guide

The guide is located at `.paper/_cfg/guides/harvard-citation-guide.md` and includes:

- **Complete formatting rules** for all source types
- **In-text citation examples** for every scenario
- **Reference list templates** with real examples
- **Common errors** and how to avoid them
- **Agent implementation guidelines** for automated checking

**Key Sections:**
- Core Principles (p.1-2)
- In-Text Citations (p.3-5)
- Reference List Formats (p.6-12)
- Special Cases (p.13-14)
- Agent Guidelines (p.18-19)

### 3. Running Citation Validation

#### Basic Validation

```bash
paperkit run validate-citations
```

This will:
1. Scan all `.tex` files for citations
2. Check against your `references.bib`
3. Validate formatting and completeness
4. Generate a detailed report

#### Section-Specific Validation

```bash
paperkit run validate-citations --input texFiles=['latex/sections/intro.tex']
```

#### Strict Mode (Warnings as Errors)

```bash
paperkit run validate-citations --strict
```

#### Auto-Fix Simple Issues

```bash
paperkit run validate-citations --auto-fix
```

### 4. Workflow Integration

#### Complete Paper Writing Flow

```bash
# 1. Research Phase
paperkit run consolidate
paperkit run literature-review

# 2. Planning Phase
paperkit run outline
paperkit run skeleton
paperkit run section-plan --section introduction

# 3. Drafting Phase
paperkit run write-section --section introduction
paperkit run write-section --section methodology
# ... repeat for all sections

# 4. Refinement Phase
paperkit run refine-section --section introduction
paperkit run coherence-check
paperkit run style-consistency

# 5. Reference Management
paperkit run validate-citations
paperkit run citation-completeness
paperkit run format-bibliography

# 6. Final Assembly
paperkit run build
paperkit run final-review
```

#### Quick Quality Check

```bash
# Run all validation workflows
paperkit run validate-citations
paperkit run coherence-check
paperkit run style-consistency
```

---

## Working with the Reference Manager (Harper)

### Agent Capabilities

Harper can:
- ✅ Extract citations from LaTeX files
- ✅ Validate citations against BibTeX database
- ✅ Check format compliance with Harvard style
- ✅ Identify missing or incomplete entries
- ✅ Generate formatted bibliographies
- ✅ Provide citation guidance and education
- ✅ Auto-fix simple formatting issues

### Example Interactions

#### 1. Validating Your Work

**You:** "Check all my citations"

**Harper:** "I'll validate your citations systematically. Scanning files..."

**Harper:** 
```
📊 Validation Complete

Statistics:
- Total citations: 47
- Unique citations: 38
- BibTeX entries: 42
- Match rate: 97.4%

✓ 37 citations valid and complete
⚠️ 1 missing citation
⚠️ 3 incomplete entries
ℹ️ 4 unused entries in bibliography

Critical Issues:
1. Missing: Smith2023 (used in intro.tex:45)
2. Incomplete: Jones2022 (missing journal volume)
3. Incomplete: Chen2021 (missing page numbers)
4. Incomplete: Davis2020 (missing publisher location)

See detailed report for recommendations.
```

#### 2. Getting Format Help

**You:** "How do I cite a website with no date?"

**Harper:**
```
For websites without publication dates, use (n.d.) meaning "no date":

In-text citation:
(Title or Organization, n.d.)

Reference list:
Organization Name (n.d.) Title. Available at: URL (Accessed: Date).

Example:
Climate Change Facts (n.d.) Available at: 
https://www.climate.org/facts (Accessed: 15 December 2025).

Important: You MUST include the access date for all online sources.
```

#### 3. Fixing Errors

**Harper identifies an error:**
```
❌ Format Error Detected

Entry: Johnson2021
Field: author
Current: "Johnson, A"
Required: "Johnson, A.A."

Issue: Initials must have periods in Harvard style.
Fix: author = {Johnson, A.A.},

This is auto-fixable. Would you like me to correct it?
```

**You:** "Yes, please fix it"

**Harper:** "✓ Fixed author format for Johnson2021. Updated references.bib."

---

## Best Practices

### Citation Management

1. **Validate Early and Often**
   - Run validation after writing each section
   - Fix issues immediately rather than accumulating them
   - Use `--strict` mode before final submission

2. **Maintain Your BibTeX Database**
   - Add complete information from the start
   - Use consistent citation key format (Author_Year)
   - Keep entries organized by category
   - Remove unused entries periodically

3. **Follow Harvard Style Consistently**
   - Reference the guide for any uncertainty
   - Use sentence case for titles
   - Include access dates for all online sources
   - Always include page numbers for quotes

4. **Leverage Auto-Fix**
   - Let Harper fix simple formatting issues
   - Review auto-fixes before committing
   - Learn from corrections to avoid future errors

### Workflow Optimization

1. **Use Workflow Chains**
   - Follow the defined dependency order
   - Don't skip prerequisite steps
   - Complete validation before building

2. **Parallel Work When Possible**
   - Multiple sections can be drafted simultaneously
   - Quality checks can run in parallel
   - But always finish validation before final build

3. **Regular Quality Checks**
   - Run coherence-check after major changes
   - Validate citations after adding new sources
   - Style-check before sharing drafts

---

## Troubleshooting

### Common Issues

#### "Missing citation: XYZ"

**Cause:** Citation used in text but no BibTeX entry exists  
**Fix:** Add complete entry to references.bib

```bibtex
@article{XYZ_2023,
  author = {Surname, I.I.},
  title = {Article title},
  journal = {Journal Name},
  year = {2023},
  volume = {10},
  number = {2},
  pages = {123--145},
  doi = {10.1234/example}
}
```

#### "Incomplete entry: missing required fields"

**Cause:** BibTeX entry lacks required information  
**Fix:** Add missing fields based on entry type

Required fields by type:
- **Article:** author, year, title, journal, volume
- **Book:** author, year, title, publisher, address
- **Website:** author/title, year/n.d., title, url, accessed

#### "Format error: incorrect author format"

**Cause:** Author names not in Harvard format  
**Fix:** Use format "Surname, I.I."

Wrong: `author = {John Smith}`  
Right: `author = {Smith, J.}`  
Best: `author = {Smith, J.J.}`

#### "Access date missing for online source"

**Cause:** Online source without access date  
**Fix:** Add access date to BibTeX entry

```bibtex
@misc{WebSource_2023,
  author = {Organization},
  title = {Page title},
  year = {2023},
  url = {https://example.com},
  note = {Accessed: 15 December 2025}
}
```

---

## Advanced Features

### Custom Validation Rules

Create `.paper/_cfg/validation/custom-rules.yaml`:

```yaml
rules:
  - name: require-doi-for-journals
    description: All journal articles should have DOI
    severity: warning
    applies_to: [article]
    check: doi field present
    
  - name: recent-sources-only
    description: Prefer sources from last 5 years
    severity: info
    check: year >= current_year - 5
```

### Integration with CI/CD

Add to your `.github/workflows/paper-validation.yml`:

```yaml
name: Paper Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate Citations
        run: |
          paperkit run validate-citations --strict
      - name: Check Coherence
        run: |
          paperkit run coherence-check
      - name: Style Check
        run: |
          paperkit run style-consistency
```

### Editor Integration

For VS Code, add to `.vscode/settings.json`:

```json
{
  "paperkit.validation.onSave": true,
  "paperkit.validation.strict": false,
  "paperkit.citation.style": "harvard-cite-them-right",
  "paperkit.citation.autofix": true
}
```

---

## Migration from Old System

### Step 1: Update Manifests

Replace your old `workflow-manifest.yaml` with the enhanced version:

```bash
cp enhanced-workflow-manifest.yaml .paper/_cfg/workflow-manifest.yaml
```

### Step 2: Add Citation Guide

```bash
mkdir -p .paper/_cfg/guides
cp harvard-citation-guide.md .paper/_cfg/guides/
```

### Step 3: Update Workflow Definitions

```bash
cp enhanced-validate-citations.yaml .paper/_cfg/workflows/core/
```

### Step 4: Update Agent Definitions

```bash
cp enhanced-reference-manager.yaml .paper/_cfg/agents/
```

### Step 5: Validate Configuration

```bash
python3 open-agents/tools/validate-workflow-schema.py
```

### Step 6: Test Workflows

```bash
# Test validation workflow
paperkit run validate-citations --dry-run

# Test full chain
paperkit test workflow-chain full-paper-workflow
```

---

## Resources

### Documentation

- **Harvard Citation Guide:** `.paper/_cfg/guides/harvard-citation-guide.md`
- **Workflow Manifest:** `.paper/_cfg/workflow-manifest.yaml`
- **Agent Definitions:** `.paper/_cfg/agents/`
- **Workflow Definitions:** `.paper/_cfg/workflows/`

### External References

- **Cite Them Right Online:** https://www.citethemrightonline.com
- **Open University Guide:** https://university.open.ac.uk/library/referencing
- **UCD Harvard Guide:** https://libguides.ucd.ie/harvardstyle

### Support

- **Report Issues:** https://github.com/paperkit/paperkit/issues
- **Documentation:** https://paperkit.dev/docs
- **Community:** https://paperkit.dev/community

---

## Quick Reference Card

### Most Common Commands

```bash
# Validate all citations
paperkit run validate-citations

# Check specific section
paperkit run validate-citations --section intro

# Auto-fix formatting
paperkit run validate-citations --auto-fix

# Generate bibliography
paperkit run format-bibliography

# Full quality check
paperkit run final-review

# Build PDF
paperkit run build
```

### Citation Quick Reference

**In-text:**
- Single author: (Smith, 2020)
- Two authors: (Smith and Jones, 2020)
- Three authors: (Smith, Jones and Brown, 2020)
- Four+ authors: (Smith et al., 2020)
- With page: (Smith, 2020, p. 45)
- Multiple: (Smith, 2020; Jones, 2021)

**Reference list:**
- Alphabetical by author surname
- Hanging indent
- Sentence case for titles
- Round brackets for dates
- Access dates for online sources

---

## Next Steps

1. ✅ Review the Harvard Citation Guide
2. ✅ Update your workflow manifests
3. ✅ Run validation on existing work
4. ✅ Fix any identified issues
5. ✅ Integrate into your writing process
6. ✅ Set up CI/CD validation (optional)

**Questions?** Consult the documentation or ask Harper!