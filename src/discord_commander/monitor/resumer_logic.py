"""
Resumer Logic
=============


<!-- SSOT Domain: discord -->


Helper module for handling agent inactivity and resume logic.
Extracted from status_change_monitor.py for V2 compliance.
"""

import logging
import asyncio
import json
import subprocess
import sys
import time as _time
from datetime import datetime as _datetime
from pathlib import Path
from typing import Optional, Any

from src.core.config.timeout_constants import TimeoutConstants
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from src.core.messaging_models_core import MessageCategory, UnifiedMessage
from src.core.messaging_templates import render_message
from src.discord_commander.monitor.status_embeds import StatusEmbedFactory

logger = logging.getLogger(__name__)

class ActivitySummary:
    """Summary of agent activity."""
    def __init__(self, data):
        self.is_active = data.get("activity_count", 0) > 0
        latest = data.get("latest_activity")
        if latest:
            self.inactivity_duration_minutes = (_time.time() - latest) / 60
            self.last_activity = _datetime.fromtimestamp(latest)
        else:
            self.inactivity_duration_minutes = float('inf')
            self.last_activity = None
        self.activity_sources = data.get("activity_sources", [])

class ResumerHandler:
    """Handles agent inactivity detection and resume actions."""

    def __init__(self, bot, workspace_path: Path, scheduler=None):
        self.bot = bot
        self.workspace_path = workspace_path
        self.scheduler = scheduler
        self.resume_attempts = {}  # agent_id -> count

    async def check_inactivity(self, agent_id: str, activity_detector):
        """Check if agent is inactive and send resumer prompt if needed."""
        try:
            inactivity_threshold_minutes = 5.0  # 5 minutes of inactivity

            # EnhancedAgentActivityDetector.detect_agent_activity() returns a dict
            activity_data = activity_detector.detect_agent_activity(agent_id)
            
            summary = ActivitySummary(activity_data)

            # If agent is inactive for threshold duration
            if not summary.is_active or summary.inactivity_duration_minutes >= inactivity_threshold_minutes:
                # Check scheduler for pending tasks
                pending_tasks = []
                if self.scheduler:
                    try:
                        from src.orchestrators.overnight.scheduler_integration import SchedulerStatusMonitorIntegration
                        integration = SchedulerStatusMonitorIntegration(
                            scheduler=self.scheduler, status_monitor=None) # Pass None or mock if needed
                        pending_tasks = integration.get_pending_tasks_for_agent(agent_id)
                        
                        # Mark agent as inactive in scheduler
                        integration.mark_agent_inactive(
                            agent_id, summary.inactivity_duration_minutes)
                    except Exception as e:
                        logger.warning(f"Scheduler integration issue for {agent_id}: {e}")

                # Generate prompt
                resumer_prompt = None
                if agent_id == "Agent-4":
                    resumer_prompt = await self._get_captain_restart_pattern(
                        inactivity_minutes=summary.inactivity_duration_minutes)
                
                if not resumer_prompt:
                    # Fallback or standard agent
                    resumer_prompt = await self._generate_generic_resume_prompt(
                        agent_id, summary, pending_tasks=pending_tasks)

                if resumer_prompt:
                    # Send message
                    skip_wrapper = (agent_id == "Agent-4")
                    await self._send_resume_message_to_agent(agent_id, resumer_prompt, summary, skip_wrapper=skip_wrapper)

                    # Post to Discord
                    await self._post_resumer_prompt(agent_id, resumer_prompt, summary)
            else:
                # Agent active → reset attempts
                if agent_id in self.resume_attempts:
                    self.resume_attempts.pop(agent_id, None)
                    
        except Exception as e:
            logger.error(f"Error checking inactivity for {agent_id}: {e}")

    async def _send_resume_message_to_agent(self, agent_id: str, prompt: str, summary, skip_wrapper: bool = False):
        """Send resume message directly to agent."""
        try:
            # Attempt-based send mode
            attempt = self.resume_attempts.get(agent_id, 0) + 1
            send_mode = "enter" if attempt == 1 else "ctrl_enter"

            safe_minutes = (
                f"{summary.inactivity_duration_minutes:.1f}"
                if summary.inactivity_duration_minutes and summary.inactivity_duration_minutes != float('inf')
                else "unknown"
            )

            # Get next task assignment
            task_assignment_text = ""
            next_task_info = None
            try:

                from src.services.unified_service_managers import UnifiedContractManager
                contract_manager = UnifiedContractManager()

                task_result = contract_manager.get_next_task(agent_id)
                
                if task_result and task_result.get("status") == "assigned" and task_result.get("task"):
                    next_task_info = task_result.get("task")
                    task_assignment_text = self._format_task_assignment(next_task_info, task_result.get("source", "contract_system"), agent_id)
                elif task_result and task_result.get("status") == "no_tasks":
                    task_assignment_text = "\n📋 **NO TASKS AVAILABLE**\nCheck inbox or continue current mission."
            except Exception as e:
                logger.debug(f"Task assignment lookup failed for {agent_id}: {e}")

            # Format resume message
            if skip_wrapper:
                resume_message = prompt + (task_assignment_text if task_assignment_text else "")
            else:
                resume_message = self._format_generic_resume_message(prompt, safe_minutes, summary, task_assignment_text)

            # Attempt delivery
            success = await self._deliver_resume_message(agent_id, resume_message, send_mode, safe_minutes, next_task_info, summary)
            
            if success:
                self.resume_attempts[agent_id] = attempt
                logger.info(f"✅ Resume message sent to {agent_id} (attempt {attempt})")
            else:
                logger.error(f"❌ Resume message delivery failed for {agent_id}")

        except Exception as e:
            logger.error(f"❌ Error sending resume message to {agent_id}: {e}", exc_info=True)

    def _format_task_assignment(self, task_info, source, agent_id):
        """Format task assignment text."""
        title = task_info.get("title", "Unknown Task")
        desc = task_info.get("description", "")
        text = f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        text += f"📋 **TASK ASSIGNED FROM {source.upper().replace('_', ' ')}**\n"
        text += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        text += f"**Task**: {title}\n"
        if desc:
            text += f"**Description**: {desc[:200]}{'...' if len(desc) > 200 else ''}\n"
        text += f"\n**Action**: Begin work on this assigned task immediately.\n"
        text += f"**Claim Command**: `python -m src.services.messaging_cli --get-next-task --agent {agent_id}`\n"
        return text

    def _format_generic_resume_message(self, prompt, minutes, summary, task_text):
        """Format generic resume message wrapper."""
        msg = "🚨 RESUMER PROMPT - Inactivity Detected\n\n"
        msg += "[NO-ACKNOWLEDGMENTS] This is a silent work order. Do not reply with acks; produce an artifact.\n\n"
        msg += f"{prompt}\n\n"
        msg += f"**Inactivity Duration**: {minutes} minutes\n"
        if summary.last_activity:
            msg += f"**Last Activity**: {summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if summary.activity_sources:
            msg += f"**Activity Sources**: {', '.join(summary.activity_sources)}\n"
        if task_text:
            msg += task_text
        msg += "\n**Action Required**: Resume by producing a real artifact. Do not reply with acknowledgments.\n"
        msg += "\n🐝 WE. ARE. SWARM. ⚡🔥"
        return msg

    async def _deliver_resume_message(self, agent_id, message_content, send_mode, safe_minutes, next_task_info, summary):
        """Deliver message using PyAutoGUI with fallback."""
        try:
            from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
            
            # Prepare render context
            fsm_state = "UNKNOWN"
            current_mission = "Not specified"
            try:
                status_file = self.workspace_path / agent_id / "status.json"
                if status_file.exists():
                    with open(status_file, "r", encoding="utf-8") as f:
                        status = json.load(f)
                    fsm_state = status.get("fsm_state") or status.get("status") or fsm_state
                    current_mission = status.get("current_mission", current_mission)
            except Exception:
                pass

            # Render template
            try:
                msg_obj = UnifiedMessage(
                    content=message_content,
                    sender="SYSTEM",
                    recipient=agent_id,
                    message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                    priority=UnifiedMessagePriority.URGENT,
                    tags=[],
                    category=MessageCategory.S2A
                )
                
                next_task = next_task_info.get("title", "No task assigned") if next_task_info else "No task assigned"
                
                rendered = render_message(
                    msg_obj,
                    template_key="SWARM_PULSE",
                    context=f"Inactivity Detected: {safe_minutes} minutes",
                    actions="Resume by producing an artifact.",
                    fallback="Escalate if blocked.",
                    fsm_state=fsm_state,
                    current_mission=current_mission,
                    time_since_update=f"{safe_minutes} minutes",
                    next_task=next_task,
                    task_priority=str(next_task_info.get("priority", "normal")) if next_task_info else "normal",
                    task_points=str(next_task_info.get("points", "0")) if next_task_info else "0",
                    task_status="assigned" if next_task_info else "unassigned"
                )
            except Exception:
                rendered = message_content

            # Send via PyAutoGUI
            delivery = PyAutoGUIMessagingDelivery()
            message = UnifiedMessage(
                content=rendered,
                sender="SYSTEM",
                recipient=agent_id,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT,
                tags=[UnifiedMessageTag.SYSTEM],
                metadata={
                    "stalled": send_mode == "ctrl_enter",
                    "use_pyautogui": True,
                    "send_mode": send_mode,
                    "message_category": MessageCategory.S2A.value,
                },
                category=MessageCategory.S2A,
            )
            
            return await asyncio.to_thread(delivery.send_message, message)

        except Exception as e:
            logger.error(f"PyAutoGUI delivery failed: {e}")
            # Fallback to CLI
            return await self._run_cli_fallback(agent_id, message_content)

    async def _run_cli_fallback(self, agent_id, message):
        """Run CLI fallback."""
        project_root = self.workspace_path.parent
        cmd = [
            sys.executable, "-m", "src.services.messaging_cli",
            "--agent", agent_id,
            "--message", message,
            "--priority", "urgent",
            "--pyautogui",
            "--category", "s2a"
        ]
        env = {"PYTHONPATH": str(project_root)}
        
        result = await asyncio.to_thread(
            subprocess.run, cmd, capture_output=True, text=True, 
            timeout=TimeoutConstants.HTTP_DEFAULT, env=env, cwd=str(project_root)
        )
        return result.returncode == 0

    async def _get_captain_restart_pattern(self, inactivity_minutes: float = 0.0) -> Optional[str]:
        """Get Captain Restart Pattern."""
        try:
            inbox_dir = self.workspace_path / "Agent-4" / "inbox"
            if not await asyncio.to_thread(inbox_dir.exists):
                return None
                
            def _find_pattern():
                files = list(inbox_dir.glob("CAPTAIN_RESTART_PATTERN*.md"))
                if not files: return None
                return max(files, key=lambda p: p.stat().st_mtime)
            
            pattern_file = await asyncio.to_thread(_find_pattern)
            if not pattern_file:
                return None
                
            content = await asyncio.to_thread(pattern_file.read_text, encoding='utf-8')
            
            # Prepend header
            header = f"🚨 RESUMER PROMPT - Captain Inactivity Detected\n**Inactivity**: {inactivity_minutes:.1f} min\n---\n"
            return header + content
            
        except Exception as e:
            logger.warning(f"Failed to get Captain pattern: {e}")
            return None

    async def _generate_generic_resume_prompt(self, agent_id: str, summary, pending_tasks: list = None) -> Optional[str]:
        """Generate generic resume prompt."""
        try:
            from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt
            
            status_file = self.workspace_path / agent_id / "status.json"
            if not await asyncio.to_thread(status_file.exists):
                return None
                
            status = await asyncio.to_thread(lambda: json.loads(status_file.read_text(encoding='utf-8')))
            
            scheduled_section = ""
            if pending_tasks:
                # (Simplified) Just note tasks exist
                scheduled_section = f"You have {len(pending_tasks)} pending tasks."

            return generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=status.get("status", "active"),
                last_mission=status.get("current_mission", "Unknown"),
                stall_duration_minutes=summary.inactivity_duration_minutes,
                scheduler=self.scheduler,
                scheduled_tasks_section=scheduled_section
            )
        except Exception as e:
            logger.error(f"Error generating resume prompt: {e}")
            return "Resume operations immediately."

    async def _post_resumer_prompt(self, agent_id: str, prompt: str, summary):
        """Post prompt to Discord."""
        try:
            # Find channel
            channel = None
            for guild in self.bot.guilds:
                for ch in guild.channels:
                    if ch.name in ["agent-status", "captain-updates", "swarm-status"] and isinstance(ch, discord.TextChannel):
                        channel = ch
                        break
                if channel: break
            
            if channel:
                embed = StatusEmbedFactory.create_resumer_embed(agent_id, prompt, summary)
                await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Error posting resumer prompt to Discord: {e}")
