#!/bin/bash

# ==============================================================================
# Dependency Verification Script
# ==============================================================================
# Checks all required dependencies for the Academic Paper Writing System
# ==============================================================================

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

REQUIRED_MISSING=0
OPTIONAL_MISSING=0

echo "===================================="
echo "  Dependency Check"
echo "===================================="
echo ""

# ==============================================================================
# LaTeX Dependencies (REQUIRED)
# ==============================================================================
echo "LaTeX Distribution:"
echo "-------------------"

if command -v pdflatex >/dev/null 2>&1; then
  VERSION=$(pdflatex --version | head -n 1)
  echo -e "  ${GREEN}✓${NC} pdflatex: $VERSION"
else
  echo -e "  ${RED}✗${NC} pdflatex: NOT FOUND (REQUIRED)"
  echo "     Install: brew install --cask basictex (macOS)"
  echo "              sudo apt-get install texlive-latex-base (Linux)"
  REQUIRED_MISSING=$((REQUIRED_MISSING + 1))
fi

if command -v bibtex >/dev/null 2>&1; then
  VERSION=$(bibtex --version | head -n 1)
  echo -e "  ${GREEN}✓${NC} bibtex: $VERSION"
else
  echo -e "  ${RED}✗${NC} bibtex: NOT FOUND (REQUIRED)"
  echo "     Usually installed with LaTeX distribution"
  REQUIRED_MISSING=$((REQUIRED_MISSING + 1))
fi

echo ""

# ==============================================================================
# Python Dependencies (REQUIRED)
# ==============================================================================
echo "Python:"
echo "-------"

if command -v python3 >/dev/null 2>&1; then
  VERSION=$(python3 --version)
  echo -e "  ${GREEN}✓${NC} python3: $VERSION"
  
  # Check Python version (need 3.7+)
  PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
  PY_MAJOR=$(echo $PY_VERSION | cut -d. -f1)
  PY_MINOR=$(echo $PY_VERSION | cut -d. -f2)
  
  if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 7 ]); then
    echo -e "  ${YELLOW}⚠${NC}  Python version $PY_VERSION detected. Version 3.7+ recommended."
  fi
else
  echo -e "  ${RED}✗${NC} python3: NOT FOUND (REQUIRED)"
  echo "     Install: brew install python3 (macOS)"
  echo "              sudo apt-get install python3 (Linux)"
  REQUIRED_MISSING=$((REQUIRED_MISSING + 1))
fi

# Check PyYAML
if python3 -c "import yaml" 2>/dev/null; then
  VERSION=$(python3 -c "import yaml; print(yaml.__version__)" 2>/dev/null || echo "unknown")
  echo -e "  ${GREEN}✓${NC} pyyaml: $VERSION"
else
  echo -e "  ${RED}✗${NC} pyyaml: NOT FOUND (REQUIRED)"
  echo "     Install: pip3 install pyyaml"
  REQUIRED_MISSING=$((REQUIRED_MISSING + 1))
fi

echo ""

# ==============================================================================
# Optional Dependencies
# ==============================================================================
echo "Optional Tools:"
echo "---------------"

if command -v pdfinfo >/dev/null 2>&1; then
  VERSION=$(pdfinfo -v 2>&1 | head -n 1 | awk '{print $3}')
  echo -e "  ${GREEN}✓${NC} pdfinfo: $VERSION"
else
  echo -e "  ${YELLOW}○${NC} pdfinfo: NOT FOUND (optional)"
  echo "     Install: brew install poppler (macOS)"
  echo "              sudo apt-get install poppler-utils (Linux)"
  OPTIONAL_MISSING=$((OPTIONAL_MISSING + 1))
fi

echo ""

# ==============================================================================
# LaTeX Package Check
# ==============================================================================
echo "LaTeX Packages:"
echo "---------------"

if command -v pdflatex >/dev/null 2>&1; then
  PACKAGES=(
    "biblatex"
    "geometry"
    "hyperref"
    "amsmath"
    "tikz"
    "listings"
  )
  
  MISSING_PACKAGES=0
  
  for pkg in "${PACKAGES[@]}"; do
    if kpsewhich "${pkg}.sty" >/dev/null 2>&1; then
      echo -e "  ${GREEN}✓${NC} $pkg"
    else
      echo -e "  ${RED}✗${NC} $pkg: NOT FOUND"
      MISSING_PACKAGES=$((MISSING_PACKAGES + 1))
    fi
  done
  
  if [ $MISSING_PACKAGES -gt 0 ]; then
    echo ""
    echo -e "  ${YELLOW}⚠${NC}  Missing $MISSING_PACKAGES LaTeX packages"
    echo "     Install with: sudo tlmgr install <package-name>"
    echo "     Or see DEPENDENCIES.md for complete list"
  fi
else
  echo -e "  ${YELLOW}○${NC} Cannot check LaTeX packages (pdflatex not installed)"
fi

echo ""

# ==============================================================================
# Summary
# ==============================================================================
echo "===================================="
echo "  Summary"
echo "===================================="

if [ $REQUIRED_MISSING -eq 0 ]; then
  echo -e "${GREEN}✓ All required dependencies installed${NC}"
else
  echo -e "${RED}✗ Missing $REQUIRED_MISSING required dependencies${NC}"
fi

if [ $OPTIONAL_MISSING -gt 0 ]; then
  echo -e "${YELLOW}○ Missing $OPTIONAL_MISSING optional dependencies${NC}"
fi

echo ""

if [ $REQUIRED_MISSING -eq 0 ]; then
  echo "Ready to build papers!"
  echo "Run: ./open-agents/tools/build-latex.sh"
  exit 0
else
  echo "Please install missing required dependencies."
  echo "See: open-agents/DEPENDENCIES.md"
  exit 1
fi
