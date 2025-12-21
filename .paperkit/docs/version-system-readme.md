# PaperKit Version Management System

> Do not edit `.paperkit/_cfg/version.yaml` manually. Use `.paperkit/tools/version-manager.py` (`set`/`bump`) to update; the `current` field is generated from `semver`.

This directory contains the YAML-based version management system for PaperKit.

## Quick Start

### Get Current Version

```bash
# Using shell script (works without Python)
./.paperkit/tools/get-version.sh

# Using Python tool (more features)
python3 ./.paperkit/tools/version-manager.py get
```

### View Full Version Info

```bash
python3 ./.paperkit/tools/version-manager.py info
```

### Update Version

```bash
# Set a specific version
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0

# Or bump version automatically
python3 ./.paperkit/tools/version-manager.py bump patch  # 1.2.0 -> 1.2.1
python3 ./.paperkit/tools/version-manager.py bump minor  # 1.2.0 -> 1.3.0
python3 ./.paperkit/tools/version-manager.py bump major  # 1.2.0 -> 2.0.0

# Include an optional build number (appends `+build`)
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0+45
```

## Configuration File

**Location:** `.paperkit/_cfg/version.yaml` (generated; do not edit manually)

This YAML file is the source of truth for all version information. It contains:

- **current**: Generated version string derived from `semver`
- **semver**: Semantic components (major, minor, patch, optional prerelease, optional build metadata)
- **release**: Release metadata (date, type)
- **metadata**: Build and update dates
- **compatibility**: Minimum required versions of dependencies
- **references**: Paths to release notes and changelog

## Tools

### Shell Script: `get-version.sh`

**Purpose**: Simple, dependency-free version retrieval  
**Requirements**: None (bash only)  
**Fallback**: Automatically falls back to legacy VERSION file

```bash
./.paperkit/tools/get-version.sh
```

### Python Script: `version-manager.py`

**Purpose**: Full-featured version management  
**Requirements**: Python 3.7+, PyYAML  
**Features**:
- Get current version
- View full version info
- Set new version
- Bump version (major/minor/patch)
- Auto-update dates

```bash
# Get help
python3 ./.paperkit/tools/version-manager.py --help

# Commands
python3 ./.paperkit/tools/version-manager.py get
python3 ./.paperkit/tools/version-manager.py info
python3 ./.paperkit/tools/version-manager.py set <version>
python3 ./.paperkit/tools/version-manager.py bump <major|minor|patch>
```

## Integration

The version system is integrated into:

1. **`paperkit` CLI**: Main command-line tool reads from YAML config
2. **`.paperkit/tools/bundle.sh`**: Bundle creator uses YAML version for naming
3. **CI/CD**: Can be used in automated release workflows

## Backwards Compatibility

The system maintains full backwards compatibility with the legacy `VERSION` file:

1. Scripts try YAML config first
2. Fall back to `VERSION` file if YAML unavailable
3. Return "unknown" if neither exists

## Migration

See `.paperkit/docs/version-migration-guide.md` for complete migration instructions.

## Examples

### Release Workflow

```bash
# 1. Bump version
python3 ./.paperkit/tools/version-manager.py bump minor
# Output: Version bumped to: alpha-1.3.0

# 2. Verify
./paperkit version
# Output: paperkit version alpha-1.3.0

# 3. Create bundle
./.paperkit/tools/bundle.sh
# Creates: paperkit-alpha-1.3.0.tar.gz
```

### Version Info in Scripts

```bash
#!/bin/bash
VERSION=$(./.paperkit/tools/get-version.sh)
echo "Current version: $VERSION"
```

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, '.paperkit/tools')
from version_manager import VersionManager

vm = VersionManager()
print(f"Current version: {vm.get_version()}")
```

## Files

- **`version.yaml`**: Version configuration (source of truth)
- **`get-version.sh`**: Shell script for getting version
- **`version-manager.py`**: Python tool for version management
- **`version-migration-guide.md`**: Migration documentation

## Development

When making changes:

1. Update `.paperkit/_cfg/version.yaml`
2. Test with both tools to ensure consistency
3. Run `./paperkit version` to verify
4. Update RELEASE-NOTES.md and CHANGELOG.md
