#!/usr/bin/env python3
"""
Thea Domain Module - Business Entities
======================================

<!-- SSOT Domain: thea -->

Public API exports for Thea domain models and enums.

V2 Compliance: Clean module exports.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from .models import (
    AuthenticationContext,
    BrowserContext,
    CommunicationResult,
    CookieData,
    CookieDict,
    ConversationId,
    MessageId,
    MessagePriority,
    MessageStatus,
    MetadataDict,
    TheaConversation,
    TheaMessage,
    TheaResponse,
)
from .enums import (
    AuthenticationMethod,
    AuthenticationStatus,
    BrowserAutomationType,
    BrowserState,
    CircuitBreakerState,
    CommunicationMode,
    CookieStorageType,
    ErrorCategory,
    ResponseExtractionStrategy,
    TheaServiceType,
)

__all__ = [
    # Models
    "TheaMessage",
    "TheaResponse",
    "TheaConversation",
    "CookieData",
    "AuthenticationContext",
    "BrowserContext",
    "CommunicationResult",

    # Type aliases
    "MessageId",
    "ConversationId",
    "CookieDict",
    "MetadataDict",

    # Enums
    "MessageStatus",
    "AuthenticationStatus",
    "BrowserState",
    "MessagePriority",
    "TheaServiceType",
    "CookieStorageType",
    "BrowserAutomationType",
    "ResponseExtractionStrategy",
    "AuthenticationMethod",
    "CommunicationMode",
    "ErrorCategory",
    "CircuitBreakerState",
]