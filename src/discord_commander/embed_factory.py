"""
Embed Factory - Agent Cellphone V2
==================================

SSOT Domain: discord

Base embed factory classes for creating Discord embeds with consistent styling.

Features:
- Base embed factory with common functionality
- Specialized embed creators for different types
- Consistent color schemes and formatting
- Reusable embed components

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod

try:
    import discord
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    discord = None

class BaseEmbedFactory(ABC):
    """Base factory class for creating Discord embeds."""

    # Standard color scheme
    COLORS = {
        "general": 0x3498DB,
        "cleanup": 0xE74C3C,
        "consolidation": 0x9B59B6,
        "coordination": 0x1ABC9C,
        "testing": 0xF39C12,
        "deployment": 0x27AE60,
        "success": 0x2ECC71,
        "error": 0xE74C3C,
        "warning": 0xF39C12,
        "info": 0x3498DB,
        "achievement": 0xF1C40F,
        "milestone": 0x9B59B6,
        "architectural": 0x34495E,
        "validation": 0x16A085
    }

    def __init__(self):
        self.default_footer = "Agent Cellphone V2"

    def create_base_embed(self, title: str, description: str = "",
                         color_key: str = "general") -> Dict[str, Any]:
        """Create a base embed structure."""
        return {
            "title": title,
            "description": description[:2000] if description else "",
            "color": self.COLORS.get(color_key, self.COLORS["general"]),
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {"text": self.default_footer}
        }

    def add_field(self, embed: Dict[str, Any], name: str, value: str,
                  inline: bool = False) -> None:
        """Add a field to an embed."""
        if "fields" not in embed:
            embed["fields"] = []

        # Ensure field limits
        if len(embed["fields"]) >= 25:  # Discord limit
            return

        embed["fields"].append({
            "name": name[:256],  # Discord field name limit
            "value": value[:1024],  # Discord field value limit
            "inline": inline
        })

    def add_timestamp_field(self, embed: Dict[str, Any]) -> None:
        """Add a timestamp field."""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.add_field(embed, "Timestamp", timestamp, inline=True)

    def add_agent_field(self, embed: Dict[str, Any], agent: str) -> None:
        """Add an agent field."""
        self.add_field(embed, "Agent", agent, inline=True)

    def add_category_field(self, embed: Dict[str, Any], category: str) -> None:
        """Add a category field."""
        self.add_field(embed, "Category", category.title(), inline=True)

    @abstractmethod
    def create_embed(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a specific type of embed. Override in subclasses."""
        pass

class DevlogEmbedFactory(BaseEmbedFactory):
    """Factory for devlog notification embeds."""

    def create_embed(self, devlog_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create devlog embed."""
        embed = self.create_base_embed(
            title=f"📋 {devlog_data.get('title', 'DevLog Update')}",
            description=devlog_data.get("description", ""),
            color_key=devlog_data.get("category", "general")
        )

        self.add_category_field(embed, devlog_data.get("category", "general"))
        self.add_agent_field(embed, devlog_data.get("agent", "Unknown"))
        self.add_timestamp_field(embed)

        return embed

class AgentStatusEmbedFactory(BaseEmbedFactory):
    """Factory for agent status embeds."""

    def create_embed(self, agent_status: Dict[str, Any]) -> Dict[str, Any]:
        """Create agent status embed."""
        agent_id = agent_status.get("agent_id", "Unknown")
        status = agent_status.get("status", "unknown")

        embed = self.create_base_embed(
            title=f"🤖 Agent Status: {agent_id}",
            description=f"Current status and activity for {agent_id}",
            color_key="success" if status == "ACTIVE_AGENT_MODE" else "warning"
        )

        self.add_field(embed, "Status", status.replace("_", " ").title(), inline=True)
        self.add_field(embed, "Current Mission",
                      agent_status.get("current_mission", "No active mission"), inline=False)

        # Task counts
        completed = len(agent_status.get("completed_tasks", []))
        active = len(agent_status.get("current_tasks", []))
        self.add_field(embed, "Completed Tasks", str(completed), inline=True)
        self.add_field(embed, "Active Tasks", str(active), inline=True)
        self.add_field(embed, "Total Tasks", str(completed + active), inline=True)

        return embed

class CoordinationEmbedFactory(BaseEmbedFactory):
    """Factory for coordination embeds."""

    def create_embed(self, coordination_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create coordination embed."""
        title = coordination_data.get("title", "Coordination Update")

        embed = self.create_base_embed(
            title=f"🤝 {title}",
            description=coordination_data.get("description", ""),
            color_key="coordination"
        )

        self.add_field(embed, "Type", coordination_data.get("type", "General"), inline=True)
        self.add_agent_field(embed, coordination_data.get("agent", "Unknown"))
        self.add_timestamp_field(embed)

        if "details" in coordination_data:
            self.add_field(embed, "Details", coordination_data["details"], inline=False)

        return embed

class AchievementEmbedFactory(BaseEmbedFactory):
    """Factory for achievement embeds."""

    def create_embed(self, achievement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create achievement embed."""
        title = achievement_data.get("title", "Achievement Unlocked")

        embed = self.create_base_embed(
            title=f"🏆 {title}",
            description=achievement_data.get("description", ""),
            color_key="achievement"
        )

        self.add_category_field(embed, achievement_data.get("category", "achievement"))
        self.add_agent_field(embed, achievement_data.get("agent", "Unknown"))

        if "points" in achievement_data:
            self.add_field(embed, "Points", str(achievement_data["points"]), inline=True)

        if "milestone" in achievement_data:
            self.add_field(embed, "Milestone", achievement_data["milestone"], inline=False)

        return embed

class ValidationEmbedFactory(BaseEmbedFactory):
    """Factory for validation embeds."""

    def create_embed(self, validation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create validation embed."""
        status = validation_data.get("status", "unknown")
        title = validation_data.get("title", "Validation Results")

        embed = self.create_base_embed(
            title=f"✅ {title}" if status == "PASS" else f"❌ {title}",
            description=validation_data.get("description", ""),
            color_key="success" if status == "PASS" else "error"
        )

        self.add_field(embed, "Status", status, inline=True)
        self.add_field(embed, "Type", validation_data.get("type", "General"), inline=True)

        if "details" in validation_data:
            self.add_field(embed, "Details", validation_data["details"], inline=False)

        return embed

class ErrorEmbedFactory(BaseEmbedFactory):
    """Factory for error embeds."""

    def create_embed(self, error_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create error embed."""
        title = error_data.get("title", "Error Occurred")

        embed = self.create_base_embed(
            title=f"❌ {title}",
            description=error_data.get("description", ""),
            color_key="error"
        )

        if "error_code" in error_data:
            self.add_field(embed, "Error Code", error_data["error_code"], inline=True)

        if "component" in error_data:
            self.add_field(embed, "Component", error_data["component"], inline=True)

        self.add_timestamp_field(embed)

        if "traceback" in error_data:
            traceback = error_data["traceback"][:500]  # Limit length
            self.add_field(embed, "Traceback", f"```\n{traceback}\n```", inline=False)

        return embed

class MilestoneEmbedFactory(BaseEmbedFactory):
    """Factory for milestone embeds."""

    def create_embed(self, milestone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create milestone embed."""
        title = milestone_data.get("title", "Milestone Reached")

        embed = self.create_base_embed(
            title=f"🎯 {title}",
            description=milestone_data.get("description", ""),
            color_key="milestone"
        )

        if "progress" in milestone_data:
            progress = milestone_data["progress"]
            self.add_field(embed, "Progress", f"{progress}%", inline=True)

        if "phase" in milestone_data:
            self.add_field(embed, "Phase", milestone_data["phase"], inline=True)

        self.add_timestamp_field(embed)

        return embed

class CleanupEmbedFactory(BaseEmbedFactory):
    """Factory for cleanup embeds."""

    def create_embed(self, cleanup_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create cleanup embed."""
        title = cleanup_data.get("title", "Cleanup Completed")

        embed = self.create_base_embed(
            title=f"🧹 {title}",
            description=cleanup_data.get("description", ""),
            color_key="cleanup"
        )

        if "files_removed" in cleanup_data:
            self.add_field(embed, "Files Removed", str(cleanup_data["files_removed"]), inline=True)

        if "space_freed" in cleanup_data:
            self.add_field(embed, "Space Freed", cleanup_data["space_freed"], inline=True)

        self.add_timestamp_field(embed)

        return embed

# Factory instances for easy access
devlog_factory = DevlogEmbedFactory()
agent_status_factory = AgentStatusEmbedFactory()
coordination_factory = CoordinationEmbedFactory()
achievement_factory = AchievementEmbedFactory()
validation_factory = ValidationEmbedFactory()
error_factory = ErrorEmbedFactory()
milestone_factory = MilestoneEmbedFactory()
cleanup_factory = CleanupEmbedFactory()

__all__ = [
    "BaseEmbedFactory",
    "DevlogEmbedFactory",
    "AgentStatusEmbedFactory",
    "CoordinationEmbedFactory",
    "AchievementEmbedFactory",
    "ValidationEmbedFactory",
    "ErrorEmbedFactory",
    "MilestoneEmbedFactory",
    "CleanupEmbedFactory",
    # Factory instances
    "devlog_factory",
    "agent_status_factory",
    "coordination_factory",
    "achievement_factory",
    "validation_factory",
    "error_factory",
    "milestone_factory",
    "cleanup_factory"
]