#!/bin/bash

# PaperKit Base Installation Script
# Version: 2.2.0
# Installs PaperKit to specified directory

set -e

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
INSTALL_DIR=""
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
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Get installation directory from user
get_install_directory() {
    echo ""
    echo -e "${BOLD}Installation Location${NC}"
    echo ""
    echo "Where would you like to install PaperKit?"
    echo ""
    echo -e "  ${CYAN}1)${NC} Current directory: $(pwd)"
    echo -e "  ${CYAN}2)${NC} Home directory: ${HOME}/paperkit"
    echo -e "  ${CYAN}3)${NC} Custom path (you specify)"
    echo ""
    read -p "Selection [1]: " location_choice
    location_choice=${location_choice:-1}
    
    case $location_choice in
        1)
            INSTALL_DIR="$(pwd)/paperkit"
            ;;
        2)
            INSTALL_DIR="${HOME}/paperkit"
            ;;
        3)
            echo ""
            read -p "Enter installation path: " custom_path
            if [ -z "$custom_path" ]; then
                error_exit "Installation path cannot be empty"
            fi
            # Expand ~ to home directory
            custom_path="${custom_path/#\~/$HOME}"
            INSTALL_DIR="$custom_path"
            ;;
        *)
            error_exit "Invalid selection"
            ;;
    esac
    
    # Create parent directory if it doesn't exist
    local parent_dir=$(dirname "$INSTALL_DIR")
    if [ ! -d "$parent_dir" ]; then
        warning_msg "Parent directory does not exist: $parent_dir"
        read -p "Create it? [Y/n]: " create_parent
        create_parent=${create_parent:-Y}
        if [[ "$create_parent" =~ ^[Yy]$ ]]; then
            mkdir -p "$parent_dir" || error_exit "Failed to create parent directory"
        else
            error_exit "Cannot proceed without parent directory"
        fi
    fi
    
    echo ""
    info_msg "Installing to: ${INSTALL_DIR}"
    echo ""
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

# Detect platform
detect_platform() {
    info_msg "Detecting platform..."
    local os_type="unknown"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        os_type="Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        os_type="macOS"
    elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        os_type="Windows (via $OSTYPE)"
        warning_msg "You are running on Windows. For best experience, use WSL (Windows Subsystem for Linux)."
        echo ""
        echo -e "${CYAN}Windows Users:${NC}"
        echo "  • Recommended: Windows Subsystem for Linux (WSL) - provides a full Linux environment"
        echo "  • Alternative: Git Bash (included with Git for Windows)"
        echo "  • Once installed, open your bash terminal and rerun this script"
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
    
    # Python3 (recommended for tools)
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

# Check for existing installation
check_existing_installation() {
    if [ -d "$INSTALL_DIR" ]; then
        echo ""
        warning_msg "PaperKit is already installed at $INSTALL_DIR"
        echo ""
        echo -e "${BOLD}What would you like to do?${NC}"
        echo ""
        echo -e "  ${CYAN}1)${NC} Update (pull latest changes, preserve your work)"
        echo -e "  ${CYAN}2)${NC} Backup and reinstall (creates backup, fresh install)"
        echo -e "  ${CYAN}3)${NC} Cancel installation"
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

# Create backup of existing installation
create_backup() {
    local timestamp=$(date +%Y%m%d_%H%M%S)
    BACKUP_DIR="${INSTALL_DIR}_backup_${timestamp}"
    
    info_msg "Creating backup..."
    echo "  From: $INSTALL_DIR"
    echo "  To:   $BACKUP_DIR"
    
    if cp -r "$INSTALL_DIR" "$BACKUP_DIR"; then
        success_msg "Backup created successfully"
        
        # Remove old installation
        info_msg "Removing old installation..."
        rm -rf "$INSTALL_DIR"
        success_msg "Old installation removed"
    else
        error_exit "Failed to create backup"
    fi
}

# Update existing installation
update_installation() {
    cd "$INSTALL_DIR"
    
    info_msg "Checking for local changes..."
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        warning_msg "You have local changes. Stashing them before update..."
        git stash save "Auto-stash before PaperKit update $(date +%Y%m%d_%H%M%S)"
        echo ""
        info_msg "Your changes have been stashed. After update, you can restore them with:"
        echo "  cd $INSTALL_DIR"
        echo "  git stash pop"
        echo ""
        read -p "Press Enter to continue with update..."
    fi
    
    info_msg "Pulling latest changes..."
    if git pull origin master; then
        success_msg "Installation updated successfully"
        
        # Regenerate IDE files if needed
        if [ -x "./paperkit" ]; then
            info_msg "Regenerating IDE integration files..."
            ./paperkit generate || warning_msg "Generation had issues but update continues"
        fi
        
        show_update_completion
        exit 0
    else
        error_exit "Failed to update installation"
    fi
}

# Clone repository
clone_repository() {
    info_msg "Cloning PaperKit repository..."
    echo "  From: $REPO_URL"
    echo "  To:   $INSTALL_DIR"
    echo ""
    
    if git clone "$REPO_URL" "$INSTALL_DIR"; then
        success_msg "Repository cloned successfully"
        cd "$INSTALL_DIR"
    else
        error_exit "Failed to clone repository"
    fi
}

# IDE selection with fzf (interactive multi-select)
select_ides_fzf() {
    info_msg "Select IDE integrations (TAB to select, ENTER to confirm):"
    echo ""
    
    local options="GitHub Copilot (VS Code)
OpenAI Codex
Both (recommended)
None (core only)"
    
    local selection=$(echo "$options" | fzf --multi --header="Select IDE(s) - TAB to toggle, ENTER to confirm" \
        --preview="echo 'Selected: {}'" \
        --height=10 \
        --reverse \
        --bind="tab:toggle" \
        --marker="✓" \
        --prompt="IDE> ")
    
    if [[ -z "$selection" ]]; then
        warning_msg "No IDE selected. Installing core only."
        return
    fi
    
    while IFS= read -r line; do
        case "$line" in
            *"GitHub Copilot"*)
                SELECTED_IDES+=("copilot")
                ;;
            *"OpenAI Codex"*)
                SELECTED_IDES+=("codex")
                ;;
            *"Both"*)
                SELECTED_IDES=("copilot" "codex")
                break
                ;;
            *"None"*)
                SELECTED_IDES=()
                break
                ;;
        esac
    done <<< "$selection"
}

# IDE selection fallback (numbered menu)
select_ides_menu() {
    echo ""
    echo -e "${BOLD}Select IDE integration(s):${NC}"
    echo ""
    echo -e "  ${CYAN}1)${NC} GitHub Copilot (VS Code chat modes)"
    echo -e "  ${CYAN}2)${NC} OpenAI Codex (prompt library)"
    echo -e "  ${CYAN}3)${NC} Both (recommended)"
    echo -e "  ${CYAN}4)${NC} None (core .paperkit system only)"
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

# Run post-install setup
run_post_install_setup() {
    info_msg "Running post-installation setup..."
    
    # Run the paperkit init command if available
    if [ -x "./paperkit" ]; then
        # Create a temporary response file to automate the installer
        # Using mktemp for secure temporary file creation instead of PID-based naming
        local temp_response
        temp_response=$(mktemp "/tmp/paperkit_install_response.XXXXXX")
        
        # Ensure cleanup on exit or interruption
        trap 'rm -f "$temp_response"' EXIT INT TERM
        
        # Prepare responses based on selected IDEs
        case "${#SELECTED_IDES[@]}" in
            0)
                echo "4" > "$temp_response"  # None
                ;;
            1)
                if [[ " ${SELECTED_IDES[*]} " =~ " copilot " ]]; then
                    echo "1" >> "$temp_response"  # Copilot
                else
                    echo "2" >> "$temp_response"  # Codex
                fi
                ;;
            *)
                echo "3" > "$temp_response"  # Both
                ;;
        esac
        echo "yes" >> "$temp_response"  # Confirm directory
        echo "yes" >> "$temp_response"  # Continue with non-empty directory
        echo "2" >> "$temp_response"    # Skip Python venv setup (user can do later)
        
        # Note: The paperkit-install.sh expects interactive input
        # For now, we'll just notify the user to run it manually
        # Trap handler will clean up temp file on function exit
        
        info_msg "Generating IDE integration files..."
        if [ ${#SELECTED_IDES[@]} -gt 0 ]; then
            for ide in "${SELECTED_IDES[@]}"; do
                ./paperkit generate --target="$ide" || warning_msg "Generation for $ide had issues"
            done
        fi
    else
        warning_msg "paperkit command not found, skipping automated setup"
    fi
}

# Show completion message
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
    info_msg "Installed components:"
    echo "  • Core .paperkit/ structure"
    echo "  • LaTeX document structure"
    echo "  • Planning directory"
    
    if [[ " ${SELECTED_IDES[*]} " =~ " copilot " ]]; then
        echo "  • GitHub Copilot agents (.github/agents/)"
    fi
    
    if [[ " ${SELECTED_IDES[*]} " =~ " codex " ]]; then
        echo "  • OpenAI Codex prompts (.codex/prompts/)"
    fi
    
    echo ""
    info_msg "Next steps:"
    echo -e "  1. Navigate to PaperKit: ${CYAN}cd $INSTALL_DIR${NC}"
    echo -e "  2. Review available agents: ${CYAN}cat AGENTS.md${NC}"
    echo "  3. (Optional) Set up Python environment:"
    echo -e "     ${CYAN}python3 -m venv .venv${NC}"
    echo -e "     ${CYAN}source .venv/bin/activate${NC}"
    echo -e "     ${CYAN}pip install -r requirements.txt${NC}"
    echo "  4. Open your IDE (VS Code for Copilot, etc.)"
    echo "  5. Select 'paper-architect' to begin your paper"
    echo ""
    
    info_msg "To regenerate IDE files after editing .paperkit/ agents:"
    echo -e "  ${CYAN}cd $INSTALL_DIR${NC}"
    echo -e "  ${CYAN}./paperkit generate${NC}"
    
    echo ""
    info_msg "For more information, see:"
    echo "  • README.md - Quick start guide"
    echo "  • INSTALL-INSTRUCTIONS.md - Detailed installation guide"
    echo "  • AGENTS.md - Agent reference"
    echo ""
}

# Show update completion message
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
    info_msg "If you had local changes, they were stashed. To restore them:"
    echo -e "  ${CYAN}cd $INSTALL_DIR${NC}"
    echo -e "  ${CYAN}git stash pop${NC}"
    echo ""
}

# Main installation
main() {
    show_banner
    
    # Get installation directory first
    get_install_directory
    
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

main "$@"
