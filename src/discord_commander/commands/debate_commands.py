#!/usr/bin/env python3
"""
Debate Commands - Modular V2 Compliance
========================================

<!-- SSOT Domain: integration -->

Debate and proposal system commands extracted from monolithic file.

V2 Compliant: Modular commands
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import logging
import discord
from discord.ext import commands
from datetime import datetime, timedelta
from typing import Dict

from .technical_debt_base import DebateBase

logger = logging.getLogger(__name__)


class DebateCommands(commands.Cog, DebateBase):
    """Debate and proposal system commands."""

    def __init__(self, bot):
        """Initialize debate commands."""
        DebateBase.__init__(self)
<<<<<<< HEAD
        super().__init__()
=======
        commands.Cog.__init__(self)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.bot = bot

    @commands.command(name="debate", aliases=["create_debate"])
    async def create_debate(self, ctx, topic: str, duration_hours: int = 48):
        """Create a new debate for democratic decision making."""
        try:
            # Parse topic and create structured debate
            debate_id = f"debate_{int(datetime.now().timestamp())}"

            # Create basic debate structure
            debate_data = {
                "debate_id": debate_id,
                "topic": topic,
                "description": f"Democratic debate on: {topic}",
                "created_by": str(ctx.author),
                "created": datetime.now().isoformat(),
                "deadline": (datetime.now() + timedelta(hours=duration_hours)).isoformat(),
                "duration_hours": duration_hours,
                "status": "active",
                "votes": {},
                "arguments": []
            }

            # Save debate
            self._save_debate(debate_data)
            self.active_debates[debate_id] = debate_data

            embed = discord.Embed(
                title="🗳️ Debate Created",
                description=f"**Topic:** {topic}",
                color=0x3498DB,  # Blue
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="⏰ Duration",
                value=f"{duration_hours} hours",
                inline=True
            )

            embed.add_field(
                name="🎯 Status",
                value="ACTIVE - Open for arguments and voting",
                inline=True
            )

            embed.add_field(
                name="📋 How to Participate",
                value="• `!debate_vote <debate_id> <option>` - Cast your vote\n• `!debate_argue <debate_id> <argument>` - Add argument\n• `!debate_status <debate_id>` - View current status",
                inline=False
            )

            embed.set_footer(text=f"Created by {ctx.author} • Debate ID: {debate_id}")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error creating debate: {e}")
            await ctx.send(f"❌ Error creating debate: {e}")

    @commands.command(name="debate_vote", aliases=["vote"])
    async def vote_in_debate(self, ctx, debate_id: str, option: str):
        """Vote in an active debate."""
        try:
            if debate_id not in self.active_debates:
                return await ctx.send(f"❌ Debate '{debate_id}' not found or expired.")

            debate = self.active_debates[debate_id]

            # Check if debate has expired
            deadline = datetime.fromisoformat(debate["deadline"].replace('Z', '+00:00'))
            if datetime.now().replace(tzinfo=deadline.tzinfo) > deadline:
                return await ctx.send(f"❌ Debate '{debate_id}' has expired.")

            # Record vote
            voter_id = str(ctx.author)
            if "votes" not in debate:
                debate["votes"] = {}

            debate["votes"][voter_id] = {
                "option": option,
                "timestamp": datetime.now().isoformat(),
                "voter": str(ctx.author)
            }

            # Save updated debate
            self._save_debate(debate)

            embed = discord.Embed(
                title="✅ Vote Recorded",
                color=0x00FF00,  # Green
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="🗳️ Debate",
                value=debate.get("topic", debate_id),
                inline=True
            )

            embed.add_field(
                name="🎯 Your Vote",
                value=f"**{option}**",
                inline=True
            )

            embed.set_footer(text=f"Voted by {ctx.author}")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error voting in debate: {e}")
            await ctx.send(f"❌ Error recording vote: {e}")

    @commands.command(name="debate_status", aliases=["debate_info", "debate_results"])
    async def debate_status(self, ctx, debate_id: str = None):
        """View status and results of debates."""
        try:
            if debate_id:
                # Show specific debate
                if debate_id not in self.active_debates:
                    return await ctx.send(f"❌ Debate '{debate_id}' not found.")

                debate = self.active_debates[debate_id]
                await self._show_debate_details(ctx, debate)
            else:
                # Show all active debates
                if not self.active_debates:
                    return await ctx.send("📭 No active debates currently.")

                embed = discord.Embed(
                    title="🗳️ Active Debates",
                    description=f"**{len(self.active_debates)} active debates**",
                    color=0x3498DB,  # Blue
                    timestamp=ctx.message.created_at
                )

                for debate_id, debate in list(self.active_debates.items())[:5]:  # Limit to 5
                    deadline = datetime.fromisoformat(debate["deadline"].replace('Z', '+00:00'))
                    time_left = deadline - datetime.now().replace(tzinfo=deadline.tzinfo)
                    hours_left = max(0, int(time_left.total_seconds() / 3600))

                    votes_count = len(debate.get("votes", {}))
                    args_count = len(debate.get("arguments", []))

                    embed.add_field(
                        name=f"📋 {debate.get('topic', debate_id)[:50]}",
                        value=f"⏰ {hours_left}h left • 🗳️ {votes_count} votes • 💬 {args_count} arguments\n`!debate_status {debate_id}`",
                        inline=False
                    )

                embed.set_footer(text="Use !debate_status <debate_id> for detailed view")

                await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error showing debate status: {e}")
            await ctx.send(f"❌ Error retrieving debate status: {e}")

    async def _show_debate_details(self, ctx, debate: Dict):
        """Show detailed view of a specific debate."""
        try:
            debate_id = debate.get("debate_id", "unknown")
            topic = debate.get("topic", "Unknown Topic")

            # Calculate time remaining
            deadline = datetime.fromisoformat(debate["deadline"].replace('Z', '+00:00'))
            time_left = deadline - datetime.now().replace(tzinfo=deadline.tzinfo)
            hours_left = max(0, int(time_left.total_seconds() / 3600))

            embed = discord.Embed(
                title=f"🗳️ Debate: {topic}",
                description=f"**ID:** {debate_id}",
                color=0x3498DB,  # Blue
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="⏰ Time Remaining",
                value=f"{hours_left} hours",
                inline=True
            )

            # Vote breakdown
            votes = debate.get("votes", {})
            vote_counts = {}
            for vote_data in votes.values():
                option = vote_data.get("option", "unknown")
                vote_counts[option] = vote_counts.get(option, 0) + 1

            vote_summary = "\n".join([f"• **{option}**: {count} votes" for option, count in vote_counts.items()])
            if not vote_summary:
                vote_summary = "No votes yet"

            embed.add_field(
                name=f"🗳️ Votes ({len(votes)} total)",
                value=vote_summary,
                inline=True
            )

            embed.set_footer(text=f"Created by {debate.get('created_by', 'Unknown')} • Use !debate_vote {debate_id} <option> to vote")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error showing debate details: {e}")
            await ctx.send(f"❌ Error showing debate details: {e}")


__all__ = ["DebateCommands"]