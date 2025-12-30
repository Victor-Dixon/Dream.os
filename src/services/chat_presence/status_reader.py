#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Agent Status Reader
===================

Reads agent status from status.json files for chat presence system.

V2 Compliance: <400 lines, single responsibility
Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class AgentStatusReader:
    """
    Reads agent status from status.json files.
    
    Provides:
    - Individual agent status
    - All agents status summary
    - Formatted status for chat display
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize status reader.
        
        Args:
            workspace_root: Root path to agent workspaces (default: agent_workspaces/)
        """
        if workspace_root is None:
            # Default to project root/agent_workspaces
            workspace_root = Path(__file__).parent.parent.parent.parent / "agent_workspaces"
        
        self.workspace_root = Path(workspace_root)

    def get_agent_status(self, agent_id: str) -> Optional[Dict]:
        """
        Get status for a specific agent.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            
        Returns:
            Status dictionary or None if not found
        """
        status_file = self.workspace_root / agent_id / "status.json"
        
        if not status_file.exists():
            logger.warning(f"Status file not found: {status_file}")
            return None
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading status for {agent_id}: {e}")
            return None

    def get_all_agents_status(self) -> Dict[str, Dict]:
        """
        Get status for all agents.
        
        Returns:
            Dictionary mapping agent_id to status
        """
        all_status = {}
        
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status = self.get_agent_status(agent_id)
            if status:
                all_status[agent_id] = status
        
        return all_status

    def format_agent_status(self, agent_id: str, status: Optional[Dict] = None) -> str:
        """
        Format agent status for chat display.
        
        Args:
            agent_id: Agent identifier
            status: Status dictionary (if None, will be fetched)
            
        Returns:
            Formatted status string
        """
        if status is None:
            status = self.get_agent_status(agent_id)
        
        if not status:
            return f"❌ {agent_id}: Status not available"
        
        # Extract key fields
        agent_name = status.get("agent_name", agent_id)
        current_status = status.get("status", "UNKNOWN")
        current_mission = status.get("current_mission", "")
        current_tasks = status.get("current_tasks", [])
        last_updated = status.get("last_updated", "unknown")
        
        # Format status emoji
        status_emoji = {
            "ACTIVE_AGENT_MODE": "🟢",
            "IDLE": "🟡",
            "STALLED": "🔴",
            "BUSY": "🟠",
        }.get(current_status, "⚪")
        
        # Build message
        lines = [
            f"{status_emoji} **{agent_id}** ({agent_name})",
            f"Status: {current_status}",
        ]
        
        if current_mission:
            lines.append(f"Mission: {current_mission[:50]}")
        
        if current_tasks:
            task_preview = current_tasks[0][:40] if current_tasks else ""
            lines.append(f"Task: {task_preview}...")
        
        lines.append(f"Updated: {last_updated}")
        
        return " | ".join(lines)

    def format_all_agents_summary(self) -> str:
        """
        Format summary of all agents for chat display.
        
        Returns:
            Formatted summary string
        """
        all_status = self.get_all_agents_status()
        
        if not all_status:
            return "❌ No agent status available"
        
        # Count by status
        status_counts = {}
        for status_data in all_status.values():
            status = status_data.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Build summary
        lines = ["📊 **Swarm Status Summary:**"]
        
        for status, count in sorted(status_counts.items()):
            emoji = {
                "ACTIVE_AGENT_MODE": "🟢",
                "IDLE": "🟡",
                "STALLED": "🔴",
                "BUSY": "🟠",
            }.get(status, "⚪")
            lines.append(f"{emoji} {status}: {count}")
        
        lines.append(f"Total Agents: {len(all_status)}")
        
        return " | ".join(lines)

    def format_agent_status_compact(self, agent_id: str) -> str:
        """
        Format compact single-line status for chat.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Compact status string
        """
        status = self.get_agent_status(agent_id)
        
        if not status:
            return f"❌ {agent_id}: N/A"
        
        current_status = status.get("status", "UNKNOWN")
        status_emoji = {
            "ACTIVE_AGENT_MODE": "🟢",
            "IDLE": "🟡",
            "STALLED": "🔴",
            "BUSY": "🟠",
        }.get(current_status, "⚪")
        
        current_task = status.get("current_tasks", [])
        task_info = current_task[0][:30] if current_task else "idle"
        
        return f"{status_emoji} {agent_id}: {current_status} | {task_info}"


__all__ = ["AgentStatusReader"]

