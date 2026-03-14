#!/usr/bin/env python3
# Header-Variant: full
# Owner: Dream.os
# Purpose: Module implementation and orchestration logic.
# SSOT: docs/recovery/recovery_registry.yaml#src-core-message-queue-init
# @registry docs/recovery/recovery_registry.yaml#src-core-message-queue-init

"""
Message Queue Package
=====================

Provides message queue functionality with proper separation of concerns.

V2 Compliance | Author: Agent-2 | Date: 2026-01-01

<!-- SSOT Domain: core -->
"""

# Import classes from the implementation module to avoid naming conflicts
from ..message_queue_impl import MessageQueue, QueueConfig, AsyncQueueProcessor
from ..message_queue_interfaces import IMessageQueue

__all__ = [
    'MessageQueue',
    'QueueConfig',
    'AsyncQueueProcessor',
    'IMessageQueue',
]
