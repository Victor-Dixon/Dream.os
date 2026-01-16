#!/usr/bin/env python3
"""
Merge Conflict Detector - Agent-2 Closure Improvement Tool
Scans codebase for unresolved git merge conflicts.
"""

import os
import re
from pathlib import Path


def detect_merge_conflicts(repo_root: str) -> list[dict]:
    """
    Scan repository for merge conflict markers.

    Returns list of files with conflicts and their line counts.
    """
    conflicts = []
    conflict_pattern = re.compile(r'^<{7} |^={7}$|^>{7} ')

    for py_file in Path(repo_root).rglob("*.py"):
        if py_file.is_file():
            try:
                content = py_file.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')

                conflict_lines = []
                for i, line in enumerate(lines, 1):
                    if conflict_pattern.match(line.strip()):
                        conflict_lines.append(i)

                if conflict_lines:
                    conflicts.append({
                        'file': str(py_file.relative_to(repo_root)),
                        'conflict_lines': conflict_lines,
                        'total_conflicts': len(conflict_lines) // 3  # Each conflict has 3 markers
                    })

            except Exception:
                continue

    return conflicts


def main():
    """CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(description="Detect merge conflicts in codebase")
    parser.add_argument("--repo-root", default=".", help="Repository root directory")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    conflicts = detect_merge_conflicts(args.repo_root)

    if args.json:
        import json
        print(json.dumps(conflicts, indent=2))
    else:
        if conflicts:
            print(f"🚨 Found {len(conflicts)} files with merge conflicts:")
            for conflict in conflicts:
                print(f"  📄 {conflict['file']}: {conflict['total_conflicts']} conflicts")
                print(f"     Lines: {', '.join(map(str, conflict['conflict_lines']))}")
        else:
            print("✅ No merge conflicts detected")


if __name__ == "__main__":
    main()