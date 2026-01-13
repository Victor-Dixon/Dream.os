#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

File Utils - V2 Compliance Redirect Shim
=======================================

Redirects to unified_file_utils.py for backward compatibility.
Maintains FileUtils static methods interface.

This module acts as a redirect shim to eliminate duplicate code.
All functionality is provided by unified_file_utils.py (SSOT).

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-04
License: MIT
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any

from .unified_file_utils import (
    UnifiedFileUtils,
    BackupOperations,
    FileMetadataOperations,
    DataSerializationOperations,
    DirectoryOperations,
    FileValidationResult,
)

# Create singleton instance for backward compatibility
_unified_instance = UnifiedFileUtils()


class FileUtils:
    """Backward compatibility wrapper for UnifiedFileUtils.
    
    This class provides static methods that delegate to UnifiedFileUtils
    to maintain backward compatibility while eliminating code duplication.
    """

    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False

    # JSON/YAML operations
    @staticmethod
    def read_json(file_path: str) -> dict[str, Any] | None:
        """Read JSON file and return data."""
        return _unified_instance.read_json(file_path)

    @staticmethod
    def write_json(file_path: str, data: dict[str, Any]) -> bool:
        """Write data to JSON file."""
        return _unified_instance.write_json(file_path, data)

    @staticmethod
    def read_yaml(file_path: str) -> dict[str, Any] | None:
        """Read YAML file and return data."""
        return _unified_instance.read_yaml(file_path)

    @staticmethod
    def write_yaml(file_path: str, data: dict[str, Any]) -> bool:
        """Write data to YAML file."""
        return _unified_instance.write_yaml(file_path, data)

    # File metadata operations
    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return _unified_instance.file_exists(file_path)

    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if a file is readable."""
        return FileMetadataOperations.is_file_readable(file_path)

    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if a file is writable."""
        return FileMetadataOperations.is_file_writable(file_path)

    @staticmethod
    def get_file_size(file_path: str) -> int | None:
        """Get file size in bytes."""
        return _unified_instance.get_file_size(file_path)

    @staticmethod
    def get_file_modified_time(file_path: str) -> datetime | None:
        """Get file last modified time."""
        return FileMetadataOperations.get_file_modified_time(file_path)

    @staticmethod
    def get_file_hash(file_path: str) -> str | None:
        """Get SHA256 hash of file."""
        return _unified_instance.get_file_hash(file_path)

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension."""
        return FileMetadataOperations.get_file_extension(file_path)

    @staticmethod
    def is_json_file(file_path: str) -> bool:
        """Check if file has JSON extension."""
        return FileMetadataOperations.is_json_file(file_path)

    # Directory and list operations
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> list[str]:
        """List files in directory matching pattern."""
        return _unified_instance.list_files(directory, pattern)

    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """Get total size of directory in bytes."""
        return _unified_instance.get_directory_size(directory_path)

    # Backup and copy operations
    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination."""
        return _unified_instance.copy_file(source, destination)

    @staticmethod
    def create_backup(file_path: str, backup_suffix: str = ".backup") -> str | None:
        """Create a backup of a file."""
        return BackupOperations.create_backup(file_path, backup_suffix)

    @staticmethod
    def restore_from_backup(backup_path: str, target_path: str) -> bool:
        """Restore a file from backup."""
        return BackupOperations.restore_from_backup(backup_path, target_path)

    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """Safely delete a file with backup."""
        return BackupOperations.safe_delete_file(file_path)

    # Validation helpers
    @staticmethod
    def validate_file_path(file_path: str) -> dict[str, Any]:
        """Validate file path and return detailed information."""
        result_obj: FileValidationResult = _unified_instance.validate_file(file_path)
        # Convert FileValidationResult to dict for backward compatibility
        return {
            "path": result_obj.path,
            "exists": result_obj.exists,
            "is_file": result_obj.is_file,
            "is_directory": result_obj.is_directory,
            "readable": result_obj.readable,
            "writable": result_obj.writable,
            "size_bytes": result_obj.size_bytes,
            "modified_time": (
                result_obj.modified_time.isoformat()
                if result_obj.modified_time
                else None
            ),
            "errors": result_obj.errors,
        }


# Backward compatibility exports
__all__ = ["FileUtils"]
