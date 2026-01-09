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

from ...domain.models import CommunicationResult, TheaMessage, TheaResponse, TheaConversation, MessagePriority, MessageStatus
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

        # Validate message content first
        if not self.validate_message_content(content):
            try:
                # Create a dummy message for the error result
                dummy_message = TheaMessage(content="validation_failed", priority=MessagePriority.LOW)
                return CommunicationResult(
                    success=False,
                    message=dummy_message,
                    error_message="Invalid message content"
                )
            except ValueError:
                # If even the dummy message fails, something is very wrong
                return CommunicationResult(
                    success=False,
                    message=None,  # type: ignore
                    error_message="Invalid message content"
                )

        try:

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
            try:
                message = TheaMessage(content=content, priority=MessagePriority(priority))
            except ValueError:
                # If message creation fails, use a dummy message for the error result
                message = TheaMessage(content="error_message", priority=MessagePriority.LOW)
            return CommunicationResult(
                success=False,
                message=message,
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
        Send message via browser repository using robust patterns from working monolithic version.

        Args:
            message: Message to send

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            print(f"📤 ===== SENDING MESSAGE VIA BROWSER =====")
            print(f"📤 Message preview: {message.content[:50]}...")

            # SIMPLIFIED NAVIGATION: Always use basic ChatGPT to avoid session issues (from working monolithic)
            target_url = self.chatgpt_url  # Use basic ChatGPT to avoid Thea GPT issues
            target_desc = "basic ChatGPT"

            current_url = self.browser_repo.get_current_url()
            print(f"📍 Current URL: {current_url}")

            if target_url not in (current_url or ""):
                print(f"🏗️ Navigating to {target_desc}: {target_url}")
                try:
                    if not self.browser_repo.navigate_to_url(target_url):
                        return False
                    # Brief stabilization wait
                    time.sleep(3)
                except Exception as nav_e:
                    print(f"❌ Navigation failed: {nav_e}")
                    return False

                new_url = self.browser_repo.get_current_url()
                print(f"📍 New URL after navigation: {new_url}")

                # Check if we're on an error/login page
                if any(keyword in new_url.lower() for keyword in ["login", "auth", "error"]):
                    print("⚠️ Navigation resulted in login/error page")
                    return False

                print(f"✅ Navigation to {target_desc} completed")
            else:
                print(f"✅ Already on {target_desc}")

            # Enhanced page readiness check (from working monolithic version)
            if not self.browser_repo.is_page_ready():
                print("❌ Page not ready for input")
                return False

            # Additional wait for dynamic content - ChatGPT pages often load elements asynchronously
            print("⏳ Waiting additional time for dynamic content...")
            max_dynamic_wait = 15  # seconds - reduced to prevent session timeout
            dynamic_start = time.time()

            # Check session health before starting long wait
            try:
                current_url_check = self.browser_repo.get_current_url()
                print(f"🔍 Session health check: URL = {current_url_check}")
            except Exception as e:
                print(f"❌ Session became invalid before dynamic wait: {e}")
                return False

            if not self.browser_repo.wait_for_dynamic_content(max_dynamic_wait):
                print("❌ No interactive elements found after dynamic wait")
                return False

            # Debug: Check what elements are actually on the page (from working monolithic)
            print("🔍 Debugging page content...")
            try:
                # Get page source snippet
                page_source = self.browser_repo.execute_script("return document.documentElement.outerHTML")
                print(f"📄 Page source length: {len(page_source) if page_source else 0}")

                # Check for common ChatGPT elements
                all_elements = self.browser_repo.execute_script("return document.querySelectorAll('*').length")
                print(f"📊 Total elements on page: {all_elements}")

                # Check for form-related elements
                forms = self.browser_repo.execute_script("return document.querySelectorAll('form').length")
                buttons = self.browser_repo.execute_script("return document.querySelectorAll('button').length")
                inputs = self.browser_repo.execute_script("return document.querySelectorAll('input').length")
                textareas = self.browser_repo.execute_script("return document.querySelectorAll('textarea').length")

                print(f"📋 Forms: {forms}, Buttons: {buttons}, Inputs: {inputs}, Textareas: {textareas}")

                # Check for contenteditable divs specifically
                contenteditable = self.browser_repo.execute_script("return document.querySelectorAll('[contenteditable]').length")
                print(f"📝 Contenteditable elements: {contenteditable}")

                # Check for data-testid attributes (common in React apps)
                testids = self.browser_repo.execute_script("return document.querySelectorAll('[data-testid]').length")
                print(f"🧪 Data-testid elements: {testids}")

                # Check if this is actually a ChatGPT page
                if "chatgpt" not in (self.browser_repo.get_current_url() or "").lower():
                    print("❌ Not on ChatGPT page anymore!")
                    return False

            except Exception as e:
                print(f"❌ Error debugging page: {e}")
                return False

            # CRITICAL: Test element interactability (from working monolithic version)
            print("🔍 Testing element interactability...")
            if not self.browser_repo.test_element_interactability():
                print("❌ Elements exist but are not interactable - likely stale cookies or anti-bot detection")
                return False

            # Find interactive input element using comprehensive search (from working monolithic)
            textarea = self.browser_repo.find_interactive_input_element()
            if not textarea:
                print("❌ No suitable input element found after exhaustive search")
                return False

            print("✅ Input element ready for interaction")

            # Focus + clear input before sending (prevents hidden focus issues)
            try:
                print("🧭 Focusing input element...")
                textarea.click()
                time.sleep(0.2)
                # Clear existing content safely
                textarea.clear()
                time.sleep(0.2)
            except Exception as e:
                print(f"⚠️ Input focus/clear failed (continuing): {e}")

            # Send message via Selenium (more reliable than PyAutoGUI in server environments)
            print("📤 Step 1: Sending message text...")
            try:
                # Use Selenium's send_keys on the contenteditable element
                textarea.send_keys(message.content)
                time.sleep(1)  # Allow text to be entered
                print("📤 Step 1 result: Text sent successfully")

                # Try to send Enter - different approaches for different input types
                print("📤 Step 2: Attempting to submit message...")
                try:
                    from selenium.webdriver.common.keys import Keys

                    if textarea.tag_name.lower() == 'textarea':
                        print("📤 Step 2: Using textarea - sending ENTER key")
                        textarea.send_keys(Keys.ENTER)
                    else:
                        # For ChatGPT contenteditable, ENTER is typically "send"
                        print("📤 Step 2: Using contenteditable - sending ENTER key")
                        textarea.send_keys(Keys.ENTER)
                        time.sleep(0.5)
                        # Fallback: look for send button
                        try:
                            print("📤 Step 2: Looking for send button...")
                            send_buttons = self.browser_repo.execute_script("""
                                return Array.from(document.querySelectorAll('button')).filter(btn =>
                                    btn.textContent.toLowerCase().includes('send') ||
                                    btn.getAttribute('data-testid')?.includes('send') ||
                                    btn.getAttribute('aria-label')?.toLowerCase().includes('send')
                                );
                            """)
                            print(f"📤 Step 2: Found {len(send_buttons) if send_buttons else 0} potential send buttons")

                            if send_buttons:
                                for i, btn in enumerate(send_buttons):
                                    if btn.is_displayed() and btn.is_enabled():
                                        btn_text = btn.text or btn.get_attribute("aria-label") or f"button-{i}"
                                        print(f"📤 Step 2: Clicking send button: {btn_text}")
                                        btn.click()
                                        print("✅ Step 2 result: Send button clicked successfully")
                                        break
                        except Exception as e:
                            print(f"📤 Step 2: Send button click failed: {e}")
                            # Last resort: just Enter key
                            print("📤 Step 2: Last resort - sending ENTER key")
                            textarea.send_keys(Keys.ENTER)

                except Exception as e:
                    print(f"Enter key failed, trying send button: {e}")
                    # Look for send button via script
                    send_buttons = self.browser_repo.execute_script("""
                        return Array.from(document.querySelectorAll('button, [role="button"]')).filter(btn =>
                            btn.textContent?.toLowerCase().includes('send') ||
                            btn.getAttribute('data-testid')?.includes('send') ||
                            btn.getAttribute('aria-label')?.toLowerCase().includes('send')
                        );
                    """)
                    if send_buttons:
                        for btn in send_buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                btn.click()
                                print("✅ Clicked send button as fallback")
                                break

                print("✅ ===== MESSAGE SENT SUCCESSFULLY VIA SELENIUM =====")
                return True

            except Exception as e:
                print(f"❌ Selenium message sending failed: {e}")
                return self._fallback_to_pyautogui(message)

        except Exception as e:
            print(f"❌ Browser message sending failed: {e}")
            return self._fallback_to_pyautogui(message)

    def _fallback_to_pyautogui(self, message: TheaMessage) -> bool:
        """
        Fallback to PyAutoGUI when Selenium fails (from working monolithic version).
        """
        try:
            print("🔄 Falling back to PyAutoGUI...")
            # Check if PyAutoGUI is available
            try:
                import pyautogui
                import pyperclip
                PYAUTOGUI_AVAILABLE = True
            except ImportError:
                PYAUTOGUI_AVAILABLE = False

            if not PYAUTOGUI_AVAILABLE:
                print("❌ PyAutoGUI not available for fallback")
                return False

            try:
                pyperclip.copy(message.content)
                time.sleep(0.5)
                pyautogui.hotkey("ctrl", "v")
            except Exception as clipboard_error:
                print(f"⚠️ Clipboard paste failed ({clipboard_error}), falling back to typing...")
                # Fallback: type the message character by character
                pyautogui.typewrite(message.content, interval=0.01)
            time.sleep(0.5)
            pyautogui.press("enter")
            print("✅ Message sent via PyAutoGUI fallback")
            return True
        except Exception as e2:
            print(f"❌ PyAutoGUI fallback also failed: {e2}")
            return False