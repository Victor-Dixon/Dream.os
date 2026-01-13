<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python3
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
=======
=======
#!/usr/bin/env python3
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
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

<<<<<<< HEAD
# Technical Debt Integration
import sys
from pathlib import Path as PathLib
project_root = PathLib(__file__).resolve().parents[4]
sys.path.insert(0, str(project_root))

# Debate System Integration
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
# Import modular command handlers
from .technical_debt_core import TechnicalDebtCoreCommands
from .debate_commands import DebateCommands
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

logger = logging.getLogger(__name__)


class TechnicalDebtCommands(commands.Cog):
<<<<<<< HEAD
<<<<<<< HEAD
    """Main technical debt commands cog that includes all modular handlers."""

    def __init__(self, bot):
        """Initialize technical debt commands with modular handlers."""
        super().__init__()
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
=======
    """Technical debt management commands with full system integration."""
=======
    """Main technical debt commands cog that includes all modular handlers."""
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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


<<<<<<< HEAD
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

            # TODO: Integration with task creation system
            # This would automatically create tasks in MASTER_TASK_LOG.md

        except Exception as e:
            self.logger.error(f"Error adopting proposal: {e}")
            await ctx.send(f"❌ Error adopting proposal: {e}")
>>>>>>> origin/codex/build-tsla-morning-report-system
=======
__all__ = ["TechnicalDebtCommands"]
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
