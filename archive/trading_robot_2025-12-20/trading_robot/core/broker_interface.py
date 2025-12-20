"""
Broker Interface - Abstract base class for broker integrations
Enables multi-broker support (Alpaca, Robinhood, etc.)
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from datetime import datetime


class BrokerInterface(ABC):
    """Abstract interface for broker API clients"""

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to broker API."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connected to broker API."""
        pass

    @abstractmethod
    def get_account_info(self) -> Dict[str, Any]:
        """Get account information."""
        pass

    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get current positions."""
        pass

    @abstractmethod
    def get_orders(self, status: str = "open") -> List[Dict[str, Any]]:
        """Get orders by status."""
        pass

    @abstractmethod
    def get_historical_data(
        self,
        symbol: str,
        timeframe: str = "1Min",
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: int = 1000,
    ) -> Any:  # Returns DataFrame or similar
        """Get historical market data."""
        pass

    @abstractmethod
    def submit_market_order(
        self, symbol: str, qty: int, side: str, time_in_force: str = "gtc"
    ) -> Dict[str, Any]:
        """Submit a market order."""
        pass

    @abstractmethod
    def submit_limit_order(
        self,
        symbol: str,
        qty: int,
        side: str,
        limit_price: float,
        time_in_force: str = "gtc",
    ) -> Dict[str, Any]:
        """Submit a limit order."""
        pass

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """Cancel an order."""
        pass

    @abstractmethod
    def get_market_clock(self) -> Dict[str, Any]:
        """Get market clock information."""
        pass







