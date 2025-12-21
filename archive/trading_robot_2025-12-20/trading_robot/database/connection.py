"""
Database Connection Utilities
==============================

Handles database connection, engine creation, and session management.
Supports SQLite (development) and PostgreSQL (production).

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

from typing import Optional, Generator
from contextlib import contextmanager
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from loguru import logger

from config.settings import config
from .models import Base


def get_db_engine() -> Engine:
    """
    Create and return database engine based on configuration.
    
    Returns:
        SQLAlchemy engine instance
        
    Raises:
        ValueError: If database URL is invalid
    """
    database_url = config.database_url
    
    # SQLite-specific configuration
    if database_url.startswith("sqlite"):
        # Use StaticPool for SQLite to handle threading
        engine = create_engine(
            database_url,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
            echo=False,  # Set to True for SQL query logging
        )
    else:
        # PostgreSQL or other databases
        engine = create_engine(
            database_url,
            pool_pre_ping=True,  # Verify connections before using
            echo=False,
        )
    
    return engine


# Global engine instance (lazy initialization)
_engine: Optional[Engine] = None
_session_factory: Optional[sessionmaker] = None


def get_session_factory() -> sessionmaker:
    """
    Get or create session factory.
    
    Returns:
        SQLAlchemy sessionmaker instance
    """
    global _session_factory
    
    if _session_factory is None:
        engine = get_db_engine()
        _session_factory = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
        )
    
    return _session_factory


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session context manager.
    
    Usage:
        with get_db_session() as session:
            # Use session here
            session.commit()
    
    Yields:
        SQLAlchemy session instance
    """
    factory = get_session_factory()
    session = factory()
    
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_database(create_tables: bool = True) -> None:
    """
    Initialize database: create tables if they don't exist.
    
    Args:
        create_tables: If True, create all tables defined in models
        
    Raises:
        Exception: If database initialization fails
    """
    try:
        engine = get_db_engine()
        
        if create_tables:
            logger.info("📊 Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Database tables created successfully")
        
        # Test connection
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        logger.info("✅ Database connection established")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def test_database_connection() -> bool:
    """
    Test database connection.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        from sqlalchemy import text
        engine = get_db_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection test passed")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {e}")
        return False
