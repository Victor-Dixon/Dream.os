"""
Tests for navigator_messaging.py - NavigatorMessaging class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.chatgpt.navigator_messaging import NavigatorMessaging, PLAYWRIGHT_AVAILABLE


class TestNavigatorMessaging:
    """Test NavigatorMessaging class."""

    @pytest.mark.asyncio
    async def test_send_message_no_playwright(self):
        """Test send_message when Playwright not available."""
        with patch(
            "src.services.chatgpt.navigator_messaging.PLAYWRIGHT_AVAILABLE", False
        ):
            logger = Mock()
            result = await NavigatorMessaging.send_message_to_page(
                None, "test message", False, "textarea", logger
            )
            assert result is None

    @pytest.mark.asyncio
    async def test_send_message_no_page(self):
        """Test send_message when page is None."""
        logger = Mock()
        result = await NavigatorMessaging.send_message_to_page(
            None, "test message", False, "textarea", logger
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_send_message_success(self):
        """Test successful message sending."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_textarea = AsyncMock()

        mock_page.wait_for_selector = AsyncMock(return_value=mock_textarea)
        mock_textarea.fill = AsyncMock()
        mock_page.keyboard = AsyncMock()
        mock_page.keyboard.press = AsyncMock()

        logger = Mock()

        result = await NavigatorMessaging.send_message_to_page(
            mock_page, "test message", False, "textarea", logger
        )

        assert result is None
        mock_textarea.fill.assert_called_once_with("test message")
        mock_page.keyboard.press.assert_called_once_with("Enter")

    @pytest.mark.asyncio
    async def test_send_message_wait_for_response(self):
        """Test message sending with wait_for_response."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_textarea = AsyncMock()
        mock_message = AsyncMock()
        mock_text_element = AsyncMock()

        mock_page.wait_for_selector = AsyncMock(return_value=mock_textarea)
        mock_textarea.fill = AsyncMock()
        mock_page.keyboard = AsyncMock()
        mock_page.keyboard.press = AsyncMock()
        mock_page.query_selector_all = AsyncMock(return_value=[mock_message])
        mock_message.query_selector = AsyncMock(return_value=mock_text_element)
        mock_text_element.inner_text = AsyncMock(return_value="Response text")

        logger = Mock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await NavigatorMessaging.send_message_to_page(
                mock_page, "test message", True, "textarea", logger
            )

        assert result == "Response text"

    @pytest.mark.asyncio
    async def test_send_message_selector_not_found(self):
        """Test message sending when selector not found."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.wait_for_selector = AsyncMock(return_value=None)

        logger = Mock()

        result = await NavigatorMessaging.send_message_to_page(
            mock_page, "test message", False, "textarea", logger
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_send_message_exception(self):
        """Test message sending with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception("Error"))

        logger = Mock()

        result = await NavigatorMessaging.send_message_to_page(
            mock_page, "test message", False, "textarea", logger
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_wait_for_response_success(self):
        """Test successful response waiting."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_message = AsyncMock()
        mock_text_element = AsyncMock()

        mock_page.query_selector_all = AsyncMock(return_value=[mock_message])
        mock_message.query_selector = AsyncMock(return_value=mock_text_element)
        mock_text_element.inner_text = AsyncMock(return_value="Response text")

        logger = Mock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await NavigatorMessaging.wait_for_response(mock_page, logger)

        assert result == "Response text"

    @pytest.mark.asyncio
    async def test_wait_for_response_no_messages(self):
        """Test response waiting with no messages."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.query_selector_all = AsyncMock(return_value=[])

        logger = Mock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await NavigatorMessaging.wait_for_response(mock_page, logger)

        assert result is None

    @pytest.mark.asyncio
    async def test_wait_for_response_no_text_element(self):
        """Test response waiting with no text element."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_message = AsyncMock()

        mock_page.query_selector_all = AsyncMock(return_value=[mock_message])
        mock_message.query_selector = AsyncMock(return_value=None)

        logger = Mock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await NavigatorMessaging.wait_for_response(mock_page, logger)

        assert result is None

    @pytest.mark.asyncio
    async def test_wait_for_response_exception(self):
        """Test response waiting with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.query_selector_all = AsyncMock(side_effect=Exception("Error"))

        logger = Mock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await NavigatorMessaging.wait_for_response(mock_page, logger)

        assert result is None

    @pytest.mark.asyncio
    async def test_wait_for_response_timeout(self):
        """Test response waiting with custom timeout."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_message = AsyncMock()
        mock_text_element = AsyncMock()

        mock_page.query_selector_all = AsyncMock(return_value=[mock_message])
        mock_message.query_selector = AsyncMock(return_value=mock_text_element)
        mock_text_element.inner_text = AsyncMock(return_value="Response")

        logger = Mock()

        with patch("asyncio.sleep", new_callable=AsyncMock):
            result = await NavigatorMessaging.wait_for_response(
                mock_page, logger, timeout=60000
            )

        assert result == "Response"




