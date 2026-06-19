# PaperKit Installation Scripts

This directory contains installation scripts for PaperKit.

## Installation Entry Points

User-facing setup should normally go through `./paperkit init` from the repository root.

This directory contains the bootstrap and implementation scripts behind that CLI:

- `base-install.sh` - Remote bootstrap installer for `~/paperkit`
- `paperkit-install.sh` - Bash installer invoked by `./paperkit init`

## Base Installation Script

### `base-install.sh`

The main installation script that installs PaperKit to `~/paperkit`.

**Usage:**

```bash
# Remote installation (recommended)
curl -sSL https://raw.githubusercontent.com/peternicholls/PaperKit/master/scripts/base-install.sh | bash

# Or download and run locally
wget https://raw.githubusercontent.com/peternicholls/PaperKit/master/scripts/base-install.sh
chmod +x base-install.sh
./base-install.sh
```

**Features:**

- ✓ Installs to standard location (`~/paperkit`)
- ✓ Detects existing installations
- ✓ Offers update or backup options
- ✓ Automatic backup with timestamps
- ✓ Stashes local changes during updates
- ✓ Platform detection (macOS, Linux, Windows)
- ✓ Prerequisite checking
- ✓ IDE selection (GitHub Copilot, OpenAI Codex, both, or none)
- ✓ Automatic IDE file generation
- ✓ WSL guidance for Windows users

**What it does:**

1. **First Installation:**
   - Clones the PaperKit repository to `~/paperkit`
   - Prompts for IDE integrations
   - Generates IDE-specific files
   - Provides next steps

2. **Update Existing Installation:**
   - Detects existing `~/paperkit` directory
   - Offers three options:
     - Update: Pull latest changes (preserves your work)
     - Backup and reinstall: Creates timestamped backup, then fresh install
     - Cancel: Exit without changes
   - Stashes uncommitted changes before update
   - Regenerates IDE files after update
   - Provides instructions to restore stashed changes

3. **Backup Creation:**
   - Creates timestamped backup: `~/paperkit_backup_YYYYMMDD_HHMMSS`
   - Preserves all your work
   - Allows fresh installation

**Platform Support:**

- **macOS**: Native support (Intel and Apple Silicon)
- **Linux**: Native support (all distributions)
- **Windows**: Via WSL only

**Prerequisites:**

- Bash shell
- Git
- curl (for remote installation)

**Optional:**

- Python 3.7+ (for validation tools)
- fzf (for enhanced IDE selection)
- LaTeX distribution (for PDF compilation)

## Repository Installer Scripts

### `paperkit-install.sh`

This is the bash installer used internally by `./paperkit init`.

## Testing

To test the script without running it:

```bash
# Syntax check
bash -n scripts/base-install.sh

# Dry run (review the script)
less scripts/base-install.sh
```

## Maintenance

When updating the script:

1. Test syntax: `bash -n scripts/base-install.sh`
2. Test locally in a clean environment
3. Verify all functions work correctly
4. Update version number in the script
5. Commit changes
6. Test remote installation from GitHub

## Version History

- **v2.1.0** (Current)
  - Added base installation to `~/paperkit`
  - Added update detection
  - Added backup functionality
   - Added WSL guidance for Windows users
  - Added automatic stashing of local changes

- **v2.0.0**
  - IDE selection
  - Platform detection
  - Prerequisite checking
