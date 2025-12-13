# PaperKit Installer for Windows
# Version: alpha-1.0.0
# Installs the Research Paper Assistant Kit into the current directory

# Set error action preference
$ErrorActionPreference = "Stop"

# Display banner
Write-Host @"

╔═══════════════════════════════════════════════════╗
║                                                   ║
║             📝 PaperKit Installer                 ║
║                                                   ║
║    Research Paper Assistant Kit                   ║
║    Version: alpha-1.0.0                           ║
║                                                   ║
╚═══════════════════════════════════════════════════╝

"@ -ForegroundColor Blue

# Function to display error and exit
function Exit-WithError {
    param([string]$Message)
    Write-Host "❌ Error: $Message" -ForegroundColor Red
    exit 1
}

# Function to display success
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

# Function to display warning
function Write-Warning-Custom {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

# Function to display info
function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Cyan
}

# Check 1: Verify user is in a directory (not root)
Write-Info "Checking installation directory..."
$currentDir = Get-Location
if ($currentDir.Path -match '^[A-Z]:\\$') {
    Exit-WithError "Cannot install in root directory. Please navigate to your project directory first."
}
Write-Success "Directory check passed: $currentDir"

# Check 2: Confirm with user that this is the right directory
Write-Host ""
Write-Host "You are about to install PaperKit in:" -ForegroundColor Yellow
Write-Host "$currentDir" -ForegroundColor Blue
Write-Host ""
$confirm = Read-Host "Is this the correct directory? (yes/no)"

if ($confirm -notmatch '^[Yy][Ee][Ss]$') {
    Write-Warning-Custom "Installation cancelled by user."
    exit 0
}

# Check 3: Warn if directory is not empty
$items = Get-ChildItem -Force
if ($items.Count -gt 0) {
    Write-Warning-Custom "This directory is not empty."
    Write-Host "Existing files:"
    $items | Select-Object -First 10 | ForEach-Object { Write-Host "  $($_.Name)" }
    if ($items.Count -gt 10) {
        Write-Host "... and more"
    }
    Write-Host ""
    $continueInstall = Read-Host "Continue installation anyway? (yes/no)"
    if ($continueInstall -notmatch '^[Yy][Ee][Ss]$') {
        Write-Warning-Custom "Installation cancelled by user."
        exit 0
    }
}

# Check 4: Verify required commands are available
Write-Info "Checking for required dependencies..."

# Check for PowerShell version
Write-Success "PowerShell: $($PSVersionTable.PSVersion)"

# Check for git (recommended)
try {
    $gitVersion = git --version
    Write-Success "Git: $gitVersion"
} catch {
    Write-Warning-Custom "Git not found. Some features may be limited."
}

# Check for python (recommended)
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match 'Python') {
        Write-Success "Python: $pythonVersion"
    } else {
        # Try python3
        try {
            $pythonVersion = python3 --version 2>&1
            Write-Success "Python3: $pythonVersion"
        } catch {
            Write-Warning-Custom "Python not found. Some tools may not work."
        }
    }
} catch {
    Write-Warning-Custom "Python not found. Some tools may not work."
}

# Check for node (optional)
try {
    $nodeVersion = node --version
    Write-Success "Node.js: $nodeVersion"
} catch {
    Write-Info "Node.js not found (optional)."
}

# Check 5: Detect platform
Write-Info "Detecting platform..."
$osInfo = [System.Environment]::OSVersion
Write-Success "Platform detected: Windows $($osInfo.Version)"

# Determine installation method
Write-Host ""
Write-Info "Determining installation method..."

# Check if we're in a git repository that might be paperkit
if ((Test-Path ".git") -and (Test-Path "AGENTS.md") -and (Test-Path "VERSION")) {
    Write-Info "Detected existing PaperKit installation in current directory."
    $reinit = Read-Host "Reinitialize this installation? (yes/no)"
    if ($reinit -notmatch '^[Yy][Ee][Ss]$') {
        Write-Info "Using existing installation."
        exit 0
    }
}

# Check if paperkit files exist in current directory
if ((Test-Path "VERSION") -or (Test-Path ".paper")) {
    Write-Warning-Custom "PaperKit files detected in current directory."
    $continueAnyway = Read-Host "This may be an existing installation. Continue anyway? (yes/no)"
    if ($continueAnyway -notmatch '^[Yy][Ee][Ss]$') {
        Write-Warning-Custom "Installation cancelled."
        exit 0
    }
}

# Main installation logic
Write-Host ""
Write-Info "Starting installation..."

# For now, this is a placeholder for actual file copying/downloading
# In a real implementation, this would:
# 1. Download or copy PaperKit files
# 2. Set up directory structure
# 3. Initialize configuration

Write-Warning-Custom "Installation script is in alpha stage."
Write-Info "This installer currently validates prerequisites and directory setup."
Write-Info "Full installation logic will be implemented in subsequent versions."

# Create basic directory structure
Write-Info "Creating directory structure..."
$directories = @(
    ".paper\data\output-drafts",
    ".paper\data\output-refined",
    ".paper\data\output-final",
    "latex\sections",
    "latex\references",
    "planning"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

Write-Success "Basic directory structure created."

# Final success message
Write-Host ""
Write-Host @"

╔═══════════════════════════════════════════════════╗
║                                                   ║
║         ✓ Installation Complete!                  ║
║                                                   ║
║    PaperKit alpha-1.0.0 is ready to use.         ║
║                                                   ║
╚═══════════════════════════════════════════════════╝

"@ -ForegroundColor Green

Write-Info "Next steps:"
Write-Host "  1. If you have the complete PaperKit bundle, review AGENTS.md for available agents"
Write-Host "  2. Open GitHub Copilot or Codex in your IDE"
Write-Host "  3. Use paper-architect to begin your research paper"
Write-Host ""
Write-Info "Note: This alpha installer creates the directory structure."
Write-Info "Ensure you have the complete PaperKit files (.paper/, .github/, etc.) in this directory."
Write-Host ""
