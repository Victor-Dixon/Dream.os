"""
<!-- SSOT Domain: discord -->

Discord Commander Utilities
============================

Utility modules for Discord bot functionality.
"""

from .message_chunking import (
    chunk_message,
    chunk_field_value,
    chunk_embed_description,
    format_chunk_header,
    MAX_MESSAGE_LENGTH,
    MAX_FIELD_VALUE,
    MAX_EMBED_DESCRIPTION,
    SAFE_MESSAGE_CHUNK,
    SAFE_FIELD_CHUNK,
)

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

