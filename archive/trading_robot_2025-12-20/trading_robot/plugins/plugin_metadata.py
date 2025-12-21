"""
Plugin Metadata
===============

Metadata structure for trading robot plugins.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class PluginMetadata:
    """Metadata for a trading robot plugin."""

    plugin_id: str
    name: str
    version: str
    description: str
    author: str
    symbol: str  # Primary symbol this strategy targets (e.g., "TSLA")
    strategy_type: str  # e.g., "Trend Following", "Mean Reversion", etc.
    created_date: datetime = field(default_factory=datetime.now)
    updated_date: datetime = field(default_factory=datetime.now)

    # Marketplace fields
    is_for_sale: bool = False
    price: float = 0.0
    currency: str = "USD"
    sales_count: int = 0
    rating: float = 0.0
    review_count: int = 0

    # Performance tracking
    total_pnl: float = 0.0
    total_trades: int = 0
    win_rate: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0

    # Configuration
    default_parameters: Dict[str, Any] = field(default_factory=dict)
    required_parameters: List[str] = field(default_factory=list)

    # Tags and categories
    tags: List[str] = field(default_factory=list)
    category: str = "General"

    # Documentation
    documentation_url: Optional[str] = None
    support_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary."""
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "symbol": self.symbol,
            "strategy_type": self.strategy_type,
            "created_date": self.created_date.isoformat(),
            "updated_date": self.updated_date.isoformat(),
            "is_for_sale": self.is_for_sale,
            "price": self.price,
            "currency": self.currency,
            "sales_count": self.sales_count,
            "rating": self.rating,
            "review_count": self.review_count,
            "total_pnl": self.total_pnl,
            "total_trades": self.total_trades,
            "win_rate": self.win_rate,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "default_parameters": self.default_parameters,
            "required_parameters": self.required_parameters,
            "tags": self.tags,
            "category": self.category,
            "documentation_url": self.documentation_url,
            "support_url": self.support_url,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PluginMetadata":
        """Create metadata from dictionary."""
        # Handle datetime strings
        if isinstance(data.get("created_date"), str):
            data["created_date"] = datetime.fromisoformat(data["created_date"])
        if isinstance(data.get("updated_date"), str):
            data["updated_date"] = datetime.fromisoformat(data["updated_date"])

        return cls(**data)

