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
EXCLUDED_PARTS = {
    "vendor",
    "generated",
    "build",
    "dist",
    "cache",
    "lock",
    ".venv",
    "node_modules",
}


def _load_registry() -> tuple[list[object] | None, list[str]]:
    errors: list[str] = []
    if not REGISTRY_PATH.exists():
        return None, [f"Missing registry file: {REGISTRY_PATH}"]

    try:
        data = yaml.safe_load(REGISTRY_PATH.read_text())
    except yaml.YAMLError as exc:
        return None, [f"Invalid YAML in {REGISTRY_PATH}: {exc}"]

    if data is None:
        data = {}

    if not isinstance(data, dict):
        return None, ["Registry root must be an object with top-level key 'files'"]

    files = data.get("files")
    if files is None:
        return None, ["Registry must define a top-level 'files' list"]
    if not isinstance(files, list):
        return None, ["Registry key 'files' must be a list"]

    return files, errors


def _is_excluded(path: Path) -> bool:
    return any(part.lower() in EXCLUDED_PARTS for part in path.parts)


def _validate_entry_shape(entry: object, index: int) -> tuple[list[str], dict | None]:
    if not isinstance(entry, dict):
        return [f"Entry index {index} must be an object, got {type(entry).__name__}"], None

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
    entry_id = entry.get("id", f"index-{index}")
    errors = [f"Entry '{entry_id}' missing field '{name}'" for name in missing]
    return errors, entry


def _extract_registry_id(file_path: Path) -> str | None:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    match = REGISTRY_PATTERN.search(text[:500])
    return match.group(1) if match else None


def run() -> int:
    errors: list[str] = []
    entries, load_errors = _load_registry()
    errors.extend(load_errors)

    if entries is None:
        print("❌ Recovery registry validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    ids: set[str] = set()
    for index, raw_entry in enumerate(entries):
        shape_errors, entry = _validate_entry_shape(raw_entry, index)
        errors.extend(shape_errors)
        if entry is None:
            continue

        entry_id_obj = entry.get("id")
        if not isinstance(entry_id_obj, str) or not entry_id_obj.strip():
            errors.append(f"Entry index {index} has invalid 'id'; expected non-empty string")
            entry_id = f"index-{index}"
        else:
            entry_id = entry_id_obj

        if entry_id in ids:
            errors.append(f"Duplicate registry id '{entry_id}'")
        ids.add(entry_id)

        file_rel_obj = entry.get("file")
        if not isinstance(file_rel_obj, str) or not file_rel_obj.strip():
            errors.append(f"Entry '{entry_id}' has invalid 'file'; expected non-empty string path")
            continue
        file_rel = file_rel_obj

        file_path = ROOT / file_rel
        if _is_excluded(file_path):
            errors.append(f"Registry entry '{entry_id}' points to excluded path '{file_rel}'")
            continue

        if not file_path.exists():
            errors.append(f"Entry '{entry_id}' file not found: {file_rel}")
            continue

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
