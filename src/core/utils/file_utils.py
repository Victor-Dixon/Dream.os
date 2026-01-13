#!/usr/bin/env python3
"""
File and Directory Utilities - SSOT for File Operations
=========================================================

Provides standardized file and directory operations.
Consolidates duplicate directory removal code.

<!-- SSOT Domain: core -->

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-04
V2 Compliant: Yes (<300 lines)
"""

import os
import shutil
import stat
import time
from pathlib import Path
from typing import Optional


def ensure_directory_removed(
    dir_path: Path,
    name: Optional[str] = None,
    retry_delay: float = 0.5,
    max_retries: int = 2,
) -> bool:
    """
    Ensure directory is completely removed, handling readonly files.
    
    SSOT for directory removal - consolidates duplicate code from:
    - tools/resolve_merge_conflicts.py
    - tools/complete_merge_into_main.py
    - tools/review_dreamvault_integration.py
    
    Args:
        dir_path: Path to directory to remove
        name: Optional name for logging
        retry_delay: Delay between retry attempts (seconds)
        max_retries: Maximum number of retry attempts
        
    Returns:
        True if directory was removed, False otherwise
    """
    if not dir_path.exists():
        return True
    
    display_name = name or str(dir_path)
    print(f"🧹 Removing existing {display_name} directory: {dir_path}")
    
    try:
        # First attempt: standard removal
        shutil.rmtree(dir_path, ignore_errors=True)
        time.sleep(retry_delay)
        
        # If still exists, try with readonly handler
        if dir_path.exists():
            def remove_readonly(func, path, exc):
                """Handle readonly files on Windows."""
                os.chmod(path, stat.S_IWRITE)
                func(path)
            
            shutil.rmtree(dir_path, onerror=remove_readonly)
            time.sleep(retry_delay)
        
        # Final check
        if dir_path.exists():
            print(f"⚠️ Warning: Could not fully remove {display_name} directory")
            return False
        
        return True
        
    except Exception as e:
        print(f"⚠️ Cleanup warning for {display_name}: {e}")
        return False


__all__ = ["ensure_directory_removed"]


