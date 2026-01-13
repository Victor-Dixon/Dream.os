#!/usr/bin/env python3
"""
File Utilities Module
====================

Consolidated file and path operations for tools consolidation.
Provides unified interface for file I/O, path validation, and directory operations.

Part of Phase 2A: Foundation Consolidation
Used by 85% of tools according to dependency analysis.

Author: Agent-7 (Tools Consolidation & Architecture Lead)
Date: 2026-01-13
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from datetime import datetime

logger = logging.getLogger(__name__)

class FileUtils:
    """Unified file and path operations for tools consolidation."""

    @staticmethod
    def ensure_directory(path: Union[str, Path]) -> Path:
        """Ensure a directory exists, creating it if necessary.

        Args:
            path: Directory path to ensure exists

        Returns:
            Path object for the ensured directory
        """
        dir_path = Path(path)
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    @staticmethod
    def safe_read_json(file_path: Union[str, Path], default: Any = None) -> Any:
        """Safely read JSON file with error handling.

        Args:
            file_path: Path to JSON file
            default: Default value to return on error

        Returns:
            Parsed JSON data or default value
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
            logger.debug(f"Failed to read JSON {file_path}: {e}")
            return default

    @staticmethod
    def safe_write_json(file_path: Union[str, Path], data: Any, indent: int = 2) -> bool:
        """Safely write JSON file with error handling.

        Args:
            file_path: Path to write JSON file
            data: Data to serialize
            indent: JSON indentation level

        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure directory exists
            FileUtils.ensure_directory(Path(file_path).parent)

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except (IOError, TypeError) as e:
            logger.error(f"Failed to write JSON {file_path}: {e}")
            return False

    @staticmethod
    def find_files_by_pattern(directory: Union[str, Path], pattern: str = "*.py") -> List[Path]:
        """Find files matching a pattern in a directory recursively.

        Args:
            directory: Directory to search in
            pattern: Glob pattern to match (default: "*.py")

        Returns:
            List of matching file paths
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            return []

        return list(dir_path.rglob(pattern))

    @staticmethod
    def get_file_info(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """Get comprehensive file information.

        Args:
            file_path: Path to file

        Returns:
            Dictionary with file information or None if file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            return None

        stat = path.stat()
        return {
            "name": path.name,
            "path": str(path.absolute()),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "extension": path.suffix,
            "parent": str(path.parent)
        }

    @staticmethod
    def validate_path_exists(path: Union[str, Path], create_if_missing: bool = False) -> bool:
        """Validate that a path exists, optionally creating directories.

        Args:
            path: Path to validate
            create_if_missing: Whether to create missing directories

        Returns:
            True if path exists (or was created), False otherwise
        """
        path_obj = Path(path)

        if path_obj.exists():
            return True

        if create_if_missing:
            try:
                if path_obj.suffix:  # Has extension, treat as file
                    path_obj.parent.mkdir(parents=True, exist_ok=True)
                else:  # No extension, treat as directory
                    path_obj.mkdir(parents=True, exist_ok=True)
                return True
            except Exception as e:
                logger.error(f"Failed to create path {path}: {e}")
                return False

        return False

    @staticmethod
    def backup_file(file_path: Union[str, Path], suffix: str = ".backup") -> Optional[Path]:
        """Create a backup of a file.

        Args:
            file_path: Path to file to backup
            suffix: Suffix to append to backup filename

        Returns:
            Path to backup file or None on failure
        """
        source = Path(file_path)
        if not source.exists():
            return None

        backup_path = source.with_suffix(f"{source.suffix}{suffix}")
        try:
            import shutil
            shutil.copy2(source, backup_path)
            logger.info(f"Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Failed to create backup for {file_path}: {e}")
            return None

    @staticmethod
    def clean_directory(directory: Union[str, Path], pattern: str = "*") -> int:
        """Clean files matching pattern from directory.

        Args:
            directory: Directory to clean
            pattern: Glob pattern for files to remove

        Returns:
            Number of files removed
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            return 0

        removed_count = 0
        for file_path in dir_path.glob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                    removed_count += 1
            except Exception as e:
                logger.warning(f"Failed to remove {file_path}: {e}")

        logger.info(f"Cleaned {removed_count} files from {directory}")
        return removed_count

# Convenience functions for backward compatibility
def ensure_dir(path: Union[str, Path]) -> Path:
    """Legacy function for ensure_directory."""
    return FileUtils.ensure_directory(path)

def read_json_safe(file_path: Union[str, Path], default: Any = None) -> Any:
    """Legacy function for safe_read_json."""
    return FileUtils.safe_read_json(file_path, default)

def write_json_safe(file_path: Union[str, Path], data: Any, indent: int = 2) -> bool:
    """Legacy function for safe_write_json."""
    return FileUtils.safe_write_json(file_path, data, indent)