"""
Base Classes for Code Consolidation

<!-- SSOT Domain: core -->

Created by: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-02
Purpose: Consolidate duplicate code patterns across Manager/Handler/Service classes
Updated: 2025-12-04 - Agent-1 (Initialization and Error Handling consolidation)
"""

from .error_handling_mixin import ErrorHandlingMixin
from .initialization_mixin import InitializationMixin
from .base_service import BaseService
from .base_handler import BaseHandler
from .base_manager import BaseManager


__all__ = [
    'BaseManager',
    'BaseHandler',
    'BaseService',
    'InitializationMixin',
    'ErrorHandlingMixin',
]
