#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Activity File Checkers - Modular Activity Detection
===================================================

File system activity detection components extracted from monolithic detector.

V2 Compliant: Modular file activity checking
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class FileSystemActivityChecker:
    """Checks file system activity indicators."""

    def __init__(self, workspace_root: Path):
        """Initialize file system checker."""
        self.workspace_root = workspace_root
        self.agent_workspaces = workspace_root / "agent_workspaces"

    def check_status_json(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check status.json for activity indicators."""
        try:
            status_file = self.agent_workspaces / agent_id / "status.json"
            if not status_file.exists():
                return None

            with open(status_file, 'r', encoding='utf-8') as f:
                status_data = json.load(f)

            last_updated = status_data.get('last_updated', '')
            current_tasks = status_data.get('current_tasks', [])
            completed_tasks = status_data.get('completed_tasks', [])

            return {
                'last_updated': last_updated,
                'current_tasks_count': len(current_tasks),
                'completed_tasks_count': len(completed_tasks),
                'has_active_work': len(current_tasks) > 0
            }

        except Exception as e:
            logger.error(f"Error checking status.json for {agent_id}: {e}")
            return None

    def check_inbox_files(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check inbox files for new messages."""
        try:
            inbox_dir = self.agent_workspaces / agent_id / "inbox"
            if not inbox_dir.exists():
                return None

            inbox_files = list(inbox_dir.glob("*.md"))
            if not inbox_files:
                return None

            # Check modification times
            latest_modification = max(f.stat().st_mtime for f in inbox_files)
            latest_datetime = datetime.fromtimestamp(latest_modification)

            return {
                'file_count': len(inbox_files),
                'latest_modification': latest_datetime.isoformat(),
                'has_unread_messages': True
            }

        except Exception as e:
            logger.error(f"Error checking inbox files for {agent_id}: {e}")
            return None

    def check_devlogs(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check devlogs for recent activity."""
        try:
            devlogs_dir = self.workspace_root / "devlogs"
            if not devlogs_dir.exists():
                return None

            # Look for agent-specific devlogs
            agent_devlogs = list(devlogs_dir.glob(f"*{agent_id}*"))
            if not agent_devlogs:
                return None

            latest_devlog = max(agent_devlogs, key=lambda f: f.stat().st_mtime)
            latest_modification = latest_devlog.stat().st_mtime
            latest_datetime = datetime.fromtimestamp(latest_modification)

            return {
                'devlog_count': len(agent_devlogs),
                'latest_devlog': latest_devlog.name,
                'latest_modification': latest_datetime.isoformat()
            }

        except Exception as e:
            logger.error(f"Error checking devlogs for {agent_id}: {e}")
            return None

    def check_reports(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check for recent reports."""
        try:
            reports_dir = self.workspace_root / "reports"
            if not reports_dir.exists():
                return None

            agent_reports = list(reports_dir.glob(f"*{agent_id}*"))
            if not agent_reports:
                return None

            latest_report = max(agent_reports, key=lambda f: f.stat().st_mtime)
            latest_modification = latest_report.stat().st_mtime
            latest_datetime = datetime.fromtimestamp(latest_modification)

            return {
                'report_count': len(agent_reports),
                'latest_report': latest_report.name,
                'latest_modification': latest_datetime.isoformat()
            }

        except Exception as e:
            logger.error(f"Error checking reports for {agent_id}: {e}")
            return None

    def check_workspace_files(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check workspace files for modifications."""
        try:
            workspace_dir = self.agent_workspaces / agent_id
            if not workspace_dir.exists():
                return None

            # Get all files in workspace
            all_files = list(workspace_dir.rglob("*"))
            files_only = [f for f in all_files if f.is_file()]

            if not files_only:
                return None

            # Find most recently modified file
            latest_file = max(files_only, key=lambda f: f.stat().st_mtime)
            latest_modification = latest_file.stat().st_mtime
            latest_datetime = datetime.fromtimestamp(latest_modification)

            return {
                'total_files': len(files_only),
                'latest_file': str(latest_file.relative_to(workspace_dir)),
                'latest_modification': latest_datetime.isoformat()
            }

        except Exception as e:
            logger.error(f"Error checking workspace files for {agent_id}: {e}")
            return None


__all__ = ["FileSystemActivityChecker"]