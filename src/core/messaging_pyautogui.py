#!/usr/bin/env python3
"""
PyAutoGUI Messaging Delivery
Sends messages to agent chat input coordinates using PyAutoGUI

<!-- SSOT Domain: communication -->

RACE CONDITION FIXES (2025-10-15):
- Clipboard locking to prevent concurrent overwrites
- Increased delays (0.5s→1.0s) for slow systems
- 3-attempt retry mechanism for reliability

CRITICAL FIX (2025-01-27): Global keyboard control lock
- Prevents "9 ppl controlling my keyboard" scenario
- Synchronizes Discord + computer + agents
- Single lock for entire PyAutoGUI operation sequence
"""

import logging
import time
import threading

# Import global keyboard control lock
from .keyboard_control_lock import keyboard_control
from typing import Dict, List, Callable, Any, Optional, Union, Tuple, Set

# Import service modules (Phase 2A refactoring)
from .messaging_coordinate_routing import CoordinateRoutingService
from .messaging_formatting import MessageFormattingService
from .messaging_clipboard import ClipboardService
from .messaging_pyautogui_operations import PyAutoGUIOperationsService

logger = logging.getLogger(__name__)

# RACE CONDITION FIX #1: Global clipboard lock
_clipboard_lock = threading.Lock()

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False


class PyAutoGUIMessagingDelivery:
    """Delivers messages via PyAutoGUI to agent chat coordinates."""

    def __init__(self):
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI not available")
        self.pyautogui = pyautogui
        
        # Initialize service modules (Phase 2A refactoring)
        self.coordinate_service = CoordinateRoutingService()
        self.formatting_service = MessageFormattingService()
        self.clipboard_service = ClipboardService()
        self.operations_service = PyAutoGUIOperationsService(pyautogui_module=pyautogui)

    def validate_coordinates(self, agent_id: str, coords: tuple[int, int]) -> bool:
        """
        Validate coordinates using CoordinateRoutingService.
        """
        return self.coordinate_service.validate_coordinates(agent_id, coords)

    def send_message(self, message) -> bool:
        """
        Send message to agent chat input coordinates.
        
        RACE CONDITION FIXES:
        - Clipboard locking (prevents concurrent overwrites)
        - Increased delays (1.0s for slow systems)
        - 3-attempt retry mechanism
        
        CRITICAL FIX: Handles both dict and UnifiedMessage object formats.
        """
        # Extract recipient for logging (handles both dict and object)
        recipient = None
        if isinstance(message, dict):
            recipient = message.get('recipient') or message.get('to', 'UNKNOWN')
        elif hasattr(message, 'recipient'):
            recipient = message.recipient
        else:
            recipient = 'UNKNOWN'
        
        # RACE CONDITION FIX #3: Retry mechanism (3 attempts)
        for attempt in range(3):
            try:
                success = self._send_message_attempt(message, attempt + 1)
                if success:
                    return True
                
                # Wait before retry
                if attempt < 2:
                    logger.warning(f"⚠️ Retry {attempt + 1}/3 for {recipient}")
                    time.sleep(1.0)
            
            except Exception as e:
                logger.error(
                    f"❌ Attempt {attempt + 1} failed for {recipient}: {e}",
                    exc_info=True
                )
                if attempt < 2:
                    time.sleep(1.0)
        
        logger.error(
            f"❌ All 3 attempts failed for {recipient} - message not delivered",
            exc_info=False
        )
        return False
    
    def _send_message_attempt(self, message, attempt_num: int) -> bool:
        """Single message delivery attempt with all race condition fixes."""
        # Normalize message to UnifiedMessage object using FormattingService
        message = self.formatting_service.normalize_message(message)
        if not message:
            return False

        # Get sender for lock identifier
        sender = message.sender
        if isinstance(message.metadata, dict):
            sender = message.metadata.get('sender', sender)
        
        # CRITICAL: Check if keyboard lock is already held
        from .keyboard_control_lock import is_locked
        lock_already_held = is_locked()
        
        # CRITICAL: Global keyboard control lock
        source = message.metadata.get('source', 'unknown') if isinstance(message.metadata, dict) else 'unknown'
        lock_source = f"{source}:{sender}:{message.recipient}"
        
        if lock_already_held:
            logger.debug(f"🔒 Keyboard lock already held, skipping for {message.recipient}")
            return self._execute_delivery_operations(message, attempt_num, sender)
        else:
            with keyboard_control(lock_source):
                return self._execute_delivery_operations(message, attempt_num, sender)
    
    def _execute_delivery_operations(self, message, attempt_num: int, sender: str) -> bool:
        """Execute the actual PyAutoGUI delivery operations (no lock management)."""
        try:
            coords = self.coordinate_service.get_coordinates_for_message(message, sender)
            if not coords:
                logger.error(f"No coordinates for {message.recipient}")
                return False

            x, y = coords
            msg_content = self.formatting_service.format_message_content(message, sender)

            # Execute PyAutoGUI operations
            if not self.operations_service.move_to_coordinates(
                (x, y), message.recipient, validate_callback=self.validate_coordinates
            ):
                return False
            
            self.operations_service.focus_input_field(message.recipient, (x, y))
            self.operations_service.clear_input_field(message.recipient)
            self.operations_service.verify_coordinates_before_paste(message.recipient, (x, y))
            
            # Final focus check
            try:
                import pyautogui
                pyautogui.click(x, y)
                time.sleep(0.3)
            except Exception: pass
            
            # Copy and paste
            if not self.clipboard_service.copy_to_clipboard(msg_content):
                return False
                
            if not self.operations_service.paste_content(message.recipient, (x, y), self.clipboard_service):
                return False
            
            # Send and verify
            message_metadata = message.metadata if isinstance(message.metadata, dict) else {}
            if not self.operations_service.send_message(message.recipient, message_metadata):
                return False
            
            self.operations_service.verify_send_completion(message.recipient, (x, y))
            logger.info(f"✅ Sent to {message.recipient} at {coords} (attempt {attempt_num})")
            return True

        except Exception as e:
            logger.error(f"❌ Delivery failed for {message.recipient}: {e}", exc_info=True)
            return False


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Legacy function for sending messages via PyAutoGUI."""
    try:
        delivery = PyAutoGUIMessagingDelivery()
        from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType

        msg = UnifiedMessage(
            content=message,
            sender="CAPTAIN",
            recipient=agent_id,
            message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[],
            metadata={},
        )
        return delivery.send_message(msg)
    except Exception as e:
        logger.error(f"Failed to send PyAutoGUI message: {e}")
        return False


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send message to onboarding coordinates."""
    return send_message_pyautogui(agent_id, message, timeout)


def send_message_to_agent(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Alias for send_message_pyautogui for backward compatibility."""
    return send_message_pyautogui(agent_id, message, timeout)
