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
        if not isinstance(data, dict):
            raise ValueError('version.yaml must be a mapping')
        version = data.get('version', {}) if isinstance(data.get('version', {}), dict) else {}
        current = version.get('current', '')
        if current:
            print(current)
            sys.exit(0)
        semver = version.get('semver', {}) if isinstance(version.get('semver', {}), dict) else {}
        if all(k in semver for k in ('major', 'minor', 'patch')):
            base = '{}.{}.{}'.format(semver['major'], semver['minor'], semver['patch'])
            prerelease = semver.get('prerelease') or ''
            build = semver.get('build') or ''

            current = '{}-{}'.format(prerelease, base) if prerelease else base
            if build:
                current = '{}+{}'.format(current, build)

            print(current)
            sys.exit(0)
    sys.exit(1)
except Exception:
    sys.exit(1)
" 2>/dev/null)
        
        if [ $? -eq 0 ] && [ -n "$version" ]; then
            echo "$version"
            return 0
        fi
    fi
    
    # Fallback: Simple sed-based extraction (works without PyYAML)
    # Expected YAML format for this fallback:
    #   version:
    #     current: 1.2.3
    # or:
    #   current: "1.2.3"
    # It intentionally supports only simple 'current: <value>' mappings on a single line.
    local version
    version=$(sed -n -E "s/^[[:space:]]*current:[[:space:]]*[\"']?([^\"']*)[\"']?.*/\\1/p" "$version_file" | head -n 1 | tr -d '[:space:]')
    
    if [ -n "$version" ]; then
        echo "$version"
        return 0
    fi
    
    return 1
}

# Function to get version from deprecated VERSION file (backwards compatibility only)
get_version_from_file() {
    local version_file="${PAPERKIT_ROOT}/VERSION.deprecated"
    
    if [ -f "$version_file" ]; then
        # Extract only the version line (first line, ignore comments)
        grep -v '^#' "$version_file" | head -n 1 | tr -d '[:space:]'
        return 0
    fi
    
    # Fallback to old VERSION file name if it still exists
    version_file="${PAPERKIT_ROOT}/VERSION"
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
