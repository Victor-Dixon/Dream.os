#!/usr/bin/env python3
"""
Status JSON Integration for Output Flywheel
===========================================

Integration with Output Flywheel for status tracking and session management.
"""

import logging
from typing import Dict, Any, Optional
import time
import json
import os

logger = logging.getLogger(__name__)


class StatusJsonIntegration:
    """
    Integration with Output Flywheel for status tracking and session management.

    This class provides functionality to:
    - Check for new sessions that need processing
    - Trigger session processing
    - Update status with artifacts
    """

    def __init__(self, agent_id: str):
        """
        Initialize the Status JSON integration.

        Args:
            agent_id: The agent identifier for this integration
        """
        self.agent_id = agent_id
        self.status_file_path = os.getenv(
            "OUTPUT_FLYWHEEL_STATUS_FILE",
            f"output_flywheel_status_{agent_id}.json"
        )
        self.session_check_interval = float(os.getenv("OUTPUT_FLYWHEEL_CHECK_INTERVAL", "60.0"))
        logger.info(f"StatusJsonIntegration initialized for agent {agent_id}")

    def check_and_trigger(self) -> Optional[Dict[str, Any]]:
        """
        Check for new sessions that need processing and trigger if available.

        Returns:
            Session data dictionary if a session needs processing, None otherwise
        """
        try:
            # Check if status file exists
            if not os.path.exists(self.status_file_path):
                return None

            # Read status file
            with open(self.status_file_path, 'r') as f:
                status_data = json.load(f)

            # Check for pending sessions
            pending_sessions = status_data.get("pending_sessions", [])
            if not pending_sessions:
                return None

            # Get the next pending session
            session = pending_sessions[0]
            session_id = session.get("session_id")

            if session_id:
                logger.info(f"Triggering session {session_id} for agent {self.agent_id}")
                return session

        except Exception as e:
            logger.warning(f"Error checking for sessions: {e}")

        return None

    def update_status_with_artifacts(self, artifacts: Dict[str, Any], session_id: Optional[str] = None) -> bool:
        """
        Update the status file with processing artifacts.

        Args:
            artifacts: Artifacts from session processing
            session_id: Optional session identifier

        Returns:
            True if update was successful, False otherwise
        """
        try:
            # Read current status
            status_data = {}
            if os.path.exists(self.status_file_path):
                with open(self.status_file_path, 'r') as f:
                    status_data = json.load(f)

            # Update with artifacts
            if "completed_sessions" not in status_data:
                status_data["completed_sessions"] = []

            completed_session = {
                "session_id": session_id,
                "artifacts": artifacts,
                "completed_at": time.time(),
                "agent_id": self.agent_id
            }

            status_data["completed_sessions"].append(completed_session)

            # Remove from pending if present
            pending_sessions = status_data.get("pending_sessions", [])
            status_data["pending_sessions"] = [
                s for s in pending_sessions
                if s.get("session_id") != session_id
            ]

            # Write updated status
            with open(self.status_file_path, 'w') as f:
                json.dump(status_data, f, indent=2)

            logger.info(f"Updated status with artifacts for session {session_id}")
            return True

        except Exception as e:
            logger.error(f"Error updating status with artifacts: {e}")
            return False