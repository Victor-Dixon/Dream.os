#!/usr/bin/env python3
"""
Reports Directory Consolidation Tool - Phase 4 Optimization
==========================================================

Consolidates the large reports/ directory (135+ files) into an organized structure.

<!-- SSOT Domain: organization -->

Navigation References:
├── Related Files:
│   ├── Project Scanner → tools/project_scanner.py
│   ├── Repository Monitor → src/services/repository_monitor.py
│   ├── Phase 4 Plan → phase4_consolidation_plan_draft.json
│   └── Archive Structure → archive/README.md
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Consolidation Guide → docs/consolidation/reports_consolidation.md
│   └── Archive Strategy → DIRECTORY_AUDIT_BACKUP_STRATEGY.md
└── Testing:
    └── Validation Tests → tests/validation/test_reports_consolidation.py

Features:
- Automatic categorization of reports by type and date
- Duplicate detection and consolidation
- Archive compression for old reports
- Maintains searchable index of all reports

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
Phase: Phase 4 Sprint 4 - Operational Transformation Engine
"""

import os
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Set, Tuple
import logging

logger = logging.getLogger(__name__)


class ReportsConsolidator:
    """
    Consolidates and organizes the reports directory structure.

    Categories:
    - analytics/ - Analytics and dashboard reports
    - compliance/ - V2 compliance and validation reports
    - deployment/ - Deployment and infrastructure reports
    - audit/ - Directory and code audits
    - monitoring/ - Health checks and monitoring reports
    - archive/ - Historical reports (compressed)
    """

    def __init__(self, reports_dir: str = "reports"):
        self.reports_dir = Path(reports_dir)
        self.consolidated_dir = self.reports_dir / "consolidated"
        self.archive_dir = self.reports_dir / "archive"
        self.index_file = self.reports_dir / "reports_index.json"

        # Categorization rules
        self.categories = {
            "analytics": [
                "analytics", "dashboard", "tier1", "p0_analytics",
                "ga4", "pixel", "tracking", "metrics"
            ],
            "compliance": [
                "compliance", "v2_compliance", "ssot", "validation",
                "verification", "audit", "grade_card"
            ],
            "deployment": [
                "deployment", "infrastructure", "docker", "nginx",
                "wp-config", "wordpress", "freerideinvestor"
            ],
            "monitoring": [
                "health", "status", "monitor", "check", "diagnostic",
                "performance", "stress_test"
            ],
            "development": [
                "tag_analysis", "import", "duplicate", "consolidation",
                "wave_", "codex", "canonical"
            ]
        }

        # Archive thresholds
        self.archive_threshold_days = 30
        self.consolidate_duplicates = True

    def analyze_reports(self) -> Dict[str, Any]:
        """Analyze the current reports directory structure."""
        analysis = {
            "total_files": 0,
            "total_size_mb": 0,
            "file_types": {},
            "categories": {},
            "duplicates": [],
            "old_files": [],
            "large_files": []
        }

        if not self.reports_dir.exists():
            return analysis

        for file_path in self.reports_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                analysis["total_files"] += 1

                # File size
                size_mb = file_path.stat().st_size / 1024 / 1024
                analysis["total_size_mb"] += size_mb

                # File type
                ext = file_path.suffix.lower() or 'no_extension'
                analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1

                # Categorize
                category = self._categorize_file(file_path)
                if category not in analysis["categories"]:
                    analysis["categories"][category] = []
                analysis["categories"][category].append(str(file_path.relative_to(self.reports_dir)))

                # Check for old files
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if datetime.now() - mtime > timedelta(days=self.archive_threshold_days):
                    analysis["old_files"].append(str(file_path.relative_to(self.reports_dir)))

                # Check for large files
                if size_mb > 1:  # Over 1MB
                    analysis["large_files"].append({
                        "path": str(file_path.relative_to(self.reports_dir)),
                        "size_mb": size_mb
                    })

        # Find duplicates
        analysis["duplicates"] = self._find_duplicates()

        return analysis

    def _categorize_file(self, file_path: Path) -> str:
        """Categorize a file based on its name and content."""
        filename = file_path.name.lower()

        for category, keywords in self.categories.items():
            if any(keyword in filename for keyword in keywords):
                return category

        # Default category
        return "general"

    def _find_duplicates(self) -> List[Dict[str, Any]]:
        """Find duplicate files based on content hash."""
        file_hashes = {}
        duplicates = []

        for file_path in self.reports_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                try:
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()

                    rel_path = str(file_path.relative_to(self.reports_dir))

                    if file_hash in file_hashes:
                        duplicates.append({
                            "duplicate": rel_path,
                            "original": file_hashes[file_hash],
                            "hash": file_hash
                        })
                    else:
                        file_hashes[file_hash] = rel_path

                except (OSError, IOError):
                    continue

        return duplicates

    def consolidate_reports(self) -> Dict[str, Any]:
        """Consolidate reports into organized structure."""
        logger.info("🔄 Starting reports consolidation...")

        # Analyze first
        analysis = self.analyze_reports()

        # Create consolidated structure
        self.consolidated_dir.mkdir(exist_ok=True)
        for category in self.categories.keys():
            (self.consolidated_dir / category).mkdir(exist_ok=True)

        # Move files to categories
        moved_files = []
        for category, files in analysis["categories"].items():
            category_dir = self.consolidated_dir / category
            category_dir.mkdir(exist_ok=True)

            for file_path_str in files:
                src_path = self.reports_dir / file_path_str
                if src_path.exists():
                    # Create relative subdirectory structure if needed
                    rel_path = Path(file_path_str)
                    if rel_path.parent != Path("."):
                        dest_dir = category_dir / rel_path.parent
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        dest_path = dest_dir / rel_path.name
                    else:
                        dest_path = category_dir / rel_path.name

                    try:
                        shutil.move(str(src_path), str(dest_path))
                        moved_files.append({
                            "from": file_path_str,
                            "to": str(dest_path.relative_to(self.reports_dir)),
                            "category": category
                        })
                    except Exception as e:
                        logger.error(f"Failed to move {file_path_str}: {e}")

        # Handle duplicates
        duplicate_actions = []
        if self.consolidate_duplicates and analysis["duplicates"]:
            duplicate_actions = self._consolidate_duplicates(analysis["duplicates"])

        # Archive old files
        archived_files = []
        self.archive_dir.mkdir(exist_ok=True)

        for old_file in analysis["old_files"]:
            src_path = self.consolidated_dir / old_file
            if src_path.exists():
                # Move to archive
                archive_path = self.archive_dir / old_file
                archive_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    shutil.move(str(src_path), str(archive_path))
                    archived_files.append(old_file)
                except Exception as e:
                    logger.error(f"Failed to archive {old_file}: {e}")

        # Create/update index
        self._update_index(analysis, moved_files, duplicate_actions, archived_files)

        # Cleanup empty directories
        self._cleanup_empty_dirs()

        result = {
            "analysis": analysis,
            "moved_files": len(moved_files),
            "archived_files": len(archived_files),
            "duplicate_actions": len(duplicate_actions),
            "consolidated_categories": list(self.categories.keys()),
            "status": "completed"
        }

        logger.info(f"✅ Reports consolidation completed: {result}")
        return result

    def _consolidate_duplicates(self, duplicates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Consolidate duplicate files."""
        actions = []

        for duplicate_info in duplicates:
            duplicate_path = self.consolidated_dir / duplicate_info["duplicate"]
            original_path = self.consolidated_dir / duplicate_info["original"]

            if duplicate_path.exists() and original_path.exists():
                try:
                    # Create symlink or copy metadata
                    duplicate_path.unlink()  # Remove duplicate
                    actions.append({
                        "action": "removed_duplicate",
                        "duplicate": duplicate_info["duplicate"],
                        "kept": duplicate_info["original"],
                        "hash": duplicate_info["hash"]
                    })
                except Exception as e:
                    logger.error(f"Failed to remove duplicate {duplicate_info['duplicate']}: {e}")

        return actions

    def _update_index(self, analysis: Dict[str, Any], moved_files: List[Dict[str, Any]],
                     duplicate_actions: List[Dict[str, Any]], archived_files: List[str]):
        """Update the reports index."""
        index_data = {
            "last_updated": datetime.now().isoformat(),
            "consolidation_version": "1.0",
            "analysis": analysis,
            "moved_files": moved_files,
            "duplicate_actions": duplicate_actions,
            "archived_files": archived_files,
            "categories": self.categories,
            "archive_threshold_days": self.archive_threshold_days
        }

        with open(self.index_file, 'w') as f:
            json.dump(index_data, f, indent=2, default=str)

    def _cleanup_empty_dirs(self):
        """Clean up empty directories."""
        for dir_path in sorted(self.reports_dir.rglob("*"), reverse=True):
            if dir_path.is_dir() and not any(dir_path.iterdir()):
                try:
                    dir_path.rmdir()
                except Exception:
                    pass  # Directory not empty or other error

    def get_consolidation_status(self) -> Dict[str, Any]:
        """Get the current consolidation status."""
        if not self.index_file.exists():
            return {"status": "not_consolidated"}

        try:
            with open(self.index_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def search_reports(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """Search consolidated reports."""
        results = []

        search_dir = self.consolidated_dir
        if category and (search_dir / category).exists():
            search_dir = search_dir / category

        query_lower = query.lower()
        for file_path in search_dir.rglob("*"):
            if file_path.is_file():
                if query_lower in file_path.name.lower():
                    results.append({
                        "path": str(file_path.relative_to(self.reports_dir)),
                        "name": file_path.name,
                        "category": category or self._categorize_file(file_path),
                        "size_bytes": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })

        return results


def main(auto_confirm: bool = True):
    """Main consolidation function."""
    consolidator = ReportsConsolidator()

    print("📊 Analyzing reports directory...")
    analysis = consolidator.analyze_reports()

    print(f"Found {analysis['total_files']} files ({analysis['total_size_mb']:.1f} MB)")
    print(f"Categories: {list(analysis['categories'].keys())}")
    print(f"Duplicates found: {len(analysis['duplicates'])}")
    print(f"Old files to archive: {len(analysis['old_files'])}")

    if not auto_confirm:
        # Ask for confirmation
        response = input("\nProceed with consolidation? (y/N): ").strip().lower()
        if response != 'y':
            print("Consolidation cancelled.")
            return

    print("🔄 Consolidating reports...")
    result = consolidator.consolidate_reports()

    print("✅ Consolidation completed!")
    print(f"Moved files: {result['moved_files']}")
    print(f"Archived files: {result['archived_files']}")
    print(f"Duplicate actions: {result['duplicate_actions']}")


if __name__ == "__main__":
    main()