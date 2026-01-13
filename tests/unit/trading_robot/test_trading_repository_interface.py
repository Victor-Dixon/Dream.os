"""
Tests for Trading Repository Interface - V2 Compliant

Tests abstract interface contract compliance and error handling.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliance: <300 lines, ≥85% coverage
"""

"""
Tests for Trading Repository Interface - V2 Compliant

Tests abstract interface contract compliance and error handling.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliance: <300 lines, ≥85% coverage
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Direct imports to avoid circular dependencies
from src.trading_robot.repositories.interfaces.trading_repository_interface import (
    TradingRepositoryInterface
)
from src.trading_robot.repositories.models.trade import Trade


class MockTradingRepository(TradingRepositoryInterface):
    """Mock implementation for testing interface contract."""

    def __init__(self):
        self.trades = {}
        self.trade_count = 0

    async def save_trade(self, trade: Trade) -> bool:
        """Save a trade to storage."""
        self.trades[trade.id] = trade
        self.trade_count = len(self.trades)
        return True

    async def get_trade(self, trade_id: str) -> Trade | None:
        """Retrieve a trade by ID."""
        return self.trades.get(trade_id)

    async def get_trades_by_symbol(self, symbol: str, limit: int = 100) -> list[Trade]:
        """Get trades for a specific symbol."""
        symbol_trades = [t for t in self.trades.values() if t.symbol == symbol]
        return sorted(symbol_trades, key=lambda t: t.timestamp, reverse=True)[:limit]

    async def get_all_trades(self, limit: int = 1000) -> list[Trade]:
        """Get all trades."""
        all_trades = list(self.trades.values())
        return sorted(all_trades, key=lambda t: t.timestamp, reverse=True)[:limit]

    async def update_trade_status(self, trade_id: str, status: str) -> bool:
        """Update trade status."""
        if trade_id in self.trades:
            self.trades[trade_id].status = status
            return True
        return False

    async def delete_trade(self, trade_id: str) -> bool:
        """Delete a trade."""
        if trade_id in self.trades:
            del self.trades[trade_id]
            self.trade_count = len(self.trades)
            return True
        return False

    async def get_trades_by_status(self, status: str, limit: int = 100) -> list[Trade]:
        """Get trades by status."""
        status_trades = [t for t in self.trades.values() if t.status == status]
        return sorted(status_trades, key=lambda t: t.timestamp, reverse=True)[:limit]

    async def get_trades_by_date_range(self, start_date, end_date, limit: int = 100) -> list[Trade]:
        """Get trades within date range."""
        range_trades = [
            t for t in self.trades.values()
            if start_date <= t.timestamp <= end_date
        ]
        return sorted(range_trades, key=lambda t: t.timestamp, reverse=True)[:limit]

    async def get_trade_count(self) -> int:
        """Get total number of trades."""
        return self.trade_count

    async def clear_all_trades(self) -> bool:
        """Clear all trades from storage."""
        self.trades.clear()
        self.trade_count = 0
        return True


@pytest.fixture
def mock_repo():
    """Create mock repository instance."""
    return MockTradingRepository()


@pytest.fixture
def sample_trade():
    """Create sample trade for testing."""
    return Trade(
        id="trade_001",
        symbol="AAPL",
        side="buy",
        quantity=100.0,
        price=150.0,
        timestamp=datetime.now(),
        status="pending"
    )


@pytest.fixture
def sample_executed_trade():
    """Create sample executed trade."""
    return Trade(
        id="trade_002",
        symbol="GOOGL",
        side="sell",
        quantity=50.0,
        price=2500.0,
        timestamp=datetime.now() - timedelta(hours=1),
        status="executed"
    )


class TestTradingRepositoryInterface:
    """Test suite for TradingRepositoryInterface."""

    @pytest.mark.asyncio
    async def test_save_trade(self, mock_repo, sample_trade):
        """Test saving a trade."""
        result = await mock_repo.save_trade(sample_trade)
        assert result is True
        assert sample_trade.id in mock_repo.trades

    @pytest.mark.asyncio
    async def test_get_trade(self, mock_repo, sample_trade):
        """Test retrieving a trade by ID."""
        await mock_repo.save_trade(sample_trade)
        retrieved = await mock_repo.get_trade("trade_001")
        assert retrieved is not None
        assert retrieved.id == "trade_001"
        assert retrieved.symbol == "AAPL"

    @pytest.mark.asyncio
    async def test_get_trade_not_found(self, mock_repo):
        """Test retrieving non-existent trade."""
        result = await mock_repo.get_trade("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_trades_by_symbol(self, mock_repo, sample_trade, sample_executed_trade):
        """Test retrieving trades by symbol."""
        await mock_repo.save_trade(sample_trade)
        await mock_repo.save_trade(sample_executed_trade)
        aapl_trades = await mock_repo.get_trades_by_symbol("AAPL")
        assert len(aapl_trades) == 1
        assert aapl_trades[0].symbol == "AAPL"

    @pytest.mark.asyncio
    async def test_get_trades_by_symbol_limit(self, mock_repo):
        """Test symbol trades with limit."""
        for i in range(150):
            trade = Trade(
                id=f"trade_{i}",
                symbol="AAPL",
                side="buy",
                quantity=10.0,
                price=150.0,
                timestamp=datetime.now() - timedelta(minutes=i)
            )
            await mock_repo.save_trade(trade)
        trades = await mock_repo.get_trades_by_symbol("AAPL", limit=100)
        assert len(trades) == 100

    @pytest.mark.asyncio
    async def test_get_all_trades(self, mock_repo, sample_trade, sample_executed_trade):
        """Test retrieving all trades."""
        await mock_repo.save_trade(sample_trade)
        await mock_repo.save_trade(sample_executed_trade)
        all_trades = await mock_repo.get_all_trades()
        assert len(all_trades) == 2

    @pytest.mark.asyncio
    async def test_get_all_trades_limit(self, mock_repo):
        """Test all trades with limit."""
        for i in range(1500):
            trade = Trade(
                id=f"trade_{i}",
                symbol="AAPL",
                side="buy",
                quantity=10.0,
                price=150.0,
                timestamp=datetime.now() - timedelta(minutes=i)
            )
            await mock_repo.save_trade(trade)
        trades = await mock_repo.get_all_trades(limit=1000)
        assert len(trades) == 1000

    @pytest.mark.asyncio
    async def test_update_trade_status(self, mock_repo, sample_trade):
        """Test updating trade status."""
        await mock_repo.save_trade(sample_trade)
        result = await mock_repo.update_trade_status("trade_001", "executed")
        assert result is True
        updated = await mock_repo.get_trade("trade_001")
        assert updated.status == "executed"

    @pytest.mark.asyncio
    async def test_update_trade_status_not_found(self, mock_repo):
        """Test updating non-existent trade status."""
        result = await mock_repo.update_trade_status("nonexistent", "executed")
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_trade(self, mock_repo, sample_trade):
        """Test deleting a trade."""
        await mock_repo.save_trade(sample_trade)
        result = await mock_repo.delete_trade("trade_001")
        assert result is True
        assert await mock_repo.get_trade("trade_001") is None

    @pytest.mark.asyncio
    async def test_delete_trade_not_found(self, mock_repo):
        """Test deleting non-existent trade."""
        result = await mock_repo.delete_trade("nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_get_trades_by_status(self, mock_repo, sample_trade, sample_executed_trade):
        """Test retrieving trades by status."""
        await mock_repo.save_trade(sample_trade)
        await mock_repo.save_trade(sample_executed_trade)
        pending_trades = await mock_repo.get_trades_by_status("pending")
        assert len(pending_trades) == 1
        assert pending_trades[0].status == "pending"
        executed_trades = await mock_repo.get_trades_by_status("executed")
        assert len(executed_trades) == 1
        assert executed_trades[0].status == "executed"

    @pytest.mark.asyncio
    async def test_get_trades_by_date_range(self, mock_repo):
        """Test retrieving trades by date range."""
        now = datetime.now()
        trade1 = Trade(
            id="trade_1",
            symbol="AAPL",
            side="buy",
            quantity=100.0,
            price=150.0,
            timestamp=now - timedelta(days=2)
        )
        trade2 = Trade(
            id="trade_2",
            symbol="AAPL",
            side="buy",
            quantity=100.0,
            price=150.0,
            timestamp=now - timedelta(days=1)
        )
        trade3 = Trade(
            id="trade_3",
            symbol="AAPL",
            side="buy",
            quantity=100.0,
            price=150.0,
            timestamp=now
        )
        await mock_repo.save_trade(trade1)
        await mock_repo.save_trade(trade2)
        await mock_repo.save_trade(trade3)
        start_date = now - timedelta(days=1.5)
        end_date = now
        range_trades = await mock_repo.get_trades_by_date_range(start_date, end_date)
        assert len(range_trades) == 2

    @pytest.mark.asyncio
    async def test_get_trade_count(self, mock_repo, sample_trade, sample_executed_trade):
        """Test getting trade count."""
        assert await mock_repo.get_trade_count() == 0
        await mock_repo.save_trade(sample_trade)
        assert await mock_repo.get_trade_count() == 1
        await mock_repo.save_trade(sample_executed_trade)
        assert await mock_repo.get_trade_count() == 2

    @pytest.mark.asyncio
    async def test_clear_all_trades(self, mock_repo, sample_trade, sample_executed_trade):
        """Test clearing all trades."""
        await mock_repo.save_trade(sample_trade)
        await mock_repo.save_trade(sample_executed_trade)
        result = await mock_repo.clear_all_trades()
        assert result is True
        assert await mock_repo.get_trade_count() == 0
        assert len(await mock_repo.get_all_trades()) == 0

