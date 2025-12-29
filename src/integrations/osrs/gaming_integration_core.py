"""
<!-- SSOT Domain: core -->

Gaming Integration Core - SOLID Compliant Refactoring
====================================================

SOLID Compliant refactoring following V2 standards.
- SRP: Single Responsibility Principle - Each module has one responsibility
- OCP: Open-Closed Principle - Extension without modification of core classes
- LSP: Liskov Substitution Principle - Subtypes honor base contracts
- ISP: Interface Segregation Principle - Focused interfaces
- DIP: Dependency Inversion Principle - Depend on abstractions

Author: Agent-1 (SOLID Sentinel) - SOLID Enforcement
Original: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import logging
from datetime import datetime
from enum import Enum
from typing import Any, Protocol

logger = logging.getLogger(__name__)


# DIP: Abstract interfaces for dependency injection
class IGameSessionManager(Protocol):
    """Interface for game session management (ISP: Segregated interface)."""

    def create_session(self, game_type: str, player_id: str) -> dict[str, Any] | None: ...
    def get_session(self, session_id: str) -> dict[str, Any] | None: ...
    def end_session(self, session_id: str) -> bool: ...
    def get_active_sessions(self) -> list[dict[str, Any]]: ...


class IEntertainmentSystemManager(Protocol):
    """Interface for entertainment system management (ISP: Segregated interface)."""

    def register_system(self, system_id: str, system_type: str) -> bool: ...
    def get_system(self, system_id: str) -> dict[str, Any] | None: ...
    def get_all_systems(self) -> list[dict[str, Any]]: ...


class IIntegrationHandler(Protocol):
    """Interface for integration event handlers (ISP: Segregated interface)."""

    def handle_event(self, event: dict[str, Any]) -> dict[str, Any]: ...


# IntegrationStatus - Redirect to SSOT
# SSOT: src/architecture/system_integration.py
from src.architecture.system_integration import IntegrationStatus

# Gaming Classes - Redirect to SSOT
# SSOT: src/gaming/models/gaming_models.py
from src.gaming.models.gaming_models import (
    GameType,
    GameSession,
    EntertainmentSystem,
)

# Backward compatibility: Add to_dict() methods if needed
# Note: SSOT uses dataclasses, but some code may expect to_dict()
# This is handled by dataclass.asdict() or manual conversion where needed


# SRP: GameSessionManager handles only session-related operations
class GameSessionManager:
    """Game session manager - Single Responsibility: Session management."""

    def __init__(self):
        self.sessions: dict[str, GameSession] = {}

    def create_session(self, game_type: str, player_id: str) -> dict[str, Any] | None:
        """Create a new game session."""
        try:
            session_id = f"session_{int(datetime.now().timestamp())}"
            game_type_enum = GameType(game_type)
            # SSOT uses dataclass - create with all required fields
            session = GameSession(
                session_id=session_id,
                game_type=game_type_enum,
                player_id=player_id,
                start_time=datetime.now(),
                status="active",
                metadata={},
                performance_metrics={}
            )
            self.sessions[session_id] = session

            logger.info(f"Created game session: {session_id}")
            # Convert dataclass to dict using SSOT utility
            from src.core.utils.serialization_utils import to_dict
            return to_dict(session)
        except Exception as e:
            logger.error(f"Error creating game session: {e}")
            return None

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get game session."""
        from src.core.utils.serialization_utils import to_dict
        session = self.sessions.get(session_id)
        return to_dict(session) if session else None

    def end_session(self, session_id: str) -> bool:
        """End game session."""
        try:
            if session_id in self.sessions:
                session = self.sessions[session_id]
                session.status = "ended"
                logger.info(f"Ended game session: {session_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error ending game session: {e}")
            return False

    def get_active_sessions(self) -> list[dict[str, Any]]:
        """Get active game sessions."""
        from src.core.utils.serialization_utils import to_dict
        return [
            to_dict(session) for session in self.sessions.values() if session.status == "active"
        ]


# SRP: EntertainmentSystemManager handles only system-related operations
class EntertainmentSystemManager:
    """Entertainment system manager - Single Responsibility: System management."""

    def __init__(self):
        self.systems: dict[str, EntertainmentSystem] = {}

    def register_system(self, system_id: str, system_type: str) -> bool:
        """Register entertainment system."""
        try:
            from src.architecture.system_integration import IntegrationStatus
            # SSOT uses dataclass - create with all required fields
            system = EntertainmentSystem(
                system_id=system_id,
                system_type=system_type,
                status=IntegrationStatus.CONNECTED,
                capabilities=[],
                configuration={},
                last_updated=datetime.now()
            )
            self.systems[system_id] = system
            logger.info(f"Registered entertainment system: {system_id}")
            return True
        except Exception as e:
            logger.error(f"Error registering entertainment system: {e}")
            return False

    def get_system(self, system_id: str) -> dict[str, Any] | None:
        """Get entertainment system."""
        from src.core.utils.serialization_utils import to_dict
        system = self.systems.get(system_id)
        return to_dict(system) if system else None

    def get_all_systems(self) -> list[dict[str, Any]]:
        """Get all entertainment systems."""
        from src.core.utils.serialization_utils import to_dict
        return [to_dict(system) for system in self.systems.values()]


# SRP: IntegrationEventHandler handles only event processing
class IntegrationEventHandler:
    """Integration event handler - Single Responsibility: Event processing."""

    def __init__(self, session_manager: IGameSessionManager):
        self.session_manager = session_manager

    def handle_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Handle integration events."""
        try:
            event_type = event.get("type", "unknown")

            if event_type == "create_session":
                return self._handle_create_session(event)
            elif event_type == "end_session":
                return self._handle_end_session(event)
            elif event_type == "get_session":
                return self._handle_get_session(event)

            return {"success": False, "error": "Unknown event type"}
        except Exception as e:
            logger.error(f"Error handling event: {e}")
            return {"success": False, "error": str(e)}

    def _handle_create_session(self, event: dict[str, Any]) -> dict[str, Any]:
        """Handle session creation event."""
        game_type = event.get("game_type", "strategy")
        player_id = event.get("player_id", "unknown")
        session = self.session_manager.create_session(game_type, player_id)
        return {
            "success": session is not None,
            "session_id": session.get("session_id") if session else None,
        }

    def _handle_end_session(self, event: dict[str, Any]) -> dict[str, Any]:
        """Handle session end event."""
        session_id = event.get("session_id")
        return {"success": self.session_manager.end_session(session_id)}

    def _handle_get_session(self, event: dict[str, Any]) -> dict[str, Any]:
        """Handle session retrieval event."""
        session_id = event.get("session_id")
        session = self.session_manager.get_session(session_id)
        return {
            "success": session is not None,
            "session": session,
        }


# DIP & OCP: GamingIntegrationCore uses composition and dependency injection
class GamingIntegrationCore:
    """Gaming integration core - SOLID Compliant: Uses composition and interfaces."""

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        session_manager: IGameSessionManager | None = None,
        system_manager: IEntertainmentSystemManager | None = None,
    ):
        """Initialize with dependency injection."""
        self.config = config or {}
        self.status = IntegrationStatus.DISCONNECTED

        # DIP: Inject dependencies or use defaults
        self.session_manager = session_manager or GameSessionManager()
        self.system_manager = system_manager or EntertainmentSystemManager()

        # OCP: Event handlers can be extended without modifying core
        self.event_handlers: dict[str, IIntegrationHandler] = {}
        self.is_initialized = False

        self._initialize_integration()

    def _initialize_integration(self):
        """Initialize the integration system."""
        try:
            logger.info("Initializing Gaming Integration Core")
            self._setup_default_handlers()
            self._connect_to_systems()
            self.is_initialized = True
            self.status = IntegrationStatus.CONNECTED
        except Exception as e:
            logger.error(f"Error initializing gaming integration: {e}")
            self.status = IntegrationStatus.ERROR

    def _setup_default_handlers(self):
        """Setup default event handlers."""
        self.event_handlers["session_management"] = IntegrationEventHandler(self.session_manager)

    def _connect_to_systems(self):
        """Connect to gaming systems."""
        try:
            logger.info("Connecting to gaming systems")
            self.status = IntegrationStatus.CONNECTED
        except Exception as e:
            logger.error(f"Error connecting to systems: {e}")
            self.status = IntegrationStatus.ERROR

    # SRP: Delegate session operations to session manager
    def create_game_session(self, game_type: GameType, player_id: str) -> dict[str, Any] | None:
        """Create a new game session - delegates to session manager."""
        if not self.is_initialized:
            logger.warning("Gaming integration not initialized")
            return None
        # Handle both enum and string inputs
        game_type_str = game_type.value if hasattr(game_type, "value") else str(game_type)
        return self.session_manager.create_session(game_type_str, player_id)

    def get_game_session(self, session_id: str) -> dict[str, Any] | None:
        """Get game session - delegates to session manager."""
        return self.session_manager.get_session(session_id)

    def end_game_session(self, session_id: str) -> bool:
        """End game session - delegates to session manager."""
        return self.session_manager.end_session(session_id)

    def get_active_sessions(self) -> list[dict[str, Any]]:
        """Get active game sessions - delegates to session manager."""
        return self.session_manager.get_active_sessions()

    # SRP: Delegate system operations to system manager
    def register_entertainment_system(self, system_id: str, system_type: str) -> bool:
        """Register entertainment system - delegates to system manager."""
        return self.system_manager.register_system(system_id, system_type)

    def get_entertainment_system(self, system_id: str) -> dict[str, Any] | None:
        """Get entertainment system - delegates to system manager."""
        return self.system_manager.get_system(system_id)

    def get_all_entertainment_systems(self) -> list[dict[str, Any]]:
        """Get all entertainment systems - delegates to system manager."""
        return self.system_manager.get_all_systems()

    # OCP: Add event handler registration without modifying core
    def register_event_handler(self, name: str, handler: IIntegrationHandler) -> None:
        """Register event handler - Open-Closed Principle."""
        self.event_handlers[name] = handler

    def handle_event(self, handler_name: str, event: dict[str, Any]) -> dict[str, Any]:
        """Handle event using registered handler."""
        handler = self.event_handlers.get(handler_name)
        if handler:
            return handler.handle_event(event)
        return {"success": False, "error": f"Handler '{handler_name}' not found"}

    # LSP: Maintain backward compatibility while honoring new interface contracts
    def get_status(self) -> str:
        """Get integration status."""
        return self.status.value

    def is_connected(self) -> bool:
        """Check if integration is connected."""
        return self.status == IntegrationStatus.CONNECTED

    def get_core_health(self) -> dict[str, Any]:
        """Get core health status."""
        return {
            "status": self.get_status(),
            "initialized": self.is_initialized,
            "session_count": len(self.session_manager.get_active_sessions()),
            "system_count": len(self.system_manager.get_all_systems()),
            "handler_count": len(self.event_handlers),
        }


# Factory function for backward compatibility
def create_gaming_integration_core(config: dict[str, Any] | None = None) -> GamingIntegrationCore:
    """Factory function for creating GamingIntegrationCore instances."""
    return GamingIntegrationCore(config)


# Backward compatibility alias
GamingCore = GamingIntegrationCore
