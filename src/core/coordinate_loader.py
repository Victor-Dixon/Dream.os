"""
Mock Coordinate Loader for Testing
==================================

<!-- SSOT Domain: integration -->

Provides mock coordinate loading functionality for smoke testing.
FIXED: Always loads coordinates for ALL agents, regardless of mode.
This allows Discord messages to be delivered to inactive agents.
Mode filtering only affects processing order, not message delivery capability.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _load_coordinates() -> dict[str, dict[str, Any]]:
    """Load agent coordinates from the cursor_agent_coords.json SSOT.
    
    CRITICAL: chat_input_coordinates goes to "coords", onboarding_input_coords goes to "onboarding_coords".
    These must NEVER be swapped.
    
    FIXED: Always loads coordinates for ALL agents, regardless of mode.
    This allows Discord messages to be delivered to inactive agents (e.g., agents 5-8 in 4-agent mode).
    Mode filtering only affects processing order, not message delivery capability.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    coord_file = Path("cursor_agent_coords.json")
    
    # Handle missing file gracefully
    if not coord_file.exists():
        return {}
    
    try:
        data = json.loads(coord_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        return {}
    
    # Get active agents from mode manager (for logging only)
    try:
        from .agent_mode_manager import get_mode_manager
        mode_manager = get_mode_manager()
        active_agents = set(mode_manager.get_active_agents())
        current_mode = mode_manager.get_current_mode()
        logger.debug(f"📍 Loading coordinates for all agents (mode: {current_mode}, {len(active_agents)} active)")
    except Exception as e:
        logger.warning(f"⚠️ Could not load mode manager: {e}")
        active_agents = None
    
    agents: dict[str, dict[str, Any]] = {}
    for agent_id, info in data.get("agents", {}).items():
        # FIXED: Always load coordinates for all agents, even if inactive
        # This allows Discord messages to inactive agents (e.g., agents 5-8 in 4-agent mode)
        # Mode filtering only affects processing order, not message delivery
        # CRITICAL: chat_input_coordinates is the PRIMARY chat input field
        chat = info.get("chat_input_coordinates", [0, 0])
        # onboarding_input_coords is ONLY for onboarding messages
        onboarding = info.get("onboarding_input_coords", chat)  # Fallback to chat if not present
        
        # DEFENSIVE CHECK: Verify coordinates are different (except for fallback cases)
        # - Agent-4 might have same coords (legacy/edge case)
        # - Discord intentionally uses [0,0] as sentinel value: indicates API-based delivery
        #   (Discord is primarily a sender via bot API, not a PyAutoGUI coordinate recipient)
        #   When coordinates are [0,0], system falls back to inbox file-based delivery
        if chat == onboarding and agent_id not in ("Agent-4", "Discord"):
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"⚠️ {agent_id}: chat and onboarding coords are the same: {chat}")
        
        agents[agent_id] = {
            "coords": tuple(chat),  # CRITICAL: This is chat_input_coordinates - NEVER swap with onboarding
            "onboarding_coords": tuple(onboarding),  # This is onboarding_input_coords - separate field
            "x": chat[0],
            "y": chat[1],
            "description": info.get("description", ""),
        }
        
        # CRITICAL VERIFICATION: Log for Agent-4 to catch any bugs
        if agent_id == "Agent-4":
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"✅ Agent-4 coordinates loaded: chat={agents[agent_id]['coords']}, onboarding={agents[agent_id]['onboarding_coords']}")
    
    return agents


COORDINATES: dict[str, dict[str, Any]] = _load_coordinates()


class CoordinateLoader:
    """Mock coordinate loader for testing."""

    def __init__(self):
        """Initialize coordinate loader."""
        self.coordinates = COORDINATES.copy()
        self._last_load_time = None
    
    def _reload_coordinates(self):
        """Reload coordinates from SSOT file to ensure we have latest values."""
        try:
            global COORDINATES
            COORDINATES = _load_coordinates()
            self.coordinates = COORDINATES.copy()
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"🔄 Reloaded coordinates from SSOT")
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"⚠️ Failed to reload coordinates: {e}")

    def get_all_agents(self) -> list[str]:
        """Get all agent IDs."""
        return list(self.coordinates.keys())

    def is_agent_active(self, agent_id: str) -> bool:
        """Check if agent is active."""
        return agent_id in self.coordinates

    def get_chat_coordinates(self, agent_id: str) -> tuple[int, int]:
        """Get chat coordinates for agent.
        
        CRITICAL: Always returns chat_input_coordinates, NEVER onboarding coordinates.
        """
        # Map CAPTAIN to Agent-4
        if agent_id.upper() == "CAPTAIN":
            agent_id = "Agent-4"
        
        # Reload coordinates to ensure we have latest values
        self._reload_coordinates()
        if agent_id in self.coordinates:
            # CRITICAL FIX: Always use "coords" which is chat_input_coordinates
            # Never use onboarding_coords here
            coords = self.coordinates[agent_id]["coords"]
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"📍 Chat coordinates for {agent_id}: {coords}")
            
            # DEFENSIVE CHECK: Verify we're not accidentally returning onboarding coords
            onboarding_coords = self.coordinates[agent_id].get("onboarding_coords")
            if coords == onboarding_coords:
                logger.error(f"❌ CRITICAL BUG: get_chat_coordinates returned onboarding coords for {agent_id}!")
                logger.error(f"   Chat coords should be: {coords}, Onboarding: {onboarding_coords}")
                # Force reload and try again
                self._reload_coordinates()
                coords = self.coordinates[agent_id]["coords"]
            
            return coords
        raise ValueError(f"No coordinates found for agent {agent_id}")

    def get_onboarding_coordinates(self, agent_id: str) -> tuple[int, int]:
        """Get onboarding coordinates for agent."""
        # Map CAPTAIN to Agent-4
        if agent_id.upper() == "CAPTAIN":
            agent_id = "Agent-4"
        # Reload coordinates to ensure we have latest values
        self._reload_coordinates()
        if agent_id in self.coordinates:
            coords = self.coordinates[agent_id]["onboarding_coords"]
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"📍 Onboarding coordinates for {agent_id}: {coords}")
            return coords
        raise ValueError(f"No onboarding coordinates found for agent {agent_id}")

    def get_agent_description(self, agent_id: str) -> str:
        """Get agent description."""
        if agent_id in self.coordinates:
            return self.coordinates[agent_id].get("description", "")
        return ""

    def get_agent_info(self, agent_id: str) -> dict | None:
        """Get agent information."""
        return self.coordinates.get(agent_id)


# Global coordinate loader instance
_coordinate_loader = None


def get_coordinate_loader() -> CoordinateLoader:
    """Get global coordinate loader instance."""
    global _coordinate_loader
    if _coordinate_loader is None:
        _coordinate_loader = CoordinateLoader()
    return _coordinate_loader
