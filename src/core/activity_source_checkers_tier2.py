#!/usr/bin/env python3
"""
Activity Source Checkers (Tier 2)
==================================

Tier 2 activity source checkers for hardened activity detector.
These checkers detect moderately reliable activity signals:
- Status.json updates
- File modifications
- Devlog creation
- Inbox processing

<!-- SSOT Domain: infrastructure -->

V2 Compliance: <300 lines | Author: Agent-3 | Date: 2025-12-15
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from .activity_detector_models import (
    ActivitySource,
    ActivitySignal,
)

logger = logging.getLogger(__name__)


class ActivitySourceCheckersTier2:
    """Tier 2 activity source checkers."""

    def __init__(
        self,
        agent_workspaces: Path,
        workspace_root: Path,
    ):
        """Initialize Tier 2 activity source checkers."""
        self.agent_workspaces = agent_workspaces
        self.workspace_root = workspace_root

    def check_status_updates(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check status.json updates (Tier 2)."""
        signals = []
        status_file = self.agent_workspaces / agent_id / "status.json"

        if not status_file.exists():
            return signals

        try:
            mtime = status_file.stat().st_mtime
            if mtime < lookback_time.timestamp():
                return signals

            # Read status to validate meaningful content
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)

            # Check if status has meaningful content (not just noise)
            last_updated_str = status.get("last_updated", "")
            mission = status.get("current_mission", "")
            current_tasks = status.get("current_tasks", [])

            # Require meaningful content to count as activity
            if not (mission.strip() or current_tasks):
                return signals

            # Parse last_updated timestamp
            try:
                if 'T' in last_updated_str:
                    last_updated = datetime.fromisoformat(
                        last_updated_str.replace("Z", "+00:00")
                    ).replace(tzinfo=None)
                else:
                    last_updated = datetime.strptime(
                        last_updated_str, "%Y-%m-%d %H:%M:%S"
                    )

                if last_updated >= lookback_time:
                    signals.append(ActivitySignal(
                        source=ActivitySource.STATUS_UPDATE,
                        timestamp=last_updated.timestamp(),
                        confidence=ActivitySource.STATUS_UPDATE.base_confidence,
                        metadata={
                            "status": status.get("status", ""),
                            "mission": mission[:50],
                            "task_count": len(current_tasks)
                        },
                        agent_id=agent_id
                    ))
            except Exception:
                # Fallback to file mtime
                signals.append(ActivitySignal(
                    source=ActivitySource.STATUS_UPDATE,
                    timestamp=mtime,
                    confidence=ActivitySource.STATUS_UPDATE.base_confidence * 0.7,
                    metadata={"file_mtime": True},
                    agent_id=agent_id
                ))
        except Exception as e:
            logger.debug(f"Error checking status updates: {e}")

        return signals

    def check_file_modifications(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check file modifications in workspace (Tier 2)."""
        signals = []
        agent_dir = self.agent_workspaces / agent_id

        if not agent_dir.exists():
            return signals

        try:
            exclude_dirs = {"__pycache__", ".git",
                            "node_modules", ".venv", "inbox"}
            exclude_files = {"status.json"}  # Checked separately

            latest_mtime = 0
            file_count = 0

            for file_path in agent_dir.rglob("*"):
                if file_path.is_file():
                    if any(exclude in file_path.parts for exclude in exclude_dirs):
                        continue
                    if file_path.name in exclude_files:
                        continue

                    try:
                        mtime = file_path.stat().st_mtime
                        if mtime >= lookback_time.timestamp():
                            latest_mtime = max(latest_mtime, mtime)
                            file_count += 1
                    except (OSError, PermissionError):
                        continue

            if latest_mtime > 0 and file_count > 0:
                signals.append(ActivitySignal(
                    source=ActivitySource.FILE_MODIFICATION,
                    timestamp=latest_mtime,
                    confidence=ActivitySource.FILE_MODIFICATION.base_confidence,
                    metadata={"file_count": file_count},
                    agent_id=agent_id
                ))
        except Exception as e:
            logger.debug(f"Error checking file modifications: {e}")

        return signals

    def check_devlog_activity(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check devlog creation (Tier 2)."""
        signals = []
        devlogs_dir = self.workspace_root / "devlogs"

        if not devlogs_dir.exists():
            return signals

        try:
            patterns = [
                f"*{agent_id.lower()}*",
                f"*{agent_id.replace('-', '_').lower()}*",
            ]

            for pattern in patterns:
                for devlog_file in devlogs_dir.glob(f"{pattern}.md"):
                    try:
                        mtime = devlog_file.stat().st_mtime
                        if mtime >= lookback_time.timestamp():
                            signals.append(ActivitySignal(
                                source=ActivitySource.DEVLOG_CREATED,
                                timestamp=mtime,
                                confidence=ActivitySource.DEVLOG_CREATED.base_confidence,
                                metadata={"file": devlog_file.name},
                                agent_id=agent_id
                            ))
                            break  # Only need one recent devlog
                    except (OSError, PermissionError):
                        continue
        except Exception as e:
            logger.debug(f"Error checking devlog activity: {e}")

        return signals

    def check_inbox_processing(
        self,
        agent_id: str,
        lookback_time: datetime
    ) -> List[ActivitySignal]:
        """Check inbox message processing (Tier 2)."""
        signals = []
        inbox_dir = self.agent_workspaces / agent_id / "inbox"

        if not inbox_dir.exists():
            return signals

        try:
            # Check for processed/read indicators
            processed_files = list(inbox_dir.glob("*_processed.md"))
            read_files = list(inbox_dir.glob("*_read.md"))

            all_processed = processed_files + read_files
            if all_processed:
                latest = max(all_processed, key=lambda p: p.stat().st_mtime)
                mtime = latest.stat().st_mtime

                if mtime >= lookback_time.timestamp():
                    signals.append(ActivitySignal(
                        source=ActivitySource.INBOX_PROCESSING,
                        timestamp=mtime,
                        confidence=ActivitySource.INBOX_PROCESSING.base_confidence,
                        metadata={"file": latest.name},
                        agent_id=agent_id
                    ))
        except Exception as e:
            logger.debug(f"Error checking inbox processing: {e}")

        return signals
