
"""
Technical Debt Commands - Main Entry Point (Modular V2 Compliance)
==================================================================

Main entry point for technical debt management commands.
Uses modular command handlers for maintainability.

V2 Compliant: <100 lines, modular architecture
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import logging
import discord
from discord.ext import commands


# Import modular command handlers
from .technical_debt_core import TechnicalDebtCoreCommands
from .debate_commands import DebateCommands


logger = logging.getLogger(__name__)


class TechnicalDebtCommands(commands.Cog):


    def __init__(self, bot):
        """Initialize technical debt commands with modular handlers."""
        commands.Cog.__init__(self)
        self.bot = bot
        self.logger = logging.getLogger(__name__)

        # Initialize modular command handlers
        self.debt_commands = TechnicalDebtCoreCommands(bot)
        self.debate_commands = DebateCommands(bot)

        self.logger.info("✅ Technical Debt Commands initialized with modular architecture")

    # Delegate commands to modular handlers
    @commands.command(name="technical_debt", aliases=["debt", "tech_debt"])
    async def technical_debt_status(self, ctx):
        """Delegate to core debt commands."""
        await self.debt_commands.technical_debt_status(ctx)

    @commands.command(name="debt_recommendations", aliases=["debt_rec"])
    async def debt_recommendations(self, ctx):
        """Delegate to core debt commands."""
        await self.debt_commands.debt_recommendations(ctx)

    @commands.command(name="debt_assign", aliases=["assign_debt"])
    async def assign_debt_task(self, ctx, category: str, agent_id: str):
        """Delegate to core debt commands."""
        await self.debt_commands.assign_debt_task(ctx, category, agent_id)

    @commands.command(name="debate", aliases=["create_debate"])
    async def create_debate(self, ctx, topic: str, duration_hours: int = 48):
        """Delegate to debate commands."""
        await self.debate_commands.create_debate(ctx, topic, duration_hours)

    @commands.command(name="debate_vote", aliases=["vote"])
    async def vote_in_debate(self, ctx, debate_id: str, option: str):
        """Delegate to debate commands."""
        await self.debate_commands.vote_in_debate(ctx, debate_id, option)

    @commands.command(name="debate_status", aliases=["debate_info", "debate_results"])
    async def debate_status(self, ctx, debate_id: str = None):
        """Delegate to debate commands."""
        await self.debate_commands.debate_status(ctx, debate_id)



__all__ = ["TechnicalDebtCommands"]

