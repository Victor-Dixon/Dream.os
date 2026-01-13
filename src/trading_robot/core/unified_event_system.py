#!/usr/bin/env python3
"""
Unified Event System for Trading Robot
=====================================

Provides unified event publishing and handling for the trading robot core.

This module serves as a compatibility layer and re-exports EventPublisher
from the V2 event system for backward compatibility.
"""

# Re-export EventPublisher from V2 system for compatibility
from .event_publisher_v2 import EventPublisherV2 as EventPublisher

__all__ = ['EventPublisher']