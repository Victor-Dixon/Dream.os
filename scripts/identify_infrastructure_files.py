#!/usr/bin/env python3
"""
Identify Infrastructure-Related Files Across Codebase
====================================================

Scans the codebase to identify all infrastructure-related files that need SSOT tagging.
Infrastructure domain includes: infrastructure services, adapters, utilities, tools.

Author: Agent-2
Date: 2025-12-14
"""

import json
import sys
from pathlib import Path
from typing import List, Set


def get_file_line_count(file_path: Path) -> int:
    """Get line count for a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0


def has_ssot_tag(file_path: Path) -> bool:
    """Check if file has SSOT tag."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return 'SSOT Domain' in content or '<!-- SSOT' in content
    except Exception:
        return False


def is_infrastructure_related(file_path: Path) -> bool:
    """Determine if file is infrastructure-related based on path and content."""
    path_str = str(file_path).lower()

    # Infrastructure directory files
    if 'infrastructure' in path_str:
        return True

    # Core infrastructure files
    infrastructure_keywords = [
        'infrastructure',
        'browser',
        'persistence',
        'logging',
        'database',
        'connection',
        'adapter',
        'service_adapter',
        'infrastructure_health',
        'unified_browser',
        'database_connection',
        'persistence_models',
        'log_handlers',
        'log_formatters',
    ]

    for keyword in infrastructure_keywords:
        if keyword in path_str:
            return True

    return False


def scan_infrastructure_files(base_dir: Path) -> List[dict]:
    """Scan for infrastructure-related files."""
    infrastructure_files = []
    scanned = 0

    print(f"🔍 Scanning {base_dir} for infrastructure-related files...")

    for py_file in base_dir.rglob("*.py"):
        scanned += 1
        if scanned % 100 == 0:
            print(f"   Scanned {scanned} files...")

        if is_infrastructure_related(py_file):
            line_count = get_file_line_count(py_file)
            has_tag = has_ssot_tag(py_file)

            infrastructure_files.append({
                "path": str(py_file.relative_to(base_dir)),
                "full_path": str(py_file),
                "line_count": line_count,
                "has_ssot_tag": has_tag,
                "needs_tagging": not has_tag
            })

    return infrastructure_files


def categorize_files(files: List[dict]) -> dict:
    """Categorize files by directory."""
    categories = {
        "infrastructure_directory": [],
        "core_infrastructure": [],
        "services_infrastructure": [],
        "other_infrastructure": []
    }

    for file_info in files:
        path = file_info["path"]
        if path.startswith("src/infrastructure/"):
            categories["infrastructure_directory"].append(file_info)
        elif path.startswith("src/core/"):
            categories["core_infrastructure"].append(file_info)
        elif path.startswith("src/services/"):
            categories["services_infrastructure"].append(file_info)
        else:
            categories["other_infrastructure"].append(file_info)

    return categories


def main():
    """Main entry point."""
    base_dir = Path(".")
    if not base_dir.exists():
        print(f"❌ Base directory not found: {base_dir}")
        sys.exit(1)

    print("=" * 80)
    print("🔍 INFRASTRUCTURE FILES IDENTIFICATION")
    print("=" * 80)
    print()

    # Scan infrastructure files
    infrastructure_files = scan_infrastructure_files(base_dir)

    # Categorize
    categories = categorize_files(infrastructure_files)

    # Statistics
    total_files = len(infrastructure_files)
    tagged_files = sum(1 for f in infrastructure_files if f["has_ssot_tag"])
    untagged_files = total_files - tagged_files

    print()
    print("=" * 80)
    print("📊 INFRASTRUCTURE FILES SUMMARY")
    print("=" * 80)
    print(f"Total Infrastructure Files: {total_files}")
    print(
        f"Files with SSOT Tags: {tagged_files} ({tagged_files/total_files*100:.1f}%)")
    print(
        f"Files Needing Tags: {untagged_files} ({untagged_files/total_files*100:.1f}%)")
    print()

    print("📁 By Category:")
    print(
        f"  Infrastructure Directory: {len(categories['infrastructure_directory'])} files")
    print(
        f"  Core Infrastructure: {len(categories['core_infrastructure'])} files")
    print(
        f"  Services Infrastructure: {len(categories['services_infrastructure'])} files")
    print(
        f"  Other Infrastructure: {len(categories['other_infrastructure'])} files")
    print()

    # Files needing tagging
    files_needing_tags = [
        f for f in infrastructure_files if f["needs_tagging"]]

    if files_needing_tags:
        print("=" * 80)
        print(f"📋 FILES NEEDING SSOT TAGS ({len(files_needing_tags)} files)")
        print("=" * 80)
        print()

        # Group by category
        for category_name, category_files in categories.items():
            untagged = [f for f in category_files if f["needs_tagging"]]
            if untagged:
                print(
                    f"### {category_name.replace('_', ' ').title()}: {len(untagged)} files")
                # Show first 20
                for file_info in sorted(untagged, key=lambda x: x["path"])[:20]:
                    print(
                        f"  - {file_info['path']} ({file_info['line_count']} lines)")
                if len(untagged) > 20:
                    print(f"  ... and {len(untagged) - 20} more files")
                print()

    # Save results
    output_file = Path("docs/infrastructure_files_scan_2025-12-14.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    results = {
        "scan_date": "2025-12-14",
        "total_files": total_files,
        "tagged_files": tagged_files,
        "untagged_files": untagged_files,
        "categories": {
            category: {
                "total": len(files),
                "tagged": sum(1 for f in files if f["has_ssot_tag"]),
                "untagged": sum(1 for f in files if not f["has_ssot_tag"]),
                "files": files
            }
            for category, files in categories.items()
        },
        "files_needing_tags": files_needing_tags
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to: {output_file}")
    print()
    print(f"📋 Next Steps:")
    print(f"  1. Review files needing tags: {len(files_needing_tags)} files")
    print(f"  2. Prioritize tagging batches")
    print(f"  3. Begin systematic SSOT tagging")
    print()


if __name__ == "__main__":
    main()
