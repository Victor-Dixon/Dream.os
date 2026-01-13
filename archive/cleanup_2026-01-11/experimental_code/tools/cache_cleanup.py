#!/usr/bin/env python3
"""
Cache Cleanup Tool - Phase 4 Storage Optimization
================================================

Cleans up cache files and temporary data for storage optimization.

<!-- SSOT Domain: maintenance -->

Navigation References:
├── Related Files:
│   ├── Repository Monitor → src/services/repository_monitor.py
│   ├── Project Scanner → tools/project_scanner.py
│   ├── Phase 4 Plan → phase4_consolidation_plan_draft.json
│   └── Archive Strategy → DIRECTORY_AUDIT_BACKUP_STRATEGY.md
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Cleanup Guide → docs/maintenance/cache_cleanup.md
│   └── Storage Optimization → docs/infrastructure/storage_optimization.md
└── Testing:
    └── Validation Tests → tests/validation/test_cache_cleanup.py

Features:
- Removes Python bytecode files (.pyc, __pycache__)
- Cleans up linting caches (.ruff_cache)
- Removes temporary files and directories
- Provides storage savings analysis
- Safe cleanup with confirmation

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class CacheCleanup:
    """
    Comprehensive cache and temporary file cleanup system.

    Targets:
    - Python bytecode (__pycache__ directories, .pyc files)
    - Linting caches (.ruff_cache, .mypy_cache)
    - IDE caches (.vscode, .idea)
    - OS temporary files
    - Build artifacts (if safe to remove)
    """

    def __init__(self, repository_path: str = "."):
        self.repository_path = Path(repository_path)
        self.cleanup_targets = {
            "python_cache": {
                "patterns": ["__pycache__", "*.pyc", "*.pyo"],
                "description": "Python bytecode cache files"
            },
            "linting_cache": {
                "patterns": [".ruff_cache", ".mypy_cache", ".tox", ".coverage"],
                "description": "Linting and testing caches"
            },
            "ide_cache": {
                "patterns": [".vscode", ".idea", "*.swp", "*.swo", "*~"],
                "description": "IDE and editor temporary files"
            },
            "os_temp": {
                "patterns": ["Thumbs.db", ".DS_Store", "desktop.ini"],
                "description": "OS-generated temporary files"
            },
            "build_artifacts": {
                "patterns": ["build", "dist", "*.egg-info", ".pytest_cache"],
                "description": "Build and packaging artifacts",
                "requires_confirmation": True
            }
        }

    def analyze_cache_files(self) -> Dict[str, Any]:
        """Analyze cache files and temporary data for cleanup."""
        analysis = {
            "total_files": 0,
            "total_size_mb": 0,
            "categories": {},
            "large_files": [],
            "old_files": []
        }

        for category, config in self.cleanup_targets.items():
            category_files = []
            category_size = 0

            for pattern in config["patterns"]:
                try:
                    if "*" in pattern:
                        # Glob pattern for files
                        for file_path in self.repository_path.rglob(pattern):
                            if file_path.is_file():
                                try:
                                    size = file_path.stat().st_size
                                    category_files.append({
                                        "path": str(file_path.relative_to(self.repository_path)),
                                        "size_bytes": size,
                                        "category": category
                                    })
                                    category_size += size
                                    analysis["total_files"] += 1
                                    analysis["total_size_mb"] += size / 1024 / 1024

                                    # Track large files
                                    if size > 10 * 1024 * 1024:  # Over 10MB
                                        analysis["large_files"].append({
                                            "path": str(file_path.relative_to(self.repository_path)),
                                            "size_mb": size / 1024 / 1024,
                                            "category": category
                                        })

                                except (OSError, IOError):
                                    continue
                    else:
                        # Directory pattern
                        for dir_path in self.repository_path.rglob(pattern):
                            if dir_path.is_dir():
                                try:
                                    # Calculate directory size
                                    total_size = 0
                                    file_count = 0
                                    for root, dirs, files in os.walk(dir_path):
                                        for file in files:
                                            try:
                                                total_size += os.path.getsize(os.path.join(root, file))
                                                file_count += 1
                                            except (OSError, IOError):
                                                continue

                                    if total_size > 0:
                                        category_files.append({
                                            "path": str(dir_path.relative_to(self.repository_path)),
                                            "size_bytes": total_size,
                                            "file_count": file_count,
                                            "category": category,
                                            "is_directory": True
                                        })
                                        category_size += total_size
                                        analysis["total_files"] += file_count
                                        analysis["total_size_mb"] += total_size / 1024 / 1024

                                except (OSError, IOError):
                                    continue
                except Exception as e:
                    # Skip patterns that cause errors (missing directories, etc.)
                    continue

            analysis["categories"][category] = {
                "files": category_files,
                "total_size_mb": category_size / 1024 / 1024,
                "file_count": len(category_files),
                "description": config["description"],
                "requires_confirmation": config.get("requires_confirmation", False)
            }

        return analysis

    def cleanup_cache_files(self, categories: List[str] = None,
                           skip_confirmation: bool = False) -> Dict[str, Any]:
        """Clean up cache files in specified categories."""
        logger.info("🧹 Starting cache cleanup...")

        analysis = self.analyze_cache_files()

        if categories is None:
            categories = list(self.cleanup_targets.keys())

        # Filter categories
        categories_to_clean = []
        for category in categories:
            if category in analysis["categories"]:
                cat_data = analysis["categories"][category]
                if cat_data["file_count"] > 0:
                    if cat_data.get("requires_confirmation") and not skip_confirmation:
                        print(f"⚠️  Category '{category}' requires confirmation to clean:")
                        print(f"   {cat_data['description']}")
                        print(f"   Contains {cat_data['file_count']} items, {cat_data['total_size_mb']:.1f} MB")
                        response = input("   Clean this category? (y/N): ").strip().lower()
                        if response != 'y':
                            continue
                    categories_to_clean.append(category)

        # Perform cleanup
        cleaned_files = []
        total_cleaned_size = 0

        for category in categories_to_clean:
            cat_data = analysis["categories"][category]
            logger.info(f"Cleaning {category}: {cat_data['file_count']} items, {cat_data['total_size_mb']:.1f} MB")

            for item in cat_data["files"]:
                path = self.repository_path / item["path"]

                try:
                    if item.get("is_directory", False):
                        shutil.rmtree(path)
                        cleaned_files.append({
                            "path": item["path"],
                            "size_bytes": item["size_bytes"],
                            "category": category,
                            "type": "directory"
                        })
                    else:
                        path.unlink()
                        cleaned_files.append({
                            "path": item["path"],
                            "size_bytes": item["size_bytes"],
                            "category": category,
                            "type": "file"
                        })

                    total_cleaned_size += item["size_bytes"]

                except Exception as e:
                    logger.error(f"Failed to remove {item['path']}: {e}")

        result = {
            "cleaned_files": len(cleaned_files),
            "total_size_cleaned_mb": total_cleaned_size / 1024 / 1024,
            "categories_cleaned": categories_to_clean,
            "files_detail": cleaned_files,
            "status": "completed"
        }

        logger.info(f"✅ Cache cleanup completed: {result['cleaned_files']} items, {result['total_size_cleaned_mb']:.1f} MB cleaned")
        return result

    def get_cleanup_recommendations(self) -> Dict[str, Any]:
        """Get cleanup recommendations based on analysis."""
        analysis = self.analyze_cache_files()

        recommendations = {
            "safe_cleanup": [],
            "caution_cleanup": [],
            "manual_review": [],
            "total_potential_savings_mb": 0
        }

        for category, data in analysis["categories"].items():
            if data["file_count"] == 0:
                continue

            size_mb = data["total_size_mb"]

            if category in ["python_cache", "linting_cache", "os_temp"]:
                recommendations["safe_cleanup"].append({
                    "category": category,
                    "description": data["description"],
                    "size_mb": size_mb,
                    "file_count": data["file_count"],
                    "reason": "Safe to remove - regenerated automatically"
                })
            elif category in ["ide_cache"]:
                recommendations["caution_cleanup"].append({
                    "category": category,
                    "description": data["description"],
                    "size_mb": size_mb,
                    "file_count": data["file_count"],
                    "reason": "May affect IDE settings - backup recommended"
                })
            elif category in ["build_artifacts"]:
                recommendations["manual_review"].append({
                    "category": category,
                    "description": data["description"],
                    "size_mb": size_mb,
                    "file_count": data["file_count"],
                    "reason": "Build artifacts - verify not needed for deployment"
                })

            recommendations["total_potential_savings_mb"] += size_mb

        return recommendations


def main():
    """Main cleanup function."""
    cleanup = CacheCleanup()

    print("🔍 Analyzing cache files...")
    analysis = cleanup.analyze_cache_files()

    print(f"📊 Found {analysis['total_files']} cache files, {analysis['total_size_mb']:.1f} MB total")
    print(f"📂 Categories found: {len(analysis['categories'])}")

    for category, data in analysis["categories"].items():
        if data["file_count"] > 0:
            print(f"  • {category}: {data['file_count']} items, {data['total_size_mb']:.1f} MB")

    print("\n💡 Cleanup Recommendations:")
    recommendations = cleanup.get_cleanup_recommendations()

    if recommendations["safe_cleanup"]:
        print("🟢 Safe to clean automatically:")
        for rec in recommendations["safe_cleanup"]:
            print(f"  • {rec['category']}: {rec['size_mb']:.1f} MB")

    if recommendations["caution_cleanup"]:
        print("🟡 Clean with caution:")
        for rec in recommendations["caution_cleanup"]:
            print(f"  • {rec['category']}: {rec['size_mb']:.1f} MB")

    if recommendations["manual_review"]:
        print("🔴 Manual review required:")
        for rec in recommendations["manual_review"]:
            print(f"  • {rec['category']}: {rec['size_mb']:.1f} MB")

    print(f"💾 Total potential savings: {recommendations['total_potential_savings_mb']:.1f} MB")

    # Auto cleanup with safe categories only
    categories = ["python_cache", "linting_cache", "os_temp"]

    print(f"🧹 Auto-cleaning safe categories: {', '.join(categories)}")
    result = cleanup.cleanup_cache_files(categories, skip_confirmation=True)

    print("✅ Cleanup completed!")
    print(f"🗑️  Removed {result['cleaned_files']} items")
    print(f"💾 Space saved: {result['total_size_cleaned_mb']:.1f} MB")
if __name__ == "__main__":
    main()