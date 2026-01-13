"""
Circuit Breaker Package - Dependency Injection Pattern
=======================================================

<!-- SSOT Domain: integration -->

Package for Circuit Breaker functionality with dependency injection.
Uses provider pattern to break circular imports.

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2025-12-03
V2 Compliant: Yes
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .implementation import CircuitBreaker

# Export provider and protocol (no circular dependency)
from .provider import CircuitBreakerProvider
from .protocol import ICircuitBreaker
# Export CircuitBreaker from within directory (resolves file/directory conflict)
from .implementation import CircuitBreaker

__all__ = [
    'CircuitBreakerProvider',
    'ICircuitBreaker',
    'CircuitBreaker',  # Now exported from directory
]
