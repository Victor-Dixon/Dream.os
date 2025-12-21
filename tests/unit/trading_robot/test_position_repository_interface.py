"""
Tests for Position Repository Interface - V2 Compliant

Tests abstract interface contract compliance and error handling.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliance: <300 lines, ≥85% coverage
"""

"""
Tests for Position Repository Interface - V2 Compliant

Tests abstract interface contract compliance and error handling.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-12-03
V2 Compliance: <300 lines, ≥85% coverage
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime
from src.trading_robot.repositories.models.position import Position
from src.trading_robot.repositories.interfaces.position_repository_interface import (
    PositionRepositoryInterface
)
from unittest.mock import AsyncMock, MagicMock

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Direct imports to avoid circular dependencies


class MockPositionRepository(PositionRepositoryInterface):
    """Mock implementation for testing interface contract."""

    def __init__(self):
        self.positions = {}
        self.position_count = 0

    async def save_position(self, position: Position) -> bool:
        """Save position to storage."""
        self.positions[position.symbol] = position
        self.position_count = len(self.positions)
        return True

    async def get_position(self, symbol: str) -> Position | None:
        """Retrieve position by symbol."""
        return self.positions.get(symbol)

    async def get_all_positions(self) -> list[Position]:
        """Get all positions."""
        return list(self.positions.values())

    async def update_position(self, position: Position) -> bool:
        """Update existing position."""
        if position.symbol in self.positions:
            self.positions[position.symbol] = position
            return True
        return False

    async def delete_position(self, symbol: str) -> bool:
        """Delete position by symbol."""
        if symbol in self.positions:
            del self.positions[symbol]
            self.position_count = len(self.positions)
            return True
        return False

    async def get_long_positions(self) -> list[Position]:
        """Get all long positions."""
        return [p for p in self.positions.values() if p.is_long()]

    async def get_short_positions(self) -> list[Position]:
        """Get all short positions."""
        return [p for p in self.positions.values() if p.is_short()]

    async def get_flat_positions(self) -> list[Position]:
        """Get all flat positions."""
        return [p for p in self.positions.values() if p.is_flat()]

    async def get_profitable_positions(self) -> list[Position]:
        """Get all profitable positions."""
        return [p for p in self.positions.values() if p.is_profitable()]

    async def get_losing_positions(self) -> list[Position]:
        """Get all losing positions."""
        return [p for p in self.positions.values() if not p.is_profitable() and not p.is_flat()]

    async def update_position_prices(self, price_updates: dict) -> bool:
        """Update current prices for positions."""
        for symbol, price in price_updates.items():
            if symbol in self.positions:
                self.positions[symbol].update_price(price)
        return True

    async def get_position_count(self) -> int:
        """Get total number of positions."""
        return self.position_count

    async def clear_all_positions(self) -> bool:
        """Clear all positions from storage."""
        self.positions.clear()
        self.position_count = 0
        return True


@pytest.fixture
def mock_repo():
    """Create mock repository instance."""
    return MockPositionRepository()


@pytest.fixture
def sample_position():
    """Create sample position for testing."""
    return Position(
        symbol="AAPL",
        quantity=100.0,
        average_price=150.0,
        current_price=155.0,
        timestamp=datetime.now()
    )


@pytest.fixture
def sample_short_position():
    """Create sample short position (losing position)."""
    return Position(
        symbol="TSLA",
        quantity=-50.0,
        average_price=200.0,
        current_price=205.0,  # Higher price = losing for short position
        timestamp=datetime.now()
    )


class TestPositionRepositoryInterface:
    """Test suite for PositionRepositoryInterface."""

    @pytest.mark.asyncio
    async def test_save_position(self, mock_repo, sample_position):
        """Test saving a position."""
        result = await mock_repo.save_position(sample_position)
        assert result is True
        assert sample_position.symbol in mock_repo.positions

    @pytest.mark.asyncio
    async def test_get_position(self, mock_repo, sample_position):
        """Test retrieving a position by symbol."""
        await mock_repo.save_position(sample_position)
        retrieved = await mock_repo.get_position("AAPL")
        assert retrieved is not None
        assert retrieved.symbol == "AAPL"
        assert retrieved.quantity == 100.0

    @pytest.mark.asyncio
    async def test_get_position_not_found(self, mock_repo):
        """Test retrieving non-existent position."""
        result = await mock_repo.get_position("NONEXISTENT")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_positions(self, mock_repo, sample_position, sample_short_position):
        """Test retrieving all positions."""
        await mock_repo.save_position(sample_position)
        await mock_repo.save_position(sample_short_position)
        all_positions = await mock_repo.get_all_positions()
        assert len(all_positions) == 2

    @pytest.mark.asyncio
    async def test_update_position(self, mock_repo, sample_position):
        """Test updating a position."""
        await mock_repo.save_position(sample_position)
        sample_position.quantity = 150.0
        result = await mock_repo.update_position(sample_position)
        assert result is True
        updated = await mock_repo.get_position("AAPL")
        assert updated.quantity == 150.0

    @pytest.mark.asyncio
    async def test_update_position_not_found(self, mock_repo, sample_position):
        """Test updating non-existent position."""
        result = await mock_repo.update_position(sample_position)
        assert result is False

    @pytest.mark.asyncio
    async def test_delete_position(self, mock_repo, sample_position):
        """Test deleting a position."""
        await mock_repo.save_position(sample_position)
        result = await mock_repo.delete_position("AAPL")
        assert result is True
        assert await mock_repo.get_position("AAPL") is None

    @pytest.mark.asyncio
    async def test_delete_position_not_found(self, mock_repo):
        """Test deleting non-existent position."""
        result = await mock_repo.delete_position("NONEXISTENT")
        assert result is False

    @pytest.mark.asyncio
    async def test_get_long_positions(self, mock_repo, sample_position, sample_short_position):
        """Test retrieving long positions."""
        await mock_repo.save_position(sample_position)
        await mock_repo.save_position(sample_short_position)
        long_positions = await mock_repo.get_long_positions()
        assert len(long_positions) == 1
        assert long_positions[0].symbol == "AAPL"

    @pytest.mark.asyncio
    async def test_get_short_positions(self, mock_repo, sample_position, sample_short_position):
        """Test retrieving short positions."""
        await mock_repo.save_position(sample_position)
        await mock_repo.save_position(sample_short_position)
        short_positions = await mock_repo.get_short_positions()
        assert len(short_positions) == 1
        assert short_positions[0].symbol == "TSLA"

    @pytest.mark.asyncio
    async def test_get_flat_positions(self, mock_repo):
        """Test retrieving flat positions."""
        # Create position with non-zero quantity first (validation requirement)
        flat_position = Position(
            symbol="FLAT",
            quantity=1.0,  # Start with non-zero
            average_price=100.0,
            current_price=100.0,
            timestamp=datetime.now()
        )
        # Set to flat after creation (bypasses __post_init__ validation)
        flat_position.quantity = 0.0
        await mock_repo.save_position(flat_position)
        flat_positions = await mock_repo.get_flat_positions()
        assert len(flat_positions) == 1

    @pytest.mark.asyncio
    async def test_get_profitable_positions(self, mock_repo, sample_position):
        """Test retrieving profitable positions."""
        await mock_repo.save_position(sample_position)
        profitable = await mock_repo.get_profitable_positions()
        assert len(profitable) == 1
        assert profitable[0].is_profitable()

    @pytest.mark.asyncio
    async def test_get_losing_positions(self, mock_repo, sample_short_position):
        """Test retrieving losing positions."""
        await mock_repo.save_position(sample_short_position)
        losing = await mock_repo.get_losing_positions()
        assert len(losing) == 1
        assert not losing[0].is_profitable()

    @pytest.mark.asyncio
    async def test_update_position_prices(self, mock_repo, sample_position):
        """Test updating position prices."""
        await mock_repo.save_position(sample_position)
        price_updates = {"AAPL": 160.0}
        result = await mock_repo.update_position_prices(price_updates)
        assert result is True
        updated = await mock_repo.get_position("AAPL")
        assert updated.current_price == 160.0

    @pytest.mark.asyncio
    async def test_get_position_count(self, mock_repo, sample_position, sample_short_position):
        """Test getting position count."""
        assert await mock_repo.get_position_count() == 0
        await mock_repo.save_position(sample_position)
        assert await mock_repo.get_position_count() == 1
        await mock_repo.save_position(sample_short_position)
        assert await mock_repo.get_position_count() == 2

    @pytest.mark.asyncio
    async def test_clear_all_positions(self, mock_repo, sample_position, sample_short_position):
        """Test clearing all positions."""
        await mock_repo.save_position(sample_position)
        await mock_repo.save_position(sample_short_position)
        result = await mock_repo.clear_all_positions()
        assert result is True
        assert await mock_repo.get_position_count() == 0
        assert len(await mock_repo.get_all_positions()) == 0
