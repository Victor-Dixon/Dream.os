"""
<!-- SSOT Domain: core -->

Message Bus Port - Domain Layer
================================

Port (interface) for message bus implementation.
Defines the contract for publishing and subscribing to domain events.

V2 Compliance: < 300 lines, single responsibility.
Repository Pattern: Port interface for hexagonal architecture.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-03
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional
from collections.abc import Iterable


class MessageBus(ABC):
    """
    Message bus port for publishing and subscribing to domain events.
    
    This is a port (interface) in hexagonal architecture that defines
    the contract for message bus implementations in the infrastructure layer.
    
    V2 Compliance: Interface-only, < 300 lines, single responsibility.
    Design Pattern: Port-Adapter pattern (hexagonal architecture).
    """

    @abstractmethod
    def publish(
        self, 
        event_type: str, 
        event_data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Publish a domain event to all subscribers.
        
        Args:
            event_type: Type of event (e.g., "task.assigned", "agent.status_changed")
            event_data: Event data dictionary
            metadata: Optional metadata (timestamp, source, etc.)
        
        Returns:
            True if published successfully, False otherwise
        
        Raises:
            ValueError: If event_type is empty or invalid
            RuntimeError: If message bus is not available
        """
        pass

    @abstractmethod
    def subscribe(
        self,
        event_type: str,
        handler: Callable[[str, Dict[str, Any]], None],
        handler_id: Optional[str] = None
    ) -> str:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type: Type of event to subscribe to (use "*" for all events)
            handler: Callback function(event_type, event_data) -> None
            handler_id: Optional unique identifier for the handler
        
        Returns:
            Handler ID (generated if not provided)
        
        Raises:
            ValueError: If event_type is empty or handler is not callable
        """
        pass

    @abstractmethod
    def unsubscribe(self, handler_id: str) -> bool:
        """
        Unsubscribe a handler from events.
        
        Args:
            handler_id: Unique identifier of the handler to remove
        
        Returns:
            True if handler was removed, False if not found
        
        Raises:
            ValueError: If handler_id is empty
        """
        pass

    @abstractmethod
    def get_subscribers(self, event_type: Optional[str] = None) -> Dict[str, list[str]]:
        """
        Get list of subscribers for event types.
        
        Args:
            event_type: Optional specific event type, or None for all
        
        Returns:
            Dictionary mapping event types to list of handler IDs
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if message bus is available and ready.
        
        Returns:
            True if message bus is available, False otherwise
        """
        pass

    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """
        Get message bus statistics.
        
        Returns:
            Dictionary with stats (total_events, subscribers_count, etc.)
        """
        pass
