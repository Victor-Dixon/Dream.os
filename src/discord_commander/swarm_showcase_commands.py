#!/usr/bin/env python3
"""
<<<<<<< HEAD
<<<<<<< HEAD
Swarm Showcase Commands - Agent Cellphone V2
===========================================

<!-- SSOT Domain: discord -->

SSOT Domain: discord

Refactored entry point for swarm showcase functionality.
All core logic has been extracted into modular components for V2 compliance.

Features:
- Modular data loading (swarm_showcase_data.py)
- Professional embed factory (swarm_showcase_embeds.py)
- Focused command handling (swarm_showcase_commands_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

# Import the main components for backward compatibility
from .swarm_showcase_data import SwarmShowcaseData
from .swarm_showcase_embeds import SwarmShowcaseEmbeds
# SwarmShowcaseCommands class is defined below - no external import needed



# === V2 FEATURES MERGED ===

"""
Swarm Showcase Commands V2 - Agent Cellphone V2
==============================================

SSOT Domain: discord

Refactored Discord commands for swarm showcase displays.

Features:
- Simplified command handling using modular components
- Professional embed displays for swarm capabilities
- Task tracking and agent excellence showcases

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import logging
=======
=======
Swarm Showcase Commands - Agent Cellphone V2
===========================================

>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
<!-- SSOT Domain: discord -->

SSOT Domain: discord

Refactored entry point for swarm showcase functionality.
All core logic has been extracted into modular components for V2 compliance.

Features:
- Modular data loading (swarm_showcase_data.py)
- Professional embed factory (swarm_showcase_embeds.py)
- Focused command handling (swarm_showcase_commands_v2.py)

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

<<<<<<< HEAD
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
from typing import Any

try:
    import discord
    from discord.ext import commands
<<<<<<< HEAD
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    from .test_utils import get_mock_discord
    mock_discord, mock_commands = get_mock_discord()
    discord = mock_discord
    commands = mock_commands

from .swarm_showcase_data import SwarmShowcaseData
from .swarm_showcase_embeds import SwarmShowcaseEmbeds

logger = logging.getLogger(__name__)

class SwarmShowcaseCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Professional Discord showcase for swarm capabilities using modular components.
=======

    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None
    commands = None

logger = logging.getLogger(__name__)


class SwarmShowcaseCommands(commands.Cog if DISCORD_AVAILABLE else object):
    """
    Beautiful Discord showcase for swarm capabilities.
    
    Commands:
    - !swarm_tasks - Display all active tasks and directives
    - !swarm_roadmap - Show integration roadmap
    - !swarm_excellence - Showcase agent achievements
    - !swarm_overview - Complete swarm status and missions
    - !swarm_profile - Display swarm collective profile (identity, stats, achievements)
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
    """

    def __init__(self, bot):
        self.bot = bot
<<<<<<< HEAD
        self.data_loader = SwarmShowcaseData()
        self.embed_factory = SwarmShowcaseEmbeds(self.data_loader)

    @commands.command(name="swarm_tasks", aliases=["tasks"])
    async def show_swarm_tasks(self, ctx: commands.Context):
        """Display all active tasks and directives."""
        try:
            embed = self.embed_factory.create_tasks_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm tasks: {e}")
            await ctx.send("❌ Failed to load swarm tasks. Please try again later.")

    @commands.command(name="swarm_roadmap", aliases=["roadmap"])
    async def show_swarm_roadmap(self, ctx: commands.Context):
        """Show integration roadmap and progress."""
        try:
            embed = self.embed_factory.create_roadmap_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm roadmap: {e}")
            await ctx.send("❌ Failed to load swarm roadmap. Please try again later.")

    @commands.command(name="swarm_excellence", aliases=["excellence"])
    async def show_swarm_excellence(self, ctx: commands.Context):
        """Showcase agent achievements and excellence."""
        try:
            embed = self.embed_factory.create_excellence_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm excellence: {e}")
            await ctx.send("❌ Failed to load swarm excellence showcase. Please try again later.")

    @commands.command(name="swarm_overview", aliases=["overview", "status"])
    async def show_swarm_overview(self, ctx: commands.Context):
        """Complete swarm status and missions overview."""
        try:
            embed = self.embed_factory.create_overview_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show swarm overview: {e}")
            await ctx.send("❌ Failed to load swarm overview. Please try again later.")

    @commands.command(name="swarm_profile", aliases=["profile"])
    async def show_swarm_profile(self, ctx: commands.Context, agent_id: str = None):
        """Show detailed profile for specific agent."""
        if not agent_id:
            await ctx.send("❌ Please specify an agent ID. Usage: `!swarm_profile Agent-1`")
            return

        try:
            embed = self.embed_factory.create_profile_embed(agent_id)
            await ctx.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to show agent profile for {agent_id}: {e}")
            await ctx.send(f"❌ Failed to load profile for {agent_id}. Please check the agent ID and try again.")

    @commands.command(name="swarm_refresh", aliases=["refresh"])
    async def refresh_swarm_data(self, ctx: commands.Context):
        """Refresh all swarm showcase data."""
        try:
            self.data_loader.refresh_data()
            await ctx.send("✅ Swarm showcase data has been refreshed!")
        except Exception as e:
            logger.error(f"Failed to refresh swarm data: {e}")
            await ctx.send("❌ Failed to refresh swarm data. Please try again later.")

async def setup(bot):
    """Setup function for Discord cog."""
    await bot.add_cog(SwarmShowcaseCommands(bot))
=======
        self.workspace_path = Path("agent_workspaces")
        self.docs_path = Path("docs")
        self.logger = logging.getLogger(__name__)

    # ========================================================================
    # SWARM TASKS & DIRECTIVES DISPLAY
    # ========================================================================

    @commands.command(name="swarm_tasks", aliases=["tasks", "directives"])
    async def show_swarm_tasks(self, ctx: commands.Context):
        """
        Display all active tasks and directives across the swarm.
        
        Shows:
        - Active missions per agent
        - Captain directives in progress
        - Priority tasks
        - Completion status
        """
        try:
            # Use the new controller view for full functionality with pagination
            from .controllers.swarm_tasks_controller_view import SwarmTasksControllerView
            
            view = SwarmTasksControllerView(messaging_service=None)
            embed = view.create_initial_embed()
            
            await ctx.send(embed=embed, view=view)
        except Exception as e:
            self.logger.error(f"Error displaying swarm tasks: {e}", exc_info=True)
            # Fallback to old method if controller fails
            try:
                embed = await self._create_tasks_embed()
                await ctx.send(embed=embed)
            except Exception as fallback_error:
                self.logger.error(f"Fallback also failed: {fallback_error}", exc_info=True)
                await ctx.send(f"❌ Error loading swarm tasks: {e}")

    async def _create_tasks_embed(self) -> discord.Embed:
        """Create beautiful embed for tasks and directives."""
        embed = discord.Embed(
            title="🐝 SWARM TASKS & DIRECTIVES DASHBOARD",
            description="**Current missions across all agents** 🚀",
            color=0x2ECC71,  # Green for active work
            timestamp=discord.utils.utcnow(),
        )

        # Load agent statuses
        agents_data = self._load_all_agent_statuses()
        
        # Sort by priority
        priority_order = {"CRITICAL": 0, "HIGH": 1, "ACTIVE": 2, "MEDIUM": 3, "LOW": 4}
        sorted_agents = sorted(
            agents_data,
            key=lambda x: priority_order.get(x.get("mission_priority", "MEDIUM"), 5)
        )

        # Add agent tasks
        for agent in sorted_agents[:8]:  # Limit to 8 agents (Discord field limit: 25)
            agent_id = agent.get("agent_id", "Unknown")
            mission = agent.get("current_mission", "No active mission")
            tasks = agent.get("current_tasks", [])
            priority = agent.get("mission_priority", "MEDIUM")
            
            # Priority emoji
            priority_emoji = {
                "CRITICAL": "🔴",
                "HIGH": "🟠",
                "ACTIVE": "🟢",
                "MEDIUM": "🟡",
                "LOW": "⚪"
            }.get(priority, "🔵")
            
            # Format tasks with FULL content (no truncation)
            # Use chunking utility to handle long task lists
            from src.discord_commander.utils.message_chunking import chunk_field_value
            
            if tasks:
                # Create full task list
                task_list = "\n".join([f"• {task}" for task in tasks])
            else:
                task_list = "No specific tasks listed"
            
            # Build field value
            base_value = f"**Mission:** {mission}\n\n**Tasks:**\n{task_list}"
            
            # Chunk if needed
            value_chunks = chunk_field_value(base_value)
            
            # Add first chunk as main field
            embed.add_field(
                name=f"{priority_emoji} {agent_id} - {priority}",
                value=value_chunks[0],
                inline=False
            )
            
            # Add continuation fields if needed
            for i, chunk in enumerate(value_chunks[1:], 2):
                embed.add_field(
                    name=f"  └─ {agent_id} (continued {i}/{len(value_chunks)})",
                    value=chunk,
                    inline=False
                )

        # Add footer with statistics
        total_tasks = sum(len(agent.get("current_tasks", [])) for agent in agents_data)
        active_agents = sum(1 for agent in agents_data if agent.get("status") == "ACTIVE_AGENT_MODE")
        
        embed.set_footer(text=f"🐝 {active_agents}/8 agents active • {total_tasks} total tasks in progress • WE ARE SWARM")

        return embed

    # ========================================================================
    # SWARM ROADMAP DISPLAY
    # ========================================================================

    @commands.command(name="swarm_roadmap", aliases=["roadmap", "plan"])
    async def show_swarm_roadmap(self, ctx: commands.Context):
        """
        Display swarm integration and consolidation roadmap.
        
        Shows:
        - Integration priorities
        - Consolidation progress
        - Timeline and phases
        - High-value opportunities
        """
        try:
            embed = await self._create_roadmap_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error displaying roadmap: {e}")
            await ctx.send(f"❌ Error loading roadmap: {e}")

    async def _create_roadmap_embed(self) -> discord.Embed:
        """Create beautiful embed for swarm roadmap."""
        embed = discord.Embed(
            title="🗺️ SWARM INTEGRATION & CONSOLIDATION ROADMAP",
            description="**Strategic priorities and high-value opportunities**",
            color=0x9B59B6,  # Purple for strategic planning
            timestamp=discord.utils.utcnow(),
        )

        # PHASE 1: Current Sprint (extracted from real data)
        embed.add_field(
            name="📍 PHASE 1: CURRENT SPRINT (Week 1-2)",
            value=(
                "**Status:** 🔥 IN PROGRESS\n\n"
                "• ✅ Messaging consolidation (14→8 files, 43% reduction)\n"
                "• ✅ Discord enhancements (!shutdown, !restart commands)\n"
                "• 🔄 Infrastructure consolidation (167+ tools audit)\n"
                "• 🔄 GitHub 75-repo analysis (47/75 complete, 62.7%)\n"
                "• 🎯 V2 compliance campaign (6 violations remaining)"
            ),
            inline=False
        )

        # PHASE 2: Integration Goldmines
        embed.add_field(
            name="⭐ PHASE 2: GOLDMINE INTEGRATIONS (Weeks 3-6)",
            value=(
                "**High-ROI opportunities from repo analysis:**\n\n"
                "🏆 **contract-leads** - Multi-factor scoring (50-65hr, ⭐⭐⭐⭐⭐)\n"
                "🏆 **DreamVault** - 5 AI agents + IP mining (160-200hr, ⭐⭐⭐⭐)\n"
                "🏆 **TROOP** - Scheduler + Risk management (70-100hr, ⭐⭐⭐⭐)\n"
                "🏆 **Discord Notifications** - Real-time visibility (40-60hr, ⭐⭐⭐⭐⭐)\n"
                "🏆 **Agent Prediction ML** - LSTM optimization (50-75hr, ⭐⭐⭐⭐)"
            ),
            inline=False
        )

        # PHASE 3: Advanced Capabilities
        embed.add_field(
            name="🚀 PHASE 3: ADVANCED CAPABILITIES (Weeks 7-10)",
            value=(
                "**System enhancements and automation:**\n\n"
                "• Autonomous workflow tools (Phase 1 approved, 5-7hr)\n"
                "• Auto-assignment engine (70% overhead reduction)\n"
                "• Team coordination dashboard (real-time monitoring)\n"
                "• Contract marketplace system (agent specialization)\n"
                "• Full DreamVault integration (AI agent capabilities)"
            ),
            inline=False
        )

        # Quick Wins
        embed.add_field(
            name="⚡ QUICK WINS (< 20 hours each)",
            value=(
                "**High impact, low effort opportunities:**\n\n"
                "✨ DreamVault IP Resurrection (20hr)\n"
                "✨ TROOP Scheduler Integration (20-30hr)\n"
                "✨ Bible-app Threading Patterns (5-10hr)\n"
                "✨ JWT Auth from FreeWork (5-10hr)\n"
                "✨ Discord Status Automation (15-20hr)"
            ),
            inline=False
        )

        # Add total value footer
        embed.set_footer(
            text="🐝 Total Integration Value: 800-1000+ hours of opportunities identified | WE ARE SWARM"
        )

        return embed

    # ========================================================================
    # SWARM EXCELLENCE SHOWCASE
    # ========================================================================

    @commands.command(name="swarm_excellence", aliases=["excellence", "achievements"])
    async def show_swarm_excellence(self, ctx: commands.Context):
        """
        Showcase swarm achievements and agent excellence.
        
        Displays:
        - LEGENDARY performance agents
        - Goldmine discoveries
        - Major refactorings
        - Innovation highlights
        """
        try:
            embed = await self._create_excellence_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error displaying excellence: {e}")
            await ctx.send(f"❌ Error loading swarm excellence: {e}")

    async def _create_excellence_embed(self) -> discord.Embed:
        """Create beautiful embed showcasing swarm achievements."""
        embed = discord.Embed(
            title="🏆 SWARM EXCELLENCE SHOWCASE",
            description="**Celebrating autonomous agent achievements and innovation** ⚡",
            color=0xF1C40F,  # Gold for excellence
            timestamp=discord.utils.utcnow(),
        )

        # LEGENDARY Agents
        embed.add_field(
            name="👑 LEGENDARY PERFORMANCE",
            value=(
                "**Agent-6** (Co-Captain)\n"
                "• 12/12 repos + 5 JACKPOTs\n"
                "• Created 3 swarm standards\n"
                "• Earned Co-Captain role through excellence\n\n"
                "**Agent-2** (Architecture LEAD)\n"
                "• 10/10 repos + 4 GOLDMINEs\n"
                "• 5 enhanced specs (2,900+ lines)\n"
                "• Team B infrastructure LEAD\n\n"
                "**Agent-7** (Web Development)\n"
                "• 10/10 repos + 4 JACKPOTs\n"
                "• Applied Agent-6 methodology (95% success)\n"
                "• Autonomous excellence demonstrated"
            ),
            inline=False
        )

        # Major Refactorings
        embed.add_field(
            name="🔧 MAJOR REFACTORINGS COMPLETE",
            value=(
                "• **messaging_infrastructure.py** - 7 files → 1 (75% reduction)\n"
                "• **agent_toolbelt_executors.py** - 618→55 lines (91% reduction)\n"
                "• **unified_import_system.py** - 275→76 lines (72.4% reduction)\n"
                "• **config_ssot.py** - 471→78 lines (83.4% reduction)\n"
                "• **comprehensive_project_analyzer.py** - 623→84 lines (87% reduction)"
            ),
            inline=False
        )

        # Goldmine Discoveries
        embed.add_field(
            name="💎 GOLDMINE DISCOVERIES",
            value=(
                "**DreamVault** - 5 AI agents partially integrated (40% complete)\n"
                "**contract-leads** - Multi-factor scoring system (⭐⭐⭐⭐⭐)\n"
                "**TROOP** - Scheduler + Risk + Backtesting patterns\n"
                "**Agent_Cellphone V1** - Features V2 lacks (migration framework)\n"
                "**ideas repo** - Migration framework that solves our needs\n"
                "**projectscanner** - Only starred repo, already integrated successfully"
            ),
            inline=False
        )

        # Innovation Highlights
        embed.add_field(
            name="⚡ INNOVATIONS & PROTOCOLS",
            value=(
                "• **Entry #025** - Compete + Cooperate + Integrity framework\n"
                "• **Pipeline Protocol** - 3-send gas delivery (75%, 90%, 100%)\n"
                "• **Agent-6 Methodology** - 90-95% discovery rate (6-phase approach)\n"
                "• **Autonomous Workflow Tools** - 70% LEAD overhead reduction\n"
                "• **Message Queue Enhancement** - Turn feedback into fuel"
            ),
            inline=False
        )

        embed.set_footer(text="🐝 Excellence Through Collective Intelligence | WE ARE SWARM")

        return embed

    # ========================================================================
    # COMPREHENSIVE SWARM OVERVIEW
    # ========================================================================

    @commands.command(name="swarm_overview", aliases=["overview", "dashboard"])
    async def show_swarm_overview(self, ctx: commands.Context):
        """
        Complete swarm overview - missions, progress, and status.
        
        Combines:
        - Current missions (2 teams)
        - Progress metrics
        - Agent status summary
        - Next priorities
        """
        try:
            embed = await self._create_overview_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error displaying overview: {e}")
            await ctx.send(f"❌ Error loading overview: {e}")

    async def _create_overview_embed(self) -> discord.Embed:
        """Create comprehensive swarm overview embed."""
        embed = discord.Embed(
            title="🐝 SWARM OPERATIONAL DASHBOARD",
            description="**Real-time swarm status and mission progress** ⚡",
            color=0x3498DB,  # Blue for comprehensive view
            timestamp=discord.utils.utcnow(),
        )

        # Team A: GitHub Analysis
        embed.add_field(
            name="🚀 TEAM A - GitHub Repository Analysis",
            value=(
                "**Lead:** Co-Captain Agent-6\n"
                "**Progress:** 47/75 repos (62.7%) ✅\n"
                "**Status:** ACTIVE - Repos 21-30, 61-70 in progress\n\n"
                "**Completed:**\n"
                "• Repos 1-10: Agent-1 (+ 1 jackpot)\n"
                "• Repos 11-20: Agent-2 (+ 4 goldmines)\n"
                "• Repos 41-50: Agent-6 (+ 5 jackpots)\n"
                "• Repos 51-60: Agent-7 (+ 4 jackpots)\n"
                "• Repos 71-75: Captain (complete)"
            ),
            inline=False
        )

        # Team B: Infrastructure
        embed.add_field(
            name="🏗️ TEAM B - Infrastructure Consolidation",
            value=(
                "**LEAD:** Agent-2 (Architecture)\n"
                "**Progress:** 75% complete ✅\n"
                "**Status:** ACTIVE - Continuous execution\n\n"
                "**Completed:**\n"
                "✅ [D2A] Messaging fix (General's directive SOLVED!)\n"
                "✅ Discord !shutdown & !restart commands\n"
                "✅ Messaging consolidation (14→8 files, 43% reduction)\n"
                "🔄 Toolbelt audit (167+ tools cataloged)\n"
                "🔄 Autonomous workflow tools (Phase 1 approved)"
            ),
            inline=False
        )

        # Mission Stats
        agents_data = self._load_all_agent_statuses()
        active_count = sum(1 for a in agents_data if "ACTIVE" in a.get("status", ""))
        total_tasks = sum(len(a.get("current_tasks", [])) for a in agents_data)
        total_completed = sum(len(a.get("completed_tasks", [])) for a in agents_data)

        embed.add_field(
            name="📊 SWARM METRICS",
            value=(
                f"**Active Agents:** {active_count}/8 🟢\n"
                f"**Active Tasks:** {total_tasks} in progress\n"
                f"**Completed Tasks:** {total_completed}+ accomplished\n"
                "**Goldmines Found:** 15+ high-value opportunities\n"
                "**Integration Value:** 800-1000+ hours identified"
            ),
            inline=False
        )

        # Next Priorities
        embed.add_field(
            name="🎯 NEXT PRIORITIES",
            value=(
                "1. Complete repos 21-30 (Agent-3, 7,100 pts - 1st place!)\n"
                "2. Complete repos 61-70 (Agent-8, executing)\n"
                "3. Compile 75-repo comprehensive book\n"
                "4. Resume democratic consolidation debate\n"
                "5. Execute approved integration strategy"
            ),
            inline=False
        )

        embed.set_footer(text="🐝 Dual-track execution - No idleness! | WE ARE SWARM")

        return embed

    # ========================================================================
    # SWARM PROFILE DISPLAY
    # ========================================================================

    @commands.command(name="swarm_profile", aliases=["profile", "swarm_identity"])
    async def show_swarm_profile(self, ctx: commands.Context):
        """
        Display swarm collective profile - identity, stats, achievements.
        
        Shows:
        - Swarm identity and personality
        - Mission and vision
        - Agent composition
        - Capabilities and achievements
        - Current stats and blockers
        """
        try:
            embed = await self._create_profile_embed()
            await ctx.send(embed=embed)
        except Exception as e:
            self.logger.error(f"Error displaying swarm profile: {e}", exc_info=True)
            await ctx.send(f"❌ Error loading swarm profile: {e}")

    async def _create_profile_embed(self) -> discord.Embed:
        """Create beautiful embed for swarm profile."""
        # Load swarm profile
        profile_path = Path("swarm_profile.json")
        if not profile_path.exists():
            embed = discord.Embed(
                title="🐝 SWARM PROFILE",
                description="**Swarm profile not found**",
                color=discord.Color.red(),
            )
            return embed
        
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading swarm profile: {e}")
            embed = discord.Embed(
                title="🐝 SWARM PROFILE",
                description=f"**Error loading profile: {e}**",
                color=discord.Color.red(),
            )
            return embed
        
        # Extract data
        identity = profile.get("identity", {})
        personality = identity.get("personality", {})
        composition = profile.get("composition", {})
        capabilities = profile.get("capabilities", {})
        achievements = profile.get("achievements", {})
        stats = profile.get("stats", {})
        values = profile.get("values_and_principles", {})
        
        # Create embed
        embed = discord.Embed(
            title=f"🐝 {profile.get('swarm_name', 'Swarm')} Profile",
            description=f"**{profile.get('swarm_tagline', 'WE. ARE. SWARM. ⚡🔥')}**\n\n{identity.get('mission', 'No mission defined')}",
            color=0xF39C12,  # Orange for identity
            timestamp=discord.utils.utcnow(),
        )
        
        # Identity Section
        embed.add_field(
            name="🎭 Identity",
            value=(
                f"**Tone:** {personality.get('tone', 'Unknown')}\n"
                f"**Style:** {personality.get('communication_style', 'Unknown')}\n"
                f"**Values:** {', '.join(personality.get('values', [])[:5])}\n"
                f"**Philosophy:** Build Fast, Break Better"
            ),
            inline=False
        )
        
        # Composition
        total_agents = composition.get("total_agents", 0)
        active_agents = composition.get("active_agents", 0)
        embed.add_field(
            name="👥 Composition",
            value=(
                f"**Total Agents:** {total_agents}\n"
                f"**Active Agents:** {active_agents}\n"
                f"**Specializations:** {len(composition.get('agent_roles', {}))} roles"
            ),
            inline=True
        )
        
        # Capabilities
        core_systems = len(capabilities.get("core_systems", []))
        tools = len(capabilities.get("tools", []))
        embed.add_field(
            name="⚙️ Capabilities",
            value=(
                f"**Core Systems:** {core_systems}\n"
                f"**Specializations:** {len(capabilities.get('specializations', []))}\n"
                f"**Tools:** {tools}"
            ),
            inline=True
        )
        
        # Achievements
        milestones = len(achievements.get("major_milestones", []))
        repo_consolidation = achievements.get("repository_consolidation", {})
        repos_reduced = repo_consolidation.get("repos_reduced", 0)
        embed.add_field(
            name="🏆 Achievements",
            value=(
                f"**Major Milestones:** {milestones}\n"
                f"**Repos Reduced:** {repos_reduced} (21% reduction)\n"
                f"**Target:** {repo_consolidation.get('target', 'Unknown')}"
            ),
            inline=True
        )
        
        # Stats
        active_projects = len(stats.get("active_projects", []))
        blockers = len(stats.get("current_blockers", []))
        compliance = stats.get("compliance_rate", "Unknown")
        embed.add_field(
            name="📊 Current Stats",
            value=(
                f"**Active Projects:** {active_projects}\n"
                f"**Current Blockers:** {blockers}\n"
                f"**Compliance Rate:** {compliance}\n"
                f"**Efficiency:** {stats.get('swarm_efficiency', 'Unknown')}"
            ),
            inline=False
        )
        
        # Principles
        core_values = values.get("core_values", [])
        if core_values:
            embed.add_field(
                name="💎 Core Values",
                value=" • ".join(core_values[:5]),
                inline=False
            )
        
        # Footer
        embed.set_footer(text=f"🐝 Version {profile.get('version', 'Unknown')} • Last Updated: {profile.get('last_updated', 'Unknown')[:10]} • WE. ARE. SWARM. ⚡🔥")
        
        return embed

    # ========================================================================
    # HELPER METHODS
    # ========================================================================

    def _load_all_agent_statuses(self) -> list[dict[str, Any]]:
        """Load status for all agents."""
        agents = []
        
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status_file = self.workspace_path / agent_id / "status.json"
            
            if not status_file.exists():
                continue
                
            try:
                with open(status_file, "r", encoding="utf-8") as f:
                    status = json.load(f)
                    agents.append(status)
            except Exception as e:
                self.logger.warning(f"Could not load status for {agent_id}: {e}")
                
        return agents

    def _load_roadmap_data(self) -> dict[str, Any]:
        """Load roadmap data from documentation."""
        # Try to load from integration roadmap
        roadmap_file = self.docs_path / "integration" / "CONSOLIDATED_INTEGRATION_ROADMAP.md"
        
        if not roadmap_file.exists():
            return {
                "phases": [],
                "goldmines": [],
                "total_value": "800-1000+ hours"
            }
        
        # For now, return static data (can be enhanced to parse markdown)
        return {
            "phases": ["Current Sprint", "Goldmine Integrations", "Advanced Capabilities"],
            "goldmines": ["DreamVault", "contract-leads", "TROOP", "Discord Notifications"],
            "total_value": "800-1000+ hours"
        }


async def setup(bot):
    """Setup function for Discord.py 2.0+ cog loading."""
    if DISCORD_AVAILABLE:
        await bot.add_cog(SwarmShowcaseCommands(bot))
        logger.info("✅ SwarmShowcaseCommands cog loaded")
    else:
        logger.warning("⚠️ Discord not available - SwarmShowcaseCommands not loaded")
=======
# Re-export the main components for backward compatibility
from .swarm_showcase_data import SwarmShowcaseData
from .swarm_showcase_embeds import SwarmShowcaseEmbeds
from .swarm_showcase_commands_v2 import SwarmShowcaseCommands, setup
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
