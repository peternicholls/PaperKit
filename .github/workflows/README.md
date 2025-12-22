# GitHub Actions Workflows

This directory contains automated workflows for the PaperKit repository.

## Workflows

### `release.yml` - Release Automation

**Purpose**: Enforces service-side authorization for releases and automates release creation.

**Trigger**: Automatically runs when a version tag is pushed to the repository.

**Tag Patterns**:
- `1.2.3` - Standard semantic version
- `v1.2.3` - Version with 'v' prefix
- `alpha-1.2.3` - Alpha release
- `beta-1.2.3` - Beta release
- `1.2.3+build.456` - Version with build metadata

**What It Does**:
1. Validates the tag format
2. Verifies version consistency with configuration files
3. **Requires approval from authorized reviewers** (via `release` environment)
4. Creates the distribution bundle
5. Publishes a GitHub Release with the bundle attached

**Security**: This workflow uses GitHub Environment protection rules to enforce authorization. Even if someone bypasses local authorization checks in `./paperkit-dev`, they cannot complete a release without approval from authorized GitHub users.

**Setup Required**: 
- Create a `release` environment in repository settings
- Add authorized users as required reviewers
- See [dev-docs/service-side-authorization.md](../dev-docs/service-side-authorization.md) for detailed setup instructions

### `validate-agent-metadata.yml` - Agent Schema Validation

**Purpose**: Validates agent metadata and schemas.

**Trigger**: Runs on push/PR to master when agent files are modified.

**What It Does**:
1. Sets up Python environment
2. Installs dependencies
3. Validates agent schema definitions

## Environment Protection

The `release` workflow uses GitHub's Environment protection feature:

- **Environment**: `release`
- **Protection**: Requires approval from authorized reviewers
- **Enforcement**: Cannot be bypassed - provides true security

### Setting Up Protection

1. Go to repository **Settings** → **Environments**
2. Create environment named `release`
3. Enable "Required reviewers"
4. Add authorized users (e.g., repository owner)
5. Save protection rules

See the [Service-Side Authorization Guide](../dev-docs/service-side-authorization.md) for complete setup instructions.

## Workflow Permissions

### `release.yml`
- `contents: write` - Required to create releases and upload assets

### `validate-agent-metadata.yml`
- `contents: read` - Read-only access to repository

## Testing Workflows

### Local Testing
Use `act` to test workflows locally:
```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
# or follow instructions at https://github.com/nektos/act

# Test release workflow (dry-run)
act push -j create-release
```

### Test in Repository
1. Create a test tag: `git tag test-1.0.0`
2. Push tag: `git push origin test-1.0.0`
3. Watch workflow in Actions tab
4. Delete test release and tag after testing

## Troubleshooting

### "Environment not found" Error
- Ensure the `release` environment exists in repository settings
- Environment name must match exactly: `release`

### Workflow Not Triggering
- Check that tag matches one of the supported patterns
- Verify workflow file is in `.github/workflows/` directory
- Check workflow syntax with `yamllint` or GitHub's workflow validator

### Bundle Creation Fails
- Ensure all required files exist in the repository
- Check that `bundle.sh` script is executable
- Review workflow logs in Actions tab for detailed error messages

## Related Documentation

- [Service-Side Authorization](../dev-docs/service-side-authorization.md) - Setup guide for environment protection
- [Developer Commands](../dev-docs/developer-commands.md) - Local development commands
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Environments Documentation](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
