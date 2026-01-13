<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
"""
Utility Commands - Modular V2 Compliance
========================================

Utility commands (mermaid, help, commands) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular utility commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController
=======
=======
#!/usr/bin/env python3
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
"""
Utility Commands - Modular V2 Compliance
========================================

Utility commands (mermaid, help, commands) extracted from bot_messaging_commands.py.

<!-- SSOT Domain: messaging -->

V2 Compliant: Modular utility commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08
"""

import logging
<<<<<<< HEAD
import subprocess
from pathlib import Path
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
from typing import TYPE_CHECKING
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

if TYPE_CHECKING:
    from src.discord_commander.unified_discord_bot import UnifiedDiscordBot
    from src.discord_commander.discord_gui_controller import DiscordGUIController

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class UtilityCommands(commands.Cog):
<<<<<<< HEAD
<<<<<<< HEAD
    """Utility commands for various bot functions."""

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize utility commands."""
        super().__init__()
=======
    """Utility commands for bot operations."""
=======
    """Utility commands for various bot functions."""
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

    def __init__(self, bot: "UnifiedDiscordBot", gui_controller: "DiscordGUIController"):
        """Initialize utility commands."""
<<<<<<< HEAD
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
        commands.Cog.__init__(self)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="mermaid", description="Render Mermaid diagram")
<<<<<<< HEAD
<<<<<<< HEAD
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Render Mermaid diagram code."""
        try:
            diagram_code = self._clean_mermaid_code(diagram_code)
=======
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Render Mermaid diagram code."""
        try:
<<<<<<< HEAD
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
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            diagram_code = self._clean_mermaid_code(diagram_code)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            embed = discord.Embed(
                title="📊 Mermaid Diagram",
                description="Mermaid diagram code:",
                color=discord.Color.blue(),
            )
<<<<<<< HEAD
<<<<<<< HEAD
            mermaid_block = f"```mermaid\n{diagram_code}\n```"

=======

            # Send mermaid code in code block
            # Discord doesn't natively render mermaid, but we can format it nicely
            mermaid_block = f"```mermaid\n{diagram_code}\n```"

            # Discord has a 2000 character limit per message
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            mermaid_block = f"```mermaid\n{diagram_code}\n```"

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            if len(mermaid_block) > 1900:
                await ctx.send("❌ Mermaid diagram too long. Please shorten it.")
                return

<<<<<<< HEAD
<<<<<<< HEAD
            embed.add_field(name="Diagram Code", value=mermaid_block, inline=False)
            embed.set_footer(text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering")
            await ctx.send(embed=embed)
=======
            embed.add_field(
                name="Diagram Code",
                value=mermaid_block,
                inline=False
            )

            embed.set_footer(
                text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering"
            )

            await ctx.send(embed=embed)

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            embed.add_field(name="Diagram Code", value=mermaid_block, inline=False)
            embed.set_footer(text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering")
            await ctx.send(embed=embed)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        except Exception as e:
            self.logger.error(f"Error rendering mermaid: {e}")
            await ctx.send(f"❌ Error rendering mermaid diagram: {e}")

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    def _clean_mermaid_code(self, diagram_code: str) -> str:
        """Clean mermaid code block markers."""
        diagram_code = diagram_code.strip()
        if diagram_code.startswith("```mermaid"):
            diagram_code = diagram_code[10:]
        elif diagram_code.startswith("```"):
            diagram_code = diagram_code[3:]
        if diagram_code.endswith("```"):
            diagram_code = diagram_code[:-3]
        return diagram_code.strip()

<<<<<<< HEAD
    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Show interactive help menu with navigation buttons."""
        try:
            from src.discord_commander.views import HelpGUIView
            view = HelpGUIView()
            embed = view._create_main_embed()
=======
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    @commands.command(name="help", description="Show help information")
    async def help_cmd(self, ctx: commands.Context):
        """Show interactive help menu with navigation buttons."""
        try:
            from src.discord_commander.views import HelpGUIView
            view = HelpGUIView()
            embed = view._create_main_embed()
<<<<<<< HEAD

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
            await ctx.send(f"❌ Error: {e}")

<<<<<<< HEAD
<<<<<<< HEAD
    @commands.command(name="commands", description="List all registered commands")
    async def list_commands(self, ctx: commands.Context):
        """List all registered bot commands - redirects to Control Panel button view."""
        try:
=======
    @commands.command(name="commands", description="List all registered commands (use Control Panel buttons instead!)")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
=======
    @commands.command(name="commands", description="List all registered commands")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
    async def list_commands(self, ctx: commands.Context):
        """List all registered bot commands - redirects to Control Panel button view."""
        try:
<<<<<<< HEAD
            # Instead of listing commands, open Control Panel which has all buttons
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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
<<<<<<< HEAD
<<<<<<< HEAD
=======

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            embed.add_field(
                name="💡 Quick Access",
                value="Type `!control` (or `!panel`, `!menu`) to open Control Panel anytime!",
                inline=False,
            )
<<<<<<< HEAD
<<<<<<< HEAD
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!")
=======

            embed.set_footer(
                text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!"
            )

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!")
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await ctx.send(f"❌ Error: {e}")

<<<<<<< HEAD
<<<<<<< HEAD

__all__ = ["UtilityCommands"]
=======
    @commands.command(name="git_push", aliases=["push", "github_push"], description="Push project to GitHub")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def git_push(self, ctx: commands.Context, *, commit_message: str = None):
        """
        Push project to GitHub. Automatically stages, commits, and pushes changes.

        Usage:
        !git_push "Your commit message"
        !push "Fixed bug in messaging system"
        """
        self.logger.info(f"Command 'git_push' triggered by {ctx.author}")
        try:
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
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def unstall(self, ctx: commands.Context, agent_id: str):
        """Unstall an agent by sending reset signal and continuation message."""
        self.logger.info(f"Command 'unstall' triggered by {ctx.author} on {agent_id}")
        try:
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

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======

__all__ = ["UtilityCommands"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
