"""
<!-- SSOT Domain: integration -->

Shared PyAutoGUI Operations
===========================

Provides shared PyAutoGUI operations for onboarding services.
Extracted to reduce duplication and improve testability.

V2 Compliant: < 200 lines
"""

import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)

# Import PyAutoGUI
try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    logger.warning("⚠️ PyAutoGUI not available - operations will be disabled")


class PyAutoGUIOperations:
    """Shared PyAutoGUI operations for onboarding services."""
    
    def __init__(self):
        """Initialize PyAutoGUI operations."""
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("⚠️ PyAutoGUI not available - operations disabled")
        self.pyautogui = pyautogui if PYAUTOGUI_AVAILABLE else None
        self.pyperclip = pyperclip if PYAUTOGUI_AVAILABLE else None
        self.available = PYAUTOGUI_AVAILABLE
    
    def click_at_coords(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Click at coordinates with animation.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Animation duration in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping click")
            return False
        
        try:
            self.pyautogui.moveTo(x, y, duration=duration)
            self.pyautogui.click()
            return True
        except Exception as e:
            logger.error(f"❌ Failed to click at ({x}, {y}): {e}")
            return False
    
    def send_hotkey(self, *keys: str, wait: float = 0.8) -> bool:
        """
        Send hotkey combination.
        
        Args:
            *keys: Key names (e.g., "ctrl", "enter")
            wait: Wait time after hotkey in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping hotkey")
            return False
        
        try:
            self.pyautogui.hotkey(*keys)
            time.sleep(wait)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to send hotkey {keys}: {e}")
            return False
    
    def paste_text(self, text: str, wait: float = 0.5) -> bool:
        """
        Paste text via clipboard.
        
        Args:
            text: Text to paste
            wait: Wait time after paste in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping paste")
            return False
        
        try:
            self.pyperclip.copy(text)
            self.pyautogui.hotkey("ctrl", "v")
            time.sleep(wait)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to paste text: {e}")
            return False
    
    def clear_input(self, wait: float = 0.3) -> bool:
        """
        Clear input field (Ctrl+A, Delete).
        
        Args:
            wait: Wait time after clear in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping clear")
            return False
        
        try:
            self.pyautogui.hotkey("ctrl", "a")
            time.sleep(0.1)
            self.pyautogui.press("delete")
            time.sleep(wait)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to clear input: {e}")
            return False
    
    def press_key(self, key: str, wait: float = 0.5) -> bool:
        """
        Press a single key.
        
        Args:
            key: Key name (e.g., "enter", "delete")
            wait: Wait time after key press in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping key press")
            return False
        
        try:
            self.pyautogui.press(key)
            time.sleep(wait)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to press key {key}: {e}")
            return False
    
    def move_to(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move mouse to coordinates with animation.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Animation duration in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.available:
            logger.warning("⚠️ PyAutoGUI not available - skipping move")
            return False
        
        try:
            self.pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to move to ({x}, {y}): {e}")
            return False

