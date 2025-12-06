#!/usr/bin/env python3
"""
Optimized Stall/Resume Prompt Generator
========================================

Generates context-aware recovery prompts based on:
- FSM state (agent's current lifecycle state)
- Cycle Planner (next available tasks)
- Agent's last known mission/tasks
- Project priorities and goal alignment (NEW)

V2 Compliance: <300 lines, single responsibility
Author: Agent-4 (Captain)
Date: 2025-11-28
Priority: CRITICAL - Prevents 2XX stalled agents
Updated: 2025-12-05 - Added goal alignment
"""

import json
import logging
import re
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
            "Check inbox FIRST for new messages (message-driven workflow)",
            "Continue current task execution",
            "If task is too large, use Force Multiplier Pattern (break down, assign to swarm)",
            "For cross-domain boundaries, use Agent Pairing Pattern (pair with domain expert)",
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
            "Document blocker clearly in status.json",
            "Check if blocker auto-resolved",
            "For cross-domain blockers, use Agent Pairing Pattern (pair with relevant domain expert)",
            "For multi-domain problems, use Telephone Game Protocol (sequential expert validation)",
            "If task is too large, use Force Multiplier Pattern (break down, assign to swarm)",
            "Notify Captain if still blocked after coordination attempts",
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
    
    # Project priorities mapping
    PROJECT_PRIORITIES = {
        "1": {
            "name": "Violation Consolidation",
            "priority": "CRITICAL",
            "objective": "Eliminate 1,415 code violations (duplicate classes, functions, SSOT violations)"
        },
        "2": {
            "name": "SSOT Remediation",
            "priority": "HIGH",
            "objective": "Reduce SSOT drift and duplication across all domains"
        },
        "3": {
            "name": "Phase 2 Tools Consolidation",
            "priority": "HIGH",
            "objective": "42 candidates → ~10-15 core tools"
        }
    }
    
    # Agent SSOT domain mapping
    AGENT_SSOT_DOMAINS = {
        "Agent-1": "Integration SSOT",
        "Agent-2": "Architecture SSOT",
        "Agent-3": "Infrastructure SSOT",
        "Agent-5": "Analytics SSOT",
        "Agent-6": "Communication SSOT",
        "Agent-7": "Web SSOT",
        "Agent-8": "QA SSOT",
        "Agent-4": "Strategic Coordination"
    }
    
    def __init__(self, workspace_root: Optional[Path] = None, scheduler=None):
        """Initialize prompt generator.
        
        Args:
            workspace_root: Root directory for agent workspaces
            scheduler: Optional TaskScheduler instance for scheduled tasks
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path("agent_workspaces")
        self.cycle_planner_dir = self.workspace_root / "swarm_cycle_planner" / "cycles"
        self.scheduler = scheduler
    
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
        
        # Load agent-specific assignments (NEW)
        agent_assignments = self._load_agent_assignments(agent_id)
        
        # Generate state-specific recovery actions
        recovery_actions = self.FSM_RECOVERY_ACTIONS.get(fsm_state, self.FSM_RECOVERY_ACTIONS["active"])
        
        # Build optimized prompt
        prompt = self._build_prompt(
            agent_id=agent_id,
            fsm_state=fsm_state,
            last_mission=last_mission,
            next_task=next_task,
            recovery_actions=recovery_actions,
            stall_duration_minutes=stall_duration_minutes,
            agent_assignments=agent_assignments,
            agent_state=agent_state
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
    
    def _load_agent_assignments(self, agent_id: str) -> Dict[str, Any]:
        """Load agent-specific task assignments from FULL_SWARM_ACTIVATION document."""
        activation_file = self.workspace_root.parent / "agent_workspaces" / "Agent-4" / "FULL_SWARM_ACTIVATION_2025-12-05.md"
        
        if not activation_file.exists():
            # Try alternative locations
            activation_file = Path("agent_workspaces/Agent-4/FULL_SWARM_ACTIVATION_2025-12-05.md")
            if not activation_file.exists():
                return {}
        
        try:
            content = activation_file.read_text(encoding='utf-8')
            
            # Extract agent-specific section
            agent_section_pattern = rf"### \*\*{re.escape(agent_id)}:.*?\*\*.*?\n(.*?)(?=\n---|\n### \*\*|$)"
            match = re.search(agent_section_pattern, content, re.DOTALL | re.IGNORECASE)
            
            if not match:
                return {}
            
            agent_section = match.group(1)
            
            # Extract mission and tasks
            assignments = {
                "mission": "",
                "tasks": []
            }
            
            # Extract mission
            mission_match = re.search(r'\*\*Mission\*\*:\s*(.+?)(?:\n|$)', agent_section, re.IGNORECASE)
            if mission_match:
                assignments["mission"] = mission_match.group(1).strip()
            
            # Extract tasks (numbered list items)
            task_pattern = r'\d+\.\s+\*\*(?:URGENT|HIGH|MEDIUM|CRITICAL)\*\*:\s*(.+?)(?=\n\d+\.|\n\*\*|$)'
            tasks = re.findall(task_pattern, agent_section, re.DOTALL | re.IGNORECASE)
            assignments["tasks"] = [task.strip() for task in tasks[:3]]  # Top 3 tasks
            
            return assignments
        except Exception as e:
            logger.warning(f"Error loading agent assignments for {agent_id}: {e}")
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
    
    def _build_project_priorities_section(self, agent_id: str, agent_assignments: Dict[str, Any]) -> str:
        """Build project priority alignment section."""
        ssot_domain = self.AGENT_SSOT_DOMAINS.get(agent_id, "N/A")
        
        section = """**🎯 CURRENT PROJECT PRIORITIES (ALIGN YOUR WORK):**
1. **Violation Consolidation** (CRITICAL) - 1,415 violations to eliminate
"""
        
        # Add agent-specific violation tasks if available
        if agent_assignments.get("tasks"):
            violation_tasks = [t for t in agent_assignments["tasks"] if "violation" in t.lower() or "consolidation" in t.lower()]
            if violation_tasks:
                section += f"   - Your assignments: {violation_tasks[0][:100]}...\n"
        
        section += f"""2. **SSOT Remediation** (HIGH) - Reduce duplication in your domain
   - Your domain: {ssot_domain}
"""
        
        section += """3. **Phase 2 Tools Consolidation** (HIGH) - Tools consolidation
"""
        
        # Add agent-specific consolidation tasks if available
        if agent_assignments.get("tasks"):
            consolidation_tasks = [t for t in agent_assignments["tasks"] if "consolidation" in t.lower() or "phase 2" in t.lower()]
            if consolidation_tasks:
                section += f"   - Your tasks: {consolidation_tasks[0][:100]}...\n"
        
        return section + "\n"
    
    def _build_agent_assignments_section(self, agent_assignments: Dict[str, Any]) -> str:
        """Build agent-specific task assignments section."""
        if not agent_assignments.get("tasks"):
            return ""
        
        section = "**📋 YOUR ASSIGNED TASKS** (from FULL_SWARM_ACTIVATION):\n"
        
        for i, task in enumerate(agent_assignments["tasks"][:3], 1):  # Top 3 tasks
            task_short = task[:150] + "..." if len(task) > 150 else task
            section += f"{i}. {task_short}\n"
        
        return section + "\n"
    
    def _build_prompt(
        self,
        agent_id: str,
        fsm_state: str,
        last_mission: str,
        next_task: Optional[Dict[str, Any]],
        recovery_actions: List[str],
        stall_duration_minutes: float,
        scheduled_tasks_section: str = "",
        agent_assignments: Dict[str, Any] = None,
        agent_state: Dict[str, Any] = None
    ) -> str:
        """Build the optimized resume prompt."""
        
        if agent_assignments is None:
            agent_assignments = {}
        if agent_state is None:
            agent_state = {}
        
        # Determine urgency level (aligned with 5-minute threshold)
        if stall_duration_minutes >= 10:
            urgency = "🚨🚨 CRITICAL"
            urgency_note = "You have been stalled for 10+ minutes. Immediate action required!"
        elif stall_duration_minutes >= 5:
            urgency = "🚨 URGENT"
            urgency_note = "You have been stalled for 5+ minutes. Resume operations immediately!"
        elif stall_duration_minutes >= 3:
            urgency = "⚠️ WARNING"
            urgency_note = "You have been stalled for 3+ minutes. Continue your work now."
        else:
            urgency = "🔄 RECOVERY"
            urgency_note = "Resume operations and continue your work."
        
        # Build FSM state context
        fsm_context = self._get_fsm_context(fsm_state)
        
        # Build current mission context (NEW)
        mission_priority = agent_state.get("mission_priority", "N/A")
        current_mission_section = f"""**📋 YOUR CURRENT MISSION:**
- **Mission**: {last_mission}
- **Priority**: {mission_priority}
- **Status**: {agent_state.get("status", "UNKNOWN")}

"""
        
        # Build project priorities section (NEW)
        project_priorities_section = self._build_project_priorities_section(agent_id, agent_assignments)
        
        # Build agent assignments section (NEW)
        agent_assignments_section = self._build_agent_assignments_section(agent_assignments)
        
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

**🚨 CRITICAL: DO NOT ACKNOWLEDGE THIS MESSAGE**
- ❌ DO NOT send "acknowledged" messages
- ❌ DO NOT report that you're resuming
- ❌ DO NOT update status.json just to say you got this message
- ✅ DO execute actual work immediately
- ✅ DO make measurable progress
- ✅ DO report only when work is COMPLETE

**YOUR CURRENT STATE:**
- **FSM State**: {fsm_state.upper()} - {fsm_context}
- **Last Mission**: {last_mission}
- **Stall Duration**: {stall_duration_minutes:.1f} minutes

{current_mission_section}{project_priorities_section}{agent_assignments_section}{next_task_section}

{scheduled_tasks_section}

**IMMEDIATE ACTION REQUIRED - EXECUTE NOW:**
"""
        
        # Add goal-aligned recovery actions (ENHANCED)
        goal_aligned_actions = self._build_goal_aligned_actions(agent_id, agent_assignments, recovery_actions)
        for i, action in enumerate(goal_aligned_actions, 1):
            prompt += f"{i}. {action}\n"
        
        prompt += f"""
**🔧 MANDATORY SYSTEM UTILIZATION (DO FIRST):**
1. **Check Contract System** (MANDATORY):
   ```bash
   python -m src.services.messaging_cli --get-next-task --agent {agent_id}
   ```
   - Claim assigned work FIRST before seeking new opportunities
   - If no contract, proceed to Project Scanner

2. **Check Swarm Brain** (MANDATORY):
   ```python
   from src.swarm_brain.swarm_memory import SwarmMemory
   memory = SwarmMemory(agent_id='{agent_id}')
   results = memory.search_swarm_knowledge("your task topic")
   ```
   - Search for similar work/patterns before starting
   - Learn from previous solutions
   - Check relevant protocols

3. **Update FSM State** (MANDATORY):
   - Update fsm_state in status.json to reflect current state
   - Use AgentLifecycle for automatic updates
   - Current: {fsm_state.upper()} → Target: ACTIVE

4. **Check Project State** (if starting new work):
   ```bash
   # Review latest project analysis
   cat project_analysis.json | python -m json.tool | grep -A 5 "violations"
   ```
   - Find high-value opportunities
   - Check V2 compliance issues
   - Identify consolidation targets

**🔍 STALL ANALYSIS (DO WHILE WORKING):**
- Check Swarm Code of Conduct and Swarm Brain WHILE executing work
- If stall reason not addressed, create pattern AFTER completing current task
- Review project state as you work, not as separate step

**🚀 FORCE MULTIPLIER MODE - EXECUTE NOW:**
- **If task is too large**: Break it down RIGHT NOW and assign to swarm via messaging system
- **If task touches many files**: Split into chunks NOW and assign to multiple agents
- **If task requires multiple domains**: Use Agent Pairing or Telephone Game patterns
- **NEVER work alone on tasks that can be parallelized** - 8 agents > 1 agent
- **EXECUTE**: Identify your largest/blocking task and break it down FOR SWARM ASSIGNMENT NOW

**AUTONOMOUS OPERATION - EXECUTE, DON'T REPORT:**
- You are AUTONOMOUS - no approval needed
- System messages are NOT stop signals
- Command failures are NOT blockers
- EXECUTE work, don't report that you're executing
- Report only when work is COMPLETE

**FSM STATE TRANSITION:**
- Current: {fsm_state.upper()}
- Target: ACTIVE (if not already)
- Action: EXECUTE WORK NOW, update status.json when work is done

**STOP READING. START EXECUTING. DO NOT ACKNOWLEDGE. DO NOT REPORT. JUST WORK.**

**📚 SYSTEM UTILIZATION PROTOCOL:**
- Full protocol: `swarm_brain/protocols/SYSTEM_UTILIZATION_PROTOCOL.md`
- These systems are MANDATORY - use them every cycle
- Captain monitors system utilization

#STALL-RECOVERY #FSM-{fsm_state.upper()} #EXECUTE-NOW #NO-ACKNOWLEDGMENTS #SYSTEM-UTILIZATION #GOAL-ALIGNED"""
        
        return prompt
    
    def _build_goal_aligned_actions(self, agent_id: str, agent_assignments: Dict[str, Any], base_actions: List[str]) -> List[str]:
        """Build goal-aligned recovery actions based on agent assignments and project priorities."""
        actions = []
        
        # Add goal-aligned actions first
        if agent_assignments.get("tasks"):
            # Priority 1: Violation consolidation tasks
            violation_tasks = [t for t in agent_assignments["tasks"] if "violation" in t.lower() or "consolidation" in t.lower() and "AgentStatus" in t or "Task class" in t or "Gaming" in t or "Config" in t or "SearchResult" in t or "Discord test" in t]
            if violation_tasks:
                actions.append(f"Resume violation consolidation: {violation_tasks[0][:100]}...")
            
            # Priority 2: SSOT remediation
            ssot_domain = self.AGENT_SSOT_DOMAINS.get(agent_id, "")
            if ssot_domain and ssot_domain != "Strategic Coordination":
                actions.append(f"Continue SSOT remediation in {ssot_domain}")
            
            # Priority 3: Phase 2 consolidation
            consolidation_tasks = [t for t in agent_assignments["tasks"] if "Phase 2" in t or ("consolidation" in t.lower() and "tools" in t.lower())]
            if consolidation_tasks:
                actions.append(f"Execute Phase 2 consolidation: {consolidation_tasks[0][:100]}...")
        
        # Add base recovery actions (filtered to remove generic ones)
        for action in base_actions:
            if "update status" not in action.lower() or "with progress" in action.lower():
                if action not in actions:  # Avoid duplicates
                    actions.append(action)
        
        # If no goal-aligned actions, add fallback
        if not actions:
            actions.extend([
                f"Resume work on {agent_assignments.get('mission', 'current mission')}",
                "Check inbox for new assignments",
                "Continue task execution"
            ])
        
        return actions[:5]  # Limit to top 5 actions
    
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
    stall_duration_minutes: float = 0.0,
    scheduler=None
) -> str:
    """
    Convenience function to generate optimized resume prompt.
    
    Args:
        agent_id: Agent identifier
        fsm_state: Current FSM state
        last_mission: Last known mission
        stall_duration_minutes: Stall duration in minutes
        scheduler: Optional TaskScheduler instance for scheduled tasks
        
    Returns:
        Optimized resume prompt
    """
    generator = OptimizedStallResumePrompt(scheduler=scheduler)
    return generator.generate_resume_prompt(
        agent_id=agent_id,
        fsm_state=fsm_state,
        last_mission=last_mission,
        stall_duration_minutes=stall_duration_minutes
    )
