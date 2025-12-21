# PaperKit Developer Commands

## Overview

PaperKit separates user commands from developer/maintainer commands to ensure system integrity and prevent accidental modifications by end users.

## Command Separation

### User Commands: `./paperkit`

For general paper writing workflow:

```bash
./paperkit init          # Initialize new paper project
./paperkit generate      # Generate IDE-specific files
./paperkit validate      # Validate YAML schemas
./paperkit latex         # LaTeX document operations
./paperkit evidence      # Extract evidence from PDFs
./paperkit version       # Show version information
```

### Developer Commands: `./paperkit-dev`

For system development and maintenance:

```bash
./paperkit-dev release   # Create releases, tag versions, bundle distributions
./paperkit-dev version   # Modify version numbers (--bump, --set, --build)
```

## Authorization System

Developer commands require authorization to prevent unauthorized modifications.

### How Authorization Works

1. **Git Email Verification**: The system checks your git user.email configuration
2. **Authorized List**: Only emails in the `AUTHORIZED_OWNERS` array can run dev commands
3. **Automatic Check**: Authorization is verified before any modification operation

### Configure Authorized Users

Edit the `AUTHORIZED_OWNERS` array in `paperkit-dev`:

```bash
# Authorized owners (add git config emails here)
AUTHORIZED_OWNERS=(
    "your-email@example.com"
    "another-dev@example.com"
)
```

### Check Your Git Email

```bash
git config user.email
```

### Set Your Git Email

```bash
git config user.email "your-email@example.com"
```

## Examples

### User Workflow (No Authorization Required)

```bash
# Show current version
./paperkit version

# Show detailed version info
./paperkit version --info

# Build LaTeX document
./paperkit latex --build

# Extract evidence from PDFs
./paperkit evidence --dir research/pdfs --output evidence.md
```

### Developer Workflow (Requires Authorization)

```bash
# Bump patch version (1.2.0 → 1.2.1)
./paperkit-dev version --bump patch

# Set specific version
./paperkit-dev version --set alpha-1.3.0

# Create full release (bundle + tag + push)
./paperkit-dev release --full

# Preview release without making changes
./paperkit-dev release --full --dry-run
```

## Error Messages

### Unauthorized User

If you try to run a dev command without authorization:

```
Error: Unauthorized user.
Current git user: user@example.com
Authorized users: authorized@example.com

Only repository owners can run development commands.
```

**Solution**: Contact a repository owner to add your email to `AUTHORIZED_OWNERS`.

### Git Email Not Configured

If git user.email is not set:

```
Error: Git user.email not configured.
Configure with: git config user.email 'your@email.com'
```

**Solution**: Configure your git email as shown above.

### Command Moved to paperkit-dev

If you try to use a dev command via `./paperkit`:

```
Version modification commands have moved to paperkit-dev
Use: paperkit-dev version --bump patch
```

**Solution**: Use `./paperkit-dev` instead of `./paperkit` for that command.

## Security Rationale

The separation between user and developer commands provides:

1. **Protection**: Prevents accidental version changes or releases
2. **Accountability**: Only authorized maintainers can modify system state
3. **Clarity**: Clear distinction between everyday usage and system maintenance
4. **Safety**: Dry-run modes available for all critical operations

## See Also

- [Release Workflow](release-workflow.md) - Complete release process
- [Release Quick Start](release-quick-start.md) - Quick reference for releases
- [Version System](../README.md) - Version management overview
