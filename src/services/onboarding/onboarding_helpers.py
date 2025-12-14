#!/usr/bin/env python3
"""
Onboarding Helpers Module
=========================

<!-- SSOT Domain: integration -->

Helper functions for onboarding operations:
- Coordinate loading and validation
- Message formatting utilities
- Common onboarding operations

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def load_agent_coordinates(agent_id: str) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
    """
    Load chat and onboarding coordinates for agent.
    
    Args:
        agent_id: Target agent ID
        
    Returns:
        Tuple of (chat_coords, onboarding_coords) or (None, None) if not found
    """
    try:
        from ...core.coordinate_loader import get_coordinate_loader
        
        coord_loader = get_coordinate_loader()
        chat_coords = coord_loader.get_chat_coordinates(agent_id)
        onboarding_coords = coord_loader.get_onboarding_coordinates(agent_id)
        
        return chat_coords, onboarding_coords
    except Exception as e:
        logger.error(f"Failed to load coordinates for {agent_id}: {e}")
        return None, None


def validate_coordinates(agent_id: str, coords: Tuple[int, int]) -> bool:
    """
    Validate coordinates before sending.
    
    Args:
        agent_id: Target agent ID
        coords: Coordinates to validate
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    try:
        from ...core.messaging_pyautogui import PyAutoGUIMessagingDelivery
        
        delivery = PyAutoGUIMessagingDelivery()
        return delivery.validate_coordinates(agent_id, coords)
    except Exception as e:
        logger.error(f"Failed to validate coordinates for {agent_id}: {e}")
        return False


def validate_onboarding_coordinates(agent_id: str, coords: Tuple[int, int]) -> bool:
    """
    Validate onboarding coordinates (bounds check only).
    
    Args:
        agent_id: Target agent ID
        coords: Coordinates to validate
        
    Returns:
        True if coordinates are within bounds, False otherwise
    """
    x, y = coords
    
    # Simple bounds check
    if x < -2000 or x > 2000 or y < 0 or y > 1500:
        logger.error(
            f"Onboarding coordinates out of bounds for {agent_id}: {coords}"
        )
        return False
    
    return True

