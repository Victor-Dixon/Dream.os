#!/usr/bin/env python3
"""
Status Change Monitor - Automatic Discord Updates
=================================================

Monitors agent status.json files for changes and automatically posts updates to Discord.

Features:
- File modification time tracking
- Automatic Discord notifications on status change
- Integration with AgentLifecycle
- Background task for continuous monitoring

Improvements (2025-12-27 by Agent-1):
- Enhanced error handling with specific exception types (ImportError, AttributeError, PermissionError, JSONDecodeError)
- Detailed debug logging at all critical points
- SSOT import error detection and logging
- Better exception messages with type information
- Non-blocking error recovery for task assignment failures
- Detailed PyAutoGUI delivery logging for debugging

Author: Agent-4 (Captain)
Created: 2025-11-29
Updated: 2025-12-27 (Agent-1 - Error Handling & Debugging Enhancement)
"""

from src.core.config.timeout_constants import TimeoutConstants
import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime

try:
    import discord
    from discord.ext import tasks
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

# Add project root to path
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))


if not DISCORD_AVAILABLE:
    discord = None
    tasks = None

logger = logging.getLogger(__name__)


class StatusChangeMonitor:
    """Monitor status.json files and post Discord updates on changes."""

    def __init__(self, bot, channel_id: Optional[int] = None, scheduler=None):
        """
        Initialize status change monitor.

        Args:
            bot: Discord bot instance
            channel_id: Optional Discord channel ID for status updates
            scheduler: Optional TaskScheduler instance for integration
        """
        self.bot = bot
        self.channel_id = channel_id
        self.scheduler = scheduler
        self.workspace_path = Path("agent_workspaces")
        self.last_modified: Dict[str, float] = {}  # agent_id -> mtime
        self.last_status: Dict[str, dict] = {}  # agent_id -> status data
        self.check_interval = 15  # Check every 15 seconds
        # agent_id -> pending tasks
        self.pending_tasks: Dict[str, List[dict]] = {}
        # agent_id -> resume attempts (for send mode escalation)
        self.resume_attempts: Dict[str, int] = {}

    def start_monitoring(self):
        """Start the background monitoring task."""
        if DISCORD_AVAILABLE and self.bot:
            try:
                if not self.monitor_status_changes.is_running():
                    self.monitor_status_changes.start()
                    logger.info("✅ Status change monitor started")
                else:
                    logger.info("ℹ️ Status change monitor already running")
            except Exception as e:
                logger.error(
                    f"❌ Failed to start status monitor: {e}", exc_info=True)
        else:
            logger.warning(
                "⚠️ Discord not available, status monitoring disabled")

    def stop_monitoring(self):
        """Stop the background monitoring task."""
        if hasattr(self, 'monitor_status_changes'):
            self.monitor_status_changes.cancel()
            logger.info("🛑 Status change monitor stopped")

    @tasks.loop(seconds=15)
    async def monitor_status_changes(self):
        """Background task to monitor status.json files for changes."""
        try:
            # Import activity detector for inactivity detection
            try:
                # FIX: Use correct import path for activity detector
                from src.orchestrators.overnight.enhanced_agent_activity_detector import EnhancedAgentActivityDetector
                activity_detector = EnhancedAgentActivityDetector()
                logger.debug("✅ EnhancedAgentActivityDetector imported successfully")
            except ImportError as ie:
                activity_detector = None
                logger.warning(
                    f"⚠️ AgentActivityDetector not available - using status.json only. ImportError: {ie}", exc_info=True)
            except Exception as e:
                activity_detector = None
                logger.error(
                    f"❌ Unexpected error loading AgentActivityDetector: {e}", exc_info=True)

            changes_detected = 0
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_file = self.workspace_path / agent_id / "status.json"

                if not status_file.exists():
                    continue

                # Check file modification time (non-blocking)
                try:
                    # Use asyncio.to_thread to avoid blocking event loop
                    def get_file_mtime():
                        return status_file.stat().st_mtime
                    current_mtime = await asyncio.to_thread(get_file_mtime)
                    last_mtime = self.last_modified.get(agent_id, 0)

                    # If file was modified since last check
                    if current_mtime > last_mtime:
                        # Read new status (non-blocking)
                        try:
                            def read_status_file():
                                with open(status_file, 'r', encoding='utf-8') as f:
                                    return json.load(f)
                            new_status = await asyncio.to_thread(read_status_file)

                            # Compare with last known status
                            old_status = self.last_status.get(agent_id, {})

                            # Detect significant changes
                            changes = self._detect_changes(
                                old_status, new_status)

                            if changes:
                                logger.info(
                                    f"📊 Status change detected for {agent_id}: {list(changes.keys())}")
                                await self._post_status_update(agent_id, new_status, changes)
                                changes_detected += 1
                            else:
                                logger.debug(
                                    f"No significant changes for {agent_id} (file modified but no status changes)")

                            # Update tracking
                            self.last_modified[agent_id] = current_mtime
                            self.last_status[agent_id] = new_status.copy()

                        except json.JSONDecodeError as e:
                            logger.error(
                                f"❌ Invalid JSON in {agent_id} status.json at {status_file}: {e}", exc_info=True)
                            logger.debug(f"🔍 JSON decode error details - File: {status_file}, Error: {str(e)}")
                        except PermissionError as e:
                            logger.error(
                                f"❌ Permission denied reading {agent_id} status.json: {e}")
                        except Exception as e:
                            logger.error(
                                f"❌ Error reading status for {agent_id}: {type(e).__name__}: {e}", exc_info=True)
                            logger.debug(f"🔍 Status file path: {status_file}, exists: {status_file.exists()}")

                    # Check for inactivity (every 5 minutes = 20 iterations)
                    if activity_detector:
                        if not hasattr(self, '_inactivity_check_counter'):
                            self._inactivity_check_counter = {}
                        if agent_id not in self._inactivity_check_counter:
                            self._inactivity_check_counter[agent_id] = 0

                        self._inactivity_check_counter[agent_id] += 1
                        # 5 minutes (20 * 15s)
                        if self._inactivity_check_counter[agent_id] >= 20:
                            self._inactivity_check_counter[agent_id] = 0
                            await self._check_inactivity(agent_id, activity_detector)
                except FileNotFoundError:
                    logger.debug(
                        f"Status file not found for {agent_id} (may have been deleted)")
                except Exception as e:
                    logger.error(
                        f"❌ Error checking status for {agent_id}: {e}", exc_info=True)

            if changes_detected > 0:
                logger.info(
                    f"✅ Status monitoring cycle complete: {changes_detected} updates posted")

        except Exception as e:
            logger.error(
                f"❌ Error in status monitoring loop: {e}", exc_info=True)

    @monitor_status_changes.before_loop
    async def before_monitor(self):
        """Wait for bot to be ready before starting monitoring."""
        logger.info("🔍 Waiting for bot to be ready before starting status monitoring...")
        await self.bot.wait_until_ready()
        logger.info("✅ Bot ready, initializing status tracking for all agents...")
        
        # Initialize tracking for all agents
        initialized_count = 0
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status_file = self.workspace_path / agent_id / "status.json"
            
            # Use asyncio.to_thread for file operations to avoid blocking
            try:
                exists = await asyncio.to_thread(status_file.exists)
                if exists:
                    # Get file modification time
                    def get_file_mtime():
                        return status_file.stat().st_mtime
                    self.last_modified[agent_id] = await asyncio.to_thread(get_file_mtime)
                    logger.debug(f"✅ Initialized mtime tracking for {agent_id}")
                    
                    # Read status file
                    def read_status_file():
                        with open(status_file, 'r', encoding='utf-8') as f:
                            return json.load(f)
                    self.last_status[agent_id] = await asyncio.to_thread(read_status_file)
                    logger.debug(f"✅ Loaded initial status for {agent_id}")
                    initialized_count += 1
                else:
                    logger.debug(f"⚠️ Status file not found for {agent_id} at {status_file}")
            except json.JSONDecodeError as je:
                logger.error(f"❌ JSON decode error initializing {agent_id}: {je}")
            except Exception as e:
                logger.error(f"❌ Error initializing {agent_id}: {type(e).__name__}: {e}")
        
        logger.info(f"✅ Status monitoring initialized: {initialized_count}/8 agents tracked")

    def _detect_changes(self, old_status: dict, new_status: dict) -> Dict[str, any]:
        """Detect significant status changes."""
        changes = {}

        # Status change
        old_status_val = old_status.get("status", "")
        new_status_val = new_status.get("status", "")
        if old_status_val != new_status_val:
            changes["status"] = {"old": old_status_val, "new": new_status_val}

        # Phase change
        old_phase = old_status.get("current_phase", "")
        new_phase = new_status.get("current_phase", "")
        if old_phase != new_phase:
            changes["phase"] = {"old": old_phase, "new": new_phase}

        # Mission change
        old_mission = old_status.get("current_mission", "")
        new_mission = new_status.get("current_mission", "")
        if old_mission != new_mission:
            changes["mission"] = {"old": old_mission, "new": new_mission}

        # Task completion (new completed tasks)
        old_completed = set(old_status.get("completed_tasks", []))
        new_completed = set(new_status.get("completed_tasks", []))
        newly_completed = new_completed - old_completed
        if newly_completed:
            changes["completed_tasks"] = list(newly_completed)

        # New tasks added
        old_tasks = set(old_status.get("current_tasks", []))
        new_tasks = set(new_status.get("current_tasks", []))
        new_tasks_added = new_tasks - old_tasks
        if new_tasks_added:
            changes["new_tasks"] = list(new_tasks_added)

        # Points earned
        old_points = old_status.get("points_earned", 0)
        new_points = new_status.get("points_earned", 0)
        if new_points > old_points:
            changes["points_earned"] = new_points - old_points

        return changes

    async def _post_status_update(self, agent_id: str, status: dict, changes: dict):
        """Post status update to Discord."""
        try:
            # Find status update channel
            channel = None
            if self.channel_id:
                channel = self.bot.get_channel(self.channel_id)
                if channel:
                    logger.debug(
                        f"Using configured channel: {channel.name} ({channel.id})")

            if not channel:
                # Try to find #agent-status or #captain-updates channel
                preferred_channels = [
                    "agent-status", "captain-updates", "swarm-status", "agent-4-devlogs"]
                for guild in self.bot.guilds:
                    for ch in guild.channels:
                        if isinstance(ch, discord.TextChannel):
                            if ch.name in preferred_channels:
                                channel = ch
                                logger.debug(
                                    f"Found preferred channel: {ch.name} ({ch.id})")
                                break
                    if channel:
                        break

            # Fallback: Use first available text channel if preferred not found
            if not channel:
                for guild in self.bot.guilds:
                    for ch in guild.channels:
                        if isinstance(ch, discord.TextChannel):
                            # Skip bot channels and system channels
                            if not ch.name.startswith("system-") and "bot" not in ch.name.lower():
                                channel = ch
                                logger.warning(
                                    f"Using fallback channel: {ch.name} ({ch.id})")
                                break
                    if channel:
                        break

            if not channel:
                logger.error(
                    "❌ No status update channel found - cannot post status update")
                logger.error(
                    f"Available channels: {[ch.name for guild in self.bot.guilds for ch in guild.channels if isinstance(ch, discord.TextChannel)]}")
                return

            # Create embed
            embed = self._create_status_update_embed(agent_id, status, changes)

            # Post update
            await channel.send(embed=embed)
            logger.info(
                f"✅ Status update posted for {agent_id} to #{channel.name}")

        except discord.errors.Forbidden as e:
            logger.error(f"❌ Permission denied posting to channel: {e}")
        except discord.errors.HTTPException as e:
            logger.error(f"❌ HTTP error posting status update: {e}")
        except Exception as e:
            logger.error(f"❌ Error posting status update: {e}", exc_info=True)

    def _create_status_update_embed(self, agent_id: str, status: dict, changes: dict) -> discord.Embed:
        """Create Discord embed for status update."""
        # Status emoji
        status_val = status.get("status", "UNKNOWN")
        if "ACTIVE" in status_val.upper():
            emoji = "🟢"
            color = 0x27AE60
        elif "COMPLETE" in status_val.upper():
            emoji = "✅"
            color = 0x3498DB
        elif "BLOCKED" in status_val.upper():
            emoji = "🔴"
            color = 0xE74C3C
        else:
            emoji = "🟡"
            color = 0xF39C12

        embed = discord.Embed(
            title=f"{emoji} {agent_id} Status Update",
            description=f"**{status.get('agent_name', 'Agent')}** status changed",
            color=color,
            timestamp=datetime.utcnow()
        )

        # Add change details
        if "status" in changes:
            embed.add_field(
                name="Status Change",
                value=f"`{changes['status']['old']}` → `{changes['status']['new']}`",
                inline=False
            )

        if "phase" in changes:
            embed.add_field(
                name="Phase Change",
                value=f"`{changes['phase']['old'][:50]}` → `{changes['phase']['new'][:50]}`",
                inline=False
            )

        if "mission" in changes:
            embed.add_field(
                name="Mission Change",
                value=f"`{changes['mission']['old'][:50]}` → `{changes['mission']['new'][:50]}`",
                inline=False
            )

        if "completed_tasks" in changes:
            tasks_list = "\n".join(
                [f"✅ {task[:80]}" for task in changes["completed_tasks"][:5]])
            if len(changes["completed_tasks"]) > 5:
                tasks_list += f"\n... and {len(changes['completed_tasks']) - 5} more"
            embed.add_field(
                name="Tasks Completed",
                value=tasks_list or "None",
                inline=False
            )

        if "points_earned" in changes:
            embed.add_field(
                name="Points Earned",
                value=f"+{changes['points_earned']} points",
                inline=True
            )

        # Current status summary
        current_phase = status.get("current_phase", "N/A")
        current_mission = status.get("current_mission", "No mission")
        embed.add_field(
            name="Current Status",
            value=f"**Phase:** {current_phase[:100]}\n**Mission:** {current_mission[:100]}",
            inline=False
        )

        embed.set_footer(
            text=f"Last updated: {status.get('last_updated', 'Unknown')}")

        return embed

    async def _check_inactivity(self, agent_id: str, activity_detector):
        """Check if agent is inactive and send resumer prompt if needed."""
        try:
            import time as _time
            from datetime import datetime as _datetime
            
            inactivity_threshold_minutes = 5.0  # 5 minutes of inactivity

            # EnhancedAgentActivityDetector.detect_agent_activity() returns a dict
            activity_data = activity_detector.detect_agent_activity(agent_id)
            
            # FIX: Convert dict response to an object-like summary for compatibility
            class ActivitySummary:
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
            
            summary = ActivitySummary(activity_data)

            # If agent is inactive for threshold duration
            if not summary.is_active or summary.inactivity_duration_minutes >= inactivity_threshold_minutes:
                # NEW: Check scheduler for pending tasks
                pending_tasks = []
                if self.scheduler:
                    try:
                        logger.debug(f"🔍 Attempting scheduler integration for {agent_id}")
                        from src.orchestrators.overnight.scheduler_integration import SchedulerStatusMonitorIntegration
                        integration = SchedulerStatusMonitorIntegration(
                            scheduler=self.scheduler, status_monitor=self)
                        pending_tasks = integration.get_pending_tasks_for_agent(
                            agent_id)
                        logger.debug(f"✅ Found {len(pending_tasks)} pending tasks for {agent_id}")

                        # Mark agent as inactive in scheduler
                        integration.mark_agent_inactive(
                            agent_id, summary.inactivity_duration_minutes)
                        logger.debug(f"✅ Marked {agent_id} as inactive in scheduler")
                    except ImportError as ie:
                        logger.warning(
                            f"⚠️ Scheduler integration not available for {agent_id}: {ie}", exc_info=True)
                    except AttributeError as ae:
                        logger.error(
                            f"❌ Scheduler attribute error for {agent_id}: {ae}. Scheduler object: {type(self.scheduler)}", exc_info=True)
                    except Exception as e:
                        logger.error(
                            f"❌ Failed to query scheduler for {agent_id}: {type(e).__name__}: {e}", exc_info=True)

                # Special handling for Agent-4 (Captain): Use Captain Restart Pattern from inbox
                if agent_id == "Agent-4":
                    resumer_prompt = self._get_captain_restart_pattern(
                        inactivity_minutes=summary.inactivity_duration_minutes)
                    if not resumer_prompt:
                        # Fallback to generic prompt if pattern not found
                        resumer_prompt = await self._generate_generic_resume_prompt(
                            agent_id, summary, pending_tasks=pending_tasks)
                else:
                    # Regular agents: Use generic optimized prompt
                    resumer_prompt = await self._generate_generic_resume_prompt(
                        agent_id, summary, pending_tasks=pending_tasks)

                if resumer_prompt:
                    # SEND resume message directly to agent via messaging system
                    # For Agent-4, pattern already includes resume context, so send as-is
                    # For other agents, wrap with standard resume message format
                    if agent_id == "Agent-4":
                        await self._send_resume_message_to_agent(agent_id, resumer_prompt, summary, skip_wrapper=True)
                    else:
                        await self._send_resume_message_to_agent(agent_id, resumer_prompt, summary)

                    # Also post resumer prompt to Discord for visibility
                    await self._post_resumer_prompt(agent_id, resumer_prompt, summary)
            else:
                # Agent active → reset attempts for clean next cycle
                if agent_id in self.resume_attempts:
                    self.resume_attempts.pop(agent_id, None)
        except Exception as e:
            logger.error(f"Error checking inactivity for {agent_id}: {e}")

    async def _send_resume_message_to_agent(self, agent_id: str, prompt: str, summary, skip_wrapper: bool = False):
        """Send resume message directly to agent via messaging system using PyAutoGUI to chat input coordinates.
        
        Now includes cycle planner task assignment integration - automatically fetches and assigns next available task.
        """
        try:
            # Attempt-based send mode (enter on first, ctrl+enter on escalations)
            attempt = self.resume_attempts.get(agent_id, 0) + 1
            send_mode = "enter" if attempt == 1 else "ctrl_enter"

            # Calculate safe_minutes for use in template rendering (needed for both paths)
            safe_minutes = (
                f"{summary.inactivity_duration_minutes:.1f}"
                if summary.inactivity_duration_minutes and summary.inactivity_duration_minutes != float('inf')
                else "unknown"
            )

            # CRITICAL: Get next task from cycle planner/contract system
            next_task_info = None
            task_assignment_text = ""
            try:
                logger.debug(f"🔍 Attempting to get task assignment for {agent_id}")
                from src.services.contract_system.manager import ContractManager
                logger.debug(f"✅ ContractManager imported successfully")
                contract_manager = ContractManager()
                logger.debug(f"✅ ContractManager initialized")
                task_result = contract_manager.get_next_task(agent_id)
                logger.debug(f"✅ get_next_task returned: {task_result}")
                
                if task_result and task_result.get("status") == "assigned" and task_result.get("task"):
                    next_task_info = task_result.get("task")
                    task_title = next_task_info.get("title", "Unknown Task")
                    task_description = next_task_info.get("description", "")
                    task_source = task_result.get("source", "contract_system")
                    
                    task_assignment_text = f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    task_assignment_text += f"📋 **TASK ASSIGNED FROM {task_source.upper().replace('_', ' ')}**\n"
                    task_assignment_text += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    task_assignment_text += f"**Task**: {task_title}\n"
                    if task_description:
                        task_assignment_text += f"**Description**: {task_description[:200]}{'...' if len(task_description) > 200 else ''}\n"
                    task_assignment_text += f"\n**Action**: Begin work on this assigned task immediately.\n"
                    task_assignment_text += f"**Claim Command**: `python -m src.services.messaging_cli --get-next-task --agent {agent_id}`\n"
                    task_assignment_text += f"\n"
                    
                    logger.info(f"✅ Retrieved task assignment for {agent_id}: {task_title} (source: {task_source})")
                elif task_result and task_result.get("status") == "no_tasks":
                    task_assignment_text = f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    task_assignment_text += f"📋 **NO TASKS AVAILABLE**\n"
                    task_assignment_text += f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    task_assignment_text += f"No tasks available in cycle planner or contract system.\n"
                    task_assignment_text += f"Check inbox for new assignments or continue with current mission.\n\n"
                    logger.info(f"⚠️ No tasks available for {agent_id} from cycle planner/contract system")
                else:
                    logger.warning(f"⚠️ Unexpected task_result format for {agent_id}: {task_result}")
            except ImportError as ie:
                logger.error(f"❌ Failed to import ContractManager for {agent_id}: {ie}", exc_info=True)
                # Continue without task assignment - non-blocking
            except AttributeError as ae:
                logger.error(f"❌ ContractManager attribute error for {agent_id}: {ae}", exc_info=True)
            except Exception as e:
                logger.error(f"❌ Failed to get task assignment for {agent_id}: {type(e).__name__}: {e}", exc_info=True)
                # Continue without task assignment - non-blocking

            # Format resume message with context (unless skip_wrapper=True for Agent-4)
            if skip_wrapper:
                # For Agent-4, prompt already includes resume context
                resume_message = prompt
                if task_assignment_text:
                    resume_message += task_assignment_text
            else:
                # For other agents, wrap with standard resume message format (no-ack, artifact-only)
                resume_message = "🚨 RESUMER PROMPT - Inactivity Detected\n\n"
                resume_message += "[NO-ACKNOWLEDGMENTS] This is a silent work order. Do not reply with acks; produce an artifact.\n\n"
                resume_message += f"{prompt}\n\n"
                resume_message += f"**Inactivity Duration**: {safe_minutes} minutes\n"
                if summary.last_activity:
                    resume_message += f"**Last Activity**: {summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')}\n"
                if summary.activity_sources:
                    resume_message += f"**Activity Sources**: {', '.join(summary.activity_sources)}\n"
                
                # Add task assignment section if available
                if task_assignment_text:
                    resume_message += task_assignment_text
                
                resume_message += "\n**Action Required**: Resume by producing a real artifact (commit, file update, test run, report). Do not reply with acknowledgments.\n"
                resume_message += f"\n🐝 WE. ARE. SWARM. ⚡🔥"

            # CRITICAL: Resumer must hit chat input coordinates.
            # Do NOT rely on queue success; attempt direct PyAutoGUI send and surface failures.
            try:
                logger.debug(f"🔍 Starting PyAutoGUI messaging delivery for {agent_id}")
                from src.core.messaging_pyautogui import PyAutoGUIMessagingDelivery
                logger.debug(f"✅ PyAutoGUIMessagingDelivery imported")
                from src.core.messaging_models_core import MessageCategory, UnifiedMessage
                logger.debug(f"✅ messaging_models_core imported")
                from src.core.messaging_core import (
                    UnifiedMessagePriority,
                    UnifiedMessageTag,
                    UnifiedMessageType,
                )
                logger.debug(f"✅ messaging_core enums imported")
                from src.core.messaging_templates import render_message
                logger.debug(f"✅ messaging_templates imported")

                # Build actions text for SWARM_PULSE template
                actions_text = "Resume by producing an artifact: commit/test/report or real code/doc delta."
                if next_task_info:
                    task_title = next_task_info.get("title", "Unknown Task")
                    task_description = next_task_info.get("description", "")
                    task_source = task_result.get("source", "contract_system")
                    actions_text = f"**TASK ASSIGNED**: {task_title}\n"
                    if task_description:
                        actions_text += (
                            f"Description: {task_description[:150]}{'...' if len(task_description) > 150 else ''}\n"
                        )
                    actions_text += f"Source: {task_source}\n"
                    actions_text += "\n**Action**: Begin work on this assigned task immediately.\n"
                    actions_text += f"**Claim Command**: `python -m src.services.messaging_cli --get-next-task --agent {agent_id}`\n"
                elif task_result and task_result.get("status") == "no_tasks":
                    actions_text = (
                        "No tasks available in cycle planner. Check inbox for new assignments or continue with current mission.\n"
                        "Resume by producing an artifact: commit/test/report or real code/doc delta."
                    )

                # Required SWARM_PULSE fields (best-effort from status.json)
                fsm_state = "UNKNOWN"
                current_mission = "Not specified"
                time_since_update = f"{safe_minutes} minutes"
                try:
                    status_file = self.workspace_path / agent_id / "status.json"
                    if status_file.exists():
                        def _read_status():
                            with open(status_file, "r", encoding="utf-8") as f:
                                return json.load(f)
                        status = await asyncio.to_thread(_read_status)
                        fsm_state = status.get("fsm_state") or status.get("status") or fsm_state
                        current_mission = status.get("current_mission", current_mission)
                except Exception:
                    pass

                next_task = "No task assigned"
                task_priority = "normal"
                task_points = "0"
                task_status = "unassigned"
                if next_task_info:
                    next_task = next_task_info.get("title", next_task)
                    task_priority = str(next_task_info.get("priority", task_priority))
                    task_points = str(next_task_info.get("points", task_points))
                    task_status = str(next_task_info.get("status", "assigned"))
                elif task_result and task_result.get("status") == "no_tasks":
                    next_task = "No tasks available"
                    task_status = "no_tasks"

                # Render SWARM_PULSE; if templating fails, fall back to raw resume_message
                try:
                    msg_for_template = UnifiedMessage(
                        content=resume_message,
                        sender="SYSTEM",
                        recipient=agent_id,
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                        priority=UnifiedMessagePriority.URGENT,
                        tags=[],
                        category=MessageCategory.S2A,
                    )
                    rendered = render_message(
                        msg_for_template,
                        template_key="SWARM_PULSE",
                        context=f"Inactivity Detected: {safe_minutes} minutes",
                        actions=actions_text,
                        fallback="If blocked, escalate to Captain with concrete blocker + ETA.",
                        fsm_state=fsm_state,
                        current_mission=current_mission,
                        time_since_update=time_since_update,
                        next_task=next_task,
                        task_priority=task_priority,
                        task_points=task_points,
                        task_status=task_status,
                    )
                except Exception as template_error:
                    logger.warning(f"⚠️ SWARM_PULSE template render failed for {agent_id}: {template_error}")
                    rendered = resume_message

                logger.debug(f"🔍 Creating PyAutoGUIMessagingDelivery instance")
                delivery = PyAutoGUIMessagingDelivery()
                logger.debug(f"✅ PyAutoGUIMessagingDelivery instance created")
                
                logger.debug(f"🔍 Creating UnifiedMessage for {agent_id} (send_mode={send_mode})")
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
                logger.debug(f"✅ UnifiedMessage created for {agent_id}")
                
                logger.debug(f"🔍 Sending message to {agent_id} via PyAutoGUI coords...")
                ok = await asyncio.to_thread(
                    delivery.send_message,
                    message,
                )
                logger.debug(f"✅ PyAutoGUI send_message completed for {agent_id}, result: {ok}")

                self.resume_attempts[agent_id] = attempt
                if ok:
                    logger.info(f"✅ Resume message sent to {agent_id} via PyAutoGUI coords (attempt {attempt}, mode={send_mode})")
                else:
                    logger.error(f"❌ Resume PyAutoGUI delivery FAILED for {agent_id} (coords send returned False, attempt {attempt}, mode={send_mode})")

            except ImportError as ie:
                logger.error(f"❌ Import error during PyAutoGUI resume send for {agent_id}: {ie}", exc_info=True)
                logger.debug(f"🔍 Check SSOT domain markers and import paths")
            except AttributeError as ae:
                logger.error(f"❌ Attribute error during PyAutoGUI resume send for {agent_id}: {ae}", exc_info=True)
                logger.debug(f"🔍 Check PyAutoGUIMessagingDelivery methods and UnifiedMessage attributes")
            except Exception as direct_error:
                logger.error(f"❌ Direct PyAutoGUI resume send failed for {agent_id}: {type(direct_error).__name__}: {direct_error}", exc_info=True)
                # Best-effort CLI fallback (still PyAutoGUI-based)
                import subprocess
                import sys
                from pathlib import Path

                project_root = Path(__file__).parent.parent.parent
                cmd = [
                    sys.executable,
                    "-m",
                    "src.services.messaging_cli",
                    "--agent",
                    agent_id,
                    "--message",
                    resume_message,
                    "--priority",
                    "urgent",
                    "--pyautogui",
                    "--category",
                    "s2a",
                ]
                env = {"PYTHONPATH": str(project_root)}
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=TimeoutConstants.HTTP_DEFAULT,
                    env=env,
                    cwd=str(project_root),
                )
                if result.returncode == 0:
                    logger.info(f"✅ Resume message sent to {agent_id} via messaging CLI (PyAutoGUI)")
                else:
                    error_msg = result.stderr or result.stdout or "Unknown error"
                    logger.error(f"❌ Resume CLI PyAutoGUI delivery failed for {agent_id}: {error_msg}")

        except Exception as e:
            logger.error(
                f"❌ Error sending resume message to {agent_id}: {e}", exc_info=True)

    def _get_captain_restart_pattern(self, inactivity_minutes: float = 0.0) -> Optional[str]:
        """Get Captain Restart Pattern from Agent-4 inbox, modified for resume context."""
        try:
            inbox_dir = self.workspace_path / "Agent-4" / "inbox"
            if not inbox_dir.exists():
                return None

            # Look for Captain Restart Pattern files
            pattern_files = list(inbox_dir.glob("CAPTAIN_RESTART_PATTERN*.md"))
            if not pattern_files:
                return None

            # Get most recent pattern file
            pattern_file = max(pattern_files, key=lambda p: p.stat().st_mtime)

            # Read pattern content
            with open(pattern_file, 'r', encoding='utf-8') as f:
                pattern_content = f.read()

            # Extract the pattern message (skip headers if present)
            # Look for the actual pattern content after headers
            lines = pattern_content.split('\n')
            start_idx = 0
            for i, line in enumerate(lines):
                if line.startswith('Subject:') or (line.startswith('#') and 'RESTART' in line.upper()):
                    start_idx = i
                    break

            pattern_message = '\n'.join(lines[start_idx:])

            # Modify pattern for resume context: Add inactivity header
            resume_header = f"""🚨 RESUMER PROMPT - Captain Inactivity Detected

**Inactivity Duration**: {inactivity_minutes:.1f} minutes
**Trigger**: Status Monitor detected inactivity (5+ minute threshold)

---
"""
            modified_pattern = resume_header + pattern_message

            return modified_pattern

        except Exception as e:
            logger.warning(f"Could not load Captain Restart Pattern: {e}")
            return None

    async def _generate_generic_resume_prompt(self, agent_id: str, summary, pending_tasks: list = None) -> Optional[str]:
        """Generate generic resume prompt for regular agents."""
        try:
            logger.debug(f"🔍 Generating resume prompt for {agent_id}")
            from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt
            logger.debug(f"✅ generate_optimized_resume_prompt imported")

            # Load status for context
            status_file = self.workspace_path / agent_id / "status.json"
            if not status_file.exists():
                logger.warning(f"⚠️ Status file not found for {agent_id} at {status_file}")
                return None

            logger.debug(f"🔍 Reading status file for {agent_id}")
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            logger.debug(f"✅ Status loaded for {agent_id}")

            fsm_state = status.get("status", "active")
            last_mission = status.get("current_mission", "Unknown")
            logger.debug(f"🔍 {agent_id} fsm_state={fsm_state}, mission={last_mission}")

            # Format scheduled tasks section if available
            scheduled_tasks_section = ""
            if pending_tasks and len(pending_tasks) > 0:
                try:
                    logger.debug(f"🔍 Formatting {len(pending_tasks)} scheduled tasks for {agent_id}")
                    from src.orchestrators.overnight.scheduler_integration import SchedulerStatusMonitorIntegration
                    integration = SchedulerStatusMonitorIntegration(
                        scheduler=self.scheduler, status_monitor=self)
                    scheduled_tasks_section = integration.format_scheduled_tasks_for_prompt(
                        agent_id) or ""
                    logger.debug(f"✅ Scheduled tasks formatted for {agent_id}")
                except ImportError as ie:
                    logger.warning(
                        f"⚠️ Scheduler integration import failed for {agent_id}: {ie}", exc_info=True)
                except Exception as e:
                    logger.error(
                        f"❌ Failed to format scheduled tasks for {agent_id}: {type(e).__name__}: {e}", exc_info=True)

            # Generate comprehensive SWARM_PULSE prompt with scheduled tasks integrated
            logger.debug(f"🔍 Generating optimized resume prompt for {agent_id}")
            resumer_prompt = generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=fsm_state,
                last_mission=last_mission,
                stall_duration_minutes=summary.inactivity_duration_minutes,
                scheduler=self.scheduler,
                scheduled_tasks_section=scheduled_tasks_section
            )
            logger.debug(f"✅ Resume prompt generated for {agent_id}, length: {len(resumer_prompt) if resumer_prompt else 0}")

            return resumer_prompt

        except ImportError as ie:
            logger.error(f"❌ Import error generating resume prompt for {agent_id}: {ie}", exc_info=True)
            logger.debug("🔍 Check SSOT domain markers and import paths for optimized_stall_resume_prompt")
            return None
        except json.JSONDecodeError as je:
            logger.error(f"❌ JSON decode error in status file for {agent_id}: {je}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"❌ Error generating resume prompt for {agent_id}: {type(e).__name__}: {e}", exc_info=True)
            return None

    async def _post_resumer_prompt(self, agent_id: str, prompt: str, summary):
        """Post resumer prompt to Discord."""
        try:
            # Find status update channel
            channel = None
            if self.channel_id:
                channel = self.bot.get_channel(self.channel_id)
            else:
                # Try to find #agent-status or #captain-updates channel
                for guild in self.bot.guilds:
                    for ch in guild.channels:
                        if isinstance(ch, discord.TextChannel):
                            if ch.name in ["agent-status", "captain-updates", "swarm-status"]:
                                channel = ch
                                break
                    if channel:
                        break

            if not channel:
                logger.warning(
                    "No status update channel found for resumer prompt")
                return

            # Create embed for resumer prompt
            embed = discord.Embed(
                title=f"🚨 RESUMER PROMPT - {agent_id}",
                description=prompt[:2000],  # Discord embed limit
                color=0xE74C3C,  # Red for urgency
                timestamp=datetime.utcnow()
            )

            # Add activity summary
            if summary.last_activity:
                embed.add_field(
                    name="Last Activity",
                    value=f"{summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')} ({summary.inactivity_duration_minutes:.1f} min ago)",
                    inline=False
                )

            if summary.activity_sources:
                embed.add_field(
                    name="Activity Sources",
                    value=", ".join(summary.activity_sources),
                    inline=False
                )

            embed.set_footer(
                text="Agent Activity Detector | Multi-Source Monitoring")

            # Post to channel
            await channel.send(embed=embed)
            logger.info(f"✅ Resumer prompt posted for {agent_id}")

        except Exception as e:
            logger.error(f"Error posting resumer prompt: {e}")

    def notify_status_change(self, agent_id: str, status: dict):
        """
        Manually trigger status update notification.

        Can be called by AgentLifecycle when status is updated.

        Args:
            agent_id: Agent identifier
            status: Current status data
        """
        if not self.bot or not self.bot.is_ready():
            return

        # Create task to post update
        asyncio.create_task(self._post_status_update(
            agent_id, status, {"manual": True}))


def setup_status_monitor(bot, channel_id: Optional[int] = None, scheduler=None) -> StatusChangeMonitor:
    """
    Setup and start status change monitoring.

    Args:
        bot: Discord bot instance
        channel_id: Optional channel ID for status updates
        scheduler: Optional TaskScheduler instance for integration

    Returns:
        StatusChangeMonitor instance
    """
    monitor = StatusChangeMonitor(bot, channel_id, scheduler=scheduler)
    monitor.start_monitoring()
    return monitor
