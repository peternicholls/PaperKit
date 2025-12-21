#!/bin/bash

# PaperKit Base Installation Script
# Version: 2.2.0
# Installs PaperKit to ~/paperkit with backup and update support
# Addresses all code review comments from PR #13

set -e

# Global flag to track if changes were stashed
CHANGES_STASHED=false

# Trap handler for cleanup on interruption
cleanup_on_interrupt() {
    echo ""
    warning_msg "Installation interrupted by user."
    if [ -n "$BACKUP_DIR" ] && [ -d "$BACKUP_DIR" ]; then
        warning_msg "Partial backup may exist at: $BACKUP_DIR"
        warning_msg "Please verify and clean up manually if needed."
    fi
    exit 130
}

# Set up trap for interruption signals
trap cleanup_on_interrupt INT TERM

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'
BOLD='\033[1m'

# Global variables
VERSION="2.2.0"
INSTALL_DIR="${HOME}/paperkit"
REPO_URL="https://github.com/peternicholls/PaperKit"
BACKUP_DIR=""
SELECTED_IDES=()

# Display banner
show_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║             📝 PaperKit Installer                 ║
║                                                   ║
║    Research Paper Assistant Kit v2.2.0            ║
║    Installing to ~/paperkit                       ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Utility functions
error_exit() { echo -e "${RED}❌ Error: $1${NC}" >&2; exit 1; }
success_msg() { echo -e "${GREEN}✓ $1${NC}"; }
warning_msg() { echo -e "${YELLOW}⚠ $1${NC}"; }
info_msg() { echo -e "${BLUE}ℹ $1${NC}"; }

# Check if fzf is available
has_fzf() {
    command -v fzf &> /dev/null
}

# Detect platform with WSL detection (Comment #19)
detect_platform() {
    info_msg "Detecting platform..."
    local os_type="unknown"
    local is_wsl="false"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Check for WSL
        if [[ -f /proc/version ]] && grep -qiE 'microsoft|wsl' /proc/version 2>/dev/null; then
            is_wsl="true"
            os_type="WSL (Linux)"
            info_msg "Detected Windows Subsystem for Linux (WSL). PaperKit will be installed as on a Linux system."
        else
            os_type="Linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        os_type="macOS"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        os_type="Windows (via $OSTYPE)"
        warning_msg "You are running on Windows."
        echo ""
        echo -e "${CYAN}Windows Users:${NC}"
        echo "  • Recommended: Windows Subsystem for Linux (WSL) - provides a full Linux environment"
        echo "  • Alternative: Git Bash (included with Git for Windows)"
        echo "  • If you are already running this script from WSL or Git Bash, you can continue the installation."
        echo "  • Otherwise, install WSL or Git Bash first, then run this script from that environment."
        echo ""
    else
        os_type="$OSTYPE"
    fi
    
    success_msg "Platform: $os_type"
}

# Check prerequisites
check_prerequisites() {
    info_msg "Checking prerequisites..."
    
    # Bash version
    if ! command -v bash &> /dev/null; then
        error_exit "Bash is required but not found."
    fi
    success_msg "Bash: $(bash --version | head -n1 | cut -d' ' -f1-4)"
    
    # Git (required for clone)
    if ! command -v git &> /dev/null; then
        error_exit "Git is required but not found. Please install Git first."
    fi
    success_msg "Git: $(git --version | cut -d' ' -f3)"
    
    # curl (should be available if we got here)
    if command -v curl &> /dev/null; then
        success_msg "curl: available"
    fi
    
    # Python3 (recommended for tools) - Comment #3: Aligned to 3.8+
    if command -v python3 &> /dev/null; then
        local py_version=$(python3 --version | cut -d' ' -f2)
        success_msg "Python3: $py_version"
    else
        warning_msg "Python3 not found. Some tools may not work."
    fi
    
    # LaTeX (optional)
    if command -v pdflatex &> /dev/null; then
        success_msg "pdflatex: available"
    else
        info_msg "pdflatex not found (optional - install TeX Live for PDF compilation)"
    fi
}

# Check for existing installation with validation (Comment #9)
check_existing_installation() {
    if [ -d "$INSTALL_DIR" ]; then
        # Verify that this looks like a valid PaperKit installation before offering update options
        if [ ! -d "$INSTALL_DIR/.git" ] && [ ! -f "$INSTALL_DIR/VERSION" ]; then
            warning_msg "Directory $INSTALL_DIR exists but does not appear to be a PaperKit installation."
            warning_msg "Skipping update options; proceeding as if this is a fresh installation."
            return 1  # Treat as no existing PaperKit installation
        fi
        
        echo ""
        warning_msg "PaperKit is already installed at $INSTALL_DIR"
        echo ""
        echo -e "${BOLD}What would you like to do?${NC}"
        echo ""
        echo "  ${CYAN}1)${NC} Update (pull latest changes, preserve your work)"
        echo "  ${CYAN}2)${NC} Backup and reinstall (creates backup, fresh install)"
        echo "  ${CYAN}3)${NC} Cancel installation"
        echo ""
        
        read -p "Selection [1]: " choice
        choice=${choice:-1}
        
        case $choice in
            1)
                info_msg "Updating existing installation..."
                return 0  # Continue with update
                ;;
            2)
                create_backup
                return 1  # Continue with fresh install after backup
                ;;
            3)
                info_msg "Installation cancelled."
                exit 0
                ;;
            *)
                warning_msg "Invalid choice. Defaulting to update."
                return 0
                ;;
        esac
    fi
    return 1  # No existing installation
}

# Create backup of existing installation with unique naming (Comment #20, #22)
create_backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    
    # Use mktemp for guaranteed unique directory name
    if ! BACKUP_DIR=$(mktemp -d "${INSTALL_DIR}_backup_${timestamp}_XXXXXX" 2>/dev/null); then
        # Fallback if mktemp fails
        BACKUP_DIR="${INSTALL_DIR}_backup_${timestamp}"
    fi
    
    info_msg "Creating backup..."
    echo "  From: $INSTALL_DIR"
    echo "  To:   $BACKUP_DIR"
    
    # Use cp -a to preserve symlinks, permissions, and timestamps (Comment #22)
    if cp -a "$INSTALL_DIR" "$BACKUP_DIR"; then
        success_msg "Backup created successfully"
        
        # Comment #8: Add safety checks before rm -rf
        if [ -n "$INSTALL_DIR" ] && [ "$INSTALL_DIR" != "$HOME" ] && [ "$INSTALL_DIR" != "/" ]; then
            info_msg "Removing old installation..."
            rm -rf "$INSTALL_DIR"
            success_msg "Old installation removed"
        else
            error_exit "Safety check failed: refusing to remove $INSTALL_DIR"
        fi
    else
        error_exit "Failed to create backup"
    fi
}

# Update existing installation (Comments #6, #7, #13, #15, #16)
update_installation() {
    # Comment #15: Validate directory exists and is a git repository
    if [ ! -d "$INSTALL_DIR" ]; then
        error_exit "Installation directory '$INSTALL_DIR' does not exist. Please reinstall PaperKit."
    fi

    if [ ! -d "$INSTALL_DIR/.git" ]; then
        error_exit "Installation directory '$INSTALL_DIR' is not a valid Git repository. Please backup and reinstall PaperKit."
    fi

    # Change to installation directory with error handling
    if ! cd "$INSTALL_DIR"; then
        error_exit "Failed to change directory to '$INSTALL_DIR'. Please check permissions and try again."
    fi
    
    # Comment #6: Check for both uncommitted changes and untracked files
    info_msg "Checking for local changes..."
    local status_output
    status_output="$(git status --porcelain 2>/dev/null || true)"
    if [ -n "$status_output" ]; then
        warning_msg "You have local changes (including possible untracked files). Stashing them before update..."
        # Comment #13: Use git stash push instead of deprecated git stash save
        git stash push -u -m "Auto-stash before PaperKit update $(date +%Y%m%d_%H%M%S)"
        CHANGES_STASHED=true
        echo ""
        info_msg "Your changes have been stashed. After update, you can restore them with:"
        echo "  cd $INSTALL_DIR"
        echo "  git stash pop"
        echo ""
        read -p "Press Enter to continue with update..."
    fi
    
    # Comment #16: Auto-detect repository default branch instead of hardcoding "main"
    local branch_to_pull
    local current_branch
    local default_branch

    if current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) && [ "$current_branch" != "HEAD" ]; then
        branch_to_pull="$current_branch"
    else
        default_branch=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's@^origin/@@')
        if [ -n "$default_branch" ]; then
            branch_to_pull="$default_branch"
        else
            # Fallback to 'main' to maintain previous behavior if detection fails
            branch_to_pull="main"
        fi
    fi
    
    info_msg "Pulling latest changes from branch '$branch_to_pull'..."
    if git pull origin "$branch_to_pull"; then
        success_msg "Installation updated successfully"
        
        # Regenerate IDE files if needed
        if [ -x "./paperkit" ]; then
            info_msg "Regenerating IDE integration files..."
            ./paperkit generate || warning_msg "Generation had issues but update continues"
        fi
        
        show_update_completion
        exit 0
    else
        # Comment #7: Provide recovery instructions on failed git pull
        error_exit "Failed to update installation.
If you had stashed changes, you can restore them with:
  cd $INSTALL_DIR
  git stash pop

Please resolve any conflicts manually and try again."
    fi
}

# Clone repository with retry logic and cleanup (Comments #1, #4, #21)
clone_repository() {
    info_msg "Cloning PaperKit repository..."
    echo "  From: $REPO_URL"
    echo "  To:   $INSTALL_DIR"
    echo ""
    
    local max_retries=3
    local attempt=1

    while [ "$attempt" -le "$max_retries" ]; do
        if git clone "$REPO_URL" "$INSTALL_DIR"; then
            success_msg "Repository cloned successfully"
            # Comment #21: Explicit error handling for cd command
            if ! cd "$INSTALL_DIR"; then
                error_exit "Failed to change directory to '$INSTALL_DIR'. Please check permissions."
            fi
            return 0
        fi

        # Comment #1: Clean up partially-created directory on clone failure
        if [ -d "$INSTALL_DIR" ]; then
            warning_msg "Clone failed; removing partially created directory at $INSTALL_DIR"
            rm -rf "$INSTALL_DIR"
        fi

        warning_msg "Failed to clone repository (attempt $attempt of $max_retries)."
        warning_msg "This is often caused by network connectivity issues or a temporary problem reaching:"
        echo "  $REPO_URL"

        if [ "$attempt" -lt "$max_retries" ]; then
            echo ""
            info_msg "Please check your internet connection. The script will retry."
            read -p "Press Enter to retry now, or Ctrl+C to abort... " _
            attempt=$((attempt + 1))
            echo ""
        else
            error_exit "Failed to clone repository after $max_retries attempts.
Please:
  - Check your internet connection.
  - Verify that '$REPO_URL' is reachable in your browser or via 'git ls-remote'.
  - If a partial '$INSTALL_DIR' directory was created, remove it before re-running this script.
Then re-run this installation script to try again."
        fi
    done
}

# IDE selection with fzf (Comment #18: prevent contradictory selections)
select_ides_fzf() {
    info_msg "Select IDE integrations (SPACE to select, ENTER to confirm):"
    echo ""
    
    local options="GitHub Copilot (VS Code)
OpenAI Codex
Both (recommended)
None (core only)"
    
    # Remove --multi to prevent contradictory selections (Comment #18)
    local selection=$(echo "$options" | fzf --header="Select IDE - ENTER to confirm" \
        --preview="echo 'Selected: {}'" \
        --height=10 \
        --reverse \
        --prompt="IDE> ")
    
    if [[ -z "$selection" ]]; then
        warning_msg "No IDE selected. Installing core only."
        return
    fi
    
    case "$selection" in
        *"GitHub Copilot"*)
            SELECTED_IDES=("copilot")
            ;;
        *"OpenAI Codex"*)
            SELECTED_IDES=("codex")
            ;;
        *"Both"*)
            SELECTED_IDES=("copilot" "codex")
            ;;
        *"None"*)
            SELECTED_IDES=()
            ;;
    esac
}

# IDE selection fallback (numbered menu)
select_ides_menu() {
    echo ""
    echo -e "${BOLD}Select IDE integration(s):${NC}"
    echo ""
    echo "  ${CYAN}1)${NC} GitHub Copilot (VS Code chat modes)"
    echo "  ${CYAN}2)${NC} OpenAI Codex (prompt library)"
    echo "  ${CYAN}3)${NC} Both (recommended)"
    echo "  ${CYAN}4)${NC} None (core .paperkit system only)"
    echo ""
    
    while true; do
        read -p "Selection [3]: " choice
        choice=${choice:-3}
        
        case $choice in
            1)
                SELECTED_IDES=("copilot")
                break
                ;;
            2)
                SELECTED_IDES=("codex")
                break
                ;;
            3)
                SELECTED_IDES=("copilot" "codex")
                break
                ;;
            4)
                SELECTED_IDES=()
                break
                ;;
            *)
                warning_msg "Invalid choice. Please enter 1, 2, 3, or 4."
                ;;
        esac
    done
}

# Select IDEs based on available tools
select_ides() {
    if has_fzf; then
        select_ides_fzf
    else
        info_msg "Tip: Install 'fzf' for a better selection experience."
        select_ides_menu
    fi
    
    echo ""
    if [ ${#SELECTED_IDES[@]} -eq 0 ]; then
        info_msg "IDE integrations: None (core only)"
    else
        info_msg "IDE integrations: ${SELECTED_IDES[*]}"
    fi
}

# Run post-install setup (Comment #14, #17)
run_post_install_setup() {
    info_msg "Running post-installation setup..."
    
    # Run the paperkit init command if available
    if [ -x "./paperkit" ]; then
        # Comment #17: Remove dead code for temporary file creation
        # Comment #14: Run generate even when "None" selected
        info_msg "Generating IDE integration files..."
        if [ ${#SELECTED_IDES[@]} -gt 0 ]; then
            for ide in "${SELECTED_IDES[@]}"; do
                ./paperkit generate --target="$ide" || warning_msg "Generation for $ide had issues"
            done
        else
            info_msg "No IDE integrations selected; running default PaperKit generation..."
            ./paperkit generate || warning_msg "Default PaperKit generation had issues"
        fi
    else
        warning_msg "paperkit command not found, skipping automated setup"
    fi
}

# Show completion message (Comment #11)
show_completion() {
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║         ✓ PaperKit Installation Complete!         ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    info_msg "Installation location: ${BOLD}${INSTALL_DIR}${NC}"
    
    if [ -n "$BACKUP_DIR" ]; then
        echo ""
        info_msg "Previous installation backed up to:"
        echo "  $BACKUP_DIR"
    fi
    
    echo ""
    # Comment #11: Clarify which components come from repository vs generated
    info_msg "Components from repository:"
    echo "  • Core .paperkit/ structure"
    echo "  • LaTeX document structure"
    echo "  • Planning directory"
    
    if [ ${#SELECTED_IDES[@]} -gt 0 ]; then
        echo ""
        info_msg "Generated IDE integration files:"
        if [[ " ${SELECTED_IDES[*]} " =~ " copilot " ]]; then
            echo "  • GitHub Copilot agents (.github/agents/)"
        fi
        
        if [[ " ${SELECTED_IDES[*]} " =~ " codex " ]]; then
            echo "  • OpenAI Codex prompts (.codex/prompts/)"
        fi
    fi
    
    echo ""
    info_msg "Next steps:"
    echo "  1. Navigate to PaperKit: ${CYAN}cd $INSTALL_DIR${NC}"
    echo "  2. Review available agents: ${CYAN}cat AGENTS.md${NC}"
    echo "  3. (Optional) Set up Python environment:"
    echo "     ${CYAN}python3 -m venv .venv${NC}"
    echo "     ${CYAN}source .venv/bin/activate${NC}"
    echo "     ${CYAN}pip install -r requirements.txt${NC}"
    echo "  4. Open your IDE (VS Code for Copilot, etc.)"
    echo "  5. Select 'paper-architect' to begin your paper"
    echo ""
    
    info_msg "To regenerate IDE files after editing .paperkit/ agents:"
    echo "  ${CYAN}cd $INSTALL_DIR${NC}"
    echo "  ${CYAN}./paperkit generate${NC}"
    
    echo ""
    info_msg "For more information, see:"
    echo "  • README.md - Quick start guide"
    echo "  • INSTALL-INSTRUCTIONS.md - Detailed installation guide"
    echo "  • AGENTS.md - Agent reference"
    echo ""
}

# Show update completion message (Comment #10)
show_update_completion() {
    echo ""
    echo -e "${GREEN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║           ✓ PaperKit Update Complete!             ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
    
    info_msg "Installation location: ${BOLD}${INSTALL_DIR}${NC}"
    echo ""
    info_msg "Your PaperKit installation has been updated to the latest version."
    echo ""
    
    # Comment #10: Only show stash message if changes were actually stashed
    if [ "$CHANGES_STASHED" = true ]; then
        info_msg "Your local changes were stashed. To restore them:"
        echo "  ${CYAN}cd $INSTALL_DIR${NC}"
        echo "  ${CYAN}git stash pop${NC}"
        echo ""
    fi
}

# Main installation (Comment #12: no arguments supported currently)
main() {
    show_banner
    
    echo ""
    detect_platform
    
    echo ""
    check_prerequisites
    
    # Check for existing installation
    if check_existing_installation; then
        # User chose to update
        update_installation
        # This will exit, so code below won't run
    fi
    
    # Fresh installation (or after backup)
    clone_repository
    
    echo ""
    select_ides
    
    echo ""
    run_post_install_setup
    
    show_completion
}

main
