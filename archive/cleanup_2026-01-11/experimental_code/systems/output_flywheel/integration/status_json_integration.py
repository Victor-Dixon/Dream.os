"""
Status.json Integration for Output Flywheel
===========================================

Hooks into agent status.json updates to automatically track work sessions
and trigger Output Flywheel when appropriate.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from systems.output_flywheel.integration.agent_session_hooks import AgentSessionHook

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class StatusJsonIntegration:
    """
    Integrates Output Flywheel with agent status.json updates.
    
    Monitors status.json changes and automatically triggers artifact
    generation when significant work is completed.
    """

    def __init__(self, agent_id: str, workspace_root: Optional[Path] = None):
        """
        Initialize status.json integration.
        
        Args:
            agent_id: Agent identifier
            workspace_root: Root of workspace
        """
        self.agent_id = agent_id
        self.workspace_root = workspace_root or PROJECT_ROOT
        self.agent_workspace = self.workspace_root / "agent_workspaces" / agent_id
        self.status_file = self.agent_workspace / "status.json"
        self.session_hook = AgentSessionHook(agent_id, workspace_root)
        self.last_status_hash = None

    def check_and_trigger(self, force: bool = False) -> Optional[Dict[str, Any]]:
        """
        Check status.json for significant changes and trigger Output Flywheel if needed.
        
        Args:
            force: Force trigger even if no significant changes detected
        
        Returns:
            Updated session data if triggered, None otherwise
        """
        if not self.status_file.exists():
            return None
        
        try:
            status_data = json.loads(self.status_file.read_text(encoding="utf-8"))
            status_hash = self._hash_status(status_data)
            
            # Skip if no changes detected (unless forced)
            if not force and status_hash == self.last_status_hash:
                return None
            
            self.last_status_hash = status_hash
            
            # Determine session type from status
            session_type = self._infer_session_type(status_data)
            
            # Check if significant work completed
            if self._should_trigger(status_data, session_type) or force:
                logger.info(f"🔄 Triggering Output Flywheel for {self.agent_id} ({session_type} session)")
                return self.session_hook.end_of_session(
                    session_type=session_type,
                    auto_trigger=True,
                )
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Status.json integration check failed: {e}", exc_info=True)
            return None

    def _infer_session_type(self, status_data: Dict[str, Any]) -> str:
        """
        Infer session type from status.json.
        
        Args:
            status_data: Agent status.json data
        
        Returns:
            Session type: "build", "trade", or "life_aria"
        """
        current_mission = status_data.get("current_mission", "").lower()
        
        # Check for trading-related keywords
        if any(keyword in current_mission for keyword in ["trade", "trading", "market", "stock"]):
            return "trade"
        
        # Check for life/aria-related keywords
        if any(keyword in current_mission for keyword in ["aria", "life", "game", "website"]):
            return "life_aria"
        
        # Default to build session
        return "build"

    def _should_trigger(self, status_data: Dict[str, Any], session_type: str) -> bool:
        """
        Determine if Output Flywheel should be triggered.
        
        Args:
            status_data: Agent status.json data
            session_type: Inferred session type
        
        Returns:
            True if should trigger, False otherwise
        """
        # Check for completed tasks
        completed_tasks = status_data.get("completed_tasks", [])
        if len(completed_tasks) > 0:
            return True
        
        # Check for achievements
        achievements = status_data.get("achievements", [])
        if len(achievements) > 0:
            return True
        
        # Check for significant status changes
        current_phase = status_data.get("current_phase", "")
        if current_phase in ["TASK_EXECUTION", "COMPLETE"]:
            return True
        
        return False

    def _hash_status(self, status_data: Dict[str, Any]) -> str:
        """
        Generate hash of status.json for change detection.
        
        Args:
            status_data: Agent status.json data
        
        Returns:
            Hash string
        """
        import hashlib
        
        # Create hash from key fields
        key_fields = {
            "current_mission": status_data.get("current_mission", ""),
            "completed_tasks": status_data.get("completed_tasks", []),
            "achievements": status_data.get("achievements", []),
            "current_phase": status_data.get("current_phase", ""),
        }
        
        status_str = json.dumps(key_fields, sort_keys=True)
        return hashlib.md5(status_str.encode()).hexdigest()

    def update_status_with_artifacts(
        self,
        artifacts: Dict[str, Any],
        session_id: Optional[str] = None,
    ) -> bool:
        """
        Update status.json with generated artifact paths.
        
        Args:
            artifacts: Artifact paths from Output Flywheel
            session_id: Optional session ID
        
        Returns:
            True if updated successfully
        """
        if not self.status_file.exists():
            return False
        
        try:
            status_data = json.loads(self.status_file.read_text(encoding="utf-8"))
            
            # Add artifacts to status
            if "artifacts" not in status_data:
                status_data["artifacts"] = {}
            
            if session_id:
                status_data["artifacts"][session_id] = artifacts
            else:
                status_data["artifacts"]["latest"] = artifacts
            
            # Update timestamp
            status_data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save updated status
            self.status_file.write_text(
                json.dumps(status_data, indent=2), encoding="utf-8"
            )
            
            logger.info(f"✅ Updated status.json with artifacts for {self.agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update status.json: {e}", exc_info=True)
            return False


def auto_trigger_on_status_update(agent_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to check status.json and auto-trigger Output Flywheel.
    
    Usage:
        from systems.output_flywheel.integration.status_json_integration import auto_trigger_on_status_update
        
        artifacts = auto_trigger_on_status_update("Agent-1")
    
    Args:
        agent_id: Agent identifier
    
    Returns:
        Updated session data if triggered, None otherwise
    """
    integration = StatusJsonIntegration(agent_id)
    return integration.check_and_trigger()

