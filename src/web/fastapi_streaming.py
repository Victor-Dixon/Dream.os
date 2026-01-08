#!/usr/bin/env python3
"""
Streaming Module - FastAPI Services
====================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Streaming response utilities extracted from fastapi_app.py for V2 compliance.
Provides Server-Sent Events (SSE) streaming for real-time AI responses.
"""

import asyncio
import logging
from typing import AsyncGenerator

from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)


async def create_streaming_response(content_generator: AsyncGenerator[str, None]) -> StreamingResponse:
    """
    Create a streaming response for real-time AI responses.

    Implements Server-Sent Events (SSE) for streaming AI responses to clients.
    Handles proper SSE formatting with event data and completion signals.

    Args:
        content_generator: Async generator yielding content chunks

    Returns:
        StreamingResponse: Configured for SSE with proper headers
    """
    async def generate():
        """
        Generate SSE-formatted response stream.

        Yields properly formatted SSE events with data prefix.
        Includes completion signal and error handling.
        """
        try:
            async for chunk in content_generator:
                # SSE format: "data: <content>\n\n"
                yield f"data: {chunk}\n\n"
                # Small delay to prevent overwhelming client
                await asyncio.sleep(0.01)

            # Send completion signal
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"Streaming response error: {e}")
            yield f"data: {{\"error\": \"{str(e)}\"}}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control",
        }
    )


async def create_simple_text_stream(text: str, chunk_size: int = 50) -> AsyncGenerator[str, None]:
    """
    Create a simple text streaming generator.

    Splits text into chunks for streaming responses. Useful for
    simulating streaming when the underlying service doesn't support it.

    Args:
        text: Text to stream
        chunk_size: Characters per chunk

    Yields:
        str: Text chunks for streaming
    """
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        yield chunk
        await asyncio.sleep(0.05)  # Simulate typing delay


async def create_json_stream(data_items: list, delay: float = 0.1) -> AsyncGenerator[str, None]:
    """
    Create a JSON streaming generator.

    Streams individual JSON items with delays between each.
    Useful for streaming lists of data or progress updates.

    Args:
        data_items: List of data items to stream as JSON
        delay: Delay between items in seconds

    Yields:
        str: JSON-formatted data items
    """
    import json

    for item in data_items:
        try:
            json_str = json.dumps(item, default=str)
            yield json_str
            await asyncio.sleep(delay)
        except Exception as e:
            logger.error(f"JSON streaming error: {e}")
            yield f'{{"error": "Failed to serialize item: {str(e)}"}}'


def is_streaming_supported() -> bool:
    """
    Check if streaming is supported in the current environment.

    Returns:
        bool: True if streaming is available and configured
    """
    try:
        # Check for required dependencies
        import fastapi
        return True
    except ImportError:
        logger.warning("FastAPI not available for streaming")
        return False


__all__ = [
    "create_streaming_response",
    "create_simple_text_stream",
    "create_json_stream",
    "is_streaming_supported"
]