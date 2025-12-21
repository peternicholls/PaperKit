#!/bin/bash
# Test script for PaperKit version management system
# Tests both YAML-based and legacy VERSION file systems

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PAPERKIT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((TESTS_PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((TESTS_FAILED++))
    return 0  # Don't exit on fail
}

info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

section() {
    echo ""
    echo -e "${YELLOW}━━━ $1 ━━━${NC}"
}

# Start tests
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     PaperKit Version System Tests                ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"

# Test 1: Check version.yaml exists
section "Test 1: Configuration File"
if [ -f "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml" ]; then
    pass "version.yaml exists"
else
    fail "version.yaml not found"
fi

# Test 2: Check get-version.sh exists and is executable
section "Test 2: Shell Script"
if [ -x "${PAPERKIT_ROOT}/.paperkit/tools/get-version.sh" ]; then
    pass "get-version.sh is executable"
else
    fail "get-version.sh not found or not executable"
fi

# Test 3: Test get-version.sh output
section "Test 3: Version Retrieval (Shell)"
VERSION_SH=$("${PAPERKIT_ROOT}/.paperkit/tools/get-version.sh" 2>/dev/null)
if [ -n "$VERSION_SH" ] && [ "$VERSION_SH" != "unknown" ]; then
    pass "get-version.sh returns version: $VERSION_SH"
else
    fail "get-version.sh did not return a valid version"
fi

# Test 4: Check version-manager.py exists and is executable
section "Test 4: Python Tool"
if [ -x "${PAPERKIT_ROOT}/.paperkit/tools/version-manager.py" ]; then
    pass "version-manager.py is executable"
else
    fail "version-manager.py not found or not executable"
fi

# Test 5: Test version-manager.py get command
section "Test 5: Version Retrieval (Python)"
if command -v python3 >/dev/null 2>&1; then
    if python3 -c "import yaml" 2>/dev/null; then
        VERSION_PY=$(python3 "${PAPERKIT_ROOT}/.paperkit/tools/version-manager.py" get 2>/dev/null)
        if [ -n "$VERSION_PY" ] && [ "$VERSION_PY" != "unknown" ]; then
            pass "version-manager.py get returns: $VERSION_PY"
        else
            fail "version-manager.py get did not return a valid version"
        fi
    else
        info "PyYAML not installed, skipping Python tests"
    fi
else
    info "Python3 not available, skipping Python tests"
fi

# Test 6: Test paperkit version command
section "Test 6: Integration Test (paperkit CLI)"
cd "${PAPERKIT_ROOT}"
PAPERKIT_VERSION=$(./paperkit version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "")
if [ -n "$PAPERKIT_VERSION" ]; then
    pass "paperkit version command works"
    info "  Version: $PAPERKIT_VERSION"
else
    # Try without grep filtering
    PAPERKIT_OUTPUT=$(./paperkit version 2>/dev/null || echo "")
    if echo "$PAPERKIT_OUTPUT" | grep -q "version"; then
        pass "paperkit version command works"
        info "  Output: $PAPERKIT_OUTPUT"
    else
        fail "paperkit version command failed"
    fi
fi

# Test 7: Verify shell and Python return same version
section "Test 7: Consistency Check"
if [ -n "$VERSION_SH" ] && [ -n "$VERSION_PY" ]; then
    if [ "$VERSION_SH" = "$VERSION_PY" ]; then
        pass "Shell and Python tools return same version"
    else
        fail "Version mismatch: Shell=$VERSION_SH, Python=$VERSION_PY"
    fi
else
    info "Skipping consistency check (one or both tools not available)"
fi

# Test 8: Test backwards compatibility with VERSION file
section "Test 8: Backwards Compatibility"
if [ -f "${PAPERKIT_ROOT}/VERSION" ]; then
    LEGACY_VERSION=$(cat "${PAPERKIT_ROOT}/VERSION")
    pass "Legacy VERSION file exists: $LEGACY_VERSION"
    
    # Temporarily move version.yaml and test fallback
    if [ -f "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml" ]; then
        mv "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml" "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml.bak"
        FALLBACK_VERSION=$("${PAPERKIT_ROOT}/.paperkit/tools/get-version.sh" 2>/dev/null)
        mv "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml.bak" "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml"
        
        if [ "$FALLBACK_VERSION" = "$LEGACY_VERSION" ]; then
            pass "Fallback to VERSION file works correctly"
        else
            fail "Fallback version mismatch: Expected=$LEGACY_VERSION, Got=$FALLBACK_VERSION"
        fi
    fi
else
    info "Legacy VERSION file not present (acceptable)"
fi

# Test 9: Test version.yaml structure
section "Test 9: YAML Structure Validation"
if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" 2>/dev/null; then
    YAML_VALID=$(python3 << 'EOF'
import yaml
import sys
try:
    with open('.paperkit/_cfg/version.yaml', 'r') as f:
        data = yaml.safe_load(f)
    required = ['version']
    version_required = ['current', 'release', 'components']
    
    if 'version' not in data:
        print("Missing 'version' key")
        sys.exit(1)
    
    for key in version_required:
        if key not in data['version']:
            print(f"Missing 'version.{key}' key")
            sys.exit(1)
    
    print("valid")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
EOF
)
    if [ "$YAML_VALID" = "valid" ]; then
        pass "version.yaml has correct structure"
    else
        fail "version.yaml structure invalid: $YAML_VALID"
    fi
else
    info "Python/PyYAML not available, skipping YAML structure validation"
fi

# Test 10: Test version bumping (if PyYAML available)
section "Test 10: Version Bump Functionality"
if command -v python3 >/dev/null 2>&1 && python3 -c "import yaml" 2>/dev/null; then
    # Create a test version file
    TEST_VERSION_FILE="/tmp/test-version-$$.yaml"
    cp "${PAPERKIT_ROOT}/.paperkit/_cfg/version.yaml" "$TEST_VERSION_FILE"
    
    # Test bump
    BUMP_RESULT=$(python3 "${PAPERKIT_ROOT}/.paperkit/tools/version-manager.py" --config "$TEST_VERSION_FILE" bump patch 2>/dev/null || echo "error")
    if echo "$BUMP_RESULT" | grep -q "Version bumped to:"; then
        pass "Version bump functionality works"
        info "  $BUMP_RESULT"
    else
        fail "Version bump failed: $BUMP_RESULT"
    fi
    
    # Cleanup
    rm -f "$TEST_VERSION_FILE"
else
    info "Python/PyYAML not available, skipping version bump test"
fi

# Summary
section "Test Summary"
echo ""
TOTAL=$((TESTS_PASSED + TESTS_FAILED))
echo "Tests run: $TOTAL"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
else
    echo -e "${GREEN}Failed: 0${NC}"
fi
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    exit 1
fi
