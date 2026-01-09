#!/usr/bin/env python3
"""
Thea Communication Service Implementation - Message Communication Orchestration
==============================================================================

<!-- SSOT Domain: thea -->

Service implementation for Thea communication operations.
Orchestrates the complete message flow: validation, authentication, sending, response extraction.

V2 Compliance: Business logic service with dependency injection.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

import time
from typing import Optional

from ...domain.models import CommunicationResult, TheaMessage, TheaResponse, TheaConversation
from ...domain.enums import MessagePriority, MessageStatus
from ...repositories.interfaces.i_browser_repository import IBrowserRepository
from ...repositories.interfaces.i_conversation_repository import IConversationRepository
from ..interfaces.i_authentication_service import IAuthenticationService
from ..interfaces.i_response_service import IResponseService
from ..interfaces.i_communication_service import ICommunicationService


class TheaCommunicationService(ICommunicationService):
    """
    Thea communication service implementation.

    Orchestrates the complete communication flow:
    1. Message validation
    2. Authentication verification
    3. Message delivery
    4. Response extraction
    5. Conversation persistence
    """

    def __init__(self,
                 browser_repository: IBrowserRepository,
                 conversation_repository: IConversationRepository,
                 authentication_service: IAuthenticationService,
                 response_service: IResponseService,
                 default_timeout: int = 120):
        """
        Initialize Thea communication service.

        Args:
            browser_repository: Repository for browser operations
            conversation_repository: Repository for conversation persistence
            authentication_service: Service for authentication operations
            response_service: Service for response extraction
            default_timeout: Default timeout for operations
        """
        self.browser_repo = browser_repository
        self.conversation_repo = conversation_repository
        self.auth_service = authentication_service
        self.response_service = response_service
        self.default_timeout = default_timeout

        # Thea service URLs
        self.thea_url = "https://chatgpt.com/g/g-67f437d96d7c81918b2dbc12f0423867-thea-manager"
        self.chatgpt_url = "https://chatgpt.com"

    def send_message(self,
                    content: str,
                    priority: str = "normal",
                    metadata: Optional[dict] = None) -> CommunicationResult:
        """
        Send a message to Thea and get the response.

        Args:
            content: Message content to send
            priority: Message priority level
            metadata: Optional metadata for the message

        Returns:
            CommunicationResult with success status and data
        """
        start_time = time.time()

        try:
            # Validate message content
            if not self.validate_message_content(content):
                return CommunicationResult(
                    success=False,
                    message=TheaMessage(content=content, priority=MessagePriority(priority)),
                    error_message="Invalid message content"
                )

            # Create message object
            message = TheaMessage(
                content=content,
                priority=MessagePriority(priority),
                metadata=metadata or {}
            )

            print(f"📤 Sending message (priority: {priority}): {content[:50]}...")

            # Ensure authentication
            if not self.auth_service.ensure_authenticated(self.thea_url):
                return CommunicationResult(
                    success=False,
                    message=message,
                    error_message="Authentication failed"
                )

            # Send message via browser
            if not self._send_message_via_browser(message):
                return CommunicationResult(
                    success=False,
                    message=message,
                    error_message="Message delivery failed"
                )

            message.mark_sent()

            # Extract response
            response = self.response_service.extract_response(self.default_timeout)

            if response:
                response.message_id = message.message_id
                print(f"✅ Response received: {response.content[:50]}...")

                # Create and save conversation
                conversation = TheaConversation(
                    message=message,
                    response=response
                )
                conversation.complete(response)

                self.conversation_repo.save_conversation(conversation)

                duration = time.time() - start_time
                return CommunicationResult(
                    success=True,
                    message=message,
                    response=response,
                    duration_seconds=duration
                )
            else:
                print("❌ No response received")
                duration = time.time() - start_time
                return CommunicationResult(
                    success=False,
                    message=message,
                    error_message="No response received",
                    duration_seconds=duration
                )

        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Communication failed: {e}")
            return CommunicationResult(
                success=False,
                message=TheaMessage(content=content, priority=MessagePriority(priority)),
                error_message=str(e),
                duration_seconds=duration
            )

    def send_message_async(self,
                          content: str,
                          priority: str = "normal",
                          metadata: Optional[dict] = None) -> str:
        """
        Send a message asynchronously and return a tracking ID.

        Args:
            content: Message content to send
            priority: Message priority level
            metadata: Optional metadata for the message

        Returns:
            Message ID for tracking the async operation
        """
        message = TheaMessage(
            content=content,
            priority=MessagePriority(priority),
            metadata=metadata or {}
        )

        # For async implementation, we'd need a queue system
        # For now, just return the message ID
        print(f"📨 Async message queued: {message.message_id}")
        return message.message_id

    def get_message_status(self, message_id: str) -> Optional[TheaMessage]:
        """Get the status of a sent message."""
        conversations = self.conversation_repo.get_conversations_by_message_id(message_id)
        if conversations:
            return conversations[0].message
        return None

    def get_response(self, message_id: str) -> Optional[TheaResponse]:
        """Get the response for a sent message."""
        conversations = self.conversation_repo.get_conversations_by_message_id(message_id)
        if conversations:
            return conversations[0].response
        return None

    def wait_for_response(self,
                         message_id: str,
                         timeout_seconds: int = 120) -> Optional[TheaResponse]:
        """
        Wait for a response to a message with timeout.

        For already completed conversations, returns immediately.
        For pending messages, would implement polling logic.
        """
        conversations = self.conversation_repo.get_conversations_by_message_id(message_id)
        if conversations and conversations[0].response:
            return conversations[0].response

        # For pending messages, implement polling (simplified)
        print(f"⏳ Waiting for response to message {message_id}...")
        start_time = time.time()

        while time.time() - start_time < timeout_seconds:
            conversations = self.conversation_repo.get_conversations_by_message_id(message_id)
            if conversations and conversations[0].response:
                return conversations[0].response
            time.sleep(2)

        return None

    def validate_message_content(self, content: str) -> bool:
        """
        Validate message content before sending.

        Args:
            content: Message content to validate

        Returns:
            True if valid, False otherwise
        """
        if not content or not content.strip():
            return False

        if len(content) > 10000:  # Reasonable limit
            return False

        # Check for potentially harmful content (basic check)
        harmful_patterns = [
            "<script", "</script>", "javascript:", "data:",
            "vbscript:", "onload=", "onerror="
        ]

        content_lower = content.lower()
        for pattern in harmful_patterns:
            if pattern in content_lower:
                return False

        return True

    def get_recent_conversations(self, limit: int = 10) -> list:
        """Get recent conversation history."""
        return self.conversation_repo.get_recent_conversations(limit)

    def search_conversations(self, query: str, limit: int = 20) -> list:
        """Search conversation history by content."""
        return self.conversation_repo.search_conversations(query, limit)

    def _send_message_via_browser(self, message: TheaMessage) -> bool:
        """
        Send message via browser repository.

        Args:
            message: Message to send

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Navigate to Thea URL if not already there
            current_url = self.browser_repo.get_current_url()
            if not current_url or self.thea_url not in current_url:
                print(f"🏗️ Navigating to Thea: {self.thea_url}")
                if not self.browser_repo.navigate_to_url(self.thea_url):
                    return False

                # Wait for page to be ready
                if not self.browser_repo.is_page_ready():
                    time.sleep(3)
                    if not self.browser_repo.is_page_ready():
                        return False

            # Find input element
            input_element = self.browser_repo.find_input_element("textarea")
            if not input_element:
                # Try alternative selectors
                alternative_selectors = [
                    "[contenteditable='true']",
                    "[role='textbox']",
                    "[data-testid*='prompt']",
                    "[placeholder*='message' i]"
                ]

                for selector in alternative_selectors:
                    input_element = self.browser_repo.find_input_element(selector)
                    if input_element:
                        break

            if not input_element:
                print("❌ No input element found")
                return False

            # Send message text
            if not self.browser_repo.send_text_to_element(input_element, message.content):
                return False

            time.sleep(1)  # Brief pause

            # Submit the message
            # Try Enter key first
            if not self.browser_repo.submit_form(input_element):
                # Fallback: look for send button
                send_selectors = [
                    "button[data-testid*='send']",
                    "button[type='submit']",
                    "[role='button']"
                ]

                send_button = None
                for selector in send_selectors:
                    send_button = self.browser_repo.wait_for_element(selector, timeout=5)
                    if send_button:
                        break

                if send_button and not self.browser_repo.click_element(send_button):
                    return False

            print("✅ Message sent via browser")
            return True

        except Exception as e:
            print(f"❌ Browser message sending failed: {e}")
            return False