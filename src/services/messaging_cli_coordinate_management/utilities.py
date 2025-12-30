"""
<!-- SSOT Domain: integration -->

Coordinate Management Utilities
==============================

Utility functions for loading and managing agent coordinates.

Uses SSOT coordinate loader (get_coordinate_loader()) to ensure
single source of truth for coordinate data.
"""

from typing import Any
from ...core.coordinate_loader import get_coordinate_loader


def load_coords_file() -> dict[str, Any]:
    """
    Load agent coordinates using SSOT coordinate loader.

    Returns:
        Dictionary of agent coordinates in format:
        {agent_id: {'x': x, 'y': y, 'description': str, 'active': bool}}
    """
    try:
        # Use SSOT coordinate loader
        coord_loader = get_coordinate_loader()
        all_agents = coord_loader.get_all_agents()
        
        # Transform to expected format
        result = {}
        for agent_id in all_agents:
            try:
                chat_coords = coord_loader.get_chat_coordinates(agent_id)
                
                result[agent_id] = {
                    "x": chat_coords[0],
                    "y": chat_coords[1],
                    "description": coord_loader.get_agent_description(agent_id),
                    "active": coord_loader.is_agent_active(agent_id),
                }
            except (ValueError, KeyError) as e:
                # Fallback for missing coordinates
                result[agent_id] = {
                    "x": 0,
                    "y": 0,
                    "description": "",
                    "active": False,
                }
        
        return result

    except Exception as e:
        print(f"Error loading coordinates: {e}")
        return {}
