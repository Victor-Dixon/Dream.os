"""
<!-- SSOT Domain: core -->

Scheduler Integration - Status Monitor & Resume Logic
=====================================================

Integration layer connecting TaskScheduler with StatusMonitor and Resume Logic.

Provides:
- Bidirectional communication between scheduler and status monitor
- Scheduled tasks included in resume prompts
- Agent inactivity feedback to scheduler
- Pending task awareness in status monitoring

V2 Compliance: <300 lines, single responsibility

Author: Agent-4 (Captain)
Date: 2025-12-04
"""

import logging
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    # Avoid circular import at runtime
    from .scheduler import TaskScheduler
    from ..discord_commander.status_change_monitor import StatusChangeMonitor

logger = logging.getLogger(__name__)


class SchedulerStatusMonitorIntegration:
    """
    Integration between TaskScheduler and StatusChangeMonitor.
    
    Enables:
    - Scheduler notifications to status monitor
    - Status monitor queries to scheduler
    - Resume prompts with scheduled tasks
    - Agent inactivity feedback
    """
    
    def __init__(self, scheduler=None, status_monitor=None):
        """
        Initialize integration.
        
        Args:
            scheduler: TaskScheduler instance (optional)
            status_monitor: StatusChangeMonitor instance (optional)
        """
        self.scheduler = scheduler
        self.status_monitor = status_monitor
        logger.info("Scheduler-StatusMonitor integration initialized")
    
    def set_scheduler(self, scheduler: "TaskScheduler"):
        """Set scheduler instance."""
        self.scheduler = scheduler
    
    def set_status_monitor(self, status_monitor: "StatusChangeMonitor"):
        """Set status monitor instance."""
        self.status_monitor = status_monitor
    
    def notify_pending_task(self, agent_id: str, task_id: str, task_type: str, 
                           priority: int, scheduled_cycle: int):
        """
        Notify status monitor about pending scheduled task.
        
        Args:
            agent_id: Target agent
            task_id: Task identifier
            task_type: Type of task
            priority: Task priority
            scheduled_cycle: Scheduled cycle number
        """
        if not self.status_monitor:
            return
        
        try:
            if not hasattr(self.status_monitor, 'pending_tasks'):
                self.status_monitor.pending_tasks = {}
            
            if agent_id not in self.status_monitor.pending_tasks:
                self.status_monitor.pending_tasks[agent_id] = []
            
            self.status_monitor.pending_tasks[agent_id].append({
                "task_id": task_id,
                "task_type": task_type,
                "priority": priority,
                "scheduled_cycle": scheduled_cycle,
                "notified_at": datetime.now().isoformat()
            })
            
            logger.info(f"Notified status monitor: {agent_id} has pending task {task_id}")
        except Exception as e:
            logger.error(f"Failed to notify pending task: {e}")
    
    def get_pending_tasks_for_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all pending tasks for an agent from scheduler.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of pending task dictionaries
        """
        if not self.scheduler:
            return []
        
        try:
            pending = []
            task_registry = getattr(self.scheduler, 'task_registry', {})
            completed_tasks = getattr(self.scheduler, 'completed_tasks', set())
            failed_tasks = getattr(self.scheduler, 'failed_tasks', set())
            
            for task_id, task in task_registry.items():
                # Check if task has agent_id attribute and matches
                if (hasattr(task, 'agent_id') and 
                    getattr(task, 'agent_id', None) == agent_id and 
                    task_id not in completed_tasks and 
                    task_id not in failed_tasks):
                    pending.append({
                        "task_id": task.id,
                        "type": task.type,
                        "priority": task.priority,
                        "scheduled_cycle": getattr(task, 'scheduled_cycle', None),
                        "data": getattr(task, 'data', {}),
                        "estimated_duration": getattr(task, 'estimated_duration', 0)
                    })
            
            # Sort by priority (lower = higher priority), then scheduled cycle
            pending.sort(key=lambda x: (x.get("priority", 99), x.get("scheduled_cycle", 9999)))
            return pending
        except Exception as e:
            logger.error(f"Failed to get pending tasks for {agent_id}: {e}")
            return []
    
    def mark_agent_inactive(self, agent_id: str, inactivity_duration_minutes: float):
        """
        Mark agent as inactive in scheduler.
        
        Args:
            agent_id: Agent identifier
            inactivity_duration_minutes: Duration of inactivity
        """
        if not self.scheduler:
            return
        
        try:
            if not hasattr(self.scheduler, 'agent_inactivity'):
                self.scheduler.agent_inactivity = {}
            
            self.scheduler.agent_inactivity[agent_id] = {
                "is_inactive": True,
                "duration_minutes": inactivity_duration_minutes,
                "timestamp": datetime.now().isoformat()
            }
            
            # Reset agent load if very inactive (30+ minutes)
            if inactivity_duration_minutes > 30:
                if hasattr(self.scheduler, 'agent_load'):
                    self.scheduler.agent_load[agent_id] = 0.0
                    logger.info(f"Reset load for inactive agent {agent_id}")
            
            logger.info(f"Marked {agent_id} as inactive ({inactivity_duration_minutes:.1f} min)")
        except Exception as e:
            logger.error(f"Failed to mark agent inactive: {e}")
    
    def format_scheduled_tasks_for_prompt(self, agent_id: str) -> str:
        """
        Format scheduled tasks for inclusion in resume prompt.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Formatted string for prompt
        """
        pending_tasks = self.get_pending_tasks_for_agent(agent_id)
        
        if not pending_tasks:
            return ""
        
        formatted = "\n## 📋 SCHEDULED TASKS\n\n"
        formatted += f"You have **{len(pending_tasks)}** scheduled task(s) waiting:\n\n"
        
        for i, task in enumerate(pending_tasks, 1):
            formatted += f"### Task {i}: {task['type']}\n"
            formatted += f"- **Task ID**: `{task['task_id']}`\n"
            formatted += f"- **Priority**: {task['priority']}\n"
            if task.get('scheduled_cycle'):
                formatted += f"- **Scheduled Cycle**: {task['scheduled_cycle']}\n"
            if task.get('estimated_duration'):
                formatted += f"- **Estimated Duration**: {task['estimated_duration']}s\n"
            formatted += "\n"
        
        formatted += "**Action**: Review these tasks and continue execution.\n"
        
        return formatted
    
    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get integration status.
        
        Returns:
            Status dictionary
        """
        return {
            "scheduler_connected": self.scheduler is not None,
            "status_monitor_connected": self.status_monitor is not None,
            "integration_active": (self.scheduler is not None and 
                                  self.status_monitor is not None)
        }
