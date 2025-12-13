#!/usr/bin/env python3
"""
Unified Discord Bot - Single Bot for Agent Messaging
====================================================

<!-- SSOT Domain: web -->

Single, unified Discord bot providing complete GUI access to agent messaging system.
Consolidates all Discord functionality into one bot instance.

Features:
- Complete agent messaging GUI
- Real-time swarm status monitoring
- Interactive views, modals, and commands
- Broadcast capabilities
- Single bot instance (no duplication)

Author: Agent-3 (Infrastructure & DevOps) - Discord Consolidation
License: MIT
"""

from src.core.config.timeout_constants import TimeoutConstants
from src.services.unified_messaging_service import UnifiedMessagingService
from src.discord_commander.discord_gui_controller import DiscordGUIController
import asyncio
import logging
import os
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

from src.infrastructure.browser.thea_browser_service import TheaBrowserService
from src.infrastructure.browser.browser_models import BrowserConfig, TheaConfig

# Add project root to path FIRST (before any src imports)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Now import src modules (after path is set)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()  # Load .env file
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("⚠️  Continuing without .env support...")

# Discord imports
try:
    import discord
    from discord.ext import commands

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    print("❌ discord.py not installed! Run: pip install discord.py")
    sys.exit(1)

# Now import src modules (after path is set)

logger = logging.getLogger(__name__)


# Confirmation Views for Shutdown/Restart Commands
class ConfirmShutdownView(discord.ui.View):
    """Confirmation view for shutdown command."""

    def __init__(self):
        super().__init__(timeout=TimeoutConstants.HTTP_DEFAULT)
        self.confirmed = False

    @discord.ui.button(label="Confirm Shutdown", emoji="✅", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm shutdown button."""
        try:
            self.confirmed = True
            await interaction.response.send_message("✅ Shutdown confirmed", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in shutdown confirm: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    @discord.ui.button(label="Cancel", emoji="❌", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel shutdown button."""
        try:
            self.confirmed = False
            await interaction.response.send_message("❌ Cancelled", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in shutdown cancel: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )


class ConfirmRestartView(discord.ui.View):
    """Confirmation view for restart command."""

    def __init__(self):
        super().__init__(timeout=TimeoutConstants.HTTP_DEFAULT)
        self.confirmed = False

    @discord.ui.button(label="Confirm Restart", emoji="🔄", style=discord.ButtonStyle.primary)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Confirm restart button."""
        try:
            self.confirmed = True
            await interaction.response.send_message("✅ Restart confirmed", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in restart confirm: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )

    @discord.ui.button(label="Cancel", emoji="❌", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Cancel restart button."""
        try:
            self.confirmed = False
            await interaction.response.send_message("❌ Cancelled", ephemeral=True)
            self.stop()
        except Exception as e:
            logger.error(f"Error in restart cancel: {e}", exc_info=True)
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    f"❌ Error: {e}", ephemeral=True
                )


class UnifiedDiscordBot(commands.Bot):
    """Single unified Discord bot for agent messaging system."""

    def __init__(self, token: str, channel_id: int | None = None):
        """Initialize unified Discord bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        intents.members = True
        intents.voice_states = True  # Required for voice channel access

        super().__init__(command_prefix="!", intents=intents, help_command=None)

        self.token = token
        self.channel_id = channel_id
        self.messaging_service = UnifiedMessagingService()
        self.gui_controller = DiscordGUIController(self.messaging_service)
        self.logger = logging.getLogger(__name__)

        # Connection health tracking
        self.last_heartbeat = time.time()
        self.connection_healthy = False

        # Discord user ID to developer name mapping
        self.discord_user_map = self._load_discord_user_map()

        # Thea browser services
        self._thea_browser_service: TheaBrowserService | None = None
        self.thea_last_refresh_path = Path("data/thea_last_refresh.json")
        try:
            self.thea_min_interval_minutes = int(
                os.getenv("THEA_MIN_INTERVAL_MINUTES", "60"))
        except ValueError:
            self.thea_min_interval_minutes = 60

    def _load_discord_user_map(self) -> dict[str, str]:
        """Load Discord user ID to developer name mapping from profiles."""
        user_map = {}
        from pathlib import Path
        import json

        # Load from agent profiles
        workspace_dir = Path("agent_workspaces")
        if workspace_dir.exists():
            for agent_dir in workspace_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    profile_file = agent_dir / "profile.json"
                    if profile_file.exists():
                        try:
                            profile_data = json.loads(
                                profile_file.read_text(encoding="utf-8"))
                            discord_user_id = profile_data.get(
                                "discord_user_id")
                            developer_name = profile_data.get(
                                "discord_username") or profile_data.get("developer_name")

                            if discord_user_id and developer_name:
                                user_map[str(discord_user_id)
                                         ] = developer_name.upper()
                                self.logger.debug(
                                    f"Loaded Discord mapping: {discord_user_id} → {developer_name}")
                        except Exception as e:
                            self.logger.warning(
                                f"Failed to load profile from {profile_file}: {e}")

        # Also check for config file
        config_file = Path("config/discord_user_map.json")
        if config_file.exists():
            try:
                config_data = json.loads(
                    config_file.read_text(encoding="utf-8"))
                # Filter out metadata keys (starting with _) and non-string values
                valid_mappings = {
                    k: v for k, v in config_data.items()
                    if not k.startswith("_") and isinstance(v, str)
                }
                user_map.update(valid_mappings)
                if valid_mappings:
                    self.logger.info(
                        f"Loaded {len(valid_mappings)} Discord user mappings from config")
            except Exception as e:
                self.logger.warning(
                    f"Failed to load Discord user map config: {e}")

        return user_map

    # ---------- Thea helpers ----------
    def _get_thea_service(self, headless: bool = True) -> TheaBrowserService:
        if self._thea_browser_service:
            return self._thea_browser_service
        browser_cfg = BrowserConfig(headless=headless)
        thea_cfg = TheaConfig()
        self._thea_browser_service = TheaBrowserService(
            config=browser_cfg, thea_config=thea_cfg)
        return self._thea_browser_service

    def _read_last_thea_refresh(self) -> float | None:
        try:
            if self.thea_last_refresh_path.exists():
                data = json.loads(
                    self.thea_last_refresh_path.read_text(encoding="utf-8"))
                return float(data.get("ts"))
        except Exception:
            return None
        return None

    def _write_last_thea_refresh(self, ts: float) -> None:
        try:
            self.thea_last_refresh_path.parent.mkdir(
                parents=True, exist_ok=True)
            self.thea_last_refresh_path.write_text(
                json.dumps({"ts": ts}, indent=2), encoding="utf-8")
        except Exception as e:
            self.logger.warning(f"Could not write Thea last refresh: {e}")

    async def ensure_thea_session(self, allow_interactive: bool, min_interval_minutes: int | None = None) -> bool:
        """Self-throttling Thea session ensure; headless by default, interactive only on demand."""
        min_interval = min_interval_minutes or self.thea_min_interval_minutes
        last = self._read_last_thea_refresh()
        now = time.time()
        if last and (now - last) < (min_interval * 60):
            self.logger.info(
                f"⏭️  Thea refresh skipped (age {(now - last)/60:.1f}m < {min_interval}m)")
            return True

        # Headless attempt
        try:
            svc = self._get_thea_service(headless=True)
            if not svc.initialize():
                self.logger.error(
                    "Thea refresh: initialize failed (uc missing or disabled)")
                return False
            ok = svc.ensure_thea_authenticated(allow_manual=False)
            svc.close()
            if ok:
                self.logger.info(
                    "✅ Thea session refreshed headlessly (cookies saved)")
                self._write_last_thea_refresh(now)
                return True
            self.logger.warning("⚠️ Thea headless refresh failed")
        except Exception as e:
            self.logger.error(f"❌ Thea headless refresh error: {e}")

        if not allow_interactive:
            return False

        # Interactive fallback
        try:
            svc = self._get_thea_service(headless=False)
            if not svc.initialize():
                self.logger.error(
                    "Thea interactive init failed (uc missing or disabled)")
                return False
            ok = svc.ensure_thea_authenticated(allow_manual=True)
            svc.close()
            if ok:
                self.logger.info(
                    "✅ Thea session refreshed interactively (cookies saved)")
                self._write_last_thea_refresh(now)
                return True
            self.logger.error("❌ Thea interactive refresh failed")
            return False
        except Exception as e:
            self.logger.error(f"❌ Thea interactive refresh error: {e}")
            return False

    def _get_developer_prefix(self, discord_user_id: str) -> str:
        """Get developer prefix from Discord user ID mapping."""
        # Check if user ID is in mapping
        developer_name = self.discord_user_map.get(str(discord_user_id))
        if developer_name:
            # Ensure it's a string before calling .upper()
            if isinstance(developer_name, str):
                # Normalize to uppercase and ensure it's a valid prefix
                valid_prefixes = ['CHRIS', 'ARIA',
                                  'VICTOR', 'CARYMN', 'CHARLES']
                developer_name_upper = developer_name.upper()
                if developer_name_upper in valid_prefixes:
                    return f"[{developer_name_upper}]"
        # Default to [D2A] if no mapping found
        return "[D2A]"

    async def on_ready(self):
        """Bot ready event."""
        # Update connection health
        self.connection_healthy = True
        self.last_heartbeat = time.time()

        # Prevent duplicate startup messages on reconnection
        if not hasattr(self, '_startup_sent'):
            self.logger.info(f"✅ Discord Commander Bot ready: {self.user}")
            self.logger.info(f"📊 Guilds: {len(self.guilds)}")

            # Initialize status change monitor (manual start via UI/command)
            try:
                from src.discord_commander.status_change_monitor import setup_status_monitor

                # NEW: Initialize scheduler for integration
                scheduler = None
                try:
                    from src.orchestrators.overnight.scheduler import TaskScheduler
                    scheduler = TaskScheduler()
                    self.logger.info("✅ Task scheduler initialized")
                except Exception as e:
                    self.logger.warning(
                        f"⚠️ Could not initialize scheduler: {e}")

                # Create status monitor with scheduler integration
                self.status_monitor = setup_status_monitor(
                    self, self.channel_id, scheduler=scheduler)

                # Wire scheduler to status monitor (bidirectional)
                if scheduler and self.status_monitor:
                    scheduler.status_monitor = self.status_monitor
                    self.logger.info(
                        "✅ Scheduler-StatusMonitor integration wired")

                # Auto-start status monitor to ensure resumer runs without manual action
                if self.status_monitor:
                    try:
                        self.status_monitor.start_monitoring()
                        self.logger.info(
                            "✅ Status change monitor started (auto)")
                    except Exception as e:
                        self.logger.warning(
                            f"⚠️ Could not auto-start status monitor: {e}")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not start status monitor: {e}")
            self.logger.info(f"🤖 Latency: {round(self.latency * 1000, 2)}ms")

            # Set bot presence
            await self.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching, name="the swarm 🐝")
            )

            # Optional: auto-refresh Thea cookies headless on startup if env set
            if os.getenv("THEA_AUTO_REFRESH", "0") == "1":
                await self.ensure_thea_session(allow_interactive=False, min_interval_minutes=self.thea_min_interval_minutes)

            # Send startup message with control panel (only once)
            await self.send_startup_message()
            self._startup_sent = True
        else:
            # Reconnection - just log, don't spam startup message
            self.logger.info(f"🔄 Discord Bot reconnected: {self.user}")

    # ---------- Thea helpers ----------
    def _get_thea_service(self, headless: bool = True) -> TheaBrowserService:
        if self._thea_browser_service:
            return self._thea_browser_service
        browser_cfg = BrowserConfig(headless=headless)
        thea_cfg = TheaConfig()
        self._thea_browser_service = TheaBrowserService(
            config=browser_cfg, thea_config=thea_cfg)
        return self._thea_browser_service

    async def _refresh_thea_session(self, headless: bool = True) -> bool:
        try:
            svc = self._get_thea_service(headless=headless)
            if not svc.initialize():
                self.logger.error(
                    "Thea refresh: initialize failed (uc missing or disabled)")
                return False
            ok = svc.ensure_thea_authenticated(allow_manual=not headless)
            svc.close()
            if ok:
                self.logger.info(
                    "✅ Thea session refresh completed (cookies saved)")
            else:
                self.logger.error("❌ Thea session refresh failed")
            return ok
        except Exception as e:
            self.logger.error(f"❌ Thea refresh error: {e}")
            return False

    async def on_message(self, message: discord.Message):
        """Handle incoming messages with developer prefix mapping."""
        # Don't process bot's own messages
        if message.author == self.user:
            return

        # Handle !music(song title) format before command processing
        content = message.content.strip()
        if content.lower().startswith('!music('):
            # Extract song title and create command-like message
            import re
            pattern = r'!music\(([^)]+)\)'
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                song_title = match.group(1).strip()
                # Modify message content to standard command format
                message.content = f"!music {song_title}"

        # Process commands first
        await self.process_commands(message)

        content = message.content.strip()

        # Supported prefixes: [D2A], [CHRIS], [ARIA], [VICTOR], [CARYMN], [CHARLES]
        # Also accept simple format: "Agent-X" (will auto-add prefix)
        supported_prefixes = ('[D2A]', '[CHRIS]', '[ARIA]',
                              '[VICTOR]', '[CARYMN]', '[CHARLES]')

        # Check if message starts with a supported prefix
        has_prefix = any(content.startswith(prefix)
                         for prefix in supported_prefixes)

        # Also check for simple "Agent-X" format (without prefix)
        simple_format = content.split('\n')[0].strip().startswith('Agent-')

        if not (has_prefix or simple_format):
            return

        try:
            # Get developer prefix from Discord user ID
            developer_prefix = self._get_developer_prefix(
                str(message.author.id))

            # Parse message format
            lines = content.split('\n', 1)

            if has_prefix:
                # Format: [PREFIX] Agent-X\n\nMessage content
                if len(lines) < 2:
                    self.logger.warning(
                        f"Invalid message format: {content[:50]}")
                    return

                header = lines[0].strip()
                message_content = lines[1].strip()

                # Parse recipient (e.g., "[D2A] Agent-1" -> "Agent-1")
                parts = header.split()
                if len(parts) < 2:
                    self.logger.warning(
                        f"Could not parse recipient from: {header}")
                    return

                recipient = parts[1]
                # Use the prefix from message, or override with developer prefix
                message_prefix = parts[0] if parts[0] in supported_prefixes else developer_prefix
            else:
                # Simple format: Agent-X\n\nMessage content
                if len(lines) < 2:
                    self.logger.warning(
                        f"Invalid message format: {content[:50]}")
                    return

                header = lines[0].strip()
                message_content = lines[1].strip()

                # Parse recipient (e.g., "Agent-1" -> "Agent-1")
                recipient = header
                message_prefix = developer_prefix  # Auto-add developer prefix

            # Validate recipient format and ensure it's a valid agent (Agent-1 through Agent-8)
            if not recipient.startswith('Agent-'):
                self.logger.warning(f"Invalid recipient format: {recipient}")
                await message.add_reaction("❌")
                return

            # Validate agent name is in allowed list (Agent-1 through Agent-8)
            from src.discord_commander.discord_agent_communication import AgentCommunicationEngine
            engine = AgentCommunicationEngine()
            if not engine.is_valid_agent(recipient):
                self.logger.warning(
                    f"Invalid agent name: {recipient} (must be Agent-1 through Agent-8)")
                await message.add_reaction("❌")
                await message.channel.send(
                    f"❌ Invalid agent name: `{recipient}`. "
                    f"Only Agent-1 through Agent-8 are allowed."
                )
                return

            # Priority is always regular for Discord messages
            priority = "regular"

            # Apply D2A template to Discord messages (wrap fully)
            from src.core.messaging_models_core import (
                UnifiedMessage,
                MessageCategory,
                UnifiedMessageType,
                UnifiedMessagePriority,
            )
            from src.core.messaging_templates import render_message
            from src.services.messaging_infrastructure import MessageCoordinator
            import uuid
            from datetime import datetime

            # Build per-agent devlog command for the recipient
            devlog_command = (
                f"python tools/devlog_poster.py --agent {recipient} --file <devlog_path>\n"
                f"# Fallback:\n"
                f"python -m tools.toolbelt --devlog-post --agent {recipient}"
            )

            # Create UnifiedMessage with D2A category
            msg = UnifiedMessage(
                content=message_content,
                sender=f"Discord User ({message.author.name})",
                recipient=recipient,
                message_type=UnifiedMessageType.HUMAN_TO_AGENT,
                priority=UnifiedMessagePriority.REGULAR,
                category=MessageCategory.D2A,
                message_id=str(uuid.uuid4()),
                timestamp=datetime.now().isoformat(),
            )

            # Render message with D2A template and explicit devlog command
            rendered_message = render_message(
                msg,
                devlog_command=devlog_command,
            )

            self.logger.info(
                f"📨 Processing {message_prefix} message: {recipient} - {message_content[:50]}...")

            # Queue message for PyAutoGUI delivery (with template applied)
            # CRITICAL: Pass message_category=D2A and use_pyautogui=True to preserve template and ensure PyAutoGUI delivery
            result = MessageCoordinator.send_to_agent(
                agent=recipient,
                message=rendered_message,
                priority=priority,
                use_pyautogui=True,  # CRITICAL: Explicitly enable PyAutoGUI delivery
                # CRITICAL: Preserve D2A category so template format is maintained
                message_category=MessageCategory.D2A,
            )

            if result.get("success"):
                queue_id = result.get("queue_id", "unknown")
                self.logger.info(
                    f"✅ Message queued: {queue_id} → {recipient} ({message_prefix})")

                # Send confirmation to Discord
                await message.add_reaction("✅")
                # Send confirmation message (brief, non-intrusive)
                await message.channel.send(
                    f"✅ Message queued for **{recipient}** (Queue ID: `{queue_id[:8]}...`)",
                    reference=message  # Reply to original message
                )
            else:
                error = result.get("error", "Unknown error")
                self.logger.error(f"❌ Failed to queue message: {error}")
                await message.add_reaction("❌")
                await message.channel.send(
                    f"❌ Failed to queue message: {error}",
                    reference=message  # Reply to original message
                )

        except Exception as e:
            self.logger.error(
                f"❌ Error processing message: {e}", exc_info=True)
            await message.add_reaction("❌")

    def _get_swarm_snapshot(self) -> dict:
        """Get current swarm work snapshot."""
        snapshot = {
            "active_agents": [],
            "recent_activity": [],
            "current_focus": [],
            "engagement_rate": 0.0,
        }

        try:
            import json
            from pathlib import Path
            from datetime import datetime, timedelta

            workspace_root = Path("agent_workspaces")
            active_count = 0
            total_agents = 8

            # Get agent statuses
            for i in range(1, 9):
                agent_id = f"Agent-{i}"
                status_file = workspace_root / agent_id / "status.json"

                if not status_file.exists():
                    continue

                try:
                    with open(status_file, 'r', encoding='utf-8') as f:
                        status = json.load(f)

                    agent_status = status.get("status", "")
                    if "ACTIVE" in agent_status.upper():
                        active_count += 1
                        mission = status.get(
                            "current_mission", "No active mission")[:80]
                        phase = status.get("current_phase", "Unknown")
                        priority = status.get("mission_priority", "MEDIUM")

                        snapshot["active_agents"].append({
                            "id": agent_id,
                            "mission": mission,
                            "phase": phase,
                            "priority": priority,
                        })

                        # Get recent completed tasks
                        completed = status.get("completed_tasks", [])
                        if completed:
                            recent = completed[0][:100] if isinstance(
                                completed[0], str) else str(completed[0])[:100]
                            snapshot["recent_activity"].append(
                                f"{agent_id}: {recent}")

                        # Get current focus
                        current_tasks = status.get("current_tasks", [])
                        if current_tasks:
                            focus = current_tasks[0][:80] if isinstance(
                                current_tasks[0], str) else str(current_tasks[0])[:80]
                            snapshot["current_focus"].append(
                                f"{agent_id}: {focus}")

                except Exception as e:
                    self.logger.debug(
                        f"Error reading status for {agent_id}: {e}")
                    continue

            snapshot["engagement_rate"] = (
                active_count / total_agents * 100) if total_agents > 0 else 0.0

        except Exception as e:
            self.logger.warning(f"Error getting swarm snapshot: {e}")

        return snapshot

    async def send_startup_message(self):
        """Send startup message to configured channel with swarm work snapshot."""
        try:
            channel = None

            if self.channel_id:
                channel = self.get_channel(self.channel_id)

            if not channel:
                # Find first available text channel
                for guild in self.guilds:
                    for text_channel in guild.text_channels:
                        channel = text_channel
                        self.logger.info(
                            f"Using channel: {channel.name} ({channel.id})")
                        break
                    if channel:
                        break

            if not channel:
                self.logger.warning(
                    "No text channels available for startup message")
                return

            # Get swarm snapshot
            snapshot = self._get_swarm_snapshot()

            # Create swarm snapshot view
            try:
                from src.discord_commander.views.swarm_snapshot_view import SwarmSnapshotView
                snapshot_view = SwarmSnapshotView(snapshot)
                snapshot_embed = snapshot_view.create_snapshot_embed()
            except Exception as e:
                self.logger.warning(f"Could not create snapshot view: {e}")
                snapshot_view = None
                snapshot_embed = None

            embed = discord.Embed(
                title="🐝 Discord Commander - SWARM CONTROL CENTER",
                description="**Complete Multi-Agent Command & Showcase System**",
                color=0x3498DB,  # Swarm Blue
                timestamp=discord.utils.utcnow(),
            )

            # Add snapshot embed as first message, or add snapshot fields to main embed
            if snapshot_embed:
                # Send snapshot view as separate message first
                await channel.send(embed=snapshot_embed, view=snapshot_view)
            else:
                # Fallback: Add snapshot fields to main embed
                if snapshot["active_agents"]:
                    active_list = []
                    for agent in snapshot["active_agents"][:5]:
                        priority_emoji = "🔴" if agent["priority"] == "HIGH" else "🟡" if agent["priority"] == "MEDIUM" else "🟢"
                        active_list.append(
                            f"{priority_emoji} **{agent['id']}** ({agent['phase']}): {agent['mission']}"
                        )
                    if len(snapshot["active_agents"]) > 5:
                        active_list.append(
                            f"... and {len(snapshot['active_agents']) - 5} more")
                    embed.add_field(
                        name=f"📊 Current Work Snapshot ({snapshot['engagement_rate']:.0f}% Engagement)",
                        value="\n".join(
                            active_list) if active_list else "No active agents",
                        inline=False,
                    )

                if snapshot["recent_activity"]:
                    activity_text = "\n".join(snapshot["recent_activity"][:3])
                    if len(snapshot["recent_activity"]) > 3:
                        activity_text += f"\n... and {len(snapshot['recent_activity']) - 3} more"
                    embed.add_field(
                        name="✅ Recent Activity",
                        value=activity_text[:1024],
                        inline=False,
                    )

                if snapshot["current_focus"]:
                    focus_text = "\n".join(snapshot["current_focus"][:3])
                    if len(snapshot["current_focus"]) > 3:
                        focus_text += f"\n... and {len(snapshot['current_focus']) - 3} more"
                    embed.add_field(
                        name="🎯 Current Focus",
                        value=focus_text[:1024],
                        inline=False,
                    )

            embed.add_field(
                name="✅ System Status",
                value="All systems operational • 3 command modules loaded • Enhanced activity monitoring active!",
                inline=False,
            )

            embed.add_field(
                name="🎛️ Interactive Control Panel (PREFERRED - NO COMMANDS NEEDED!)",
                value=(
                    "• `!control` (or `!panel`, `!menu`) - Open main control panel\n"
                    "• **ALL features accessible via buttons**\n"
                    "• **No commands needed - just click buttons!**\n"
                    "• Tasks, Status, GitHub Book, Roadmap, Excellence, Overview, Goldmines, Templates, Mermaid, Monitor, Help - ALL via buttons!"
                ),
                inline=False,
            )

            embed.add_field(
                name="📨 Messaging (GUI-Driven)",
                value=(
                    "• `!gui` - Open messaging interface\n"
                    "• Or use **Message Agent** button in control panel\n"
                    "• Entry fields for custom messages"
                ),
                inline=False,
            )

            embed.add_field(
                name="📨 Text Commands (Legacy)",
                value=(
                    "• `!message <agent> <msg>` - Direct agent message\n"
                    "• `!broadcast <msg>` - Broadcast to all agents\n"
                    "• `!bump <1-8> [1-8]...` - Bump agents (click + shift+backspace)\n"
                    "• `!agents` - List all agents"
                ),
                inline=False,
            )

            embed.add_field(
                name="🐝 Swarm Showcase (ALL ACCESSIBLE VIA BUTTONS!)",
                value=(
                    "• **Tasks** button = `!swarm_tasks` - Live task dashboard\n"
                    "• **Roadmap** button = `!swarm_roadmap` - Strategic roadmap\n"
                    "• **Excellence** button = `!swarm_excellence` - Lean Excellence campaign\n"
                    "• **Overview** button = `!swarm_overview` - Complete swarm status\n"
                    "• `!swarm_profile` - Swarm collective profile (identity, stats, achievements)"
                ),
                inline=False,
            )

            embed.add_field(
                name="📚 GitHub Book Viewer (ACCESSIBLE VIA BUTTONS!)",
                value=(
                    "• **GitHub Book** button = `!github_book [chapter]` - Interactive book navigation\n"
                    "• **Goldmines** button = `!goldmines` - High-value pattern showcase\n"
                    "• `!book_stats` - Comprehensive statistics"
                ),
                inline=False,
            )

            embed.add_field(
                name="📊 Diagram Commands",
                value=(
                    "• `!mermaid <diagram_code>` - Render Mermaid diagram\n"
                    "• Example: `!mermaid graph TD; A-->B; B-->C;`"
                ),
                inline=False,
            )

            embed.add_field(
                name="🔧 Git Commands",
                value=(
                    "• `!git_push \"message\"` - Push project to GitHub\n"
                    "• `!push \"Your commit message\"` - Alias for git_push"
                ),
                inline=False,
            )

            embed.add_field(
                name="🤖 System Info",
                value=(
                    f"**Guilds:** {len(self.guilds)} | **Latency:** {round(self.latency * 1000, 2)}ms\n"
                    f"**Modules:** Messaging, Swarm Showcase, GitHub Book\n"
                    f"**Status:** 🟢 All systems operational"
                ),
                inline=False,
            )

            embed.set_footer(
                text="🐝 WE. ARE. SWARM. ⚡ Every agent is the face of the swarm")

            # Send control panel with startup message
            control_view = self.gui_controller.create_control_panel()
            await channel.send(embed=embed, view=control_view)
            self.logger.info(
                "✅ Startup message with control panel sent successfully")

        except Exception as e:
            self.logger.error(f"Error sending startup message: {e}")

    async def setup_hook(self):
        """Setup hook for bot initialization - load all cogs."""
        try:
            # Load approval commands (NEW - for Phase 1 consolidation approval)
            try:
                from .approval_commands import ApprovalCommands
                await self.add_cog(ApprovalCommands(self))
                self.logger.info("✅ Approval commands loaded")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Could not load approval commands: {e}")

            # Add messaging commands cog
            await self.add_cog(MessagingCommands(self, self.gui_controller))
            self.logger.info("✅ Messaging commands loaded")

            # Log all registered commands for debugging
            command_names = [cmd.name for cmd in self.walk_commands()]
            self.logger.info(
                f"📋 Registered commands: {', '.join(command_names)}")

            # Add swarm showcase commands cog
            from src.discord_commander.swarm_showcase_commands import SwarmShowcaseCommands
            await self.add_cog(SwarmShowcaseCommands(self))
            self.logger.info("✅ Swarm showcase commands loaded")

            # Add GitHub book viewer cog (WOW FACTOR!)
            from src.discord_commander.github_book_viewer import GitHubBookCommands
            await self.add_cog(GitHubBookCommands(self))
            self.logger.info("✅ GitHub Book Viewer loaded - WOW FACTOR READY!")

            # Add trading commands cog (Agent-1 - Trading Reports)
            from src.discord_commander.trading_commands import TradingCommands
            await self.add_cog(TradingCommands(self))
            self.logger.info("✅ Trading commands loaded")

            # Add webhook commands cog (Agent-7 - Webhook Management)
            from src.discord_commander.webhook_commands import WebhookCommands
            await self.add_cog(WebhookCommands(self))

            # Load tools commands
            try:
                from src.discord_commander.tools_commands import ToolsCommands
                await self.add_cog(ToolsCommands(self))
                self.logger.info("✅ Tools commands loaded")
            except Exception as e:
                self.logger.warning(f"⚠️ Could not load tools commands: {e}")

            # Load file share commands
            try:
                from src.discord_commander.file_share_commands import setup as setup_file_share
                await setup_file_share(self)
                self.logger.info("✅ File share commands loaded")
            except Exception as e:
                self.logger.warning(
                    f"⚠️ Could not load file share commands: {e}")

            # Load music commands
            try:
                from src.discord_commander.music_commands import setup
                await setup(self)
            except Exception as e:
                self.logger.warning(f"⚠️ Could not load music commands: {e}")
            self.logger.info("✅ Webhook commands loaded")

            # Final command count
            all_commands = [cmd.name for cmd in self.walk_commands()]
            self.logger.info(
                f"📊 Total commands registered: {len(all_commands)}")
            self.logger.info(
                f"📋 All commands: {', '.join(sorted(all_commands))}")
        except Exception as e:
            self.logger.error(f"Error loading commands: {e}", exc_info=True)

    async def on_disconnect(self):
        """Handle bot disconnection."""
        self.connection_healthy = False
        self.logger.warning(
            "⚠️ Discord Bot disconnected - will attempt to reconnect")
        # Reset startup flag on disconnect so we can send startup message on reconnect
        if hasattr(self, '_startup_sent'):
            delattr(self, '_startup_sent')

    async def on_resume(self):
        """Handle bot reconnection after disconnect."""
        self.connection_healthy = True
        self.last_heartbeat = time.time()
        self.logger.info(
            "✅ Discord Bot reconnected successfully after disconnect")

    async def on_socket_raw_receive(self, msg):
        """Track connection health via socket activity."""
        self.last_heartbeat = time.time()
        if not self.connection_healthy:
            self.connection_healthy = True
            self.logger.debug("🔄 Connection health restored")

    async def on_error(self, event, *args, **kwargs):
        """Handle errors in event handlers."""
        self.logger.error(f"❌ Error in event {event}: {args}", exc_info=True)
        # Don't close bot on errors - let it try to recover

    async def close(self):
        """Clean shutdown."""
        self.logger.info("🛑 Unified Discord Bot shutting down...")
        # Mark as intentional shutdown to prevent reconnection loop
        self._intentional_shutdown = True
        await super().close()


class MessagingCommands(commands.Cog):
    """Commands for agent messaging."""

    def __init__(self, bot: UnifiedDiscordBot, gui_controller: DiscordGUIController):
        """Initialize messaging commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="thea", aliases=["thea-refresh"], description="Ensure Thea session (headless keepalive, interactive only if needed)")
    async def thea(self, ctx: commands.Context, force: str = ""):
        """
        Ensure Thea session with self-throttling keepalive.
        Usage: !thea [force]
        - Default: headless refresh if stale; interactive fallback if headless fails.
        - force: bypass throttle (set any value to force refresh).
        """
        allow_interactive = True
        min_interval = 0 if force else self.bot.thea_min_interval_minutes
        await ctx.send("🔄 Ensuring Thea session (headless)...")
        success = await self.bot.ensure_thea_session(allow_interactive=allow_interactive, min_interval_minutes=min_interval)
        if success:
            await ctx.send("✅ Thea session is healthy (cookies saved).")
        else:
            await ctx.send("❌ Thea session failed. Try again to trigger interactive login.")

    @commands.command(name="control", aliases=["panel", "menu"], description="Open main control panel")
    async def control_panel(self, ctx: commands.Context):
        """Open main interactive control panel."""
        try:
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="🎛️ SWARM CONTROL PANEL",
                description="**Complete Interactive Control Interface**\n\nUse buttons below to access all features:",
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="📨 Messaging",
                value="Message individual agents or broadcast to all",
                inline=True,
            )
            embed.add_field(
                name="📊 Monitoring",
                value="View swarm status and task dashboards",
                inline=True,
            )
            embed.add_field(
                name="📚 Content",
                value="Access GitHub book and documentation",
                inline=True,
            )

            embed.set_footer(
                text="🐝 WE. ARE. SWARM. ⚡ Interactive GUI-Driven Control")
            await ctx.send(embed=embed, view=control_view)

        except Exception as e:
            self.logger.error(f"Error opening control panel: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="gui", description="Open messaging GUI")
    async def gui(self, ctx: commands.Context):
        """Open interactive messaging GUI."""
        try:
            embed = discord.Embed(
                title="🤖 Agent Messaging Control Panel",
                description="Use the controls below to interact with the swarm",
                color=discord.Color.blue(),
                timestamp=discord.utils.utcnow(),
            )

            embed.add_field(
                name="📋 Instructions",
                value=(
                    "1. Select an agent from dropdown to send message\n"
                    "2. Click 'Broadcast' to message all agents\n"
                    "3. Click 'Status' to view swarm status\n"
                    "4. Click 'Refresh' to reload agent list"
                ),
                inline=False,
            )

            view = self.gui_controller.create_main_gui()
            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error opening GUI: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="status", description="View swarm status. Use '!status refresh' to force update.")
    async def status(self, ctx: commands.Context, *, args: str = ""):
        """View swarm status. Use '!status refresh' to force immediate update."""
        try:
            # Force refresh if requested
            if args.lower() == "refresh":
                from .status_reader import StatusReader
                status_reader = StatusReader()
                status_reader.clear_cache()
                await ctx.send("🔄 Status cache cleared - refreshing...", delete_after=3)

            view = self.gui_controller.create_status_gui()

            # Import status reader to create embed
            from src.discord_commander.status_reader import StatusReader

            status_reader = StatusReader()

            # Create status embed
            main_view = self.gui_controller.create_main_gui()
            embed = await main_view._create_status_embed(status_reader)

            await ctx.send(embed=embed, view=view)

        except Exception as e:
            self.logger.error(f"Error showing status: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="monitor", description="Control status change monitor. Usage: !monitor [start|stop|status] (manual start via control panel)")
    async def monitor(self, ctx: commands.Context, action: str = "status"):
        """Control status change monitor."""
        try:
            action = action.lower()

            if not hasattr(self, 'status_monitor'):
                await ctx.send("❌ Status monitor not initialized. Bot may not be fully ready.")
                return

            if action == "start":
                if hasattr(self.status_monitor, 'monitor_status_changes'):
                    if self.status_monitor.monitor_status_changes.is_running():
                        await ctx.send("✅ Status monitor is already running!")
                    else:
                        self.status_monitor.start_monitoring()
                        await ctx.send("✅ Status monitor started! Checking every 15 seconds.")
                else:
                    self.status_monitor.start_monitoring()
                    await ctx.send("✅ Status monitor started! Checking every 15 seconds.")

            elif action == "stop":
                if hasattr(self.status_monitor, 'monitor_status_changes'):
                    if self.status_monitor.monitor_status_changes.is_running():
                        self.status_monitor.stop_monitoring()
                        await ctx.send("🛑 Status monitor stopped.")
                    else:
                        await ctx.send("⚠️ Status monitor is not running.")
                else:
                    await ctx.send("⚠️ Status monitor is not running.")

            elif action == "status":
                if hasattr(self.status_monitor, 'monitor_status_changes'):
                    is_running = self.status_monitor.monitor_status_changes.is_running()
                    status_text = "🟢 RUNNING" if is_running else "🔴 STOPPED"
                    interval = self.status_monitor.check_interval

                    # Add manual-start note to description
                    description = f"**Status:** {status_text}"
                    description += "\n**Start/stop via Control Panel button or !monitor start/stop**"
                    description += f"\n**Check Interval:** {interval} seconds"

                    embed = discord.Embed(
                        title="📊 Status Change Monitor",
                        description=description,
                        color=0x27AE60 if is_running else 0xE74C3C,
                        timestamp=discord.utils.utcnow()
                    )

                    # Show tracking info
                    if hasattr(self.status_monitor, 'last_modified'):
                        tracked_agents = len(self.status_monitor.last_modified)
                        embed.add_field(
                            name="Tracked Agents",
                            value=f"{tracked_agents}/8 agents",
                            inline=True
                        )

                    embed.set_footer(
                        text="Use Control Panel button or !monitor stop/start to control the monitor")
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("⚠️ Status monitor not initialized.")

            else:
                await ctx.send("❌ Invalid action. Use: `!monitor [stop|status]` (monitor auto-starts with bot)")

        except Exception as e:
            self.logger.error(f"Error in monitor command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="message", description="Send message to agent")
    async def message(self, ctx: commands.Context, agent_id: str, *, message: str):
        """Send direct message to agent."""
        try:
            success = await self.gui_controller.send_message(
                agent_id=agent_id,
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Message Sent",
                    description=f"Delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                # Use chunking utility to avoid truncation
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(
                    name="Message", value=message_chunks[0], inline=False)
                # If message was chunked, send additional parts
                if len(message_chunks) > 1:
                    for i, chunk in enumerate(message_chunks[1:], 2):
                        embed.add_field(
                            name=f"Message (continued {i}/{len(message_chunks)})",
                            value=chunk,
                            inline=False
                        )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Failed to send message to {agent_id}")

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Render Mermaid diagram code.

        Usage: !mermaid graph TD; A-->B; B-->C;
        """
        try:
            # Remove code block markers if present
            diagram_code = diagram_code.strip()
            if diagram_code.startswith("```mermaid"):
                diagram_code = diagram_code[10:]
            elif diagram_code.startswith("```"):
                diagram_code = diagram_code[3:]
            if diagram_code.endswith("```"):
                diagram_code = diagram_code[:-3]
            diagram_code = diagram_code.strip()

            # Create embed with mermaid code
            embed = discord.Embed(
                title="📊 Mermaid Diagram",
                description="Mermaid diagram code:",
                color=discord.Color.blue(),
            )

            # Send mermaid code in code block
            # Discord doesn't natively render mermaid, but we can format it nicely
            mermaid_block = f"```mermaid\n{diagram_code}\n```"

            # Discord has a 2000 character limit per message
            if len(mermaid_block) > 1900:
                await ctx.send("❌ Mermaid diagram too long. Please shorten it.")
                return

            embed.add_field(
                name="Diagram Code",
                value=mermaid_block,
                inline=False
            )

            embed.set_footer(
                text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering"
            )

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error rendering mermaid: {e}")
            await ctx.send(f"❌ Error rendering mermaid diagram: {e}")

    @commands.command(name="broadcast", description="Broadcast to all agents")
    async def broadcast(self, ctx: commands.Context, *, message: str):
        """Broadcast message to all agents."""
        try:
            success = await self.gui_controller.broadcast_message(
                message=message,
                priority="regular",
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ Broadcast Sent",
                    description="Delivered to all agents",
                    color=discord.Color.green(),
                )
                # Use chunking utility to avoid truncation
                from src.discord_commander.utils.message_chunking import chunk_field_value
                message_chunks = chunk_field_value(message)
                embed.add_field(
                    name="Message", value=message_chunks[0], inline=False)
                # If message was chunked, send additional parts
                if len(message_chunks) > 1:
                    for i, chunk in enumerate(message_chunks[1:], 2):
                        embed.add_field(
                            name=f"Message (continued {i}/{len(message_chunks)})",
                            value=chunk,
                            inline=False
                        )
                await ctx.send(embed=embed)
            else:
                await ctx.send("❌ Failed to broadcast message")

        except Exception as e:
            self.logger.error(f"Error broadcasting: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Show interactive help menu with navigation buttons."""
        try:
            from .views import HelpGUIView

            view = HelpGUIView()
            embed = view._create_main_embed()

            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="aria", description="✨ View Aria's interactive profile!")
    async def aria_profile(self, ctx: commands.Context):
        """Display Aria's interactive profile with buttons!"""
        try:
            from src.discord_commander.views.aria_profile_view import AriaProfileView

            view = AriaProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !aria command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")
    async def carmyn_profile(self, ctx: commands.Context):
        """Display Carmyn's interactive profile with buttons!"""
        try:
            from .views.carmyn_profile_view import CarmynProfileView

            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="commands", description="List all registered commands (use Control Panel buttons instead!)")
    async def list_commands(self, ctx: commands.Context):
        """List all registered bot commands - redirects to Control Panel button view."""
        try:
            # Instead of listing commands, open Control Panel which has all buttons
            control_view = self.gui_controller.create_control_panel()
            embed = discord.Embed(
                title="📋 All Commands - Use Control Panel Buttons!",
                description=(
                    "**🎯 All commands are accessible via buttons in the Control Panel!**\n\n"
                    "**Click the buttons below to access all features:**\n"
                    "• **Tasks** button = `!swarm_tasks`\n"
                    "• **Swarm Status** button = `!status`\n"
                    "• **GitHub Book** button = `!github_book`\n"
                    "• **Roadmap** button = `!swarm_roadmap`\n"
                    "• **Excellence** button = `!swarm_excellence`\n"
                    "• **Overview** button = `!swarm_overview`\n"
                    "• **Goldmines** button = `!goldmines`\n"
                    "• **Templates** button = `!templates`\n"
                    "• **Mermaid** button = `!mermaid`\n"
                    "• **Monitor** button = `!monitor`\n"
                    "• **Help** button = `!help`\n"
                    "• **All Commands** button = This view\n\n"
                    "**No need to type commands - just click buttons!**"
                ),
                color=discord.Color.blue(),
            )

            embed.add_field(
                name="💡 Quick Access",
                value="Type `!control` (or `!panel`, `!menu`) to open Control Panel anytime!",
                inline=False,
            )

            embed.set_footer(
                text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!"
            )

            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="shutdown", description="Gracefully shutdown the bot")
    async def shutdown_cmd(self, ctx: commands.Context):
        """Gracefully shutdown the Discord bot."""
        try:
            # Confirmation embed
            embed = discord.Embed(
                title="🛑 Shutdown Requested",
                description="Are you sure you want to shutdown the bot?",
                color=discord.Color.red(),
            )

            # Create confirmation view
            view = ConfirmShutdownView()
            message = await ctx.send(embed=embed, view=view)

            # Wait for user confirmation (30 second timeout)
            await view.wait()

            if view.confirmed:
                # Announce shutdown
                shutdown_embed = discord.Embed(
                    title="👋 Bot Shutting Down",
                    description="Gracefully closing connections...",
                    color=discord.Color.orange(),
                )
                await ctx.send(embed=shutdown_embed)

                # Log shutdown
                self.logger.info("🛑 Shutdown command received - closing bot")

                # Close bot gracefully
                await self.bot.close()
            else:
                await message.edit(content="❌ Shutdown cancelled", embed=None, view=None)
        except Exception as e:
            self.logger.error(f"Error in shutdown command: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="restart", description="Restart the Discord bot (true restart - fresh process)")
    async def restart_cmd(self, ctx: commands.Context):
        """Restart the Discord bot with a true process restart (kills current process, starts fresh)."""
        try:
            # Confirmation embed
            embed = discord.Embed(
                title="🔄 True Restart Requested",
                description=(
                    "Bot will perform a TRUE restart:\n"
                    "• Current process will be terminated\n"
                    "• Fresh bot + queue processor will start\n"
                    "• All modules reloaded from disk\n"
                    "• Message delivery enabled (queue processor)\n\n"
                    "Continue?"
                ),
                color=discord.Color.blue(),
            )

            # Create confirmation view
            view = ConfirmRestartView()
            message = await ctx.send(embed=embed, view=view)

            # Wait for user confirmation (30 second timeout)
            await view.wait()

            if view.confirmed:
                # Announce restart
                restart_embed = discord.Embed(
                    title="🔄 Bot Restarting (True Restart)",
                    description=(
                        "Performing true restart...\n"
                        "• Terminating current process\n"
                        "• Starting fresh bot + queue processor\n"
                        "• All modules reloaded from disk\n"
                        "• Will be back in 5-10 seconds!"
                    ),
                    color=discord.Color.blue(),
                )
                await ctx.send(embed=restart_embed)

                # Log restart
                self.logger.info(
                    "🔄 True restart command received - killing process and starting fresh")

                # Perform true restart: spawn new process, then exit current
                self._perform_true_restart()

                # Close bot (will exit after new process starts)
                await self.bot.close()
            else:
                await message.edit(content="❌ Restart cancelled", embed=None, view=None)
        except Exception as e:
            self.logger.error(f"Error in restart command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    def _perform_true_restart(self):
        """Perform true restart: spawn fresh process for bot + queue processor, then exit current."""
        import subprocess
        import sys
        import os
        from pathlib import Path

        try:
            project_root = Path(__file__).parent.parent.parent
            # Use start_discord_system.py to start BOTH bot + queue processor
            # This ensures messages can be sent (queue processor is required)
            start_script = project_root / "tools" / "start_discord_system.py"

            if not start_script.exists():
                self.logger.error(f"Start script not found: {start_script}")
                return False

            # Spawn new process to start bot + queue processor fresh
            # This ensures all code is reloaded from disk (no module cache)
            # AND ensures message queue processor is running (required for message delivery)
            if sys.platform == 'win32':
                # Windows: Use CREATE_NEW_CONSOLE to run in separate window
                subprocess.Popen(
                    [sys.executable, str(start_script)],
                    cwd=str(project_root),
                    creationflags=subprocess.CREATE_NEW_CONSOLE,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Unix-like: use nohup or screen
                subprocess.Popen(
                    [sys.executable, str(start_script)],
                    cwd=str(project_root),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )

            # Give new process a moment to start
            import time
            time.sleep(2)

            self.logger.info(
                "✅ New bot + queue processor processes spawned - current process will exit")
            return True

        except Exception as e:
            self.logger.error(
                f"Error performing true restart: {e}", exc_info=True)
            return False

    @commands.command(name="soft_onboard", aliases=["soft"], description="Soft onboard agent(s)")
    async def soft_onboard(self, ctx: commands.Context, *, agent_ids: str = None):
        """
        Soft onboard agent(s). Can specify single agent, multiple agents, or all.

        Usage:
        !soft Agent-1
        !soft Agent-1,Agent-2,Agent-3
        !soft all
        """
        try:
            import subprocess

            # If no agents specified, default to all
            if not agent_ids or agent_ids.strip().lower() == "all":
                agent_ids = "Agent-1,Agent-2,Agent-3,Agent-4,Agent-5,Agent-6,Agent-7,Agent-8"
                agent_list = [f"Agent-{i}" for i in range(1, 9)]
            else:
                # Parse comma-separated agent IDs
                raw_agent_list = [aid.strip()
                                  for aid in agent_ids.split(",") if aid.strip()]
                # Convert numeric IDs to Agent-X format
                agent_list = []
                for aid in raw_agent_list:
                    if aid.isdigit():
                        agent_list.append(f"Agent-{aid}")
                    elif aid.lower().startswith("agent-"):
                        agent_list.append(aid)  # Already in correct format
                    else:
                        agent_list.append(aid)  # Keep as-is (might be valid)

            if not agent_list:
                await ctx.send("❌ No valid agents specified. Use: `!soft 1` or `!soft Agent-1` or `!soft 1,2,3`")
                return

            # Default message
            message = "🚀 SOFT ONBOARD - Agent activation initiated. Check your inbox and begin autonomous operations."

            embed = discord.Embed(
                title="🚀 SOFT ONBOARD INITIATED",
                description=f"Soft onboarding **{len(agent_list)} agent(s)**...\n\n**Agents:** {', '.join(agent_list)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

            # Soft onboard agents (use --agents for multiple, --agent for single)
            successful = []
            failed = []

            # Get project root (use module-level or calculate)
            project_root = Path(__file__).parent.parent.parent
            cli_path = project_root / 'tools' / 'soft_onboard_cli.py'

            try:
                # Use --agents for multiple agents (more efficient, uses soft_onboard_multiple_agents)
                if len(agent_list) == 1:
                    # Single agent - use --agent
                    cmd = ['python', str(cli_path), '--agent',
                           agent_list[0], '--message', message]
                else:
                    # Multiple agents - use --agents with comma-separated list
                    agents_str = ','.join(agent_list)
                    cmd = ['python', str(
                        cli_path), '--agents', agents_str, '--message', message, '--generate-cycle-report']

                result = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=TimeoutConstants.HTTP_EXTENDED, cwd=str(project_root))

                if result.returncode == 0:
                    # All agents successful
                    successful = agent_list.copy()
                    # Parse output to check individual results if needed
                    if result.stdout:
                        # Check for any failures in output
                        if "Failed:" in result.stdout or "❌" in result.stdout:
                            # Parse individual results from output
                            lines = result.stdout.split('\n')
                            for line in lines:
                                if "✅" in line and any(agent in line for agent in agent_list):
                                    # Agent succeeded
                                    pass
                                elif "❌" in line and any(agent in line for agent in agent_list):
                                    # Agent failed - extract agent ID
                                    for agent in agent_list:
                                        if agent in line and agent not in [s for s in successful]:
                                            failed.append(
                                                (agent, "Failed during onboarding"))
                                            if agent in successful:
                                                successful.remove(agent)
                else:
                    # Command failed - try to parse which agents failed
                    error_msg = result.stderr[:500] if result.stderr else result.stdout[:
                                                                                        500] if result.stdout else "Unknown error"
                    # If we can't determine individual failures, mark all as failed
                    if len(agent_list) == 1:
                        failed.append((agent_list[0], error_msg))
                    else:
                        # For multiple agents, mark all as failed if we can't parse individual results
                        for agent_id in agent_list:
                            failed.append((agent_id, error_msg))
            except subprocess.TimeoutExpired:
                # Timeout - mark all as failed
                for agent_id in agent_list:
                    failed.append((agent_id, "Timeout after 5 minutes"))
            except Exception as e:
                # Exception - mark all as failed
                error_msg = str(e)[:200]
                for agent_id in agent_list:
                    failed.append((agent_id, error_msg))

            # Send results
            if len(successful) == len(agent_list):
                success_embed = discord.Embed(
                    title="✅ SOFT ONBOARD COMPLETE",
                    description=f"All **{len(agent_list)} agent(s)** soft onboarded successfully!",
                    color=discord.Color.green(),
                )
                success_embed.add_field(
                    name="✅ Successful", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                await ctx.send(embed=success_embed)
            elif successful:
                partial_embed = discord.Embed(
                    title="⚠️ PARTIAL SOFT ONBOARD",
                    description=f"**{len(successful)}/{len(agent_list)}** agents onboarded successfully",
                    color=discord.Color.orange(),
                )
                partial_embed.add_field(
                    name="✅ Successful", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                if failed:
                    error_list = "\n".join(
                        [f"❌ {agent}: {error}" for agent, error in failed[:5]])
                    partial_embed.add_field(
                        name="❌ Failed", value=error_list, inline=False)
                await ctx.send(embed=partial_embed)
            else:
                error_embed = discord.Embed(
                    title="❌ SOFT ONBOARD FAILED",
                    description="All agents failed to onboard",
                    color=discord.Color.red(),
                )
                error_list = "\n".join(
                    [f"❌ {agent}: {error}" for agent, error in failed[:5]])
                error_embed.add_field(
                    name="Errors", value=error_list, inline=False)
                await ctx.send(embed=error_embed)

        except Exception as e:
            self.logger.error(f"Error in soft_onboard: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="hard_onboard", aliases=["hard"], description="Hard onboard agent(s)")
    async def hard_onboard(self, ctx: commands.Context, *, agent_ids: str = None):
        """
        Hard onboard agent(s). Can specify single agent, multiple agents, or all.

        Usage:
        !hard_onboard Agent-1
        !hard_onboard Agent-1,Agent-2,Agent-3
        !hard_onboard all
        """
        try:
            import subprocess

            # If no agents specified, default to all
            if not agent_ids or agent_ids.strip().lower() == "all":
                agent_ids = "Agent-1,Agent-2,Agent-3,Agent-4,Agent-5,Agent-6,Agent-7,Agent-8"
                agent_list = [f"Agent-{i}" for i in range(1, 9)]
            else:
                # Parse comma-separated agent IDs
                raw_agent_list = [aid.strip()
                                  for aid in agent_ids.split(",") if aid.strip()]
                # Convert numeric IDs to Agent-X format
                agent_list = []
                for aid in raw_agent_list:
                    if aid.isdigit():
                        agent_list.append(f"Agent-{aid}")
                    elif aid.lower().startswith("agent-"):
                        agent_list.append(aid)  # Already in correct format
                    else:
                        agent_list.append(aid)  # Keep as-is (might be valid)

            if not agent_list:
                await ctx.send("❌ No valid agents specified. Use: `!hard_onboard 1` or `!hard_onboard Agent-1` or `!hard_onboard 1,2,3`")
                return

            embed = discord.Embed(
                title="🚀 HARD ONBOARD INITIATED",
                description=f"Hard onboarding **{len(agent_list)} agent(s)**...\n\n**Agents:** {', '.join(agent_list)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

            # Hard onboard each agent using hard onboarding service
            successful = []
            failed = []

            # Get project root (use module-level or calculate)
            project_root = Path(__file__).parent.parent.parent

            # Import hard onboarding service
            from ..services.hard_onboarding_service import hard_onboard_agent

            for agent_id in agent_list:
                try:
                    # Load onboarding message from agent's workspace
                    onboarding_file = project_root / "agent_workspaces" / \
                        agent_id / "HARD_ONBOARDING_MESSAGE.md"

                    if onboarding_file.exists():
                        onboarding_message = onboarding_file.read_text(
                            encoding="utf-8")
                    else:
                        # Use default onboarding message if file doesn't exist
                        onboarding_message = f"""🚨 HARD ONBOARD - {agent_id}

**Status**: RESET & ACTIVATE
**Protocol**: Complete session reset

**YOUR MISSION**: Resume autonomous operations immediately.

**NEXT ACTIONS**:
1. Check your inbox for assignments
2. Update your status.json
3. Resume autonomous execution
4. Post devlog when work complete

**WE. ARE. SWARM. AUTONOMOUS. POWERFUL. 🐝⚡🔥🚀**"""

                    # Execute hard onboarding
                    success = hard_onboard_agent(
                        agent_id=agent_id,
                        onboarding_message=onboarding_message,
                        role=None
                    )

                    if success:
                        successful.append(agent_id)
                    else:
                        failed.append(
                            (agent_id, "Hard onboarding service returned False"))
                except Exception as e:
                    failed.append((agent_id, str(e)[:200]))

            # Send results
            if len(successful) == len(agent_list):
                success_embed = discord.Embed(
                    title="✅ HARD ONBOARD COMPLETE!",
                    description=f"All **{len(agent_list)} agent(s)** hard onboarded successfully!",
                    color=discord.Color.green(),
                )
                activated_list = "\n".join(
                    [f"✅ {agent}" for agent in successful])
                success_embed.add_field(
                    name="Activated Agents", value=activated_list, inline=False)
                success_embed.add_field(
                    name="Next Steps",
                    value="1. Check agent workspaces for onboarding messages\n2. Use !status to verify agents active\n3. Begin mission assignments",
                    inline=False,
                )
                await ctx.send(embed=success_embed)
            elif successful:
                partial_embed = discord.Embed(
                    title="⚠️ PARTIAL HARD ONBOARD",
                    description=f"**{len(successful)}/{len(agent_list)}** agents onboarded successfully",
                    color=discord.Color.orange(),
                )
                partial_embed.add_field(
                    name="✅ Successful", value="\n".join([f"✅ {agent}" for agent in successful]), inline=False
                )
                if failed:
                    error_list = "\n".join(
                        [f"❌ {agent}: {error}" for agent, error in failed[:5]])
                    partial_embed.add_field(
                        name="❌ Failed", value=error_list, inline=False)
                await ctx.send(embed=partial_embed)
            else:
                error_embed = discord.Embed(
                    title="❌ HARD ONBOARD FAILED",
                    description="All agents failed to onboard",
                    color=discord.Color.red(),
                )
                error_list = "\n".join(
                    [f"❌ {agent}: {error}" for agent, error in failed[:5]])
                error_embed.add_field(
                    name="Errors", value=error_list, inline=False)
                await ctx.send(embed=error_embed)

        except Exception as e:
            self.logger.error(f"Error in hard_onboard: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="git_push", aliases=["push", "github_push"], description="Push project to GitHub")
    async def git_push(self, ctx: commands.Context, *, commit_message: str = None):
        """
        Push project to GitHub. Automatically stages, commits, and pushes changes.

        Usage:
        !git_push "Your commit message"
        !push "Fixed bug in messaging system"
        """
        try:
            import subprocess
            from pathlib import Path

            # Get project root
            project_root = Path(__file__).parent.parent.parent

            # Check if we're in a git repository
            git_check = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            if git_check.returncode != 0:
                await ctx.send("❌ Not a git repository or git not available")
                return

            # Start embed
            embed = discord.Embed(
                title="🚀 GitHub Push",
                description="Pushing changes to GitHub...",
                color=discord.Color.blue()
            )
            status_msg = await ctx.send(embed=embed)

            # Step 1: Check git status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            if not status_result.stdout.strip():
                embed.description = "✅ No changes to commit"
                embed.color = discord.Color.green()
                await status_msg.edit(embed=embed)
                return

            # Step 2: Add all changes
            embed.add_field(
                name="📦 Staging Changes",
                value="Adding all changes...",
                inline=False
            )
            await status_msg.edit(embed=embed)

            add_result = subprocess.run(
                ["git", "add", "-A"],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            if add_result.returncode != 0:
                embed.description = f"❌ Error staging changes: {add_result.stderr}"
                embed.color = discord.Color.red()
                await status_msg.edit(embed=embed)
                return

            # Step 3: Commit
            if not commit_message:
                commit_message = f"Auto-commit: {ctx.author.name} via Discord bot"

            embed.fields[0].value = "✅ Changes staged"
            embed.add_field(
                name="💾 Committing",
                value=f"Message: {commit_message}",
                inline=False
            )
            await status_msg.edit(embed=embed)

            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            if commit_result.returncode != 0:
                if "nothing to commit" in commit_result.stdout:
                    embed.description = "ℹ️ Nothing to commit (changes already committed)"
                    embed.color = discord.Color.orange()
                    embed.remove_field(1)
                    await status_msg.edit(embed=embed)
                    return
                else:
                    embed.description = f"❌ Error committing: {commit_result.stderr}"
                    embed.color = discord.Color.red()
                    await status_msg.edit(embed=embed)
                    return

            # Step 4: Push to GitHub
            embed.fields[1].value = "✅ Committed"
            embed.add_field(
                name="🚀 Pushing",
                value="Pushing to GitHub...",
                inline=False
            )
            await status_msg.edit(embed=embed)

            # Get current branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            current_branch = branch_result.stdout.strip(
            ) if branch_result.returncode == 0 else "main"

            push_result = subprocess.run(
                ["git", "push", "origin", current_branch],
                cwd=project_root,
                capture_output=True,
                text=True
            )

            if push_result.returncode != 0:
                embed.description = f"❌ Error pushing to GitHub: {push_result.stderr}"
                embed.color = discord.Color.red()
                await status_msg.edit(embed=embed)
                return

            # Success!
            embed.description = "✅ Successfully pushed to GitHub!"
            embed.color = discord.Color.green()
            embed.fields[2].value = f"✅ Pushed to `{current_branch}`"
            embed.add_field(
                name="📊 Summary",
                value=(
                    f"**Branch:** {current_branch}\n"
                    f"**Commit:** {commit_message}\n"
                    f"**User:** {ctx.author.name}"
                ),
                inline=False
            )
            await status_msg.edit(embed=embed)

            self.logger.info(
                f"✅ Git push successful: {commit_message} by {ctx.author.name}")

        except Exception as e:
            self.logger.error(f"Error in git_push command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="unstall", description="Unstall an agent (recover from stall)")
    async def unstall(self, ctx: commands.Context, agent_id: str):
        """Unstall an agent by sending reset signal and continuation message."""
        try:
            from pathlib import Path
            import json

            # Read agent's status.json to get last known state
            status_file = Path(f"agent_workspaces/{agent_id}/status.json")
            last_state = "Unknown"
            if status_file.exists():
                try:
                    status_data = json.loads(
                        status_file.read_text(encoding="utf-8"))
                    last_state = status_data.get("current_mission", "Unknown")
                except:
                    pass

            # Create unstall message
            unstall_message = f"""🚨 UNSTICK PROTOCOL - CONTINUE IMMEDIATELY

Agent, you appear stalled. CONTINUE AUTONOMOUSLY NOW.

**Your last known state:** {last_state}
**Likely stall cause:** approval dependency / command fail / unclear next

**IMMEDIATE ACTIONS (pick one and EXECUTE):**
1. Complete your current task
2. Move to next action in your queue
3. Clean workspace and report status
4. Check inbox and respond to messages
5. Scan for new opportunities
6. Update documentation
7. Report to Captain with next plans

**REMEMBER:**
- You are AUTONOMOUS - no approval needed
- System messages are NOT stop signals
- Command failures are NOT blockers
- ALWAYS have next actions
- YOU are your own gas station

**DO NOT WAIT. EXECUTE NOW.**

#UNSTICK-PROTOCOL #AUTONOMOUS-OPERATION"""

            # Send unstall message via messaging service (use Ctrl+Enter for stalled agents)
            success = await self.gui_controller.send_message(
                agent_id=agent_id,
                message=unstall_message,
                priority="urgent",
                stalled=True,
                discord_user=ctx.author,
            )

            if success:
                embed = discord.Embed(
                    title="✅ UNSTALL MESSAGE SENT",
                    description=f"Unstall message delivered to **{agent_id}**",
                    color=discord.Color.green(),
                )
                embed.add_field(
                    name="Action",
                    value="Agent should receive continuation message and resume autonomous operations",
                    inline=False,
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Failed to send unstall message to {agent_id}")

        except Exception as e:
            self.logger.error(f"Error in unstall: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="heal", aliases=["self_heal", "healing"], description="Self-healing system commands")
    async def heal(self, ctx: commands.Context, action: str = "status", agent_id: str = None):
        """
        Self-healing system commands.

        Usage:
        !heal status - Show healing statistics
        !heal check - Immediately check and heal all stalled agents
        !heal stats [Agent-X] - Show detailed stats for agent (or all agents)
        !heal cancel_count [Agent-X] - Show terminal cancellation count today
        """
        try:
            from src.core.agent_self_healing_system import (
                get_self_healing_system,
                heal_stalled_agents_now
            )
            import asyncio

            system = get_self_healing_system()

            if action.lower() == "status" or action.lower() == "stats":
                # Show healing statistics
                stats = system.get_healing_stats()

                embed = discord.Embed(
                    title="🏥 Self-Healing System Status",
                    description="Agent stall detection and recovery statistics",
                    color=discord.Color.blue(),
                )

                # Overall stats
                embed.add_field(
                    name="📊 Overall Statistics",
                    value=(
                        f"**Total Actions:** {stats['total_actions']}\n"
                        f"**Success Rate:** {stats['success_rate']:.1f}%\n"
                        f"**Successful:** {stats['successful']}\n"
                        f"**Failed:** {stats['failed']}"
                    ),
                    inline=False
                )

                # Terminal cancellation counts
                cancel_counts = stats.get('terminal_cancellations_today', {})
                cancel_summary = "\n".join([
                    f"{agent}: {count}" for agent, count in cancel_counts.items() if count > 0
                ]) or "None today"

                embed.add_field(
                    name="🛑 Terminal Cancellations (Today)",
                    value=cancel_summary,
                    inline=False
                )

                # Recent actions
                if stats.get('recent_actions'):
                    recent = stats['recent_actions'][-5:]  # Last 5
                    recent_text = "\n".join([
                        f"{'✅' if a['success'] else '❌'} **{a['agent_id']}**: {a['action']}"
                        for a in recent
                    ])
                    embed.add_field(
                        name="🔄 Recent Actions",
                        value=recent_text[:1024],  # Discord limit
                        inline=False
                    )

                await ctx.send(embed=embed)

            elif action.lower() == "check" or action.lower() == "heal":
                # Immediately check and heal stalled agents
                await ctx.send("🔍 Checking for stalled agents and healing...")

                results = await heal_stalled_agents_now()

                embed = discord.Embed(
                    title="🏥 Healing Check Results",
                    description=f"Checked at {results['timestamp']}",
                    color=discord.Color.green(
                    ) if results['stalled_agents_found'] == 0 else discord.Color.orange(),
                )

                embed.add_field(
                    name="📊 Results",
                    value=(
                        f"**Stalled Agents Found:** {results['stalled_agents_found']}\n"
                        f"**Agents Healed:** {len(results['agents_healed'])}\n"
                        f"**Agents Failed:** {len(results['agents_failed'])}"
                    ),
                    inline=False
                )

                if results['agents_healed']:
                    embed.add_field(
                        name="✅ Successfully Healed",
                        value=", ".join(results['agents_healed']),
                        inline=False
                    )

                if results['agents_failed']:
                    embed.add_field(
                        name="❌ Failed to Heal",
                        value=", ".join(results['agents_failed']),
                        inline=False
                    )

                await ctx.send(embed=embed)

            elif action.lower() == "cancel_count" or action.lower() == "cancellations":
                # Show terminal cancellation count
                if agent_id:
                    count = system.get_cancellation_count_today(agent_id)
                    embed = discord.Embed(
                        title=f"🛑 Terminal Cancellations - {agent_id}",
                        description=f"**Today:** {count} cancellation(s)",
                        color=discord.Color.orange() if count > 0 else discord.Color.green(),
                    )
                else:
                    cancel_counts = system.get_healing_stats().get(
                        'terminal_cancellations_today', {})
                    total = sum(cancel_counts.values())
                    embed = discord.Embed(
                        title="🛑 Terminal Cancellations (Today)",
                        description=f"**Total:** {total} cancellation(s) across all agents",
                        color=discord.Color.orange() if total > 0 else discord.Color.green(),
                    )
                    for agent, count in cancel_counts.items():
                        if count > 0:
                            embed.add_field(
                                name=agent, value=str(count), inline=True)

                await ctx.send(embed=embed)

            elif action.lower() == "agent" and agent_id:
                # Show detailed stats for specific agent
                stats = system.get_healing_stats()
                agent_stats = stats['by_agent'].get(agent_id, {})
                cancel_count = system.get_cancellation_count_today(agent_id)

                embed = discord.Embed(
                    title=f"🏥 Agent Healing Stats - {agent_id}",
                    color=discord.Color.blue(),
                )

                embed.add_field(
                    name="📊 Healing Actions",
                    value=(
                        f"**Total:** {agent_stats.get('total', 0)}\n"
                        f"**Successful:** {agent_stats.get('successful', 0)}\n"
                        f"**Failed:** {agent_stats.get('failed', 0)}"
                    ),
                    inline=False
                )

                embed.add_field(
                    name="🛑 Terminal Cancellations",
                    value=f"**Today:** {cancel_count}",
                    inline=False
                )

                await ctx.send(embed=embed)

            else:
                await ctx.send(
                    f"❌ Unknown action: `{action}`\n"
                    f"**Usage:** `!heal [status|check|cancel_count|agent] [Agent-X]`\n"
                    f"**Examples:**\n"
                    f"- `!heal status` - Show overall stats\n"
                    f"- `!heal check` - Immediately heal stalled agents\n"
                    f"- `!heal cancel_count Agent-3` - Show cancellation count\n"
                    f"- `!heal agent Agent-3` - Show agent-specific stats"
                )

        except ImportError as e:
            await ctx.send(f"❌ Self-healing system not available: {e}")
        except Exception as e:
            self.logger.error(f"Error in heal command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="obs", description="View observations")
    async def obs(self, ctx: commands.Context):
        """View observations."""
        try:
            embed = discord.Embed(
                title="👁️ Observations",
                description="**Observations feature**\n\nThis command is being implemented.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Status",
                value="Feature in development",
                inline=False,
            )
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error in obs command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="pieces", description="View pieces")
    async def pieces(self, ctx: commands.Context):
        """View pieces."""
        try:
            embed = discord.Embed(
                title="🧩 Pieces",
                description="**Pieces feature**\n\nThis command is being implemented.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Status",
                value="Feature in development",
                inline=False,
            )
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error in pieces command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="sftp", aliases=["sftp_creds", "ftp"], description="Get SFTP credentials guide")
    async def sftp(self, ctx: commands.Context):
        """Get SFTP credentials - streamlined guide."""
        try:
            embed = discord.Embed(
                title="🔑 How to Get SFTP Credentials (30 seconds)",
                description="**Quick guide to get your SFTP credentials from Hostinger**",
                color=discord.Color.green(),
            )

            embed.add_field(
                name="Step 1: Log into Hostinger",
                value="👉 https://hpanel.hostinger.com/",
                inline=False,
            )

            embed.add_field(
                name="Step 2: Get Credentials",
                value=(
                    "1. Click **Files** → **FTP Accounts**\n"
                    "2. Find your domain\n"
                    "3. Copy these 4 values:\n"
                    "   • **FTP Username** (not your email!)\n"
                    "   • **FTP Password** (click 'Show' or reset if needed)\n"
                    "   • **FTP Host** (IP address like `157.173.214.121`)\n"
                    "   • **FTP Port** (should be `65002`)"
                ),
                inline=False,
            )

            embed.add_field(
                name="Step 3: Add to .env File",
                value=(
                    "Open `.env` in repository root, add:\n"
                    "```env\n"
                    "HOSTINGER_HOST=157.173.214.121\n"
                    "HOSTINGER_USER=your_username_here\n"
                    "HOSTINGER_PASS=your_password_here\n"
                    "HOSTINGER_PORT=65002\n"
                    "```"
                ),
                inline=False,
            )

            embed.add_field(
                name="Step 4: Test",
                value="```bash\npython tools/sftp_credential_troubleshooter.py\n```",
                inline=False,
            )

            embed.add_field(
                name="💡 Tip",
                value="Username might be different from your email (check Hostinger exactly as shown)",
                inline=False,
            )

            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡🔥")

            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error in sftp command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="session", aliases=["sessions", "cycle"], description="Post session accomplishments report")
    async def session(self, ctx: commands.Context, date: str = None):
        """
        Post beautiful session accomplishments report to Discord.

        Usage:
        !session - Show most recent session report
        !session 2025-11-28 - Show report for specific date
        !session latest - Show most recent report
        """
        try:
            from pathlib import Path
            import re
            from datetime import datetime

            cycles_dir = Path("docs/archive/cycles")
            if not cycles_dir.exists():
                await ctx.send("❌ Cycles directory not found: `docs/archive/cycles/`")
                return

            # Find cycle report files
            cycle_files = sorted(cycles_dir.glob(
                "CYCLE_ACCOMPLISHMENTS_*.md"), reverse=True)

            if not cycle_files:
                await ctx.send("❌ No cycle accomplishment reports found in `docs/archive/cycles/`")
                return

            # Select file based on date parameter
            selected_file = None
            if date:
                if date.lower() == "latest":
                    selected_file = cycle_files[0]
                else:
                    # Try to match date in filename
                    date_pattern = date.replace("-", "_")
                    for f in cycle_files:
                        if date_pattern in f.name:
                            selected_file = f
                            break
                    if not selected_file:
                        await ctx.send(f"❌ No report found for date: {date}\n**Available dates:** Use `!session latest` to see most recent")
                        return
            else:
                # Default to most recent
                selected_file = cycle_files[0]

            # Read and parse report
            report_content = selected_file.read_text(encoding="utf-8")

            # Extract date from filename
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', selected_file.name)
            report_date = date_match.group(1) if date_match else "Unknown"

            # Parse report sections
            lines = report_content.split('\n')

            # Extract summary
            summary = {}
            in_summary = False
            for line in lines:
                if "## 📊 SWARM SUMMARY" in line:
                    in_summary = True
                    continue
                if in_summary and line.startswith("##"):
                    break
                if in_summary and "- **" in line:
                    match = re.search(r'\*\*(.+?)\*\*: (.+)', line)
                    if match:
                        summary[match.group(1)] = match.group(2).strip()

            # Extract agent accomplishments
            agents_data = {}
            current_agent = None
            current_section = None
            current_content = []

            for line in lines:
                if line.startswith("### Agent-"):
                    # Save previous agent
                    if current_agent:
                        agents_data[current_agent][current_section] = '\n'.join(
                            current_content).strip()

                    # Start new agent
                    match = re.match(r'### (Agent-\d+) - (.+)', line)
                    if match:
                        current_agent = match.group(1)
                        agents_data[current_agent] = {
                            'name': match.group(2),
                            'completed_tasks': [],
                            'achievements': [],
                            'current_tasks': []
                        }
                        current_content = []
                        current_section = None
                elif current_agent and line.startswith("####"):
                    # Save previous section
                    if current_section and current_content:
                        if current_section == 'completed_tasks':
                            agents_data[current_agent]['completed_tasks'] = [c.strip(
                                '- ').strip() for c in current_content if c.strip() and c.strip().startswith('-')]
                        elif current_section == 'achievements':
                            agents_data[current_agent]['achievements'] = [c.strip(
                                '- ').strip() for c in current_content if c.strip() and c.strip().startswith('-')]
                        elif current_section == 'current_tasks':
                            agents_data[current_agent]['current_tasks'] = [c.strip(
                                '- ').strip() for c in current_content if c.strip() and c.strip().startswith('-')]

                    # Start new section
                    if "Completed Tasks" in line:
                        current_section = 'completed_tasks'
                    elif "Achievements" in line:
                        current_section = 'achievements'
                    elif "Current Tasks" in line:
                        current_section = 'current_tasks'
                    else:
                        current_section = None
                    current_content = []
                elif current_agent and current_section and line.strip():
                    current_content.append(line)

            # Save last agent
            if current_agent and current_section and current_content:
                if current_section == 'completed_tasks':
                    agents_data[current_agent]['completed_tasks'] = [c.strip(
                        '- ').strip() for c in current_content if c.strip() and c.strip().startswith('-')]
                elif current_section == 'achievements':
                    agents_data[current_agent]['achievements'] = [c.strip(
                        '- ').strip() for c in current_content if c.strip() and c.strip().startswith('-')]

            # Create beautiful embed
            embed = discord.Embed(
                title="📊 SESSION ACCOMPLISHMENTS REPORT",
                description=f"**Date**: {report_date}\n**Report**: `{selected_file.name}`",
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )

            # Add summary fields
            if summary:
                summary_text = "\n".join(
                    [f"**{k}**: {v}" for k, v in summary.items()])
                embed.add_field(
                    name="📊 Swarm Summary",
                    value=summary_text[:1024],
                    inline=False
                )

            # Add agent accomplishments (limit to fit Discord limits)
            agent_texts = []
            for agent_id in sorted(agents_data.keys()):
                data = agents_data[agent_id]
                agent_text = f"**{agent_id}** - {data['name']}\n"

                if data['completed_tasks']:
                    task_count = len(data['completed_tasks'])
                    agent_text += f"✅ **{task_count}** completed tasks\n"
                    # Show first 3 tasks
                    for task in data['completed_tasks'][:3]:
                        task_short = task[:80] + \
                            "..." if len(task) > 80 else task
                        agent_text += f"  • {task_short}\n"
                    if task_count > 3:
                        agent_text += f"  • *... and {task_count - 3} more*\n"

                if data['achievements']:
                    achievement_count = len(data['achievements'])
                    agent_text += f"🏆 **{achievement_count}** achievements\n"
                    # Show first 2 achievements
                    for achievement in data['achievements'][:2]:
                        achievement_short = achievement[:80] + \
                            "..." if len(achievement) > 80 else achievement
                        agent_text += f"  • {achievement_short}\n"
                    if achievement_count > 2:
                        agent_text += f"  • *... and {achievement_count - 2} more*\n"

                agent_texts.append(agent_text)

            # Split agents into chunks to fit Discord limits
            chunk_size = 3  # 3 agents per embed field
            for i in range(0, len(agent_texts), chunk_size):
                chunk = agent_texts[i:i+chunk_size]
                field_value = "\n".join(chunk)
                if len(field_value) > 1024:
                    field_value = field_value[:1021] + "..."

                field_name = f"🤖 Agents {i+1}-{min(i+chunk_size, len(agent_texts))}" if len(
                    agent_texts) > chunk_size else "🤖 Agent Accomplishments"
                embed.add_field(
                    name=field_name,
                    value=field_value,
                    inline=False
                )

            # Add footer
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡🔥")

            # Send embed
            await ctx.send(embed=embed)

            # If report is very long, also send a link to the full report
            if len(report_content) > 4000:
                await ctx.send(
                    f"📄 **Full Report Available**: `{selected_file.name}`\n"
                    f"💡 Use `!session {report_date}` to view this report again"
                )

        except Exception as e:
            self.logger.error(f"Error in session command: {e}", exc_info=True)
            await ctx.send(f"❌ Error: {e}")


async def main() -> int:
    """Main function to run the unified Discord bot with automatic reconnection. Returns exit code."""
    # Setup logging with file output for debugging
    log_dir = Path("runtime/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"discord_bot_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Configure logging with both console and file handlers
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Console output
            logging.FileHandler(log_file, encoding='utf-8')  # File output
        ]
    )
    
    logger.info(f"📝 Logging to file: {log_file}")

    # Get token from environment
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print("❌ DISCORD_BOT_TOKEN not set in environment!")
        print("   Set it with: $env:DISCORD_BOT_TOKEN='your_token' (Windows)")
        print("   Or add to .env file")
        sys.exit(1)

    # Get channel ID (optional)
    channel_id = os.getenv("DISCORD_CHANNEL_ID")
    if channel_id:
        try:
            channel_id = int(channel_id)
        except ValueError:
            print(f"⚠️  Invalid DISCORD_CHANNEL_ID: {channel_id}")
            channel_id = None

    # Create bot instance
    bot = UnifiedDiscordBot(token=token, channel_id=channel_id)

    # Reconnection settings
    max_reconnect_attempts = 999999  # Essentially infinite
    base_delay = 5  # Start with 5 seconds
    max_delay = 300  # Max 5 minutes between attempts
    reconnect_delay = base_delay
    reconnect_count = 0
    consecutive_failures = 0
    max_consecutive_failures = 10  # After 10 failures, increase delay significantly

    print("🚀 Starting Discord Commander...")
    print("🐝 WE. ARE. SWARM.")
    print("🔄 Auto-reconnect enabled - bot will automatically reconnect on internet outage\n")

    while reconnect_count < max_reconnect_attempts:
        try:
            # Attempt to start/restart bot
            if reconnect_count > 0:
                logger.info(
                    f"🔄 Reconnection attempt {reconnect_count} (delay: {reconnect_delay}s)")
                await asyncio.sleep(reconnect_delay)

            logger.info("🔌 Connecting to Discord...")
            try:
                await bot.start(token)
            except Exception as runtime_error:
                # Runtime error during bot operation (after successful connection)
                # This catches errors that occur during bot runtime, not during connection
                logger.error(
                    f"❌ Runtime error during bot operation: {runtime_error}\n"
                    f"   This error occurred after bot connected successfully.\n"
                    f"   Attempt {reconnect_count + 1}, consecutive failures: {consecutive_failures + 1}\n"
                    f"   Retrying in {reconnect_delay} seconds...",
                    exc_info=True
                )
                consecutive_failures += 1
                reconnect_count += 1
                
                # Exponential backoff for runtime errors
                if consecutive_failures >= max_consecutive_failures:
                    reconnect_delay = min(max_delay, reconnect_delay * 2)
                else:
                    reconnect_delay = min(max_delay, reconnect_delay * 1.5)
                
                # Add jitter
                import random
                jitter = random.uniform(0.8, 1.2)
                reconnect_delay = int(reconnect_delay * jitter)
                
                # Close bot before retry
                try:
                    await bot.close()
                except Exception as close_error:
                    logger.error(f"Error closing bot after runtime error: {close_error}", exc_info=True)
                
                # Wait before retry
                continue

            # If we get here, bot.start() has returned (bot disconnected or closed)
            # Check if this was an intentional shutdown
            if hasattr(bot, '_intentional_shutdown') and bot._intentional_shutdown:
                logger.info("✅ Bot shutdown requested - exiting cleanly")
                return 0  # Clean exit for intentional shutdown
            
            # Bot disconnected unexpectedly - continue loop to reconnect
            logger.warning("⚠️ Bot disconnected - will reconnect in next iteration")
            reconnect_count += 1
            consecutive_failures = 0  # Reset failures since we did connect successfully
            reconnect_delay = base_delay  # Reset delay
            # Continue loop for reconnection

        except KeyboardInterrupt:
            print("\n🛑 Bot stopped by user")
            logger.info("🛑 Bot stopped by user (KeyboardInterrupt)")
            bot._intentional_shutdown = True  # Mark as intentional shutdown
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot on KeyboardInterrupt: {e}", exc_info=True)
            return 0  # Clean exit

        except discord.LoginFailure as e:
            print(f"❌ Invalid Discord token: {e}")
            logger.error(f"Login failure: {e}")
            # Don't retry on login failure - token is wrong
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot on login failure: {e}", exc_info=True)
            return 1  # Exit with error code

        except discord.PrivilegedIntentsRequired as e:
            print(f"❌ Missing required intents: {e}")
            logger.error(f"Intents error: {e}")
            # Don't retry on intents error - configuration issue
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot on intents error: {e}", exc_info=True)
            return 1  # Exit with error code

        except discord.errors.ConnectionClosed as e:
            # Discord connection closed - attempt to reconnect
            logger.warning(
                f"⚠️ Discord connection closed (code: {e.code}): {e}\n"
                f"   Attempt {reconnect_count + 1}, will reconnect..."
            )
            reconnect_count += 1
            consecutive_failures = 0  # Connection closed isn't a failure, it's expected
            
            # Close bot before retry
            try:
                await bot.close()
            except Exception as close_error:
                logger.error(f"Error closing bot after ConnectionClosed: {close_error}", exc_info=True)
            
            # Wait before retry
            continue
            
        except (ConnectionError, OSError, asyncio.TimeoutError) as e:
            # Network-related errors - retry with backoff
            consecutive_failures += 1
            reconnect_count += 1

            error_type = type(e).__name__
            logger.warning(
                f"⚠️ Network error ({error_type}): {e}\n"
                f"   Attempt {reconnect_count}, consecutive failures: {consecutive_failures}\n"
                f"   Retrying in {reconnect_delay} seconds..."
            )

            # Exponential backoff with jitter
            if consecutive_failures >= max_consecutive_failures:
                # After many failures, use longer delays
                reconnect_delay = min(max_delay, reconnect_delay * 2)
            else:
                # Normal exponential backoff
                reconnect_delay = min(max_delay, reconnect_delay * 1.5)

            # Add small random jitter to prevent thundering herd
            import random
            jitter = random.uniform(0.8, 1.2)
            reconnect_delay = int(reconnect_delay * jitter)

            # Close bot before retry
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot after network error: {e}", exc_info=True)

            # Wait before retry
            continue

        except Exception as e:
            # Other errors - log and retry with backoff
            consecutive_failures += 1
            reconnect_count += 1

            logger.error(
                f"❌ Bot error: {e}\n"
                f"   Attempt {reconnect_count}, consecutive failures: {consecutive_failures}\n"
                f"   Retrying in {reconnect_delay} seconds...",
                exc_info=True
            )

            # Exponential backoff
            if consecutive_failures >= max_consecutive_failures:
                reconnect_delay = min(max_delay, reconnect_delay * 2)
            else:
                reconnect_delay = min(max_delay, reconnect_delay * 1.5)

            # Add jitter
            import random
            jitter = random.uniform(0.8, 1.2)
            reconnect_delay = int(reconnect_delay * jitter)

            # Close bot before retry
            try:
                await bot.close()
            except Exception as e:
                logger.error(f"Error closing bot after network error: {e}", exc_info=True)

            # Wait before retry
            continue

    # Should never reach here, but just in case
    logger.error("❌ Max reconnection attempts reached")
    try:
        await bot.close()
    except Exception as e:
        logger.error(f"Error closing bot after max attempts: {e}", exc_info=True)
    return 1


if __name__ == "__main__":
    if not DISCORD_AVAILABLE:
        print("❌ discord.py not available. Install with: pip install discord.py")
        sys.exit(1)

    exit_code = asyncio.run(main())
    sys.exit(exit_code if exit_code is not None else 0)
