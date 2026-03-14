"""Archive analysis for the audit harness (SSOT)."""

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def analyze_archive(project_root: Path, timestamp: str, root: str, output_file: str) -> Dict[str, Any]:
    """Analyze archive directory for retention candidates."""
    print("📦 Analyzing archive contents...")

    analysis: Dict[str, Any] = {
        "timestamp": timestamp,
        "command": f"python tools/audit_harness.py archive --root {root} --out {output_file}",
        "root": root,
        "buckets": {},
        "large_files": [],
        "old_files": [],
    }

    root_path = project_root / root
    if not root_path.exists():
        print(f"⚠️ Root {root} does not exist")
        return analysis

    now = datetime.now()
    buckets = {
        "0-90d": [],
        "90-180d": [],
        "180-365d": [],
        "365d+": [],
    }

    large_files = []
    old_files = []

    for py_file in root_path.rglob("*.py"):
        try:
            stat = py_file.stat()
            modified = datetime.fromtimestamp(stat.st_mtime)
            age_days = (now - modified).days
            size = stat.st_size

            file_info = {
                "path": str(py_file.relative_to(project_root)),
                "size": size,
                "modified": modified.isoformat(),
                "age_days": age_days,
            }

            if age_days <= 90:
                buckets["0-90d"].append(file_info)
            elif age_days <= 180:
                buckets["90-180d"].append(file_info)
            elif age_days <= 365:
                buckets["180-365d"].append(file_info)
            else:
                buckets["365d+"].append(file_info)

            if size > 100 * 1024:
                large_files.append(file_info)

            if age_days > 365:
                old_files.append(file_info)

        except OSError as exc:
            print(f"⚠️ Error analyzing {py_file}: {exc}")

    analysis["buckets"] = {k: len(v) for k, v in buckets.items()}
    analysis["large_files"] = sorted(large_files, key=lambda x: x["size"], reverse=True)[:10]
    analysis["old_files"] = sorted(old_files, key=lambda x: x["age_days"], reverse=True)[:10]

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["Path", "Size", "Modified", "Age_Days", "Bucket"])

        for bucket_name, files in buckets.items():
            for file_info in files:
                writer.writerow(
                    [
                        file_info["path"],
                        file_info["size"],
                        file_info["modified"],
                        file_info["age_days"],
                        bucket_name,
                    ]
                )

    print(f"✅ Archive analysis saved to {output_file}")
    print(f"   Files by age bucket: {analysis['buckets']}")
    print(f"   Large files (>100KB): {len(large_files)}")
    print(f"   Very old files (>365d): {len(old_files)}")

    return analysis
