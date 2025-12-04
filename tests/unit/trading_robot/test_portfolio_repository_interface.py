"""
Tests for Portfolio Repository Interface
========================================

Tests for src/trading_robot/repositories/interfaces/portfolio_repository_interface.py.

V2 Compliance: < 300 lines, ≥85% coverage.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

"""
Tests for Portfolio Repository Interface
========================================

Tests for src/trading_robot/repositories/interfaces/portfolio_repository_interface.py.

V2 Compliance: < 300 lines, ≥85% coverage.
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, AsyncMock

# Import directly from source files to avoid dependency chain issues
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Direct imports
from src.trading_robot.repositories.interfaces.portfolio_repository_interface import (
    PortfolioRepositoryInterface
)

# Import models directly
from src.trading_robot.repositories.models.portfolio import Portfolio
from src.trading_robot.repositories.models.position import Position


class MockPortfolioRepository(PortfolioRepositoryInterface):
    """Mock implementation of PortfolioRepositoryInterface for testing."""
    
    def __init__(self):
        self._portfolios: dict[str, Portfolio] = {}
    
    async def save_portfolio(self, portfolio: Portfolio) -> bool:
        """Save portfolio."""
        if not portfolio or not portfolio.id:
            raise ValueError("Portfolio is invalid or missing required fields")
        self._portfolios[portfolio.id] = portfolio
        return True
    
    async def get_portfolio(self, portfolio_id: str):
        """Get portfolio by ID."""
        if not portfolio_id or not portfolio_id.strip():
            raise ValueError("Portfolio ID cannot be empty")
        return self._portfolios.get(portfolio_id)
    
    async def get_all_portfolios(self) -> list[Portfolio]:
        """Get all portfolios."""
        return list(self._portfolios.values())
    
    async def update_portfolio(self, portfolio: Portfolio) -> bool:
        """Update portfolio."""
        if not portfolio or not portfolio.id:
            raise ValueError("Portfolio is invalid or missing required fields")
        if portfolio.id not in self._portfolios:
            raise RuntimeError("Portfolio not found")
        self._portfolios[portfolio.id] = portfolio
        return True
    
    async def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete portfolio."""
        if not portfolio_id or not portfolio_id.strip():
            raise ValueError("Portfolio ID cannot be empty")
        if portfolio_id in self._portfolios:
            del self._portfolios[portfolio_id]
            return True
        return False
    
    async def get_portfolio_by_name(self, name: str):
        """Get portfolio by name."""
        if not name or not name.strip():
            raise ValueError("Portfolio name cannot be empty")
        for portfolio in self._portfolios.values():
            if portfolio.name == name:
                return portfolio
        return None
    
    async def get_portfolio_count(self) -> int:
        """Get portfolio count."""
        return len(self._portfolios)
    
    async def clear_all_portfolios(self) -> bool:
        """Clear all portfolios."""
        self._portfolios.clear()
        return True


@pytest.fixture
def sample_portfolio():
    """Create sample portfolio for testing."""
    return Portfolio(
        id="portfolio-1",
        name="Test Portfolio",
        cash_balance=1000.0,
        total_value=1000.0
    )


@pytest.fixture
def sample_portfolio_with_position():
    """Create sample portfolio with position."""
    portfolio = Portfolio(
        id="portfolio-2",
        name="Portfolio with Position",
        cash_balance=500.0
    )
    position = Position(
        symbol="AAPL",
        quantity=10,
        average_price=150.0,
        current_price=155.0
    )
    portfolio.add_position(position)
    return portfolio


class TestPortfolioRepositoryInterface:
    """Test suite for PortfolioRepositoryInterface."""
    
    @pytest.mark.asyncio
    async def test_save_portfolio_success(self, sample_portfolio):
        """Test saving portfolio successfully."""
        repo = MockPortfolioRepository()
        result = await repo.save_portfolio(sample_portfolio)
        assert result is True
        assert await repo.get_portfolio_count() == 1
    
    @pytest.mark.asyncio
    async def test_save_portfolio_invalid_raises_error(self):
        """Test that invalid portfolio raises ValueError."""
        repo = MockPortfolioRepository()
        with pytest.raises(ValueError, match="Portfolio is invalid"):
            await repo.save_portfolio(None)
    
    @pytest.mark.asyncio
    async def test_get_portfolio_success(self, sample_portfolio):
        """Test getting portfolio by ID."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio)
        result = await repo.get_portfolio("portfolio-1")
        assert result is not None
        assert result.id == "portfolio-1"
        assert result.name == "Test Portfolio"
    
    @pytest.mark.asyncio
    async def test_get_portfolio_not_found_returns_none(self):
        """Test getting non-existent portfolio returns None."""
        repo = MockPortfolioRepository()
        result = await repo.get_portfolio("non-existent")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_portfolio_empty_id_raises_error(self):
        """Test that empty portfolio ID raises ValueError."""
        repo = MockPortfolioRepository()
        with pytest.raises(ValueError, match="Portfolio ID cannot be empty"):
            await repo.get_portfolio("")
    
    @pytest.mark.asyncio
    async def test_get_all_portfolios(self, sample_portfolio):
        """Test getting all portfolios."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio)
        portfolios = await repo.get_all_portfolios()
        assert len(portfolios) == 1
        assert portfolios[0].id == "portfolio-1"
    
    @pytest.mark.asyncio
    async def test_update_portfolio_success(self, sample_portfolio):
        """Test updating portfolio successfully."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio)
        sample_portfolio.cash_balance = 2000.0
        result = await repo.update_portfolio(sample_portfolio)
        assert result is True
        updated = await repo.get_portfolio("portfolio-1")
        assert updated.cash_balance == 2000.0
    
    @pytest.mark.asyncio
    async def test_update_portfolio_not_found_raises_error(self, sample_portfolio):
        """Test that updating non-existent portfolio raises RuntimeError."""
        repo = MockPortfolioRepository()
        with pytest.raises(RuntimeError, match="Portfolio not found"):
            await repo.update_portfolio(sample_portfolio)
    
    @pytest.mark.asyncio
    async def test_delete_portfolio_success(self, sample_portfolio):
        """Test deleting portfolio successfully."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio)
        result = await repo.delete_portfolio("portfolio-1")
        assert result is True
        assert await repo.get_portfolio_count() == 0
    
    @pytest.mark.asyncio
    async def test_delete_portfolio_not_found_returns_false(self):
        """Test deleting non-existent portfolio returns False."""
        repo = MockPortfolioRepository()
        result = await repo.delete_portfolio("non-existent")
        assert result is False
    
    @pytest.mark.asyncio
    async def test_get_portfolio_by_name_success(self, sample_portfolio):
        """Test getting portfolio by name."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio)
        result = await repo.get_portfolio_by_name("Test Portfolio")
        assert result is not None
        assert result.name == "Test Portfolio"
    
    @pytest.mark.asyncio
    async def test_get_portfolio_by_name_not_found_returns_none(self):
        """Test getting portfolio by non-existent name returns None."""
        repo = MockPortfolioRepository()
        result = await repo.get_portfolio_by_name("Non-existent")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_portfolio_by_name_empty_raises_error(self):
        """Test that empty name raises ValueError."""
        repo = MockPortfolioRepository()
        with pytest.raises(ValueError, match="Portfolio name cannot be empty"):
            await repo.get_portfolio_by_name("")
    
    @pytest.mark.asyncio
    async def test_get_portfolio_count(self, sample_portfolio):
        """Test getting portfolio count."""
        repo = MockPortfolioRepository()
        assert await repo.get_portfolio_count() == 0
        await repo.save_portfolio(sample_portfolio)
        assert await repo.get_portfolio_count() == 1
    
    @pytest.mark.asyncio
    async def test_clear_all_portfolios(self, sample_portfolio):
        """Test clearing all portfolios."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio)
        result = await repo.clear_all_portfolios()
        assert result is True
        assert await repo.get_portfolio_count() == 0
    
    @pytest.mark.asyncio
    async def test_portfolio_with_positions(self, sample_portfolio_with_position):
        """Test portfolio with positions."""
        repo = MockPortfolioRepository()
        await repo.save_portfolio(sample_portfolio_with_position)
        portfolio = await repo.get_portfolio("portfolio-2")
        assert portfolio is not None
        assert portfolio.get_position_count() == 1
        assert portfolio.has_position("AAPL") is True

