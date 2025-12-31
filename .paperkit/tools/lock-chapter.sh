#!/usr/bin/env bash
# ==============================================================================
# Lock Chapter Tool
# ==============================================================================
# Execute the chapter locking protocol:
# 1. Validate chapter is ready (build succeeds)
# 2. Commit final state
# 3. Create annotated git tag
# 4. Generate PDF snapshot
# 5. Create/update documentation
# ==============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ==============================================================================
# Configuration
# ==============================================================================

SNAPSHOT_DIR="$PROJECT_ROOT/open-agents/output-final/snapshots"
DOCS_DIR="$PROJECT_ROOT/dev-docs"
LOCK_INDEX="$DOCS_DIR/00README-CHAPTER-LOCKS.md"

# ==============================================================================
# Color output
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $*"; }
info() { echo -e "${BLUE}[INFO]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

# ==============================================================================
# Usage
# ==============================================================================

usage() {
    cat <<EOF
Usage: $(basename "$0") --target <target> --title <title> [options]

Lock a chapter or section from further conceptual edits.

Required:
  --target <id>        Short identifier (ch2, frontmatter, etc.)
  --title <title>      Human-readable title

Optional:
  --major <n>          Major version (default: 0)
  --minor <n>          Minor version (auto-assigned if not provided)
  --type <type>        Content type: chapter|frontmatter|appendix|section (default: chapter)
  --files <paths>      Comma-separated file paths being locked
  --help               Show this help

Examples:
  $(basename "$0") --target ch2 --title "Perceptual Foundations"
  $(basename "$0") --target frontmatter --title "Abstract and Metadata" --type frontmatter

EOF
    exit 1
}

# ==============================================================================
# Parse arguments
# ==============================================================================

TARGET=""
TITLE=""
VERSION_MAJOR=0
VERSION_MINOR=""
TARGET_TYPE="chapter"
FILE_PATHS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --target) TARGET="$2"; shift 2 ;;
        --title) TITLE="$2"; shift 2 ;;
        --major) VERSION_MAJOR="$2"; shift 2 ;;
        --minor) VERSION_MINOR="$2"; shift 2 ;;
        --type) TARGET_TYPE="$2"; shift 2 ;;
        --files) FILE_PATHS="$2"; shift 2 ;;
        --help) usage ;;
        *) error "Unknown option: $1"; usage ;;
    esac
done

# Validate required args
if [[ -z "$TARGET" ]] || [[ -z "$TITLE" ]]; then
    error "Missing required arguments"
    usage
fi

# Auto-assign minor version if not provided
if [[ -z "$VERSION_MINOR" ]]; then
    # Get next minor version by counting existing tags
    EXISTING_COUNT=$(git tag -l "paper-v${VERSION_MAJOR}.*" | wc -l | tr -d ' ')
    VERSION_MINOR=$((EXISTING_COUNT + 1))
    info "Auto-assigned minor version: $VERSION_MINOR"
fi

TAG="paper-v${VERSION_MAJOR}.${VERSION_MINOR}-${TARGET}-signedoff"
DATESTAMP=$(date +%Y%m%d)
SNAPSHOT_FILE="$SNAPSHOT_DIR/${TAG}_${DATESTAMP}.pdf"
LOCK_SUMMARY="$DOCS_DIR/${TARGET^^}-LOCK-SUMMARY.md"

# ==============================================================================
# Pre-flight checks
# ==============================================================================

info "Pre-flight checks..."

# Check we're in project root
cd "$PROJECT_ROOT" || { error "Cannot cd to project root"; exit 1; }

# Check git working directory is clean
if [[ -n "$(git status --porcelain)" ]]; then
    warn "Git working directory is not clean"
    git status --short
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# ==============================================================================
# Step 1: Build and validate
# ==============================================================================

info "Building LaTeX document..."
if ! ./paperkit latex build; then
    error "LaTeX build failed - cannot lock"
    exit 1
fi
success "Build succeeded"

# ==============================================================================
# Step 2: Create git commit
# ==============================================================================

info "Creating git commit..."

COMMIT_MSG="Lock ${TARGET}: ${TITLE} - signed off"

if [[ -n "$FILE_PATHS" ]]; then
    IFS=',' read -ra FILES <<< "$FILE_PATHS"
    git add "${FILES[@]}"
fi

# Add lock documentation
mkdir -p "$SNAPSHOT_DIR"
git add "$SNAPSHOT_DIR" 2>/dev/null || true

if git diff --cached --quiet; then
    warn "No changes to commit"
else
    git commit -m "$COMMIT_MSG"
    success "Committed: $COMMIT_MSG"
fi

COMMIT_HASH=$(git rev-parse HEAD)

# ==============================================================================
# Step 3: Create annotated tag
# ==============================================================================

info "Creating git tag: $TAG..."

TAG_MSG="${TITLE} signed off - locked for conceptual edits. Only mechanical fixes permitted."

if git tag -l "$TAG" | grep -q "$TAG"; then
    warn "Tag $TAG already exists - skipping"
else
    git tag -a "$TAG" -m "$TAG_MSG"
    success "Created tag: $TAG"
fi

# ==============================================================================
# Step 4: Create PDF snapshot
# ==============================================================================

info "Creating PDF snapshot..."

mkdir -p "$SNAPSHOT_DIR"

# Find the built PDF
if [[ -f "latex/main.pdf" ]]; then
    cp "latex/main.pdf" "$SNAPSHOT_FILE"
    success "Snapshot created: $SNAPSHOT_FILE"
elif [[ -f ".paperkit/data/output-final/pdf/main.pdf" ]]; then
    cp ".paperkit/data/output-final/pdf/main.pdf" "$SNAPSHOT_FILE"
    success "Snapshot created: $SNAPSHOT_FILE"
else
    error "Cannot find built PDF"
    exit 1
fi

SNAPSHOT_SIZE=$(du -h "$SNAPSHOT_FILE" | cut -f1)
info "Snapshot size: $SNAPSHOT_SIZE"

# ==============================================================================
# Step 5: Create lock summary documentation
# ==============================================================================

info "Creating lock summary: $LOCK_SUMMARY..."

cat > "$LOCK_SUMMARY" <<EOF
# ${TITLE} Lock Summary

**Status:** 🔒 LOCKED  
**Locked Date:** $(date '+%d %b %Y')  
**Git Tag:** \`$TAG\`  
**Snapshot:** \`$(basename "$SNAPSHOT_FILE")\`  
**Commit:** \`$COMMIT_HASH\`

---

## 📄 Locked Content

### Target
- **Identifier:** $TARGET
- **Type:** $TARGET_TYPE
- **Title:** $TITLE

$(if [[ -n "$FILE_PATHS" ]]; then
    echo "### Files Affected"
    IFS=',' read -ra FILES <<< "$FILE_PATHS"
    for file in "${FILES[@]}"; do
        echo "- \`$file\`"
    done
fi)

---

## 🔐 Lock Policy

### ✅ Permitted (Mechanical Fixes Only)
- Typo corrections
- LaTeX formatting fixes
- Build error resolution
- Reference formatting

### ❌ Prohibited (Requires Unlock)
- Conceptual changes
- Content additions/removals
- Structural modifications
- Substantive rewording

---

## 🔄 Unlock Protocol

If substantive changes are needed:

1. **Document rationale:** Why unlock is necessary
2. **Get approval:** From Paper Architect
3. **Create revision tag:** \`paper-v${VERSION_MAJOR}.${VERSION_MINOR}.1-${TARGET}-revised\`
4. **Make changes:** With full documentation
5. **Re-lock:** New snapshot and tag

---

## 📅 History

| Date | Event | Tag |
|------|-------|-----|
| $(date '+%d %b %Y') | Initial sign-off | \`$TAG\` |

---

**Maintained by:** Paper Architect agent  
**Last Updated:** $(date '+%d %b %Y')
EOF

success "Created: $LOCK_SUMMARY"

# ==============================================================================
# Step 6: Update master lock index
# ==============================================================================

info "Updating master lock index..."

# Check if entry already exists
if grep -q "$TAG" "$LOCK_INDEX" 2>/dev/null; then
    warn "Entry already exists in lock index"
else
    # This is complex - just notify user to update manually
    warn "Please manually update $LOCK_INDEX with:"
    echo ""
    echo "| **$TITLE** | $TITLE | \`$TAG\` | [PDF](../open-agents/output-final/snapshots/$(basename "$SNAPSHOT_FILE")) | $(date '+%d %b %Y') |"
    echo ""
fi

# ==============================================================================
# Step 7: Commit lock documentation
# ==============================================================================

info "Committing lock documentation..."

git add "$LOCK_SUMMARY" "$SNAPSHOT_FILE"
git commit -m "Add lock documentation for ${TARGET}: ${TITLE}"

success "Documentation committed"

# ==============================================================================
# Summary
# ==============================================================================

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}  ✅ Lock Complete: $TITLE"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "📋 Summary:"
echo "  • Tag: $TAG"
echo "  • Commit: ${COMMIT_HASH:0:8}"
echo "  • Snapshot: $(basename "$SNAPSHOT_FILE") ($SNAPSHOT_SIZE)"
echo "  • Documentation: $(basename "$LOCK_SUMMARY")"
echo ""
echo "🔒 Lock Policy:"
echo "  ✅ Mechanical fixes permitted"
echo "  ❌ Conceptual changes require unlock"
echo ""
echo "📚 Documentation:"
echo "  • Lock summary: $LOCK_SUMMARY"
echo "  • Master index: $LOCK_INDEX (update manually)"
echo ""

exit 0
