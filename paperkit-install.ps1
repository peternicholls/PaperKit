# PaperKit Installer for Windows
# Installs the Research Paper Assistant Kit into the current directory

# Set error action preference
$ErrorActionPreference = "Stop"

# Get version and title from version.yaml
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VersionYamlPath = Join-Path $ScriptDir ".paperkit\_cfg\version.yaml"

$Version = "unknown"
$TitleShort = "PaperKit"
$TitleLong = "Research Paper Assistant"

if (Test-Path $VersionYamlPath) {
    try {
        # Try using Python with PyYAML
        if (Get-Command python -ErrorAction SilentlyContinue) {
            $VersionInfo = python -c @"
import yaml
try:
    with open(r'$VersionYamlPath', 'r') as f:
        data = yaml.safe_load(f)
        version = data.get('version', {})
        print(version.get('current', 'unknown'))
        title = version.get('title', {})
        print(title.get('short', 'PaperKit'))
        print(title.get('long', 'Research Paper Assistant'))
except:
    print('unknown')
    print('PaperKit')
    print('Research Paper Assistant')
"@ 2>$null
            if ($VersionInfo) {
                $Lines = $VersionInfo -split '\r?\n'
                if ($Lines.Length -ge 3) {
                    $Version = $Lines[0]
                    $TitleShort = $Lines[1]
                    $TitleLong = $Lines[2]
                }
            }
        }
    } catch {
        # Fallback to defaults if any error
    }
}

# Display banner
Write-Host @"

╔═══════════════════════════════════════════════════╗
║                                                   ║
║             📝 PaperKit Installer                 ║
║                                                   ║
║    $($TitleLong.PadRight(47))║
║    Version: $($Version.PadRight(37))║
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
        
        # Check for pip
        try {
            $pipVersion = python -m pip --version 2>&1
            if ($pipVersion -match 'pip') {
                Write-Success "pip: available"
            }
        } catch {
            Write-Warning-Custom "pip not found. Install pip for Python package management."
        }
    } else {
        # Try python3
        try {
            $pythonVersion = python3 --version 2>&1
            Write-Success "Python3: $pythonVersion"
            
            # Check for pip3
            try {
                $pipVersion = python3 -m pip --version 2>&1
                if ($pipVersion -match 'pip') {
                    Write-Success "pip3: available"
                }
            } catch {
                Write-Warning-Custom "pip3 not found."
            }
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

# Python virtual environment setup
Write-Host ""
Write-Info "Python environment setup (recommended for validation tools)"
Write-Host ""
Write-Host "Would you like to create a Python virtual environment?"
Write-Host "  1) Yes - Create .venv and install dependencies"
Write-Host "  2) No - Skip (setup later)"
Write-Host ""
$pyChoice = Read-Host "Selection [2]"
if ([string]::IsNullOrEmpty($pyChoice)) { $pyChoice = "2" }

switch ($pyChoice) {
    "1" {
        Write-Info "Creating Python virtual environment..."
        try {
            # Try python first, then python3
            $pythonCmd = "python"
            try {
                & $pythonCmd --version 2>&1 | Out-Null
            } catch {
                $pythonCmd = "python3"
            }
            
            & $pythonCmd -m venv .venv
            Write-Success "Virtual environment created: .venv\"
            
            # Check for requirements.txt
            if (Test-Path "requirements.txt") {
                Write-Info "Installing Python dependencies..."
                try {
                    & .venv\Scripts\python.exe -m pip install -r requirements.txt | Out-Null
                    Write-Success "Dependencies installed (pyyaml, jsonschema)"
                    Write-Host ""
                    Write-Info "To activate the environment:"
                    Write-Host "  .venv\Scripts\activate"
                } catch {
                    Write-Warning-Custom "Failed to install dependencies. Run manually:"
                    Write-Host "  .venv\Scripts\activate"
                    Write-Host "  pip install -r requirements.txt"
                }
            } else {
                Write-Warning-Custom "requirements.txt not found in current directory."
            }
        } catch {
            Write-Warning-Custom "Failed to create virtual environment: $_"
            Write-Info "You can create it manually:"
            Write-Host "  python -m venv .venv"
            Write-Host "  .venv\Scripts\activate"
            Write-Host "  pip install -r requirements.txt"
        }
    }
    "2" {
        Write-Info "Skipping Python environment setup."
        Write-Info "To set up later:"
        Write-Host "  python -m venv .venv"
        Write-Host "  .venv\Scripts\activate"
        Write-Host "  pip install -r requirements.txt"
    }
    default {
        Write-Info "Invalid selection. Skipping Python environment setup."
    }
}

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
