#!/usr/bin/env python3
"""
Deprecated file usage check for CI.

SSOT: scripts/ci_check_deprecated_files.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Set


def find_deprecated_files(root: Path) -> List[Path]:
    deprecated_files: List[Path] = []
    for path in root.rglob("*.py"):
        name = path.name.lower()
        if "deprecated" in name or "_legacy" in name:
            deprecated_files.append(path)
    return deprecated_files


def has_deprecated_header(path: Path) -> bool:
    header = "\n".join(path.read_text(encoding="utf-8", errors="ignore").splitlines()[:30])
    return "DEPRECATED" in header.upper()


def build_module_map(paths: List[Path]) -> Dict[str, Path]:
    modules = {}
    for path in paths:
        module_name = path.with_suffix("").as_posix().replace("/", ".")
        modules[module_name] = path
    return modules


def find_deprecated_imports(root: Path, deprecated_modules: Set[str]) -> Dict[str, List[str]]:
    findings: Dict[str, List[str]] = {}
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for module in deprecated_modules:
            if f"import {module}" in text or f"from {module} import" in text:
                findings.setdefault(path.as_posix(), []).append(module)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Deprecated file checker")
    parser.add_argument("--root", default="src", help="Root directory to scan")
    args = parser.parse_args()

    root = Path(args.root)
    deprecated_files = find_deprecated_files(root)
    missing_headers = [path for path in deprecated_files if not has_deprecated_header(path)]

    deprecated_modules = set(build_module_map(deprecated_files).keys())
    deprecated_imports = find_deprecated_imports(root, deprecated_modules)

    if missing_headers:
        print(f"❌ Deprecated files missing headers: {len(missing_headers)}")
        for path in missing_headers:
            print(f"  - {path.as_posix()}")
        return 1

    if deprecated_imports:
        print(f"❌ Deprecated file usage found: {len(deprecated_imports)} files")
        for path, modules in deprecated_imports.items():
            print(f"  - {path}: {', '.join(modules)}")
        return 1

    print("✅ No deprecated file usage found")
    print("✅ All deprecated files have proper headers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
