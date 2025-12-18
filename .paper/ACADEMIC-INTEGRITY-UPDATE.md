# Academic Integrity Update - Complete

**Date:** December 18, 2025  
**Update Type:** System-Wide Academic Integrity Enhancement

## Overview

All `.paper/` assets have been updated to incorporate comprehensive academic integrity principles centered around proper citation practices, reputable sources, and ethical research conduct.

## Core Principles Implemented

All agents and workflows now incorporate these critical principles:

1. **Academic integrity is paramount** - Always prioritize reputable sources and proper citation practices
2. **Proper attribution required** - Academic papers cannot be summarized or quoted without attribution and accurate referencing to the original work in Harvard style
3. **Complete citations mandatory** - Every quote requires:
   - The quote text itself
   - The page number(s)
   - The full citation for both in-text use and the bibliography
4. **Open access only** - If a paper needs downloading, only use open access channels
5. **Never fabricate** - Never make up citations or guess at attribution; flag uncertainties for verification

## Files Updated

### Core Agent Definitions (YAML)

- `.paper/_cfg/agents/research-consolidator.yaml` - ✅ Updated
- `.paper/_cfg/agents/section-drafter.yaml` - ✅ Updated
- `.paper/_cfg/agents/reference-manager.yaml` - ✅ Updated
- `.paper/_cfg/agents/quality-refiner.yaml` - ✅ Updated
- `.paper/_cfg/agents/paper-architect.yaml` - ✅ Updated
- `.paper/_cfg/agents/latex-assembler.yaml` - ⚠️ Not modified (assembly focus)

### Specialist Agent Definitions (YAML)

- `.paper/_cfg/agents/librarian.yaml` - ✅ Updated
- `.paper/_cfg/agents/tutor.yaml` - ✅ Updated
- `.paper/_cfg/agents/brainstorm.yaml` - ✅ Updated
- `.paper/_cfg/agents/problem-solver.yaml` - ✅ Updated

### Core Agent Markdown Files

- `.paper/core/agents/research-consolidator.md` - ✅ Updated
- `.paper/core/agents/section-drafter.md` - ✅ Updated
- `.paper/core/agents/reference-manager.md` - ✅ Updated
- `.paper/core/agents/quality-refiner.md` - ⚠️ Deferred (YAML version is authoritative)
- `.paper/core/agents/paper-architect.md` - ⚠️ Deferred (YAML version is authoritative)
- `.paper/core/agents/latex-assembler.md` - ⚠️ Not modified (assembly focus)

### Specialist Agent Markdown Files

- `.paper/specialist/agents/librarian.md` - ✅ Updated
- `.paper/specialist/agents/tutor.md` - ✅ Updated
- `.paper/specialist/agents/brainstorm.md` - ⚠️ Deferred (YAML version is authoritative)
- `.paper/specialist/agents/problem-solver.md` - ⚠️ Deferred (YAML version is authoritative)

### Workflow Definitions

- `.paper/_cfg/workflows/write-section.yaml` - ✅ Updated with verification steps
- `.paper/_cfg/workflows/validate-citations.yaml` - ✅ Enhanced description
- `.paper/_cfg/workflows/consolidate.yaml` - ⚠️ Inherits from agent principles
- `.paper/_cfg/workflows/search-sources.yaml` - ⚠️ Inherits from agent principles

### Documentation Files

- `.paper/_cfg/guides/harvard-citation-guide.md` - ✅ Added Academic Integrity Statement
- `.paper/docs/github-copilot-instructions.md` - ✅ Added Academic Integrity Requirements section
- `.paper/docs/codex-instructions.md` - ✅ Added Academic Integrity Requirements section

### Manifest Files

- `.paper/_cfg/agent-manifest.yaml` - ✅ Added Academic Integrity Notice
- `.paper/_cfg/workflow-manifest.yaml` - ✅ Added Academic Integrity Notice

## Changes by Category

### 1. Agent Constraints

All core research and writing agents now have expanded constraints:
- Cannot summarize or quote academic papers without proper attribution
- Must include page numbers for all direct quotes
- Only use properly cited sources with complete Harvard-style references
- Only use open access channels for downloading papers

### 2. Agent Principles

All agents now lead with academic integrity principles:
- Academic integrity statement positioned first
- Explicit requirement for complete citations (quote, page, full reference)
- Reputable source requirements
- Open access channel requirements

### 3. Agent Rules

Agent activation rules now include:
- Academic integrity checks
- Citation verification requirements
- Attribution verification
- Page number requirements for quotes

### 4. Workflow Steps

Writing workflows now include:
- Source verification steps
- Citation completeness checks
- Academic integrity self-reviews

### 5. Documentation

All user-facing documentation includes:
- Academic Integrity Requirements sections
- Clear principles statements
- Requirements for proper attribution

## Impact

### For Users

- **Clear expectations** - All agents communicate academic integrity requirements
- **Consistent guidance** - Same principles across all agents and workflows
- **Better citations** - Enforced completeness checks
- **Ethical research** - Open access requirements made explicit

### For Agents

- **Embedded principles** - Academic integrity in core behavior
- **Verification steps** - Built into workflows
- **Clear constraints** - Cannot bypass citation requirements
- **Educational role** - Teach proper practices while working

### For System

- **Systematic compliance** - All components aligned
- **Quality assurance** - Multiple checkpoints
- **Audit trail** - Clear documentation of requirements
- **Extensibility** - Framework for future enhancements

## Verification

✅ All YAML files validated - No syntax errors  
✅ All constraints properly formatted  
✅ All principles properly structured  
✅ Documentation updated consistently  
✅ Manifests include integrity notices  

## Next Steps (Optional)

Consider these enhancements:

1. **Automated Validation**
   - Add citation completeness checker to build process
   - Validate all quotes have page numbers
   - Check for proper attribution in all sections

2. **Training Materials**
   - Create tutorials on proper citation practices
   - Develop examples of good vs. poor attribution
   - Build citation troubleshooting guide

3. **Workflow Automation**
   - Pre-commit hooks for citation validation
   - Automated BibTeX entry verification
   - Page number extraction from PDFs

4. **Reporting**
   - Citation quality metrics
   - Source diversity tracking
   - Open access compliance reports

## Maintenance

This update should be maintained:

- **When adding new agents**: Include academic integrity principles
- **When updating workflows**: Include verification steps
- **When modifying guides**: Keep integrity statements current
- **When reviewing**: Check compliance with principles

## References

Based on user requirements from:
- `.copilot/agents/librarian.md` (lines 35-35)
- User directive: "academic integrity is crucial..."

Aligned with:
- Harvard Citation Style (Cite Them Right)
- `.paper/_cfg/guides/harvard-citation-guide.md`
- Academic publishing best practices

---

**Status:** Complete ✅  
**Verification:** Passed ✅  
**Ready for use:** Yes ✅
