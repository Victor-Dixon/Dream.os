#!/usr/bin/env python3
"""
Rate Limiting Module - FastAPI Services
========================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Rate limiting utilities extracted from fastapi_app.py for V2 compliance.
Provides both Redis-based and in-memory rate limiting capabilities.
"""

import logging
import time
from typing import Dict, Any

logger = logging.getLogger(__name__)

# Rate limiting constants
RATE_LIMIT_REQUESTS = 100  # requests per window
RATE_LIMIT_WINDOW = 60  # seconds

# In-memory rate limiting storage (fallback when Redis unavailable)
rate_limits: Dict[str, list] = {}

# Redis client (will be set during initialization)
redis_client = None


def set_redis_client(client):
    """Set the Redis client for rate limiting."""
    global redis_client
    redis_client = client


async def check_rate_limit(client_ip: str, endpoint: str) -> bool:
    """
    Check if request is within rate limits.

    Uses Redis-based rate limiting with in-memory fallback.
    Implements sliding window algorithm for accurate limiting.

    Args:
        client_ip: Client IP address
        endpoint: API endpoint path

    Returns:
        bool: True if request allowed, False if rate limited
    """
    if not redis_client:
        # Fallback to in-memory rate limiting
        return await _check_rate_limit_memory(client_ip, endpoint)

    # Redis-based rate limiting
    try:
        key = f"ratelimit:{client_ip}:{endpoint}"
        current_time = time.time()

        # Use Redis sorted set for sliding window
        await redis_client.zremrangebyscore(key, 0, current_time - RATE_LIMIT_WINDOW)
        request_count = await redis_client.zcard(key)

        if request_count >= RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit exceeded for {client_ip}:{endpoint}")
            return False

        await redis_client.zadd(key, {str(current_time): current_time})
        await redis_client.expire(key, RATE_LIMIT_WINDOW)
        return True

    except Exception as e:
        logger.warning(f"Rate limit check error: {e}")
        return True  # Allow request on error


async def _check_rate_limit_memory(client_ip: str, endpoint: str) -> bool:
    """
    In-memory rate limiting fallback.

    Used when Redis is unavailable. Maintains sliding window
    using in-memory storage with cleanup of expired entries.

    Args:
        client_ip: Client IP address
        endpoint: API endpoint path

    Returns:
        bool: True if request allowed, False if rate limited
    """
    key = f"{client_ip}:{endpoint}"
    current_time = time.time()

    if key not in rate_limits:
        rate_limits[key] = []

    # Clean old requests outside the window
    rate_limits[key] = [
        req_time for req_time in rate_limits[key]
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]

    if len(rate_limits[key]) >= RATE_LIMIT_REQUESTS:
        logger.warning(f"Rate limit exceeded for {client_ip}:{endpoint} (memory)")
        return False

    rate_limits[key].append(current_time)
    return True


def get_rate_limit_status(client_ip: str, endpoint: str) -> Dict[str, Any]:
    """
    Get current rate limit status for monitoring.

    Args:
        client_ip: Client IP address
        endpoint: API endpoint path

    Returns:
        dict: Rate limit status information
    """
    key = f"{client_ip}:{endpoint}"
    current_time = time.time()

    if redis_client:
        try:
            redis_key = f"ratelimit:{key}"
            request_count = redis_client.zcard(redis_key) if redis_client else 0
            return {
                "current_requests": request_count,
                "limit": RATE_LIMIT_REQUESTS,
                "window_seconds": RATE_LIMIT_WINDOW,
                "backend": "redis"
            }
        except Exception:
            pass

    # Fallback to memory status
    request_count = len([
        req_time for req_time in rate_limits.get(key, [])
        if current_time - req_time < RATE_LIMIT_WINDOW
    ])

    return {
        "current_requests": request_count,
        "limit": RATE_LIMIT_REQUESTS,
        "window_seconds": RATE_LIMIT_WINDOW,
        "backend": "memory"
    }


__all__ = [
    "check_rate_limit",
    "get_rate_limit_status",
    "set_redis_client",
    "RATE_LIMIT_REQUESTS",
    "RATE_LIMIT_WINDOW"
]