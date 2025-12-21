#!/bin/bash
# PaperKit Version Reader
# Reads version from .paperkit/_cfg/version.yaml
# Fallback to VERSION file for backwards compatibility

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERKIT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Function to get version from YAML file
get_version_from_yaml() {
    local version_file="${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml"
    
    if [ ! -f "$version_file" ]; then
        return 1
    fi
    
    # Try using Python with PyYAML (most reliable)
    if command -v python3 >/dev/null 2>&1; then
        local version=$(python3 -c "
import sys
try:
    import yaml
    with open('${version_file}', 'r') as f:
        data = yaml.safe_load(f)
        print(data.get('version', {}).get('current', ''))
    sys.exit(0)
except:
    sys.exit(1)
" 2>/dev/null)
        
        if [ $? -eq 0 ] && [ -n "$version" ]; then
            echo "$version"
            return 0
        fi
    fi
    
    # Fallback: Simple grep/sed (less reliable but works without PyYAML)
    local version=$(grep -A1 '^version:' "$version_file" | grep 'current:' | sed 's/.*current:[[:space:]]*["'\'']\?\([^"'\'']*\)["'\'']\?.*/\1/' | tr -d ' ')
    
    if [ -n "$version" ]; then
        echo "$version"
        return 0
    fi
    
    return 1
}

# Function to get version from legacy VERSION file
get_version_from_file() {
    local version_file="${PAPERKIT_ROOT}/VERSION"
    
    if [ -f "$version_file" ]; then
        cat "$version_file"
        return 0
    fi
    
    return 1
}

# Main logic: Try YAML first, then fallback to VERSION file
VERSION=""

# Try YAML config first
VERSION=$(get_version_from_yaml 2>/dev/null || echo "")

# Fallback to legacy VERSION file if YAML didn't return a valid version
if [ -z "$VERSION" ] || [ "$VERSION" = "unknown" ]; then
    VERSION=$(get_version_from_file 2>/dev/null || echo "")
fi

# Final fallback to unknown
if [ -z "$VERSION" ]; then
    VERSION="unknown"
fi

echo "$VERSION"
