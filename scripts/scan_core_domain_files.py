#!/usr/bin/env python3
"""
Scan Core Domain Files for Task 1
==================================

Scans core domain files (excluding analytics) to identify files for Task 1 scanning.
Focus: Files 200-300 lines (approaching V2 limit) for code quality & structure assessment.

Author: Agent-2
Date: 2025-12-14
"""

import sys
from pathlib import Path


def get_line_count(file_path: Path) -> int:
    """Get line count for a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def main():
    """Main entry point."""
    base_dir = Path("src/core")

    if not base_dir.exists():
        print(f"❌ Directory not found: {base_dir}")
        sys.exit(1)

    core_files = []

    # Scan core directory (excluding analytics)
    for py_file in base_dir.rglob("*.py"):
        # Skip analytics directory
        if "analytics" in str(py_file):
            continue

        # Skip __init__.py files
        if py_file.name == "__init__.py":
            continue

        line_count = get_line_count(py_file)
        relative_path = str(py_file.relative_to(Path(".")))

        # Focus on files 200-300 lines (approaching limit)
        if line_count >= 200:
            core_files.append({
                "path": relative_path,
                "lines": line_count
            })

    # Sort by line count (descending)
    core_files.sort(key=lambda x: x["lines"], reverse=True)

    print("=" * 80)
    print("📊 CORE DOMAIN FILES - LINE COUNTS (200+ lines, excluding analytics)")
    print("=" * 80)
    print()

    for i, file_info in enumerate(core_files, 1):
        status = "⚠️ APPROACHING LIMIT" if file_info["lines"] >= 250 else "✅ OK"
        print(
            f"{i:2d}. {status:25s} {file_info['lines']:4d} lines - {file_info['path']}")

    print()
    print("=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)

    total_files = len(core_files)
    approaching_limit = [f for f in core_files if f["lines"] >= 250]
    large_files = [f for f in core_files if f["lines"]
                   >= 200 and f["lines"] < 250]

    print(f"Total Core Domain Files (200+ lines): {total_files}")
    print(f"Files 250-300 lines (approaching limit): {len(approaching_limit)}")
    print(f"Files 200-250 lines: {len(large_files)}")
    print()

    if approaching_limit:
        print("⚠️ FILES APPROACHING 300-LINE LIMIT (250-300 lines):")
        for file_info in approaching_limit[:21]:  # Top 21
            print(f"  - {file_info['path']} ({file_info['lines']} lines)")
        print()

    if total_files >= 21:
        print("✅ RECOMMENDATION: Select top 21 files for Task 1 scanning")
        print("   Prioritize files 250-300 lines first, then 200-250 lines")
    else:
        print(f"💡 NOTE: Only {total_files} files found (200+ lines)")
        print("   May need to include files 150-200 lines to reach 21 files")
    print()


if __name__ == "__main__":
    main()
