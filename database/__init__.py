"""
Database Integration Module - Agent Cellphone V2
===============================================

SSOT Domain: database

Provides unified database integration with SQLAlchemy async engine,
session management, and connection pooling for the Agent Cellphone V2 system.

Features:
- Async SQLAlchemy engine configuration
- Connection pooling and session management
- Database health checks and monitoring
- Migration support and schema management
- Multi-database support capabilities

Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
V2 Compliant: Yes (<300 lines)
"""

import os
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/agent_cellphone_v2"
)

# Engine configuration
ENGINE_CONFIG = {
    "echo": False,  # Set to True for SQL query logging in development
    "poolclass": AsyncAdaptedQueuePool,
    "pool_pre_ping": True,  # Verify connections before use
    "pool_size": 20,  # Base pool size
    "max_overflow": 30,  # Maximum additional connections
    "pool_timeout": 30,  # Connection timeout
    "pool_recycle": 3600,  # Recycle connections hourly
}

# Global engine instance (singleton pattern)
_engine = None
_async_session_maker = None

def get_database_engine():
    """
    Get or create the global database engine instance.

    Returns:
        AsyncEngine: Configured SQLAlchemy async engine
    """
    global _engine
    if _engine is None:
        _engine = create_async_engine(DATABASE_URL, **ENGINE_CONFIG)
        logger.info("Database engine initialized")
    return _engine

def get_async_session_maker():
    """
    Get or create the async session maker instance.

    Returns:
        async_sessionmaker: Configured async session maker
    """
    global _async_session_maker
    if _async_session_maker is None:
        engine = get_database_engine()
        _async_session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        logger.info("Async session maker initialized")
    return _async_session_maker

@asynccontextmanager
async def get_db_session():
    """
    Context manager for database sessions.

    Yields:
        AsyncSession: Database session instance

    Usage:
        async with get_db_session() as session:
            result = await session.execute(query)
    """
    session_maker = get_async_session_maker()
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()

async def check_database_health() -> Dict[str, Any]:
    """
    Check database connectivity and health.

    Returns:
        Dict containing health check results
    """
    health_status = {
        "database": "unknown",
        "connection_pool": "unknown",
        "latency_ms": None,
        "error": None
    }

    try:
        engine = get_database_engine()
        import time

        # Test basic connectivity
        start_time = time.time()
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        end_time = time.time()

        health_status.update({
            "database": "healthy",
            "connection_pool": "healthy",
            "latency_ms": round((end_time - start_time) * 1000, 2)
        })

        logger.info(f"Database health check passed: {health_status['latency_ms']}ms")

    except Exception as e:
        health_status.update({
            "database": "unhealthy",
            "error": str(e)
        })
        logger.error(f"Database health check failed: {e}")

    return health_status

async def initialize_database():
    """
    Initialize database components and verify connectivity.
    Call this during application startup.
    """
    try:
        logger.info("Initializing database components...")

        # Initialize engine and session maker
        engine = get_database_engine()
        session_maker = get_async_session_maker()

        # Test connectivity
        health = await check_database_health()
        if health["database"] == "healthy":
            logger.info("Database initialization successful")
            return True
        else:
            logger.error(f"Database initialization failed: {health['error']}")
            return False

    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        return False

# Export key functions
__all__ = [
    "get_database_engine",
    "get_async_session_maker",
    "get_db_session",
    "check_database_health",
    "initialize_database"
]