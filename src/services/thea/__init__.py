<<<<<<< HEAD
#!/usr/bin/env python3
"""
Thea Service Module - V2 Compliant Modular Architecture
======================================================

<!-- SSOT Domain: thea -->

Main module for Thea communication service with V2 compliant architecture.

Features:
- Modular design with clear separation of concerns
- Repository pattern for data access
- Dependency injection for testability
- Circuit breaker pattern for resilience
- Comprehensive error handling

V2 Compliance: Repository → Service → Controller pattern.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from .domain import *
from .repositories import *
from .services import *

# Main coordinator import
try:
    from .thea_service_coordinator import TheaServiceCoordinator
except ImportError:
    TheaServiceCoordinator = None

# DI Container import
try:
    from .di_container import TheaDIContainer
except ImportError:
    TheaDIContainer = None

__all__ = [
    # Domain exports
    "TheaMessage",
    "TheaResponse",
    "TheaConversation",
    "CookieData",
    "AuthenticationContext",
    "BrowserContext",
    "CommunicationResult",

    # Repository interfaces
    "ICookieRepository",
    "IBrowserRepository",
    "IConversationRepository",

    # Service interfaces
    "IAuthenticationService",
    "ICommunicationService",
    "IResponseService",

    # Main components
    "TheaServiceCoordinator",
    "TheaDIContainer",
]
=======
# <!-- SSOT Domain: integration -->
# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

from . import thea_service

__all__ = [
    'thea_service',
]
>>>>>>> origin/codex/build-cross-platform-control-plane-for-swarm-console
