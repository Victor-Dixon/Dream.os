"""
Technical Debt Commands - V2 Compliant
======================================

Discord commands for technical debt management and monitoring.

Integrates with:
- Agent Status Monitor (intelligent task assignment)
- Master Task Log (task visibility)
- Audit Trail (compliance tracking)

<!-- SSOT Domain: integration -->
"""

import logging
from pathlib import Path

import discord
from discord.ext import commands

# Technical Debt Integration
import sys
from pathlib import Path as PathLib
project_root = PathLib(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

# Debate System Integration
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class TechnicalDebtCommands(commands.Cog):
    """Technical debt management commands with full system integration."""

    def __init__(self, bot):
        """Initialize technical debt commands."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)

        # Initialize Technical Debt Integration Orchestrator
        try:
            from systems.technical_debt.integration.orchestrator import TechnicalDebtIntegrationOrchestrator
            self.debt_orchestrator = TechnicalDebtIntegrationOrchestrator()
            self.logger.info("✅ Technical Debt Integration Orchestrator initialized")
        except ImportError as e:
            self.logger.warning(f"⚠️ Technical Debt integration not available: {e}")
            self.debt_orchestrator = None

        # Initialize Debate System
        self.debates_dir = Path(__file__).resolve().parents[4] / "debates"
        self.debates_dir.mkdir(exist_ok=True)
        self.active_debates: Dict[str, Dict] = {}
        self._load_active_debates()

    @commands.command(name="technical_debt", aliases=["debt", "tech_debt"])
    async def technical_debt_status(self, ctx):
        """Get current technical debt status with full system integration."""
        if not self.debt_orchestrator:
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
            self.logger.error(f"Error getting technical debt status: {e}")
            await ctx.send(f"❌ Error retrieving technical debt status: {e}")

    @commands.command(name="debt_recommendations", aliases=["debt_rec"])
    async def debt_recommendations(self, ctx):
        """Get intelligent task assignment recommendations."""
        if not self.debt_orchestrator:
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
            self.logger.error(f"Error getting debt recommendations: {e}")
            await ctx.send(f"❌ Error retrieving recommendations: {e}")

    @commands.command(name="debt_assign", aliases=["assign_debt"])
    async def assign_debt_task(self, ctx, category: str, agent_id: str):
        """Manually assign a debt task category to a specific agent."""
        if not self.debt_orchestrator:
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
            self.logger.error(f"Error assigning debt task: {e}")
            await ctx.send(f"❌ Error assigning task: {e}")

    @commands.command(name="debt_sync", aliases=["sync_debt"])
    async def sync_debt_system(self, ctx):
        """Synchronize technical debt system with all integrations."""
        if not self.debt_orchestrator:
            return await ctx.send("❌ Technical Debt system not available.")

        try:
            embed = discord.Embed(
                title="🔄 Synchronizing Technical Debt System",
                description="Running full integration cycle...",
                color=0x3498DB,  # Blue
            )
            message = await ctx.send(embed=embed)

            # Run full integration cycle
            results = self.debt_orchestrator.run_full_integration_cycle()

            # Update embed with results
            if results.get("overall_status") == "completed":
                embed.color = 0x00FF00  # Green
                embed.title = "✅ Technical Debt System Synchronized"

                steps = results.get("steps", {})

                # Task sync results
                task_sync = steps.get("task_sync", {})
                embed.add_field(
                    name="📋 Master Task Log",
                    value=f"Added: {task_sync.get('tasks_added', 0)}\nUpdated: {task_sync.get('tasks_updated', 0)}\nRemoved: {task_sync.get('tasks_removed', 0)}",
                    inline=True
                )

                # Assignment results
                assignment = steps.get("task_assignment", {})
                embed.add_field(
                    name="🤖 Task Assignments",
                    value=f"Assigned: {assignment.get('assigned_count', 0)}\nUnassigned: {len(assignment.get('unassigned_tasks', []))}",
                    inline=True
                )

                # Audit results
                audit = steps.get("audit_logging", {})
                embed.add_field(
                    name="📊 Audit Trail",
                    value=f"Audited: {audit.get('assignments_audited', 0)}\nSuccess Rate: {audit.get('audit_success_rate', 0):.1%}",
                    inline=True
                )

                embed.add_field(
                    name="⏱️ Cycle Time",
                    value=f"Started: {results.get('cycle_start', 'Unknown')[:19]}\nCompleted: {results.get('cycle_end', 'Unknown')[:19]}",
                    inline=False
                )

            else:
                embed.color = 0xFF0000  # Red
                embed.title = "❌ Synchronization Failed"
                embed.add_field(
                    name="Error",
                    value=results.get("error", "Unknown error occurred"),
                    inline=False
                )

            await message.edit(embed=embed)

        except Exception as e:
            self.logger.error(f"Error syncing debt system: {e}")
            embed = discord.Embed(
                title="❌ Synchronization Failed",
                description=f"Error: {e}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

    @commands.command(name="debt_audit", aliases=["audit_debt"])
    async def debt_audit_status(self, ctx):
        """Check technical debt audit compliance and history."""
        if not self.debt_orchestrator:
            return await ctx.send("❌ Technical Debt system not available.")

        try:
            audit_history = self.debt_orchestrator.audit_integration.get_debt_audit_history(days=7)

            if audit_history.get("status") != "success":
                return await ctx.send(f"❌ Error retrieving audit history: {audit_history.get('message')}")

            summary = audit_history.get("summary", {})
            events = audit_history.get("events", [])

            embed = discord.Embed(
                title="📊 Technical Debt Audit Trail",
                description=f"**Last 7 days activity**",
                color=0x9B59B6,  # Purple
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="📈 Activity Summary",
                value=f"**Total Events:** {summary.get('total_events', 0)}\n**Time Range:** {summary.get('time_range', {}).get('start', 'Unknown')[:10]} to {summary.get('time_range', {}).get('end', 'Unknown')[:10]}",
                inline=False
            )

            # Event type breakdown
            event_types = summary.get("event_types", {})
            if event_types:
                type_text = ""
                for event_type, count in event_types.items():
                    type_text += f"• {event_type}: {count}\n"
                embed.add_field(
                    name="🔍 Event Types",
                    value=type_text,
                    inline=True
                )

            # Recent events
            if events:
                recent_text = ""
                for event in events[-3:]:  # Last 3 events
                    recent_text += f"• {event.get('timestamp', 'Unknown')[:19]}: {event.get('summary', 'Unknown')}\n"
                embed.add_field(
                    name="🕐 Recent Activity",
                    value=recent_text,
                    inline=True
                )

            embed.set_footer(text="🔗 Full audit trail available in system logs")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error getting debt audit status: {e}")
            await ctx.send(f"❌ Error retrieving audit status: {e}")

    @commands.command(name="debt_report", aliases=["debt_weekly"])
    async def generate_debt_report(self, ctx, report_type: str = "comprehensive"):
        """Generate a comprehensive technical debt report."""
        if not self.debt_orchestrator:
            return await ctx.send("❌ Technical Debt system not available.")

        try:
            embed = discord.Embed(
                title="📋 Generating Technical Debt Report",
                description=f"Creating {report_type} report...",
                color=0x3498DB,  # Blue
            )
            message = await ctx.send(embed=embed)

            # Generate integrated report
            report = self.debt_orchestrator.generate_integrated_report(report_type)

            if report.get("status") == "error":
                embed.color = 0xFF0000  # Red
                embed.title = "❌ Report Generation Failed"
                embed.description = f"Error: {report.get('error')}"
                await message.edit(embed=embed)
                return

            # Create summary embed
            embed.color = 0x00FF00  # Green
            embed.title = f"✅ {report_type.title()} Technical Debt Report Generated"

            summary = report.get("sections", {}).get("executive_summary", {})
            embed.add_field(
                name="📊 Executive Summary",
                value=f"**Total Debt:** {summary.get('total_debt_items', 0)}\n**Resolved:** {summary.get('resolved_items', 0)}\n**Available Agents:** {summary.get('available_agents', 0)}",
                inline=True
            )

            audit_compliance = summary.get('audit_compliance', False)
            recommendations = summary.get('assignment_recommendations', 0)
            embed.add_field(
                name="🏥 System Health",
                value=f"**Audit Compliant:** {'✅' if audit_compliance else '❌'}\n**Recommendations:** {recommendations}",
                inline=True
            )

            embed.add_field(
                name="📅 Generated",
                value=f"{report.get('generated_at', 'Unknown')[:19]}\n**Audit Logged:** {'✅' if report.get('audit_logged') else '❌'}",
                inline=False
            )

            embed.set_footer(text="🔗 Full report available in systems/technical_debt/reports/")

            await message.edit(embed=embed)

        except Exception as e:
            self.logger.error(f"Error generating debt report: {e}")
            embed = discord.Embed(
                title="❌ Report Generation Failed",
                description=f"Error: {e}",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

    # ===== DEBATE SYSTEM INTEGRATION =====

    def __init__(self, bot):
        """Initialize technical debt commands."""
        self.bot = bot
        self.logger = logging.getLogger(__name__)

        # Initialize Technical Debt Integration Orchestrator
        try:
            from systems.technical_debt.integration.orchestrator import TechnicalDebtIntegrationOrchestrator
            self.debt_orchestrator = TechnicalDebtIntegrationOrchestrator()
            self.logger.info("✅ Technical Debt Integration Orchestrator initialized")
        except ImportError as e:
            self.logger.warning(f"⚠️ Technical Debt integration not available: {e}")
            self.debt_orchestrator = None

        # Initialize Debate System
        self.debates_dir = Path(__file__).resolve().parents[4] / "debates"
        self.debates_dir.mkdir(exist_ok=True)
        self.active_debates: Dict[str, Dict] = {}
        self._load_active_debates()

    def _load_active_debates(self):
        """Load active debates from files."""
        try:
            for debate_file in self.debates_dir.glob("*.json"):
                try:
                    with open(debate_file, 'r', encoding='utf-8') as f:
                        debate_data = json.load(f)

                    debate_id = debate_data.get("debate_id")
                    deadline = debate_data.get("deadline")

                    # Check if debate is still active
                    if deadline:
                        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                        if datetime.now().replace(tzinfo=deadline_dt.tzinfo) < deadline_dt:
                            self.active_debates[debate_id] = debate_data

                except Exception as e:
                    self.logger.warning(f"Failed to load debate {debate_file}: {e}")

            self.logger.info(f"Loaded {len(self.active_debates)} active debates")

        except Exception as e:
            self.logger.error(f"Error loading active debates: {e}")

    def _save_debate(self, debate_data: Dict):
        """Save debate data to file."""
        try:
            debate_id = debate_data["debate_id"]
            debate_file = self.debates_dir / f"{debate_id}.json"

            with open(debate_file, 'w', encoding='utf-8') as f:
                json.dump(debate_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            self.logger.error(f"Error saving debate {debate_data.get('debate_id')}: {e}")

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
            self.logger.error(f"Error creating debate: {e}")
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
            self.logger.error(f"Error voting in debate: {e}")
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
            self.logger.error(f"Error showing debate status: {e}")
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

            # Recent arguments
            arguments = debate.get("arguments", [])
            if arguments:
                recent_args = []
                for arg in arguments[-3:]:  # Last 3 arguments
                    author = arg.get("author", "Unknown")[:20]
                    content = arg.get("content", "")[:100]
                    recent_args.append(f"**{author}**: {content}{'...' if len(content) > 100 else ''}")

                args_text = "\n".join(recent_args)
                embed.add_field(
                    name=f"💬 Recent Arguments ({len(arguments)} total)",
                    value=args_text,
                    inline=False
                )

            embed.set_footer(text=f"Created by {debate.get('created_by', 'Unknown')} • Use !debate_vote {debate_id} <option> to vote")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error showing debate details: {e}")
            await ctx.send(f"❌ Error showing debate details: {e}")

    # ===== SWARM PROPOSALS SYSTEM INTEGRATION =====

    @commands.command(name="propose", aliases=["create_proposal", "proposal"])
    async def create_proposal(self, ctx, topic: str, title: str, *, content: str):
        """Create a new proposal in the swarm proposals system."""
        try:
            # Create proposal structure
            proposal_id = f"proposal_{int(datetime.now().timestamp())}"
            proposal_dir = self.debates_dir.parent / "swarm_proposals" / topic
            proposal_dir.mkdir(parents=True, exist_ok=True)

            proposal_data = f"""# {title}

**Author:** {ctx.author}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Topic:** {topic}
**Proposal ID:** {proposal_id}

---

## Problem Statement

{content}

---

## Proposed Solution

[To be filled by proposal author]

## Benefits

- [Benefit 1]
- [Benefit 2]

## Implementation Plan

1. [Step 1]
2. [Step 2]

## Success Criteria

- [Criteria 1]
- [Criteria 2]
"""

            # Save proposal
            proposal_file = proposal_dir / f"{proposal_id}_{title.lower().replace(' ', '_')}.md"
            with open(proposal_file, 'w', encoding='utf-8') as f:
                f.write(proposal_data)

            embed = discord.Embed(
                title="📝 Proposal Created",
                description=f"**{title}**",
                color=0x2ECC71,  # Green
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="📂 Topic",
                value=topic,
                inline=True
            )

            embed.add_field(
                name="👤 Author",
                value=str(ctx.author),
                inline=True
            )

            embed.add_field(
                name="📋 Next Steps",
                value="• Edit proposal with full solution details\n• Use `!debate` to start community discussion\n• Community voting determines implementation",
                inline=False
            )

            embed.set_footer(text=f"Proposal ID: {proposal_id}")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error creating proposal: {e}")
            await ctx.send(f"❌ Error creating proposal: {e}")

    @commands.command(name="proposals", aliases=["list_proposals", "show_proposals"])
    async def list_proposals(self, ctx, topic: str = None):
        """List proposals in the swarm proposals system."""
        try:
            proposals_dir = self.debates_dir.parent / "swarm_proposals"

            if not proposals_dir.exists():
                return await ctx.send("📭 No proposals found. Create your first with `!propose <topic> <title> <content>`")

            embed = discord.Embed(
                title="📋 Swarm Proposals",
                description="Democratic solution development system",
                color=0x3498DB,  # Blue
                timestamp=ctx.message.created_at
            )

            total_proposals = 0

            if topic:
                # Show proposals for specific topic
                topic_dir = proposals_dir / topic
                if topic_dir.exists():
                    proposal_files = list(topic_dir.glob("*.md"))
                    if proposal_files:
                        proposal_list = []
                        for proposal_file in proposal_files[:5]:  # Limit to 5
                            try:
                                with open(proposal_file, 'r', encoding='utf-8') as f:
                                    lines = f.readlines()
                                    title = lines[0].strip('# ').strip() if lines else "Unknown Title"
                                    author_line = [line for line in lines if "**Author:**" in line]
                                    author = author_line[0].split("**Author:**")[1].strip() if author_line else "Unknown"

                                proposal_list.append(f"• **{title}**\n  _{author}_")
                            except Exception:
                                proposal_list.append(f"• {proposal_file.stem}")

                        embed.add_field(
                            name=f"📂 {topic}",
                            value="\n\n".join(proposal_list),
                            inline=False
                        )
                        total_proposals = len(proposal_files)
                    else:
                        embed.add_field(
                            name=f"📂 {topic}",
                            value="No proposals in this topic yet.",
                            inline=False
                        )
                else:
                    embed.add_field(
                        name=f"📂 {topic}",
                        value="Topic not found.",
                        inline=False
                    )
            else:
                # Show all topics
                topics = [d for d in proposals_dir.iterdir() if d.is_dir()]
                if topics:
                    topic_summary = []
                    for topic_dir in topics[:5]:  # Limit to 5 topics
                        proposal_count = len(list(topic_dir.glob("*.md")))
                        total_proposals += proposal_count
                        topic_summary.append(f"• **{topic_dir.name}**: {proposal_count} proposals")

                    embed.add_field(
                        name="📂 Topics",
                        value="\n".join(topic_summary),
                        inline=False
                    )
                else:
                    embed.add_field(
                        name="📭 No Topics",
                        value="No proposal topics exist yet.",
                        inline=False
                    )

            embed.add_field(
                name="📊 Statistics",
                value=f"**Total Proposals:** {total_proposals}",
                inline=True
            )

            embed.set_footer(text="Use !propose <topic> <title> <content> to create new proposals")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error listing proposals: {e}")
            await ctx.send(f"❌ Error listing proposals: {e}")

    @commands.command(name="view_proposal", aliases=["read_proposal", "proposal_view"])
    async def view_proposal(self, ctx, topic: str, proposal_id: str):
        """View the content of a specific proposal."""
        try:
            proposals_dir = self.debates_dir.parent / "swarm_proposals" / topic

            if not proposals_dir.exists():
                return await ctx.send(f"❌ Topic '{topic}' not found.")

            # Find proposal file
            proposal_files = list(proposals_dir.glob(f"*{proposal_id}*.md"))

            if not proposal_files:
                return await ctx.send(f"❌ Proposal '{proposal_id}' not found in topic '{topic}'.")

            proposal_file = proposal_files[0]

            # Read proposal content
            with open(proposal_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract key sections for embed
            lines = content.split('\n')
            title = lines[0].strip('# ').strip() if lines else "Unknown Title"

            # Find author
            author_line = [line for line in lines if "**Author:**" in line]
            author = author_line[0].split("**Author:**")[1].strip() if author_line else "Unknown"

            # Find problem statement
            problem_start = -1
            for i, line in enumerate(lines):
                if "## Problem Statement" in line:
                    problem_start = i + 1
                    break

            problem_text = ""
            if problem_start > 0:
                for line in lines[problem_start:]:
                    if line.strip() and not line.startswith("##"):
                        problem_text += line + "\n"
                    elif line.startswith("##"):
                        break
                problem_text = problem_text.strip()[:500]  # Limit length

            embed = discord.Embed(
                title=f"📄 {title}",
                color=0x9B59B6,  # Purple
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="👤 Author",
                value=author,
                inline=True
            )

            embed.add_field(
                name="📂 Topic",
                value=topic,
                inline=True
            )

            if problem_text:
                embed.add_field(
                    name="🎯 Problem Statement",
                    value=problem_text + ("..." if len(problem_text) > 500 else ""),
                    inline=False
                )

            embed.set_footer(text=f"Proposal ID: {proposal_id} • Use !proposals {topic} to see all proposals in this topic")

            await ctx.send(embed=embed)

            # Send full content as file attachment for detailed reading
            from io import StringIO
            file_obj = StringIO(content)
            file_obj.seek(0)

            await ctx.send(file=discord.File(file_obj, f"{proposal_id}.md"))

        except Exception as e:
            self.logger.error(f"Error viewing proposal: {e}")
            await ctx.send(f"❌ Error viewing proposal: {e}")

    @commands.command(name="debate_proposal", aliases=["debate_prop"])
    async def debate_proposal(self, ctx, topic: str, proposal_id: str, duration_hours: int = 72):
        """Start a debate on a specific proposal."""
        try:
            # Check if proposal exists
            proposals_dir = self.debates_dir.parent / "swarm_proposals" / topic
            proposal_files = list(proposals_dir.glob(f"*{proposal_id}*.md"))

            if not proposal_files:
                return await ctx.send(f"❌ Proposal '{proposal_id}' not found in topic '{topic}'.")

            # Read proposal to get title
            with open(proposal_files[0], 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[0].strip('# ').strip() if lines else f"Proposal {proposal_id}"

            # Create debate topic
            debate_topic = f"Should we implement: {title}?"

            # Use existing debate creation
            await self.create_debate(ctx, debate_topic, duration_hours)

            # Add context about the proposal
            embed = discord.Embed(
                title="🔗 Proposal Debate Started",
                description=f"Debate created for proposal: **{title}**",
                color=0xE67E22,  # Orange
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="📋 Related Proposal",
                value=f"Topic: {topic}\nProposal ID: {proposal_id}\n\nUse `!view_proposal {topic} {proposal_id}` to read the full proposal.",
                inline=False
            )

            embed.add_field(
                name="🗳️ Voting Options",
                value="• **Yes** - Implement this proposal\n• **No** - Do not implement\n• **Modify** - Implement with changes\n• **Alternative** - Pursue different approach",
                inline=False
            )

            embed.set_footer(text=f"Started by {ctx.author}")

            await ctx.send(embed=embed)

        except Exception as e:
            self.logger.error(f"Error starting proposal debate: {e}")
            await ctx.send(f"❌ Error starting proposal debate: {e}")

    @commands.command(name="implement_proposal", aliases=["adopt_proposal"])
    @commands.has_permissions(administrator=True)
    async def implement_proposal(self, ctx, topic: str, proposal_id: str):
        """Mark a proposal as accepted for implementation (Admin only)."""
        try:
            # Check if proposal exists
            proposals_dir = self.debates_dir.parent / "swarm_proposals" / topic
            proposal_files = list(proposals_dir.glob(f"*{proposal_id}*.md"))

            if not proposal_files:
                return await ctx.send(f"❌ Proposal '{proposal_id}' not found in topic '{topic}'.")

            # Read proposal to get title
            with open(proposal_files[0], 'r', encoding='utf-8') as f:
                lines = f.readlines()
                title = lines[0].strip('# ').strip() if lines else f"Proposal {proposal_id}"

            embed = discord.Embed(
                title="🎉 Proposal Adopted for Implementation",
                description=f"**{title}**",
                color=0x27AE60,  # Dark Green
                timestamp=ctx.message.created_at
            )

            embed.add_field(
                name="📂 Topic",
                value=topic,
                inline=True
            )

            embed.add_field(
                name="🆔 Proposal ID",
                value=proposal_id,
                inline=True
            )

            embed.add_field(
                name="👑 Adopted By",
                value=str(ctx.author),
                inline=True
            )

            embed.add_field(
                name="📋 Next Steps",
                value="• Implementation plan to be created\n• Tasks added to MASTER_TASK_LOG.md\n• Development team assigned\n• Progress tracking begins",
                inline=False
            )

            embed.set_footer(text="This proposal has been democratically approved and will be implemented")

            await ctx.send(embed=embed)

            # Task creation integration implemented
            await self._create_technical_debt_tasks(proposal_data)

        except Exception as e:
            self.logger.error(f"Error adopting proposal: {e}")
            await ctx.send(f"❌ Error adopting proposal: {e}")

    async def _create_technical_debt_tasks(self, proposal_data: dict):
        """
        Create tasks in MASTER_TASK_LOG.md for adopted technical debt proposals.

        Args:
            proposal_data: Dictionary containing proposal information including:
                - title: Proposal title
                - description: Proposal description
                - priority: HIGH/MEDIUM/LOW
                - estimated_effort: Implementation effort estimate
                - proposed_by: Agent who proposed it
        """
        try:
            # Calculate point value based on priority and effort
            priority = proposal_data.get('priority', 'MEDIUM')
            effort = proposal_data.get('estimated_effort', 'medium')

            # Point calculation logic
            base_points = {'HIGH': 75, 'MEDIUM': 50, 'LOW': 25}
            effort_multiplier = {'small': 0.8, 'medium': 1.0, 'large': 1.2}

            points = int(base_points.get(priority, 50) * effort_multiplier.get(effort, 1.0))

            # Format task description
            task_title = proposal_data.get('title', 'Technical Debt Implementation')
            task_description = f"**{priority.upper()}** ({points} pts): {task_title}"

            # Add implementation context
            task_description += f" - Implement technical debt proposal: {proposal_data.get('description', '')[:100]}..."

            # Add agent assignment if available
            proposed_by = proposal_data.get('proposed_by')
            if proposed_by:
                task_description += f" [{proposed_by}]"

            # Create the task entry
            task_entry = f"- [ ] {task_description}\n"

            # Read current MASTER_TASK_LOG.md
            master_task_log_path = Path("MASTER_TASK_LOG.md")
            if not master_task_log_path.exists():
                self.logger.error("MASTER_TASK_LOG.md not found")
                return

            # Read the current content
            with open(master_task_log_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Find the INBOX section and add the task
            inbox_marker = "## 📥 INBOX"
            if inbox_marker in content:
                # Split content at INBOX section
                parts = content.split(inbox_marker, 1)
                if len(parts) == 2:
                    # Insert task at the beginning of INBOX section
                    updated_content = parts[0] + inbox_marker + "\n\n" + task_entry + parts[1]

                    # Write back to file
                    with open(master_task_log_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)

                    self.logger.info(f"✅ Added technical debt task to MASTER_TASK_LOG.md: {task_title}")
                else:
                    self.logger.error("Could not parse MASTER_TASK_LOG.md structure")
            else:
                self.logger.error("INBOX section not found in MASTER_TASK_LOG.md")

        except Exception as e:
            self.logger.error(f"Error creating technical debt tasks: {e}")
            # Don't raise exception - task creation failure shouldn't break proposal adoption