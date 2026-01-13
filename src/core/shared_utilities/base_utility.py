"""
<!-- SSOT Domain: core -->

Base Utility - Abstract Base Class
===================================

Base class for all shared utilities.

Author: Agent-6 (Coordination & Communication Specialist)
Refactored: Agent-1 (Integration & Core Systems Specialist) - 2025-12-04
License: MIT
"""

import logging
from abc import ABC, abstractmethod


class BaseUtility(ABC):
    """Base class for all shared utilities."""

    def __init__(self, name: str = None):
        self.name = name or self.__class__.__name__
        self.logger = logging.getLogger(self.name)

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the utility."""
        pass

    @abstractmethod
    def cleanup(self) -> bool:
        """Clean up resources."""
        pass


