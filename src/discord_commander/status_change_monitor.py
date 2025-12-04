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

Author: Agent-4 (Captain)
Created: 2025-11-29
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from datetime import datetime

try:
    import discord
    from discord.ext import tasks
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    tasks = None

logger = logging.getLogger(__name__)


class StatusChangeMonitor:
    """Monitor status.json files and post Discord updates on changes."""

    def __init__(self, bot, channel_id: Optional[int] = None):
        """
        Initialize status change monitor.

        Args:
            bot: Discord bot instance
            channel_id: Optional Discord channel ID for status updates
        """
        self.bot = bot
        self.channel_id = channel_id
        self.workspace_path = Path("agent_workspaces")
        self.last_modified: Dict[str, float] = {}  # agent_id -> mtime
        self.last_status: Dict[str, dict] = {}  # agent_id -> status data
        self.check_interval = 15  # Check every 15 seconds

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
                from tools.agent_activity_detector import AgentActivityDetector
                activity_detector = AgentActivityDetector()
            except ImportError:
                activity_detector = None
                logger.warning(
                    "AgentActivityDetector not available - using status.json only")

            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_file = self.workspace_path / agent_id / "status.json"

                if not status_file.exists():
                    continue

                # Check file modification time
                current_mtime = status_file.stat().st_mtime
                last_mtime = self.last_modified.get(agent_id, 0)

                # If file was modified since last check
                if current_mtime > last_mtime:
                    # Read new status
                    try:
                        with open(status_file, 'r', encoding='utf-8') as f:
                            new_status = json.load(f)

                        # Compare with last known status
                        old_status = self.last_status.get(agent_id, {})

                        # Detect significant changes
                        changes = self._detect_changes(old_status, new_status)

                        if changes:
                            await self._post_status_update(agent_id, new_status, changes)

                        # Update tracking
                        self.last_modified[agent_id] = current_mtime
                        self.last_status[agent_id] = new_status.copy()

                    except Exception as e:
                        logger.error(
                            f"Error reading status for {agent_id}: {e}")

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

        except Exception as e:
            logger.error(f"Error in status monitoring: {e}")

    @monitor_status_changes.before_loop
    async def before_monitor(self):
        """Wait for bot to be ready before starting monitoring."""
        await self.bot.wait_until_ready()
        # Initialize tracking for all agents
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status_file = self.workspace_path / agent_id / "status.json"
            if status_file.exists():
                self.last_modified[agent_id] = status_file.stat().st_mtime
                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        self.last_status[agent_id] = json.load(f)
                except Exception:
                    pass

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
                logger.warning("No status update channel found")
                return

            # Create embed
            embed = self._create_status_update_embed(agent_id, status, changes)

            # Post update
            await channel.send(embed=embed)
            logger.info(f"✅ Status update posted for {agent_id}")

        except Exception as e:
            logger.error(f"Error posting status update: {e}")

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
            inactivity_threshold_minutes = 5.0  # 5 minutes of inactivity

            summary = activity_detector.detect_agent_activity(
                agent_id, lookback_minutes=60)

            # If agent is inactive for threshold duration
            if not summary.is_active or summary.inactivity_duration_minutes >= inactivity_threshold_minutes:
                # Special handling for Agent-4 (Captain): Use Captain Restart Pattern from inbox
                if agent_id == "Agent-4":
                    resumer_prompt = self._get_captain_restart_pattern(
                        inactivity_minutes=summary.inactivity_duration_minutes)
                    if not resumer_prompt:
                        # Fallback to generic prompt if pattern not found
                        resumer_prompt = await self._generate_generic_resume_prompt(
                            agent_id, summary)
                else:
                    # Regular agents: Use generic optimized prompt
                    resumer_prompt = await self._generate_generic_resume_prompt(
                        agent_id, summary)

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
        except Exception as e:
            logger.error(f"Error checking inactivity for {agent_id}: {e}")

    async def _send_resume_message_to_agent(self, agent_id: str, prompt: str, summary, skip_wrapper: bool = False):
        """Send resume message directly to agent via messaging system."""
        try:
            import subprocess
            import sys
            from pathlib import Path

            # Format resume message with context (unless skip_wrapper=True for Agent-4)
            if skip_wrapper:
                # For Agent-4, prompt already includes resume context
                resume_message = prompt
            else:
                # For other agents, wrap with standard resume message format
                resume_message = f"🚨 RESUMER PROMPT - Inactivity Detected\n\n"
                resume_message += f"{prompt}\n\n"
                resume_message += f"**Inactivity Duration**: {summary.inactivity_duration_minutes:.1f} minutes\n"
                if summary.last_activity:
                    resume_message += f"**Last Activity**: {summary.last_activity.strftime('%Y-%m-%d %H:%M:%S')}\n"
                if summary.activity_sources:
                    resume_message += f"**Activity Sources**: {', '.join(summary.activity_sources)}\n"
                resume_message += f"\n**Action Required**: Review your status, update status.json, and resume operations.\n"
                resume_message += f"\n🐝 WE. ARE. SWARM. ⚡🔥"

            # Send message via messaging CLI (proven reliable method)
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
            ]

            # Set PYTHONPATH and run command
            env = {"PYTHONPATH": str(project_root)}
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
                cwd=str(project_root)
            )

            if result.returncode == 0:
                logger.info(
                    f"✅ Resume message sent to {agent_id} via messaging CLI")
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                logger.warning(
                    f"⚠️ Failed to send resume message to {agent_id}: {error_msg}")

        except subprocess.TimeoutExpired:
            logger.error(f"❌ Timeout sending resume message to {agent_id}")
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

    async def _generate_generic_resume_prompt(self, agent_id: str, summary) -> Optional[str]:
        """Generate generic resume prompt for regular agents."""
        try:
            from src.core.optimized_stall_resume_prompt import generate_optimized_resume_prompt

            # Load status for context
            status_file = self.workspace_path / agent_id / "status.json"
            if not status_file.exists():
                return None

            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)

            fsm_state = status.get("status", "active")
            last_mission = status.get("current_mission", "Unknown")

            resumer_prompt = generate_optimized_resume_prompt(
                agent_id=agent_id,
                fsm_state=fsm_state,
                last_mission=last_mission,
                stall_duration_minutes=summary.inactivity_duration_minutes
            )

            return resumer_prompt

        except ImportError:
            logger.warning("OptimizedStallResumePrompt not available")
            return None
        except Exception as e:
            logger.error(f"Error generating resume prompt for {agent_id}: {e}")
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


def setup_status_monitor(bot, channel_id: Optional[int] = None) -> StatusChangeMonitor:
    """
    Setup and start status change monitoring.

    Args:
        bot: Discord bot instance
        channel_id: Optional channel ID for status updates

    Returns:
        StatusChangeMonitor instance
    """
    monitor = StatusChangeMonitor(bot, channel_id)
    monitor.start_monitoring()
    return monitor
