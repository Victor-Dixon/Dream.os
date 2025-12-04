# Base Classes for Code Consolidation
# Created by: Agent-2 (Architecture & Design Specialist)
# Date: 2025-12-02
# Purpose: Consolidate duplicate code patterns across Manager/Handler/Service classes

from .base_manager import BaseManager
from .base_handler import BaseHandler
from .base_service import BaseService
from .initialization_mixin import InitializationMixin

__all__ = [
    'BaseManager',
    'BaseHandler',
    'BaseService',
    'InitializationMixin',
]



