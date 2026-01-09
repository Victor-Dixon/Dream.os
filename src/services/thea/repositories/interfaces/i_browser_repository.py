#!/usr/bin/env python3
"""
Browser Repository Interface - Browser Automation Contract
=========================================================

<!-- SSOT Domain: thea -->

Repository interface for browser automation operations.
Defines the contract for browser control and interaction.

V2 Compliance: Repository pattern, abstracted browser operations.

Author: Agent-4 (V2 Architecture Specialist)
Date: 2025-01-08
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Protocol

from ...domain.models import BrowserContext


class IBrowserRepository(Protocol):
    """
    Interface for browser automation operations.

    This interface abstracts browser interactions, allowing different
    implementations (Selenium, Playwright, etc.) and easy testing.
    """

    @abstractmethod
    def start_browser(self) -> bool:
        """
        Start the browser instance.

        Returns:
            True if browser started successfully, False otherwise
        """
        pass

    @abstractmethod
    def close_browser(self) -> bool:
        """
        Close the browser instance.

        Returns:
            True if browser closed successfully, False otherwise
        """
        pass

    @abstractmethod
    def navigate_to_url(self, url: str) -> bool:
        """
        Navigate to the specified URL.

        Args:
            url: URL to navigate to

        Returns:
            True if navigation successful, False otherwise
        """
        pass

    @abstractmethod
    def get_current_url(self) -> Optional[str]:
        """
        Get the current URL.

        Returns:
            Current URL string, or None if unavailable
        """
        pass

    @abstractmethod
    def get_page_title(self) -> Optional[str]:
        """
        Get the current page title.

        Returns:
            Page title string, or None if unavailable
        """
        pass

    @abstractmethod
    def is_page_ready(self) -> bool:
        """
        Check if the page is fully loaded and ready for interaction.

        Returns:
            True if page is ready, False otherwise
        """
        pass

    @abstractmethod
    def find_input_element(self, selector: str) -> Optional[Any]:
        """
        Find an input element on the page.

        Args:
            selector: CSS selector for the input element

        Returns:
            Element object if found, None otherwise
        """
        pass

    @abstractmethod
    def send_text_to_element(self, element: Any, text: str) -> bool:
        """
        Send text to a specific element.

        Args:
            element: Element to send text to
            text: Text to send

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def click_element(self, element: Any) -> bool:
        """
        Click on a specific element.

        Args:
            element: Element to click

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def submit_form(self, element: Any) -> bool:
        """
        Submit a form via an element.

        Args:
            element: Form element or submit button

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def wait_for_element(self, selector: str, timeout: int = 10) -> Optional[Any]:
        """
        Wait for an element to appear on the page.

        Args:
            selector: CSS selector to wait for
            timeout: Maximum time to wait in seconds

        Returns:
            Element if found within timeout, None otherwise
        """
        pass

    @abstractmethod
    def get_element_text(self, selector: str) -> Optional[str]:
        """
        Get text content of an element.

        Args:
            selector: CSS selector for the element

        Returns:
            Text content if found, None otherwise
        """
        pass

    @abstractmethod
    def get_elements_text(self, selector: str) -> list[str]:
        """
        Get text content of multiple elements.

        Args:
            selector: CSS selector for elements

        Returns:
            List of text contents
        """
        pass

    @abstractmethod
    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript in the browser context.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Result of script execution
        """
        pass

    @abstractmethod
    def load_cookies(self, cookies: Dict[str, Any]) -> bool:
        """
        Load cookies into the browser.

        Args:
            cookies: Cookie dictionary to load

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    def get_cookies(self) -> Dict[str, Any]:
        """
        Get current cookies from the browser.

        Returns:
            Dictionary of current cookies
        """
        pass

    @abstractmethod
    def get_browser_context(self) -> BrowserContext:
        """
        Get current browser context information.

        Returns:
            BrowserContext with current state
        """
        pass

    @abstractmethod
    def is_browser_operational(self) -> bool:
        """
        Check if browser is operational and ready for commands.

        Returns:
            True if operational, False otherwise
        """
        pass