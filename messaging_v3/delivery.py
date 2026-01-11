#!/usr/bin/env python3
"""
PyAutoGUI Delivery - Clean and Simple
"""

import logging
import time
import threading
from typing import Tuple, Dict, Any, Optional

logger = logging.getLogger(__name__)

# Global delivery lock to prevent concurrent PyAutoGUI operations
_delivery_lock = threading.Lock()

try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("PyAutoGUI not available - delivery will fail")


class DeliveryService:
    """Clean PyAutoGUI delivery service."""

    def __init__(self):
        if not PYAUTOGUI_AVAILABLE:
            raise ImportError("PyAutoGUI not available")

        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1

        # Agent coordinates mapping (clean and simple)
        self.coordinates = {
            "Agent-1": (-1269, 481),
            "Agent-2": (-308, 480),
            "Agent-3": (-1269, 1001),
            "Agent-4": (-308, 1000),
            "Agent-5": (652, 421),
            "Agent-6": (1612, 419),
            "Agent-7": (653, 940),
            "Agent-8": (1611, 941),
        }

    def get_coordinates(self, agent_id: str) -> Tuple[int, int]:
        """Get coordinates for agent."""
        if agent_id not in self.coordinates:
            raise ValueError(f"Unknown agent: {agent_id}")
        return self.coordinates[agent_id]

    def validate_coordinates(self, agent_id: str, coords: Tuple[int, int]) -> bool:
        """Basic coordinate validation."""
        screen_width, screen_height = pyautogui.size()
        x, y = coords
        return 0 <= x < screen_width and 0 <= y < screen_height

    def deliver_message(self, message) -> bool:
        """
        Deliver message via PyAutoGUI with global lock.

        Args:
            message: Message object or dict with recipient, content, etc.

        Returns:
            bool: Success status
        """
        # Extract message data
        if hasattr(message, 'recipient'):
            recipient = message.recipient
            content = message.content
            sender = getattr(message, 'sender', 'system')
        else:
            recipient = message.get('recipient')
            content = message.get('content')
            sender = message.get('sender', 'system')

        with _delivery_lock:
            try:
                return self._deliver_message_internal(recipient, content, sender)
            except Exception as e:
                logger.error(f"Delivery failed for {recipient}: {e}")
                return False

    def _deliver_message_internal(self, recipient: str, content: str, sender: str) -> bool:
        """Internal delivery implementation."""
        try:
            # Get coordinates
            coords = self.get_coordinates(recipient)
            x, y = coords

            logger.info(f"Delivering to {recipient} at {coords}")

            # Move to coordinates
            pyautogui.moveTo(x, y, duration=0.5)
            time.sleep(0.5)  # Wait for focus

            # Click to focus
            pyautogui.click()
            time.sleep(0.5)

            # Clear input (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.5)

            # Copy and paste content
            pyperclip.copy(content)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(1.0)  # Wait for paste

            # Send message (Enter)
            pyautogui.press('enter')
            time.sleep(0.5)

            logger.info(f"✅ Message delivered to {recipient}")
            return True

        except Exception as e:
            logger.error(f"Delivery error for {recipient}: {e}")
            return False


# Global delivery service instance
_delivery_service = None

def get_delivery_service() -> DeliveryService:
    """Get or create delivery service singleton."""
    global _delivery_service
    if _delivery_service is None:
        _delivery_service = DeliveryService()
    return _delivery_service

def send_message(recipient: str, content: str, sender: str = "system") -> bool:
    """Simple function to send a message."""
    service = get_delivery_service()
    message = {
        'recipient': recipient,
        'content': content,
        'sender': sender
    }
    return service.deliver_message(message)