#!/usr/bin/env python3
"""
Timeout Constants - SSOT for All Timeout Values
===============================================

Provides single source of truth for all timeout values across the system.
Consolidates 404 hardcoded timeout instances across 6 timeout levels.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""


class TimeoutConstants:
    """
    SSOT for all timeout values across the system.
    
    Consolidates duplicate timeout values:
    - timeout=30: 175 locations → HTTP_DEFAULT
    - timeout=10: 69 locations → HTTP_SHORT
    - timeout=60: 53 locations → HTTP_MEDIUM
    - timeout=120: 45 locations → HTTP_LONG
    - timeout=300: 33 locations → HTTP_EXTENDED
    - timeout=5: 29 locations → HTTP_QUICK
    """
    
    # HTTP/API Request Timeouts
    HTTP_DEFAULT = 30  # Standard HTTP request timeout (most common)
    HTTP_SHORT = 10    # Quick HTTP requests (Discord, status checks)
    HTTP_MEDIUM = 60   # Medium-duration requests (file operations)
    HTTP_LONG = 120    # Long-duration requests (large file transfers)
    HTTP_EXTENDED = 300  # Extended operations (complex merges, deployments)
    HTTP_QUICK = 5     # Very quick requests (health checks, pings)
    
    # Subprocess/Command Timeouts
    SUBPROCESS_DEFAULT = 30  # Default subprocess timeout
    SUBPROCESS_SHORT = 10    # Quick subprocess commands
    SUBPROCESS_LONG = 120    # Long-running subprocess commands
    
    # Database/Connection Timeouts
    DATABASE_DEFAULT = 30    # Database connection timeout
    DATABASE_QUERY = 60      # Database query timeout
    
    # File Operation Timeouts
    FILE_OPERATION_DEFAULT = 30  # File read/write operations
    FILE_OPERATION_LONG = 120    # Large file operations


# Convenience aliases for backward compatibility
DEFAULT_TIMEOUT = TimeoutConstants.HTTP_DEFAULT
SHORT_TIMEOUT = TimeoutConstants.HTTP_SHORT
MEDIUM_TIMEOUT = TimeoutConstants.HTTP_MEDIUM
LONG_TIMEOUT = TimeoutConstants.HTTP_LONG
EXTENDED_TIMEOUT = TimeoutConstants.HTTP_EXTENDED
QUICK_TIMEOUT = TimeoutConstants.HTTP_QUICK


__all__ = [
    "TimeoutConstants",
    "DEFAULT_TIMEOUT",
    "SHORT_TIMEOUT",
    "MEDIUM_TIMEOUT",
    "LONG_TIMEOUT",
    "EXTENDED_TIMEOUT",
    "QUICK_TIMEOUT",
]


