# System Dependencies

This document lists all required dependencies for the Academic Paper Writing System.

## Required Software

### 1. LaTeX Distribution

**Purpose:** Compile LaTeX documents to PDF

**Install Options:**

**macOS:**
```bash
# Option 1: Full MacTeX (4GB+ download, ~7GB installed)
brew install --cask mactex

# Option 2: BasicTeX (smaller, faster ~100MB)
brew install --cask basictex
# Then install required packages:
sudo tlmgr update --self
sudo tlmgr install \
  biblatex biber \
  geometry setspace \
  fancyhdr hyperref cleveref \
  amsmath amssymb amsthm mathtools physics \
  tikz pgf \
  booktabs array longtable enumitem \
  listings xcolor \
  babel lmodern
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  texlive-bibtex-extra \
  biber
```

**Linux (Fedora/RHEL):**
```bash
sudo dnf install texlive-scheme-medium
```

**Verification:**
```bash
pdflatex --version    # Should show version info
bibtex --version      # Should show version info
```

---

### 2. Python 3

**Purpose:** Run validation and formatting tools

**Required Version:** Python 3.7+

**Install:**

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
# Usually pre-installed; if not:
sudo apt-get install python3
```

**Verification:**
```bash
python3 --version     # Should show 3.7 or higher
```

---

### 3. Python Packages

**Purpose:** YAML parsing for validation tools

**Required Packages:**
- `pyyaml` (for metadata validation)

**Install:**
```bash
# Using pip
pip3 install pyyaml

# Or with virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pyyaml
```

**Create requirements.txt:**
```bash
echo "pyyaml>=6.0" > open-agents/tools/requirements.txt
pip install -r open-agents/tools/requirements.txt
```

---

### 4. PDF Utilities (Optional but Recommended)

**Purpose:** PDF metadata and page counting in build scripts

**Install:**

**macOS:**
```bash
brew install poppler  # Provides pdfinfo
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

**Verification:**
```bash
pdfinfo -v
```

**Note:** Build script will work without this but won't display PDF page count

---

## LaTeX Package Dependencies

The following LaTeX packages are used in `latex/preamble.tex`:

### Core Text Packages
- `inputenc` (UTF-8 support)
- `fontenc` (Font encoding)
- `lmodern` (Latin Modern fonts)
- `babel` (Language support)

### Mathematics
- `amsmath`, `amssymb`, `amsthm` (AMS math packages)
- `mathtools` (Enhanced math tools)
- `physics` (Physics notation)

### Graphics
- `graphicx` (Image inclusion)
- `xcolor` (Color support)
- `tikz` (Diagrams and graphics)

### Page Layout
- `geometry` (Page dimensions)
- `setspace` (Line spacing)
- `fancyhdr` (Headers and footers)

### Bibliography
- `biblatex` (Bibliography management)
- `biber` or `bibtex` (Backend)

### Cross-references
- `hyperref` (Hyperlinks)
- `cleveref` (Intelligent cross-references)

### Tables and Lists
- `booktabs` (Professional tables)
- `array`, `longtable` (Table extensions)
- `enumitem` (List customization)

### Code Listings
- `listings` (Code formatting)

---

## Quick Installation Guide

### Complete Setup (macOS)

```bash
# 1. Install LaTeX
brew install --cask basictex

# 2. Update LaTeX package manager
sudo tlmgr update --self

# 3. Install required LaTeX packages
sudo tlmgr install \
  biblatex biber \
  geometry setspace \
  fancyhdr hyperref cleveref \
  amsmath amssymb amsthm mathtools physics \
  tikz pgf \
  booktabs array longtable enumitem \
  listings xcolor \
  babel lmodern

# 4. Install Python packages
pip3 install pyyaml

# 5. Install PDF utilities (optional)
brew install poppler

# 6. Verify installation
pdflatex --version
bibtex --version
python3 --version
pdfinfo -v
```

### Complete Setup (Linux)

```bash
# 1. Install LaTeX
sudo apt-get update
sudo apt-get install \
  texlive-latex-base \
  texlive-latex-extra \
  texlive-fonts-recommended \
  texlive-fonts-extra \
  texlive-bibtex-extra \
  biber

# 2. Install Python packages
pip3 install pyyaml

# 3. Install PDF utilities
sudo apt-get install poppler-utils

# 4. Verify installation
pdflatex --version
bibtex --version
python3 --version
pdfinfo -v
```

---

## Troubleshooting

### LaTeX Not Found

**Issue:** `pdflatex: command not found`

**Solution:**
- Ensure LaTeX is installed
- Add to PATH: `export PATH="/Library/TeX/texbin:$PATH"` (macOS)
- Restart terminal after installation

### Missing LaTeX Packages

**Issue:** Compilation fails with "Package X not found"

**Solution:**
```bash
# Find the package
tlmgr search --global <package-name>

# Install it
sudo tlmgr install <package-name>
```

### Python Module Not Found

**Issue:** `ModuleNotFoundError: No module named 'yaml'`

**Solution:**
```bash
pip3 install pyyaml
```

### Permission Denied for tlmgr

**Issue:** `tlmgr: permission denied`

**Solution:**
```bash
# Use sudo for system-wide installation
sudo tlmgr install <package>

# Or install to user directory
tlmgr init-usertree
tlmgr --usermode install <package>
```

---

## Minimal Setup (For Testing Only)

If you only want to test the Python tools without LaTeX:

```bash
pip3 install pyyaml
```

This allows you to run:
- `validate-structure.py`
- `format-references.py`

But **not**:
- `build-latex.sh` (requires pdflatex, bibtex)
- `lint-latex.sh` (basic checks work, but limited)

---

## Disk Space Requirements

- **BasicTeX:** ~100MB download, ~500MB installed
- **MacTeX (full):** ~4GB download, ~7GB installed
- **Linux texlive-medium:** ~1GB installed
- **Python + packages:** ~50MB

**Recommendation:** Use BasicTeX + manual package installation for minimal footprint

---

## Verification Script

Run this to check all dependencies:

```bash
#!/bin/bash
echo "=== Dependency Check ==="
echo ""

# LaTeX
echo "LaTeX:"
command -v pdflatex >/dev/null 2>&1 && echo "  ✓ pdflatex" || echo "  ✗ pdflatex (REQUIRED)"
command -v bibtex >/dev/null 2>&1 && echo "  ✓ bibtex" || echo "  ✗ bibtex (REQUIRED)"

# Python
echo ""
echo "Python:"
command -v python3 >/dev/null 2>&1 && echo "  ✓ python3" || echo "  ✗ python3 (REQUIRED)"
python3 -c "import yaml" 2>/dev/null && echo "  ✓ pyyaml" || echo "  ✗ pyyaml (REQUIRED)"

# Optional
echo ""
echo "Optional:"
command -v pdfinfo >/dev/null 2>&1 && echo "  ✓ pdfinfo" || echo "  ○ pdfinfo (optional)"

echo ""
echo "=== End Check ==="
```

Save as `check-dependencies.sh` and run with `bash check-dependencies.sh`
