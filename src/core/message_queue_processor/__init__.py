#!/usr/bin/env python3
"""
Message Queue Processor - Backward Compatibility Shim
====================================================

<!-- SSOT Domain: communication -->

Backward compatibility shim for message_queue_processor refactoring.
Maintains existing import paths while using new modular structure.
"""

from __future__ import annotations

from .core.processor import MessageQueueProcessor

__all__ = ["MessageQueueProcessor"]
