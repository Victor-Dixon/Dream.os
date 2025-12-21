#!/usr/bin/env python3
"""
Get Line Counts for Analytics Files
===================================

Quick script to get line counts for analytics files to prioritize V2 violation scanning.

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
    base_dir = Path("src/core/analytics")

    if not base_dir.exists():
        print(f"❌ Directory not found: {base_dir}")
        sys.exit(1)

    analytics_files = []

    # Scan analytics directory
    for py_file in base_dir.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue

        line_count = get_line_count(py_file)
        relative_path = str(py_file.relative_to(Path(".")))

        analytics_files.append({
            "path": relative_path,
            "lines": line_count
        })

    # Sort by line count (descending)
    analytics_files.sort(key=lambda x: x["lines"], reverse=True)

    print("=" * 80)
    print("📊 ANALYTICS FILES - LINE COUNTS (Sorted by Size)")
    print("=" * 80)
    print()

    for i, file_info in enumerate(analytics_files, 1):
        status = "⚠️ VIOLATION" if file_info["lines"] > 300 else "✅ OK"
        print(
            f"{i:2d}. {status:15s} {file_info['lines']:4d} lines - {file_info['path']}")

    print()
    print("=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)

    total_files = len(analytics_files)
    violation_files = [f for f in analytics_files if f["lines"] > 300]
    large_files = [f for f in analytics_files if f["lines"] > 500]

    print(f"Total Analytics Files: {total_files}")
    print(f"Files >300 lines (V2 Violations): {len(violation_files)}")
    print(f"Files >500 lines (Large Violations): {len(large_files)}")
    print()

    if violation_files:
        print("⚠️ FILES WITH V2 VIOLATIONS (>300 lines):")
        for file_info in violation_files:
            print(f"  - {file_info['path']} ({file_info['lines']} lines)")
        print()

    if len(violation_files) < 21:
        print("💡 RECOMMENDATION: Include largest files <300 lines to reach 21 files")
        print("   Focus on engines, processors, orchestrators, intelligence files")
        print()


if __name__ == "__main__":
    main()
