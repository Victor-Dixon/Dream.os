"""
<!-- SSOT Domain: core -->

Browser Port Interface - Domain Layer
=====================================

Defines the browser interface contract for the domain layer.

V2 Compliance: < 300 lines, single responsibility.
Repository Pattern: Port interface for hexagonal architecture.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-12-03
License: MIT
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class PageReply:
    """
    Standardized response from browser interactions.
    
    Attributes:
        id: Unique identifier for the response
        text: Response text content
        success: Whether the operation succeeded
        error: Optional error message if operation failed
    """
    id: str
    text: str
    success: bool = True
    error: Optional[str] = None


class Browser(ABC):
    """
    Abstract browser interface for domain layer.
    
    This is a port (interface) in hexagonal architecture that defines
    the contract for browser implementations in the infrastructure layer.
    
    V2 Compliance: Interface-only, < 300 lines, single responsibility.
    Design Pattern: Port-Adapter pattern (hexagonal architecture).
    """

    @abstractmethod
    def open(self, profile: Optional[str] = None) -> None:
        """
        Open browser with optional profile.
        
        Args:
            profile: Optional browser profile name
        
        Raises:
            RuntimeError: If browser cannot be opened
            ValueError: If profile is invalid
        """
        pass

    @abstractmethod
    def goto(self, url: str) -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
        
        Raises:
            ValueError: If URL is empty or invalid
            RuntimeError: If navigation fails
        """
        pass

    @abstractmethod
    def send_and_wait(
        self, 
        prompt: str, 
        timeout_s: float = 120.0
    ) -> PageReply:
        """
        Send prompt and wait for response.
        
        Args:
            prompt: Text prompt to send
            timeout_s: Maximum time to wait in seconds (default: 120.0)
        
        Returns:
            PageReply with response data
        
        Raises:
            ValueError: If prompt is empty
            TimeoutError: If response timeout exceeded
            RuntimeError: If browser interaction fails
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close the browser.
        
        Raises:
            RuntimeError: If browser cannot be closed
        """
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """
        Check if browser is ready for interactions.
        
        Returns:
            True if browser is ready, False otherwise
        """
        pass

    @abstractmethod
    def get_current_url(self) -> Optional[str]:
        """
        Get current browser URL.
        
        Returns:
            Current URL or None if not available
        """
        pass

    @abstractmethod
    def wait_for_element(
        self,
        selector: str,
        timeout_s: float = 10.0
    ) -> bool:
        """
        Wait for element to appear on page.
        
        Args:
            selector: CSS selector for the element
            timeout_s: Maximum time to wait in seconds
        
        Returns:
            True if element appeared, False if timeout
        
        Raises:
            ValueError: If selector is empty
        """
        pass
