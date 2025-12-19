# Specification: Onboarding, Examples, and Developer Docs

**Spec ID:** 008-onboarding-docs  
**Date:** 2025-12-13  
**Status:** Draft  
**Priority:** Medium  
**Category:** Developer Experience

---

## Problem Statement

Copilot/Codex instruction files describe activation steps but are somewhat redundant and could be more actionable with examples. Documentation is fragmented across multiple files, and there's no clear onboarding path for new users or contributors.

### Current State

- Multiple documentation files exist (README.md, AGENTS.md, SYSTEM_GUIDE.md, etc.)
- Some redundancy between documentation files
- Limited examples of actual usage
- No recorded sessions or notebooks
- No sample prompts with expected outputs
- No troubleshooting guide
- Documentation scattered across different directories

### Impact

- New users struggle to get started
- Time wasted finding the right documentation
- Users don't understand full system capabilities
- Common issues repeatedly encountered
- Contributors unclear on how to extend system

---

## Proposed Solution

### Overview

Consolidate and streamline documentation with a unified onboarding guide, comprehensive examples, troubleshooting resources, and clear contributor documentation.

### Technical Requirements

#### 1. Unified Onboarding Guide

```markdown
# docs/GETTING_STARTED.md

# Getting Started with PaperKit

Welcome to PaperKit! This guide will help you write your first 
academic paper using our AI-powered agent system.

## Prerequisites

Before you begin, make sure you have:
- [ ] VS Code with GitHub Copilot extension
- [ ] Python 3.8+ installed
- [ ] LaTeX distribution (TeX Live recommended)
- [ ] Git

## Quick Start (5 minutes)

### Step 1: Install Paper Kit

```bash
# Clone the repository
git clone https://github.com/peternicholls/PaperKit.git
cd PaperKit

# Run the installer
./paperkit-install.sh
```

### Step 2: Activate Your First Agent

1. Open VS Code
2. Open Copilot Chat (Ctrl+Shift+I / Cmd+Shift+I)
3. Select "paper-architect" from the agent dropdown
4. Type: "Create an outline for a paper on [your topic]"

### Step 3: Follow the Workflow

```
Define Topic → Outline → Research → Draft → Refine → Build PDF
```

Each step uses a different agent. See [Agent Guide](AGENT_GUIDE.md) for details.

## What's Next?

- [Full Tutorial](tutorials/first-paper.md) - Write your first paper
- [Agent Reference](AGENT_GUIDE.md) - All available agents
- [Examples](examples/) - Sample papers and prompts
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
```

#### 2. Example Collection

```
docs/
├── examples/
│   ├── README.md                    # Examples overview
│   ├── prompts/
│   │   ├── research-consolidator/
│   │   │   ├── basic-research.md
│   │   │   ├── multi-source.md
│   │   │   └── expected-output.md
│   │   ├── paper-architect/
│   │   │   ├── simple-outline.md
│   │   │   ├── detailed-structure.md
│   │   │   └── expected-output.md
│   │   ├── section-drafter/
│   │   │   ├── introduction.md
│   │   │   ├── methodology.md
│   │   │   └── expected-output.md
│   │   └── quality-refiner/
│   │       ├── clarity-improvement.md
│   │       └── expected-output.md
│   │
│   ├── workflows/
│   │   ├── quick-paper/             # 1-hour paper workflow
│   │   │   ├── README.md
│   │   │   ├── step-1-outline.md
│   │   │   ├── step-2-draft.md
│   │   │   └── step-3-build.md
│   │   └── full-research-paper/     # Full workflow example
│   │       ├── README.md
│   │       └── ...
│   │
│   └── sample-outputs/
│       ├── outline-example.md
│       ├── draft-section.tex
│       └── final-paper.pdf
```

#### 3. Sample Prompts with Expected Outputs

```markdown
# docs/examples/prompts/paper-architect/simple-outline.md

# Paper Architect: Simple Outline

## Prompt

```
Create an outline for a research paper on "The Impact of 
Machine Learning on Medical Diagnosis". 

Target audience: Healthcare technology researchers
Target length: 8,000 words
Focus: Practical applications and current limitations
```

## Expected Output

The Paper Architect will produce:

1. **Outline document** at `output-drafts/outlines/paper-outline.md`
2. **LaTeX skeleton** in `latex/sections/`
3. **Updated metadata** in `memory/paper-metadata.yaml`

### Sample Outline Output

```markdown
# Paper Outline: ML in Medical Diagnosis

## 1. Introduction (1000 words)
- Problem statement: Current diagnostic challenges
- Thesis: ML offers transformative potential with caveats
- Scope: Focus on imaging, pathology, clinical decision support

## 2. Background (1500 words)
### 2.1 Traditional Diagnostic Methods
### 2.2 Rise of ML in Healthcare
### 2.3 Key Technologies (CNN, Transformers, etc.)

## 3. Current Applications (2000 words)
### 3.1 Medical Imaging Analysis
### 3.2 Pathology and Lab Results
### 3.3 Clinical Decision Support Systems

## 4. Evaluation and Limitations (1500 words)
### 4.1 Performance Metrics
### 4.2 Current Limitations
### 4.3 Regulatory Considerations

## 5. Case Studies (1000 words)
### 5.1 Successful Implementation: [Example]
### 5.2 Challenges Faced: [Example]

## 6. Future Directions (800 words)

## 7. Conclusion (200 words)
```

## Common Variations

- **More detailed**: Add "Include subsections for each major point"
- **Specific focus**: Add "Focus particularly on cardiology applications"
- **Different length**: Adjust "Target length: X words"
```

#### 4. Troubleshooting Guide

```markdown
# docs/TROUBLESHOOTING.md

# Troubleshooting Guide

## LaTeX Build Errors

### Error: "Missing \begin{document}"

**Symptom**: Build fails with "Missing \begin{document}" error

**Cause**: Section file doesn't have proper LaTeX structure

**Solution**:
```bash
# Check for syntax errors
./tools/lint-latex.sh

# Common fixes:
# 1. Ensure section files don't have \begin{document}
# 2. Check for unclosed braces
# 3. Verify all \input{} paths are correct
```

### Error: "Citation undefined"

**Symptom**: Build warns about undefined citations

**Cause**: Citation key in text doesn't match bibliography

**Solution**:
```bash
# Run citation consistency check
python3 tools/validate-references.py --check-consistency

# Common causes:
# 1. Typo in citation key
# 2. Entry missing from references.bib
# 3. BibTeX not run (need multiple builds)
```

### Error: "Package not found"

**Symptom**: Build fails with "Package X not found"

**Solution**:
```bash
# Install missing package (TeX Live)
tlmgr install <package-name>

# Or use full TeX Live installation
sudo apt-get install texlive-full
```

## Agent Issues

### Agent Not Responding

**Symptom**: Agent doesn't respond or gives generic answers

**Possible causes**:
1. Agent not properly activated
2. Context too large
3. Ambiguous prompt

**Solutions**:
```
# Re-select agent from dropdown
# Clear chat and start fresh
# Be more specific in your prompt
```

### Agent Produces Wrong Output

**Symptom**: Agent output doesn't match expected format

**Solutions**:
```
# Provide clearer instructions
# Reference specific output format
# Use example from docs/examples/prompts/
```

## Common Build Issues

| Issue | Quick Fix |
|-------|-----------|
| PDF not generated | Run `./tools/build-latex.sh` |
| Blank PDF | Check for LaTeX errors in .log file |
| Missing figures | Verify image paths in \includegraphics |
| Wrong citations | Run build 3 times for BibTeX |
| Encoding errors | Save files as UTF-8 |
```

#### 5. Contributor Documentation

```markdown
# docs/CONTRIBUTING_GUIDE.md

# Contributor Guide

## Adding a New Agent

### Step 1: Define Agent Specification

Create `.paper/[module]/agents/[agent-name].md`:

```markdown
# Agent: [Name]

## Identity
- **Role**: [Role description]
- **Persona**: [Persona name]

## Capabilities
- [Capability 1]
- [Capability 2]

## Constraints
- [Constraint 1]
- [Constraint 2]

## Example Prompts
- "[Example prompt 1]"
- "[Example prompt 2]"
```

### Step 2: Register in Manifest

Add to `.paper/_cfg/agent-manifest.yaml`:

```yaml
- name: "[agent-id]"
  displayName: "[Display Name]"
  module: "[core|specialist]"
  path: ".paper/[module]/agents/[agent-name].md"
```

### Step 3: Create GitHub Copilot Mode

Create `.github/agents/paper-[agent-name].agent.md`:

```markdown
---
name: paper-[agent-name]
description: [Brief description]
---

[Agent instructions from Step 1]
```

### Step 4: Test the Agent

1. Open Copilot Chat
2. Select new agent from dropdown
3. Test with example prompts
4. Verify output format

### Step 5: Add Documentation

- Add example prompts to `docs/examples/prompts/[agent-name]/`
- Update `docs/AGENT_GUIDE.md`
- Add to README agent table
```

#### 6. Documentation Structure

```
docs/
├── README.md                  # Docs index
├── GETTING_STARTED.md         # Quick start guide
├── AGENT_GUIDE.md             # Complete agent reference
├── WORKFLOW_GUIDE.md          # Workflow documentation
├── TROUBLESHOOTING.md         # Problem solving
├── FAQ.md                     # Frequently asked questions
├── CONTRIBUTING_GUIDE.md      # For contributors
│
├── tutorials/
│   ├── first-paper.md         # Write your first paper
│   ├── using-agents.md        # Agent interaction tutorial
│   ├── latex-basics.md        # LaTeX for PaperKit
│   └── citation-management.md # Managing references
│
├── examples/
│   ├── prompts/               # Example prompts per agent
│   ├── workflows/             # Complete workflow examples
│   └── sample-outputs/        # Expected outputs
│
├── reference/
│   ├── agent-contracts.md     # Agent input/output specs
│   ├── file-formats.md        # YAML/LaTeX formats
│   └── api-reference.md       # Tool API documentation
│
└── videos/                    # Video tutorials (links)
    └── README.md
```

#### 7. Interactive Examples (Notebook Format)

```markdown
# docs/tutorials/first-paper.md

# Tutorial: Write Your First Paper

This tutorial walks you through creating a complete paper
using PaperKit.

## Setup

Estimated time: 45 minutes
Prerequisites: PaperKit installed, VS Code with Copilot

## Part 1: Define Your Paper (5 min)

### 1.1 Activate Paper Architect

1. Open Copilot Chat
2. Select `paper-architect` from dropdown
3. You should see the agent's welcome menu

### 1.2 Create Your Outline

Copy and paste this prompt:

```
Create an outline for a short position paper on 
"Why Every Developer Should Understand Basic Statistics".

Target: Software developers
Length: 2000 words
Sections: 5
```

Expected output: An outline file at `output-drafts/outlines/`

✅ **Checkpoint**: Verify the outline file exists

## Part 2: Draft Your Introduction (10 min)

### 2.1 Switch to Section Drafter

Select `paper-section-drafter` from the agent dropdown.

### 2.2 Draft the Introduction

```
Draft the introduction section based on the outline.
Make it engaging and establish why this topic matters
to software developers.
```

Expected output: A .tex file at `output-drafts/sections/`

✅ **Checkpoint**: Open the .tex file and verify content

[Continue with remaining sections...]

## Troubleshooting This Tutorial

| Issue | Solution |
|-------|----------|
| Agent not appearing | Restart VS Code |
| Output file not created | Check for error messages in chat |
| LaTeX syntax errors | Run `./tools/lint-latex.sh` |
```

---

## Implementation Steps

| Step | Description | Estimated Effort |
|------|-------------|------------------|
| 1 | Audit existing documentation | 2 hours |
| 2 | Create unified getting started guide | 4 hours |
| 3 | Create example prompts for each agent | 8 hours |
| 4 | Create workflow examples | 6 hours |
| 5 | Write troubleshooting guide | 4 hours |
| 6 | Create contributor guide | 4 hours |
| 7 | Restructure documentation directory | 2 hours |
| 8 | Create tutorial notebooks | 6 hours |
| 9 | Review and consolidate redundant docs | 4 hours |
| 10 | Update all cross-references | 2 hours |

**Total Estimated Effort:** 42 hours

---

## Success Criteria

- [ ] Single clear entry point for new users
- [ ] Example prompts available for every agent
- [ ] At least one complete workflow example
- [ ] Troubleshooting covers top 10 issues
- [ ] Contributor guide enables new agent creation
- [ ] No redundant documentation
- [ ] All docs reachable within 2 clicks from main README

---

## Dependencies

- None (can be done independently)

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Documentation becomes stale | Medium | Link docs to tests; review quarterly |
| Examples don't match actual output | Medium | Test examples in CI |
| Too much documentation | Low | Progressive disclosure; clear navigation |

---

## Related Specifications

- [005-testing-ci.md](005-testing-ci.md) - Documentation testing
- All other specs - Need documentation updates

---

## Open Questions

1. Should we create video tutorials?
2. What's the right level of detail for examples?
3. Should docs be versioned with releases?
4. How to handle multiple IDE documentation?

---

## References

- Current docs: README.md, AGENTS.md, SYSTEM_GUIDE.md
- Diátaxis documentation framework: https://diataxis.fr/
- Write the Docs: https://www.writethedocs.org/
