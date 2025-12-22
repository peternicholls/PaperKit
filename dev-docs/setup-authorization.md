# Quick Setup: Service-Side Release Authorization

This is a quick reference for setting up GitHub Environment protection. For detailed information, see [service-side-authorization.md](service-side-authorization.md).

## One-Time Setup (Repository Admin)

### 1. Create Protected Environment

1. Go to your repository on GitHub
2. Navigate to: **Settings** → **Environments**
3. Click **New environment**
4. Name it: `release` (must match exactly)
5. Click **Configure environment**

### 2. Add Protection Rules

Enable these settings:

- ✅ **Required reviewers**
  - Click "Add required reviewers"
  - Search for and add authorized users (repository owners/maintainers)
  - Minimum reviewers: 1

- ✅ **Prevent self-review** (recommended)
  - Ensures releases are reviewed by someone other than the person who created them

- ✅ **Deployment branches** (optional)
  - Leave as "All branches" to allow tag-based releases

### 3. Save

Click **Save protection rules**

## That's It!

The workflow is already created in `.github/workflows/release.yml`. Once you've set up the `release` environment with required reviewers, the authorization enforcement is active.

## Testing the Setup

1. **Create a test tag locally:**
   ```bash
   git tag test-1.0.0
   git push origin test-1.0.0
   ```

2. **Check GitHub Actions:**
   - Go to **Actions** tab in your repository
   - You should see a workflow run waiting for approval

3. **Approve the test release:**
   - Click on the workflow run
   - Click **Review deployments**
   - Select `release` environment
   - Click **Approve and deploy**

4. **Clean up test:**
   ```bash
   # Delete the test release on GitHub (via web interface)
   # Delete the test tag
   git tag -d test-1.0.0
   git push origin --delete test-1.0.0
   ```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Environment not found" error | Create `release` environment in Settings → Environments |
| Can't approve deployments | Ask repo admin to add you as required reviewer |
| Workflow doesn't trigger | Check tag matches pattern: `1.2.3`, `alpha-1.2.3`, etc. |

## Who Can Do What

| Action | Who |
|--------|-----|
| Create environment | Repository admin |
| Add required reviewers | Repository admin |
| Push tags | Anyone with write access |
| Approve releases | Required reviewers only |
| Complete release | Automatic after approval |

## See Also

- [service-side-authorization.md](service-side-authorization.md) - Detailed documentation
- [developer-commands.md](developer-commands.md) - Developer CLI usage
- [GitHub Environments Docs](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
