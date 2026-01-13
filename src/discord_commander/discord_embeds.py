"""
<<<<<<< HEAD
Discord Embeds - Agent Cellphone V2
===================================

SSOT Domain: discord

Refactored embed creation utilities using factory pattern.

Features:
- Factory-based embed creation
- Consistent styling and formatting
- Modular embed components
- Backward compatibility maintained

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

from .embed_factory import (
    devlog_factory,
    agent_status_factory,
    coordination_factory,
    achievement_factory,
    validation_factory,
    error_factory,
    milestone_factory,
    cleanup_factory
)

# Legacy function wrappers for backward compatibility
def create_devlog_embed(devlog_data: dict) -> dict:
    """Create devlog embed using factory."""
    return devlog_factory.create_embed(devlog_data)

def create_agent_status_embed(agent_status: dict) -> dict:
    """Create agent status embed using factory."""
    return agent_status_factory.create_embed(agent_status)

def create_coordination_embed(coordination_data: dict) -> dict:
    """Create coordination embed using factory."""
    return coordination_factory.create_embed(coordination_data)

def create_achievement_embed(achievement_data: dict) -> dict:
    """Create achievement embed using factory."""
    return achievement_factory.create_embed(achievement_data)

def create_milestone_embed(milestone_data: dict) -> dict:
    """Create milestone embed using factory."""
    return milestone_factory.create_embed(milestone_data)

def create_architectural_review_embed(review_data: dict) -> dict:
    """Create architectural review embed using factory."""
    # Map to coordination embed for now
    return coordination_factory.create_embed({
        "title": "Architectural Review",
        "description": review_data.get("description", ""),
        "type": "architectural_review",
        "agent": review_data.get("agent", "Unknown")
    })

def create_error_embed(error_data: dict) -> dict:
    """Create error embed using factory."""
    return error_factory.create_embed(error_data)

def create_validation_embed(validation_data: dict) -> dict:
    """Create validation embed using factory."""
    return validation_factory.create_embed(validation_data)

def create_cleanup_embed(cleanup_data: dict) -> dict:
    """Create cleanup embed using factory."""
    return cleanup_factory.create_embed(cleanup_data)
=======
<!-- SSOT Domain: discord -->

Discord Embeds
==============

Discord embed creation utilities for V2_SWARM notifications.
Extracted from discord_service.py for V2 compliance.

Author: Agent-7 - Repository Cloning & Consolidation Specialist
Extracted: 2025-10-11 (V2 compliance refactoring)
Enhanced: 2025-01-27 - Agent-2 (Architecture & Design Specialist)
"""

from datetime import datetime
from typing import Any


def create_devlog_embed(devlog_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for devlog notification."""
    colors = {
        "general": 0x3498DB,
        "cleanup": 0xE74C3C,
        "consolidation": 0x9B59B6,
        "coordination": 0x1ABC9C,
        "testing": 0xF39C12,
        "deployment": 0x27AE60,
    }

    return {
        "title": f"📋 {devlog_data.get('title', 'DevLog Update')}",
        "description": devlog_data.get("description", "")[:2000],
        "color": colors.get(devlog_data.get("category", "general"), 0x3498DB),
        "fields": [
            {
                "name": "Category",
                "value": devlog_data.get("category", "general").title(),
                "inline": True,
            },
            {"name": "Agent", "value": devlog_data.get("agent", "Unknown"), "inline": True},
            {
                "name": "Timestamp",
                "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "inline": True,
            },
        ],
        "footer": {"text": "V2_SWARM DevLog Monitor"},
    }


def create_agent_status_embed(agent_status: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for agent status notification."""
    status_colors = {
        "active": 0x27AE60,
        "idle": 0xF39C12,
        "error": 0xE74C3C,
        "offline": 0x95A5A6,
    }

    return {
        "title": f"🤖 Agent Status Update - {agent_status.get('agent_id', 'Unknown')}",
        "color": status_colors.get(agent_status.get("status", "unknown"), 0x3498DB),
        "fields": [
            {
                "name": "Status",
                "value": agent_status.get("status", "unknown").title(),
                "inline": True,
            },
            {
                "name": "Last Activity",
                "value": agent_status.get("last_activity", "Unknown"),
                "inline": True,
            },
            {
                "name": "Timestamp",
                "value": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
                "inline": True,
            },
        ],
        "footer": {"text": "V2_SWARM Status Monitor"},
    }


def create_coordination_embed(coordination_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for swarm coordination notification."""
    priority_colors = {
        "LOW": 0x95A5A6,
        "NORMAL": 0x3498DB,
        "HIGH": 0xF39C12,
        "CRITICAL": 0xE74C3C,
    }

    return {
        "title": f"🐝 Swarm Coordination - {coordination_data.get('mission', 'Update')}",
        "color": priority_colors.get(coordination_data.get("priority", "NORMAL"), 0x3498DB),
        "fields": [
            {
                "name": "Mission",
                "value": coordination_data.get("mission", "Unknown"),
                "inline": True,
            },
            {
                "name": "Priority",
                "value": coordination_data.get("priority", "NORMAL"),
                "inline": True,
            },
            {
                "name": "Agents Involved",
                "value": str(coordination_data.get("agents", "All")),
                "inline": True,
            },
        ],
        "footer": {"text": "V2_SWARM Coordination System"},
    }


# ============================================================================
# ENHANCED EMBED TEMPLATES - Added by Agent-2
# ============================================================================

def create_achievement_embed(achievement_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for achievement notification."""
    return {
        "title": f"🏆 Achievement Unlocked - {achievement_data.get('title', 'Achievement')}",
        "description": achievement_data.get("description", ""),
        "color": 0xFFD700,  # Gold
        "fields": [
            {
                "name": "Agent",
                "value": achievement_data.get("agent", "Unknown"),
                "inline": True,
            },
            {
                "name": "Category",
                "value": achievement_data.get("category", "General"),
                "inline": True,
            },
            {
                "name": "Points",
                "value": str(achievement_data.get("points", 0)),
                "inline": True,
            },
        ],
        "footer": {"text": "🐝 WE. ARE. SWARM. ⚡ Achievement System"},
        "timestamp": achievement_data.get("timestamp"),
    }


def create_milestone_embed(milestone_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for milestone notification."""
    milestone_colors = {
        "major": 0xFF0000,  # Red
        "minor": 0x3498DB,  # Blue
        "release": 0x27AE60,  # Green
        "feature": 0x9B59B6,  # Purple
    }
    
    return {
        "title": f"🎯 Milestone Reached - {milestone_data.get('title', 'Milestone')}",
        "description": milestone_data.get("description", ""),
        "color": milestone_colors.get(milestone_data.get("type", "minor"), 0x3498DB),
        "fields": [
            {
                "name": "Milestone Type",
                "value": milestone_data.get("type", "minor").title(),
                "inline": True,
            },
            {
                "name": "Agent",
                "value": milestone_data.get("agent", "Swarm"),
                "inline": True,
            },
            {
                "name": "Progress",
                "value": f"{milestone_data.get('progress', 0)}%",
                "inline": True,
            },
        ],
        "footer": {"text": "🐝 WE. ARE. SWARM. ⚡ Milestone Tracker"},
        "timestamp": milestone_data.get("timestamp"),
    }


def create_architectural_review_embed(review_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for architectural review notification."""
    score = review_data.get("score", 0)
    score_color = (
        0x27AE60 if score >= 90 else 0xF39C12 if score >= 70 else 0xE74C3C
    )
    
    findings = review_data.get("findings", [])
    findings_text = "\n".join(findings[:3]) if findings else "No findings"
    
    return {
        "title": f"🏗️ Architectural Review - {review_data.get('component', 'Component')}",
        "description": review_data.get("summary", "")[:2000],
        "color": score_color,
        "fields": [
            {
                "name": "Compliance Score",
                "value": f"{score}/100",
                "inline": True,
            },
            {
                "name": "Status",
                "value": review_data.get("status", "PENDING"),
                "inline": True,
            },
            {
                "name": "Reviewer",
                "value": review_data.get("reviewer", "Agent-2"),
                "inline": True,
            },
            {
                "name": "Key Findings",
                "value": findings_text[:1024],  # Discord field limit
                "inline": False,
            },
        ],
        "footer": {"text": "🐝 WE. ARE. SWARM. ⚡ Architecture & Design"},
        "timestamp": review_data.get("timestamp"),
    }


def create_error_embed(error_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for error notification."""
    severity_colors = {
        "critical": 0xE74C3C,  # Red
        "high": 0xF39C12,  # Orange
        "medium": 0x3498DB,  # Blue
        "low": 0x95A5A6,  # Gray
    }
    
    error_details = error_data.get("error", "No details")[:500]
    
    return {
        "title": f"❌ Error Report - {error_data.get('title', 'Error')}",
        "description": error_data.get("description", "")[:2000],
        "color": severity_colors.get(error_data.get("severity", "medium"), 0x3498DB),
        "fields": [
            {
                "name": "Severity",
                "value": error_data.get("severity", "medium").title(),
                "inline": True,
            },
            {
                "name": "Component",
                "value": error_data.get("component", "Unknown"),
                "inline": True,
            },
            {
                "name": "Agent",
                "value": error_data.get("agent", "System"),
                "inline": True,
            },
            {
                "name": "Error Details",
                "value": f"```\n{error_details}\n```",
                "inline": False,
            },
        ],
        "footer": {"text": "🐝 WE. ARE. SWARM. ⚡ Error Monitor"},
        "timestamp": error_data.get("timestamp"),
    }


def create_validation_embed(validation_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for validation results."""
    status = validation_data.get("status", "pending")
    status_colors = {
        "passed": 0x27AE60,  # Green
        "failed": 0xE74C3C,  # Red
        "warning": 0xF39C12,  # Orange
        "pending": 0x95A5A6,  # Gray
    }
    
    results = validation_data.get("results", [])
    results_text = "\n".join(results[:5]) if results else "No results"
    
    return {
        "title": f"✅ Validation Results - {validation_data.get('type', 'Validation')}",
        "description": validation_data.get("description", "")[:2000],
        "color": status_colors.get(status, 0x95A5A6),
        "fields": [
            {
                "name": "Status",
                "value": status.title(),
                "inline": True,
            },
            {
                "name": "Type",
                "value": validation_data.get("type", "Unknown"),
                "inline": True,
            },
            {
                "name": "Score",
                "value": f"{validation_data.get('score', 0)}/100",
                "inline": True,
            },
            {
                "name": "Results",
                "value": results_text[:1024],  # Discord field limit
                "inline": False,
            },
        ],
        "footer": {"text": "🐝 WE. ARE. SWARM. ⚡ Validation System"},
        "timestamp": validation_data.get("timestamp"),
    }


def create_cleanup_embed(cleanup_data: dict[str, Any]) -> dict[str, Any]:
    """Create Discord embed for cleanup completion."""
    return {
        "title": f"🧹 Cleanup Complete - {cleanup_data.get('title', 'Cleanup')}",
        "description": cleanup_data.get("description", "")[:2000],
        "color": 0x1ABC9C,  # Teal
        "fields": [
            {
                "name": "Files Removed",
                "value": str(cleanup_data.get("files_removed", 0)),
                "inline": True,
            },
            {
                "name": "Lines Removed",
                "value": str(cleanup_data.get("lines_removed", 0)),
                "inline": True,
            },
            {
                "name": "Agent",
                "value": cleanup_data.get("agent", "System"),
                "inline": True,
            },
            {
                "name": "Impact",
                "value": cleanup_data.get("impact", "Positive"),
                "inline": False,
            },
        ],
        "footer": {"text": "🐝 WE. ARE. SWARM. ⚡ Cleanup System"},
        "timestamp": cleanup_data.get("timestamp"),
    }

>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
