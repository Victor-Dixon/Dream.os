from __future__ import annotations

"""
UI Onboarding Automation
========================

<!-- SSOT Domain: core -->

Handles UI-based onboarding automation using PyAutoGUI.
"""

import logging
import time

logger = logging.getLogger(__name__)
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    pyperclip = None

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    pyautogui = None


class UIUnavailableError(Exception):
    """Raised when UI automation is not available."""
    pass


class UIOnboarder:
    """Handles UI-based onboarding automation using PyAutoGUI."""

    def __init__(self, tolerance: int=3, retries: int=1, dry_run: bool=False):
        """Initialize UI onboarder with configuration."""
        self.tolerance = tolerance
        self.retries = retries
        self.dry_run = dry_run

    def onboard_agent(self, agent_id: str, message: str) -> bool:
        """
        Onboard an agent by sending a message to their chat input.
        
        Args:
            agent_id: The agent ID to onboard
            message: The onboarding message to send
            
        Returns:
            True if successful, False otherwise
        """
        if not PYAUTOGUI_AVAILABLE:
            logger.error("PyAutoGUI not available for UI onboarding")
            return False
        
        if self.dry_run:
            logger.info(f"[DRY RUN] Would onboard {agent_id} with message: {message[:50]}...")
            return True
        
        try:
            # Get coordinates for agent
            from ..core.coordinate_loader import get_coordinates_for_agent
            coords = get_coordinates_for_agent(agent_id)
            
            if not coords:
                logger.error(f"No coordinates found for agent {agent_id}")
                return False
            
            x, y = coords
            
            # Move to coordinates and click
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)
            
            # Clear input field
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.1)
            pyautogui.press('delete')
            time.sleep(0.1)
            
            # Paste message
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(message)
                time.sleep(0.5)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
            else:
                # Fallback to typing
                pyautogui.write(message, interval=0.01)
                time.sleep(0.5)
            
            # Send message
            pyautogui.press('enter')
            time.sleep(0.5)
            
            logger.info(f"✅ Successfully onboarded {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to onboard {agent_id}: {e}", exc_info=True)
            return False
