"""Duplication analysis for the audit harness (SSOT)."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from collections import defaultdict


def analyze_duplication(project_root: Path, timestamp: str, roots: List[str], output_file: str) -> Dict[str, Any]:
    """Analyze code duplication patterns."""
    print("🔍 Analyzing code duplication...")

    analysis: Dict[str, Any] = {
        "timestamp": timestamp,
        "command": f"python tools/audit_harness.py dup --roots {' '.join(roots)} --out {output_file}",
        "roots": roots,
        "patterns": {},
        "hotspots": [],
    }

    patterns = {
        "__init__": {
            "pattern": r"def __init__\(self.*?\):",
            "description": "Constructor methods",
        },
        "logger_setup": {
            "pattern": r"self\.logger\s*=\s*logging\.getLogger",
            "description": "Logger initialization",
        },
        "import_typing": {
            "pattern": r"from typing import",
            "description": "Typing imports",
        },
        "try_except": {
            "pattern": r"try:\s*$[\s\S]*?except.*?:",
            "description": "Exception handling blocks",
            "flags": re.MULTILINE | re.DOTALL,
        },
    }

    all_files: List[Path] = []
    for root in roots:
        root_path = project_root / root
        if root_path.exists():
            all_files.extend(list(root_path.rglob("*.py")))

    for pattern_name, pattern_info in patterns.items():
        pattern_data = {
            "description": pattern_info["description"],
            "regex": pattern_info["pattern"],
            "occurrences": [],
            "total_count": 0,
        }

        flags = pattern_info.get("flags", 0)

        for py_file in all_files:
            try:
                with open(py_file, "r", encoding="utf-8", errors="ignore") as handle:
                    content = handle.read()

                matches = re.findall(pattern_info["pattern"], content, flags)
                if matches:
                    pattern_data["occurrences"].append(
                        {
                            "file": str(py_file.relative_to(project_root)),
                            "count": len(matches),
                            "lines": sorted(
                                set(
                                    re.findall(
                                        rf".*?{pattern_info['pattern']}.*?$",
                                        content,
                                        re.MULTILINE,
                                    )
                                )
                            ),
                        }
                    )
                    pattern_data["total_count"] += len(matches)

            except OSError as exc:
                print(f"⚠️ Error analyzing {py_file}: {exc}")

        analysis["patterns"][pattern_name] = pattern_data

    file_counts = defaultdict(int)
    for pattern_data in analysis["patterns"].values():
        for occurrence in pattern_data["occurrences"]:
            file_counts[occurrence["file"]] += occurrence["count"]

    analysis["hotspots"] = [
        {"file": file, "total_patterns": count}
        for file, count in sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    import_typing_occurrences = analysis["patterns"].get("import_typing", {}).get("occurrences", [])
    redundant_typing_files = [
        occurrence["file"] for occurrence in import_typing_occurrences if occurrence["count"] > 1
    ]
    analysis["import_standardization"] = {
        "redundant_typing_files": sorted(redundant_typing_files),
        "redundant_typing_file_count": len(redundant_typing_files),
    }

    total_patterns = sum(p["total_count"] for p in analysis["patterns"].values())
    total_files = len(all_files)
    analysis["duplication_estimate"] = {
        "total_patterns": total_patterns,
        "files_analyzed": total_files,
        "avg_patterns_per_file": total_patterns / total_files if total_files > 0 else 0,
        "high_duplication_files": len([f for f in file_counts.values() if f > 5]),
    }

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(analysis, handle, indent=2, ensure_ascii=False)

    print(f"✅ Duplication analysis saved to {output_file}")
    print(f"   Patterns analyzed: {len(patterns)}")
    print(
        f"   Files with high duplication: {analysis['duplication_estimate']['high_duplication_files']}"
    )
    print(
        "   Files with redundant typing imports: "
        f"{analysis['import_standardization']['redundant_typing_file_count']}"
    )

    return analysis
