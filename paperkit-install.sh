#!/bin/bash

# PaperKit Installer v2
# Version: 2.0.0
# Installs the Research Paper Assistant Kit with IDE selection

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
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION="2.0.0"
SELECTED_IDES=()

# Display banner
show_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║             📝 PaperKit Installer                 ║
║                                                   ║
║    Research Paper Assistant Kit v2.0.0            ║
║    Source of Truth: .paper/                       ║
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
    echo "  ${CYAN}1)${NC} GitHub Copilot (VS Code chat modes)"
    echo "  ${CYAN}2)${NC} OpenAI Codex (prompt library)"
    echo "  ${CYAN}3)${NC} Both (recommended)"
    echo "  ${CYAN}4)${NC} None (core .paper system only)"
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

# Check prerequisites
check_prerequisites() {
    info_msg "Checking prerequisites..."
    
    # Bash version
    if ! command -v bash &> /dev/null; then
        error_exit "Bash is required but not found."
    fi
    success_msg "Bash: $(bash --version | head -n1 | cut -d' ' -f1-4)"
    
    # Git (recommended)
    if command -v git &> /dev/null; then
        success_msg "Git: $(git --version | cut -d' ' -f3)"
    else
        warning_msg "Git not found. Version control features limited."
    fi
    
    # Python3 (recommended for tools)
    if command -v python3 &> /dev/null; then
        success_msg "Python3: $(python3 --version | cut -d' ' -f2)"
    else
        warning_msg "Python3 not found. Some tools may not work."
    fi
    
    # pdftotext (optional, for forensic audit)
    if command -v pdftotext &> /dev/null; then
        success_msg "pdftotext: available (for evidence extraction)"
    else
        info_msg "pdftotext not found (optional - install poppler for PDF extraction)"
    fi
    
    # LaTeX (optional)
    if command -v pdflatex &> /dev/null; then
        success_msg "pdflatex: available"
    else
        info_msg "pdflatex not found (optional - install TeX Live for PDF compilation)"
    fi
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
    else
        os_type="$OSTYPE"
    fi
    
    success_msg "Platform: $os_type"
}

# Create core directory structure
create_core_structure() {
    info_msg "Creating core directory structure..."
    
    # .paper structure (always created)
    mkdir -p .paper/data/output-drafts/sections
    mkdir -p .paper/data/output-drafts/outlines
    mkdir -p .paper/data/output-refined/sections
    mkdir -p .paper/data/output-refined/research
    mkdir -p .paper/data/output-refined/references
    mkdir -p .paper/data/output-final/pdf
    mkdir -p .paper/core/agents
    mkdir -p .paper/specialist/agents
    mkdir -p .paper/_cfg/agents
    mkdir -p .paper/_cfg/workflows
    mkdir -p .paper/_cfg/tools
    mkdir -p .paper/_cfg/guides
    mkdir -p .paper/_cfg/schemas
    mkdir -p .paper/_cfg/ides
    mkdir -p .paper/docs
    
    # LaTeX structure
    mkdir -p latex/sections
    mkdir -p latex/references
    mkdir -p latex/appendices
    
    # Planning
    mkdir -p planning
    
    success_msg "Core structure created"
}

# Install GitHub Copilot integration
install_copilot() {
    info_msg "Installing GitHub Copilot integration..."
    
    mkdir -p .github/agents
    
    # Generate agent files from .paper source
    if [ -x "${SCRIPT_DIR}/paperkit-generate.sh" ]; then
        "${SCRIPT_DIR}/paperkit-generate.sh" --target=copilot
    else
        warning_msg "Generator not found. Creating placeholder agents."
        
        # Create minimal placeholder
        cat > .github/agents/paper-architect.agent.md << 'EOFAGENT'
```chatagent
---
description: "Paper Architect - Design paper structure and outline"
tools: ["changes","edit","fetch","problems","search","runSubagent","usages"]
---

# Paper Architect

<agent-activation CRITICAL="TRUE">
1. LOAD the FULL agent file from @.paper/core/agents/paper-architect.md
2. Execute ALL activation steps
3. Stay in character throughout
</agent-activation>
```
EOFAGENT
    fi
    
    # VS Code settings
    mkdir -p .vscode
    if [ ! -f .vscode/settings.json ]; then
        cat > .vscode/settings.json << 'EOFSETTINGS'
{
    "github.copilot.advanced": {
        "maxRequestsPerSession": 150
    },
    "github.copilot.editor.enableAutoCompletions": true
}
EOFSETTINGS
    fi
    
    success_msg "GitHub Copilot integration installed"
}

# Install OpenAI Codex integration
install_codex() {
    info_msg "Installing OpenAI Codex integration..."
    
    mkdir -p .codex/prompts
    
    # Generate prompt files from .paper source
    if [ -x "${SCRIPT_DIR}/paperkit-generate.sh" ]; then
        "${SCRIPT_DIR}/paperkit-generate.sh" --target=codex
    else
        warning_msg "Generator not found. Creating placeholder prompts."
        
        # Create minimal placeholder
        cat > .codex/prompts/paper-architect.md << 'EOFPROMPT'
# Paper Architect

Activate the **Paper Architect** persona from PaperKit.

## Instructions

1. Load `.paper/core/agents/paper-architect.md`
2. Follow all activation steps
3. Present menu and wait for input
EOFPROMPT
    fi
    
    success_msg "OpenAI Codex integration installed"
}

# Confirm directory
confirm_directory() {
    local current_dir=$(pwd)
    
    if [ "$current_dir" = "/" ]; then
        error_exit "Cannot install in root directory."
    fi
    
    echo ""
    echo -e "${YELLOW}Installation directory:${NC}"
    echo -e "${BOLD}$current_dir${NC}"
    echo ""
    
    read -p "Is this correct? (yes/no): " confirm
    if [[ ! "$confirm" =~ ^[Yy]([Ee][Ss])?$ ]]; then
        warning_msg "Installation cancelled."
        exit 0
    fi
    
    # Warn if not empty
    if [ "$(ls -A 2>/dev/null)" ]; then
        warning_msg "Directory is not empty."
        read -p "Continue anyway? (yes/no): " cont
        if [[ ! "$cont" =~ ^[Yy]([Ee][Ss])?$ ]]; then
            warning_msg "Installation cancelled."
            exit 0
        fi
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
    
    info_msg "Installed components:"
    echo "  • Core .paper/ structure"
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
    echo "  1. Review AGENTS.md for available agents"
    echo "  2. Open your IDE (VS Code for Copilot, etc.)"
    echo "  3. Select 'paper-architect' to begin your paper"
    echo ""
    
    if [ ${#SELECTED_IDES[@]} -gt 0 ]; then
        info_msg "To regenerate IDE files after editing .paper/ agents:"
        echo "  ./paperkit-generate.sh"
    fi
}

# Main installation
main() {
    show_banner
    confirm_directory
    
    echo ""
    check_prerequisites
    
    echo ""
    detect_platform
    
    echo ""
    select_ides
    
    echo ""
    create_core_structure
    
    # Install selected IDE integrations
    for ide in "${SELECTED_IDES[@]}"; do
        echo ""
        case $ide in
            copilot)
                install_copilot
                ;;
            codex)
                install_codex
                ;;
        esac
    done
    
    # Generate IDE files and documentation
    if [ ${#SELECTED_IDES[@]} -gt 0 ]; then
        echo ""
        info_msg "Generating IDE integration files..."
        if [ -f "./paperkit-generate.sh" ]; then
            ./paperkit-generate.sh || warning_msg "Generation had issues but installation continues"
        else
            warning_msg "paperkit-generate.sh not found, skipping file generation"
        fi
    fi
    
    show_completion
}

main "$@"
