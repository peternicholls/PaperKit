# Service-Side Release Authorization

## Overview

To prevent unauthorized releases, PaperKit uses GitHub's **Environment Protection Rules** to enforce authorization server-side. This ensures that even if someone bypasses the local authorization checks in `./paperkit-dev`, they cannot create an actual release without proper authorization.

> **Quick Start**: For a condensed setup guide, see [setup-authorization.md](setup-authorization.md)

## How It Works

### Local Authorization (First Line of Defense)

The `./paperkit-dev` script checks your git user.email against an authorized list before allowing version modifications or tag creation. This prevents accidental changes but can be circumvented by editing the script.

### Service-Side Authorization (Enforced by GitHub)

When you push a tag to GitHub, a workflow is triggered that:

1. **Requires approval from authorized users** via GitHub Environment protection rules
2. **Creates the distribution bundle** using the same scripts as local releases
3. **Publishes the GitHub release** with the bundle attached

This server-side enforcement cannot be bypassed, ensuring only authorized personnel can complete a release.

## Setting Up Environment Protection

### Prerequisites

- Repository admin access
- GitHub account with appropriate access:
  - **Public repositories**: Required reviewers available on all GitHub plans (Free, Pro, Team, Enterprise)
  - **Private repositories**: Required reviewers require GitHub Enterprise plan
  
> **Note**: Since PaperKit is a public repository, required reviewers are available without any paid plan.

### Configuration Steps

1. **Navigate to Repository Settings**
   - Go to your repository on GitHub
   - Click **Settings** → **Environments**

2. **Create Release Environment**
   - Click **New environment**
   - Name it: `release`
   - Click **Configure environment**

3. **Add Protection Rules**
   
   Enable the following protections:
   
   - ✅ **Required reviewers**
     - Add authorized users who can approve releases
     - Example: Add repository owner(s)
     - Minimum: 1 reviewer required
   
   - ✅ **Wait timer** (optional)
     - Add a delay before deployment
     - Gives time to review the release
     - Recommended: 0 minutes for most projects
   
   - ✅ **Deployment branches** (optional)
     - Restrict which branches can deploy to this environment
     - Recommended: Leave open for tag-based releases

4. **Save Protection Rules**
   - Click **Save protection rules**

### Example Configuration

```yaml
Environment: release
  Required reviewers:
    - [Add authorized GitHub usernames here]
  
  Wait timer: 0 minutes
  
  Deployment branches: All branches
```

## Release Workflow

### For Authorized Users

1. **Local Development**
   ```bash
   # Make changes, test locally
   ./paperkit-dev version --bump patch
   ```

2. **Create and Push Tag**
   ```bash
   # The paperkit-dev script will create and push the tag
   ./paperkit-dev release --tag
   ```
   
   Or manually:
   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

3. **Approve Release on GitHub**
   - Go to **Actions** tab in GitHub repository
   - Find the pending workflow run
   - Click **Review deployments**
   - Select the `release` environment
   - Click **Approve and deploy**

4. **Automated Completion**
   - GitHub Actions creates the distribution bundle
   - GitHub Release is published automatically
   - Bundle is attached to the release

### For Repository Admins

When you receive a deployment request:

1. **Review the Changes**
   - Check the tag name and version
   - Review recent commits
   - Verify changelog is updated

2. **Approve or Reject**
   - If changes are good: **Approve and deploy**
   - If issues found: **Reject** and provide feedback

## Benefits of Service-Side Enforcement

1. **Tamper-Proof**: Cannot be bypassed by editing local scripts
2. **Audit Trail**: GitHub logs all approvals and deployments
3. **Accountability**: Clear record of who approved each release
4. **Flexibility**: Can add/remove authorized reviewers without code changes
5. **Multiple Approvers**: Can require multiple reviewers for critical releases

## Troubleshooting

### Environment Not Found Error

If you see: `Error: Environment "release" not found`

**Solution**: Create the `release` environment in repository settings as described above.

### No Permission to Approve

If you cannot approve deployments:

**Solution**: Ask a repository admin to add you as a required reviewer for the `release` environment.

### Workflow Stuck in Waiting

If the workflow shows "Waiting for review":

**Solution**: This is expected. An authorized reviewer must approve the deployment before it continues.

### Bypass Protection for Testing

For testing the workflow without environment protection:

1. Temporarily comment out the `environment:` section in `.github/workflows/release.yml`
2. Push a test tag
3. Restore the `environment:` section after testing

**Warning**: Do not leave environment protection disabled in production.

## Comparison: Local vs Service-Side Authorization

| Aspect | Local (`./paperkit-dev`) | Service-Side (GitHub Actions) |
|--------|-------------------------|------------------------------|
| **Can be bypassed** | Yes (edit script) | No (enforced by GitHub) |
| **Audit trail** | Git commits only | Full GitHub deployment log |
| **Multiple approvers** | No | Yes (configurable) |
| **Works offline** | Yes | No (requires GitHub) |
| **Best for** | Quick checks, preventing accidents | Final enforcement, compliance |

## Security Best Practices

1. **Use Both Layers**
   - Keep local authorization for developer convenience
   - Rely on service-side enforcement for security

2. **Limit Reviewers**
   - Only add trusted users as required reviewers
   - Review the list periodically

3. **Monitor Deployments**
   - Check the Actions tab regularly
   - Investigate any unexpected release requests

4. **Keep Reviewers Updated**
   - Remove former team members from reviewer list
   - Add new authorized personnel as needed

5. **Regular Audits**
   - Review environment protection rules quarterly
   - Check deployment history for anomalies

## Related Documentation

- [GitHub Environments Documentation](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment)
- [Release Workflow](release-workflow.md)
- [Developer Commands](developer-commands.md)
