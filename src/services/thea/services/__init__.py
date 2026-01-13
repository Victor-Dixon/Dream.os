#!/usr/bin/env python3
"""
Thea Services Module - Business Logic Layer
===========================================

<!-- SSOT Domain: thea -->

Public API exports for Thea service interfaces and implementations.

V2 Compliance: Service layer exports.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from .interfaces.i_authentication_service import IAuthenticationService
from .interfaces.i_communication_service import ICommunicationService
from .interfaces.i_response_service import IResponseService

# Implementation imports (lazy loaded to avoid import errors)
try:
    from .implementations.thea_authentication_service import TheaAuthenticationService
except ImportError:
    TheaAuthenticationService = None

try:
    from .implementations.thea_communication_service import TheaCommunicationService
except ImportError:
    TheaCommunicationService = None

try:
    from .implementations.thea_response_service import TheaResponseService
except ImportError:
    TheaResponseService = None

__all__ = [
    # Interfaces
    "IAuthenticationService",
    "ICommunicationService",
    "IResponseService",

    # Implementations (may be None if dependencies missing)
    "TheaAuthenticationService",
    "TheaCommunicationService",
    "TheaResponseService",
]