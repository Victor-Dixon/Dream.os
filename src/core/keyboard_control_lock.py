#!/usr/bin/env python3
"""
Global Keyboard Control Lock
============================

Prevents race conditions when multiple sources (Discord, agents, user) try to
control the keyboard simultaneously. Critical for preventing "9 ppl controlling
my keyboard" scenario.

V2 Compliance: <100 lines
Author: Agent-6 (Coordination & Communication Specialist)
Date: 2025-01-27
"""

import logging
import threading
from contextlib import contextmanager
from typing import Optional

logger = logging.getLogger(__name__)

# Global lock for ALL keyboard/mouse operations
# CRITICAL: Single lock for entire PyAutoGUI operation sequence
_keyboard_control_lock = threading.Lock()

# Lock timeout to prevent deadlocks (seconds)
_LOCK_TIMEOUT = 30.0

# Track current holder for debugging
_current_holder: Optional[str] = None


@contextmanager
def keyboard_control(source: str = "unknown"):
    """
    Context manager for exclusive keyboard control.
    
    Ensures only ONE source can control keyboard at a time.
    Prevents race conditions between Discord, agents, and user.
    
    Args:
        source: Source identifier (e.g., "discord", "agent", "queue_processor")
        
    Example:
        with keyboard_control("discord"):
            # PyAutoGUI operations here
            pyautogui.typewrite("message")
    """
    global _current_holder
    
    acquired = False
    try:
        # Try to acquire lock with timeout to prevent deadlocks
        acquired = _keyboard_control_lock.acquire(timeout=_LOCK_TIMEOUT)
        
        if not acquired:
            raise RuntimeError(
                f"⚠️ TIMEOUT: Could not acquire keyboard lock within {_LOCK_TIMEOUT}s. "
                f"Another source may be holding it: {_current_holder}"
            )
        
        _current_holder = source
        logger.debug(f"🔒 Keyboard lock acquired by: {source}")
        
        yield
        
    except Exception as e:
        logger.error(f"❌ Error during keyboard control by {source}: {e}")
        raise
    finally:
        if acquired:
            _current_holder = None
            _keyboard_control_lock.release()
            logger.debug(f"🔓 Keyboard lock released by: {source}")


def is_locked() -> bool:
    """Check if keyboard lock is currently held."""
    return _keyboard_control_lock.locked()


def get_current_holder() -> Optional[str]:
    """Get identifier of current lock holder (for debugging)."""
    return _current_holder


def acquire_lock(source: str, timeout: float = _LOCK_TIMEOUT) -> bool:
    """
    Manually acquire keyboard lock (alternative to context manager).
    
    Returns:
        True if lock acquired, False if timeout
    """
    global _current_holder
    
    acquired = _keyboard_control_lock.acquire(timeout=timeout)
    if acquired:
        _current_holder = source
        logger.debug(f"🔒 Keyboard lock manually acquired by: {source}")
    
    return acquired


def release_lock(source: str):
    """Manually release keyboard lock (must match source that acquired it)."""
    global _current_holder
    
    if _current_holder != source:
        logger.warning(
            f"⚠️ Lock release mismatch: {source} trying to release, "
            f"but {_current_holder} is holder"
        )
    
    _current_holder = None
    _keyboard_control_lock.release()
    logger.debug(f"🔓 Keyboard lock manually released by: {source}")

