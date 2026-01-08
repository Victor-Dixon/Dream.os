#!/usr/bin/env python3
"""
Caching Module - FastAPI Services
==================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Caching utilities extracted from fastapi_app.py for V2 compliance.
Provides Redis-based caching with MD5 hash keys for consistent caching.
"""

import json
import logging
import hashlib
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Cache TTL constants
CACHE_TTL = 300  # 5 minutes default TTL

# Redis client (will be set during initialization)
redis_client = None

# Cache metrics for monitoring
cache_metrics = {
    "hits": 0,
    "misses": 0,
    "sets": 0,
    "errors": 0
}


def set_redis_client(client):
    """Set the Redis client for caching operations."""
    global redis_client
    redis_client = client


def get_cache_key(prefix: str, data: Dict[str, Any]) -> str:
    """
    Generate cache key from request data.

    Uses MD5 hash of sorted JSON data for consistent key generation
    across requests with same parameters in different order.

    Args:
        prefix: Cache key prefix (e.g., "api", "response")
        data: Request data dictionary

    Returns:
        str: Cache key with prefix and hash
    """
    # Sort keys for consistent hashing
    sorted_data = json.dumps(data, sort_keys=True, default=str)
    hash_obj = hashlib.md5(sorted_data.encode())
    return f"{prefix}:{hash_obj.hexdigest()}"


async def get_cached_response(cache_key: str) -> Optional[Dict[str, Any]]:
    """
    Get cached response if available.

    Retrieves and deserializes JSON response from Redis cache.
    Updates cache hit/miss metrics.

    Args:
        cache_key: Cache key to retrieve

    Returns:
        Optional[Dict[str, Any]]: Cached response data or None if not found
    """
    if not redis_client:
        cache_metrics["misses"] += 1
        return None

    try:
        cached = await redis_client.get(cache_key)
        if cached:
            cache_metrics["hits"] += 1
            logger.debug(f"Cache hit: {cache_key}")
            return json.loads(cached)
        else:
            cache_metrics["misses"] += 1
    except Exception as e:
        cache_metrics["errors"] += 1
        logger.warning(f"Cache read error for {cache_key}: {e}")

    return None


async def set_cached_response(cache_key: str, response: Dict[str, Any], ttl: int = CACHE_TTL):
    """
    Cache response with TTL.

    Serializes and stores response data in Redis cache with expiration.

    Args:
        cache_key: Cache key to store under
        response: Response data to cache
        ttl: Time-to-live in seconds (default: 5 minutes)
    """
    if not redis_client:
        return

    try:
        await redis_client.setex(cache_key, ttl, json.dumps(response, default=str))
        cache_metrics["sets"] += 1
        logger.debug(f"Cache set: {cache_key} (TTL: {ttl}s)")
    except Exception as e:
        cache_metrics["errors"] += 1
        logger.warning(f"Cache write error for {cache_key}: {e}")


async def invalidate_cache_pattern(pattern: str):
    """
    Invalidate cache keys matching a pattern.

    Uses Redis SCAN to find and delete keys matching the pattern.

    Args:
        pattern: Redis key pattern to match (e.g., "api:*")
    """
    if not redis_client:
        return

    try:
        cursor = 0
        deleted_count = 0

        while True:
            cursor, keys = await redis_client.scan(cursor, match=pattern, count=100)
            if keys:
                await redis_client.delete(*keys)
                deleted_count += len(keys)

            if cursor == 0:
                break

        if deleted_count > 0:
            logger.info(f"Invalidated {deleted_count} cache keys matching '{pattern}'")

    except Exception as e:
        logger.warning(f"Cache invalidation error for pattern '{pattern}': {e}")


def get_cache_metrics() -> Dict[str, int]:
    """
    Get current cache performance metrics.

    Returns:
        dict: Cache metrics (hits, misses, sets, errors)
    """
    return cache_metrics.copy()


def reset_cache_metrics():
    """Reset cache performance metrics to zero."""
    global cache_metrics
    cache_metrics = {
        "hits": 0,
        "misses": 0,
        "sets": 0,
        "errors": 0
    }


__all__ = [
    "get_cache_key",
    "get_cached_response",
    "set_cached_response",
    "invalidate_cache_pattern",
    "get_cache_metrics",
    "reset_cache_metrics",
    "set_redis_client",
    "CACHE_TTL"
]