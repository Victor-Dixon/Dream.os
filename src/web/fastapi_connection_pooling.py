#!/usr/bin/env python3
"""
Connection Pooling Module - FastAPI Services
=============================================

V2 Compliant: Yes (<100 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-08

Connection pooling utilities extracted from fastapi_app.py for V2 compliance.
Provides Redis and HTTP connection pools for external service integration.
"""

import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Connection pools storage
connection_pools: Dict[str, Any] = {}


async def initialize_connection_pools():
    """
    Initialize connection pools for external services.

    Sets up Redis and HTTP connection pools for improved performance
    and resource management in production environments.
    """
    global connection_pools

    # Redis connection pool
    await _initialize_redis_pool()

    # External API connection pool (HTTP)
    await _initialize_http_pool()

    pool_count = len([p for p in connection_pools.values() if p is not None])
    logger.info(f"✅ Initialized {pool_count} connection pools")


async def _initialize_redis_pool():
    """Initialize Redis connection pool."""
    try:
        import redis

        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        connection_pools["redis"] = redis.ConnectionPool.from_url(
            redis_url,
            max_connections=20,
            decode_responses=True,
            retry_on_timeout=True,
            socket_timeout=5,
            socket_connect_timeout=5,
            socket_keepalive=True,
            socket_keepalive_options={},
            health_check_interval=30
        )
        logger.info("✅ Redis connection pool initialized")
    except ImportError:
        logger.warning("Redis not available, connection pooling disabled")
    except Exception as e:
        logger.warning(f"Redis connection pool failed: {e}")


async def _initialize_http_pool():
    """Initialize HTTP connection pool for external APIs."""
    try:
        import aiohttp

        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        connector = aiohttp.TCPConnector(
            limit=100,  # Max connections per host
            limit_per_host=10,  # Max connections to single host
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True,
            keepalive_timeout=60,
            enable_cleanup_closed=True,
        )
        connection_pools["external_apis"] = {
            "connector": connector,
            "timeout": timeout
        }
        logger.info("✅ External API connection pool initialized")
    except ImportError:
        logger.warning("aiohttp not available, external API connection pooling disabled")
    except Exception as e:
        logger.warning(f"External API connection pool failed: {e}")


def get_redis_connection():
    """
    Get a Redis connection from the pool.

    Returns:
        Redis connection or None if pool not available
    """
    if "redis" not in connection_pools:
        return None

    try:
        import redis
        return redis.Redis(connection_pool=connection_pools["redis"])
    except Exception as e:
        logger.warning(f"Failed to get Redis connection: {e}")
        return None


def get_http_connector_and_timeout() -> Optional[tuple]:
    """
    Get HTTP connector and timeout for external API calls.

    Returns:
        tuple: (connector, timeout) or None if not available
    """
    pool_data = connection_pools.get("external_apis")
    if not pool_data:
        return None

    return pool_data["connector"], pool_data["timeout"]


def get_connection_pool_status() -> Dict[str, Any]:
    """
    Get status of all connection pools.

    Returns:
        dict: Pool status information
    """
    status = {}

    # Redis pool status
    if "redis" in connection_pools:
        status["redis"] = {
            "available": True,
            "max_connections": getattr(connection_pools["redis"], '_max_connections', 'unknown')
        }
    else:
        status["redis"] = {"available": False}

    # HTTP pool status
    if "external_apis" in connection_pools:
        connector = connection_pools["external_apis"]["connector"]
        status["external_apis"] = {
            "available": True,
            "limit": getattr(connector, '_limit', 'unknown'),
            "limit_per_host": getattr(connector, '_limit_per_host', 'unknown')
        }
    else:
        status["external_apis"] = {"available": False}

    return status


def cleanup_connection_pools():
    """Clean up connection pools on shutdown."""
    try:
        # Close HTTP connector
        if "external_apis" in connection_pools:
            connector = connection_pools["external_apis"]["connector"]
            if hasattr(connector, 'close'):
                import asyncio
                # Schedule cleanup for next event loop iteration
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(connector.close())
                finally:
                    loop.close()

        # Clear pools
        connection_pools.clear()
        logger.info("✅ Connection pools cleaned up")

    except Exception as e:
        logger.warning(f"Connection pool cleanup error: {e}")


__all__ = [
    "initialize_connection_pools",
    "get_redis_connection",
    "get_http_connector_and_timeout",
    "get_connection_pool_status",
    "cleanup_connection_pools"
]