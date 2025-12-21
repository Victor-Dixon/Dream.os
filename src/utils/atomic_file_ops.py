#!/usr/bin/env python3
"""
Atomic File Operations Utility
==============================

Provides atomic file write operations to prevent file corruption from partial writes.

Author: Agent-6 (Swarm Intelligence Coordinator)
Date: 2025-12-20
V2 Compliant: <300 lines, single responsibility
SSOT Domain: infrastructure
"""

import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, Union, Any

logger = logging.getLogger(__name__)


class AtomicFileWriter:
    """
    Provides atomic file write operations using temporary files and atomic moves.

    This prevents file corruption from partial writes by ensuring operations are
    either completely successful or completely rolled back.
    """

    def __init__(self, target_path: Union[str, Path], backup: bool = True):
        """
        Initialize atomic file writer.

        Args:
            target_path: Path to the file to write atomically
            backup: Whether to create backup before modification
        """
        self.target_path = Path(target_path)
        self.backup_enabled = backup
        self.backup_path: Optional[Path] = None
        self.temp_path: Optional[Path] = None

        # Create backup immediately if file exists and backup is enabled
        if self.backup_enabled and self.target_path.exists():
            self._create_backup()

    def write_text(self, content: str, encoding: str = 'utf-8') -> bool:
        """
        Atomically write text content to file.

        Args:
            content: Text content to write
            encoding: Text encoding

        Returns:
            bool: True if successful, False if failed
        """
        try:
            # Create backup if enabled and file exists
            if self.backup_enabled and self.target_path.exists():
                self._create_backup()

            # Create temporary file in same directory for atomic move
            with tempfile.NamedTemporaryFile(
                mode='w',
                dir=self.target_path.parent,
                prefix=f'.tmp_{self.target_path.name}_',
                suffix='.atomic',
                delete=False,
                encoding=encoding
            ) as temp_file:
                self.temp_path = Path(temp_file.name)
                temp_file.write(content)
                temp_file.flush()
                os.fsync(temp_file.fileno())  # Force write to disk

            # Atomically move temp file to target
            os.replace(self.temp_path, self.target_path)

            logger.info(f"Atomically wrote {len(content)} chars to {self.target_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to write {self.target_path}: {e}")
            self._cleanup_failed_write()
            return False

        finally:
            self._cleanup_temp_file()

    def write_json(self, data: Any, indent: int = 2, encoding: str = 'utf-8') -> bool:
        """
        Atomically write JSON data to file.

        Args:
            data: Data to serialize as JSON
            indent: JSON indentation level
            encoding: File encoding

        Returns:
            bool: True if successful, False if failed
        """
        import json
        try:
            content = json.dumps(data, indent=indent, ensure_ascii=False)
            return self.write_text(content, encoding)
        except Exception as e:
            logger.error(f"Failed to serialize JSON for {self.target_path}: {e}")
            return False

    def _create_backup(self) -> None:
        """Create backup of original file."""
        try:
            import datetime
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            self.backup_path = self.target_path.with_suffix(
                f'{self.target_path.suffix}.backup_{timestamp}'
            )
            # Use copy2 to preserve metadata
            import shutil
            shutil.copy2(self.target_path, self.backup_path)
            logger.debug(f"Created backup: {self.backup_path}")
        except Exception as e:
            logger.warning(f"Failed to create backup: {e}")

    def _cleanup_failed_write(self) -> None:
        """Clean up after failed write operation."""
        # Restore from backup if available
        if self.backup_path and self.backup_path.exists():
            try:
                import shutil
                shutil.copy2(self.backup_path, self.target_path)
                logger.info(f"Restored from backup: {self.backup_path}")
            except Exception as e:
                logger.error(f"Failed to restore from backup: {e}")

    def _cleanup_temp_file(self) -> None:
        """Clean up temporary file."""
        if self.temp_path and self.temp_path.exists():
            try:
                self.temp_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {self.temp_path}: {e}")


def atomic_write_text(
    file_path: Union[str, Path],
    content: str,
    encoding: str = 'utf-8',
    backup: bool = True
) -> bool:
    """
    Convenience function for atomic text file writing.

    Args:
        file_path: Path to file
        content: Text content
        encoding: Text encoding
        backup: Whether to backup original file

    Returns:
        bool: True if successful
    """
    writer = AtomicFileWriter(file_path, backup=backup)
    return writer.write_text(content, encoding)


def atomic_write_json(
    file_path: Union[str, Path],
    data: Any,
    indent: int = 2,
    encoding: str = 'utf-8',
    backup: bool = True
) -> bool:
    """
    Convenience function for atomic JSON file writing.

    Args:
        file_path: Path to file
        data: Data to serialize
        indent: JSON indentation
        encoding: File encoding
        backup: Whether to backup original file

    Returns:
        bool: True if successful
    """
    writer = AtomicFileWriter(file_path, backup=backup)
    return writer.write_json(data, indent, encoding)


# Legacy compatibility - these will be deprecated
def safe_write_file(file_path: Union[str, Path], content: str) -> bool:
    """
    Legacy function for backward compatibility.
    Use atomic_write_text() instead.
    """
    return atomic_write_text(file_path, content)


def safe_write_json(file_path: Union[str, Path], data: Any) -> bool:
    """
    Legacy function for backward compatibility.
    Use atomic_write_json() instead.
    """
    return atomic_write_json(file_path, data)
