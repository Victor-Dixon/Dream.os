"""
Tests for Browser Port Interface
=================================

Tests for src/domain/ports/browser.py following repository pattern.

V2 Compliance: < 300 lines, ≥85% coverage.
"""

import pytest
from unittest.mock import Mock, MagicMock

from src.domain.ports.browser import Browser, PageReply


class MockBrowser(Browser):
    """Mock implementation of Browser interface for testing."""
    
    def __init__(self):
        self._is_open = False
        self._current_url = None
        self._is_ready = False
    
    def open(self, profile=None):
        """Open browser."""
        if not profile or isinstance(profile, str):
            self._is_open = True
            self._is_ready = True
        else:
            raise ValueError("Invalid profile")
    
    def goto(self, url: str):
        """Navigate to URL."""
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
        if not url.startswith(("http://", "https://")):
            raise ValueError("Invalid URL format")
        self._current_url = url
    
    def send_and_wait(self, prompt: str, timeout_s: float = 120.0) -> PageReply:
        """Send prompt and wait for response."""
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        if timeout_s <= 0:
            raise ValueError("Timeout must be positive")
        
        return PageReply(
            id="test-reply-1",
            text=f"Response to: {prompt}",
            success=True
        )
    
    def close(self):
        """Close browser."""
        if not self._is_open:
            raise RuntimeError("Browser not open")
        self._is_open = False
        self._is_ready = False
    
    def is_ready(self) -> bool:
        """Check if ready."""
        return self._is_ready
    
    def get_current_url(self):
        """Get current URL."""
        return self._current_url
    
    def wait_for_element(self, selector: str, timeout_s: float = 10.0) -> bool:
        """Wait for element."""
        if not selector or not selector.strip():
            raise ValueError("Selector cannot be empty")
        return True


class TestBrowserPort:
    """Test suite for Browser port interface."""
    
    def test_open_browser_success(self):
        """Test opening browser successfully."""
        browser = MockBrowser()
        browser.open()
        assert browser.is_ready() is True
    
    def test_open_browser_with_profile(self):
        """Test opening browser with profile."""
        browser = MockBrowser()
        browser.open(profile="test-profile")
        assert browser.is_ready() is True
    
    def test_goto_valid_url(self):
        """Test navigating to valid URL."""
        browser = MockBrowser()
        browser.open()
        browser.goto("https://example.com")
        assert browser.get_current_url() == "https://example.com"
    
    def test_goto_empty_url_raises_error(self):
        """Test that empty URL raises ValueError."""
        browser = MockBrowser()
        browser.open()
        with pytest.raises(ValueError, match="URL cannot be empty"):
            browser.goto("")
    
    def test_goto_invalid_url_raises_error(self):
        """Test that invalid URL raises ValueError."""
        browser = MockBrowser()
        browser.open()
        with pytest.raises(ValueError, match="Invalid URL format"):
            browser.goto("not-a-url")
    
    def test_send_and_wait_success(self):
        """Test sending prompt and waiting for response."""
        browser = MockBrowser()
        browser.open()
        reply = browser.send_and_wait("Test prompt")
        assert isinstance(reply, PageReply)
        assert reply.id == "test-reply-1"
        assert "Test prompt" in reply.text
        assert reply.success is True
    
    def test_send_and_wait_empty_prompt_raises_error(self):
        """Test that empty prompt raises ValueError."""
        browser = MockBrowser()
        browser.open()
        with pytest.raises(ValueError, match="Prompt cannot be empty"):
            browser.send_and_wait("")
    
    def test_send_and_wait_invalid_timeout_raises_error(self):
        """Test that invalid timeout raises ValueError."""
        browser = MockBrowser()
        browser.open()
        with pytest.raises(ValueError, match="Timeout must be positive"):
            browser.send_and_wait("Test", timeout_s=-1)
    
    def test_close_browser_success(self):
        """Test closing browser successfully."""
        browser = MockBrowser()
        browser.open()
        browser.close()
        assert browser.is_ready() is False
    
    def test_close_browser_not_open_raises_error(self):
        """Test that closing unopened browser raises RuntimeError."""
        browser = MockBrowser()
        with pytest.raises(RuntimeError, match="Browser not open"):
            browser.close()
    
    def test_is_ready_returns_correct_state(self):
        """Test is_ready returns correct state."""
        browser = MockBrowser()
        assert browser.is_ready() is False
        browser.open()
        assert browser.is_ready() is True
        browser.close()
        assert browser.is_ready() is False
    
    def test_wait_for_element_success(self):
        """Test waiting for element successfully."""
        browser = MockBrowser()
        browser.open()
        result = browser.wait_for_element(".test-selector")
        assert result is True
    
    def test_wait_for_element_empty_selector_raises_error(self):
        """Test that empty selector raises ValueError."""
        browser = MockBrowser()
        browser.open()
        with pytest.raises(ValueError, match="Selector cannot be empty"):
            browser.wait_for_element("")
    
    def test_page_reply_dataclass(self):
        """Test PageReply dataclass."""
        reply = PageReply(
            id="test-id",
            text="Test response",
            success=True,
            error=None
        )
        assert reply.id == "test-id"
        assert reply.text == "Test response"
        assert reply.success is True
        assert reply.error is None
    
    def test_page_reply_with_error(self):
        """Test PageReply with error."""
        reply = PageReply(
            id="test-id",
            text="",
            success=False,
            error="Test error"
        )
        assert reply.success is False
        assert reply.error == "Test error"


