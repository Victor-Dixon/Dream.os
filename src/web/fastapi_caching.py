"""
FastAPI Redis Caching Module
=============================

V2 Compliant - Complete Redis-based caching implementation
Author: Agent-7 (Web Development Specialist)
Date: 2026-01-10

Implements Redis-based caching with fallback to in-memory cache.
Supports distributed caching and cache invalidation.
"""

import json
import hashlib
import logging
from typing import Optional, Any, Dict
from functools import wraps
from fastapi import Request, Response

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis-based caching with fallback to memory cache."""

    def __init__(self, redis_url: str = "redis://localhost:6379", ttl: int = 300):
        self.redis_url = redis_url
        self.default_ttl = ttl
        self.redis_client = None
        self.memory_cache = {}  # Fallback cache
        self._connect_redis()

    def _connect_redis(self):
        """Connect to Redis with graceful fallback."""
        try:
            import redis
            self.redis_client = redis.Redis.from_url(self.redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            logger.info("✅ Redis cache connected successfully")
        except ImportError:
            logger.warning("⚠️ Redis not available, using memory cache fallback")
            self.redis_client = None
        except Exception as e:
            logger.warning(f"⚠️ Redis connection failed ({e}), using memory cache fallback")
            self.redis_client = None

    def _generate_key(self, key_parts: list) -> str:
        """Generate cache key from parts."""
        key_string = "|".join(str(part) for part in key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if self.redis_client:
            try:
                value = self.redis_client.get(key)
                if value:
                    return json.loads(value)
            except Exception as e:
                logger.warning(f"Redis get error: {e}")

        # Fallback to memory cache
        return self.memory_cache.get(key)

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        ttl = ttl or self.default_ttl
        json_value = json.dumps(value)

        if self.redis_client:
            try:
                return bool(self.redis_client.setex(key, ttl, json_value))
            except Exception as e:
                logger.warning(f"Redis set error: {e}")

        # Fallback to memory cache (simple implementation)
        self.memory_cache[key] = value
        return True

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        success = False

        if self.redis_client:
            try:
                success = bool(self.redis_client.delete(key))
            except Exception as e:
                logger.warning(f"Redis delete error: {e}")

        # Also remove from memory cache
        if key in self.memory_cache:
            del self.memory_cache[key]
            success = True

        return success

    def clear(self) -> bool:
        """Clear all cache entries."""
        success = False

        if self.redis_client:
            try:
                success = bool(self.redis_client.flushdb())
            except Exception as e:
                logger.warning(f"Redis clear error: {e}")

        # Clear memory cache
        self.memory_cache.clear()
        success = True

        return success

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        stats = {
            'cache_type': 'redis' if self.redis_client else 'memory',
            'memory_entries': len(self.memory_cache)
        }

        if self.redis_client:
            try:
                info = self.redis_client.info()
                stats.update({
                    'redis_connected': True,
                    'redis_keys': self.redis_client.dbsize(),
                    'redis_memory_used': info.get('used_memory_human', 'unknown')
                })
            except Exception as e:
                stats['redis_error'] = str(e)

        return stats

# Global cache instance
cache = RedisCache()

def get_cache():
    """Get the global cache instance."""
    return cache

def cache_response(ttl: Optional[int] = None, key_prefix: str = ""):
    """
    Decorator to cache FastAPI endpoint responses.

    Args:
        ttl: Time to live in seconds (optional, uses default if not specified)
        key_prefix: Prefix for cache keys to allow selective clearing
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend(str(arg) for arg in args if hasattr(arg, '__dict__') or isinstance(arg, (str, int, float, bool)))

            # Add relevant kwargs
            for k, v in kwargs.items():
                if isinstance(v, (str, int, float, bool)):
                    key_parts.extend([k, str(v)])

            cache_key = cache._generate_key(key_parts)

            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result

            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)

            logger.debug(f"Cached result for {func.__name__}")
            return result

        return wrapper
    return decorator

def generate_cache_key(request: Request) -> str:
    """
    Generate cache key from FastAPI request.

    Includes method, path, query params, and relevant headers.
    """
    key_parts = [
        request.method,
        str(request.url.path),
        str(request.query_params)
    ]

    # Include important headers (but not sensitive ones)
    important_headers = ['accept', 'accept-language', 'user-agent']
    for header in important_headers:
        if header in request.headers:
            key_parts.append(f"{header}:{request.headers[header]}")

    return cache._generate_key(key_parts)

def cache_response_middleware(ttl: Optional[int] = None):
    """
    Create response caching middleware.

    Args:
        ttl: Time to live for cached responses
    """
    async def middleware(request: Request, call_next):
        # Only cache GET requests
        if request.method != "GET":
            return await call_next(request)

        cache_key = generate_cache_key(request)

        # Check cache
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.debug(f"Response cache hit for {request.url.path}")
            return Response(
                content=json.dumps(cached_response['content']),
                status_code=cached_response['status_code'],
                headers=cached_response.get('headers', {}),
                media_type='application/json'
            )

        # Execute request
        response = await call_next(request)

        # Cache successful responses
        if response.status_code == 200:
            try:
                content = response.body.decode() if hasattr(response, 'body') else ""
                cache_data = {
                    'content': json.loads(content) if content else {},
                    'status_code': response.status_code,
                    'headers': dict(response.headers)
                }
                cache.set(cache_key, cache_data, ttl)
                logger.debug(f"Cached response for {request.url.path}")
            except Exception as e:
                logger.warning(f"Failed to cache response: {e}")

        return response

    return middleware

def invalidate_cache_pattern(pattern: str) -> int:
    """
    Invalidate cache keys matching a pattern.

    Args:
        pattern: Glob pattern to match keys

    Returns:
        Number of keys deleted
    """
    deleted_count = 0

    if cache.redis_client:
        try:
            import redis
            keys = cache.redis_client.keys(pattern)
            if keys:
                deleted_count = cache.redis_client.delete(*keys)
        except Exception as e:
            logger.warning(f"Redis pattern delete error: {e}")

    # Also clear memory cache (simple implementation - clears all)
    cache.memory_cache.clear()

    return deleted_count

def warm_cache(endpoint_func, *args, **kwargs):
    """
    Pre-populate cache by calling an endpoint.

    Useful for warming up frequently accessed data.
    """
    try:
        import asyncio
        # Run the async function to populate cache
        asyncio.run(endpoint_func(*args, **kwargs))
        logger.info(f"Cache warmed for {endpoint_func.__name__}")
    except Exception as e:
        logger.warning(f"Cache warming failed: {e}")