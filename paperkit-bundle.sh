#!/bin/bash

# PaperKit Bundle Creator
# Version: alpha-1.0.0
# Creates a distribution bundle of PaperKit for easy sharing

set -e

VERSION=$(cat VERSION 2>/dev/null || echo "unknown")
BUNDLE_NAME="paperkit-${VERSION}"
BUNDLE_DIR="/tmp/${BUNDLE_NAME}"
ARCHIVE_NAME="${BUNDLE_NAME}.tar.gz"

echo "📦 Creating PaperKit distribution bundle..."
echo "Version: $VERSION"
echo ""

# Clean up any existing bundle directory
if [ -d "$BUNDLE_DIR" ]; then
    echo "Cleaning up existing bundle directory..."
    rm -rf "$BUNDLE_DIR"
fi

# Create bundle directory
echo "Creating bundle directory: $BUNDLE_DIR"
mkdir -p "$BUNDLE_DIR"

# Core files to include in the bundle
echo "Copying core files..."

# Installation scripts
cp paperkit-install.sh "$BUNDLE_DIR/"
cp paperkit-install.ps1 "$BUNDLE_DIR/"
cp paperkit "$BUNDLE_DIR/"
chmod +x "$BUNDLE_DIR/paperkit"
chmod +x "$BUNDLE_DIR/paperkit-install.sh"

# Version and documentation
cp VERSION "$BUNDLE_DIR/"
cp AGENTS.md "$BUNDLE_DIR/"
[ -f COPILOT.md ] && cp COPILOT.md "$BUNDLE_DIR/"
[ -f README.md ] && cp README.md "$BUNDLE_DIR/"

# Core directories
echo "Copying directory structure..."
cp -r .paper "$BUNDLE_DIR/"
cp -r .github "$BUNDLE_DIR/"
cp -r .codex "$BUNDLE_DIR/"
cp -r .copilot "$BUNDLE_DIR/" 2>/dev/null || true
[ -d .vscode ] && cp -r .vscode "$BUNDLE_DIR/"

# LaTeX templates
mkdir -p "$BUNDLE_DIR/latex"
cp -r latex/* "$BUNDLE_DIR/latex/" 2>/dev/null || true

# Open agents system
[ -d open-agents ] && cp -r open-agents "$BUNDLE_DIR/"
[ -d open-agent-system ] && cp -r open-agent-system "$BUNDLE_DIR/"

# Planning templates
mkdir -p "$BUNDLE_DIR/planning"
[ -f planning/.gitkeep ] && cp planning/.gitkeep "$BUNDLE_DIR/planning/"

# System planning documentation
[ -d SYSTEM-PLANNING ] && cp -r SYSTEM-PLANNING "$BUNDLE_DIR/"

# Clean up unnecessary files from bundle
echo "Cleaning bundle..."
find "$BUNDLE_DIR" -name ".DS_Store" -delete 2>/dev/null || true
find "$BUNDLE_DIR" -name "*.pyc" -delete 2>/dev/null || true
find "$BUNDLE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$BUNDLE_DIR" -name ".git" -type d -exec rm -rf {} + 2>/dev/null || true

# Create archive
echo "Creating archive: $ARCHIVE_NAME"
cd /tmp
tar -czf "$ARCHIVE_NAME" "$BUNDLE_NAME"

# Move archive to current directory
mv "$ARCHIVE_NAME" "$OLDPWD/"

# Show summary
echo ""
echo "✓ Bundle created successfully!"
echo ""
echo "Archive: $ARCHIVE_NAME"
echo "Size: $(du -h "$OLDPWD/$ARCHIVE_NAME" | cut -f1)"
echo ""
echo "Distribution instructions:"
echo "1. Share $ARCHIVE_NAME with users"
echo "2. Users extract: tar -xzf $ARCHIVE_NAME"
echo "3. Users run: cd $BUNDLE_NAME && ./paperkit init"
echo ""

# Cleanup
rm -rf "$BUNDLE_DIR"

echo "Bundle location: $OLDPWD/$ARCHIVE_NAME"
