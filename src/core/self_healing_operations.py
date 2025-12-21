#!/usr/bin/env python3
"""
Self-Healing Operations
=======================

Core healing operations for agent self-healing system:
- Terminal cancellation
- Status reset/clear
- Task clearing
- Agent recovery checking

<!-- SSOT Domain: infrastructure -->

V2 Compliance: <300 lines | Author: Agent-3 | Date: 2025-12-15
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class SelfHealingOperations:
    """Core healing operations for stalled agents."""

    def __init__(
        self,
        workspace_root: Path,
        agent_coordinates: Dict[str, Tuple[int, int]],
        pyautogui: Optional[any] = None,
    ):
        """Initialize healing operations."""
        self.workspace_root = workspace_root
        self.agent_coordinates = agent_coordinates
        self.pyautogui = pyautogui
        self.pyautogui_available = pyautogui is not None

    async def cancel_terminal_operations(self, agent_id: str) -> bool:
        """Cancel terminal operations by clicking chat input and pressing SHIFT+BACKSPACE.

        Args:
            agent_id: Agent identifier

        Returns:
            True if successful
        """
        if not self.pyautogui_available:
            logger.warning(
                f"PyAutoGUI not available - cannot cancel terminal for {agent_id}")
            return False

        if agent_id not in self.agent_coordinates:
            logger.error(f"No coordinates found for {agent_id}")
            return False

        try:
            x, y = self.agent_coordinates[agent_id]
            logger.info(f"🛑 Cancelling terminal for {agent_id} at ({x}, {y})")

            # Click chat input coordinates
            self.pyautogui.moveTo(x, y, duration=0.5)
            self.pyautogui.click()
            await asyncio.sleep(0.3)

            # Press SHIFT+BACKSPACE to cancel terminal operations
            self.pyautogui.hotkey("shift", "backspace")
            await asyncio.sleep(0.5)

            # Record cancellation if callback provided
            if self.record_cancellation:
                cancel_count = self.record_cancellation(agent_id)
                logger.info(
                    f"✅ Terminal cancelled for {agent_id} (cancellation #{cancel_count} today)")
            else:
                logger.info(f"✅ Terminal cancelled for {agent_id}")

            return True

        except Exception as e:
            logger.error(f"Error cancelling terminal for {agent_id}: {e}")
            return False

    async def check_agent_recovered(self, agent_id: str) -> bool:
        """Check if agent has recovered after cancellation.

        Args:
            agent_id: Agent identifier

        Returns:
            True if agent status was updated recently
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            if not status_file.exists():
                return False

            file_mtime = status_file.stat().st_mtime
            age_seconds = time.time() - file_mtime

            # If status updated in last 30 seconds, agent recovered
            return age_seconds < 30
        except Exception:
            return False

    async def clear_stuck_tasks(self, agent_id: str) -> bool:
        """Clear stuck tasks from agent status.

        Args:
            agent_id: Agent identifier

        Returns:
            True if successful
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"

            if not status_file.exists():
                return False

            with open(status_file, 'r') as f:
                status = json.load(f)

            # Clear current_tasks
            if "current_tasks" in status:
                status["current_tasks"] = []
                if "healing_applied" not in status:
                    status["healing_applied"] = []
                status["healing_applied"].append({
                    "timestamp": datetime.now().isoformat(),
                    "action": "clear_stuck_tasks",
                })

                status["last_updated"] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")

                with open(status_file, 'w') as f:
                    json.dump(status, f, indent=2)

                return True

            return False

        except Exception as e:
            logger.error(f"Error clearing stuck tasks for {agent_id}: {e}")
            return False

    async def reset_agent_status(self, agent_id: str) -> bool:
        """Reset agent status.json to active state.

        Args:
            agent_id: Agent identifier

        Returns:
            True if successful
        """
        try:
            status_file = self.workspace_root / agent_id / "status.json"
            status_file.parent.mkdir(parents=True, exist_ok=True)

            # Create fresh status
            reset_status = {
                "agent_id": agent_id,
                "status": "ACTIVE_AGENT_MODE",
                "current_phase": "TASK_EXECUTION",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "healing_applied": [{
                    "timestamp": datetime.now().isoformat(),
                    "action": "reset",
                    "reason": "stall_recovery",
                }],
                "current_mission": "System recovery - ready for new tasks",
                "mission_priority": "HIGH",
                "current_tasks": [],
                "next_actions": ["Awaiting task assignment"],
            }

            with open(status_file, 'w') as f:
                json.dump(reset_status, f, indent=2)

            logger.info(f"✅ {agent_id}: Status reset successfully")
            return True

        except Exception as e:
            logger.error(f"Error resetting status for {agent_id}: {e}")
            return False
