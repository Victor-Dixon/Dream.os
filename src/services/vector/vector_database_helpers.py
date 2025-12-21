#!/usr/bin/env python3
"""
Vector Database Helpers Module
==============================

<!-- SSOT Domain: integration -->

Helper classes and constants for vector database operations.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

DEFAULT_COLLECTION = "agent_cellphone_v2"


@dataclass(slots=True)
class VectorOperationResult:
    """Represents the outcome of a vector database write operation."""

    success: bool
    message: str = ""
    metadata: dict[str, Any] | None = None

