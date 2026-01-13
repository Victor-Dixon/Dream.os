#!/usr/bin/env python3
"""
Thea Repositories Module - Data Access Layer
===========================================

<!-- SSOT Domain: thea -->

Public API exports for Thea repository interfaces and implementations.

V2 Compliance: Repository pattern exports.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from .interfaces.i_browser_repository import IBrowserRepository
from .interfaces.i_conversation_repository import IConversationRepository
from .interfaces.i_cookie_repository import ICookieRepository

# Implementation imports (lazy loaded to avoid import errors)
try:
    from .implementations.secure_cookie_repository import SecureCookieRepository
except ImportError:
    SecureCookieRepository = None

try:
    from .implementations.selenium_browser_repository import SeleniumBrowserRepository
except ImportError:
    SeleniumBrowserRepository = None

try:
    from .implementations.file_conversation_repository import FileConversationRepository
except ImportError:
    FileConversationRepository = None

__all__ = [
    # Interfaces
    "ICookieRepository",
    "IBrowserRepository",
    "IConversationRepository",

    # Implementations (may be None if dependencies missing)
    "SecureCookieRepository",
    "SeleniumBrowserRepository",
    "FileConversationRepository",
]