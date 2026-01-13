#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Activity Message Checkers - Modular Activity Detection
======================================================

Message and communication activity detection components.

V2 Compliant: Modular message activity checking
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)


class MessageActivityChecker:
    """Checks message and communication activity indicators."""

    def __init__(self, workspace_root: Path):
        """Initialize message checker."""
        self.workspace_root = workspace_root

    def check_message_queue(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check message queue for agent activity."""
        try:
            message_queue_dir = self.workspace_root / "message_queue"
            if not message_queue_dir.exists():
                return None

            # Look for agent-specific message files
            agent_messages = list(message_queue_dir.glob(f"*{agent_id}*"))
            if not agent_messages:
                return None

            # Check modification times
            latest_modification = max(f.stat().st_mtime for f in agent_messages)
            latest_datetime = datetime.fromtimestamp(latest_modification)

            return {
                'message_files': len(agent_messages),
                'latest_message_activity': latest_datetime.isoformat(),
                'has_recent_messages': True
            }

        except Exception as e:
            logger.error(f"Error checking message queue for {agent_id}: {e}")
            return None

    def check_discord_posts(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check Discord posting activity."""
        try:
            # Look for Discord-related files or logs
            discord_files = [
                self.workspace_root / "discord_bot_restart",
                self.workspace_root / "agent_messages" / f"discord_{agent_id}.json"
            ]

            recent_activity = False
            latest_activity = None

            for discord_file in discord_files:
                if discord_file.exists():
                    mod_time = discord_file.stat().st_mtime
                    activity_datetime = datetime.fromtimestamp(mod_time)

                    if latest_activity is None or activity_datetime > latest_activity:
                        latest_activity = activity_datetime

                    recent_activity = True

            if recent_activity and latest_activity:
                return {
                    'has_discord_activity': True,
                    'latest_discord_activity': latest_activity.isoformat()
                }

        except Exception as e:
            logger.error(f"Error checking Discord posts for {agent_id}: {e}")

        return None

    def check_agent_communications(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Check inter-agent communication activity."""
        try:
            agent_messages_dir = self.workspace_root / "agent_messages"
            if not agent_messages_dir.exists():
                return None

            # Look for communication files involving this agent
            comm_files = list(agent_messages_dir.glob(f"*{agent_id}*"))

            if not comm_files:
                return None

            # Check for recent communications
            latest_comm = max(comm_files, key=lambda f: f.stat().st_mtime)
            latest_modification = latest_comm.stat().st_mtime
            latest_datetime = datetime.fromtimestamp(latest_modification)

            return {
                'communication_files': len(comm_files),
                'latest_communication': latest_datetime.isoformat(),
                'has_recent_communications': True
            }

        except Exception as e:
            logger.error(f"Error checking agent communications for {agent_id}: {e}")
            return None


__all__ = ["MessageActivityChecker"]