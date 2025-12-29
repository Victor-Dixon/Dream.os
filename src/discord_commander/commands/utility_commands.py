"""
Utility Commands
================

Utility commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Git operations, agent management, help, and utility functions.

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import json
import logging
import subprocess
from pathlib import Path

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class UtilityCommands(commands.Cog):
    """Utility commands for bot operations."""

    def __init__(self, bot, gui_controller):
        """Initialize utility commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="mermaid", description="Render Mermaid diagram")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def mermaid(self, ctx: commands.Context, *, diagram_code: str):
        """Render Mermaid diagram code.

        Usage: !mermaid graph TD; A-->B; B-->C;
        """
        self.logger.info(f"Command 'mermaid' triggered by {ctx.author}")
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

    @commands.command(name="help", description="Show help information")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def help_cmd(self, ctx: commands.Context):
        """Show interactive help menu with navigation buttons."""
        self.logger.info(f"Command 'help' triggered by {ctx.author}")
        try:
            from ..views import HelpGUIView

            view = HelpGUIView()
            embed = view._create_main_embed()

            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
            await ctx.send(f"❌ Error: {e}")

    @commands.command(name="commands", description="List all registered commands (use Control Panel buttons instead!)")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def list_commands(self, ctx: commands.Context):
        """List all registered bot commands - redirects to Control Panel button view."""
        self.logger.info(f"Command 'commands' triggered by {ctx.author}")
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

