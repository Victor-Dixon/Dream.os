"""
<!-- SSOT Domain: core -->

GUI System Utilities - V2 Compliance Redirect Shim
==================================================

Redirects to SSOT V2 integration utilities for backward compatibility.

SSOT: src/core/utils/v2_integration_utils.py

Author: Agent-2 (Architecture & Design Specialist) - Consolidation
Date: 2025-12-04
License: MIT
"""

# Redirect to SSOT using absolute imports to avoid relative import errors
from src.core.utils.v2_integration_utils import (
    get_coordinate_loader,
    get_logger,
    get_unified_config,
)

__all__ = [
    "get_coordinate_loader",
    "get_unified_config",
    "get_logger",
]
