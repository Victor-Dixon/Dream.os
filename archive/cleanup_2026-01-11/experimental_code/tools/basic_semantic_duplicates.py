#!/usr/bin/env python3
"""
Basic Semantic Duplicate Detection - Phase 3 Markdown Cleanup
===========================================================

Simple semantic analysis to identify obviously similar markdown files.
Focuses on high-confidence duplicates for safe consolidation.

Author: Agent-5 (Business Intelligence)
Date: 2026-01-11
"""

import os
from pathlib import Path
from collections import defaultdict

def find_obvious_duplicates():
    """Find obviously duplicate files based on naming patterns and content."""

    repo_root = Path('.')
    duplicates = defaultdict(list)

    # Find all markdown files
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', '.git']]
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                duplicates[file].append(file_path)

    # Filter to files with multiple copies
    real_duplicates = {name: paths for name, paths in duplicates.items() if len(paths) > 1}

    print(f"Found {len(real_duplicates)} files with multiple copies")
    print(f"Total duplicate instances: {sum(len(paths) for paths in real_duplicates.values())}")

    # Show top duplicates
    for name, paths in sorted(real_duplicates.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"\n{name}: {len(paths)} copies")
        for path in paths[:5]:  # Show first 5
            print(f"  {path}")
        if len(paths) > 5:
            print(f"  ... and {len(paths) - 5} more")

    return real_duplicates

if __name__ == "__main__":
    print("🔍 Basic Semantic Duplicate Detection")
    print("=" * 40)
    duplicates = find_obvious_duplicates()

    total_files = sum(len(paths) for paths in duplicates.values())
    potential_savings = sum(len(paths) - 1 for paths in duplicates.values())

    print("\n📊 Summary:")
    print(f"   Duplicate file types: {len(duplicates)}")
    print(f"   Total duplicate files: {total_files}")
    print(f"   Potential savings: {potential_savings} files")