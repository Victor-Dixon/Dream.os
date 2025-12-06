#!/usr/bin/env python3
"""
Error Response Models
=====================

Standardized error response classes for unified error handling.
Extracted from error_handling_core.py for V2 compliance.

Author: Agent-6 - Quality Gates & VSCode Specialist (V2 Refactor)
Original: Agent-3 - Infrastructure & DevOps Specialist (C-055-3)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .error_models_enums import ErrorCategory, ErrorSeverity
from dataclasses import dataclass, field

from src.core.utils.serialization_utils import to_dict



@dataclass
class ErrorContext:
    """Error context information."""

    operation: str
    timestamp: str
    error_type: str
    category: ErrorCategory
    severity: ErrorSeverity
    additional_data: dict[str, Any]


@dataclass
class StandardErrorResponse:
    """Standardized error response format."""

    success: bool = False
    error: str = ""
    error_type: str = ""
    operation: str = ""
    timestamp: str = ""
    context: dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class FileErrorResponse(StandardErrorResponse):
    """File operation error response."""

    file_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["file_path"] = self.file_path
        return result


@dataclass
class NetworkErrorResponse(StandardErrorResponse):
    """Network operation error response."""

    url: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["url"] = self.url
        return result


@dataclass
class DatabaseErrorResponse(StandardErrorResponse):
    """Database operation error response."""

    table: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        result["table"] = self.table
        return result


__all__ = [
    "ErrorContext",
    "StandardErrorResponse",
    "FileErrorResponse",
    "NetworkErrorResponse",
    "DatabaseErrorResponse",
]
