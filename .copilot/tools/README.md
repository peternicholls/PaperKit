# Tools Registry

This directory contains the tools registry that defines available scripts and utilities used by agents.

## tools.yaml

The main registry file that defines:
- **Tool metadata:** Name, description, path
- **Execution settings:** Working directory, timeout, language
- **Consent requirements:** Risk level, consent scope
- **I/O definitions:** Inputs, outputs, side effects
- **Safety properties:** Rollback capability, undo support

## Available Tools

### build-latex.sh
Compiles LaTeX document to PDF.
- **Risk level:** Medium (creates files)
- **Requires consent:** Yes
- **Used by:** LaTeX Assembler

### lint-latex.sh
Checks LaTeX syntax and common issues.
- **Risk level:** Low (read-only)
- **Requires consent:** No
- **Used by:** LaTeX Assembler

### validate-structure.py
Validates paper structure and section completeness.
- **Risk level:** Low (read-only)
- **Requires consent:** No
- **Used by:** LaTeX Assembler

### format-references.py
Formats and validates bibliography in Harvard style.
- **Risk level:** Medium (modifies files)
- **Requires consent:** Yes
- **Used by:** Reference Manager

## Adding New Tools

To add a new tool:

1. Create the script in `open-agents/tools/`
2. Add entry to `tools.yaml` with full metadata
3. Update `consent.yaml` if tool requires consent
4. Register tool with appropriate agents in `agents.yaml`

## Consent Levels

Tools are categorized by risk:
- **Low:** Read-only operations, no consent needed
- **Medium:** File modifications, consent required
- **High:** System changes, enhanced consent with confirmation
