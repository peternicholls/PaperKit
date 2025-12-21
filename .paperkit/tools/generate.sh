#!/bin/bash
# PaperKit IDE Generator
# Generates IDE-specific agent files from .paperkit/ source of truth
# Usage: ./.paperkit/tools/generate.sh [--target=copilot|codex|all] [--check]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERKIT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Defaults
TARGET="all"
CHECK_ONLY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --target=*)
            TARGET="${1#*=}"
            shift
            ;;
        --check)
            CHECK_ONLY=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [--target=copilot|codex|all] [--check]"
            echo ""
            echo "Options:"
            echo "  --target=TARGET   Generate for specific IDE (copilot, codex, all)"
            echo "  --check           Only check if files are up to date, don't generate"
            echo "  -h, --help        Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

info_msg() { echo -e "${BLUE}ℹ ${NC}$1"; }
success_msg() { echo -e "${GREEN}✓ ${NC}$1"; }
warning_msg() { echo -e "${YELLOW}⚠ ${NC}$1"; }
error_msg() { echo -e "${RED}✗ ${NC}$1"; }

# Generate GitHub Copilot agent file
generate_copilot_agent() {
    local source_file="$1"
    local agent_name=$(basename "$source_file" .md)
    local module_path=$(dirname "$source_file")
    local module_type=$(basename "$(dirname "$module_path")")  # core or specialist
    
    # Extract description from YAML frontmatter or first line
    local description=$(grep -m1 'description:' "$source_file" 2>/dev/null | sed 's/.*description:[[:space:]]*["'\'']\?\([^"'\'']*\)["'\'']\?.*/\1/' || echo "Activates the ${agent_name} agent")
    
    # Determine output filename - avoid double "paper-" prefix
    local output_name="$agent_name"
    if [[ ! "$agent_name" =~ ^paper- ]]; then
        output_name="paper-${agent_name}"
    fi
    
    local output_file="${PAPERKIT_ROOT}/.github/agents/${output_name}.agent.md"
    
    if $CHECK_ONLY; then
        if [ -f "$output_file" ]; then
            echo "  [OK] $output_file"
        else
            echo "  [MISSING] $output_file"
            return 1
        fi
        return 0
    fi
    
    mkdir -p "$(dirname "$output_file")"
    
    cat > "$output_file" << EOFAGENT
\`\`\`chatagent
---
description: "${description}"
tools: ["changes","edit","fetch","problems","search","runSubagent","usages"]
---

# ${agent_name} Agent

<agent-activation CRITICAL="TRUE">
1. LOAD the FULL agent file from @.paperkit/${module_type}/agents/${agent_name}.md
2. READ its entire contents
3. Execute ALL activation steps exactly as written
4. Follow the agent's persona and menu system
5. Stay in character throughout
</agent-activation>

## Source of Truth

This file is auto-generated from \`.paperkit/${module_type}/agents/${agent_name}.md\`.
Do not edit directly—run \`paperkit generate --target=copilot\` to regenerate.
\`\`\`
EOFAGENT
    
    success_msg "Generated: $output_file"
}

# Generate OpenAI Codex prompt file
generate_codex_prompt() {
    local source_file="$1"
    local agent_name=$(basename "$source_file" .md)
    local module_path=$(dirname "$source_file")
    local module_type=$(basename "$(dirname "$module_path")")
    
    # Extract description and role from source file
    local description=$(grep -m1 'description:' "$source_file" 2>/dev/null | sed 's/.*description:[[:space:]]*["'\'']\?\([^"'\'']*\)["'\'']\?.*/\1/' || echo "Activates the ${agent_name} agent")
    local role=$(grep -m1 '<role>' "$source_file" 2>/dev/null | sed 's/.*<role>\([^<]*\)<\/role>.*/\1/' || echo "${agent_name}")
    
    # Determine output filename - avoid double "paper-" prefix
    local output_name="$agent_name"
    if [[ ! "$agent_name" =~ ^paper- ]]; then
        output_name="paper-${agent_name}"
    fi
    
    local output_file="${PAPERKIT_ROOT}/.codex/prompts/${output_name}.md"
    
    if $CHECK_ONLY; then
        if [ -f "$output_file" ]; then
            echo "  [OK] $output_file"
        else
            echo "  [MISSING] $output_file"
            return 1
        fi
        return 0
    fi
    
    mkdir -p "$(dirname "$output_file")"
    
    cat > "$output_file" << EOFPROMPT
# ${agent_name} Agent

Activate the **${role}** persona from the Copilot Research Paper Assistant Kit.

## Instructions

1. Load the full agent definition from \`.paperkit/${module_type}/agents/${agent_name}.md\`
2. Load configuration from \`.paperkit/${module_type}/config.yaml\`
3. Follow all activation steps exactly as written
4. Present the menu and wait for user input
5. Stay in character throughout the session

## Quick Reference

**Purpose:** ${description}
**Source:** \`.paperkit/${module_type}/agents/${agent_name}.md\`
**Config:** \`.paperkit/${module_type}/config.yaml\`

---

*This file is auto-generated. Run \`paperkit generate --target=codex\` to regenerate.*
EOFPROMPT
    
    success_msg "Generated: $output_file"
}

# Main generation logic
main() {
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║         PaperKit IDE Generator                    ║${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Verify .paperkit directory exists
    if [ ! -d "${PAPERKIT_ROOT}/.paperkit" ]; then
        error_msg ".paperkit/ directory not found. Run from PaperKit root."
        exit 1
    fi
    
    local has_errors=false
    
    # Generate for GitHub Copilot
    if [[ "$TARGET" == "copilot" || "$TARGET" == "all" ]]; then
        echo ""
        if $CHECK_ONLY; then
            info_msg "Checking GitHub Copilot agents..."
        else
            info_msg "Generating GitHub Copilot agents..."
        fi
        
        # Core agents
        for agent_file in "${PAPERKIT_ROOT}"/.paperkit/core/agents/*.md; do
            [ -f "$agent_file" ] || continue
            if ! generate_copilot_agent "$agent_file"; then
                has_errors=true
            fi
        done
        
        # Specialist agents
        for agent_file in "${PAPERKIT_ROOT}"/.paperkit/specialist/agents/*.md; do
            [ -f "$agent_file" ] || continue
            if ! generate_copilot_agent "$agent_file"; then
                has_errors=true
            fi
        done
    fi
    
    # Generate for OpenAI Codex
    if [[ "$TARGET" == "codex" || "$TARGET" == "all" ]]; then
        echo ""
        if $CHECK_ONLY; then
            info_msg "Checking OpenAI Codex prompts..."
        else
            info_msg "Generating OpenAI Codex prompts..."
        fi
        
        # Core agents
        for agent_file in "${PAPERKIT_ROOT}"/.paperkit/core/agents/*.md; do
            [ -f "$agent_file" ] || continue
            if ! generate_codex_prompt "$agent_file"; then
                has_errors=true
            fi
        done
        
        # Specialist agents
        for agent_file in "${PAPERKIT_ROOT}"/.paperkit/specialist/agents/*.md; do
            [ -f "$agent_file" ] || continue
            if ! generate_codex_prompt "$agent_file"; then
                has_errors=true
            fi
        done
    fi
    
    # Generate documentation files (AGENTS.md, COPILOT.md)
    if [[ "$TARGET" == "all" ]]; then
        echo ""
        if ! $CHECK_ONLY; then
            info_msg "Generating documentation files..."
            if [ -f "${PAPERKIT_ROOT}/.paperkit/tools/generate-docs.sh" ]; then
                "${PAPERKIT_ROOT}/.paperkit/tools/generate-docs.sh" || warning_msg "Documentation generation had issues"
            else
                warning_msg "generate-docs.sh not found, skipping documentation generation"
            fi
        fi
    fi
    
    echo ""
    if $CHECK_ONLY; then
        if $has_errors; then
            warning_msg "Some IDE files are missing or out of date."
            info_msg "Run 'paperkit generate' to regenerate."
            exit 1
        else
            success_msg "All IDE files are present."
        fi
    else
        success_msg "IDE file generation complete!"
        info_msg "Generated files are derived from .paperkit/ source of truth."
    fi
    
    # Generate .copilot/ configuration files
    if [ "$TARGET" = "all" ] || [ "$TARGET" = "copilot-config" ]; then
        if [ -f "${PAPERKIT_ROOT}/.paperkit/tools/generate-copilot.sh" ]; then
            "${PAPERKIT_ROOT}/.paperkit/tools/generate-copilot.sh" || warning_msg ".copilot/ generation had issues"
        fi
    fi
}

main
