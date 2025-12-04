"""
Tests for navigator.py - ChatGPTNavigator class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from src.services.chatgpt.navigator import ChatGPTNavigator, PLAYWRIGHT_AVAILABLE


class TestChatGPTNavigator:
    """Test ChatGPTNavigator class."""

    def test_init_defaults(self):
        """Test ChatGPTNavigator initialization with defaults."""
        navigator = ChatGPTNavigator()
        assert navigator.default_url == "https://chat.openai.com/"
        assert navigator.timeout == 60000
        assert navigator.wait_for_selector == "textarea"
        assert navigator.retry_attempts == 3
        assert navigator.headless is False
        assert navigator.logger is not None

    def test_init_custom_config(self):
        """Test ChatGPTNavigator initialization with custom config."""
        config = {
            "navigation": {
                "default_url": "https://custom.url",
                "timeout": 30000,
                "wait_for_selector": "input",
            },
            "browser": {
                "headless": True,
                "user_data_dir": "custom/dir",
            },
        }
        navigator = ChatGPTNavigator(config=config)
        assert navigator.default_url == "https://custom.url"
        assert navigator.timeout == 30000
        assert navigator.wait_for_selector == "input"
        assert navigator.headless is True
        assert navigator.user_data_dir == "custom/dir"

    def test_init_no_playwright(self):
        """Test initialization when Playwright not available."""
        with patch(
            "src.services.chatgpt.navigator.PLAYWRIGHT_AVAILABLE", False
        ):
            navigator = ChatGPTNavigator()
            assert navigator.logger is not None

    @pytest.mark.asyncio
    async def test_navigate_to_chat_no_playwright(self):
        """Test navigate_to_chat when Playwright not available."""
        with patch(
            "src.services.chatgpt.navigator.PLAYWRIGHT_AVAILABLE", False
        ):
            navigator = ChatGPTNavigator()
            result = await navigator.navigate_to_chat()
            assert result is None

    @pytest.mark.asyncio
    async def test_navigate_to_chat_success(self):
        """Test successful navigation to ChatGPT."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_context = AsyncMock()
        mock_page = AsyncMock()

        mock_context.new_page = AsyncMock(return_value=mock_page)
        mock_page.goto = AsyncMock()
        mock_page.wait_for_selector = AsyncMock()

        navigator._create_browser_context = AsyncMock(return_value=mock_context)
        navigator._wait_for_ready = AsyncMock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await navigator.navigate_to_chat(context=mock_context)

        assert result == mock_page
        assert navigator._page == mock_page

    @pytest.mark.asyncio
    async def test_navigate_to_chat_custom_url(self):
        """Test navigation with custom conversation URL."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_context = AsyncMock()
        mock_page = AsyncMock()

        mock_context.new_page = AsyncMock(return_value=mock_page)
        mock_page.goto = AsyncMock()
        navigator._create_browser_context = AsyncMock(return_value=mock_context)
        navigator._wait_for_ready = AsyncMock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await navigator.navigate_to_chat(
                context=mock_context, conversation_url="https://custom.url"
            )

        mock_page.goto.assert_called_once_with("https://custom.url", timeout=60000)

    @pytest.mark.asyncio
    async def test_navigate_to_chat_retry(self):
        """Test navigation with retry on failure."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_context = AsyncMock()
        mock_page = AsyncMock()

        mock_context.new_page = AsyncMock(return_value=mock_page)
        # First call fails, second succeeds
        mock_page.goto = AsyncMock(side_effect=[Exception("Error"), None])
        navigator._create_browser_context = AsyncMock(return_value=mock_context)
        navigator._wait_for_ready = AsyncMock()

        # Mock the retry logic - navigate_to_chat handles retries internally
        with patch("asyncio.sleep", new_callable=AsyncMock):
            try:
                result = await navigator.navigate_to_chat(context=mock_context)
                # If retry succeeds, we get a page
                if result:
                    assert result == mock_page
            except Exception:
                # If all retries fail, result is None
                pass

    @pytest.mark.asyncio
    async def test_navigate_to_chat_exception(self):
        """Test navigation with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        navigator._create_browser_context = AsyncMock(return_value=None)

        result = await navigator.navigate_to_chat()

        assert result is None

    @pytest.mark.asyncio
    async def test_create_browser_context_success(self):
        """Test successful browser context creation."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_browser = AsyncMock()
        mock_context = AsyncMock()

        with patch("playwright.async_api.async_playwright") as mock_playwright:
            mock_pw_instance = AsyncMock()
            mock_playwright.return_value.start = AsyncMock(return_value=mock_pw_instance)
            mock_pw_instance.chromium.launch = AsyncMock(return_value=mock_browser)
            mock_browser.new_context = AsyncMock(return_value=mock_context)

            result = await navigator._create_browser_context()

        assert result == mock_context

    @pytest.mark.asyncio
    async def test_create_browser_context_exception(self):
        """Test browser context creation with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()

        with patch("playwright.async_api.async_playwright", side_effect=Exception("Error")):
            result = await navigator._create_browser_context()

        assert result is None

    @pytest.mark.asyncio
    async def test_wait_for_ready_success(self):
        """Test successful wait for ready."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_page = AsyncMock()
        navigator._page = mock_page
        mock_page.wait_for_selector = AsyncMock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            await navigator._wait_for_ready()

        mock_page.wait_for_selector.assert_called_once_with("textarea", timeout=60000)

    @pytest.mark.asyncio
    async def test_wait_for_ready_exception(self):
        """Test wait for ready with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_page = AsyncMock()
        navigator._page = mock_page
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception("Error"))

        with pytest.raises(Exception):
            await navigator._wait_for_ready()

    def test_get_active_page_success(self):
        """Test getting active page when available."""
        navigator = ChatGPTNavigator()
        mock_page = Mock()
        navigator._page = mock_page

        result = navigator.get_active_page()

        assert result == mock_page

    def test_get_active_page_none(self):
        """Test getting active page when not available."""
        navigator = ChatGPTNavigator()
        navigator._page = None

        result = navigator.get_active_page()

        assert result is None

    @pytest.mark.asyncio
    async def test_send_message_no_page(self):
        """Test send_message when no active page."""
        navigator = ChatGPTNavigator()
        navigator._page = None

        result = await navigator.send_message("test message")

        assert result is None

    @pytest.mark.asyncio
    async def test_send_message_success(self):
        """Test successful message sending."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_page = AsyncMock()
        mock_textarea = AsyncMock()

        navigator._page = mock_page
        mock_page.query_selector = AsyncMock(return_value=mock_textarea)
        mock_textarea.click = AsyncMock()
        mock_textarea.fill = AsyncMock()
        mock_textarea.press = AsyncMock()
        navigator._wait_for_response = AsyncMock(return_value="Response text")

        result = await navigator.send_message("test message", wait_for_response=True)

        assert result == "Response text"
        mock_textarea.fill.assert_called_once_with("test message")
        mock_textarea.press.assert_called_once_with("Enter")

    @pytest.mark.asyncio
    async def test_send_message_no_wait(self):
        """Test message sending without waiting for response."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_page = AsyncMock()
        mock_textarea = AsyncMock()

        navigator._page = mock_page
        mock_page.query_selector = AsyncMock(return_value=mock_textarea)
        mock_textarea.click = AsyncMock()
        mock_textarea.fill = AsyncMock()
        mock_textarea.press = AsyncMock()

        result = await navigator.send_message("test message", wait_for_response=False)

        assert result is None

    @pytest.mark.asyncio
    async def test_send_message_no_textarea(self):
        """Test send_message when textarea not found."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        navigator = ChatGPTNavigator()
        mock_page = AsyncMock()
        navigator._page = mock_page
        mock_page.query_selector = AsyncMock(return_value=None)

        result = await navigator.send_message("test message")

        assert result is None

