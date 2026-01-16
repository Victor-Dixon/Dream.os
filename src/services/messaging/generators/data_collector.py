#!/usr/bin/env python3
"""
Work Resume Data Collector - Data Gathering Infrastructure
=========================================================

<!-- SSOT Domain: messaging -->

Collects and aggregates data from various sources for work resume generation:
- Agent status information
- Git commit history
- Coordination activity
- Devlog entries

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class WorkResumeDataCollector:
    """Collects data from various sources for work resume generation."""

    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize with workspace root path."""
        if workspace_root is None:
            workspace_root = Path("agent_workspaces")
        self.workspace_root = Path(workspace_root)

    def collect_agent_data(self, agent_id: str, days_back: int = 7) -> Dict[str, Any]:
        """
        Collect all data needed for an agent's work resume.

        Args:
            agent_id: Agent identifier
            days_back: Number of days to look back for data

        Returns:
            Dictionary containing all collected data
        """
        status = self._load_status(agent_id)
        commits = self._get_recent_commits(days_back)
        coordination = self._get_coordination_activity(agent_id, days_back)
        devlogs = self._get_recent_devlogs(agent_id, days_back)

        return {
            'status': status,
            'commits': commits,
            'coordination': coordination,
            'devlogs': devlogs,
            'agent_id': agent_id,
            'days_back': days_back,
            'collected_at': datetime.now().isoformat()
        }

    def _load_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Load agent status from workspace.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent status data
        """
        status_file = self.workspace_root / agent_id / "status.json"

        if not status_file.exists():
            logger.warning(f"Status file not found for agent {agent_id}")
            return {}

        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load status for {agent_id}: {e}")
            return {}

    def _get_recent_commits(self, days_back: int) -> List[Dict[str, Any]]:
        """
        Get recent git commits.

        Args:
            days_back: Number of days to look back

        Returns:
            List of recent commits
        """
        try:
            import subprocess
            from datetime import datetime

            # Calculate date threshold
            since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

            # Run git log command
            result = subprocess.run([
                'git', 'log',
                '--since', since_date,
                '--pretty=format:{"hash":"%H","author":"%an","date":"%ad","message":"%s"}',
                '--date=iso'
            ], capture_output=True, text=True, cwd=self.workspace_root.parent)

            if result.returncode != 0:
                logger.warning(f"Git log failed: {result.stderr}")
                return []

            # Parse JSON lines
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    try:
                        # Fix JSON formatting (add commas between objects)
                        commit_data = json.loads(line)
                        commits.append(commit_data)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Failed to parse commit: {line} - {e}")

            return commits

        except ImportError:
            logger.warning("Git not available for commit collection")
            return []
        except Exception as e:
            logger.error(f"Failed to get recent commits: {e}")
            return []

    def _get_coordination_activity(self, agent_id: str, days_back: int) -> List[Dict[str, Any]]:
        """
        Get recent coordination activity for agent.

        Args:
            agent_id: Agent identifier
            days_back: Number of days to look back

        Returns:
            List of coordination activities
        """
        # This is a placeholder - coordination data would come from coordination tracking
        # For now, return empty list as this would need integration with coordination system
        return []

    def _get_recent_devlogs(self, agent_id: str, days_back: int) -> List[Dict[str, Any]]:
        """
        Get recent devlog entries for agent.

        Args:
            agent_id: Agent identifier
            days_back: Number of days to look back

        Returns:
            List of devlog entries
        """
        devlogs_dir = self.workspace_root / agent_id / "devlogs"

        if not devlogs_dir.exists():
            return []

        cutoff_date = datetime.now() - timedelta(days=days_back)
        devlogs = []

        try:
            for devlog_file in devlogs_dir.glob("*.md"):
                if devlog_file.stat().st_mtime > cutoff_date.timestamp():
                    try:
                        with open(devlog_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        devlogs.append({
                            'filename': devlog_file.name,
                            'content': content,
                            'modified': datetime.fromtimestamp(devlog_file.stat().st_mtime).isoformat()
                        })
                    except Exception as e:
                        logger.warning(f"Failed to read devlog {devlog_file}: {e}")

        except Exception as e:
            logger.error(f"Failed to scan devlogs for {agent_id}: {e}")

        return devlogs