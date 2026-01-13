"""
Coordinate Handler - V2 Compliance Module
========================================

Handles agent coordinate management and validation.
Extracted from messaging_cli_handlers_orchestrator.py for V2 compliance.
Migrated to BaseService for consolidated initialization and error handling.

<!-- SSOT Domain: integration -->

Author: Agent-7 - Web Development Specialist
License: MIT
"""
import logging
import time
from typing import Any
from ...core.base.base_service import BaseService
from ...core.coordinate_loader import get_coordinate_loader


class CoordinateHandler(BaseService):
    """Handler for agent coordinate management and validation."""

    def can_handle(self, args) ->bool:
        """Check if this handler can handle the given arguments."""
        return False

    def handle(self, args) ->bool:
        """Handle the command."""
        return False

    def __init__(self):
        """Initialize coordinate handler."""
        super().__init__("CoordinateHandler")
        self.coordinates_cache: dict[str, list[int]] = {}
        self.last_coordinate_load: float | None = None
        self.cache_ttl_seconds = 300

    async def load_coordinates_async(self, service=None) ->dict[str, Any]:
        """Load agent coordinates asynchronously with caching.

        Uses SSOT coordinate loader (get_coordinate_loader()) to ensure
        single source of truth for coordinate data.

        Args:
            service: Messaging service instance (optional)

        Returns:
            Dict containing coordinate data and success status
        """
        try:
            current_time = time.time()
            if (self.last_coordinate_load and self.coordinates_cache and
                current_time - self.last_coordinate_load < self.
                cache_ttl_seconds):
                return {'success': True, 'coordinates': self.
                    coordinates_cache, 'agent_count': len(self.
                    coordinates_cache), 'cached': True}
            
            # Use SSOT coordinate loader
            coord_loader = get_coordinate_loader()
            all_agents = coord_loader.get_all_agents()
            
            # Convert SSOT format to expected format: {agent_id: [x, y]}
            coordinates = {}
            for agent_id in all_agents:
                try:
                    chat_coords = coord_loader.get_chat_coordinates(agent_id)
                    # Convert tuple to list for compatibility
                    coordinates[agent_id] = [chat_coords[0], chat_coords[1]]
                except (ValueError, KeyError) as e:
                    self.logger.warning(f'Failed to get coordinates for {agent_id}: {e}')
                    coordinates[agent_id] = [0, 0]
            
            self.coordinates_cache = coordinates
            self.last_coordinate_load = current_time
            return {'success': True, 'coordinates': coordinates,
                'agent_count': len(coordinates), 'cached': False}
        except Exception as e:
            self.logger.error(f'Error loading coordinates: {e}')
            return {'success': False, 'error': str(e)}

    def print_coordinates_table(self, coordinates: dict[str, list[int]]
        ) ->None:
        """Print formatted coordinates table."""
        try:
            logger.info('\n📍 Agent Coordinates:')
            logger.info('=' * 40)
            logger.info(f"{'Agent':<12} {'X':<8} {'Y':<8}")
            logger.info('-' * 40)
            for agent_id, coords in sorted(coordinates.items()):
                x, y = coords if len(coords) >= 2 else [0, 0]
                logger.info(f'{agent_id:<12} {x:<8} {y:<8}')
            logger.info('=' * 40)
            logger.info(f'Total agents: {len(coordinates)}')
        except Exception as e:
            self.logger.error(f'Error printing coordinates table: {e}')

    def get_agent_coordinates(self, agent_id: str) ->(list[int] | None):
        """Get coordinates for specific agent."""
        return self.coordinates_cache.get(agent_id)

    def validate_coordinates(self, coordinates: list[int]) ->bool:
        """Validate coordinate format."""
        return isinstance(coordinates, list) and len(coordinates) >= 2 and all(
            isinstance(coord, (int, float)) for coord in coordinates[:2])

    def clear_cache(self) ->None:
        """Clear coordinate cache."""
        self.coordinates_cache.clear()
        self.last_coordinate_load = None
        self.logger.info('Coordinate cache cleared')
