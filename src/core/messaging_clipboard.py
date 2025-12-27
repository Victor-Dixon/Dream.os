#!/usr/bin/env python3
"""
Clipboard Service
==================

<!-- SSOT Domain: communication -->

Service for clipboard operations with thread-safe locking for PyAutoGUI message delivery.
Extracted from messaging_pyautogui.py as part of Phase 2A Infrastructure Refactoring.

V2 Compliance: Service Layer Pattern, ~80 lines target.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-27
"""

import logging
import threading
import time
from typing import Optional

logger = logging.getLogger(__name__)

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False
    logger.warning("pyperclip not available - clipboard operations disabled")

# RACE CONDITION FIX: Global clipboard lock
_clipboard_lock = threading.Lock()


class ClipboardService:
    """
    Service for clipboard operations with thread-safe locking.
    
    Handles:
    - Thread-safe clipboard copy operations
    - Clipboard verification
    - Prevents concurrent clipboard overwrites
    """
    
    def __init__(self):
        """Initialize clipboard service."""
        if not PYPERCLIP_AVAILABLE:
            logger.warning("ClipboardService initialized but pyperclip not available")
        logger.debug("ClipboardService initialized")
    
    def copy_to_clipboard(self, content: str) -> bool:
        """
        Copy content to clipboard (thread-safe).
        
        Args:
            content: Content to copy to clipboard
            
        Returns:
            True if copy successful
        """
        if not PYPERCLIP_AVAILABLE:
            logger.error("Cannot copy to clipboard - pyperclip not available")
            return False
        
        with _clipboard_lock:
            try:
                logger.debug(f"📋 Copying message to clipboard: {content[:50]}...")
                pyperclip.copy(content)
                time.sleep(0.5)  # Wait for clipboard to be ready
                logger.debug("✅ Content copied to clipboard")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to copy to clipboard: {e}")
                return False
    
    def verify_clipboard(self, expected_content: str) -> bool:
        """
        Verify clipboard contains expected content.
        
        Args:
            expected_content: Expected clipboard content
            
        Returns:
            True if clipboard matches expected content
        """
        if not PYPERCLIP_AVAILABLE:
            return False
        
        with _clipboard_lock:
            try:
                clipboard_check = pyperclip.paste()
                if clipboard_check == expected_content:
                    logger.debug("✅ Clipboard verified")
                    return True
                else:
                    logger.warning(
                        f"⚠️ Clipboard mismatch: expected {len(expected_content)} chars, "
                        f"got {len(clipboard_check)} chars"
                    )
                    return False
            except Exception as e:
                logger.warning(f"⚠️ Could not verify clipboard: {e}")
                return False
    
    def get_clipboard_lock(self):
        """
        Get clipboard lock context manager for manual locking.
        
        Returns:
            Thread lock context manager
        """
        return _clipboard_lock

