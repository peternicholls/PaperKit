#!/bin/bash
# PaperKit Title Reader
# Reads title from .paperkit/_cfg/version.yaml

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERKIT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Function to get title from YAML file
get_title_from_yaml() {
    local version_file="${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml"
    local title_type="${1:-short}"  # 'short' or 'long'
    
    if [ ! -f "$version_file" ]; then
        return 1
    fi
    
    # Try using Python with PyYAML (most reliable)
    if command -v python3 >/dev/null 2>&1; then
        local title=$(python3 -c "
import sys
try:
    import yaml
    with open('${version_file}', 'r') as f:
        data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise ValueError('version.yaml must be a mapping')
        version = data.get('version', {}) if isinstance(data.get('version', {}), dict) else {}
        title_data = version.get('title', {}) if isinstance(version.get('title', {}), dict) else {}
        title = title_data.get('${title_type}', '')
        if title:
            print(title)
            sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
" 2>/dev/null)
        
        if [ $? -eq 0 ] && [ -n "$title" ]; then
            echo "$title"
            return 0
        fi
    fi
    
    # Fallback: Simple sed-based extraction (works without PyYAML)
    # Look for 'short:' or 'long:' under title section
    local title
    if [ "$title_type" = "short" ]; then
        title=$(sed -n -E "s/^[[:space:]]*short:[[:space:]]*[\"']?([^\"']*)[\"']?.*/\\1/p" "$version_file" | head -n 1 | tr -d '[:space:]')
    else
        title=$(sed -n -E "s/^[[:space:]]*long:[[:space:]]*[\"']?([^\"']*)[\"']?.*/\\1/p" "$version_file" | head -n 1)
    fi
    
    if [ -n "$title" ]; then
        echo "$title"
        return 0
    fi
    
    return 1
}

# Main logic
TITLE_TYPE="${1:-short}"
TITLE=""

# Try YAML config
TITLE=$(get_title_from_yaml "$TITLE_TYPE" 2>/dev/null || echo "")

# Fallback defaults if not found
if [ -z "$TITLE" ]; then
    if [ "$TITLE_TYPE" = "short" ]; then
        TITLE="PaperKit"
    else
        TITLE="Research Paper Assistant"
    fi
fi

echo "$TITLE"
