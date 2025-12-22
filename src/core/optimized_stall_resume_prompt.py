#!/usr/bin/env python3
"""
Optimized Stall/Resume Prompt Generator

<!-- SSOT Domain: infrastructure -->

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

from src.core.messaging_models_core import MessageCategory, MESSAGE_TEMPLATES

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

    def __init__(self, workspace_root: Optional[Path] = None, scheduler=None, auto_claim_tasks: bool = True):
        """Initialize prompt generator.

        Args:
            workspace_root: Root directory for agent workspaces
            scheduler: Optional TaskScheduler instance for scheduled tasks
            auto_claim_tasks: If True, automatically claim tasks when resuming (default: True)
        """
        self.workspace_root = Path(
            workspace_root) if workspace_root else Path("agent_workspaces")
        self.cycle_planner_dir = self.workspace_root / "swarm_cycle_planner" / "cycles"
        self.scheduler = scheduler
        self.auto_claim_tasks = auto_claim_tasks

        # Initialize resume cycle planner integration
        try:
            from src.core.resume_cycle_planner_integration import ResumeCyclePlannerIntegration
            self.resume_planner = ResumeCyclePlannerIntegration()
        except ImportError:
            logger.warning("Resume cycle planner integration not available")
            self.resume_planner = None

    def generate_resume_prompt(
        self,
        agent_id: str,
        fsm_state: Optional[str] = None,
        last_mission: Optional[str] = None,
        stall_duration_minutes: float = 0.0,
        validate_activity: bool = True
    ) -> Optional[str]:
        """
        Generate optimized resume prompt based on FSM state and Cycle Planner.

        Args:
            agent_id: Agent identifier
            fsm_state: Current FSM state (from status.json)
            last_mission: Last known mission (from status.json)
            stall_duration_minutes: How long agent has been stalled
            validate_activity: If True, validate agent is inactive before generating

        Returns:
            Optimized resume prompt, or None if agent is active (when validate_activity=True)
        """
        # Validate agent activity before generating resume prompt
        if validate_activity:
            try:
                from src.core.stall_resumer_guard import should_send_resume
                should_send, reason = should_send_resume(agent_id, lookback_minutes=60)
                
                if not should_send:
                    logger.info(
                        f"⏸️ Skipping resume prompt for {agent_id}: {reason}"
                    )
                    return None
            except Exception as e:
                logger.warning(
                    f"Activity validation failed for {agent_id}, proceeding anyway: {e}"
                )
        
        # Load agent's current state
        agent_state = self._load_agent_state(agent_id)

        # Use provided FSM state or load from status.json
        if fsm_state is None:
            fsm_state = agent_state.get("fsm_state", "active")

        if last_mission is None:
            last_mission = agent_state.get("current_mission", "Unknown")

        # Get next task from Cycle Planner (with auto-claim if enabled)
        if self.auto_claim_tasks and self.resume_planner:
            next_task = self.resume_planner.get_and_claim_next_task(agent_id)
        else:
            # Preview mode - don't claim yet
            if self.resume_planner:
                next_task = self.resume_planner.get_next_task_preview(agent_id)
            else:
                next_task = self._get_next_cycle_planner_task(agent_id)

        # Load agent-specific assignments (NEW)
        agent_assignments = self._load_agent_assignments(agent_id)

        # Generate state-specific recovery actions
        recovery_actions = self.FSM_RECOVERY_ACTIONS.get(
            fsm_state, self.FSM_RECOVERY_ACTIONS["active"])

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
        activation_file = self.workspace_root.parent / "agent_workspaces" / \
            "Agent-4" / "FULL_SWARM_ACTIVATION_2025-12-05.md"

        if not activation_file.exists():
            # Try alternative locations
            activation_file = Path(
                "agent_workspaces/Agent-4/FULL_SWARM_ACTIVATION_2025-12-05.md")
            if not activation_file.exists():
                return {}

        try:
            content = activation_file.read_text(encoding='utf-8')

            # Extract agent-specific section
            agent_section_pattern = rf"### \*\*{re.escape(agent_id)}:.*?\*\*.*?\n(.*?)(?=\n---|\n### \*\*|$)"
            match = re.search(agent_section_pattern, content,
                              re.DOTALL | re.IGNORECASE)

            if not match:
                return {}

            agent_section = match.group(1)

            # Extract mission and tasks
            assignments = {
                "mission": "",
                "tasks": []
            }

            # Extract mission
            mission_match = re.search(
                r'\*\*Mission\*\*:\s*(.+?)(?:\n|$)', agent_section, re.IGNORECASE)
            if mission_match:
                assignments["mission"] = mission_match.group(1).strip()

            # Extract tasks (numbered list items)
            task_pattern = r'\d+\.\s+\*\*(?:URGENT|HIGH|MEDIUM|CRITICAL)\*\*:\s*(.+?)(?=\n\d+\.|\n\*\*|$)'
            tasks = re.findall(task_pattern, agent_section,
                               re.DOTALL | re.IGNORECASE)
            assignments["tasks"] = [task.strip()
                                    for task in tasks[:3]]  # Top 3 tasks

            return assignments
        except Exception as e:
            logger.warning(
                f"Error loading agent assignments for {agent_id}: {e}")
            return {}

    def _get_next_cycle_planner_task(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get next available task from Cycle Planner (fallback method)."""
        # Use cycle planner integration if available
        if self.resume_planner:
            return self.resume_planner.get_next_task_preview(agent_id)

        # Fallback to old method (deprecated)
        today = date.today().isoformat()
        cycle_file = self.workspace_root / agent_id / \
            f"cycle_planner_tasks_{today}.json"

        if not cycle_file.exists():
            return None

        try:
            with open(cycle_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                tasks = data.get("pending_tasks", data.get("tasks", []))

                # Find first pending task
                for task in tasks:
                    status = task.get("status", "").lower()
                    if status in ["pending", "ready"]:
                        return task

                return tasks[0] if tasks else None
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
            violation_tasks = [t for t in agent_assignments["tasks"]
                               if "violation" in t.lower() or "consolidation" in t.lower()]
            if violation_tasks:
                section += f"   - Your assignments: {violation_tasks[0][:100]}...\n"

        section += f"""2. **SSOT Remediation** (HIGH) - Reduce duplication in your domain
   - Your domain: {ssot_domain}
"""

        section += """3. **Phase 2 Tools Consolidation** (HIGH) - Tools consolidation
"""

        # Add agent-specific consolidation tasks if available
        if agent_assignments.get("tasks"):
            consolidation_tasks = [t for t in agent_assignments["tasks"]
                                   if "consolidation" in t.lower() or "phase 2" in t.lower()]
            if consolidation_tasks:
                section += f"   - Your tasks: {consolidation_tasks[0][:100]}...\n"

        return section + "\n"

    def _build_agent_assignments_section(self, agent_assignments: Dict[str, Any]) -> str:
        """Build agent-specific task assignments section."""
        if not agent_assignments.get("tasks"):
            return ""

        section = "**📋 YOUR ASSIGNED TASKS** (from FULL_SWARM_ACTIVATION):\n"

        # Top 3 tasks
        for i, task in enumerate(agent_assignments["tasks"][:3], 1):
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
        """Build comprehensive SWARM_PULSE-style resume prompt."""
        return self._format_swarm_pulse_prompt(
            agent_id=agent_id,
            fsm_state=fsm_state,
            last_mission=last_mission,
            next_task=next_task,
            stall_duration_minutes=stall_duration_minutes,
            scheduled_tasks_section=scheduled_tasks_section,
            agent_assignments=agent_assignments or {},
            agent_state=agent_state or {}
        )
    
    def _format_swarm_pulse_prompt(
        self,
        agent_id: str,
        fsm_state: str,
        last_mission: str,
        next_task: Optional[Dict[str, Any]],
        stall_duration_minutes: float,
        scheduled_tasks_section: str = "",
        agent_assignments: Dict[str, Any] = None,
        agent_state: Dict[str, Any] = None
    ) -> str:
        """Format SWARM_PULSE template with dynamic values and integrated sections."""
        # Get SWARM_PULSE template
        templates = MESSAGE_TEMPLATES.get(MessageCategory.S2A, {})
        swarm_pulse_template = templates.get("SWARM_PULSE", "")
        
        if not swarm_pulse_template:
            logger.warning("SWARM_PULSE template not found, falling back to minimal prompt")
            return self._build_minimal_fallback_prompt(agent_id, fsm_state, last_mission, next_task, stall_duration_minutes)
        
        # Format time since update
        time_since_update = self._format_time_since_update(stall_duration_minutes)
        
        # Get FSM context
        fsm_context = self._get_fsm_context(fsm_state)
        fsm_state_with_context = f"{fsm_state.upper()} - {fsm_context}"
        
        # Build task information
        task_title, task_priority, task_points, task_status = self._extract_task_info(next_task)
        
        # Format base template
        prompt = swarm_pulse_template.format(
            recipient=agent_id,
            fsm_state=fsm_state_with_context,
            current_mission=last_mission or "Unknown",
            time_since_update=time_since_update,
            next_task=task_title,
            task_priority=task_priority,
            task_points=task_points,
            task_status=task_status,
        )
        
        # Insert project priorities section after "YOUR CURRENT STATE"
        project_priorities = self._build_project_priorities_section(agent_id, agent_assignments or {})
        if project_priorities:
            # Insert after "YOUR CURRENT STATE" section
            state_section_end = prompt.find("**📋 NEXT TASK FROM CYCLE PLANNER:**")
            if state_section_end > 0:
                prompt = prompt[:state_section_end] + "\n" + project_priorities + prompt[state_section_end:]
        
        # Insert agent assignments section after project priorities
        agent_assignments_section = self._build_agent_assignments_section(agent_assignments or {})
        if agent_assignments_section:
            # Insert after project priorities or after current state if no priorities
            insert_point = prompt.find("**📋 NEXT TASK FROM CYCLE PLANNER:**")
            if insert_point > 0:
                prompt = prompt[:insert_point] + "\n" + agent_assignments_section + prompt[insert_point:]
        
        # Insert scheduled tasks section if available (before "SWARM SYNC CHECKLIST")
        if scheduled_tasks_section:
            checklist_start = prompt.find("**SWARM SYNC CHECKLIST (DO THESE NOW):**")
            if checklist_start > 0:
                prompt = prompt[:checklist_start] + "\n" + scheduled_tasks_section + "\n" + prompt[checklist_start:]
        
        # Enhance task section with detailed task information
        if next_task:
            task_details = self._build_detailed_task_section(agent_id, next_task)
            # Replace the basic task section with detailed one
            task_section_start = prompt.find("**📋 NEXT TASK FROM CYCLE PLANNER:**")
            task_section_end = prompt.find("**SWARM SYNC CHECKLIST", task_section_start)
            if task_section_start > 0 and task_section_end > 0:
                # Replace from start of task section to start of checklist
                prompt = prompt[:task_section_start] + task_details + "\n\n" + prompt[task_section_end:]
        else:
            # No task available - add MASTER_TASK_LOG bridge instructions
            no_task_section = self._build_no_task_section(agent_id)
            task_section_start = prompt.find("**📋 NEXT TASK FROM CYCLE PLANNER:**")
            task_section_end = prompt.find("**SWARM SYNC CHECKLIST", task_section_start)
            if task_section_start > 0 and task_section_end > 0:
                # Replace from start of task section to start of checklist
                prompt = prompt[:task_section_start] + no_task_section + "\n\n" + prompt[task_section_end:]
        
        return prompt
    
    def _format_time_since_update(self, stall_duration_minutes: float) -> str:
        """Format stall duration as human-readable time string."""
        if stall_duration_minutes < 1:
            return "Less than 1 minute"
        elif stall_duration_minutes < 60:
            return f"{int(stall_duration_minutes)} minute{'s' if int(stall_duration_minutes) != 1 else ''}"
        else:
            hours = int(stall_duration_minutes // 60)
            minutes = int(stall_duration_minutes % 60)
            if minutes == 0:
                return f"{hours} hour{'s' if hours != 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
    
    def _extract_task_info(self, next_task: Optional[Dict[str, Any]]) -> tuple[str, str, str, str]:
        """Extract task information for template formatting."""
        if not next_task:
            return "No tasks available", "N/A", "N/A", "N/A"
        
        task_title = next_task.get("title", "Untitled Task")
        task_priority = next_task.get("priority", "MEDIUM")
        task_points = str(next_task.get("points", "N/A"))
        task_status = next_task.get("status", "pending").upper()
        
        return task_title, task_priority, task_points, task_status
    
    def _build_detailed_task_section(self, agent_id: str, next_task: Dict[str, Any]) -> str:
        """Build detailed task section with claim instructions or assignment confirmation."""
        task_title = next_task.get("title", "Untitled Task")
        task_id = next_task.get("task_id", "")
        task_status = next_task.get("status", "pending")
        task_desc = next_task.get("description", "")
        task_priority = next_task.get("priority", "MEDIUM")
        task_points = next_task.get("points", "N/A")
        
        if task_status == "assigned":
            section = f"""**✅ TASK ASSIGNED FROM CYCLE PLANNER:**
- **Task**: {task_title}
- **Task ID**: {task_id}
- **Priority**: {task_priority}
- **Points**: {task_points}
- **Status**: ASSIGNED (already claimed for you)
"""
            if task_desc:
                desc_preview = task_desc[:200] + "..." if len(task_desc) > 200 else task_desc
                section += f"- **Description**: {desc_preview}\n"
            section += "\n- **Action**: Begin work on this assigned task immediately.\n"
        else:
            section = f"""**📋 AVAILABLE TASK IN CYCLE PLANNER:**
- **Task**: {task_title}
- **Task ID**: {task_id}
- **Priority**: {task_priority}
- **Points**: {task_points}
- **Status**: {task_status.upper()}
- **Action**: Claim and execute this task immediately

**To Claim**: Run `python -m src.services.messaging_cli --agent {agent_id} --get-next-task`
"""
        
        return section
    
    def _build_no_task_section(self, agent_id: str) -> str:
        """Build section for when no tasks are available."""
        return f"""**📋 NO TASKS FOUND IN CYCLE PLANNER FOR {agent_id}**

When your cycle planner is empty, you MUST refill work from `MASTER_TASK_LOG.md`:

1. Open `MASTER_TASK_LOG.md` and review the **INBOX** and **THIS_WEEK** sections.
2. If there is no READY work for `{agent_id}`, add or upgrade at least one concrete task
   that fits your current mission.
3. Run the MASTER_TASK_LOG → Cycle Planner bridge for this agent, for example:

   - `python tools/master_task_log_to_cycle_planner.py --agent {agent_id} --section THIS_WEEK --priority high`

4. After the bridge runs, claim the next task and start execution:

   - `python -m src.services.messaging_cli --agent {agent_id} --get-next-task`

**Action Required**: Refill your task list from `MASTER_TASK_LOG.md`, then execute ONE concrete task slice and produce a real artifact (code, tests, or report).
"""
    
    def _build_minimal_fallback_prompt(
        self,
        agent_id: str,
        fsm_state: str,
        last_mission: str,
        next_task: Optional[Dict[str, Any]],
        stall_duration_minutes: float
    ) -> str:
        """Build minimal fallback prompt if template is unavailable."""
        return f"""🚨 STALL RECOVERY — DO NOT REPLY

Agent: {agent_id}
FSM State: {fsm_state}
Last Mission: {last_mission}
Time Since Update: {self._format_time_since_update(stall_duration_minutes)}

Resume work immediately and produce a tangible artifact (code, tests, or report).

#STALL-RECOVERY #NO-REPLY #PROGRESS-ONLY #ARTIFACT-REQUIRED
"""

    def _build_goal_aligned_actions(self, agent_id: str, agent_assignments: Dict[str, Any], base_actions: List[str]) -> List[str]:
        """Build goal-aligned recovery actions based on agent assignments and project priorities."""
        actions = []

        # Add goal-aligned actions first
        if agent_assignments.get("tasks"):
            # Priority 1: Violation consolidation tasks
            violation_tasks = [t for t in agent_assignments["tasks"] if "violation" in t.lower() or "consolidation" in t.lower(
            ) and "AgentStatus" in t or "Task class" in t or "Gaming" in t or "Config" in t or "SearchResult" in t or "Discord test" in t]
            if violation_tasks:
                actions.append(
                    f"Resume violation consolidation: {violation_tasks[0][:100]}...")

            # Priority 2: SSOT remediation
            ssot_domain = self.AGENT_SSOT_DOMAINS.get(agent_id, "")
            if ssot_domain and ssot_domain != "Strategic Coordination":
                actions.append(f"Continue SSOT remediation in {ssot_domain}")

            # Priority 3: Phase 2 consolidation
            consolidation_tasks = [t for t in agent_assignments["tasks"] if "Phase 2" in t or (
                "consolidation" in t.lower() and "tools" in t.lower())]
            if consolidation_tasks:
                actions.append(
                    f"Execute Phase 2 consolidation: {consolidation_tasks[0][:100]}...")

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
    scheduler=None,
    scheduled_tasks_section: str = ""
) -> str:
    """
    Convenience function to generate optimized resume prompt.

    Args:
        agent_id: Agent identifier
        fsm_state: Current FSM state
        last_mission: Last known mission
        stall_duration_minutes: Stall duration in minutes
        scheduler: Optional TaskScheduler instance for scheduled tasks
        scheduled_tasks_section: Optional formatted scheduled tasks section to insert

    Returns:
        Optimized resume prompt
    """
    generator = OptimizedStallResumePrompt(scheduler=scheduler)
    prompt = generator.generate_resume_prompt(
        agent_id=agent_id,
        fsm_state=fsm_state,
        last_mission=last_mission,
        stall_duration_minutes=stall_duration_minutes
    )
    
    # If scheduled tasks provided, insert them into the prompt
    if scheduled_tasks_section and prompt:
        # Insert before "SWARM SYNC CHECKLIST" section
        checklist_start = prompt.find("**SWARM SYNC CHECKLIST (DO THESE NOW):**")
        if checklist_start > 0:
            prompt = prompt[:checklist_start] + "\n" + scheduled_tasks_section + "\n" + prompt[checklist_start:]
    
    return prompt
