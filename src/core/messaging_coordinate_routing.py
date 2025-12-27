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
        self,
        message,
        sender: str,
        chat_coords_expected: Tuple[int, int],
        onboarding_coords_check: Tuple[int, int],
        message_type_str: str
    ) -> Tuple[int, int]:
        """
        Handle Agent-4 coordinate routing with hardcoded coordinates.
        
        CRITICAL: Agent-4 ALWAYS uses chat coordinates unless EXPLICITLY ONBOARDING type.
        This includes Discord messages, CAPTAIN_TO_AGENT, SYSTEM_TO_AGENT, etc.
        """
        # Verify loader returned correct coords
        if chat_coords_expected != self.AGENT4_CHAT_COORDS:
            logger.warning(
                f"⚠️ Agent-4 chat coords mismatch! Loader: {chat_coords_expected}, "
                f"Expected: {self.AGENT4_CHAT_COORDS}. Using hardcoded."
            )
            chat_coords_expected = self.AGENT4_CHAT_COORDS
        
        if onboarding_coords_check != self.AGENT4_ONBOARDING_COORDS:
            logger.warning(
                f"⚠️ Agent-4 onboarding coords mismatch! Loader: {onboarding_coords_check}, "
                f"Expected: {self.AGENT4_ONBOARDING_COORDS}. Using hardcoded."
            )
            onboarding_coords_check = self.AGENT4_ONBOARDING_COORDS
        
        logger.info(
            f"✅ Agent-4 coordinates verified: "
            f"Chat={chat_coords_expected}, Onboarding={onboarding_coords_check}"
        )
        
        # Check if message is onboarding type
        is_onboarding_type = self._is_onboarding_message(message)
        
        # Check if Discord message
        is_discord_message = self._is_discord_message(message)
        
        if is_discord_message:
            logger.info(f"📍 Agent-4: Discord message detected - forcing chat coordinates")
            metadata = message.metadata if isinstance(message.metadata, dict) else {}
            logger.info(
                f"📍 Agent-4: Metadata source: {metadata.get('source', 'N/A')}"
            )
        
        # ONLY use onboarding coords if EXPLICITLY ONBOARDING type
        if is_onboarding_type:
            coords = self.AGENT4_ONBOARDING_COORDS
            logger.info(
                f"📍 Agent-4: Using ONBOARDING coordinates "
                f"(EXPLICIT ONBOARDING type confirmed): {coords}"
            )
        else:
            # ALL other message types for Agent-4 use chat coordinates - NO EXCEPTIONS
            coords = self.AGENT4_CHAT_COORDS
            logger.info(
                f"📍 Agent-4: FORCING hardcoded chat coordinates "
                f"(type: {message_type_str}, sender: {sender}, is_discord: {is_discord_message}): {coords}"
            )
            logger.info(
                f"📍 Agent-4: ABSOLUTE OVERRIDE - Chat coords hardcoded to prevent routing errors"
            )
        
        # Final verification for Agent-4
        return self._finalize_agent4_coordinates(message, coords, message_type_str)
    
    def _handle_agent2_routing(
        self,
        message,
        chat_coords_expected: Tuple[int, int],
        onboarding_coords_check: Tuple[int, int],
        message_type_str: str
    ) -> Tuple[int, int]:
        """Handle Agent-2 coordinate routing."""
        if message.message_type == UnifiedMessageType.ONBOARDING:
            coords = onboarding_coords_check
            logger.info(
                f"📍 Agent-2: Using ONBOARDING coordinates "
                f"(explicit ONBOARDING type): {coords}"
            )
        else:
            coords = chat_coords_expected
            logger.info(
                f"📍 Agent-2: Using chat coordinates (type: {message_type_str}): {coords}"
            )
            # Defensive check
            if coords == onboarding_coords_check:
                logger.error(
                    f"❌ CRITICAL BUG: Agent-2 non-ONBOARDING message selected "
                    f"onboarding coords! FORCING chat coords."
                )
                coords = chat_coords_expected
        
        return coords
    
    def _finalize_agent4_coordinates(
        self,
        message,
        coords: Tuple[int, int],
        message_type_str: str
    ) -> Tuple[int, int]:
        """
        Final verification and hardcoded override for Agent-4 coordinates.
        
        CRITICAL: Absolute hardcoded override to prevent routing errors.
        """
        # Re-check onboarding type status
        final_is_onboarding = self._is_onboarding_message(message)
        
        # Re-check Discord source
        final_is_discord = self._is_discord_message(message)
        
        logger.info(f"🔍 Agent-4 FINAL VERIFICATION:")
        logger.info(f"   - Final is_onboarding check: {final_is_onboarding}")
        logger.info(f"   - Final is_discord check: {final_is_discord}")
        logger.info(f"   - Selected coords: {coords}")
        logger.info(f"   - Hardcoded chat: {self.AGENT4_CHAT_COORDS}")
        logger.info(f"   - Hardcoded onboarding: {self.AGENT4_ONBOARDING_COORDS}")
        
        # CRITICAL: Discord messages ALWAYS use chat coordinates
        if final_is_discord:
            if coords != self.AGENT4_CHAT_COORDS:
                logger.error(
                    f"❌ CRITICAL ROUTING ERROR: Agent-4 Discord message using wrong coords!"
                )
                logger.error(
                    f"   Expected hardcoded chat: {self.AGENT4_CHAT_COORDS}, Got: {coords}"
                )
                coords = self.AGENT4_CHAT_COORDS
                logger.warning(
                    f"⚠️ ABSOLUTE OVERRIDE: Agent-4 Discord message forced to "
                    f"chat coordinates: {coords}"
                )
            else:
                logger.info(
                    f"✅ Agent-4 Discord message verified: Using chat coordinates"
                )
        elif not final_is_onboarding:
            # ABSOLUTE OVERRIDE: Force hardcoded chat coords for Agent-4 if not onboarding
            if coords != self.AGENT4_CHAT_COORDS:
                logger.error(
                    f"❌ CRITICAL ROUTING ERROR: Agent-4 non-ONBOARDING message "
                    f"using wrong coords!"
                )
                logger.error(
                    f"   Expected hardcoded chat: {self.AGENT4_CHAT_COORDS}, Got: {coords}"
                )
                logger.error(f"   Message type: {message.message_type}, "
                           f"Message type str: {message_type_str}")
                logger.error(f"   Is onboarding check: {final_is_onboarding}")
                coords = self.AGENT4_CHAT_COORDS
                logger.warning(
                    f"⚠️ ABSOLUTE HARDCODED OVERRIDE: Agent-4 routing fixed - "
                    f"using hardcoded chat coordinates: {coords}"
                )
            else:
                logger.info(
                    f"✅ Agent-4 routing verified: Using hardcoded chat coordinates "
                    f"for non-ONBOARDING message"
                )
        else:
            # Verify onboarding coords match hardcoded
            if coords != self.AGENT4_ONBOARDING_COORDS:
                logger.warning(
                    f"⚠️ Agent-4 ONBOARDING coords mismatch, using hardcoded: "
                    f"{self.AGENT4_ONBOARDING_COORDS}"
                )
                coords = self.AGENT4_ONBOARDING_COORDS
        
        return coords
    
    def _is_onboarding_message(self, message) -> bool:
        """Check if message is of ONBOARDING type."""
        message_type = message.message_type
        
        if hasattr(message_type, 'value'):
            return message_type.value == "onboarding" or \
                   message_type == UnifiedMessageType.ONBOARDING
        elif isinstance(message_type, str):
            return message_type.lower() == "onboarding"
        else:
            return message_type == UnifiedMessageType.ONBOARDING
    
    def _is_discord_message(self, message) -> bool:
        """Check if message is from Discord source."""
        if not hasattr(message, 'metadata') or not isinstance(message.metadata, dict):
            return False
        
        metadata = message.metadata
        source = metadata.get("source", "")
        
        return (
            source == "discord" or
            source == "DISCORD" or
            "discord" in str(source).lower() or
            metadata.get("discord_user_id") is not None or
            metadata.get("discord_username") is not None
        )
    
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

