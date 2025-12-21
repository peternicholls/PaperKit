# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- YAML-based version management system (`.paperkit/_cfg/version.yaml`)
- Version management tools:
  - `.paperkit/tools/get-version.sh` - Shell script for version retrieval
  - `.paperkit/tools/version-manager.py` - Python tool for version management
- Documentation for version system:
  - `.paperkit/docs/version-system-readme.md` - Version system overview
  - `.paperkit/docs/version-migration-guide.md` - Migration guide
- Support for version bumping (major, minor, patch)
- Rich version metadata (release dates, compatibility info, semantic components)

### Changed
- `paperkit` script now reads version from YAML config with fallback to VERSION file
- `paperkit-bundle.sh` updated to use YAML-based version system
- `.paperkit/_cfg/manifest.yaml` updated to reference new version system

### Deprecated
- `VERSION` file (legacy plain-text version file, backwards compatibility maintained)

## [alpha-1.2.0] - 2025-12-19

### Added
- Automated `.copilot/` directory generation from `.paperkit/` source files
- Automated generation of AGENTS.md and COPILOT.md documentation
- PaperKit Installer v2.0.0 with IDE selection and enhanced validation
- Comprehensive agent schema validation for all paper-writing agents
- Enhanced forensic audit documentation with practical recommendations

### Fixed
- Validation script paths updated from `.paper/` to `.paperkit/` directory structure
- Improved LaTeX document compilation and linting tools
- Enhanced academic integrity constraints in agent definitions

### Changed
- Refactored code structure for improved readability and maintainability
- Updated GitHub Copilot and Codex prompts with integrity reminders
- Enhanced agent guides with validation resources

### Deprecated
- CSV-based manifests (migrated to YAML)

## [alpha-1.0.0] - 2025-12-01

### Added
- Initial PaperKit release with core paper-writing agents
- LaTeX document generation and assembly
- Harvard citation style support
- Research consolidation and validation workflows
- Agent-based academic paper generation system
