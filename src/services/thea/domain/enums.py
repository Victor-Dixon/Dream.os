#!/usr/bin/env python3
"""
Thea Domain Enums - Domain-Specific Enumerations
================================================

<!-- SSOT Domain: thea -->

Domain-specific enumerations for Thea communication service.
These define the valid values for domain concepts.

V2 Compliance: Pure domain concepts, no implementation details.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from enum import Enum


class TheaServiceType(Enum):
    """Types of Thea services available."""
    CHATGPT_BASIC = "chatgpt_basic"
    THEA_MANAGER = "thea_manager"
    CUSTOM_GPT = "custom_gpt"


class CookieStorageType(Enum):
    """Types of cookie storage mechanisms."""
    SECURE_ENCRYPTED = "secure_encrypted"
    PLAIN_JSON = "plain_json"
    IN_MEMORY = "in_memory"


class BrowserAutomationType(Enum):
    """Types of browser automation available."""
    SELENIUM = "selenium"
    PYAUTOGUI_FALLBACK = "pyautogui_fallback"
    MANUAL = "manual"


class ResponseExtractionStrategy(Enum):
    """Strategies for extracting responses from Thea."""
    ASSISTANT_MESSAGE = "assistant_message"
    ARTICLE_CONTENT = "article_content"
    MARKDOWN_CONTENT = "markdown_content"
    MESSAGE_ID = "message_id"
    AGENT_TURN = "agent_turn"
    FALLBACK_MANUAL = "fallback_manual"


class AuthenticationMethod(Enum):
    """Methods for authenticating with Thea."""
    COOKIE_BASED = "cookie_based"
    MANUAL_LOGIN = "manual_login"
    TOKEN_BASED = "token_based"


class CommunicationMode(Enum):
    """Modes of communication with Thea."""
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    STREAMING = "streaming"


class ErrorCategory(Enum):
    """Categories of errors that can occur."""
    AUTHENTICATION = "authentication"
    NETWORK = "network"
    BROWSER = "browser"
    PARSING = "parsing"
    TIMEOUT = "timeout"
    VALIDATION = "validation"
    UNKNOWN = "unknown"


class CircuitBreakerState(Enum):
    """States for circuit breaker pattern."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, requests rejected
    HALF_OPEN = "half_open" # Testing if service recovered