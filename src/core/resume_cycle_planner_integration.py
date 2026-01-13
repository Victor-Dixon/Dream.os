#!/usr/bin/env python3
"""
Resume Cycle Planner Integration

<!-- SSOT Domain: infrastructure -->

=================================

Connects agent resume prompts with cycle planner to automatically assign
tasks when agents resume work.

V2 Compliance: <300 lines, single responsibility
Author: Agent-4 (Captain)
Date: 2025-12-10
Priority: HIGH - Improves agent resume effectiveness
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class ResumeCyclePlannerIntegration:
    """Integrates resume prompts with cycle planner task assignment."""

    def __init__(self):
        """Initialize resume cycle planner integration."""
        try:
            from src.services.unified_service_managers import UnifiedContractManager
            from src.services.contract_system.cycle_planner_integration import (
                CyclePlannerIntegration
            )
            self.contract_manager = UnifiedContractManager()
            self.cycle_planner = CyclePlannerIntegration()
            self._initialized = True
        except ImportError as e:
            logger.warning(f"Contract system not available: {e}")
            self.contract_manager = None
            self.cycle_planner = None
            self._initialized = False

    def get_and_claim_next_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get and automatically claim next available task from cycle planner.
        
        This method:
        1. Checks cycle planner for pending tasks
        2. Automatically claims/assigns the task (marks as active)
        3. Returns task details for inclusion in resume prompt
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Task dictionary with assignment details, or None if no tasks
        """
        if not self._initialized:
            logger.warning("Resume cycle planner integration not initialized")
            return None

        try:
            # Use ContractManager to get and claim next task
            result = self.contract_manager.get_next_task(agent_id)
            
            if result.get("status") == "assigned" and result.get("task"):
                task = result["task"]
                
                logger.info(
                    f"✅ Claimed cycle planner task for {agent_id}: "
                    f"{task.get('title', 'Unknown')}"
                )
                
                # Return task with assignment context
                return {
                    "task_id": task.get("task_id") or task.get("contract_id", ""),
                    "title": task.get("title", "Untitled Task"),
                    "description": task.get("description", ""),
                    "priority": task.get("priority", "MEDIUM"),
                    "status": "assigned",  # Task has been claimed
                    "assigned_at": task.get("assigned_at"),
                    "source": result.get("source", "cycle_planner"),
                    "estimated_time": task.get("estimated_time", ""),
                    "deliverables": task.get("deliverables", []),
                }
            
            elif result.get("status") == "no_tasks":
                logger.debug(f"No tasks available for {agent_id}")
                return None
            
            else:
                logger.warning(
                    f"Unexpected result from get_next_task for {agent_id}: {result}"
                )
                return None
                
        except Exception as e:
            logger.error(f"Error getting/claiming task for {agent_id}: {e}")
            return None

    def get_next_task_preview(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Preview next available task without claiming it.
        
        Useful for displaying in resume prompt when auto-claim is disabled.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            Task dictionary (preview only, not claimed)
        """
        if not self._initialized or not self.cycle_planner:
            return None

        try:
            task = self.cycle_planner.get_next_cycle_task(agent_id)
            
            if task:
                return {
                    "task_id": task.get("task_id") or task.get("contract_id", ""),
                    "title": task.get("title", "Untitled Task"),
                    "description": task.get("description", ""),
                    "priority": task.get("priority", "MEDIUM"),
                    "status": "pending",  # Not yet claimed
                    "estimated_time": task.get("estimated_time", ""),
                    "deliverables": task.get("deliverables", []),
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Error previewing task for {agent_id}: {e}")
            return None


__all__ = ["ResumeCyclePlannerIntegration"]

