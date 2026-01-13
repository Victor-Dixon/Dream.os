#!/usr/bin/env python3
"""
Thea Domain Models - Business Entities
======================================

<!-- SSOT Domain: thea -->

Core business entities for Thea communication service.
These models represent the domain concepts, not implementation details.

V2 Compliance: Pure business logic, no infrastructure dependencies.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class MessageStatus(Enum):
    """Status of a message in the communication pipeline."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    TIMEOUT = "timeout"


class MessagePriority(Enum):
    """Priority levels for message delivery."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


<<<<<<< HEAD
<<<<<<< HEAD
class MessageStatus(Enum):
    """Status of a message in the communication pipeline."""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    FAILED = "failed"
    TIMEOUT = "timeout"


=======
>>>>>>> rescue/dreamos-down-
=======
>>>>>>> origin/codex/implement-cycle-snapshot-system-phase-1
class AuthenticationStatus(Enum):
    """Status of authentication with Thea service."""
    AUTHENTICATED = "authenticated"
    REQUIRES_LOGIN = "requires_login"
    INVALID_CREDENTIALS = "invalid_credentials"
    NETWORK_ERROR = "network_error"
    SERVICE_UNAVAILABLE = "service_unavailable"


class BrowserState(Enum):
    """State of the browser automation."""
    NOT_STARTED = "not_started"
    STARTING = "starting"
    READY = "ready"
    ERROR = "error"
    CLOSED = "closed"


@dataclass
class AuthenticationContext:
    """
    Context information for authentication operations.
    """
    target_url: str
    current_status: AuthenticationStatus = AuthenticationStatus.REQUIRES_LOGIN
    last_attempt: Optional[datetime] = None
    attempt_count: int = 0
    error_message: Optional[str] = None

    def record_attempt(self, success: bool, error: Optional[str] = None) -> None:
        """Record an authentication attempt."""
        self.last_attempt = datetime.now()
        self.attempt_count += 1

        if success:
            self.current_status = AuthenticationStatus.AUTHENTICATED
            self.error_message = None
        else:
            self.current_status = AuthenticationStatus.INVALID_CREDENTIALS
            self.error_message = error or "Authentication failed"

    def should_retry(self, max_attempts: int = 3) -> bool:
        """Check if authentication should be retried."""
        return (
            self.attempt_count < max_attempts
            and self.current_status != AuthenticationStatus.AUTHENTICATED
        )


@dataclass
class TheaMessage:
    """
    Represents a message to be sent to Thea.

    This is a pure business entity - no infrastructure details.
    """
    content: str
    message_id: str = field(default_factory=lambda: str(uuid4()))
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: MessageStatus = MessageStatus.PENDING

    def __post_init__(self):
        """Validate message content."""
        if not self.content or not self.content.strip():
            raise ValueError("Message content cannot be empty")

        if len(self.content) > 10000:  # Reasonable limit
            raise ValueError("Message content too long (max 10000 characters)")

    def mark_sent(self) -> None:
        """Mark message as successfully sent."""
        self.status = MessageStatus.SENT

    def mark_failed(self, reason: str) -> None:
        """Mark message as failed."""
        self.status = MessageStatus.FAILED
        self.metadata["failure_reason"] = reason

    def mark_timeout(self) -> None:
        """Mark message as timed out."""
        self.status = MessageStatus.TIMEOUT


@dataclass
class TheaResponse:
    """
    Represents a response received from Thea.

    Pure business entity for response data.
    """
    content: str
    message_id: str
    response_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.now)
    confidence_score: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time_seconds: Optional[float] = None

    def __post_init__(self):
        """Validate response content."""
        if not isinstance(self.confidence_score, (float, type(None))):
            raise ValueError("Confidence score must be a float or None")

        if self.confidence_score is not None and not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError("Confidence score must be between 0.0 and 1.0")

    def is_confident(self, threshold: float = 0.7) -> bool:
        """Check if response meets confidence threshold."""
        return self.confidence_score is not None and self.confidence_score >= threshold


@dataclass
class TheaConversation:
    """
    Represents a complete conversation with Thea.

    Contains the message, response, and metadata.
    """
    message: TheaMessage
    response: Optional[TheaResponse] = None
    conversation_id: str = field(default_factory=lambda: str(uuid4()))
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    total_duration_seconds: Optional[float] = None

    def __post_init__(self):
        """Ensure message and response are properly linked."""
        if self.response and self.response.message_id != self.message.message_id:
            raise ValueError("Response message_id must match message message_id")

    def complete(self, response: TheaResponse) -> None:
        """Complete the conversation with a response."""
        self.response = response
        self.completed_at = datetime.now()
        self.total_duration_seconds = (
            self.completed_at - self.started_at
        ).total_seconds()

    def is_successful(self) -> bool:
        """Check if conversation completed successfully."""
        return (
            self.response is not None
            and self.message.status == MessageStatus.SENT
            and self.completed_at is not None
        )

    def get_duration(self) -> float:
        """Get conversation duration in seconds."""
        if self.total_duration_seconds is not None:
            return self.total_duration_seconds

        if self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()

        return (datetime.now() - self.started_at).total_seconds()


@dataclass
class CookieData:
    """
    Represents cookie data for Thea authentication.

    Pure business entity - no file system details.
    """
    cookies: Dict[str, Any]
    domain: str
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    is_encrypted: bool = False

    def __post_init__(self):
        """Validate cookie data."""
        if not self.cookies:
            raise ValueError("Cookies cannot be empty")

        if not self.domain:
            raise ValueError("Domain cannot be empty")

    def is_expired(self) -> bool:
        """Check if cookies have expired."""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """Check if cookies are valid and not expired."""
        return not self.is_expired() and bool(self.cookies)


@dataclass
class BrowserContext:
    """
    Context information for browser operations.
    """
    state: BrowserState = BrowserState.NOT_STARTED
    current_url: Optional[str] = None
    page_title: Optional[str] = None
    is_page_ready: bool = False
    last_activity: Optional[datetime] = None
    error_message: Optional[str] = None

    def update_state(self, new_state: BrowserState, error: Optional[str] = None) -> None:
        """Update browser state."""
        self.state = new_state
        self.last_activity = datetime.now()

        if error:
            self.error_message = error
        elif new_state == BrowserState.READY:
            self.error_message = None

    def is_operational(self) -> bool:
        """Check if browser is operational."""
        return self.state in [BrowserState.STARTING, BrowserState.READY]


@dataclass
class CommunicationResult:
    """
    Result of a communication operation.

    This is returned by the communication service to indicate success/failure.
    """
    success: bool
    message: TheaMessage
    response: Optional[TheaResponse] = None
    error_message: Optional[str] = None
    duration_seconds: Optional[float] = None

    def __post_init__(self):
        """Ensure result consistency."""
        if self.success and not self.response:
            raise ValueError("Successful communication must have a response")

        if not self.success and self.response:
            raise ValueError("Failed communication cannot have a response")


# Type aliases for better readability
MessageId = str
ConversationId = str
CookieDict = Dict[str, Any]
MetadataDict = Dict[str, Any]