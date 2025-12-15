#!/usr/bin/env python3
"""
Enhanced Activity-Aware Status Checker

<!-- SSOT Domain: infrastructure -->

======================================

Provides unified interface for checking agent status with multi-source activity
detection. Used by resume system to accurately detect when agents are actually
stalled vs. actively working.

Features:
- Multi-source activity detection integration
- Activity-aware staleness determination
- Configurable thresholds
- Meaningful progress filtering

V2 Compliance: <300 lines, single responsibility
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-12-11
Priority: HIGH - Hardens resume system
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class EnhancedActivityStatusChecker:
    """Enhanced status checker with multi-source activity detection."""

    def __init__(
        self,
        workspace_root: Optional[Path] = None,
        use_activity_detection: bool = True,
        stale_threshold_hours: float = 6.0,
        activity_lookback_minutes: int = 60
    ):
        """Initialize enhanced status checker.
        
        Args:
            workspace_root: Root workspace directory
            use_activity_detection: Enable multi-source activity detection
            stale_threshold_hours: Hours before status considered stale
            activity_lookback_minutes: Minutes to look back for activity
        """
        self.workspace_root = workspace_root or Path("agent_workspaces")
        self.use_activity_detection = use_activity_detection
        self.stale_threshold_hours = stale_threshold_hours
        self.activity_lookback_minutes = activity_lookback_minutes
        
        # Initialize activity detector
        self.activity_detector = None
        if use_activity_detection:
            try:
                from tools.agent_activity_detector import AgentActivityDetector
                self.activity_detector = AgentActivityDetector(self.workspace_root)
            except ImportError:
                logger.warning("AgentActivityDetector not available")
                self.use_activity_detection = False

    def is_agent_stalled(
        self,
        agent_id: str,
        status_timestamp: Optional[datetime] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Check if agent is actually stalled (not just status.json stale).
        
        Args:
            agent_id: Agent identifier
            status_timestamp: Last status.json update time (optional)
            
        Returns:
            Tuple of (is_stalled, details_dict)
        """
        details = {
            "agent_id": agent_id,
            "status_stale": False,
            "has_recent_activity": False,
            "activity_sources": [],
            "is_actually_stalled": False,
            "hours_since_status": None,
            "minutes_since_activity": None
        }
        
        # Get status timestamp if not provided
        if status_timestamp is None:
            status_timestamp = self._get_status_timestamp(agent_id)
        
        now = datetime.now()
        
        # Check if status.json is stale
        if status_timestamp:
            hours_old = (now - status_timestamp).total_seconds() / 3600
            details["hours_since_status"] = round(hours_old, 1)
            details["status_stale"] = hours_old > self.stale_threshold_hours
        else:
            # No status file or invalid timestamp - treat as stale
            details["status_stale"] = True
            details["hours_since_status"] = None
        
        # If status is not stale, agent is not stalled
        if not details["status_stale"]:
            details["is_actually_stalled"] = False
            return False, details
        
        # Status is stale - check for recent activity
        if self.use_activity_detection and self.activity_detector:
            try:
                summary = self.activity_detector.detect_agent_activity(
                    agent_id,
                    lookback_minutes=self.activity_lookback_minutes,
                    use_events=True
                )
                
                details["has_recent_activity"] = summary.is_active
                details["activity_sources"] = summary.activity_sources
                
                if summary.last_activity:
                    minutes_old = (
                        now - summary.last_activity
                    ).total_seconds() / 60
                    details["minutes_since_activity"] = round(minutes_old, 1)
                    
                    # Agent is active if:
                    # 1. Activity detected within lookback window, OR
                    # 2. Last activity is more recent than status timestamp
                    if summary.is_active or (
                        status_timestamp and
                        summary.last_activity > status_timestamp
                    ):
                        details["has_recent_activity"] = True
                        details["is_actually_stalled"] = False
                        return False, details
                
            except Exception as e:
                logger.warning(f"Error checking activity for {agent_id}: {e}")
                # On error, fall back to status-based determination
                pass
        
        # No recent activity detected - agent is actually stalled
        details["is_actually_stalled"] = True
        return True, details

    def get_stalled_agents(
        self,
        agent_ids: Optional[List[str]] = None
    ) -> List[Tuple[str, Dict[str, Any]]]:
        """Get list of actually stalled agents.
        
        Args:
            agent_ids: List of agent IDs to check (default: all agents)
            
        Returns:
            List of (agent_id, details_dict) tuples for stalled agents
        """
        if agent_ids is None:
            from src.core.constants.agent_constants import AGENT_LIST
            agent_ids = AGENT_LIST
        
        stalled = []
        for agent_id in agent_ids:
            is_stalled, details = self.is_agent_stalled(agent_id)
            if is_stalled:
                stalled.append((agent_id, details))
        
        return stalled

    def _get_status_timestamp(self, agent_id: str) -> Optional[datetime]:
        """Get status.json timestamp for agent."""
        status_file = self.workspace_root / agent_id / "status.json"
        
        if not status_file.exists():
            return None
        
        try:
            import json
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            last_updated_str = status.get("last_updated", "")
            if not last_updated_str:
                # Fallback to file mtime
                return datetime.fromtimestamp(status_file.stat().st_mtime)
            
            # Try parsing timestamp
            formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
            for fmt in formats:
                try:
                    return datetime.strptime(last_updated_str, fmt)
                except ValueError:
                    continue
            
            # Fallback to file mtime if parsing fails
            return datetime.fromtimestamp(status_file.stat().st_mtime)
            
        except Exception as e:
            logger.warning(f"Error reading status for {agent_id}: {e}")
            return None


def is_agent_stalled(
    agent_id: str,
    workspace_root: Optional[Path] = None,
    use_activity_detection: bool = True
) -> Tuple[bool, Dict[str, Any]]:
    """Convenience function to check if agent is stalled.
    
    Args:
        agent_id: Agent identifier
        workspace_root: Root workspace directory
        use_activity_detection: Enable activity detection
        
    Returns:
        Tuple of (is_stalled, details_dict)
    """
    checker = EnhancedActivityStatusChecker(
        workspace_root=workspace_root,
        use_activity_detection=use_activity_detection
    )
    return checker.is_agent_stalled(agent_id)


__all__ = [
    "EnhancedActivityStatusChecker",
    "is_agent_stalled"
]

