#!/usr/bin/env python3
"""
Redis Cache Manager - Phase 5 Performance Optimization
======================================================

Enterprise Redis caching layer with automatic serialization and TTL management.
Provides high-performance data caching with fallback strategies.

V2 Compliance: <300 lines
Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import time
import json
import pickle
from typing import Optional, Any, Dict, Union
import redis
import logging

logger = logging.getLogger(__name__)

class RedisCache:
    """
    Enterprise Redis Cache Manager

    Provides high-performance caching with automatic serialization,
    TTL management, and fallback strategies for cache misses.
    """

    def __init__(self):
        """Initialize Redis cache with connection pooling."""
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", "6379"))
        self.db = int(os.getenv("REDIS_DB", "0"))
        self.password = os.getenv("REDIS_PASSWORD")

        # Connection pool for better performance
        self.redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=False,  # Keep as bytes for pickle support
            socket_connect_timeout=5,
            socket_timeout=5,
            retry_on_timeout=True,
            max_connections=20
        )

        # Test connection
        try:
            self.redis_client.ping()
            logger.info(f"✅ Redis cache connected to {self.host}:{self.port}")
        except redis.ConnectionError as e:
            logger.error(f"❌ Redis connection failed: {e}")
            self.redis_client = None

    def _serialize_value(self, value: Any) -> bytes:
        """
        Serialize value for Redis storage.

        Args:
            value: Value to serialize

        Returns:
            Serialized bytes
        """
        if isinstance(value, (str, int, float, bool)):
            return json.dumps(value).encode('utf-8')
        elif isinstance(value, (dict, list)):
            return json.dumps(value).encode('utf-8')
        else:
            # Use pickle for complex objects
            return pickle.dumps(value)

    def _deserialize_value(self, value: bytes) -> Any:
        """
        Deserialize value from Redis storage.

        Args:
            value: Serialized bytes

        Returns:
            Deserialized value
        """
        try:
            # Try JSON first
            return json.loads(value.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fall back to pickle
            try:
                return pickle.loads(value)
            except Exception:
                # Return raw bytes if all else fails
                return value

    def set(self, key: str, value: Any, expire: int = 3600,
            nx: bool = False, xx: bool = False) -> bool:
        """
        Set cache value with optional expiration.

        Args:
            key: Cache key
            value: Value to cache
            expire: Expiration time in seconds (default: 1 hour)
            nx: Only set if key doesn't exist
            xx: Only set if key exists

        Returns:
            True if successful
        """
        if not self.redis_client:
            return False

        try:
            serialized_value = self._serialize_value(value)

            if nx:
                return bool(self.redis_client.set(key, serialized_value, ex=expire, nx=True))
            elif xx:
                return bool(self.redis_client.set(key, serialized_value, ex=expire, xx=True))
            else:
                return bool(self.redis_client.setex(key, expire, serialized_value))

        except Exception as e:
            logger.error(f"Cache set failed for key '{key}': {e}")
            return False

    def get(self, key: str) -> Optional[Any]:
        """
        Get cached value.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found
        """
        if not self.redis_client:
            return None

        try:
            value = self.redis_client.get(key)
            if value is None:
                return None

            return self._deserialize_value(value)

        except Exception as e:
            logger.error(f"Cache get failed for key '{key}': {e}")
            return None

    def delete(self, *keys: str) -> int:
        """
        Delete cache keys.

        Args:
            *keys: Cache keys to delete

        Returns:
            Number of keys deleted
        """
        if not self.redis_client:
            return 0

        try:
            return self.redis_client.delete(*keys)
        except Exception as e:
            logger.error(f"Cache delete failed: {e}")
            return 0

    def exists(self, key: str) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists
        """
        if not self.redis_client:
            return False

        try:
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Cache exists check failed for key '{key}': {e}")
            return False

    def expire(self, key: str, time: int) -> bool:
        """
        Set expiration time for key.

        Args:
            key: Cache key
            time: Expiration time in seconds

        Returns:
            True if successful
        """
        if not self.redis_client:
            return False

        try:
            return bool(self.redis_client.expire(key, time))
        except Exception as e:
            logger.error(f"Cache expire failed for key '{key}': {e}")
            return False

    def ttl(self, key: str) -> int:
        """
        Get time-to-live for key.

        Args:
            key: Cache key

        Returns:
            TTL in seconds (-2 if key doesn't exist, -1 if no expiration)
        """
        if not self.redis_client:
            return -2

        try:
            return self.redis_client.ttl(key)
        except Exception as e:
            logger.error(f"Cache TTL check failed for key '{key}': {e}")
            return -2

    def incr(self, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment integer value in cache.

        Args:
            key: Cache key
            amount: Amount to increment by

        Returns:
            New value after increment or None if failed
        """
        if not self.redis_client:
            return None

        try:
            return self.redis_client.incr(key, amount)
        except Exception as e:
            logger.error(f"Cache increment failed for key '{key}': {e}")
            return None

    def get_or_set(self, key: str, default_func, expire: int = 3600) -> Any:
        """
        Get cached value or set it using default function.

        Args:
            key: Cache key
            default_func: Function to call if cache miss
            expire: Expiration time in seconds

        Returns:
            Cached or newly computed value
        """
        value = self.get(key)
        if value is not None:
            return value

        # Cache miss - compute and cache
        value = default_func()
        if value is not None:
            self.set(key, value, expire)

        return value

    def clear_pattern(self, pattern: str) -> int:
        """
        Clear all keys matching pattern.

        Args:
            pattern: Redis pattern (e.g., "user:*")

        Returns:
            Number of keys deleted
        """
        if not self.redis_client:
            return 0

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            logger.error(f"Cache clear pattern failed for '{pattern}': {e}")
            return 0

    def health_check(self) -> Dict[str, Any]:
        """
        Perform Redis health check.

        Returns:
            Health status dictionary
        """
        if not self.redis_client:
            return {"status": "unhealthy", "error": "No Redis client"}

        try:
            start_time = time.time()
            self.redis_client.ping()
            latency = round((time.time() - start_time) * 1000, 2)  # ms

            # Get basic stats
            info = self.redis_client.info()
            memory_used = info.get("used_memory_human", "unknown")
            connected_clients = info.get("connected_clients", 0)

            return {
                "status": "healthy",
                "latency_ms": latency,
                "memory_used": memory_used,
                "connected_clients": connected_clients,
                "timestamp": time.time()
            }

        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get Redis statistics.

        Returns:
            Redis statistics dictionary
        """
        if not self.redis_client:
            return {"error": "No Redis client"}

        try:
            info = self.redis_client.info()
            return {
                "total_connections_received": info.get("total_connections_received", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "used_memory_human": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "expired_keys": info.get("expired_keys", 0),
                "evicted_keys": info.get("evicted_keys", 0),
            }
        except Exception as e:
            return {"error": str(e)}

# Global Redis cache instance
redis_cache = RedisCache()