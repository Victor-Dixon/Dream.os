"""
Tests for extractor_message_parser.py - MessageParser class.

Target: ≥85% coverage, 15+ tests.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from src.services.chatgpt.extractor_message_parser import MessageParser, PLAYWRIGHT_AVAILABLE


class TestMessageParser:
    """Test MessageParser class."""

    def test_init_defaults(self):
        """Test MessageParser initialization with defaults."""
        parser = MessageParser()
        assert parser.message_selector == "[data-message-author-role]"
        assert parser.text_selector == "[data-message-text]"
        assert parser.timestamp_selector == "time"
        assert parser.max_messages == 1000
        assert parser.logger is not None

    def test_init_custom(self):
        """Test MessageParser initialization with custom values."""
        custom_logger = Mock()
        parser = MessageParser(
            message_selector=".custom-message",
            text_selector=".custom-text",
            timestamp_selector=".custom-time",
            max_messages=500,
            logger=custom_logger,
        )
        assert parser.message_selector == ".custom-message"
        assert parser.text_selector == ".custom-text"
        assert parser.timestamp_selector == ".custom-time"
        assert parser.max_messages == 500
        assert parser.logger == custom_logger

    @pytest.mark.asyncio
    async def test_extract_messages_no_playwright(self):
        """Test extract_messages when Playwright not available."""
        with patch(
            "src.services.chatgpt.extractor_message_parser.PLAYWRIGHT_AVAILABLE", False
        ):
            parser = MessageParser()
            result = await parser.extract_messages(Mock())
            assert result == []

    @pytest.mark.asyncio
    async def test_extract_messages_success(self):
        """Test successful message extraction."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        # Mock page and elements
        mock_page = AsyncMock()
        mock_element1 = AsyncMock()
        mock_element2 = AsyncMock()
        mock_text_element = AsyncMock()
        mock_timestamp_element = AsyncMock()

        # Setup element attributes
        mock_element1.get_attribute = AsyncMock(return_value="user")
        mock_element1.query_selector = AsyncMock(return_value=mock_text_element)
        mock_text_element.inner_text = AsyncMock(return_value="Hello")
        mock_element1.query_selector = AsyncMock(side_effect=[
            mock_text_element,  # text selector
            mock_timestamp_element,  # timestamp selector
        ])
        mock_timestamp_element.get_attribute = AsyncMock(return_value="2024-01-01T00:00:00Z")

        mock_element2.get_attribute = AsyncMock(return_value="assistant")
        mock_element2.query_selector = AsyncMock(side_effect=[
            mock_text_element,
            mock_timestamp_element,
        ])

        # Setup page methods
        mock_page.wait_for_selector = AsyncMock()
        mock_page.query_selector_all = AsyncMock(return_value=[mock_element1, mock_element2])

        parser = MessageParser(max_messages=10)
        result = await parser.extract_messages(mock_page)

        assert len(result) == 2
        assert result[0]["role"] == "user"
        assert result[1]["role"] == "assistant"

    @pytest.mark.asyncio
    async def test_extract_messages_timeout(self):
        """Test message extraction with timeout."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.wait_for_selector = AsyncMock(side_effect=Exception("Timeout"))

        parser = MessageParser()
        result = await parser.extract_messages(mock_page)

        assert result == []

    @pytest.mark.asyncio
    async def test_extract_messages_max_limit(self):
        """Test message extraction respects max_messages limit."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_elements = [AsyncMock() for _ in range(20)]
        for elem in mock_elements:
            elem.get_attribute = AsyncMock(return_value="user")
            elem.query_selector = AsyncMock(return_value=None)
            elem.inner_text = AsyncMock(return_value="Test message")

        mock_page.wait_for_selector = AsyncMock()
        mock_page.query_selector_all = AsyncMock(return_value=mock_elements)

        parser = MessageParser(max_messages=10)
        result = await parser.extract_messages(mock_page)

        assert len(result) == 10

    @pytest.mark.asyncio
    async def test_extract_message_data_success(self):
        """Test successful message data extraction."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_element = AsyncMock()
        mock_text_element = AsyncMock()
        mock_timestamp_element = AsyncMock()

        mock_element.get_attribute = AsyncMock(return_value="user")
        mock_element.query_selector = AsyncMock(side_effect=[
            mock_text_element,
            mock_timestamp_element,
        ])
        mock_text_element.inner_text = AsyncMock(return_value="Test message")
        mock_timestamp_element.get_attribute = AsyncMock(return_value="2024-01-01T00:00:00Z")

        parser = MessageParser()
        result = await parser._extract_message_data(mock_element, 0)

        assert result is not None
        assert result["role"] == "user"
        assert result["text"] == "Test message"
        assert result["index"] == 0

    @pytest.mark.asyncio
    async def test_extract_message_data_no_role(self):
        """Test message data extraction with missing role."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_element = AsyncMock()
        mock_text_element = AsyncMock()

        mock_element.get_attribute = AsyncMock(return_value=None)
        mock_element.query_selector = AsyncMock(return_value=mock_text_element)
        mock_element.inner_text = AsyncMock(return_value="Test message")

        parser = MessageParser()
        result = await parser._extract_message_data(mock_element, 0)

        assert result is not None
        assert result["role"] == "unknown"

    @pytest.mark.asyncio
    async def test_extract_message_data_exception(self):
        """Test message data extraction with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_element = AsyncMock()
        mock_element.get_attribute = AsyncMock(side_effect=Exception("Error"))

        parser = MessageParser()
        result = await parser._extract_message_data(mock_element, 0)

        assert result is None

    @pytest.mark.asyncio
    async def test_extract_conversation_success(self):
        """Test successful conversation extraction."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.url = "https://chat.openai.com/c/test"
        mock_page.wait_for_selector = AsyncMock()
        mock_page.query_selector_all = AsyncMock(return_value=[])

        parser = MessageParser()
        result = await parser.extract_conversation(mock_page, "test_conv")

        assert result["conversation_id"] == "test_conv"
        assert result["url"] == "https://chat.openai.com/c/test"
        assert "messages" in result
        assert "extraction_time" in result

    @pytest.mark.asyncio
    async def test_extract_conversation_generate_id(self):
        """Test conversation extraction with generated ID."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.url = "https://chat.openai.com/c/test"
        mock_page.wait_for_selector = AsyncMock()
        mock_page.query_selector_all = AsyncMock(return_value=[])

        parser = MessageParser()
        result = await parser.extract_conversation(mock_page)

        assert result["conversation_id"].startswith("conv_")
        assert "extraction_time" in result

    @pytest.mark.asyncio
    async def test_extract_conversation_exception(self):
        """Test conversation extraction with exception."""
        if not PLAYWRIGHT_AVAILABLE:
            pytest.skip("Playwright not available")

        mock_page = AsyncMock()
        mock_page.url = "https://chat.openai.com/c/test"
        # Make extract_messages raise an exception
        parser = MessageParser()
        parser.extract_messages = AsyncMock(side_effect=Exception("Error"))

        result = await parser.extract_conversation(mock_page, "test_conv")

        assert result["conversation_id"] == "test_conv"
        assert "error" in result
        assert result["messages"] == []

