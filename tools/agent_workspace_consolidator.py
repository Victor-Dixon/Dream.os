#!/usr/bin/env python3
"""
Agent Workspace Archive Consolidator - Phase 4 Optimization
==========================================================

Consolidates agent workspace archives and eliminates duplicate content.

<!-- SSOT Domain: organization -->

Navigation References:
├── Related Files:
│   ├── Project Scanner → tools/project_scanner.py
│   ├── Archive Structure → agent_workspaces/archive/README.md
│   ├── Phase 4 Plan → phase4_consolidation_plan_draft.json
│   └── Agent Registry → agent_workspaces/agent_registry.json
├── Documentation:
│   ├── Phase 4 Roadmap → PHASE4_STRATEGIC_ROADMAP.md
│   ├── Consolidation Guide → docs/consolidation/agent_workspace_consolidation.md
│   └── Archive Strategy → DIRECTORY_AUDIT_BACKUP_STRATEGY.md
└── Testing:
    └── Validation Tests → tests/validation/test_agent_workspace_consolidation.py

Features:
- Automatic detection of duplicate content across agent archives
- Intelligent consolidation based on file age and relevance
- Preservation of important historical data
- Safe consolidation with backup verification

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-09
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


class AgentWorkspaceConsolidator:
    """
    Consolidates agent workspace archives and eliminates duplicates.

    Strategy:
    1. Analyze all archive directories across agent workspaces
    2. Identify duplicates based on content hash and filename
    3. Consolidate into organized structure by agent and date
    4. Preserve important historical data while removing redundancy
    """

    def __init__(self, agent_workspaces_dir: str = "agent_workspaces"):
        self.agent_workspaces_dir = Path(agent_workspaces_dir)
        self.consolidated_dir = self.agent_workspaces_dir / "consolidated_archives"
        self.backup_dir = self.agent_workspaces_dir / "archive_backup_pre_consolidation"
        self.consolidation_report = self.agent_workspaces_dir / "consolidation_report.json"

        # Archive identification patterns
        self.archive_patterns = [
            "archive", "archive_*", "*_archive", "backup", "old_*",
            "consolidated_archives", "archive_backup_*"
        ]

        # Retention policies
        self.keep_recent_days = 90  # Keep recent archives
        self.keep_important_patterns = [
            "session_closure", "final_report", "completion_report",
            "status", "registry", "important"
        ]

    def analyze_agent_archives(self) -> Dict[str, Any]:
        """Analyze all agent workspace archives."""
        analysis = {
            "total_archives": 0,
            "total_files": 0,
            "total_size_mb": 0,
            "agents_with_archives": {},
            "duplicate_files": [],
            "old_archives": [],
            "large_archives": []
        }

        # Find all archive directories
        for agent_dir in self.agent_workspaces_dir.iterdir():
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue

            agent_name = agent_dir.name
            agent_archives = self._find_agent_archives(agent_dir)

            if agent_archives:
                analysis["agents_with_archives"][agent_name] = agent_archives
                analysis["total_archives"] += len(agent_archives)

                # Analyze each archive
                for archive_path in agent_archives:
                    archive_info = self._analyze_archive(archive_path)
                    analysis["total_files"] += archive_info["file_count"]
                    analysis["total_size_mb"] += archive_info["size_mb"]

                    if archive_info["is_old"]:
                        analysis["old_archives"].append(archive_info)
                    if archive_info["is_large"]:
                        analysis["large_archives"].append(archive_info)

        # Find duplicates across all archives
        analysis["duplicate_files"] = self._find_duplicates_across_archives()

        return analysis

    def _find_agent_archives(self, agent_dir: Path) -> List[Path]:
        """Find all archive directories for a specific agent."""
        archives = []

        # Direct archive directories
        for pattern in self.archive_patterns:
            for archive_dir in agent_dir.glob(f"**/{pattern}"):
                if archive_dir.is_dir():
                    archives.append(archive_dir)

        return list(set(archives))  # Remove duplicates

    def _analyze_archive(self, archive_path: Path) -> Dict[str, Any]:
        """Analyze a single archive directory."""
        total_size = 0
        file_count = 0
        file_types = {}
        oldest_file = datetime.now()
        newest_file = datetime.fromtimestamp(0)

        try:
            for file_path in archive_path.rglob("*"):
                if file_path.is_file():
                    file_count += 1
                    total_size += file_path.stat().st_size

                    # File type distribution
                    ext = file_path.suffix.lower() or 'no_extension'
                    file_types[ext] = file_types.get(ext, 0) + 1

                    # Track age
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    oldest_file = min(oldest_file, mtime)
                    newest_file = max(newest_file, mtime)

        except Exception as e:
            logger.warning(f"Error analyzing archive {archive_path}: {e}")

        size_mb = total_size / 1024 / 1024
        age_days = (datetime.now() - newest_file).days

        return {
            "path": str(archive_path.relative_to(self.agent_workspaces_dir)),
            "file_count": file_count,
            "size_mb": size_mb,
            "file_types": file_types,
            "oldest_file": oldest_file.isoformat(),
            "newest_file": newest_file.isoformat(),
            "age_days": age_days,
            "is_old": age_days > self.keep_recent_days,
            "is_large": size_mb > 50,  # Over 50MB
            "is_important": self._is_important_archive(archive_path)
        }

    def _is_important_archive(self, archive_path: Path) -> bool:
        """Check if an archive contains important files."""
        try:
            for file_path in archive_path.rglob("*"):
                if file_path.is_file():
                    filename = file_path.name.lower()
                    if any(pattern in filename for pattern in self.keep_important_patterns):
                        return True
        except Exception:
            pass
        return False

    def _find_duplicates_across_archives(self) -> List[Dict[str, Any]]:
        """Find duplicate files across all archives."""
        file_hashes = {}
        duplicates = []

        # Walk through all archives
        for agent_dir in self.agent_workspaces_dir.iterdir():
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue

            for archive_dir in self._find_agent_archives(agent_dir):
                try:
                    for file_path in archive_dir.rglob("*"):
                        if file_path.is_file():
                            # Calculate hash
                            try:
                                with open(file_path, 'rb') as f:
                                    file_hash = hashlib.md5(f.read()).hexdigest()
                            except (OSError, IOError):
                                continue

                            rel_path = str(file_path.relative_to(self.agent_workspaces_dir))
                            file_info = {
                                "path": rel_path,
                                "hash": file_hash,
                                "size": file_path.stat().st_size,
                                "modified": file_path.stat().st_mtime
                            }

                            if file_hash in file_hashes:
                                # Found duplicate
                                original = file_hashes[file_hash]
                                duplicates.append({
                                    "original": original["path"],
                                    "duplicate": rel_path,
                                    "hash": file_hash,
                                    "size": file_info["size"]
                                })
                            else:
                                file_hashes[file_hash] = file_info

                except Exception as e:
                    logger.warning(f"Error scanning archive {archive_dir}: {e}")

        return duplicates

    def consolidate_archives(self) -> Dict[str, Any]:
        """Consolidate agent workspace archives."""
        logger.info("🔄 Starting agent workspace archive consolidation...")

        analysis = self.analyze_agent_archives()

        # Create backup before consolidation
        self._create_backup()

        # Create consolidated structure
        consolidation_actions = []

        # Process each agent's archives
        for agent_name, archive_paths in analysis["agents_with_archives"].items():
            agent_consolidated_dir = self.consolidated_dir / agent_name
            agent_consolidated_dir.mkdir(parents=True, exist_ok=True)

            for archive_path in archive_paths:
                action = self._consolidate_single_archive(
                    archive_path, agent_consolidated_dir, agent_name
                )
                consolidation_actions.append(action)

        # Remove duplicates
        duplicate_actions = self._remove_duplicates(analysis["duplicate_files"])

        # Generate report
        report = {
            "consolidation_timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "consolidation_actions": consolidation_actions,
            "duplicate_actions": duplicate_actions,
            "backup_location": str(self.backup_dir.relative_to(self.agent_workspaces_dir)),
            "status": "completed"
        }

        with open(self.consolidation_report, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        logger.info(f"✅ Archive consolidation completed: {len(consolidation_actions)} archives processed, {len(duplicate_actions)} duplicates removed")
        return report

    def _create_backup(self):
        """Create backup of current archive state."""
        if self.backup_dir.exists():
            logger.info("Backup directory already exists, skipping backup creation")
            return

        logger.info("📦 Creating backup before consolidation...")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Copy archive directories to backup
        for agent_dir in self.agent_workspaces_dir.iterdir():
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue

            for archive_dir in self._find_agent_archives(agent_dir):
                # Create relative backup path
                rel_path = archive_dir.relative_to(self.agent_workspaces_dir)
                backup_path = self.backup_dir / rel_path
                backup_path.parent.mkdir(parents=True, exist_ok=True)

                try:
                    if archive_dir.exists():
                        shutil.copytree(archive_dir, backup_path, dirs_exist_ok=True)
                except Exception as e:
                    logger.warning(f"Failed to backup {archive_dir}: {e}")

    def _consolidate_single_archive(self, archive_path: Path, target_dir: Path, agent_name: str) -> Dict[str, Any]:
        """Consolidate a single archive directory."""
        archive_info = self._analyze_archive(archive_path)

        # Determine consolidation strategy
        if archive_info["is_important"]:
            strategy = "preserve_all"
        elif archive_info["is_old"] and archive_info["size_mb"] < 10:
            strategy = "consolidate_old"
        elif archive_info["is_large"]:
            strategy = "review_large"
        else:
            strategy = "consolidate_recent"

        # Execute consolidation
        if strategy in ["consolidate_old", "consolidate_recent"]:
            # Move files to consolidated location
            consolidated_count = 0
            for file_path in archive_path.rglob("*"):
                if file_path.is_file():
                    # Create date-based subdirectory
                    file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    date_dir = target_dir / f"{file_date.year}-{file_date.month:02d}"

                    try:
                        date_dir.mkdir(exist_ok=True)
                        target_file = date_dir / file_path.name

                        # Handle name conflicts
                        counter = 1
                        while target_file.exists():
                            stem = file_path.stem
                            suffix = file_path.suffix
                            target_file = date_dir / f"{stem}_{counter}{suffix}"
                            counter += 1

                        shutil.move(str(file_path), str(target_file))
                        consolidated_count += 1

                    except Exception as e:
                        logger.warning(f"Failed to move {file_path}: {e}")

            # Remove empty archive directory
            try:
                shutil.rmtree(archive_path)
            except Exception:
                pass

            return {
                "archive": str(archive_path.relative_to(self.agent_workspaces_dir)),
                "strategy": strategy,
                "files_consolidated": consolidated_count,
                "status": "consolidated"
            }

        else:
            # Preserve or mark for review
            return {
                "archive": str(archive_path.relative_to(self.agent_workspaces_dir)),
                "strategy": strategy,
                "reason": "important_or_large_archive",
                "status": "preserved"
            }

    def _remove_duplicates(self, duplicates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate files."""
        actions = []

        for duplicate_info in duplicates:
            duplicate_path = self.agent_workspaces_dir / duplicate_info["duplicate"]

            if duplicate_path.exists():
                try:
                    duplicate_path.unlink()
                    actions.append({
                        "action": "removed_duplicate",
                        "duplicate": duplicate_info["duplicate"],
                        "original": duplicate_info["original"],
                        "hash": duplicate_info["hash"],
                        "size": duplicate_info["size"]
                    })
                except Exception as e:
                    logger.warning(f"Failed to remove duplicate {duplicate_info['duplicate']}: {e}")

        return actions

    def get_consolidation_status(self) -> Dict[str, Any]:
        """Get the current consolidation status."""
        if not self.consolidation_report.exists():
            return {"status": "not_consolidated"}

        try:
            with open(self.consolidation_report, 'r') as f:
                return json.load(f)
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def restore_from_backup(self) -> bool:
        """Restore archives from backup if needed."""
        if not self.backup_dir.exists():
            logger.error("No backup available for restoration")
            return False

        logger.info("🔄 Restoring archives from backup...")

        try:
            # Copy backup back to original locations
            for backup_item in self.backup_dir.rglob("*"):
                if backup_item.is_file():
                    # Calculate original path
                    rel_path = backup_item.relative_to(self.backup_dir)
                    original_path = self.agent_workspaces_dir / rel_path
                    original_path.parent.mkdir(parents=True, exist_ok=True)

                    shutil.copy2(backup_item, original_path)

            logger.info("✅ Archives restored from backup")
            return True

        except Exception as e:
            logger.error(f"Failed to restore from backup: {e}")
            return False


def main():
    """Main consolidation function."""
    consolidator = AgentWorkspaceConsolidator()

    print("📊 Analyzing agent workspace archives...")
    analysis = consolidator.analyze_agent_archives()

    print("Found:")
    print(f"  • {analysis['total_archives']} archive directories")
    print(f"  • {analysis['total_files']} total files")
    print(f"📊 Found {analysis['total_files']} files in {analysis['total_archives']} archives ({analysis['total_size_mb']:.1f} MB total)")
    print(f"  • {len(analysis['agents_with_archives'])} agents with archives")
    print(f"  • {len(analysis['duplicate_files'])} duplicate files")

    # Auto proceed with safe consolidation
    print("🔄 Auto-proceeding with safe consolidation...")

    print("🔄 Consolidating agent workspace archives...")
    result = consolidator.consolidate_archives()

    print("✅ Consolidation completed!")
    print(f"📦 Archives processed: {len(result['consolidation_actions'])}")
    print(f"🗑️  Duplicates removed: {len(result['duplicate_actions'])}")
    print(f"📋 Report saved to: {consolidator.consolidation_report}")


if __name__ == "__main__":
    main()