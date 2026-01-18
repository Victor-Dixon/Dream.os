#!/usr/bin/env python3
"""
SSOT compliance linter.

SSOT: scripts/ssot_linter.py
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List


def load_deprecated_modules(config_path: Path) -> List[str]:
    if not config_path.exists():
        return []
    raw = config_path.read_text(encoding="utf-8")
    return [line.strip() for line in raw.splitlines() if line.strip() and not line.strip().startswith("#")]


def check_ssot_headers(root: Path) -> List[str]:
    violations: List[str] = []
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        header = "\n".join(text.splitlines()[:20])
        if "SSOT Domain" not in header:
            violations.append(path.as_posix())
    return violations


def check_deprecated_imports(root: Path, deprecated_modules: List[str]) -> Dict[str, List[str]]:
    findings: Dict[str, List[str]] = {}
    if not deprecated_modules:
        return findings
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for module in deprecated_modules:
            if f"import {module}" in text or f"from {module} import" in text:
                findings.setdefault(path.as_posix(), []).append(module)
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="SSOT compliance linter")
    parser.add_argument("--root", default="src/core/ssot", help="Root to scan for SSOT headers")
    parser.add_argument(
        "--deprecated-config",
        default="config/ssot_deprecated_modules.txt",
        help="Optional list of deprecated modules",
    )
    args = parser.parse_args()

    ssot_violations = check_ssot_headers(Path(args.root))
    deprecated_modules = load_deprecated_modules(Path(args.deprecated_config))
    deprecated_imports = check_deprecated_imports(Path("src"), deprecated_modules)

    if ssot_violations:
        print(f"❌ FAILED: Found {len(ssot_violations)} missing SSOT headers")
        for path in ssot_violations:
            print(f"  - {path}")
        return 1

    if deprecated_imports:
        print(f"❌ FAILED: Found {len(deprecated_imports)} deprecated imports")
        for path, modules in deprecated_imports.items():
            print(f"  - {path}: {', '.join(modules)}")
        return 1

    print("✅ PASSED: No SSOT violations found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
