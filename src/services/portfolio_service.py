#!/usr/bin/env python3
"""
<!-- SSOT Domain: integration -->

Portfolio Service - DreamBank Integration
==========================================

Unified portfolio management service integrating DreamBank logic.
Service Enhancement pattern: Extracts core portfolio logic from merged repos.

Consolidated: Uses BaseService (33% code reduction).

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-11-27
V2 Compliance: <400 lines
"""

import os
import sys
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.base.base_service import BaseService
from src.core.config.timeout_constants import TimeoutConstants


@dataclass
class Stock:
    """Stock data model."""
    symbol: str
    quantity: int = 0
    purchase_price: float = 0.0
    current_price: float = 0.0
    change: str = "+0.0%"


@dataclass
class Portfolio:
    """Portfolio data model."""
    id: str
    user_id: str
    name: str
    stocks: List[Stock] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.stocks is None:
            self.stocks = []
        if self.created_at is None:
            self.created_at = datetime.now()


class PortfolioService(BaseService):
    """
    Unified portfolio management service.
    
    Integrates DreamBank portfolio logic:
    - Stock tracking and management
    - Financial data processing
    - Portfolio analysis
    - Stock recommendations
    """
    
    def __init__(self, repository=None):
        """Initialize portfolio service."""
        super().__init__("PortfolioService")
        self.repository = repository
        self.api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.portfolios: Dict[str, Portfolio] = {}
    
    def create_portfolio(
        self, 
        user_id: str, 
        portfolio_data: Dict[str, Any]
    ) -> Portfolio:
        """
        Create a new portfolio.
        
        Args:
            user_id: User identifier
            portfolio_data: Portfolio data (name, etc.)
        
        Returns:
            Created portfolio
        """
        portfolio_id = f"portfolio_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        portfolio = Portfolio(
            id=portfolio_id,
            user_id=user_id,
            name=portfolio_data.get("name", "My Portfolio"),
            stocks=[]
        )
        self.portfolios[portfolio_id] = portfolio
        self.logger.info(f"Created portfolio {portfolio_id} for user {user_id}")
        return portfolio
    
    def add_stock(
        self, 
        portfolio_id: str, 
        stock: Stock
    ) -> bool:
        """
        Add stock to portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            stock: Stock to add
        
        Returns:
            Success status
        """
        if portfolio_id not in self.portfolios:
            self.logger.error(f"Portfolio {portfolio_id} not found")
            return False
        
        portfolio = self.portfolios[portfolio_id]
        
        # Update current price
        stock.current_price = self._fetch_stock_price(stock.symbol)
        
        # Check if stock already exists
        existing = next(
            (s for s in portfolio.stocks if s.symbol == stock.symbol),
            None
        )
        if existing:
            existing.quantity += stock.quantity
            existing.current_price = stock.current_price
        else:
            portfolio.stocks.append(stock)
        
        self.logger.info(f"Added stock {stock.symbol} to portfolio {portfolio_id}")
        return True
    
    def remove_stock(
        self, 
        portfolio_id: str, 
        symbol: str
    ) -> bool:
        """
        Remove stock from portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
            symbol: Stock symbol to remove
        
        Returns:
            Success status
        """
        if portfolio_id not in self.portfolios:
            self.logger.error(f"Portfolio {portfolio_id} not found")
            return False
        
        portfolio = self.portfolios[portfolio_id]
        portfolio.stocks = [
            s for s in portfolio.stocks if s.symbol != symbol
        ]
        self.logger.info(f"Removed stock {symbol} from portfolio {portfolio_id}")
        return True
    
    def analyze_portfolio(
        self, 
        portfolio_id: str
    ) -> Dict[str, Any]:
        """
        Analyze portfolio performance.
        
        Args:
            portfolio_id: Portfolio identifier
        
        Returns:
            Analysis results
        """
        if portfolio_id not in self.portfolios:
            self.logger.error(f"Portfolio {portfolio_id} not found")
            return {}
        
        portfolio = self.portfolios[portfolio_id]
        total_value = self.calculate_total_value(portfolio_id)
        total_cost = sum(
            s.quantity * s.purchase_price for s in portfolio.stocks
        )
        total_return = total_value - total_cost
        return_percentage = (
            (total_return / total_cost * 100) if total_cost > 0 else 0.0
        )
        
        return {
            "portfolio_id": portfolio_id,
            "total_value": total_value,
            "total_cost": total_cost,
            "total_return": total_return,
            "return_percentage": return_percentage,
            "stock_count": len(portfolio.stocks)
        }
    
    def get_recommendations(
        self, 
        portfolio_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get stock recommendations for portfolio.
        
        Args:
            portfolio_id: Portfolio identifier
        
        Returns:
            List of recommendations
        """
        # Placeholder for recommendation logic
        return [
            {
                "symbol": "AAPL",
                "action": "buy",
                "reason": "Strong fundamentals"
            }
        ]
    
    def calculate_total_value(
        self, 
        portfolio_id: str
    ) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            portfolio_id: Portfolio identifier
        
        Returns:
            Total value
        """
        if portfolio_id not in self.portfolios:
            return 0.0
        
        portfolio = self.portfolios[portfolio_id]
        return sum(
            s.quantity * s.current_price for s in portfolio.stocks
        )
    
    def get_performance_metrics(
        self, 
        portfolio_id: str
    ) -> Dict[str, Any]:
        """
        Get portfolio performance metrics.
        
        Args:
            portfolio_id: Portfolio identifier
        
        Returns:
            Performance metrics
        """
        analysis = self.analyze_portfolio(portfolio_id)
        return {
            "total_value": analysis.get("total_value", 0.0),
            "return": analysis.get("return_percentage", 0.0),
            "stock_count": analysis.get("stock_count", 0)
        }
    
    def _fetch_stock_price(
        self, 
        symbol: str
    ) -> float:
        """
        Fetch current stock price from Alpha Vantage API.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Current price
        """
        if not self.api_key:
            self.logger.warning("Alpha Vantage API key not configured")
            return 0.0
        
        try:
            url = (
                f"https://www.alphavantage.co/query?"
                f"function=TIME_SERIES_INTRADAY&"
                f"symbol={symbol}&"
                f"interval=1min&"
                f"apikey={self.api_key}"
            )
            response = requests.get(url, timeout=TimeoutConstants.HTTP_SHORT)
            response.raise_for_status()
            json_data = response.json()
            
            if "Time Series (1min)" not in json_data:
                self.logger.warning(f"No intraday data for {symbol}")
                return 0.0
            
            latest_data = list(json_data["Time Series (1min)"].values())[0]
            return float(latest_data["1. open"])
        
        except Exception as e:
            self.logger.error(f"Error fetching price for {symbol}: {e}")
            return 0.0
    
    def _calculate_change(
        self, 
        current_price: float, 
        previous_price: float
    ) -> str:
        """
        Calculate percentage change.
        
        Args:
            current_price: Current price
            previous_price: Previous price
        
        Returns:
            Change percentage as string
        """
        if previous_price == 0:
            return "+0.0%"
        
        change = ((current_price - previous_price) / previous_price) * 100
        sign = "+" if change >= 0 else ""
        return f"{sign}{change:.2f}%"

