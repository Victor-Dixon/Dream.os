"""
Utilities for async testing.

V2 Compliance | Author: Agent-1 | Date: 2025-12-14
Based on Agent-2 architecture review recommendations.
"""

import asyncio
import pytest
from typing import AsyncGenerator, Coroutine, Any


async def run_with_timeout(coro: Coroutine, timeout: float = 5.0) -> Any:
    """Run async function with timeout.
    
    Args:
        coro: Coroutine to run
        timeout: Timeout in seconds (default: 5.0)
        
    Returns:
        Result of coroutine
        
    Raises:
        asyncio.TimeoutError: If coroutine exceeds timeout
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        pytest.fail(f"Test timed out after {timeout} seconds")


@pytest.fixture
async def cleanup_async_tasks():
    """Fixture to ensure cleanup of async tasks after tests."""
    yield
    # Cleanup: cancel all pending tasks in current event loop
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
            for task in pending:
                task.cancel()
            # Wait for all tasks to be canceled
            if pending:
                await asyncio.gather(*pending, return_exceptions=True)
    except RuntimeError:
        # Event loop not available, skip cleanup
        pass

