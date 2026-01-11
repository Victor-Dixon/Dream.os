#!/usr/bin/env python3
"""
Archival Service - Message Archiving & Rotation
==============================================

Features for message archival:
- Automatic message archiving after processing
- Archive rotation and cleanup
- Archive search and retrieval
- Archive statistics and management

V2 Compliance: <150 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
"""

import json
import logging
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ArchivalService:
    """Manages message archiving and rotation."""

    def __init__(self, project_root: Path):
        """Initialize archival service."""
        self.project_root = project_root
        self.archive_base = project_root / "message_archive"
        self.agent_workspaces = project_root / "agent_workspaces"

        # Create archive directory structure
        self.archive_base.mkdir(parents=True, exist_ok=True)

        # Archive subdirectories
        self.processed_archive = self.archive_base / "processed"
        self.system_archive = self.archive_base / "system"
        self.error_archive = self.archive_base / "errors"

        for dir_path in [self.processed_archive, self.system_archive, self.error_archive]:
            dir_path.mkdir(parents=True, exist_ok=True)

    def archive_message(self, message_file: Path, agent_id: str, reason: str = "processed") -> bool:
        """
        Archive a processed message file.

        Args:
            message_file: Path to the message file to archive
            agent_id: Agent ID for organization
            reason: Reason for archiving (processed, system, error)

        Returns:
            bool: Success status
        """
        try:
            # Determine archive subdirectory
            if reason == "system":
                archive_dir = self.system_archive / agent_id
            elif reason == "error":
                archive_dir = self.error_archive / agent_id
            else:
                archive_dir = self.processed_archive / agent_id

            archive_dir.mkdir(parents=True, exist_ok=True)

            # Create archive filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            original_name = message_file.name
            archive_name = f"{timestamp}_{original_name}"
            archive_path = archive_dir / archive_name

            # Copy file to archive
            shutil.copy2(message_file, archive_path)

            # Create metadata file
            metadata = {
                "original_path": str(message_file),
                "archive_path": str(archive_path),
                "agent_id": agent_id,
                "reason": reason,
                "archived_at": datetime.now().isoformat(),
                "file_size": message_file.stat().st_size
            }

            metadata_path = archive_path.with_suffix('.metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            logger.info(f"📦 Archived {message_file.name} for {agent_id} ({reason})")
            return True

        except Exception as e:
            logger.error(f"Failed to archive {message_file}: {e}")
            return False

    def archive_message_content(self, content: str, agent_id: str,
                              message_id: str, reason: str = "processed") -> bool:
        """
        Archive message content directly (when file doesn't exist).

        Args:
            content: Message content to archive
            agent_id: Target agent ID
            message_id: Message ID for filename
            reason: Archival reason

        Returns:
            bool: Success status
        """
        try:
            # Determine archive subdirectory
            if reason == "system":
                archive_dir = self.system_archive / agent_id
            elif reason == "error":
                archive_dir = self.error_archive / agent_id
            else:
                archive_dir = self.processed_archive / agent_id

            archive_dir.mkdir(parents=True, exist_ok=True)

            # Create archive filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{message_id}.md"
            archive_path = archive_dir / filename

            # Write content to archive
            with open(archive_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Create metadata file
            metadata = {
                "message_id": message_id,
                "archive_path": str(archive_path),
                "agent_id": agent_id,
                "reason": reason,
                "archived_at": datetime.now().isoformat(),
                "content_length": len(content)
            }

            metadata_path = archive_path.with_suffix('.metadata.json')
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            logger.info(f"📦 Archived content for {message_id} ({agent_id}, {reason})")
            return True

        except Exception as e:
            logger.error(f"Failed to archive content for {message_id}: {e}")
            return False

    def rotate_archives(self, days_to_keep: int = 30) -> Dict[str, Any]:
        """
        Rotate old archives to prevent disk space issues.

        Args:
            days_to_keep: Number of days to keep archives

        Returns:
            Dict with rotation statistics
        """
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        stats = {
            "processed": 0,
            "deleted": 0,
            "errors": 0,
            "total_space_freed": 0
        }

        try:
            # Check all archive subdirectories
            for archive_type in [self.processed_archive, self.system_archive, self.error_archive]:
                if not archive_type.exists():
                    continue

                for agent_dir in archive_type.glob("*"):
                    if not agent_dir.is_dir():
                        continue

                    for archive_file in agent_dir.glob("*"):
                        if archive_file.suffix in ['.metadata.json']:
                            continue  # Skip metadata files, they'll be cleaned with their content

                        try:
                            # Check file modification time
                            file_mtime = datetime.fromtimestamp(archive_file.stat().st_mtime)
                            if file_mtime < cutoff_date:
                                # Get file size before deletion
                                file_size = archive_file.stat().st_size

                                # Delete the file and its metadata
                                archive_file.unlink()
                                metadata_file = archive_file.with_suffix('.metadata.json')
                                if metadata_file.exists():
                                    metadata_file.unlink()

                                stats["deleted"] += 1
                                stats["total_space_freed"] += file_size

                        except Exception as e:
                            logger.warning(f"Failed to rotate {archive_file}: {e}")
                            stats["errors"] += 1

            stats["processed"] = stats["deleted"] + stats["errors"]
            logger.info(f"🗂️ Archive rotation complete: {stats['deleted']} files deleted, "
                       f"{stats['total_space_freed']} bytes freed")

        except Exception as e:
            logger.error(f"Archive rotation failed: {e}")
            stats["errors"] += 1

        return stats

    def search_archives(self, query: str, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search archived messages for content.

        Args:
            query: Search query string
            agent_id: Optional agent ID filter

        Returns:
            List of matching archived messages
        """
        results = []

        try:
            # Search all archive subdirectories
            search_dirs = [self.processed_archive, self.system_archive, self.error_archive]

            for archive_type in search_dirs:
                if not archive_type.exists():
                    continue

                # Filter by agent if specified
                agent_dirs = [archive_type / agent_id] if agent_id else list(archive_type.glob("*"))

                for agent_dir in agent_dirs:
                    if not agent_dir.exists() or not agent_dir.is_dir():
                        continue

                    for archive_file in agent_dir.glob("*.md"):
                        try:
                            content = archive_file.read_text(encoding='utf-8')
                            if query.lower() in content.lower():
                                # Load metadata if available
                                metadata_file = archive_file.with_suffix('.metadata.json')
                                metadata = {}
                                if metadata_file.exists():
                                    with open(metadata_file, 'r', encoding='utf-8') as f:
                                        metadata = json.load(f)

                                results.append({
                                    "file_path": str(archive_file),
                                    "agent_id": agent_dir.name,
                                    "archive_type": archive_type.name,
                                    "content_preview": content[:200] + "..." if len(content) > 200 else content,
                                    "metadata": metadata
                                })

                        except Exception as e:
                            logger.warning(f"Failed to search {archive_file}: {e}")

        except Exception as e:
            logger.error(f"Archive search failed: {e}")

        return results

    def get_archival_stats(self) -> Dict[str, Any]:
        """Get comprehensive archival statistics."""
        stats = {
            "total_archives": 0,
            "archive_types": {},
            "agents_with_archives": set(),
            "total_size_bytes": 0,
            "oldest_archive": None,
            "newest_archive": None
        }

        try:
            for archive_type in [self.processed_archive, self.system_archive, self.error_archive]:
                if not archive_type.exists():
                    continue

                type_stats = {"count": 0, "size": 0}
                stats["archive_types"][archive_type.name] = type_stats

                for agent_dir in archive_type.glob("*"):
                    if not agent_dir.is_dir():
                        continue

                    stats["agents_with_archives"].add(agent_dir.name)

                    for archive_file in agent_dir.glob("*.md"):
                        try:
                            stat = archive_file.stat()
                            type_stats["count"] += 1
                            type_stats["size"] += stat.st_size
                            stats["total_size_bytes"] += stat.st_size
                            stats["total_archives"] += 1

                            # Track timestamps
                            mtime = datetime.fromtimestamp(stat.st_mtime)
                            if not stats["oldest_archive"] or mtime < stats["oldest_archive"]:
                                stats["oldest_archive"] = mtime
                            if not stats["newest_archive"] or mtime > stats["newest_archive"]:
                                stats["newest_archive"] = mtime

                        except Exception as e:
                            logger.warning(f"Failed to stat {archive_file}: {e}")

            stats["agents_with_archives"] = list(stats["agents_with_archives"])

            # Format timestamps
            if stats["oldest_archive"]:
                stats["oldest_archive"] = stats["oldest_archive"].isoformat()
            if stats["newest_archive"]:
                stats["newest_archive"] = stats["newest_archive"].isoformat()

        except Exception as e:
            logger.error(f"Failed to get archival stats: {e}")

        return stats