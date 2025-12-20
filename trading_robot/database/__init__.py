"""
Trading Robot Database Module
=============================

Database models, initialization, and utilities for the trading robot.
Supports both SQLite (development) and PostgreSQL (production).

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
"""

from .models import Base, Trade, Position, Order, TradingSession
from .connection import get_db_engine, get_db_session, init_database
from .backup import backup_database, restore_database

__all__ = [
    "Base",
    "Trade",
    "Position",
    "Order",
    "TradingSession",
    "get_db_engine",
    "get_db_session",
    "init_database",
    "backup_database",
    "restore_database",
]
