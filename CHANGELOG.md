# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [alpha-1.3.0] - 2025-12-21

### Added
- Automated GitHub release creation via GitHub CLI integration
- Release command now creates releases, uploads bundles, and publishes automatically

### Fixed
- Color formatting in terminal output (missing `-e` flag in echo commands)
- Fixed 24 instances across `paperkit-dev`, `paperkit-install.sh`, and `scripts/base-install.sh`
- ANSI color codes now render properly instead of displaying literal escape sequences

### Changed
- Release workflow now fully automated with `./paperkit-dev release --full`
- Improved error handling with graceful fallback when GitHub CLI unavailable

## [alpha-1.2.1] - 2025-12-19

### Added
- YAML-based version management system (`.paperkit/_cfg/version.yaml`)
- Version management tools:
  - `.paperkit/tools/get-version.sh` - Shell script for version retrieval
  - `.paperkit/tools/version-manager.py` - Python tool for version management
  - `.paperkit/tools/test-version-system.sh` - Comprehensive test suite
- CLI commands for version management:
  - `./paperkit version` - Show current version
  - `./paperkit version --set <version>` - Set new version
  - `./paperkit version --bump <part>` - Bump version (major/minor/patch)
  - `./paperkit version --build <value>` - Add build metadata
  - `./paperkit version --clear-build` - Remove build metadata
  - `./paperkit version --test` - Run version system tests
- Documentation for version system:
  - `.paperkit/docs/version-system-readme.md` - Version system overview
  - `.paperkit/docs/version-migration-guide.md` - Migration guide
  - `Docs/COMMANDS.md` - Consolidated CLI command reference
- Support for optional build metadata in semantic versioning (e.g., `1.2.0+45`)
- Rich version metadata (release dates, compatibility info, semantic components)

### Changed
- All PaperKit scripts now use YAML-based version system exclusively
- `paperkit` script reads version from YAML config (get-version.sh handles fallback)
- `paperkit-bundle.sh` updated to use YAML-based version system
- `.paperkit/_cfg/manifest.yaml` updated to reference new version system

### Deprecated
- `VERSION` file renamed to `VERSION.deprecated` (backwards compatibility maintained for external tools)

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
