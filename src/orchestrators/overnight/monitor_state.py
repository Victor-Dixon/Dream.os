"""

<<<<<<< HEAD
<<<<<<< HEAD
<!-- SSOT Domain: orchestrators -->

=======
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
<!-- SSOT Domain: orchestrators -->

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
Monitor State Management
========================

State tracking for progress monitor.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: monitor.py (ProgressMonitor class split)
License: MIT
"""

import time
from typing import Any


class MonitorState:
    """Manages monitor state and agent tracking."""

    def __init__(self, config: dict):
        """Initialize monitor state."""
        monitoring_config = config.get("overnight", {}).get("monitoring", {})

        # Configuration
        self.check_interval = monitoring_config.get("check_interval", 60)
        self.stall_timeout = monitoring_config.get("stall_timeout", 300)
        self.health_checks = monitoring_config.get("health_checks", True)
        self.performance_tracking = monitoring_config.get("performance_tracking", True)

        # State
        self.is_monitoring = False
        self.start_time = 0
        self.current_cycle = 0
        self.cycle_start_times = {}
        self.agent_activity = {}
        self.agent_tasks = {}

    def start_monitoring(self) -> None:
        """Start monitoring state."""

        self.is_monitoring = True
        self.start_time = time.time()

        # Initialize agent tracking (mode-aware)
        current_time = time.time()
        try:
            from src.core.agent_mode_manager import get_active_agents
            active_agents = get_active_agents()
        except Exception:
            # Fallback to 4-agent mode
            active_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        
        for agent_id in active_agents:
            self.agent_activity[agent_id] = current_time
            self.agent_tasks[agent_id] = None

    def stop_monitoring(self) -> None:
        """Stop monitoring state."""
        self.is_monitoring = False

    def update_cycle(self, cycle_number: int, cycle_start_time: float) -> None:
        """Update cycle tracking."""

        self.current_cycle = cycle_number
        self.cycle_start_times[cycle_number] = cycle_start_time

    def update_agent_activity(self, agent_id: str, task_id: str | None) -> None:
        """Update agent activity."""
        self.agent_activity[agent_id] = time.time()
        self.agent_tasks[agent_id] = task_id

    def get_stalled_agents(self) -> list[str]:
        """Get list of stalled agents using enhanced activity detection."""

        stalled = []
        
        # Enhanced: Use comprehensive activity detection (Agent-1 proposal)
        try:
            from .enhanced_agent_activity_detector import EnhancedAgentActivityDetector
            
            detector = EnhancedAgentActivityDetector()
            stale_agents = detector.get_stale_agents(max_age_seconds=self.stall_timeout)
            
            # Extract agent IDs from stale agents
            for agent_id, age in stale_agents:
                stalled.append(agent_id)
        except ImportError:
            # Fallback to original method if enhanced detector unavailable
            current_time = time.time()
            for agent_id, last_activity in self.agent_activity.items():
                if current_time - last_activity > self.stall_timeout:
                    stalled.append(agent_id)

        return stalled

    def get_agent_status(self) -> dict[str, Any]:
        """Get status of all agents using enhanced activity detection."""
        current_time = time.time()
        agent_status = {}
        
        # Enhanced: Use comprehensive activity detection (Agent-1 proposal)
        try:
            from .enhanced_agent_activity_detector import EnhancedAgentActivityDetector
            
            detector = EnhancedAgentActivityDetector()
            all_activity = detector.get_all_agents_activity()
            
            for agent_id in self.agent_activity:
                current_task = self.agent_tasks[agent_id]
                
                # Get enhanced activity data
                activity_data = all_activity.get(agent_id, {})
                latest_activity = activity_data.get("latest_activity")
                activity_sources = activity_data.get("activity_sources", [])
                
                # Use enhanced activity if available, otherwise fallback
                if latest_activity:
                    last_activity = latest_activity
                    time_since_activity = current_time - last_activity
                else:
                    last_activity = self.agent_activity[agent_id]
                    time_since_activity = current_time - last_activity
                
                # Determine agent status
                if time_since_activity > self.stall_timeout:
                    status = "stalled"
                elif current_task:
                    status = "busy"
                else:
                    status = "idle"
                
                agent_status[agent_id] = {
                    "status": status,
                    "last_activity": last_activity,
                    "time_since_activity": time_since_activity,
                    "current_task": current_task,
                    "activity_sources": activity_sources,  # NEW: Show activity sources
                    "activity_count": len(activity_sources),
                }
        except ImportError:
            # Fallback to original method if enhanced detector unavailable
            for agent_id in self.agent_activity:
                last_activity = self.agent_activity[agent_id]
                current_task = self.agent_tasks[agent_id]

                time_since_activity = current_time - last_activity

                if time_since_activity > self.stall_timeout:
                    status = "stalled"
                elif current_task:
                    status = "busy"
                else:
                    status = "idle"

                agent_status[agent_id] = {
                    "status": status,
                    "last_activity": last_activity,
                    "time_since_activity": time_since_activity,
                    "current_task": current_task,
                }

        return agent_status

    def get_info(self) -> dict[str, Any]:
        """Get monitor configuration info."""

        return {
            "monitoring_active": self.is_monitoring,
            "check_interval": self.check_interval,
            "stall_timeout": self.stall_timeout,
            "health_checks": self.health_checks,
            "performance_tracking": self.performance_tracking,
            "start_time": self.start_time,
            "current_cycle": self.current_cycle,
            "tracked_agents": len(self.agent_activity),
        }
