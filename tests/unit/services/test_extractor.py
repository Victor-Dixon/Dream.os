"""
Unit tests for extractor.py

Target: ≥85% coverage, 15+ test methods
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.services.chatgpt.extractor import ConversationExtractor


class TestConversationExtractor:
    """Test suite for ConversationExtractor."""

    @pytest.fixture
    def extractor(self):
        """Create ConversationExtractor instance."""
        with patch('src.services.chatgpt.extractor.get_logger'):
            with patch('src.services.chatgpt.extractor.get_unified_config'):
                with patch('src.services.chatgpt.extractor.MessageParser'):
                    with patch('src.services.chatgpt.extractor.ConversationStorage'):
                        return ConversationExtractor()

    def test_extractor_initialization(self, extractor):
        """Test extractor initializes correctly."""
        assert extractor is not None

    @patch('src.services.chatgpt.extractor.PLAYWRIGHT_AVAILABLE', True)
    def test_extract_conversation_with_playwright(self, extractor):
        """Test extracting conversation when Playwright available."""
        mock_page = Mock()
        extractor.parser = Mock()
        extractor.parser.parse_messages.return_value = []
        
        result = extractor.extract_conversation(mock_page)
        
        assert result is not None

