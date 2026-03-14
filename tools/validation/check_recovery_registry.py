# Header-Variant: full
# Owner: @dreamos/platform
# Purpose: check_recovery_registry module.
# SSOT: docs/recovery/recovery_registry.yaml#recovery-registry-validator
# @registry docs/recovery/recovery_registry.yaml#recovery-registry-validator

"""
@file
@summary Validate SSOT recovery registry entries and @registry header pointers.
@registry docs/recovery/recovery_registry.yaml#recovery-registry-validator
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "docs/recovery/recovery_registry.yaml"
REGISTRY_PATTERN = re.compile(
    r"@registry\s+docs/recovery/recovery_registry\.yaml#([a-z0-9-]+)"
)
EXCLUDED_PARTS = {"vendor", "generated", "build", "dist", "cache", "lock", ".venv", "node_modules"}
HEADER_REQUIRED_SUFFIXES = {".py", ".sh", ".js", ".ts"}


def _load_registry() -> list[dict]:
    if not REGISTRY_PATH.exists():
        raise FileNotFoundError(f"Missing registry file: {REGISTRY_PATH}")

    data = yaml.safe_load(REGISTRY_PATH.read_text()) or {}
    files = data.get("files", [])
    if not isinstance(files, list):
        raise ValueError("Registry must define a top-level 'files' list")
    return files


def _is_excluded(path: Path) -> bool:
    return any(part.lower() in EXCLUDED_PARTS for part in path.parts)


def _validate_entry_shape(entry: dict) -> list[str]:
    required = {
        "id",
        "file",
        "purpose",
        "owns",
        "does_not_own",
        "inputs",
        "outputs",
        "dependencies",
        "used_by",
        "status",
        "last_updated",
        "recovery_notes",
    }
    missing = sorted(required - set(entry.keys()))
    return [f"Entry '{entry.get('id', '<missing-id>')}' missing field '{name}'" for name in missing]


def _extract_registry_id(file_path: Path) -> str | None:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    match = REGISTRY_PATTERN.search(text[:500])
    return match.group(1) if match else None


def run() -> int:
    errors: list[str] = []
    try:
        entries = _load_registry()
    except Exception as exc:
        print(f"❌ {exc}")
        return 1

    ids: set[str] = set()
    for entry in entries:
        errors.extend(_validate_entry_shape(entry))
        entry_id = entry.get("id")
        if entry_id in ids:
            errors.append(f"Duplicate registry id '{entry_id}'")
        ids.add(entry_id)

        file_rel = entry.get("file", "")
        file_path = ROOT / file_rel
        if _is_excluded(file_path):
            errors.append(f"Registry entry '{entry_id}' points to excluded path '{file_rel}'")
            continue

        if not file_path.exists():
            errors.append(f"Entry '{entry_id}' file not found: {file_rel}")
            continue

        if file_path.suffix in HEADER_REQUIRED_SUFFIXES:
            pointed_id = _extract_registry_id(file_path)
            if not pointed_id:
                errors.append(f"Core file missing @registry pointer: {file_rel}")
                continue
            if pointed_id != entry_id:
                errors.append(
                    f"Pointer mismatch in {file_rel}: header='{pointed_id}' registry='{entry_id}'"
                )

    if errors:
        print("❌ Recovery registry validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("✅ Recovery registry validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(run())
