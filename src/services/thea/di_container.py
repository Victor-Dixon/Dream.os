#!/usr/bin/env python3
"""
Thea Dependency Injection Container - Component Wiring
=====================================================

<!-- SSOT Domain: thea -->

Dependency injection container for Thea service components.
Wires together repositories, services, and infrastructure components.

V2 Compliance: Dependency injection pattern implementation.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from typing import Optional

# Repository implementations
try:
    from .repositories.implementations.secure_cookie_repository import SecureCookieRepository
    from .repositories.implementations.selenium_browser_repository import SeleniumBrowserRepository
    from .repositories.implementations.file_conversation_repository import FileConversationRepository
except ImportError as e:
    print(f"⚠️ Repository implementations not available: {e}")
    SecureCookieRepository = None
    SeleniumBrowserRepository = None
    FileConversationRepository = None

# Service implementations
try:
    from .services.implementations.thea_authentication_service import TheaAuthenticationService
    from .services.implementations.thea_communication_service import TheaCommunicationService
    from .services.implementations.thea_response_service import TheaResponseService
except ImportError as e:
    print(f"⚠️ Service implementations not available: {e}")
    TheaAuthenticationService = None
    TheaCommunicationService = None
    TheaResponseService = None

# Coordinator
try:
    from .thea_service_coordinator import TheaServiceCoordinator
except ImportError:
    TheaServiceCoordinator = None


class TheaDIContainer:
    """
    Dependency injection container for Thea service components.

    Provides centralized configuration and wiring of all Thea components.
    Allows for easy testing by swapping implementations.
    """

    def __init__(self,
                 cookie_file: str = "thea_cookies.enc",
                 key_file: str = "thea_key.bin",
                 conversations_dir: str = "thea_conversations",
                 headless: bool = False,
                 use_secure_cookies: bool = True):
        """
        Initialize the DI container with configuration.

        Args:
            cookie_file: Path to cookie storage file
            key_file: Path to encryption key file
            conversations_dir: Directory for conversation storage
            headless: Whether to run browser in headless mode
            use_secure_cookies: Whether to use encrypted cookie storage
        """
        self.cookie_file = cookie_file
        self.key_file = key_file
        self.conversations_dir = conversations_dir
        self.headless = headless
        self.use_secure_cookies = use_secure_cookies

        # Initialize repositories
        self._init_repositories()

        # Initialize services
        self._init_services()

        # Initialize coordinator
        self._init_coordinator()

    def _init_repositories(self) -> None:
        """Initialize repository components."""
        # Cookie repository
        if SecureCookieRepository and self.use_secure_cookies:
            try:
                self.cookie_repository = SecureCookieRepository(
                    cookie_file=self.cookie_file,
                    key_file=self.key_file
                )
                print("✅ Initialized secure cookie repository")
            except Exception as e:
                print(f"⚠️ Secure cookie repository failed: {e}, falling back to plain JSON")
                self.use_secure_cookies = False

        if not self.use_secure_cookies:
            # Fallback to plain JSON (development only)
            from .repositories.implementations.secure_cookie_repository import PlainJsonCookieRepository
            self.cookie_repository = PlainJsonCookieRepository(
                cookie_file=self.cookie_file.replace('.enc', '.json')
            )
            print("⚠️ Initialized plain JSON cookie repository (INSECURE)")

        # Browser repository
        if SeleniumBrowserRepository:
            try:
                self.browser_repository = SeleniumBrowserRepository(
                    headless=self.headless,
                    use_undetected=True  # Always try undetected for anti-bot
                )
                print("✅ Initialized Selenium browser repository")
            except Exception as e:
                print(f"❌ Browser repository initialization failed: {e}")
                self.browser_repository = None
        else:
            print("❌ Selenium browser repository not available")
            self.browser_repository = None

        # Conversation repository
        if FileConversationRepository:
            try:
                self.conversation_repository = FileConversationRepository(
                    storage_dir=self.conversations_dir
                )
                print("✅ Initialized file conversation repository")
            except Exception as e:
                print(f"❌ Conversation repository initialization failed: {e}")
                self.conversation_repository = None
        else:
            print("❌ File conversation repository not available")
            self.conversation_repository = None

    def _init_services(self) -> None:
        """Initialize service components."""
        # Authentication service
        if (TheaAuthenticationService and
            self.cookie_repository is not None and
            self.browser_repository is not None):

            try:
                self.authentication_service = TheaAuthenticationService(
                    cookie_repository=self.cookie_repository,
                    browser_repository=self.browser_repository
                )
                print("✅ Initialized Thea authentication service")
            except Exception as e:
                print(f"❌ Authentication service initialization failed: {e}")
                self.authentication_service = None
        else:
            print("❌ Authentication service dependencies not available")
            self.authentication_service = None

        # Response service
        if TheaResponseService and self.browser_repository is not None:
            try:
                self.response_service = TheaResponseService(
                    browser_repository=self.browser_repository
                )
                print("✅ Initialized Thea response service")
            except Exception as e:
                print(f"❌ Response service initialization failed: {e}")
                self.response_service = None
        else:
            print("❌ Response service dependencies not available")
            self.response_service = None

        # Communication service
        if (TheaCommunicationService and
            self.browser_repository is not None and
            self.conversation_repository is not None and
            self.authentication_service is not None and
            self.response_service is not None):

            try:
                self.communication_service = TheaCommunicationService(
                    browser_repository=self.browser_repository,
                    conversation_repository=self.conversation_repository,
                    authentication_service=self.authentication_service,
                    response_service=self.response_service
                )
                print("✅ Initialized Thea communication service")
            except Exception as e:
                print(f"❌ Communication service initialization failed: {e}")
                self.communication_service = None
        else:
            print("❌ Communication service dependencies not available")
            self.communication_service = None

    def _init_coordinator(self) -> None:
        """Initialize the main coordinator."""
        if (TheaServiceCoordinator and
            self.authentication_service is not None and
            self.communication_service is not None):

            try:
                self.coordinator = TheaServiceCoordinator(
                    authentication_service=self.authentication_service,
                    communication_service=self.communication_service
                )
                print("✅ Initialized Thea service coordinator")
            except Exception as e:
                print(f"❌ Coordinator initialization failed: {e}")
                self.coordinator = None
        else:
            print("❌ Coordinator dependencies not available")
            self.coordinator = None

    def is_fully_operational(self) -> bool:
        """
        Check if all components are operational.

        Returns:
            True if all required components are available and initialized
        """
        required_components = [
            self.cookie_repository,
            self.browser_repository,
            self.conversation_repository,
            self.authentication_service,
            self.response_service,
            self.communication_service,
            self.coordinator
        ]

        operational = all(component is not None for component in required_components)

        if not operational:
            missing = [
                name for name, component in zip([
                    "cookie_repository", "browser_repository", "conversation_repository",
                    "authentication_service", "response_service", "communication_service", "coordinator"
                ], required_components) if component is None
            ]
            print(f"⚠️ Thea DI container not fully operational. Missing: {', '.join(missing)}")

        return operational

    def get_status_report(self) -> dict:
        """
        Get a status report of all components.

        Returns:
            Dictionary with component status information
        """
        return {
            "repositories": {
                "cookie": self.cookie_repository is not None,
                "browser": self.browser_repository is not None,
                "conversation": self.conversation_repository is not None
            },
            "services": {
                "authentication": self.authentication_service is not None,
                "response": self.response_service is not None,
                "communication": self.communication_service is not None
            },
            "coordinator": self.coordinator is not None,
            "fully_operational": self.is_fully_operational(),
            "configuration": {
                "cookie_file": self.cookie_file,
                "key_file": self.key_file,
                "conversations_dir": self.conversations_dir,
                "headless": self.headless,
                "use_secure_cookies": self.use_secure_cookies
            }
        }


def create_thea_container(**kwargs) -> TheaDIContainer:
    """
    Factory function to create a Thea DI container.

    Args:
        **kwargs: Configuration options passed to TheaDIContainer

    Returns:
        Configured TheaDIContainer instance
    """
    return TheaDIContainer(**kwargs)


# Convenience function for quick setup
def create_default_thea_container() -> TheaDIContainer:
    """
    Create a Thea container with default settings.

    Returns:
        TheaDIContainer with default configuration
    """
    return TheaDIContainer(
        cookie_file="thea_cookies.enc",
        key_file="thea_key.bin",
        conversations_dir="thea_conversations",
        headless=False,
        use_secure_cookies=True
    )