
from typing import TYPE_CHECKING


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

        commands.Cog.__init__(self)

        self.bot = bot
        self.gui_controller = gui_controller
        self.logger = logging.getLogger(__name__)

    @commands.command(name="mermaid", description="Render Mermaid diagram")

            diagram_code = self._clean_mermaid_code(diagram_code)

            embed = discord.Embed(
                title="📊 Mermaid Diagram",
                description="Mermaid diagram code:",
                color=discord.Color.blue(),
            )

            mermaid_block = f"```mermaid\n{diagram_code}\n```"


            if len(mermaid_block) > 1900:
                await ctx.send("❌ Mermaid diagram too long. Please shorten it.")
                return


            embed.add_field(name="Diagram Code", value=mermaid_block, inline=False)
            embed.set_footer(text="💡 Tip: Copy this code to a Mermaid editor or use Discord's code block rendering")
            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error rendering mermaid: {e}")
            await ctx.send(f"❌ Error rendering mermaid diagram: {e}")



            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error showing help: {e}")
            await ctx.send(f"❌ Error: {e}")



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

            embed.set_footer(text="🐝 WE. ARE. SWARM. ⚡ Buttons > Commands!")

            await ctx.send(embed=embed, view=control_view)
        except Exception as e:
            self.logger.error(f"Error listing commands: {e}")
            await ctx.send(f"❌ Error: {e}")



__all__ = ["UtilityCommands"]

