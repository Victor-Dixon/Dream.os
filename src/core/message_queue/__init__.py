#!/usr/bin/env python3
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