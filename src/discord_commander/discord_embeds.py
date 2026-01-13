"""
<<<<<<< HEAD
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
=======
Discord Embeds - Agent Cellphone V2
===================================
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1

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

<<<<<<< HEAD
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
=======
def create_cleanup_embed(cleanup_data: dict) -> dict:
    """Create cleanup embed using factory."""
    return cleanup_factory.create_embed(cleanup_data)
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
