"""Trading data service (stub)."""

from typing import Any, Dict


class TradingDataService:
    """Provide trading data snapshots for Discord commands."""

    def get_market_conditions(self) -> Dict[str, Any]:
        """Get current market conditions."""
        return {}

    def get_portfolio_snapshot(self) -> Dict[str, Any]:
        """Get a snapshot of portfolio metrics."""
        return {}
