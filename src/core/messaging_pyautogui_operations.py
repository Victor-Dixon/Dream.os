#!/usr/bin/env python3
"""
PyAutoGUI Operations Service
=============================

<!-- SSOT Domain: communication -->

Service for PyAutoGUI operations (move, click, paste, send) for message delivery.
Extracted from messaging_pyautogui.py as part of Phase 2A Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~200 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
import time
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("pyautogui not available - GUI operations disabled")


class PyAutoGUIOperationsService:
    """
    Service for PyAutoGUI operations.
    
    Handles:
    - Mouse movement with validation
    - Input field focusing and clearing
    - Content pasting
    - Message sending
    """
    
    def __init__(self, pyautogui_module=None):
        """
        Initialize PyAutoGUI operations service.
        
        Args:
            pyautogui_module: Optional pyautogui module (for dependency injection)
        """
        if pyautogui_module:
            self.pyautogui = pyautogui_module
        elif PYAUTOGUI_AVAILABLE:
            self.pyautogui = pyautogui
        else:
            self.pyautogui = None
            logger.warning("PyAutoGUIOperationsService initialized but pyautogui not available")
        
        logger.debug("PyAutoGUIOperationsService initialized")
    
    def move_to_coordinates(
        self,
        coordinates: Tuple[int, int],
        recipient: str,
        validate_callback=None
    ) -> bool:
        """
        Move mouse to coordinates with validation.
        
        Args:
            coordinates: Tuple of (x, y) coordinates
            recipient: Agent recipient ID (for logging)
            validate_callback: Optional callback to validate coordinates
            
        Returns:
            True if move successful
        """
        if not self.pyautogui:
            logger.error("Cannot move to coordinates - pyautogui not available")
            return False
        
        x, y = coordinates
        logger.debug(f"📍 Moving to coordinates: ({x}, {y})")
        
        self.pyautogui.moveTo(x, y, duration=0.5)
        
        # Validate coordinates after move
        current_mouse_pos = self.pyautogui.position()
        if validate_callback:
            coords_valid = validate_callback(recipient, (x, y))
            if not coords_valid:
                logger.error(
                    f"❌ Coordinate validation failed for {recipient} at ({x}, {y})"
                )
                return False
        
        # Verify mouse actually moved to target coordinates (within tolerance)
        distance = ((current_mouse_pos[0] - x) ** 2 + (current_mouse_pos[1] - y) ** 2) ** 0.5
        if distance > 10:  # Allow 10px tolerance for screen variations
            logger.warning(
                f"⚠️ Mouse position mismatch for {recipient}: "
                f"expected ({x}, {y}), got {current_mouse_pos}, distance={distance:.1f}px"
            )
            # Retry moveTo if too far off
            self.pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.2)
            current_mouse_pos = self.pyautogui.position()
            distance = ((current_mouse_pos[0] - x) ** 2 + (current_mouse_pos[1] - y) ** 2) ** 0.5
            if distance > 10:
                logger.error(
                    f"❌ Failed to move to coordinates for {recipient}: "
                    f"expected ({x}, {y}), still at {current_mouse_pos}"
                )
                return False
        
        return True
    
    def focus_input_field(self, recipient: str, coordinates: Tuple[int, int]) -> bool:
        """
        Focus input field by clicking at coordinates.
        
        Args:
            recipient: Agent recipient ID (for logging)
            coordinates: Tuple of (x, y) coordinates
            
        Returns:
            True if focus successful
        """
        if not self.pyautogui:
            return False
        
        x, y = coordinates
        
        # Click to focus window and input field
        logger.debug("🖱️ Clicking to focus input field")
        self.pyautogui.click()
        time.sleep(0.5)  # Wait for initial focus
        
        # Click again to ensure input field is active
        self.pyautogui.click()
        time.sleep(0.5)  # Wait for input field to be ready
        
        return True
    
    def clear_input_field(self, recipient: str) -> bool:
        """
        Clear existing text in input field.
        
        Args:
            recipient: Agent recipient ID (for logging)
            
        Returns:
            True if clear successful
        """
        if not self.pyautogui:
            return False
        
        # CRITICAL: Clear existing text in input field first
        logger.debug("🧹 Clearing existing text")
        self.pyautogui.hotkey("ctrl", "a")
        time.sleep(0.2)
        self.pyautogui.press("delete")
        time.sleep(0.3)
        
        return True
    
    def verify_coordinates_before_paste(
        self,
        recipient: str,
        coordinates: Tuple[int, int]
    ) -> bool:
        """
        Verify coordinates before pasting (final check).
        
        Args:
            recipient: Agent recipient ID (for logging)
            coordinates: Tuple of (x, y) coordinates
            
        Returns:
            True if coordinates valid
        """
        if not self.pyautogui:
            return False
        
        x, y = coordinates
        final_mouse_pos = self.pyautogui.position()
        final_distance = ((final_mouse_pos[0] - x) ** 2 + (final_mouse_pos[1] - y) ** 2) ** 0.5
        
        if final_distance > 10:
            logger.error(
                f"❌ CRITICAL: Mouse moved away before paste for {recipient}: "
                f"expected ({x}, {y}), got {final_mouse_pos}"
            )
            # Re-position before paste
            self.pyautogui.moveTo(x, y, duration=0.2)
            time.sleep(0.2)
            self.pyautogui.click()  # Re-focus
            time.sleep(0.3)
            return False
        
        return True
    
    def paste_content(
        self,
        recipient: str,
        coordinates: Tuple[int, int],
        clipboard_service
    ) -> bool:
        """
        Paste content from clipboard.
        
        Args:
            recipient: Agent recipient ID (for logging)
            coordinates: Tuple of (x, y) coordinates
            clipboard_service: ClipboardService instance
            
        Returns:
            True if paste successful
        """
        if not self.pyautogui:
            return False
        
        x, y = coordinates
        
        # One final coordinate check before paste
        pre_paste_pos = self.pyautogui.position()
        if abs(pre_paste_pos[0] - x) > 10 or abs(pre_paste_pos[1] - y) > 10:
            logger.error(
                f"❌ CRITICAL: Mouse position invalid before paste for {recipient}: "
                f"expected ({x}, {y}), got {pre_paste_pos}"
            )
            return False
        
        logger.debug("📥 Pasting message")
        self.pyautogui.hotkey("ctrl", "v")
        time.sleep(1.0)  # Wait for paste to complete
        
        return True
    
    def send_message(
        self,
        recipient: str,
        message_metadata: dict
    ) -> bool:
        """
        Send message (press Enter or Ctrl+Enter).
        
        Args:
            recipient: Agent recipient ID (for logging)
            message_metadata: Message metadata dict (for send_mode/stalled flags)
            
        Returns:
            True if send successful
        """
        if not self.pyautogui:
            return False
        
        send_mode = message_metadata.get("send_mode")
        is_stalled = message_metadata.get("stalled", False)
        
        logger.debug(f"📤 Sending message (stalled={is_stalled}, send_mode={send_mode})")
        
        # Priority: explicit send_mode -> stalled flag -> default enter
        if send_mode == "ctrl_enter" or (send_mode is None and is_stalled):
            logger.debug("⚠️ Using Ctrl+Enter send")
            self.pyautogui.hotkey("ctrl", "enter")
        else:
            logger.debug("✅ Using Enter send")
            self.pyautogui.press("enter")
        
        time.sleep(1.0)  # Wait for message to be sent
        
        return True
    
    def verify_send_completion(
        self,
        recipient: str,
        coordinates: Tuple[int, int]
    ) -> bool:
        """
        Verify message send completion and UI settlement.
        
        Args:
            recipient: Agent recipient ID (for logging)
            coordinates: Tuple of (x, y) coordinates
            
        Returns:
            True if send verified
        """
        if not self.pyautogui:
            return False
        
        x, y = coordinates
        
        # Additional delay to allow UI to fully process
        time.sleep(2.5)  # Increased from 2.0s to 2.5s for routing stability
        
        # Verify mouse is still at correct coordinates (confirms UI is stable)
        final_verify_pos = self.pyautogui.position()
        verify_distance = ((final_verify_pos[0] - x) ** 2 + (final_verify_pos[1] - y) ** 2) ** 0.5
        
        if verify_distance > 20:  # Allow some movement tolerance
            logger.warning(
                f"⚠️ Mouse moved significantly after send for {recipient}: "
                f"distance={verify_distance:.1f}px (may indicate UI interaction)"
            )
        else:
            logger.debug(f"✅ Mouse position stable after send (distance={verify_distance:.1f}px)")
        
        logger.debug("✅ Message send sequence completed and UI settled")
        return True

