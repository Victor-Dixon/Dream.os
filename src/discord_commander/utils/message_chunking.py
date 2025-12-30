#!/usr/bin/env python3
"""
<!-- SSOT Domain: discord -->

Discord Message Chunking Utility
=================================

Utility functions for splitting long Discord messages to avoid truncation.
Discord limits:
- Regular messages: 2000 characters
- Embed descriptions: 4096 characters
- Embed field values: 1024 characters
- Total embed: 6000 characters

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-01-27
"""

import logging
from typing import List

logger = logging.getLogger(__name__)

# Discord limits
MAX_MESSAGE_LENGTH = 2000
MAX_EMBED_DESCRIPTION = 4096
MAX_FIELD_VALUE = 1024
MAX_EMBED_TOTAL = 6000

# Safe chunk sizes (leave buffer for formatting)
SAFE_MESSAGE_CHUNK = 1900  # Leave 100 chars for headers/footers
SAFE_FIELD_CHUNK = 950  # Leave 74 chars for field formatting
SAFE_EMBED_DESCRIPTION_CHUNK = 4000  # Leave 96 chars for embed formatting


def chunk_message(content: str, max_size: int = SAFE_MESSAGE_CHUNK) -> List[str]:
    """
    Split a long message into chunks that fit within Discord's limits.
    
    Args:
        content: Message content to chunk
        max_size: Maximum size per chunk (default: 1900 for safety)
    
    Returns:
        List of message chunks
    """
    if len(content) <= max_size:
        return [content]
    
    chunks = []
    lines = content.split('\n')
    current_chunk = ""
    
    for line in lines:
        # If adding this line would exceed limit, save current chunk
        if len(current_chunk) + len(line) + 1 > max_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [content[:max_size]]


def chunk_field_value(value: str, max_size: int = SAFE_FIELD_CHUNK) -> List[str]:
    """
    Split a long field value into multiple parts.
    
    Args:
        value: Field value to chunk
        max_size: Maximum size per chunk (default: 950 for safety)
    
    Returns:
        List of field value chunks
    """
    if len(value) <= max_size:
        return [value]
    
    chunks = []
    lines = value.split('\n')
    current_chunk = ""
    
    for line in lines:
        # If adding this line would exceed limit, save current chunk
        if len(current_chunk) + len(line) + 1 > max_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    # Add final chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks if chunks else [value[:max_size]]


def chunk_embed_description(description: str, max_size: int = SAFE_EMBED_DESCRIPTION_CHUNK) -> List[str]:
    """
    Split a long embed description into multiple parts.
    
    Args:
        description: Embed description to chunk
        max_size: Maximum size per chunk (default: 4000 for safety)
    
    Returns:
        List of description chunks
    """
    return chunk_message(description, max_size)


def format_chunk_header(chunk_num: int, total_chunks: int) -> str:
    """Format chunk header for multi-part messages."""
    return f"**Part {chunk_num}/{total_chunks}**\n\n"


__all__ = [
    "chunk_message",
    "chunk_field_value",
    "chunk_embed_description",
    "format_chunk_header",
    "MAX_MESSAGE_LENGTH",
    "MAX_FIELD_VALUE",
    "MAX_EMBED_DESCRIPTION",
    "SAFE_MESSAGE_CHUNK",
    "SAFE_FIELD_CHUNK",
]

