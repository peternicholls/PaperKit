#!/bin/bash

# ==============================================================================
# LaTeX Syntax Checker
# ==============================================================================
# Validates LaTeX syntax and common issues before compilation
# ==============================================================================

LATEX_DIR="latex"
ERRORS=0
WARNINGS=0

echo "LaTeX Syntax Validation"
echo "======================"

# Check for common LaTeX mistakes
check_unmatched_braces() {
  echo "Checking for unmatched braces..."
  for file in "$LATEX_DIR"/**/*.tex; do
    if [ -f "$file" ]; then
      # Count opening and closing braces
      open=$(grep -o '{' "$file" | wc -l)
      close=$(grep -o '}' "$file" | wc -l)
      if [ "$open" -ne "$close" ]; then
        echo "⚠ Unmatched braces in $file (open: $open, close: $close)"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  done
}

check_unmatched_math() {
  echo "Checking for unmatched math delimiters..."
  for file in "$LATEX_DIR"/**/*.tex; do
    if [ -f "$file" ]; then
      # Check for odd number of $
      dollar=$(grep -o '\$' "$file" | wc -l)
      if [ $((dollar % 2)) -ne 0 ]; then
        echo "⚠ Unmatched $ in $file"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  done
}

check_unclosed_commands() {
  echo "Checking for unclosed environments..."
  for file in "$LATEX_DIR"/**/*.tex; do
    if [ -f "$file" ]; then
      begins=$(grep -c '\\begin{' "$file" || true)
      ends=$(grep -c '\\end{' "$file" || true)
      if [ "$begins" -ne "$ends" ]; then
        echo "⚠ Unmatched begin/end in $file (begin: $begins, end: $ends)"
        WARNINGS=$((WARNINGS + 1))
      fi
    fi
  done
}

check_citations() {
  echo "Checking for citation references..."
  citation_keys=$(grep -ho '\\cite{[^}]*}' "$LATEX_DIR"/**/*.tex | sed 's/\\cite{//g' | sed 's/}//g' | sort -u)
  for key in $citation_keys; do
    if ! grep -q "^@.*{$key" "$LATEX_DIR"/references/references.bib 2>/dev/null; then
      echo "⚠ Citation key not found in bibliography: $key"
      WARNINGS=$((WARNINGS + 1))
    fi
  done
}

check_section_files() {
  echo "Checking for missing section files..."
  section_files=$(grep -ho '\\input{sections/[^}]*}' "$LATEX_DIR"/main.tex)
  for file in $section_files; do
    file=$(echo "$file" | sed 's/\\input{//g' | sed 's/}//g')
    if [ ! -f "$LATEX_DIR/$file.tex" ]; then
      echo "✗ Section file not found: $LATEX_DIR/$file.tex"
      ERRORS=$((ERRORS + 1))
    fi
  done
}

# Run checks
echo ""
check_unmatched_braces
echo ""
check_unmatched_math
echo ""
check_unclosed_commands
echo ""
check_citations
echo ""
check_section_files

# Summary
echo ""
echo "======================"
echo "Validation Summary"
echo "======================"
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
  echo ""
  echo "✗ Validation failed. Fix errors before compilation."
  exit 1
else
  echo ""
  echo "✓ Validation complete. Safe to compile."
  exit 0
fi
