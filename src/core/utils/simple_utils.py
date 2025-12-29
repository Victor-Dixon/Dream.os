#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Simple Utils - V2 Compliance Redirect Shim
==========================================

Redirects file operations to unified_file_utils.py for backward compatibility.
Maintains KISS principle for unique utility functions.

This module acts as a redirect shim to eliminate duplicate code.
File operations delegate to unified_file_utils.py (SSOT).
Unique functions (timestamp, string formatting, path validation) remain.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-04
License: MIT
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# Import unified file utilities (SSOT)
from ...utils.unified_file_utils import UnifiedFileUtils, DirectoryOperations

# Create singleton instance for backward compatibility
_unified_instance = UnifiedFileUtils()


# ================================
# UNIQUE FUNCTIONS (Keep)
# ================================

def get_timestamp() -> str:
    """Get current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_string(template: str, **kwargs: Any) -> str:
    """Format string with variables."""
    try:
        return template.format(**kwargs)
    except Exception:
        return template


def is_valid_path(path: str) -> bool:
    """Check if path is valid."""
    try:
        return os.path.exists(path)
    except Exception:
        return False


# ================================
# FILE OPERATIONS (Redirect to SSOT)
# ================================

def read_file(filepath: str) -> Optional[str]:
    """Read file content."""
    # Note: unified_file_utils has read_json/read_yaml, but not raw read_file
    # Keep simple implementation for raw file reading (KISS principle)
    try:
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def write_file(filepath: str, content: str) -> bool:
    """Write content to file."""
    # Use unified_file_utils for directory creation
    try:
        from pathlib import Path
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        # Keep simple implementation for raw file writing (KISS principle)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception:
        return False


def list_files(directory: str, extension: Optional[str] = None) -> list[str]:
    """List files in directory."""
    # Convert extension filter to pattern for unified_file_utils
    if extension:
        pattern = f"*.{extension.lstrip('.')}"
    else:
        pattern = "*"
    return _unified_instance.list_files(directory, pattern)


def get_file_size(filepath: str) -> int:
    """Get file size in bytes."""
    size = _unified_instance.get_file_size(filepath)
    return size or 0  # Return 0 instead of None for backward compatibility


def copy_file(source: str, destination: str) -> bool:
    """Copy file from source to destination."""
    return _unified_instance.copy_file(source, destination)


def create_directory(path: str) -> bool:
    """Create directory if it doesn't exist."""
    # Use unified_file_utils directory operations
    try:
        from pathlib import Path
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def delete_file(filepath: str) -> bool:
    """Delete file."""
    # unified_file_utils has safe_delete_file (with backup), but not simple delete
    # Keep simple implementation for backward compatibility (KISS principle)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
        return True
    except Exception:
        return False


# Backward compatibility exports
__all__ = [
    "read_file",
    "write_file",
    "list_files",
    "get_timestamp",
    "format_string",
    "is_valid_path",
    "create_directory",
    "delete_file",
    "get_file_size",
    "copy_file",
]
