#!/usr/bin/env python3
"""
Technical Debt Core Commands - Modular V2 Compliance
====================================================

<!-- SSOT Domain: integration -->

Core technical debt management commands extracted from monolithic file.

V2 Compliant: Modular commands
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08
"""

import logging
import discord
from discord.ext import commands

from .technical_debt_base import TechnicalDebtBase

logger = logging.getLogger(__name__)


class TechnicalDebtCoreCommands(commands.Cog, TechnicalDebtBase):
    """Core technical debt management commands."""

    def __init__(self, bot):
        """Initialize technical debt core commands."""
        TechnicalDebtBase.__init__(self)
<<<<<<< HEAD
        super().__init__()
=======
        commands.Cog.__init__(self)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
        self.bot = bot

    @commands.command(name="technical_debt", aliases=["debt", "tech_debt"])
    async def technical_debt_status(self, ctx):
        """Get current technical debt status with full system integration."""
        if not self._check_orchestrator_available():
            return await ctx.send("❌ Technical Debt system not available.")

        try:
            # Get comprehensive system status
            system_status = self.debt_orchestrator.get_system_status()

            if system_status.get("status") == "error":
                return await ctx.send(f"❌ Error retrieving debt status: {system_status.get('error')}")

            debt_summary = system_status.get("debt_summary", {})
            agent_availability = system_status.get("agent_availability", {})
            audit_compliance = system_status.get("audit_compliance", {})
            recommendations = system_status.get("assignment_recommendations", {})

            # Create embed
            embed = discord.Embed(
                title="🔧 Technical Debt Status - Integrated System",
                color=0xFFA500,  # Orange
                timestamp=ctx.message.created_at
            )

            # Debt Summary
            total_pending = debt_summary.get("total_pending_tasks", 0)
            total_resolved = debt_summary.get("total_resolved_tasks", 0)

            embed.add_field(
                name="📊 Overall Status",
                value=f"**Pending:** {total_pending}\n**Resolved:** {total_resolved}\n**Available Agents:** {agent_availability.get('total_available', 0)}",
                inline=True
            )

            # Categories breakdown
            categories = debt_summary.get("categories", {})
            if categories:
                category_text = ""
                for cat_name, cat_data in list(categories.items())[:6]:  # Limit to 6 for Discord
                    pending = cat_data.get("pending", 0)
                    resolved = cat_data.get("resolved", 0)
                    if pending > 0:
                        category_text += f"• {cat_name.replace('_', ' ').title()}: {pending} pending\n"

                if category_text:
                    embed.add_field(
                        name="📋 Active Categories",
                        value=category_text[:1024],  # Discord field limit
                        inline=True
                    )

            # System Health
            compliance = "✅ Compliant" if audit_compliance.get("overall_compliance") else "⚠️ Needs Attention"
            embed.add_field(
                name="🏥 System Health",
                value=f"**Audit Status:** {compliance}\n**Last Updated:** {debt_summary.get('last_updated', 'Unknown')[:19]}",
                inline=False
            )

            # Recommendations
            rec_count = recommendations.get("recommended_count", 0)
            if rec_count > 0:
                embed.add_field(
                    name="💡 Recommendations",
                    value=f"{rec_count} task assignments available\nUse `!debt_recommendations` for details",
                    inline=False
                )

            embed.set_footer(text="🔗 Connected to Agent Status Monitor, Master Task Log & Audit Trail")

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error getting technical debt status: {e}")
            await ctx.send(f"❌ Error retrieving technical debt status: {e}")

    @commands.command(name="debt_recommendations", aliases=["debt_rec"])
    async def debt_recommendations(self, ctx):
        """Get intelligent task assignment recommendations."""
        if not self._check_orchestrator_available():
            return await ctx.send("❌ Technical Debt system not available.")

        try:
            recommendations = self.debt_orchestrator.agent_integration.get_assignment_recommendations()

            if recommendations.get("status") != "success":
                return await ctx.send(f"❌ Error getting recommendations: {recommendations.get('message')}")

            recs = recommendations.get("recommendations", [])

            embed = discord.Embed(
                title="🎯 Debt Task Assignment Recommendations",
                description=f"**{len(recs)} intelligent recommendations available**",
                color=0x3498DB,  # Blue
                timestamp=ctx.message.created_at
            )

            if recs:
                rec_text = ""
                for i, rec in enumerate(recs[:5], 1):  # Limit to 5 for readability
                    task = rec.get("task", {})
                    agent = rec.get("recommended_agent", "Unknown")
                    reason = rec.get("reasoning", "Based on capabilities match")

                    rec_text += f"**{i}.** {task.get('title', 'Unknown Task')}\n"
                    rec_text += f"   → Assign to: `{agent}`\n"
                    rec_text += f"   → Reason: {reason}\n\n"

                embed.add_field(
                    name="📋 Top Recommendations",
                    value=rec_text[:1024],
                    inline=False
                )

                embed.add_field(
                    name="⚡ Quick Assign",
                    value="Use `!debt_assign <category> <agent>` to manually assign tasks",
                    inline=False
                )
            else:
                embed.add_field(
                    name="ℹ️ No Recommendations",
                    value="All pending tasks are either assigned or no suitable agents are available.",
                    inline=False
                )

            await ctx.send(embed=embed)

        except Exception as e:
            logger.error(f"Error getting debt recommendations: {e}")
            await ctx.send(f"❌ Error retrieving recommendations: {e}")

    @commands.command(name="debt_assign", aliases=["assign_debt"])
    async def assign_debt_task(self, ctx, category: str, agent_id: str):
        """Manually assign a debt task category to a specific agent."""
        if not self._check_orchestrator_available():
            return await ctx.send("❌ Technical Debt system not available.")

        try:
            result = self.debt_orchestrator.assign_specific_debt_task(category, agent_id)

            if result.get("status") == "assigned":
                assignment = result.get("assignment", {})
                task = assignment.get("task", {})

                embed = discord.Embed(
                    title="✅ Debt Task Assigned",
                    color=0x00FF00,  # Green
                    timestamp=ctx.message.created_at
                )

                embed.add_field(
                    name="📋 Task Details",
                    value=f"**Category:** {category}\n**Priority:** {task.get('priority', 'Unknown')}\n**Items:** {task.get('pending_count', 0)}",
                    inline=True
                )

                embed.add_field(
                    name="👤 Assignment",
                    value=f"**Agent:** {agent_id}\n**Timestamp:** {assignment.get('timestamp', 'Unknown')[:19]}\n**Audit Logged:** {'✅' if result.get('audit_logged') else '❌'}",
                    inline=True
                )

                embed.set_footer(text=f"Assigned by {ctx.author}")

                await ctx.send(embed=embed)

            elif result.get("status") == "agent_unavailable":
                await ctx.send(f"❌ Agent {agent_id} is not available for task assignment. Check `!technical_debt` for available agents.")

            else:
                await ctx.send(f"❌ Assignment failed: {result.get('message')}")

        except Exception as e:
            logger.error(f"Error assigning debt task: {e}")
            await ctx.send(f"❌ Error assigning task: {e}")


__all__ = ["TechnicalDebtCoreCommands"]