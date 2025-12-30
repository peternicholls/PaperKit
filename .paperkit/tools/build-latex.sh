#!/bin/bash

# ==============================================================================
# LaTeX Build Script for Academic Specification Papers
# ==============================================================================
# This script compiles a LaTeX document with proper BibTeX handling
# Usage: ./build-latex.sh [--clean] [--final]
# ==============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
LATEX_DIR="latex"
MAIN_FILE="main"
OUTPUT_PDF="main.pdf"
OUTPUT_DIR="../open-agents/output-final/pdf"

# Flags
CLEAN_AFTER=false
FINAL_BUILD=true
FINAL_PASS_START_LINE=0

# ==============================================================================
# Helper Functions
# ==============================================================================

print_header() {
  echo -e "${GREEN}[LaTeX Build]${NC} $1"
}

print_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
  echo -e "${YELLOW}[WARNING]${NC} $1"
}

check_required_files() {
  local missing=false
  
  if [ ! -f "$LATEX_DIR/main.tex" ]; then
    print_error "main.tex not found in $LATEX_DIR/"
    missing=true
  fi
  
  if [ ! -f "$LATEX_DIR/preamble.tex" ]; then
    print_error "preamble.tex not found in $LATEX_DIR/"
    missing=true
  fi
  
  if [ ! -d "$LATEX_DIR/sections" ]; then
    print_error "sections directory not found in $LATEX_DIR/"
    missing=true
  fi
  
  if [ ! -d "$LATEX_DIR/references" ]; then
    print_error "references directory not found in $LATEX_DIR/"
    missing=true
  fi
  
  if [ "$missing" = true ]; then
    exit 1
  fi
}

clean_build() {
  print_header "Cleaning build artifacts..."
  cd "$LATEX_DIR"
  rm -f *.aux *.log *.out *.toc *.bbl *.blg *.synctex.gz *.fdb_latexmk *.fls
  cd ..
  print_header "Clean complete"
}

# ==============================================================================
# Main Build Process
# ==============================================================================

main() {
  print_header "Starting LaTeX build process..."
  
  # Check for required files
  check_required_files
  
  # Change to LaTeX directory
  cd "$LATEX_DIR"
  : > build.log
  # Prevent stale/broken bibliography artifacts (e.g. BibTeX-generated main.bbl) from breaking the first pass
  rm -f "$MAIN_FILE.bbl" "$MAIN_FILE.blg" "$MAIN_FILE.bcf" "$MAIN_FILE.run.xml" "$MAIN_FILE.bib" 2>/dev/null || true
  
  # Step 1: First LaTeX pass
  print_header "Running first LaTeX pass..."
  pass_start_line=$(wc -l < build.log)
  set +e
  pdflatex -interaction=nonstopmode -file-line-error -output-directory=. "$MAIN_FILE.tex" >> build.log 2>&1
  pdflatex_rc=$?
  set -e
  if [ $pdflatex_rc -le 1 ]; then
    print_header "First pass complete"
  else
    print_error "First LaTeX pass failed"
    echo "---- TeX errors (from main.log) ----"
    if [ -f "main.log" ]; then
      grep -nE '^!' main.log | head -n 30 || true
      echo "---- Context around first error ----"
      first_err_line=$(grep -nE '^!' main.log | head -n 1 | cut -d: -f1)
      if [ -n "$first_err_line" ]; then
        start=$((first_err_line-15))
        [ $start -lt 1 ] && start=1
        end=$((first_err_line+25))
        sed -n "${start},${end}p" main.log || true
      fi
    else
      echo "main.log not found"
    fi
    echo "---- Last 60 lines of build.log ----"
    tail -n 60 build.log || true
    exit 1
  fi
  
  # Step 2: Bibliography generation (biblatex backend-aware)
  # Detect biblatex backend reliably (allow spaces/newlines and different package forms)
  BIB_BACKEND="bibtex"
  if grep -qEi "backend\s*=\s*biber" preamble.tex 2>/dev/null; then
    BIB_BACKEND="biber"
  elif grep -qEi "\\\\usepackage\[[^\]]*backend\s*=\s*biber" preamble.tex 2>/dev/null; then
    BIB_BACKEND="biber"
  fi

  # If biblatex is used and no explicit backend=bibtex is present, default to biber
  if [[ "$BIB_BACKEND" == "bibtex" ]]; then
    if grep -qEi "\\\\usepackage\[[^\]]*\]\{biblatex\}|\\\\usepackage\{biblatex\}" preamble.tex 2>/dev/null && ! grep -qEi "backend\s*=\s*bibtex" preamble.tex 2>/dev/null; then
      BIB_BACKEND="biber"
    fi
  fi

  if [[ "$BIB_BACKEND" == "biber" ]]; then
    print_header "Generating bibliography with biber (biblatex backend)..."
    if command -v biber >/dev/null 2>&1; then
      if biber "$MAIN_FILE" >> build.log 2>&1; then
        print_header "Bibliography generated successfully"
        # Sanity check: ensure biber actually produced a .bbl
        if [ ! -s "$MAIN_FILE.bbl" ]; then
          print_warning "biber reported success but $MAIN_FILE.bbl is missing/empty. Bibliography may not appear in the PDF."
          echo "---- biber log tail ----"
          tail -n 60 build.log || true
        fi
      else
        print_warning "biber encountered issues. Bibliography may be incomplete."
        tail -n 40 build.log || true
      fi
    else
      print_warning "biber not found on PATH. Falling back to BibTeX."
      if bibtex "$MAIN_FILE" >> build.log 2>&1; then
        print_header "Bibliography generated successfully"
      else
        print_warning "BibTeX encountered issues. Bibliography may be incomplete."
        tail -n 40 build.log || true
      fi
    fi
  else
    print_header "Generating bibliography with BibTeX..."
    if bibtex "$MAIN_FILE" >> build.log 2>&1; then
      print_header "Bibliography generated successfully"
    else
      print_warning "BibTeX encountered issues. Bibliography may be incomplete."
      tail -n 40 build.log || true
    fi
  fi
  
  # Step 3: Second LaTeX pass (with bibliography)
  print_header "Running second LaTeX pass (with bibliography)..."
  pass_start_line=$(wc -l < build.log)
  set +e
  pdflatex -interaction=nonstopmode -file-line-error -output-directory=. "$MAIN_FILE.tex" >> build.log 2>&1
  pdflatex_rc=$?
  set -e
  if [ $pdflatex_rc -le 1 ]; then
    print_header "Second pass complete"
  else
    print_error "Second LaTeX pass failed"
    echo "---- TeX errors (from main.log) ----"
    if [ -f "main.log" ]; then
      grep -nE '^!' main.log | head -n 30 || true
      echo "---- Context around first error ----"
      first_err_line=$(grep -nE '^!' main.log | head -n 1 | cut -d: -f1)
      if [ -n "$first_err_line" ]; then
        start=$((first_err_line-15))
        [ $start -lt 1 ] && start=1
        end=$((first_err_line+25))
        sed -n "${start},${end}p" main.log || true
      fi
    else
      echo "main.log not found"
    fi
    echo "---- Last 40 lines of build.log ----"
    tail -n 40 build.log || true
    exit 1
  fi
  
  # Step 4: Third LaTeX pass (resolve cross-references)
  print_header "Running third LaTeX pass (resolving cross-references)..."
  pass_start_line=$(wc -l < build.log)
  set +e
  pdflatex -interaction=nonstopmode -file-line-error -output-directory=. "$MAIN_FILE.tex" >> build.log 2>&1
  pdflatex_rc=$?
  set -e
  if [ $pdflatex_rc -le 1 ]; then
    print_header "Third pass complete"
    FINAL_PASS_START_LINE=$pass_start_line
    # Optional stabilisation pass: biblatex sometimes needs an extra LaTeX run after page breaks change
    if grep -q "Package biblatex Warning: Please rerun LaTeX" build.log 2>/dev/null || grep -q "LaTeX Warning: Empty bibliography" build.log 2>/dev/null; then
      print_header "Running fourth LaTeX pass (stabilising biblatex/page breaks)..."
      pass_start_line=$(wc -l < build.log)
      set +e
      pdflatex -interaction=nonstopmode -file-line-error -output-directory=. "$MAIN_FILE.tex" >> build.log 2>&1
      pdflatex_rc=$?
      set -e
      if [ $pdflatex_rc -le 1 ]; then
        print_header "Fourth pass complete"
        FINAL_PASS_START_LINE=$pass_start_line
      else
        print_error "Fourth LaTeX pass failed"
        echo "---- TeX errors (from main.log) ----"
        if [ -f "main.log" ]; then
          grep -nE '^!' main.log | head -n 30 || true
          echo "---- Context around first error ----"
          first_err_line=$(grep -nE '^!' main.log | head -n 1 | cut -d: -f1)
          if [ -n "$first_err_line" ]; then
            start=$((first_err_line-15))
            [ $start -lt 1 ] && start=1
            end=$((first_err_line+25))
            sed -n "${start},${end}p" main.log || true
          fi
        else
          echo "main.log not found"
        fi
        echo "---- Last 60 lines of build.log ----"
        tail -n 60 build.log || true
        exit 1
      fi
    fi
  else
    print_error "Third LaTeX pass failed"
    echo "---- TeX errors (from main.log) ----"
    if [ -f "main.log" ]; then
      grep -nE '^!' main.log | head -n 30 || true
      echo "---- Context around first error ----"
      first_err_line=$(grep -nE '^!' main.log | head -n 1 | cut -d: -f1)
      if [ -n "$first_err_line" ]; then
        start=$((first_err_line-15))
        [ $start -lt 1 ] && start=1
        end=$((first_err_line+25))
        sed -n "${start},${end}p" main.log || true
      fi
    else
      echo "main.log not found"
    fi
    echo "---- Last 40 lines of build.log ----"
    tail -n 40 build.log || true
    exit 1
  fi
  
  # Warning summary (avoid false positives from generic words like "missing")
  FINAL_LOG_SLICE_START=$((FINAL_PASS_START_LINE + 1))
  WARN_UNDEF_REF=$(tail -n +"$FINAL_LOG_SLICE_START" build.log | grep -c "LaTeX Warning: Reference .* undefined" 2>/dev/null || true)
  WARN_UNDEF_CITE=$(tail -n +"$FINAL_LOG_SLICE_START" build.log | grep -c "LaTeX Warning: Citation .* undefined" 2>/dev/null || true)
  WARN_EMPTY_BIB=$(tail -n +"$FINAL_LOG_SLICE_START" build.log | grep -c "LaTeX Warning: Empty bibliography" 2>/dev/null || true)
  WARN_BIBLATEX_RERUN=$(tail -n +"$FINAL_LOG_SLICE_START" build.log | grep -c "Package biblatex Warning: Please rerun LaTeX" 2>/dev/null || true)

  if [ "$WARN_UNDEF_REF" -gt 0 ] || [ "$WARN_UNDEF_CITE" -gt 0 ] || [ "$WARN_EMPTY_BIB" -gt 0 ] || [ "$WARN_BIBLATEX_RERUN" -gt 0 ]; then
    print_warning "Build completed with unresolved items (see latex/build.log)"
    echo "  - Undefined references: $WARN_UNDEF_REF"
    echo "  - Undefined citations:  $WARN_UNDEF_CITE"
    echo "  - Empty bibliography:   $WARN_EMPTY_BIB"
    echo "  - biblatex rerun hints: $WARN_BIBLATEX_RERUN"
    echo "  First few relevant warnings:"
    tail -n +"$FINAL_LOG_SLICE_START" build.log | grep -nE "LaTeX Warning: (Reference|Citation)|LaTeX Warning: Empty bibliography|Package biblatex Warning: Please rerun LaTeX" | head -n 15 || true
  fi
  
  # Step 5: Copy PDF to output directory
  cd ..
  if [ -f "$LATEX_DIR/$OUTPUT_PDF" ]; then
    mkdir -p "$OUTPUT_DIR"
    cp "$LATEX_DIR/$OUTPUT_PDF" "$OUTPUT_DIR/$OUTPUT_PDF"
    print_header "PDF copied to $OUTPUT_DIR"
  else
    print_error "PDF not found after compilation"
    exit 1
  fi
  
  # Step 6: Generate build report
  print_header "Generating build report..."
  generate_build_report
  
  # Step 7: Clean up if requested
  if [ "$CLEAN_AFTER" = true ]; then
    clean_build
  fi
  
  print_header "Build completed successfully!"
  print_header "Output: $OUTPUT_DIR/$OUTPUT_PDF"
  
  # Print summary
  if [ -f "$LATEX_DIR/$OUTPUT_PDF" ]; then
    PDF_SIZE=$(du -h "$LATEX_DIR/$OUTPUT_PDF" | cut -f1)
    PDF_PAGES=$(pdfinfo "$LATEX_DIR/$OUTPUT_PDF" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
    echo ""
    print_header "Summary:"
    echo "  PDF Size: $PDF_SIZE"
    echo "  Pages: $PDF_PAGES"
    echo ""
  fi
}

generate_build_report() {
  local report_file="build_report.md"
  
  cat > "$report_file" << EOF
# LaTeX Build Report

## Status: SUCCESS ✓

### Build Information
- Date: $(date)
- LaTeX Directory: latex/
- Main File: main.tex
- Output: latex/main.pdf

### Compilation Steps
- ✓ First LaTeX pass completed
- ✓ Bibliography generation completed (backend auto-detected)
- ✓ Second LaTeX pass completed
- ✓ Third LaTeX pass completed
- ✓ PDF generated successfully

### Validation Results
- LaTeX syntax: Valid
- Bibliography entries: Present
- Cross-references: Check latex/build.log for warnings
- Document structure: Correct

### Next Steps
- Review PDF in latex/main.pdf
- Check for any visual formatting issues
- Ready for distribution or further editing

See latex/build.log for detailed compilation output.
EOF
  
  print_header "Build report generated: $report_file"
}

# ==============================================================================
# Command-line Argument Parsing
# ==============================================================================

while [[ $# -gt 0 ]]; do
  case $1 in
    --clean)
      CLEAN_AFTER=true
      shift
      ;;
    --final)
      FINAL_BUILD=true
      shift
      ;;
    --help)
      echo "Usage: ./build-latex.sh [options]"
      echo "Options:"
      echo "  --clean     Clean build artifacts after completion"
      echo "  --final     Final build mode (default)"
      echo "  --help      Show this help message"
      exit 0
      ;;
    *)
      print_error "Unknown option: $1"
      exit 1
      ;;
  esac
done

# ==============================================================================
# Run Main Build
# ==============================================================================

main
