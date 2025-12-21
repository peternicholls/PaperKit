# Deprecation Notice: VERSION File

**Date:** December 21, 2025  
**Status:** Deprecated and renamed to `VERSION.deprecated`  
**Replacement:** `.paperkit/_cfg/version.yaml`

## Summary

The plain-text `VERSION` file has been deprecated in favor of the YAML-based version management system. The file has been renamed to `VERSION.deprecated` to clearly indicate its status while maintaining backwards compatibility for external tools.

## What Changed

### File Status
- **Old Location:** `VERSION` (root directory)
- **New Location:** `VERSION.deprecated` (root directory, with deprecation notice)
- **Replacement:** `.paperkit/_cfg/version.yaml` (YAML-based configuration)

### Script Updates
All PaperKit scripts have been updated to use the YAML-based version system:

1. **`paperkit` (CLI)** - Removed direct VERSION file fallback; uses get-version.sh which handles fallback
2. **`paperkit-bundle.sh`** - Removed direct VERSION file fallback; uses get-version.sh
3. **`.paperkit/tools/get-version.sh`** - Updated to check VERSION.deprecated (and VERSION as secondary fallback)
4. **Tests** - Updated to reflect deprecation status

### Backwards Compatibility

The system maintains backwards compatibility:
- `.paperkit/tools/get-version.sh` checks for `VERSION.deprecated` file
- Falls back to `VERSION` if `VERSION.deprecated` doesn't exist
- External tools can continue using the deprecated file temporarily

## Migration Path

### For PaperKit Users
✅ **No action required** - All PaperKit commands now use the YAML system automatically.

Use these commands for version management:
```bash
./paperkit version                    # Show current version
./paperkit version --set alpha-1.3.0  # Set new version
./paperkit version --bump patch       # Bump version
./paperkit version --info             # Show full version info (JSON)
```

### For External Tool Maintainers

If you have scripts that read the VERSION file:

1. **Update to use get-version.sh** (recommended):
   ```bash
   VERSION=$(./.paperkit/tools/get-version.sh)
   ```

2. **Continue using VERSION.deprecated** (temporary):
   ```bash
   VERSION=$(cat VERSION.deprecated | grep -v '^#' | head -n 1)
   ```

3. **Migrate to YAML** (future-proof):
   ```bash
   # Requires PyYAML
   VERSION=$(python3 ./.paperkit/tools/version-manager.py get)
   ```

## Timeline

- **December 21, 2025**: VERSION file deprecated and renamed to VERSION.deprecated
- **Current**: All PaperKit scripts migrated to YAML system
- **Future**: VERSION.deprecated may be removed in a future major version

## Documentation

See these documents for more information:
- [Version Migration Guide](.paperkit/docs/version-migration-guide.md)
- [Version System README](.paperkit/docs/version-system-readme.md)
- [Commands Reference](../../Docs/COMMANDS.md)

## Questions?

If you have questions about this deprecation or need help migrating:
1. Check the [Version Migration Guide](version-migration-guide.md)
2. Run `./paperkit version --help` for CLI usage
3. See the [System Guide](../../Docs/SYSTEM_GUIDE.md) for architecture details
