"""Gaming Models.
<!-- SSOT Domain: gaming -->


Data models and enums for gaming integration system.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List
from dataclasses import dataclass, field



# IntegrationStatus - Redirect to SSOT
# SSOT: src/architecture/system_integration.py
from src.architecture.system_integration import IntegrationStatus

# Re-export for backward compatibility
__all__ = ["IntegrationStatus", "GameType", "GameSession", "EntertainmentSystem"]


class GameType(Enum):
    """Types of games supported by the system."""

    ACTION = "action"
    ADVENTURE = "adventure"
    PUZZLE = "puzzle"
    STRATEGY = "strategy"
    SIMULATION = "simulation"
    SPORTS = "sports"
    RPG = "rpg"
    ARCADE = "arcade"


@dataclass
class GameSession:
    """Represents an active gaming session."""

    session_id: str
    game_type: GameType
    player_id: str
    start_time: datetime
    status: str
    metadata: Dict[str, Any]
    performance_metrics: Dict[str, Any]


@dataclass
class EntertainmentSystem:
    """Represents an entertainment system component."""

    system_id: str
    system_type: str
    status: IntegrationStatus
    capabilities: List[str]
    configuration: Dict[str, Any]
    last_updated: datetime
