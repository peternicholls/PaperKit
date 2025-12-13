#!/bin/bash

# PaperKit Installer
# Version: alpha-1.0.0
# Installs the Research Paper Assistant Kit into the current directory

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Display banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║             📝 PaperKit Installer                 ║
║                                                   ║
║    Research Paper Assistant Kit                   ║
║    Version: alpha-1.0.0                           ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Function to display error and exit
error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    exit 1
}

# Function to display success
success_msg() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to display warning
warning_msg() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to display info
info_msg() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check 1: Verify user is in a directory (not root)
info_msg "Checking installation directory..."
CURRENT_DIR=$(pwd)
if [ "$CURRENT_DIR" = "/" ]; then
    error_exit "Cannot install in root directory. Please navigate to your project directory first."
fi
success_msg "Directory check passed: $CURRENT_DIR"

# Check 2: Confirm with user that this is the right directory
echo ""
echo -e "${YELLOW}You are about to install PaperKit in:${NC}"
echo -e "${BLUE}$CURRENT_DIR${NC}"
echo ""
read -p "Is this the correct directory? (yes/no): " confirm

if [[ ! "$confirm" =~ ^[Yy][Ee][Ss]$ ]]; then
    warning_msg "Installation cancelled by user."
    exit 0
fi

# Check 3: Warn if directory is not empty
if [ "$(ls -A)" ]; then
    warning_msg "This directory is not empty."
    echo "Existing files:"
    ls -1 | head -10
    if [ $(ls -1 | wc -l) -gt 10 ]; then
        echo "... and more"
    fi
    echo ""
    read -p "Continue installation anyway? (yes/no): " continue_install
    if [[ ! "$continue_install" =~ ^[Yy][Ee][Ss]$ ]]; then
        warning_msg "Installation cancelled by user."
        exit 0
    fi
fi

# Check 4: Verify required commands are available
info_msg "Checking for required dependencies..."

# Check for bash (we're already in bash, but verify version)
if ! command -v bash &> /dev/null; then
    error_exit "Bash is required but not found."
fi
success_msg "Bash: $(bash --version | head -n1)"

# Check for git (recommended)
if command -v git &> /dev/null; then
    success_msg "Git: $(git --version)"
else
    warning_msg "Git not found. Some features may be limited."
fi

# Check for python3 (recommended)
if command -v python3 &> /dev/null; then
    success_msg "Python3: $(python3 --version)"
else
    warning_msg "Python3 not found. Some tools may not work."
fi

# Check for node (optional)
if command -v node &> /dev/null; then
    success_msg "Node.js: $(node --version)"
else
    info_msg "Node.js not found (optional)."
fi

# Check 5: Detect platform
info_msg "Detecting platform..."
OS_TYPE="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macOS"
elif [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS_TYPE="Windows (via $OSTYPE)"
else
    OS_TYPE="$OSTYPE"
fi
success_msg "Platform detected: $OS_TYPE"

# Determine installation method
echo ""
info_msg "Determining installation method..."

# Check if we're in a git repository that might be paperkit
if [ -d ".git" ] && [ -f "AGENTS.md" ] && [ -f "VERSION" ]; then
    info_msg "Detected existing PaperKit installation in current directory."
    read -p "Reinitialize this installation? (yes/no): " reinit
    if [[ ! "$reinit" =~ ^[Yy][Ee][Ss]$ ]]; then
        info_msg "Using existing installation."
        exit 0
    fi
fi

# Check if paperkit files exist in current directory
if [ -f "VERSION" ] || [ -d ".paper" ]; then
    warning_msg "PaperKit files detected in current directory."
    read -p "This may be an existing installation. Continue anyway? (yes/no): " continue_anyway
    if [[ ! "$continue_anyway" =~ ^[Yy][Ee][Ss]$ ]]; then
        warning_msg "Installation cancelled."
        exit 0
    fi
fi

# Main installation logic
echo ""
info_msg "Starting installation..."

# For now, this is a placeholder for actual file copying/downloading
# In a real implementation, this would:
# 1. Download or copy PaperKit files
# 2. Set up directory structure
# 3. Initialize configuration
# 4. Set permissions

warning_msg "Installation script is in alpha stage."
info_msg "This installer currently validates prerequisites and directory setup."
info_msg "Full installation logic will be implemented in subsequent versions."

# Create basic directory structure
info_msg "Creating directory structure..."
mkdir -p .paper/data/output-drafts
mkdir -p .paper/data/output-refined
mkdir -p .paper/data/output-final
mkdir -p latex/sections
mkdir -p latex/references
mkdir -p planning

success_msg "Basic directory structure created."

# Final success message
echo ""
echo -e "${GREEN}"
cat << "EOF"
╔═══════════════════════════════════════════════════╗
║                                                   ║
║         ✓ Installation Complete!                  ║
║                                                   ║
║    PaperKit alpha-1.0.0 is ready to use.         ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

info_msg "Next steps:"
echo "  1. If you have the complete PaperKit bundle, review AGENTS.md for available agents"
echo "  2. Open GitHub Copilot or Codex in your IDE"
echo "  3. Use paper-architect to begin your research paper"
echo ""
info_msg "Note: This alpha installer creates the directory structure."
info_msg "Ensure you have the complete PaperKit files (.paper/, .github/, etc.) in this directory."
echo ""
