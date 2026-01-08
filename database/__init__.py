"""
Database Integration Module for Revenue Engine

This module provides database connectivity and session management for the Revenue Engine,
enabling persistent storage of trading data, analytics, and system state.

Part of Revenue Engine Phase 3: Advanced Trading Algorithms & Risk Management
"""

from .connection import DatabaseConnection, get_db_session, create_tables

__all__ = [
    'DatabaseConnection',
    'get_db_session',
    'create_tables'
]

__version__ = "1.0.0"
__author__ = "Agent-1 (Integration & Core Systems Specialist)"