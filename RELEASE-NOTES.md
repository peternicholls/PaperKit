# Release Notes - PaperKit alpha-1.3.0

**Release Date:** December 21, 2025

## Overview

PaperKit alpha-1.3.0 delivers critical quality-of-life improvements focused on developer experience and release automation. This release fixes terminal output formatting issues that affected readability and introduces fully automated GitHub release workflows.

## Key Features

### 🚀 Release Automation
- **Fully Automated Releases**: `./paperkit-dev release --full` now handles the entire release process
  - Creates and pushes git tags
  - Generates distribution bundles
  - Creates GitHub releases with auto-generated notes
  - Uploads release assets automatically
- **GitHub CLI Integration**: Seamless integration with `gh` CLI for release management
- **Smart Fallback**: Gracefully handles missing GitHub CLI with helpful manual instructions

### 🎨 Terminal Output Improvements
- **Fixed Color Rendering**: All ANSI color codes now display correctly
- **24 Fixes Across Scripts**: Corrected missing `-e` flags in echo commands
  - `paperkit-dev` version display
  - `paperkit-install.sh` IDE selection and Python setup menus
  - `scripts/base-install.sh` installation menus and next steps
- **Enhanced Readability**: Colored output improves user experience and command clarity

## Bug Fixes

### Terminal Output Formatting
- **Fixed ANSI color codes** displaying as literal text (e.g., `\033[1;33m`) instead of formatted colors
- **Corrected 24 echo commands** missing the `-e` flag required to interpret escape sequences
- **Affected files:**
  - `paperkit-dev`: Version command output
  - `paperkit-install.sh`: IDE selection menu, Python setup options, activation instructions
  - `scripts/base-install.sh`: Installation menus, next steps, stash instructions

### Developer Experience
- **Improved error messages** in release workflow with clearer troubleshooting steps
- **Better authentication checks** for GitHub CLI before attempting release creation

## Breaking Changes

None in this release.

## Deprecations

- CSV-based manifests have been fully migrated to YAML format
- Legacy `.paper/` directory references have been updated to `.paperkit/`

## Migration Guide

If you're upgrading from alpha-1.2.x:

1. **No breaking changes** - this is a quality-of-life release
2. **Optional**: Install GitHub CLI for automated releases:
   ```bash
   # macOS
   brew install gh
   
   # Authenticate
   gh auth login
   ```
3. **Enjoy improved output** - all color formatting now works correctly

If you're upgrading from alpha-1.0.0 or earlier, see previous release notes for migration steps.

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

**Version:** alpha-1.3.0  
**Release Channel:** Alpha  
**Status:** Active Development
