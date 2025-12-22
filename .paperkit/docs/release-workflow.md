# Release Workflow with YAML Version System

This guide explains how to use the new YAML-based version system when creating releases for PaperKit.

## Quick Release Workflow

### Option A: Using the Release Command (Recommended)

```bash
# 1. Bump the version
./paperkit version --bump minor

# 2. Update release documentation
vim RELEASE-NOTES.md
vim CHANGELOG.md

# 3. Commit changes
git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
git commit -m "Release alpha-1.3.0"

# 4. Create bundle and tag release (one command!)
./paperkit release --full

# 5. Upload bundle to GitHub releases
```

### Option B: Manual Steps

### 1. Bump the Version

Choose the appropriate version bump type:

```bash
# For bug fixes (1.2.0 -> 1.2.1)
python3 ./.paperkit/tools/version-manager.py bump patch

# For new features (1.2.0 -> 1.3.0)
python3 ./.paperkit/tools/version-manager.py bump minor

# For breaking changes (1.2.0 -> 2.0.0)
python3 ./.paperkit/tools/version-manager.py bump major
```

Or set a specific version:

```bash
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0
```

### 2. Verify the Version

```bash
# Check version
./paperkit version

# View full version info
python3 ./.paperkit/tools/version-manager.py info
```

### 3. Update Release Documentation

Edit the following files:
- `RELEASE-NOTES.md` - Detailed release notes for this version
- `CHANGELOG.md` - Add entry to changelog

### 4. Create Distribution Bundle

```bash
./.paperkit/tools/bundle.sh
```

This creates a file like `paperkit-alpha-1.3.0.tar.gz` using the version from the YAML config.

### 5. Commit Changes

```bash
git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
git commit -m "Release alpha-1.3.0"
```

### 6. Create Bundle and Tag

**Option 1: Automated (Recommended)**
```bash
./paperkit release --full
```

**Option 2: Manual**
```bash
# Create bundle
./.paperkit/tools/bundle.sh

# Create and push tag
git tag -a alpha-1.3.0 -m "Release alpha-1.3.0"
git push origin alpha-1.3.0
```

### 7. Upload Distribution

Upload the bundle created in step 4 to GitHub releases or your distribution channel.

## Advanced Usage

### Setting a Specific Release Type

```bash
python3 ./.paperkit/tools/version-manager.py set alpha-2.0.0
# Then manually edit .paperkit/_cfg/version.yaml to set:
# release:
#   type: beta  # or alpha, rc, stable
```

### Custom Release Date

By default, version bumping updates the release date to today. To prevent this:

```bash
python3 ./.paperkit/tools/version-manager.py set alpha-1.3.0 --no-date-update
```

### Viewing Version Components

```bash
python3 ./.paperkit/tools/version-manager.py info | grep components
```

Output:
```json
"components": {
  "major": 1,
  "minor": 3,
  "patch": 0,
  "prerelease": "alpha"
}
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Release

on:
  push:
    tags:
      - 'alpha-*'
      - 'beta-*'
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Get version
        id: version
        run: |
          VERSION=$(python3 ./.paperkit/tools/version-manager.py get)
          echo "version=$VERSION" >> $GITHUB_OUTPUT
      
      - name: Create bundle
        run: ./.paperkit/tools/bundle.sh
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ steps.version.outputs.version }}
          draft: false
          prerelease: true
      
      - name: Upload Bundle
        uses: actions/upload-artifact@v2
        with:
          name: paperkit-${{ steps.version.outputs.version }}
          path: paperkit-*.tar.gz
```

## Version Naming Convention

PaperKit uses the following version format:

```
[prerelease]-[major].[minor].[patch]
```

Examples:
- `alpha-1.2.0` - Alpha release, version 1.2.0
- `beta-1.3.0` - Beta release, version 1.3.0
- `rc-2.0.0` - Release candidate, version 2.0.0
- `stable-2.0.0` - Stable release, version 2.0.0

## Troubleshooting

### Version not updating

Make sure you have PyYAML installed:
```bash
pip install pyyaml
```

### Release command fails

Check that git is configured and you're on the correct branch:
```bash
git status
git remote -v
```

Ensure all changes are committed before running `./paperkit release --full`.

### Tag already exists

Use `--dry-run` to preview, or delete the existing tag:
```bash
git tag -d alpha-1.3.0
git push origin :refs/tags/alpha-1.3.0
./paperkit release --tag
```

### Bundle using wrong version

The bundle script reads from YAML first, then VERSION file. Verify:
```bash
./.paperkit/tools/get-version.sh
```

### Version command shows "unknown"

Check that `.paperkit/_cfg/version.yaml` exists and is properly formatted:
```bash
cat .paperkit/_cfg/version.yaml
```

Run the test suite:
```bash
./.paperkit/tools/test-version-system.sh
```

## Best Practices

1. **Always bump version before creating a release** - Use `./paperkit version --bump <part>` instead of manually editing version.yaml
2. **Update release notes** - Keep RELEASE-NOTES.md and CHANGELOG.md in sync
3. **Test the bundle** - Extract and test the bundle before publishing
4. **Tag consistently** - Use the same version string for git tags
5. **Use CLI commands** - Use `./paperkit version` commands for all version management

## Example: Complete Release Process

**Recommended workflow using CLI commands:**

```bash
# 1. Bump version
./paperkit version --bump minor
# Output: Version bumped to: alpha-1.3.0

# 2. Verify
./paperkit version
# Output: PaperKit - version alpha-1.3.0

# 3. Update documentation
vim RELEASE-NOTES.md
vim CHANGELOG.md

# 4. Commit
git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
git commit -m "Release alpha-1.3.0"

# 5. Create bundle and tag (automated)
./paperkit release --full
# Creates: paperkit-alpha-1.3.0.tar.gz
# Creates and pushes tag: alpha-1.3.0

# 6. Upload bundle to GitHub releases
```

**Manual workflow:**

```bash
# 1. Bump version (manual)
python3 ./.paperkit/tools/version-manager.py bump minor

# 2. Verify
./paperkit version
# Output: PaperKit - version alpha-1.3.0

# 3. Update documentation
vim RELEASE-NOTES.md
vim CHANGELOG.md

# 4. Create bundle (manual)
./.paperkit/tools/bundle.sh
# Output: Archive: paperkit-alpha-1.3.0.tar.gz

# 5. Commit
git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
git commit -m "Release alpha-1.3.0"

# 6. Tag (manual)
git tag -a alpha-1.3.0 -m "Release alpha-1.3.0"
git push origin master alpha-1.3.0

# 7. Upload bundle to GitHub releases
```

**Manual workflow:**

```bash
# 1. Bump version
./paperkit version --bump minor
# Output: Version bumped to: alpha-1.3.0

# 2. Verify
./paperkit version
# Output: paperkit version alpha-1.3.0

# 3. Update documentation
vim RELEASE-NOTES.md
vim CHANGELOG.md

# 4. Create bundle
./.paperkit/tools/bundle.sh
# Output: Archive: paperkit-alpha-1.3.0.tar.gz

# 5. Commit
git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
git commit -m "Release alpha-1.3.0"

# 6. Tag
git tag alpha-1.3.0
git push origin master alpha-1.3.0

# 7. Upload bundle to GitHub releases
```

## Migration from Old System

**Status:** Migration complete as of December 21, 2025. The `VERSION` file has been deprecated and renamed to `VERSION.deprecated`.

- All PaperKit scripts now use the YAML-based version system
- The deprecated VERSION.deprecated file is maintained only for backwards compatibility with external tools
- Use `./paperkit version` commands for all version management
- External scripts should migrate to use `.paperkit/tools/get-version.sh` (which handles fallback)

See `.paperkit/docs/version-migration-guide.md` for complete migration instructions.
