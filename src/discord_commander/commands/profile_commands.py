
V2 Compliant: Modular profile commands
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-08

"""

import logging

try:
    import discord
    from discord.ext import commands
except ImportError:
    discord = None
    commands = None



            view = AriaProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !aria command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")

    @commands.command(name="carmyn", aliases=["carymn"], description="🌟 Display Carmyn's awesome profile!")

            from ..views.carmyn_profile_view import CarmynProfileView

            view = CarmynProfileView()
            embed = view._create_main_embed()
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error in !carmyn command: {e}", exc_info=True)
            await ctx.send(f"❌ Oops! Something went wrong: {e}")



__all__ = ["ProfileCommands"]

