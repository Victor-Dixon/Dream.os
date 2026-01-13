#!/usr/bin/env python3
"""
Event Filtering Service - Phase 6 Infrastructure
===============================================

Event filtering and routing functionality.

<!-- SSOT Domain: event_bus_filtering -->

Features:
- Pattern-based event filtering
- Route determination

Author: Agent-5 (Business Intelligence Specialist)
Date: 2026-01-07
Phase: Phase 6 - Infrastructure Optimization
"""

import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class EventFilterService:
    """
    Handles event filtering and routing logic.
    """

    def __init__(self):
        """Initialize the filtering service."""
        self.filters = {}

    def add_filter(self, filter_id: str, patterns: List[str]) -> str:
        """
        Add a new event filter.

        Args:
            filter_id: Unique identifier for the filter
            patterns: List of event patterns to match

        Returns:
            Filter ID
        """
        self.filters[filter_id] = patterns
        logger.info(f"Filter added: {filter_id}")
        return filter_id

    def matches_filter(self, event: Dict[str, Any], filter_id: str) -> bool:
        """
        Check if an event matches a filter.

        Args:
            event: Event data to check
            filter_id: Filter to check against

        Returns:
            True if event matches the filter
        """
        if filter_id not in self.filters:
            return False

        event_type = event.get('event_type', '')
        patterns = self.filters[filter_id]

        for pattern in patterns:
            if pattern == "*" or pattern == event_type:
                return True
            if pattern.endswith("*") and event_type.startswith(pattern[:-1]):
                return True

        return False