"""
Shared Coordinate Management
=============================

Provides coordinate loading and validation for onboarding services.
Wraps existing onboarding_helpers for consistency.

V2 Compliant: < 100 lines
"""

import logging
from typing import Optional, Tuple

from ..onboarding_helpers import (
    load_agent_coordinates,
    validate_coordinates,
    validate_onboarding_coordinates,
)

logger = logging.getLogger(__name__)


class OnboardingCoordinates:
    """Coordinate management for onboarding services."""
    
    def load_coordinates(self, agent_id: str) -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        """
        Load chat and onboarding coordinates for agent.
        
        Args:
            agent_id: Target agent ID
            
        Returns:
            Tuple of (chat_coords, onboarding_coords) or (None, None) if not found
        """
        try:
            return load_agent_coordinates(agent_id)
        except Exception as e:
            logger.error(f"Failed to load coordinates for {agent_id}: {e}")
            return None, None
    
    def validate_coordinates(self, agent_id: str, coords: Tuple[int, int]) -> bool:
        """
        Validate coordinates before sending.
        
        Args:
            agent_id: Target agent ID
            coords: Coordinates to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            return validate_coordinates(agent_id, coords)
        except Exception as e:
            logger.error(f"Failed to validate coordinates for {agent_id}: {e}")
            return False
    
    def validate_onboarding_coordinates(self, agent_id: str, coords: Tuple[int, int]) -> bool:
        """
        Validate onboarding coordinates specifically.
        
        Args:
            agent_id: Target agent ID
            coords: Onboarding coordinates to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            return validate_onboarding_coordinates(agent_id, coords)
        except Exception as e:
            logger.error(f"Failed to validate onboarding coordinates for {agent_id}: {e}")
            return False

