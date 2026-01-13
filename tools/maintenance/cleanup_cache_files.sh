#!/bin/bash

# Infrastructure Cache Cleanup Script (Cross-platform)
# Removes Python cache files and build artifacts to optimize repository size
# Usage: ./cleanup_cache_files.sh [--dry-run]

set -e

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
fi

echo "🧹 Infrastructure Cache Cleanup Script"
echo "====================================="

START_TIME=$(date +%s)
FILES_REMOVED=0
SPACE_SAVED=0

# Function to format file size
format_size() {
    local size=$1
    if [ $size -gt 1073741824 ]; then
        echo "$(( size / 1073741824 ))GB"
    elif [ $size -gt 1048576 ]; then
        echo "$(( size / 1048576 ))MB"
    elif [ $size -gt 1024 ]; then
        echo "$(( size / 1024 ))KB"
    else
        echo "${size}B"
    fi
}

# Clean .pyc files
echo ""
echo "🗂️  Cleaning Python cache files (.pyc)..."
if [ "$DRY_RUN" = true ]; then
    PYCFILES=$(find . -name "*.pyc" -type f 2>/dev/null | wc -l)
    PYCSIZE=$(find . -name "*.pyc" -type f -exec stat -f%z {} \; 2>/dev/null | awk '{sum += $1} END {print sum}')
    [ -z "$PYCSIZE" ] && PYCSIZE=0
    echo "Found $PYCFILES .pyc files using $(format_size $PYCSIZE)"
    echo "[DRY RUN] Would remove $PYCFILES .pyc files"
else
    PYCFILES=$(find . -name "*.pyc" -type f 2>/dev/null | wc -l)
    PYCSIZE=$(find . -name "*.pyc" -type f -exec stat -f%z {} \; 2>/dev/null | awk '{sum += $1} END {print sum}')
    [ -z "$PYCSIZE" ] && PYCSIZE=0
    if [ $PYCFILES -gt 0 ]; then
        echo "Found $PYCFILES .pyc files using $(format_size $PYCSIZE)"
        find . -name "*.pyc" -type f -delete 2>/dev/null
        echo "✅ Removed $PYCFILES .pyc files"
        FILES_REMOVED=$((FILES_REMOVED + PYCFILES))
        SPACE_SAVED=$((SPACE_SAVED + PYCSIZE))
    else
        echo "No .pyc files found"
    fi
fi

# Clean __pycache__ directories
echo ""
echo "📁 Cleaning __pycache__ directories..."
if [ "$DRY_RUN" = true ]; then
    PYCACHEDIRS=$(find . -name "__pycache__" -type d 2>/dev/null | wc -l)
    echo "Found $PYCACHEDIRS __pycache__ directories"
    echo "[DRY RUN] Would remove $PYCACHEDIRS __pycache__ directories"
else
    PYCACHEDIRS=$(find . -name "__pycache__" -type d 2>/dev/null | wc -l)
    if [ $PYCACHEDIRS -gt 0 ]; then
        echo "Found $PYCACHEDIRS __pycache__ directories"
        find . -name "__pycache__" -type d -exec rm -rf {} \; 2>/dev/null
        echo "✅ Removed $PYCACHEDIRS __pycache__ directories"
    else
        echo "No __pycache__ directories found"
    fi
fi

# Clean .ruff_cache directory
echo ""
echo "🔧 Cleaning .ruff_cache directory..."
if [ -d ".ruff_cache" ]; then
    RUFFSIZE=$(find .ruff_cache -type f -exec stat -f%z {} \; 2>/dev/null | awk '{sum += $1} END {print sum}')
    [ -z "$RUFFSIZE" ] && RUFFSIZE=0
    echo "Found .ruff_cache directory using $(format_size $RUFFSIZE)"
    if [ "$DRY_RUN" = true ]; then
        echo "[DRY RUN] Would remove .ruff_cache directory"
    else
        rm -rf .ruff_cache
        echo "✅ Removed .ruff_cache directory"
        SPACE_SAVED=$((SPACE_SAVED + RUFFSIZE))
    fi
else
    echo "No .ruff_cache directory found"
fi

# Clean other common cache directories
CACHE_DIRS=(
    "node_modules/.cache"
    ".next/cache"
    ".nuxt/cache"
    "target/surefire-reports"
    "build/test-results"
    ".pytest_cache"
    ".mypy_cache"
)

for cache_dir in "${CACHE_DIRS[@]}"; do
    if [ -d "$cache_dir" ]; then
        echo ""
        echo "🗂️  Cleaning $cache_dir..."
        CACHESIZE=$(find "$cache_dir" -type f -exec stat -f%z {} \; 2>/dev/null | awk '{sum += $1} END {print sum}')
        [ -z "$CACHESIZE" ] && CACHESIZE=0
        echo "Found cache directory using $(format_size $CACHESIZE)"
        if [ "$DRY_RUN" = true ]; then
            echo "[DRY RUN] Would remove $cache_dir"
        else
            rm -rf "$cache_dir"
            echo "✅ Removed $cache_dir"
            SPACE_SAVED=$((SPACE_SAVED + CACHESIZE))
        fi
    fi
done

# Calculate execution time
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Summary
echo ""
echo "📊 Cleanup Summary"
echo "=================="
echo "Execution time: ${DURATION} seconds"
echo "Files removed: $FILES_REMOVED"
echo "Space saved: $(format_size $SPACE_SAVED)"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "🔍 This was a dry run - no files were actually removed"
    echo "Run without --dry-run to perform actual cleanup"
else
    echo ""
    echo "✅ Cache cleanup completed successfully"
    echo "Repository size optimized for better performance"
fi

echo ""
echo "💡 Recommendation: Add this script to your CI/CD pipeline for automated cleanup"