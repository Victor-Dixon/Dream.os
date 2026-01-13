"""
Portfolio Repository Interface - V2 Compliant Module
===================================================

Abstract interface for portfolio data access with V2 compliance.
Extracted from trading_repository.py for V2 compliance.

<!-- SSOT Domain: trading_robot -->

V2 Compliance: < 300 lines, single responsibility.
Repository Pattern: Clean data access abstraction.

Author: Agent-2 (Architecture & Design Specialist) - Enhanced
Date: 2025-12-03
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Optional

from ..models import Portfolio


class PortfolioRepositoryInterface(ABC):
    """
    Abstract interface for portfolio data access with V2 compliance.
    
    V2 COMPLIANCE: Repository pattern with async operations and comprehensive error handling.
    DESIGN PATTERN: Repository pattern providing clean data access abstraction.
    
    This interface defines the contract for portfolio persistence operations,
    following the repository pattern for clean separation of concerns.
    """

    @abstractmethod
    async def save_portfolio(self, portfolio: Portfolio) -> bool:
        """Save portfolio to storage.

        Args:
            portfolio: Portfolio object to save

        Returns:
            True if successful, False otherwise
        
        Raises:
            ValueError: If portfolio is invalid or missing required fields
            RuntimeError: If storage operation fails
        """
        pass

    @abstractmethod
    async def get_portfolio(
        self, 
        portfolio_id: str
    ) -> Optional[Portfolio]:
        """Retrieve portfolio by ID.

        Args:
            portfolio_id: Unique identifier for the portfolio

        Returns:
            Portfolio object if found, None otherwise
        
        Raises:
            ValueError: If portfolio_id is empty or invalid
            RuntimeError: If retrieval operation fails
        """
        pass

    @abstractmethod
    async def get_all_portfolios(self) -> list[Portfolio]:
        """Get all portfolios.

        Returns:
            List of Portfolio objects
        """
        pass

    @abstractmethod
    async def update_portfolio(self, portfolio: Portfolio) -> bool:
        """Update existing portfolio.

        Args:
            portfolio: Portfolio object to update

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete_portfolio(self, portfolio_id: str) -> bool:
        """Delete portfolio by ID.

        Args:
            portfolio_id: Unique identifier for the portfolio

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_portfolio_by_name(
        self, 
        name: str
    ) -> Optional[Portfolio]:
        """Retrieve portfolio by name.

        Args:
            name: Portfolio name

        Returns:
            Portfolio object if found, None otherwise
        
        Raises:
            ValueError: If name is empty or invalid
            RuntimeError: If retrieval operation fails
        """
        pass

    @abstractmethod
    async def get_portfolio_count(self) -> int:
        """Get total number of portfolios.

        Returns:
            Total number of portfolios in storage
        """
        pass

    @abstractmethod
    async def clear_all_portfolios(self) -> bool:
        """Clear all portfolios from storage.

        Returns:
            True if successful, False otherwise
        """
        pass
