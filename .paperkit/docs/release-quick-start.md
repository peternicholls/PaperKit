# Release Quick Start Guide

## TL;DR

```bash
# Bump version
./paperkit version --bump minor

# Update docs
vim RELEASE-NOTES.md CHANGELOG.md

# Commit
git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
git commit -m "Release $(./paperkit version | awk '{print $NF}')"

# Create bundle, tag, and push (one command!)
./paperkit release --full

# Go to GitHub → Releases → Draft new release → Select tag → Upload bundle → Publish
```

## What This Does

1. **`./paperkit version --bump minor`**
   - Increments version in `.paperkit/_cfg/version.yaml`
   - Updates release date to today
   - Examples: `alpha-1.2.0` → `alpha-1.3.0`

2. **`./paperkit release --full`**
   - Creates distribution bundle: `paperkit-alpha-1.3.0.tar.gz`
   - Creates annotated git tag: `alpha-1.3.0`
   - Pushes tag to origin

3. **Manual step: GitHub Releases**
   - Go to your repository's releases page
   - Click "Draft a new release"
   - Select the tag that was just pushed
   - Upload the `.tar.gz` bundle
   - Add release notes (copy from RELEASE-NOTES.md)
   - Click "Publish release"

## Version Bumping

```bash
# Patch: 1.2.0 → 1.2.1 (bug fixes)
./paperkit version --bump patch

# Minor: 1.2.0 → 1.3.0 (new features)
./paperkit version --bump minor

# Major: 1.2.0 → 2.0.0 (breaking changes)
./paperkit version --bump major

# Custom version
./paperkit version --set alpha-2.0.0
```

## Release Options

```bash
# Just create bundle (no tagging)
./paperkit release --bundle

# Just create and push tag (no bundle)
./paperkit release --tag

# Full release (bundle + tag + push)
./paperkit release --full

# Preview what would happen
./paperkit release --full --dry-run
```

## Pre-Release Checklist

- [ ] All changes committed and pushed
- [ ] Tests passing
- [ ] CHANGELOG.md updated
- [ ] RELEASE-NOTES.md created/updated
- [ ] Version bumped appropriately
- [ ] Clean working directory (`git status`)

## Post-Release Steps

1. Verify tag was created: `git tag -l`
2. Verify tag was pushed: `git ls-remote --tags origin`
3. Extract and test the bundle
4. Create GitHub release from tag
5. Upload bundle to GitHub release
6. Announce release (if applicable)

## Troubleshooting

**Tag already exists:**
```bash
./paperkit release --full
# Will prompt to delete and recreate
```

**Bundle creation failed:**
```bash
# Check bundle script is executable
ls -la .paperkit/tools/bundle.sh
chmod +x .paperkit/tools/bundle.sh
```

**Version shows "unknown":**
```bash
# Check version file
cat .paperkit/_cfg/version.yaml

# Test version script
./.paperkit/tools/get-version.sh
```

## Release Naming Convention

PaperKit uses: `[prerelease]-[major].[minor].[patch]`

- `alpha-1.2.0` - Alpha release, experimental
- `beta-1.3.0` - Beta release, feature complete
- `rc-2.0.0` - Release candidate, final testing
- `stable-2.0.0` - Stable production release

## Example Release Session

```bash
$ ./paperkit version
PaperKit - version alpha-1.2.0

$ ./paperkit version --bump minor
Version bumped to: alpha-1.3.0

$ vim RELEASE-NOTES.md  # Add release notes
$ vim CHANGELOG.md      # Update changelog

$ git add .paperkit/_cfg/version.yaml RELEASE-NOTES.md CHANGELOG.md
$ git commit -m "Release alpha-1.3.0"
[main abc1234] Release alpha-1.3.0
 3 files changed, 45 insertions(+)

$ ./paperkit release --full
════════════════════════════════════════════════════════════════════════════
PaperKit Release: alpha-1.3.0
════════════════════════════════════════════════════════════════════════════

Creating distribution bundle...
📦 Creating PaperKit distribution bundle...
Version: alpha-1.3.0
Archive: paperkit-alpha-1.3.0.tar.gz
✓ Bundle created successfully

Creating git tag: alpha-1.3.0
✓ Tag created

Pushing tag to origin...
✓ Tag pushed

✓ Release alpha-1.3.0 complete!

Distribution bundle created:
  paperkit-alpha-1.3.0.tar.gz

Next steps:
  1. Go to GitHub releases page
  2. Draft a new release from tag: alpha-1.3.0
  3. Upload the distribution bundle
  4. Publish the release

$ # Upload to GitHub and publish 🎉
```

## See Also

- [Release Workflow](release-workflow.md) - Complete documentation
- [Version System](version-system-readme.md) - Version management details
- [CHANGELOG.md](../../CHANGELOG.md) - Version history
