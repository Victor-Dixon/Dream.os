#!/usr/bin/env python3
"""
Duplication gate for CI and pre-commit checks.

SSOT: scripts/ci_duplication_gate.py
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Dict, Iterable, List

ALLOWED_DUPLICATE_FILES = {
    "src/discord_commander/templates/broadcast_templates.py",
    "src/services/handlers/batch_message_handler.py",
    "src/gaming/dreamos/ui_integration.py",
    "tools/reports_consolidation.py",
    "tools/analysis/reports_consolidation.py",
    "tools/message_queue_launcher.py",
    "tools/utilities/message_queue_launcher.py",
    "tools/analysis/start_repository_monitoring.py",
    "scripts/start_repository_monitoring.py",
    "tools/utilities/documentation_consolidator.py",
    "scripts/documentation_consolidator.py",
}

ALLOWED_FILENAMES = {"__init__.py"}


def iter_files(roots: Iterable[str], extensions: Iterable[str]) -> Iterable[Path]:
    for root in roots:
        base = Path(root)
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix in extensions:
                if path.name in ALLOWED_FILENAMES:
                    continue
                yield path


def hash_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def is_allowed_group(files: List[Path]) -> bool:
    normalized = {path.as_posix() for path in files}
    return normalized.issubset(ALLOWED_DUPLICATE_FILES)


def find_duplicate_groups(roots: Iterable[str]) -> List[List[Path]]:
    hash_map: Dict[str, List[Path]] = {}
    for path in iter_files(roots, [".py"]):
        file_hash = hash_file(path)
        hash_map.setdefault(file_hash, []).append(path)
    return [paths for paths in hash_map.values() if len(paths) > 1]


def main() -> int:
    parser = argparse.ArgumentParser(description="CI duplication gate")
    parser.add_argument(
        "--roots",
        nargs="+",
        default=["src", "tools", "scripts"],
        help="Roots to scan for duplicate files",
    )
    args = parser.parse_args()

    duplicate_groups = find_duplicate_groups(args.roots)
    blocking_groups = [group for group in duplicate_groups if not is_allowed_group(group)]

    if blocking_groups:
        print(f"❌ BLOCKED: Found {len(blocking_groups)} blocking duplicate groups")
        for idx, group in enumerate(blocking_groups, start=1):
            print(f"\nGroup {idx}:")
            for path in group:
                print(f"  - {path.as_posix()}")
        return 1

    print("✅ PASSED: No blocking file duplications found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
