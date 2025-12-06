#!/usr/bin/env python3
"""
Specialized Error Response Models
==================================

Domain-specific error response classes.
Extracted from error_handling_core.py for V2 compliance.

Author: Agent-6 - Quality Gates & VSCode Specialist (V2 Refactor)
Original: Agent-3 - Infrastructure & DevOps Specialist (C-055-3)
License: MIT
"""

from dataclasses import dataclass
from typing import Any

# SSOT: Import from consolidated core models (deduplication)
from .error_response_models_core import StandardErrorResponse
from dataclasses import dataclass, field

from src.core.utils.serialization_utils import to_dict



@dataclass
class ValidationErrorResponse(StandardErrorResponse):
    """Validation error response."""

    validation_type: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class ConfigurationErrorResponse(StandardErrorResponse):
    """Configuration error response."""

    config_key: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class AgentErrorResponse(StandardErrorResponse):
    """Agent operation error response."""

    agent_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class CoordinationErrorResponse(StandardErrorResponse):
    """Coordination error response."""

    coordination_type: str = ""
    participants: list[str] = None

    def __post_init__(self):
        super().__post_init__()
        if self.participants is None:
            self.participants = []

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


@dataclass
class ErrorSummary:
    """Error summary statistics."""

    total_errors: int = 0
    error_types: dict[str, int] = None
    operations: dict[str, int] = None
    timestamp: str = ""

    def __post_init__(self):
        from datetime import datetime

        if self.error_types is None:
            self.error_types = {}
        if self.operations is None:
            self.operations = {}
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary using SSOT utility."""
        return to_dict(self)


__all__ = [
    "ValidationErrorResponse",
    "ConfigurationErrorResponse",
    "AgentErrorResponse",
    "CoordinationErrorResponse",
    "ErrorSummary",
]
