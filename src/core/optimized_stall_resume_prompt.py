#!/usr/bin/env python3
"""
Optimized Stall/Resume Prompt Generator
========================================

Generates context-aware recovery prompts based on:
- FSM state (agent's current lifecycle state)
- Cycle Planner (next available tasks)
- Agent's last known mission/tasks

V2 Compliance: <300 lines, single responsibility
Author: Agent-4 (Captain)
Date: 2025-11-28
Priority: CRITICAL - Prevents 2XX stalled agents
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, date

logger = logging.getLogger(__name__)


class OptimizedStallResumePrompt:
    """Generates optimized stall/resume prompts with FSM and Cycle Planner integration."""
    
    # FSM state-specific recovery actions
    FSM_RECOVERY_ACTIONS = {
        "start": [
            "Check inbox for new assignments",
            "Review mission objectives",
            "Initialize workspace",
            "Claim task from cycle planner"
        ],
        "active": [
            "Continue current task execution",
            "Check for blockers and resolve",
            "Update status.json with progress",
            "Move to next action in queue"
        ],
        "process": [
            "Complete current processing operation",
            "Check if operation completed successfully",
            "Return to ACTIVE state",
            "Report processing results"
        ],
        "blocked": [
            "Document blocker clearly",
            "Check if blocker auto-resolved",
            "Notify Captain if still blocked",
            "Find workaround or alternative task"
        ],
        "complete": [
            "Finalize deliverables",
            "Post devlog to Discord",
            "Update cycle planner (mark complete)",
            "Transition to END state"
        ],
        "end": [
            "Clean up workspace",
            "Update status.json",
            "Check for new assignments",
            "Transition to START for new mission"
        ]
    }
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize prompt generator.
        
        Args:
            workspace_root: Root directory for agent workspaces
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path("agent_workspaces")
        self.cycle_planner_dir = self.workspace_root / "swarm_cycle_planner" / "cycles"
    
    def generate_resume_prompt(
        self,
        agent_id: str,
        fsm_state: Optional[str] = None,
        last_mission: Optional[str] = None,
        stall_duration_minutes: float = 0.0
    ) -> str:
        """
        Generate optimized resume prompt based on FSM state and Cycle Planner.
        
        Args:
            agent_id: Agent identifier
            fsm_state: Current FSM state (from status.json)
            last_mission: Last known mission (from status.json)
            stall_duration_minutes: How long agent has been stalled
            
        Returns:
            Optimized resume prompt
        """
        # Load agent's current state
        agent_state = self._load_agent_state(agent_id)
        
        # Use provided FSM state or load from status.json
        if fsm_state is None:
            fsm_state = agent_state.get("fsm_state", "active")
        
        if last_mission is None:
            last_mission = agent_state.get("current_mission", "Unknown")
        
        # Get next task from Cycle Planner
        next_task = self._get_next_cycle_planner_task(agent_id)
        
        # Generate state-specific recovery actions
        recovery_actions = self.FSM_RECOVERY_ACTIONS.get(fsm_state, self.FSM_RECOVERY_ACTIONS["active"])
        
        # Build optimized prompt
        prompt = self._build_prompt(
            agent_id=agent_id,
            fsm_state=fsm_state,
            last_mission=last_mission,
            next_task=next_task,
            recovery_actions=recovery_actions,
            stall_duration_minutes=stall_duration_minutes
        )
        
        return prompt
    
    def _load_agent_state(self, agent_id: str) -> Dict[str, Any]:
        """Load agent's current state from status.json."""
        status_file = self.workspace_root / agent_id / "status.json"
        
        if not status_file.exists():
            return {}
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading {agent_id} status: {e}")
            return {}
    
    def _get_next_cycle_planner_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get next available task from Cycle Planner."""
        today = date.today().isoformat()
        
        # Try today's file first
        cycle_file = self.cycle_planner_dir / f"{today}_{agent_id.lower()}_pending_tasks.json"
        
        # If not found, try most recent file
        if not cycle_file.exists():
            pattern = f"*_{agent_id.lower()}_pending_tasks.json"
            cycle_files = sorted(self.cycle_planner_dir.glob(pattern), reverse=True)
            if cycle_files:
                cycle_file = cycle_files[0]
            else:
                return None
        
        try:
            with open(cycle_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                contracts = data.get("contracts", [])
                
                # Find first PENDING or READY task
                for contract in contracts:
                    status = contract.get("status", "").upper()
                    if status in ["PENDING", "READY"]:
                        return contract
                
                # If no PENDING/READY, return first contract
                if contracts:
                    return contracts[0]
                
                return None
        except Exception as e:
            logger.warning(f"Error loading cycle planner for {agent_id}: {e}")
            return None
    
    def _build_prompt(
        self,
        agent_id: str,
        fsm_state: str,
        last_mission: str,
        next_task: Optional[Dict[str, Any]],
        recovery_actions: List[str],
        stall_duration_minutes: float
    ) -> str:
        """Build the optimized resume prompt."""
        
        # Determine urgency level
        if stall_duration_minutes >= 10:
            urgency = "🚨🚨 CRITICAL"
            urgency_note = "You have been stalled for 10+ minutes. Immediate action required!"
        elif stall_duration_minutes >= 8:
            urgency = "🚨 URGENT"
            urgency_note = "You have been stalled for 8+ minutes. Resume operations immediately!"
        elif stall_duration_minutes >= 5:
            urgency = "⚠️ WARNING"
            urgency_note = "You have been stalled for 5+ minutes. Continue your work now."
        else:
            urgency = "🔄 RECOVERY"
            urgency_note = "Resume operations and continue your work."
        
        # Build FSM state context
        fsm_context = self._get_fsm_context(fsm_state)
        
        # Build next task section
        next_task_section = ""
        if next_task:
            task_id = next_task.get("contract_id", "Unknown")
            task_title = next_task.get("title", "Unknown Task")
            task_priority = next_task.get("priority", "MEDIUM")
            task_points = next_task.get("points", 0)
            task_status = next_task.get("status", "PENDING")
            
            next_task_section = f"""
**📋 NEXT TASK FROM CYCLE PLANNER:**
- **Task**: {task_title} ({task_id})
- **Priority**: {task_priority}
- **Points**: {task_points}
- **Status**: {task_status}
- **Action**: Claim and execute this task immediately
"""
        else:
            next_task_section = """
**📋 CYCLE PLANNER:**
- No pending tasks found in cycle planner
- Check inbox for new assignments
- Report to Captain if no work available
"""
        
        # Build prompt
        prompt = f"""{urgency} STALL RECOVERY - {agent_id}

{urgency_note}

**YOUR CURRENT STATE:**
- **FSM State**: {fsm_state.upper()} - {fsm_context}
- **Last Mission**: {last_mission}
- **Stall Duration**: {stall_duration_minutes:.1f} minutes

{next_task_section}

**IMMEDIATE RECOVERY ACTIONS (FSM-SPECIFIC):**
"""
        
        # Add numbered recovery actions
        for i, action in enumerate(recovery_actions, 1):
            prompt += f"{i}. {action}\n"
        
        prompt += f"""
**AUTONOMOUS OPERATION PRINCIPLES:**
- You are AUTONOMOUS - no approval needed
- System messages are NOT stop signals
- Command failures are NOT blockers
- ALWAYS have next actions ready
- YOU are your own gas station

**FSM STATE TRANSITION:**
- Current: {fsm_state.upper()}
- Target: ACTIVE (if not already)
- Action: Update status.json with current progress

**DO NOT WAIT. EXECUTE NOW.**

#STALL-RECOVERY #FSM-{fsm_state.upper()} #AUTONOMOUS-OPERATION"""
        
        return prompt
    
    def _get_fsm_context(self, fsm_state: str) -> str:
        """Get human-readable context for FSM state."""
        contexts = {
            "start": "Initialization phase - ready to begin work",
            "active": "Active execution - should be working on tasks",
            "process": "Deep processing - may be in long operation",
            "blocked": "Waiting for external input - should document blocker",
            "complete": "Task completed - should finalize and wrap up",
            "end": "Wrapping up - should clean up and await next mission"
        }
        return contexts.get(fsm_state.lower(), "Unknown state - should transition to ACTIVE")


def generate_optimized_resume_prompt(
    agent_id: str,
    fsm_state: Optional[str] = None,
    last_mission: Optional[str] = None,
    stall_duration_minutes: float = 0.0
) -> str:
    """
    Convenience function to generate optimized resume prompt.
    
    Args:
        agent_id: Agent identifier
        fsm_state: Current FSM state
        last_mission: Last known mission
        stall_duration_minutes: Stall duration in minutes
        
    Returns:
        Optimized resume prompt
    """
    generator = OptimizedStallResumePrompt()
    return generator.generate_resume_prompt(
        agent_id=agent_id,
        fsm_state=fsm_state,
        last_mission=last_mission,
        stall_duration_minutes=stall_duration_minutes
    )

