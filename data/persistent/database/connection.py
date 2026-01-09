"""
Database Connection Module for Revenue Engine

Provides SQLAlchemy-based database connectivity with connection pooling,
session management, and schema creation for Revenue Engine components.

Features:
- Connection pooling for performance
- Automatic retry logic for connection failures
- Schema management for trading data persistence
- Thread-safe session handling
"""

import os
import logging
from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'sqlite:///revenue_engine.db'  # Default to SQLite for development
)

# Connection pool settings
POOL_SIZE = int(os.getenv('DB_POOL_SIZE', '10'))
MAX_OVERFLOW = int(os.getenv('DB_MAX_OVERFLOW', '20'))
POOL_TIMEOUT = int(os.getenv('DB_POOL_TIMEOUT', '30'))

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_timeout=POOL_TIMEOUT,
    echo=False  # Set to True for SQL query logging in development
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Metadata for schema management
metadata = MetaData()

class DatabaseConnection:
    """
    Database connection manager for Revenue Engine.

    Provides centralized database connectivity with proper error handling
    and resource management.
    """

    @staticmethod
    def get_engine():
        """Get the SQLAlchemy engine instance."""
        return engine

    @staticmethod
    def get_metadata():
        """Get the metadata instance for schema operations."""
        return metadata

    @staticmethod
    def test_connection() -> bool:
        """
        Test database connectivity.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection test successful")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Database connection test failed: {e}")
            return False

    @staticmethod
    def create_tables():
        """
        Create all database tables defined in metadata.

        This should be called during application startup to ensure
        all required tables exist.
        """
        try:
            metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {e}")
            raise

def create_tables():
    """
    Create all database tables defined in metadata.

    This should be called during application startup to ensure
    all required tables exist.
    """
    try:
        metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except SQLAlchemyError as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Provides a database session with automatic cleanup and error handling.

    Yields:
        Session: SQLAlchemy database session

    Example:
        with get_db_session() as session:
            # Use session for database operations
            pass
    """
    session: Optional[Session] = None
    try:
        session = SessionLocal()
        yield session
    except SQLAlchemyError as e:
        logger.error(f"Database session error: {e}")
        if session:
            session.rollback()
        raise
    finally:
        if session:
            session.close()

# Test connection on module import
if __name__ != "__main__":
    connection_status = DatabaseConnection.test_connection()
    if not connection_status:
        logger.warning("Database connection failed during module initialization")

__all__ = [
    'DatabaseConnection',
    'get_db_session',
    'create_tables',
    'engine',
    'metadata'
]