#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->
Unified Data Processing System - V2 Compliance Redirect Shim
===========================================================

DEPRECATED: This module redirects to unified_file_utils.py for backward compatibility.
All functionality is provided by src/utils/file_operations/file_serialization.py (SSOT).

This shim eliminates code duplication by redirecting to the unified file utilities.
New code should import directly from unified_file_utils.py.

Author: Agent-3 (Infrastructure & DevOps Specialist) - Refactored for duplication elimination
License: MIT
"""

from utils.unified_file_utils import UnifiedFileUtils

# Create singleton instance for backward compatibility
_unified_instance = UnifiedFileUtils()


def read_json(file_path: str) -> dict[str, Any]:
    """Read JSON file with error handling.

    DEPRECATED: Use UnifiedFileUtils.serialization.read_json() instead.

    Args:
        file_path: Path to JSON file

    Returns:
        Dictionary containing JSON data or None on error
    """
    return _unified_instance.serialization.read_json(file_path) or {}


def write_json(file_path: str, data: dict[str, Any]) -> bool:
    """Write data to JSON file with error handling.

    DEPRECATED: Use UnifiedFileUtils.serialization.write_json() instead.

    Args:
        file_path: Path to JSON file
        data: Data to write

    Returns:
        True if successful, False otherwise
    """
    return _unified_instance.serialization.write_json(file_path, data)


def ensure_directory(dir_path: str) -> bool:
    """Ensure directory exists.

    Args:
        dir_path: Directory path

    Returns:
        True if successful, False otherwise
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def resolve_path(path: str) -> Path:
    """Resolve path to absolute path.

    Args:
        path: Path to resolve

    Returns:
        Resolved Path object
    """
    return Path(path).resolve()


def write_file(file_path: str, content: str) -> bool:
    """Write content to file with error handling.

    Args:
        file_path: Path to file
        content: Content to write

    Returns:
        True if successful, False otherwise
    """
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return True

    except Exception:
        return False
