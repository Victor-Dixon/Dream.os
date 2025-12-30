#!/usr/bin/env python3
"""
<!-- SSOT Domain: swarm_brain -->

Swarm Time Utility - Centralized Local Time Management
=====================================================

Provides centralized, reliable time management for the swarm.
All agents use local system time to match the user's computer time.

Author: Agent-4 (Captain)
Date: 2025-01-27
License: MIT
"""

from datetime import datetime
from typing import Optional


def get_swarm_time() -> datetime:
    """
    Get current local time for swarm operations.
    
    All agents should use this function to ensure time consistency.
    Uses local system time to match the user's computer time.
    
    Returns:
        Current local datetime
    """
    return datetime.now()


def format_swarm_timestamp(dt: Optional[datetime] = None) -> str:
    """
    Format datetime as ISO 8601 timestamp.
    
    Args:
        dt: Datetime to format (defaults to current local time)
    
    Returns:
        ISO 8601 formatted timestamp string
    """
    if dt is None:
        dt = get_swarm_time()
    
    return dt.isoformat()


def format_swarm_timestamp_readable(dt: Optional[datetime] = None) -> str:
    """
    Format datetime as human-readable timestamp.
    
    Args:
        dt: Datetime to format (defaults to current local time)
    
    Returns:
        Human-readable timestamp string (YYYY-MM-DD HH:MM:SS)
    """
    if dt is None:
        dt = get_swarm_time()
    
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def format_swarm_timestamp_filename(dt: Optional[datetime] = None) -> str:
    """
    Format datetime for use in filenames.
    
    Args:
        dt: Datetime to format (defaults to current local time)
    
    Returns:
        Filename-safe timestamp string (YYYYMMDD_HHMMSS_ffffff)
    """
    if dt is None:
        dt = get_swarm_time()
    
    return dt.strftime("%Y%m%d_%H%M%S_%f")


def get_swarm_time_display() -> str:
    """
    Get current local time formatted for display in messages.
    
    Returns:
        Formatted timestamp string for message display
    """
    return format_swarm_timestamp_readable()


__all__ = [
    "get_swarm_time",
    "format_swarm_timestamp",
    "format_swarm_timestamp_readable",
    "format_swarm_timestamp_filename",
    "get_swarm_time_display",
]
