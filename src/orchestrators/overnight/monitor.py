"""
Progress Monitor
================

Progress monitoring and agent activity tracking.
Refactored - uses MonitorState for state management.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
<!-- SSOT Domain: infrastructure -->
"""

import asyncio
import logging
from typing import Any, Dict, List
from pathlib import Path

from .monitor_state import MonitorState

logger = logging.getLogger(__name__)


class ProgressMonitor:
    """
    Progress monitor for tracking agent activity and system health.
    
    Uses MonitorState for state management and EnhancedAgentActivityDetector
    for comprehensive activity detection.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """Initialize progress monitor."""
        if config is None:
            config = self._load_default_config()
        
        self.state = MonitorState(config)
        self.logger = logger
        
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration."""
        return {
            "overnight": {
                "monitoring": {
                    "check_interval": 60,  # Check every 60 seconds
                    "stall_timeout": 7200,  # 2 hours = 7200 seconds
                    "health_checks": True,
                    "performance_tracking": True,
                }
            }
        }
    
    async def start(self) -> None:
        """Start monitoring."""
        self.state.start_monitoring()
        self.logger.info("✅ Progress monitor started")
    
    async def stop(self) -> None:
        """Stop monitoring."""
        self.state.stop_monitoring()
        self.logger.info("✅ Progress monitor stopped")
    
    async def get_stalled_agents(self) -> List[str]:
        """
        Get list of stalled agents.
        
        Returns:
            List of agent IDs that are stalled
        """
        return self.state.get_stalled_agents()
    
    async def get_health_status(self) -> Dict[str, Any]:
        """
        Get system health status.
        
        Returns:
            Dict with health status information
        """
        agent_status = self.state.get_agent_status()
        stalled_count = len(await self.get_stalled_agents())
        
        return {
            "healthy": stalled_count == 0,
            "stalled_agents": await self.get_stalled_agents(),
            "stalled_count": stalled_count,
            "agent_status": agent_status,
            "monitor_info": self.state.get_info(),
        }
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        return self.state.get_agent_status()



