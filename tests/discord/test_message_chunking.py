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
    chunk_embed_description,
    format_chunk_header,
    MAX_MESSAGE_LENGTH,
    MAX_FIELD_VALUE,
    SAFE_MESSAGE_CHUNK,
    SAFE_FIELD_CHUNK
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

    def test_chunk_embed_description(self):
        """Test chunking embed description."""
        long_description = "C" * 5000  # Exceeds embed description limit
        chunks = chunk_embed_description(long_description)
        assert len(chunks) > 1
        assert all(len(chunk) <= 4000 for chunk in chunks)

    def test_format_chunk_header(self):
        """Test chunk header formatting."""
        header = format_chunk_header(1, 3)
        assert "Part 1/3" in header
        assert header.startswith("**")

    def test_chunk_preserves_content(self):
        """Test that chunking preserves all content."""
        original = "Test message with content " * 100
        chunks = chunk_message(original)
        combined = "".join(chunks)
        assert original in combined or combined in original

