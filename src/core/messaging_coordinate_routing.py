#!/usr/bin/env python3
"""
Coordinate Routing Service
===========================

<!-- SSOT Domain: communication -->

Service for coordinate selection and routing logic for PyAutoGUI message delivery.
Extracted from messaging_pyautogui.py as part of Phase 2A Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~200 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
from typing import Tuple, Optional
from .coordinate_loader import get_coordinate_loader
from .messaging_models_core import UnifiedMessageType

logger = logging.getLogger(__name__)


class CoordinateRoutingService:
    """
    Service for coordinate selection and routing logic.
    
    Handles:
    - Coordinate selection based on message type
    - Agent-4 special case handling
    - Onboarding vs chat coordinate routing
    """
    
    # Hardcoded Agent-4 coordinates (from cursor_agent_coords.json)
    AGENT4_CHAT_COORDS = (-308, 1000)
    AGENT4_ONBOARDING_COORDS = (-304, 680)
    
    def __init__(self):
        """Initialize coordinate routing service."""
        self.coord_loader = get_coordinate_loader()
        logger.debug("CoordinateRoutingService initialized")
    
    def get_coordinates_for_message(
        self, 
        message, 
        sender: str
    ) -> Optional[Tuple[int, int]]:
        """
        Get coordinates for message delivery based on message type and recipient.
        
        Args:
            message: UnifiedMessage object
            sender: Message sender identifier
            
        Returns:
            Tuple of (x, y) coordinates or None if coordinates not found
        """
        recipient = message.recipient
        message_type = message.message_type
        message_type_str = str(message_type)
        
        logger.info(f"🔍 Message type for {recipient}: {message_type_str} (enum: {message_type})")
        
        # Get both coordinate sets for verification
        chat_coords_expected = self.coord_loader.get_chat_coordinates(recipient)
        onboarding_coords_check = self.coord_loader.get_onboarding_coordinates(recipient)
        
        # Agent-4 special handling with hardcoded coordinates
        if recipient == "Agent-4":
            return self._handle_agent4_routing(
                message, 
                sender, 
                chat_coords_expected, 
                onboarding_coords_check,
                message_type_str
            )
        
        # Agent-2 special handling
        elif recipient == "Agent-2":
            return self._handle_agent2_routing(
                message,
                chat_coords_expected,
                onboarding_coords_check,
                message_type_str
            )
        
        # All other agents: Use onboarding coords ONLY for ONBOARDING type
        elif message_type == UnifiedMessageType.ONBOARDING:
            coords = onboarding_coords_check
            logger.info(f"📍 {recipient}: Using ONBOARDING coordinates (explicit ONBOARDING type): {coords}")
            return coords
        else:
            coords = chat_coords_expected
            logger.info(f"📍 {recipient}: Using CHAT coordinates (type: {message_type_str}): {coords}")
            return coords
    
    def _handle_agent4_routing(
        self, message, sender: str, chat_coords: Tuple[int, int], onboarding_coords: Tuple[int, int], message_type_str: str
    ) -> Tuple[int, int]:
        """Handle Agent-4 coordinate routing with hardcoded overrides."""
        # Use hardcoded if loader mismatch
        if chat_coords != self.AGENT4_CHAT_COORDS: chat_coords = self.AGENT4_CHAT_COORDS
        if onboarding_coords != self.AGENT4_ONBOARDING_COORDS: onboarding_coords = self.AGENT4_ONBOARDING_COORDS
        
        is_onboarding = self._is_onboarding_message(message)
        is_discord = self._is_discord_message(message)
        
        # Discord or non-onboarding always uses chat coords
        if is_discord or not is_onboarding:
            coords = chat_coords
            logger.info(f"📍 Agent-4: Using chat coordinates (discord={is_discord})")
        else:
            coords = onboarding_coords
            logger.info(f"📍 Agent-4: Using onboarding coordinates")
            
        return coords
    
    def _handle_agent2_routing(
        self, message, chat_coords: Tuple[int, int], onboarding_coords: Tuple[int, int], message_type_str: str
    ) -> Tuple[int, int]:
        """Handle Agent-2 coordinate routing."""
        if message.message_type == UnifiedMessageType.ONBOARDING:
            return onboarding_coords
        return chat_coords

    def _is_onboarding_message(self, message) -> bool:
        """Check if message is of ONBOARDING type."""
        m_type = message.message_type
        if hasattr(m_type, 'value'): return m_type.value == "onboarding" or m_type == UnifiedMessageType.ONBOARDING
        return str(m_type).lower() == "onboarding" or m_type == UnifiedMessageType.ONBOARDING
    
    def _is_discord_message(self, message) -> bool:
        """Check if message is from Discord source."""
        if not hasattr(message, 'metadata') or not isinstance(message.metadata, dict): return False
        source = str(message.metadata.get("source", "")).lower()
        return "discord" in source or message.metadata.get("discord_user_id") is not None
    
    def validate_coordinates(self, agent_id: str, coords: Tuple[int, int]) -> bool:
        """
        Validate coordinates before sending with comprehensive checks.

        Args:
            agent_id: Agent identifier
            coords: Coordinate tuple (x, y)

        Returns:
            True if coordinates are valid
        """
        if not coords or len(coords) != 2:
            logger.error(f"❌ Invalid coordinates for {agent_id}: {coords}")
            return False

        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(f"❌ Coordinates must be numeric for {agent_id}: ({x}, {y})")
            return False

        # Platform-accurate bounds check: validate against the OS virtual screen bounds.
        try:
            from .utilities.validation_utilities import get_virtual_screen_bounds
            min_x, min_y, max_x, max_y = get_virtual_screen_bounds()
            if x < min_x or x > max_x:
                logger.error(
                    f"❌ X coordinate out of virtual screen bounds for {agent_id}: {x} "
                    f"(bounds: {min_x}..{max_x}). Re-capture coords in cursor_agent_coords.json."
                )
                return False
            if y < min_y or y > max_y:
                logger.error(
                    f"❌ Y coordinate out of virtual screen bounds for {agent_id}: {y} "
                    f"(bounds: {min_y}..{max_y}). Re-capture coords in cursor_agent_coords.json."
                )
                return False
        except Exception as e:
            logger.debug(f"Virtual screen bounds check unavailable: {e}")

        # Validate against bounds from cursor_agent_coords.json
        try:
            # Get expected coordinates for this agent
            expected_chat_coords = self.coord_loader.get_chat_coordinates(agent_id)
            expected_onboarding_coords = self.coord_loader.get_onboarding_coordinates(agent_id)
            
            # Check if coords match expected (within tolerance for screen variations)
            coords_match = (
                coords == expected_chat_coords or 
                coords == expected_onboarding_coords or
                (abs(x - expected_chat_coords[0]) <= 5 and abs(y - expected_chat_coords[1]) <= 5) or
                (abs(x - expected_onboarding_coords[0]) <= 5 and abs(y - expected_onboarding_coords[1]) <= 5)
            )
            
            if not coords_match:
                logger.warning(
                    f"⚠️ Coordinate mismatch for {agent_id}: got {coords}, "
                    f"expected chat={expected_chat_coords} or onboarding={expected_onboarding_coords}"
                )
            
            # Legacy coarse bounds (kept as a final backstop)
            if x < -5000 or x > 5000:
                logger.error(f"❌ X coordinate out of coarse bounds for {agent_id}: {x} (expected -5000..5000)")
                return False
            if y < -2000 or y > 5000:
                logger.error(f"❌ Y coordinate out of coarse bounds for {agent_id}: {y} (expected -2000..5000)")
                return False
            
            logger.debug(f"✅ Coordinates validated for {agent_id}: {coords}")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Could not validate coordinates against SSOT: {e}, using basic validation")
            return True

    def validate_coordinate_selection(
        self,
        recipient: str,
        coords: Optional[Tuple[int, int]]
    ) -> bool:
        """
        Validate coordinate selection.
        
        Args:
            recipient: Agent recipient ID
            coords: Selected coordinates tuple
            
        Returns:
            True if coordinates are valid
        """
        if coords is None:
            logger.error(f"❌ No coordinates selected for {recipient}")
            return False
        
        if not isinstance(coords, tuple) or len(coords) != 2:
            logger.error(f"❌ Invalid coordinate format for {recipient}: {coords}")
            return False
        
        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            logger.error(
                f"❌ Invalid coordinate types for {recipient}: "
                f"x={type(x)}, y={type(y)}"
            )
            return False
        
        return True

