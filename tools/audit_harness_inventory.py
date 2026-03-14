"""Inventory analysis for the audit harness (SSOT)."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from tools.audit_harness_utils import count_lines, file_hash


def inventory_files(project_root: Path, timestamp: str, roots: List[str], output_file: str) -> Dict[str, Any]:
    """Create comprehensive file inventory with metadata."""
    print("📊 Generating file inventory...")

    inventory: Dict[str, Any] = {
        "timestamp": timestamp,
        "command": f"python tools/audit_harness.py inventory --roots {' '.join(roots)} --out {output_file}",
        "roots": roots,
        "summary": {},
        "files": [],
    }

    total_files = 0
    total_size = 0
    last_root_files: List[Dict[str, Any]] = []

    for root in roots:
        root_path = project_root / root
        if not root_path.exists():
            print(f"⚠️ Root {root} does not exist")
            continue

        root_files: List[Dict[str, Any]] = []
        root_size = 0
        root_count = 0

        for py_file in root_path.rglob("*.py"):
            if not py_file.is_file():
                continue
            try:
                stat = py_file.stat()
                file_info = {
                    "path": str(py_file.relative_to(project_root)),
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "root": root,
                    "lines": count_lines(py_file),
                    "hash": file_hash(py_file),
                }
                root_files.append(file_info)
                root_size += stat.st_size
                root_count += 1
                total_files += 1
                total_size += stat.st_size
            except OSError as exc:
                print(f"⚠️ Error processing {py_file}: {exc}")

        inventory["summary"][root] = {
            "file_count": root_count,
            "total_size": root_size,
            "avg_file_size": root_size / root_count if root_count > 0 else 0,
        }
        last_root_files = root_files

    inventory["summary"]["TOTAL"] = {
        "file_count": total_files,
        "total_size": total_size,
        "avg_file_size": total_size / total_files if total_files > 0 else 0,
    }

    inventory["files"] = last_root_files

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(inventory, handle, indent=2, ensure_ascii=False)

    print(f"✅ Inventory saved to {output_file}")
    print(f"   Total files: {total_files}")
    print(f"   Total size: {total_size:,} bytes")

    return inventory
