#!/usr/bin/env python3
"""
Message Queue Processor - Backward Compatibility Shim
====================================================

<!-- SSOT Domain: communication -->

Backward compatibility shim for message_queue_processor refactoring.
Maintains existing import paths while using new modular structure.

V2 Compliance: <50 lines (shim only)
Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-12-18
License: MIT
"""

from __future__ import annotations

# Import from new modular structure
from .message_queue_processor.core.processor import MessageQueueProcessor

__all__ = ["MessageQueueProcessor"]
