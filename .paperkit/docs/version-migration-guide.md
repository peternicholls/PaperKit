# Version Management System Migration Guide

## Overview

PaperKit now uses a YAML-based configuration file (`.paperkit/_cfg/version.yaml`) for version management instead of the deprecated `VERSION` file. This provides a more robust, structured approach to version releases.

**Status:** The plain-text `VERSION` file has been deprecated and renamed to `VERSION.deprecated` as of December 21, 2025. All scripts now use the YAML-based system, with fallback support for backwards compatibility.

## What Changed

### Before (Legacy)
- Version stored in plain text `VERSION` file at repository root
- Single line containing version string (e.g., `alpha-1.2.0`)
- Limited metadata and no structured information

### After (New YAML System)
- Version stored in `.paperkit/_cfg/version.yaml`
- Rich metadata including release dates, compatibility info, semantic version components
- Tools for reading and updating versions programmatically
- Backwards compatible with deprecated `VERSION.deprecated` file

## New Version Configuration File

Location: `.paperkit/_cfg/version.yaml` (generated; do not edit manually)

```yaml
version:
  current: "alpha-1.2.0"
  # Canonical semantic version components
  semver:
    major: 1
    minor: 2
    patch: 0
    prerelease: "alpha"
    build: "" # optional build metadata (appended as +build)

  # Release metadata
  release:
    date: "2025-12-19"
    type: "alpha"

  # Build and update metadata
  metadata:
    buildDate: "2025-12-19"
    lastUpdated: "2025-12-19"

  # Compatibility information
  compatibility:
    minPythonVersion: "3.7"
    minGitVersion: "2.0"

  # References
  references:
    releaseNotes: "RELEASE-NOTES.md"
    changelog: "CHANGELOG.md"
```

## Tools

### Shell Script: `.paperkit/tools/get-version.sh`

Get the current version (tries YAML first, falls back to VERSION file):

```bash
./.paperkit/tools/get-version.sh
# Output: alpha-1.2.0
```

### Python Script: `.paperkit/tools/version-manager.py`

Comprehensive version management tool:

```bash
# Get current version
python3 ./.paperkit/tools/version-manager.py get

# Get full version information
python3 ./.paperkit/tools/version-manager.py info

# Set a new version
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0

# Optionally include a build number (appends `+build`)
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0+45

# Bump version (patch, minor, or major)
python3 ./.paperkit/tools/version-manager.py bump patch
python3 ./.paperkit/tools/version-manager.py bump minor
python3 ./.paperkit/tools/version-manager.py bump major
```

## Updated Scripts

The following scripts now use the new version system:

1. **`paperkit`** - Main CLI reads from YAML config
2. **`paperkit-bundle.sh`** - Bundle creator uses YAML config

Both scripts maintain backwards compatibility with the legacy `VERSION` file.

## Backwards Compatibility

The new system is **fully backwards compatible**:

1. Scripts try to read from `.paperkit/_cfg/version.yaml` first
2. If YAML file doesn't exist or can't be read, falls back to `VERSION` file
3. If neither exists, returns "unknown"

## Migration Path

### For Existing Installations

No action required! The system will automatically:
1. Try the new YAML-based system
2. Fall back to the existing `VERSION` file if needed

### For New Releases

When creating a new release:

```bash
# Option 1: Use Python version manager (recommended)
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0

# Option 2: Edit .paperkit/_cfg/version.yaml directly
# Update the 'current' field and related metadata

# Verify the change
./paperkit version
```

### For Package Maintainers

The `VERSION` file has been deprecated and renamed to `VERSION.deprecated`. All PaperKit scripts now use the YAML system:

1. **Migration Complete** (as of December 21, 2025):
   - All scripts now use `.paperkit/_cfg/version.yaml` as the source of truth
   - `VERSION.deprecated` is maintained only for backwards compatibility with external tools
   - Use `./paperkit version` commands to manage versions

2. **Remove VERSION.deprecated** (optional, after external tool migration):
   - Can be removed once all external scripts are updated
   - The file contains a deprecation notice for users who encounter it

## Deprecation Timeline

- **December 21, 2025**: VERSION file deprecated and renamed to VERSION.deprecated
- **Current**: All PaperKit scripts migrated to YAML system
- **Future**: VERSION.deprecated may be removed in a future major version once external dependencies are updated

## Benefits of YAML-Based System

1. **Rich Metadata**: Store release dates, compatibility info, semantic version components
2. **Structured Data**: Easy to parse and validate
3. **Extensibility**: Can add new fields without breaking existing tools
4. **Automation**: Better support for automated release workflows
5. **Consistency**: Aligns with other `.paperkit/_cfg/` configurations
6. **Version Bumping**: Built-in tools for incrementing version numbers

## FAQ

**Q: Do I need to do anything immediately?**
A: No, the system is backwards compatible. Your existing setup will continue to work.

**Q: Can I still use the VERSION file?**
A: Yes, but it's deprecated. The scripts will fall back to it if the YAML file isn't available.

**Q: What if I don't have Python installed?**
A: The shell script `.paperkit/tools/get-version.sh` works without Python, though with reduced functionality.

**Q: How do I update the version?**
A: Use `python3 ./.paperkit/tools/version-manager.py set <version>` or edit `.paperkit/_cfg/version.yaml` directly.

## Example: Creating a New Release

```bash
# 1. Bump the version
python3 ./.paperkit/tools/version-manager.py bump minor
# Output: Version bumped to: alpha-1.3.0

# 2. Verify
./paperkit version
# Output: paperkit version alpha-1.3.0

# 3. Update release notes
# Edit RELEASE-NOTES.md and CHANGELOG.md

# 4. Create bundle
./paperkit-bundle.sh
# Creates: paperkit-alpha-1.3.0.tar.gz

# 5. Commit and tag
git add .paperkit/_cfg/version.yaml
git commit -m "Release alpha-1.3.0"
git tag alpha-1.3.0
```

## Support

For issues or questions about the new version system:
1. Check this migration guide
2. Review `.paperkit/_cfg/version.yaml` structure
3. Test with `.paperkit/tools/version-manager.py --help`
