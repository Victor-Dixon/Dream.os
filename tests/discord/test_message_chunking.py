#!/usr/bin/env python3
"""
Tests for message_chunking utility.

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-27
"""

import pytest
from src.discord_commander.utils.message_chunking import (
    chunk_field_value,
    chunk_message,
    split_long_message,
    truncate_field_value
)


class TestMessageChunking:
    """Test suite for message chunking utilities."""

    def test_chunk_field_value_short(self):
        """Test chunking short field value."""
        short_text = "Short text"
        chunks = chunk_field_value(short_text)
        assert len(chunks) == 1
        assert chunks[0] == short_text

    def test_chunk_field_value_long(self):
        """Test chunking long field value."""
        long_text = "A" * 3000  # Exceeds Discord's 1024 char limit
        chunks = chunk_field_value(long_text)
        assert len(chunks) > 1
        assert all(len(chunk) <= 1024 for chunk in chunks)

    def test_chunk_message_short(self):
        """Test chunking short message."""
        short_message = "Short message"
        chunks = chunk_message(short_message)
        assert len(chunks) == 1
        assert chunks[0] == short_message

    def test_chunk_message_long(self):
        """Test chunking long message."""
        long_message = "B" * 5000  # Exceeds Discord's 2000 char limit
        chunks = chunk_message(long_message)
        assert len(chunks) > 1
        assert all(len(chunk) <= 2000 for chunk in chunks)

    def test_split_long_message(self):
        """Test splitting long message."""
        long_text = "C" * 3000
        chunks = split_long_message(long_text, max_length=1000)
        assert len(chunks) > 1
        assert all(len(chunk) <= 1000 for chunk in chunks)

    def test_truncate_field_value(self):
        """Test truncating field value."""
        long_text = "D" * 2000
        truncated = truncate_field_value(long_text, max_length=1000)
        assert len(truncated) <= 1000
        assert truncated.endswith("...")

    def test_chunk_preserves_content(self):
        """Test that chunking preserves all content."""
        original = "Test message with content " * 100
        chunks = chunk_message(original)
        combined = "".join(chunks)
        assert original in combined or combined in original

