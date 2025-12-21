<#
.SYNOPSIS
    PaperKit IDE File Generator for Windows PowerShell

.DESCRIPTION
    Generates IDE-specific files from .paper/ source of truth.
    Creates GitHub Copilot agents (.github/agents/) and 
    OpenAI Codex prompts (.codex/prompts/).

.PARAMETER Target
    Which IDE files to generate: 'copilot', 'codex', or 'all' (default)

.PARAMETER Check
    Check if files are up to date without generating

.EXAMPLE
    .\paperkit-generate.ps1
    Generates all IDE files

.EXAMPLE
    .\paperkit-generate.ps1 -Target copilot
    Generates only GitHub Copilot agents

.EXAMPLE
    .\paperkit-generate.ps1 -Check
    Checks if IDE files need updating

.NOTES
    Part of PaperKit - Research Paper Assistant Kit
    Source of truth: .paper/
#>

param(
    [ValidateSet('copilot', 'codex', 'all')]
    [string]$Target = 'all',
    
    [switch]$Check,
    
    [switch]$Verbose
)

# Colors for output
function Write-Success { param($Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Error { param($Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Warning { param($Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Info { param($Message) Write-Host "  $Message" -ForegroundColor Cyan }

# Find project root
function Find-ProjectRoot {
    $current = Get-Location
    
    while ($current) {
        if (Test-Path (Join-Path $current ".paper")) {
            return $current
        }
        $parent = Split-Path $current -Parent
        if ($parent -eq $current) { break }
        $current = $parent
    }
    
    return $null
}

# Get agent name from file (strips paper- prefix if present)
function Get-AgentName {
    param([string]$FilePath)
    
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($FilePath)
    if ($baseName.StartsWith("paper-")) {
        return $baseName.Substring(6)
    }
    return $baseName
}

# Get display name from agent file (extract from frontmatter)
function Get-AgentDisplayName {
    param([string]$FilePath)
    
    $content = Get-Content $FilePath -Raw
    if ($content -match '(?ms)^---\s*\n.*?displayName:\s*"?([^"\n]+)"?\s*\n.*?^---') {
        return $matches[1].Trim()
    }
    
    # Fallback: generate from filename
    $name = Get-AgentName $FilePath
    return ($name -replace '-', ' ' -replace '(\w)(\w*)', { $_.Groups[1].Value.ToUpper() + $_.Groups[2].Value })
}

# Get module from path
function Get-AgentModule {
    param([string]$FilePath)
    
    if ($FilePath -match 'core[/\\]agents') { return 'core' }
    if ($FilePath -match 'specialist[/\\]agents') { return 'specialist' }
    return 'unknown'
}

# Generate GitHub Copilot agent file
function New-CopilotAgent {
    param(
        [string]$SourcePath,
        [string]$OutputDir
    )
    
    $agentName = Get-AgentName $SourcePath
    $displayName = Get-AgentDisplayName $SourcePath
    $targetFile = Join-Path $OutputDir "paper-$agentName.agent.md"
    
    # Read source content
    $content = Get-Content $SourcePath -Raw
    
    # Strip YAML frontmatter if present (Copilot uses its own format)
    if ($content -match '(?ms)^---\s*\n.*?^---\s*\n(.*)$') {
        $bodyContent = $matches[1].Trim()
    } else {
        $bodyContent = $content.Trim()
    }
    
    # Generate Copilot agent file with proper header
    $copilotContent = @"
---
name: paper-$agentName
description: $displayName - PaperKit Agent
---

$bodyContent
"@
    
    # Write the file
    $copilotContent | Out-File -FilePath $targetFile -Encoding UTF8 -NoNewline
    
    return $targetFile
}

# Generate OpenAI Codex prompt file
function New-CodexPrompt {
    param(
        [string]$SourcePath,
        [string]$OutputDir
    )
    
    $agentName = Get-AgentName $SourcePath
    $targetFile = Join-Path $OutputDir "paper-$agentName.md"
    
    # Read source content
    $content = Get-Content $SourcePath -Raw
    
    # Codex uses the content as-is (may include frontmatter)
    $content | Out-File -FilePath $targetFile -Encoding UTF8 -NoNewline
    
    return $targetFile
}

# Main execution
$projectRoot = Find-ProjectRoot

if (-not $projectRoot) {
    Write-Error "Could not find PaperKit project root (.paper/ directory)"
    Write-Host "Make sure you're running from within a PaperKit project."
    exit 2
}

Write-Host ""
Write-Host "🔧 PaperKit IDE File Generator" -ForegroundColor Blue
Write-Host "   Project: $projectRoot" -ForegroundColor Cyan
Write-Host ""

# Collect all agent source files
$agentSources = @()
$coreDir = Join-Path $projectRoot ".paper\core\agents"
$specialistDir = Join-Path $projectRoot ".paper\specialist\agents"

if (Test-Path $coreDir) {
    $agentSources += Get-ChildItem -Path $coreDir -Filter "*.md" | Select-Object -ExpandProperty FullName
}
if (Test-Path $specialistDir) {
    $agentSources += Get-ChildItem -Path $specialistDir -Filter "*.md" | Select-Object -ExpandProperty FullName
}

if ($agentSources.Count -eq 0) {
    Write-Error "No agent definitions found in .paper/core/agents/ or .paper/specialist/agents/"
    exit 1
}

Write-Host "Found $($agentSources.Count) agent definitions" -ForegroundColor Gray

# Check mode
if ($Check) {
    Write-Host ""
    Write-Host "Checking IDE file status..." -ForegroundColor Blue
    
    $missing = @()
    
    if ($Target -eq 'all' -or $Target -eq 'copilot') {
        $copilotDir = Join-Path $projectRoot ".github\agents"
        foreach ($source in $agentSources) {
            $agentName = Get-AgentName $source
            $targetFile = Join-Path $copilotDir "paper-$agentName.agent.md"
            if (-not (Test-Path $targetFile)) {
                $missing += "Copilot: paper-$agentName.agent.md"
            }
        }
    }
    
    if ($Target -eq 'all' -or $Target -eq 'codex') {
        $codexDir = Join-Path $projectRoot ".codex\prompts"
        foreach ($source in $agentSources) {
            $agentName = Get-AgentName $source
            $targetFile = Join-Path $codexDir "paper-$agentName.md"
            if (-not (Test-Path $targetFile)) {
                $missing += "Codex: paper-$agentName.md"
            }
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Warning "Missing IDE files:"
        foreach ($file in $missing) {
            Write-Host "  - $file" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "Run without -Check to generate missing files." -ForegroundColor Gray
        exit 1
    } else {
        Write-Success "All IDE files are present"
        exit 0
    }
}

# Generate mode
$generated = 0
$errors = 0

# Generate GitHub Copilot agents
if ($Target -eq 'all' -or $Target -eq 'copilot') {
    $copilotDir = Join-Path $projectRoot ".github\agents"
    
    Write-Host ""
    Write-Host "Generating GitHub Copilot agents..." -ForegroundColor Blue
    
    # Create directory if needed
    if (-not (Test-Path $copilotDir)) {
        New-Item -ItemType Directory -Path $copilotDir -Force | Out-Null
        Write-Info "Created $copilotDir"
    }
    
    foreach ($source in $agentSources) {
        try {
            $targetFile = New-CopilotAgent -SourcePath $source -OutputDir $copilotDir
            $agentName = Get-AgentName $source
            Write-Success "paper-$agentName.agent.md"
            $generated++
        } catch {
            Write-Error "Failed to generate from $([System.IO.Path]::GetFileName($source)): $_"
            $errors++
        }
    }
}

# Generate OpenAI Codex prompts
if ($Target -eq 'all' -or $Target -eq 'codex') {
    $codexDir = Join-Path $projectRoot ".codex\prompts"
    
    Write-Host ""
    Write-Host "Generating OpenAI Codex prompts..." -ForegroundColor Blue
    
    # Create directory if needed
    if (-not (Test-Path $codexDir)) {
        New-Item -ItemType Directory -Path $codexDir -Force | Out-Null
        Write-Info "Created $codexDir"
    }
    
    foreach ($source in $agentSources) {
        try {
            $targetFile = New-CodexPrompt -SourcePath $source -OutputDir $codexDir
            $agentName = Get-AgentName $source
            Write-Success "paper-$agentName.md"
            $generated++
        } catch {
            Write-Error "Failed to generate from $([System.IO.Path]::GetFileName($source)): $_"
            $errors++
        }
    }
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Gray
Write-Host "Summary" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Gray
Write-Host "  Generated: $generated files" -ForegroundColor Green
if ($errors -gt 0) {
    Write-Host "  Errors: $errors" -ForegroundColor Red
}
Write-Host ""

if ($errors -gt 0) {
    Write-Warning "Generation completed with errors"
    exit 1
} else {
    Write-Success "Generation complete"
    exit 0
}
