"""
<!-- SSOT Domain: discord -->

Onboarding Commands
===================

Onboarding commands extracted from unified_discord_bot.py for V2 compliance.
Handles: Soft onboard and hard onboard agent commands.

V2 Compliance: <300 lines, <5 classes, <10 functions
"""

import logging
import subprocess
from pathlib import Path

import discord
from discord.ext import commands

from src.core.config.timeout_constants import TimeoutConstants

logger = logging.getLogger(__name__)


class OnboardingCommands(commands.Cog):
    """Onboarding commands for agent activation."""

    def __init__(self, bot, gui_controller):
        """Initialize onboarding commands."""
        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="soft_onboard", aliases=["soft"], description="Soft onboard agent(s)")
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def soft_onboard(self, ctx: commands.Context, *, agent_ids: str = None):
        """
        Soft onboard agent(s). Can specify single agent, multiple agents, or all.

        Usage:
        !soft Agent-1
        !soft Agent-1,Agent-2,Agent-3
        !soft all
        """
        self.logger.info(f"Command 'soft_onboard' triggered by {ctx.author} with agent_ids={agent_ids}")
        try:
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
    @commands.has_any_role("Admin", "Captain", "Swarm Commander")
    async def hard_onboard(self, ctx: commands.Context, *, agent_ids: str = None):
        """
        Hard onboard agent(s). Can specify single agent, multiple agents, or all.

        Usage:
        !hard_onboard Agent-1
        !hard_onboard Agent-1,Agent-2,Agent-3
        !hard_onboard all
        """
        self.logger.info(f"Command 'hard_onboard' triggered by {ctx.author} with agent_ids={agent_ids}")
        try:
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
            from src.services.hard_onboarding_service import hard_onboard_agent

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


