# Release Authorization Flow

This document shows the end-to-end flow for creating a release with service-side authorization enforcement.

## The Two-Layer Authorization Approach

```
┌─────────────────────────────────────────────────────────────────┐
│                    LAYER 1: LOCAL CHECKS                        │
│                  (Developer Convenience)                        │
├─────────────────────────────────────────────────────────────────┤
│  • paperkit-dev script checks git user.email                    │
│  • Prevents accidental changes                                  │
│  • Can be bypassed (not for security)                          │
│  • Provides immediate feedback                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   LAYER 2: SERVICE-SIDE                         │
│                   (Security Enforcement)                        │
├─────────────────────────────────────────────────────────────────┤
│  • GitHub Actions workflow                                      │
│  • Protected environment: "release"                             │
│  • Required reviewers                                           │
│  • Cannot be bypassed                                          │
│  • Audit trail in GitHub                                       │
└─────────────────────────────────────────────────────────────────┘
```

## Complete Release Flow

### Step 1: Developer Creates Version Bump

```bash
# Developer runs locally
./paperkit-dev version --bump patch
```

**What happens:**
- ✅ Local authorization check (Layer 1)
- ✅ Version bumped in config files
- ✅ Git commit created (optional)

### Step 2: Developer Pushes Tag

```bash
# Developer pushes tag
./paperkit-dev release --tag

# Or manually
git tag v1.2.3
git push origin v1.2.3
```

**What happens:**
- ✅ Tag created locally
- ✅ Tag pushed to GitHub
- 🚀 **GitHub Actions workflow triggered**

### Step 3: Workflow Waits for Approval

**On GitHub:**
- ⏳ Workflow starts and reaches environment gate
- ⏳ Waits for required reviewer approval
- 🔔 Reviewers notified

**Status:** Deployment waiting for approval

### Step 4: Authorized User Approves

**Reviewer actions:**
1. Goes to Actions tab on GitHub
2. Clicks on pending workflow run
3. Clicks "Review deployments"
4. Selects `release` environment
5. Clicks "Approve and deploy"

**What happens:**
- ✅ Approval recorded in GitHub audit log
- 🚀 Workflow continues

### Step 5: Automated Release Creation

**GitHub Actions performs:**
1. ✅ Validates tag format
2. ✅ Verifies version consistency
3. ✅ Creates distribution bundle
4. ✅ Generates release notes
5. ✅ Creates GitHub Release
6. ✅ Uploads bundle as asset

**Result:** Release published!

## Security Properties

| Property | Local Checks | Service-Side |
|----------|--------------|--------------|
| **Prevents accidents** | ✅ Yes | ✅ Yes |
| **Tamper-proof** | ❌ No | ✅ Yes |
| **Audit trail** | Partial (git) | ✅ Full (GitHub) |
| **Multi-approver** | ❌ No | ✅ Yes |
| **Works offline** | ✅ Yes | ❌ No |
| **Revocable** | ❌ No | ✅ Yes |

## Attack Scenarios & Defenses

### Scenario 1: Unauthorized user edits AUTHORIZED_OWNERS

**Attack:** User edits `paperkit-dev` to add their email to `AUTHORIZED_OWNERS`

**Defense:** 
- ❌ Local checks bypassed
- ✅ **Service-side enforcement blocks release**
- Result: Tag pushed but no release created without approval

### Scenario 2: Unauthorized user modifies workflow

**Attack:** User edits `.github/workflows/release.yml` to remove environment

**Defense:**
- ❌ If merged to master, workflow would run without approval
- ✅ **Pull request requires review** (branch protection)
- ✅ **Repository admin sees the change**
- Result: Change blocked at PR review

### Scenario 3: Compromised developer account

**Attack:** Legitimate developer's GitHub account is compromised

**Defense:**
- ⚠️ Attacker can push tags
- ✅ **Still requires approval from another reviewer**
- ✅ **Notification sent to all reviewers**
- Result: Attack detected when unauthorized release requested

### Scenario 4: Social engineering

**Attack:** Attacker tricks reviewer into approving malicious release

**Defense:**
- ⚠️ Human judgment required
- ✅ **Review diff before approving**
- ✅ **Verify requester identity**
- ✅ **Check changelog and release notes**
- Best practice: Never approve without reviewing changes

## Best Practices

### For Developers

1. ✅ Use local checks for fast feedback
2. ✅ Test version bumps before pushing tags
3. ✅ Document changes in CHANGELOG.md
4. ✅ Use `--dry-run` for release previews
5. ✅ Coordinate with team before releases

### For Reviewers

1. ✅ Review git diff before approving
2. ✅ Verify version number is correct
3. ✅ Check CHANGELOG.md is updated
4. ✅ Confirm release timing with team
5. ✅ Never approve without understanding changes

### For Repository Admins

1. ✅ Limit required reviewers to trusted personnel
2. ✅ Enable branch protection on master
3. ✅ Require PR reviews for workflow changes
4. ✅ Monitor Actions tab regularly
5. ✅ Review environment settings quarterly
6. ✅ Remove access when team members leave

## Compliance & Audit

### Audit Trail

Every release approval is logged with:
- ✅ Who requested deployment (tag pusher)
- ✅ Who approved deployment (reviewer)
- ✅ When approval occurred (timestamp)
- ✅ Which environment was deployed to
- ✅ Full workflow run logs

### Accessing Audit Logs

1. **Deployment History:**
   - Settings → Environments → release → View deployment history

2. **Workflow Runs:**
   - Actions → Select workflow → View run details

3. **Repository Audit Log:**
   - Settings → Security → Audit log

### Compliance Benefits

- ✅ Separation of duties (creator ≠ approver)
- ✅ Non-repudiation (GitHub signatures)
- ✅ Tamper-evident (blockchain-backed git)
- ✅ Change tracking (full git history)

## Troubleshooting Decision Tree

```
Release not working?
│
├─ Tag not triggering workflow?
│  ├─ Check tag format matches pattern
│  └─ Verify workflow file exists and is valid
│
├─ Workflow waiting forever?
│  ├─ Check if environment exists
│  └─ Verify required reviewers are set
│
├─ Can't approve deployment?
│  ├─ Check if you're a required reviewer
│  └─ Contact repository admin
│
└─ Workflow failing after approval?
   ├─ Check workflow logs for errors
   ├─ Verify bundle.sh script works
   └─ Check file permissions
```

## Related Documentation

- [setup-authorization.md](setup-authorization.md) - Quick setup guide
- [service-side-authorization.md](service-side-authorization.md) - Detailed documentation
- [developer-commands.md](developer-commands.md) - CLI usage
- [../.github/workflows/README.md](../.github/workflows/README.md) - Workflow documentation
