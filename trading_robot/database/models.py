"""
Database Models
===============

SQLAlchemy ORM models for trading robot data persistence.

Tables:
- trades: Trade execution records
- positions: Current portfolio positions
- orders: Order requests and status
- trading_sessions: Trading session metadata

Author: Agent-3 (Infrastructure & DevOps Specialist)
Created: 2025-12-20
V2 Compliant: Yes (<400 lines, type hints, documented)
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Boolean, Text,
    Numeric, Index, ForeignKey, Enum as SQLEnum
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class OrderSide(str, enum.Enum):
    """Order side enumeration."""
    BUY = "buy"
    SELL = "sell"


class OrderType(str, enum.Enum):
    """Order type enumeration."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"
    TRAILING_STOP = "trailing_stop"


class OrderStatus(str, enum.Enum):
    """Order status enumeration."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Trade(Base):
    """Trade execution record."""
    __tablename__ = "trades"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Trade identification
    broker_order_id = Column(String(100), unique=True, index=True, nullable=True)
    symbol = Column(String(10), nullable=False, index=True)
    side = Column(SQLEnum(OrderSide), nullable=False)
    
    # Trade execution details
    quantity = Column(Numeric(12, 4), nullable=False)
    price = Column(Numeric(12, 4), nullable=False)
    commission = Column(Numeric(10, 4), default=0.0)
    total_value = Column(Numeric(12, 2), nullable=False)
    
    # Timing
    executed_at = Column(DateTime, nullable=False, index=True, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Order relationship
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    
    # Additional metadata
    strategy_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="trades")
    
    # Indexes
    __table_args__ = (
        Index("idx_trades_symbol_executed", "symbol", "executed_at"),
        Index("idx_trades_strategy_executed", "strategy_name", "executed_at"),
    )


class Position(Base):
    """Current portfolio position."""
    __tablename__ = "positions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Position identification
    symbol = Column(String(10), unique=True, nullable=False, index=True)
    
    # Position details
    quantity = Column(Numeric(12, 4), nullable=False)
    avg_cost = Column(Numeric(12, 4), nullable=False)
    current_price = Column(Numeric(12, 4), nullable=True)
    
    # Value calculations
    cost_basis = Column(Numeric(12, 2), nullable=False)
    market_value = Column(Numeric(12, 2), nullable=True)
    unrealized_pnl = Column(Numeric(12, 2), nullable=True)
    unrealized_pnl_pct = Column(Numeric(8, 4), nullable=True)
    
    # Timing
    opened_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Status
    is_open = Column(Boolean, default=True, index=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Additional metadata
    strategy_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)


class Order(Base):
    """Order request and status tracking."""
    __tablename__ = "orders"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Order identification
    broker_order_id = Column(String(100), unique=True, index=True, nullable=True)
    symbol = Column(String(10), nullable=False, index=True)
    side = Column(SQLEnum(OrderSide), nullable=False)
    order_type = Column(SQLEnum(OrderType), nullable=False)
    
    # Order details
    quantity = Column(Numeric(12, 4), nullable=False)
    limit_price = Column(Numeric(12, 4), nullable=True)
    stop_price = Column(Numeric(12, 4), nullable=True)
    time_in_force = Column(String(20), default="day")
    
    # Status tracking
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True)
    filled_quantity = Column(Numeric(12, 4), default=0.0)
    avg_fill_price = Column(Numeric(12, 4), nullable=True)
    
    # Timing
    submitted_at = Column(DateTime, nullable=True)
    filled_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional metadata
    strategy_name = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    trades = relationship("Trade", back_populates="order", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index("idx_orders_symbol_status", "symbol", "status"),
        Index("idx_orders_status_created", "status", "created_at"),
    )


class TradingSession(Base):
    """Trading session metadata and statistics."""
    __tablename__ = "trading_sessions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Session identification
    session_name = Column(String(100), nullable=True)
    started_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    ended_at = Column(DateTime, nullable=True)
    
    # Session statistics
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)
    losing_trades = Column(Integer, default=0)
    
    # Performance metrics
    total_pnl = Column(Numeric(12, 2), default=0.0)
    total_commission = Column(Numeric(10, 2), default=0.0)
    win_rate = Column(Numeric(5, 2), nullable=True)
    
    # Portfolio metrics
    starting_balance = Column(Numeric(12, 2), nullable=True)
    ending_balance = Column(Numeric(12, 2), nullable=True)
    max_drawdown = Column(Numeric(8, 4), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, index=True)
    
    # Additional metadata
    broker = Column(String(50), nullable=True)
    trading_mode = Column(String(20), nullable=True)  # paper, live
    notes = Column(Text, nullable=True)
