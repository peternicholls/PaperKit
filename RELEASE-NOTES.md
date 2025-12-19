# Release Notes - PaperKit alpha-1.2.0

**Release Date:** December 19, 2025

## Overview

PaperKit alpha-1.2.0 introduces significant improvements to automation, validation, and documentation generation. This release focuses on streamlining the paper-writing workflow through automated CI/CD integration and enhanced IDE support.

## Key Features

### 🤖 Automation Enhancements
- **Automated Directory Generation**: The `.copilot/` directory is now automatically generated from `.paperkit/` source files, eliminating manual synchronization
- **Documentation Generation**: AGENTS.md and COPILOT.md are now auto-generated, ensuring consistency across all documentation
- **Validation Scripts**: Comprehensive agent schema validation ensures all agents meet system requirements

### 🔧 Installation & Setup
- **PaperKit Installer v2.0.0**: Enhanced installer with IDE selection (GitHub Copilot and OpenAI Codex support) and rigorous validation checks
- **Better Configuration Management**: Improved `.paperkit/_cfg/` structure with manifests and schemas

### 📚 Academic Integrity
- **Enhanced Constraints**: Stronger academic integrity enforcement in agent definitions
- **Forensic Audit Protocol**: Comprehensive documentation for auditing and validating research sources
- **Citation Validation**: Improved Harvard citation style validation and completeness checks

## Bug Fixes

- **Fixed validation script paths** from incorrect `.paper/` to correct `.paperkit/` directory structure
- **Improved LaTeX tooling** for document compilation and linting
- **Enhanced error handling** in validation and generation workflows

## Breaking Changes

None in this release.

## Deprecations

- CSV-based manifests have been fully migrated to YAML format
- Legacy `.paper/` directory references have been updated to `.paperkit/`

## Migration Guide

If you're upgrading from alpha-1.0.0:

1. Run the PaperKit installer to ensure your environment is configured correctly
2. The `.paperkit/` directory structure has been finalized—ensure your custom configurations are in `.paperkit/_cfg/`
3. All documentation generation now occurs automatically during CI/CD

## Known Issues

None reported in this release.

## System Requirements

- Python 3.11+
- LaTeX distribution (TeXLive, MiKTeX, or MacTeX)
- Git 2.30+
- VS Code with GitHub Copilot or OpenAI Codex extension

## Support

For issues, questions, or contributions, please refer to:
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [ARCHITECTURE.md](Docs/ARCHITECTURE.md)
- [Developer Improvements](Docs/DEVELOPER-IMPROVEMENTS/)

## Credits

PaperKit is maintained by Peter Nicholls and contributors.

---

**Version:** alpha-1.2.0  
**Release Channel:** Alpha  
**Status:** Active Development
