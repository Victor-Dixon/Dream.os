"""
Portfolio Handlers
==================

Handler classes for portfolio service operations.
Wires PortfolioService to web layer.

<!-- SSOT Domain: web -->

V2 Compliance: < 300 lines, handler pattern.
Consolidated: Uses BaseHandler.
"""

from flask import jsonify, request
from typing import Tuple, Any

from src.core.base.base_handler import BaseHandler
from src.services.portfolio_service import PortfolioService


class PortfolioHandlers(BaseHandler):
    """Handler class for portfolio operations."""
    
    def __init__(self):
        """Initialize portfolio handlers."""
        super().__init__("PortfolioHandlers")
        self.service = PortfolioService()
    
    def handle_list_portfolios(self, request) -> Tuple[Any, int]:
        """
        Handle request to list all portfolios.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            portfolios = list(self.service.portfolios.values())
            
            portfolios_data = [
                {
                    "id": p.id,
                    "user_id": p.user_id,
                    "name": p.name,
                    "stock_count": len(p.stocks) if p.stocks else 0
                }
                for p in portfolios
            ]
            
            response = self.format_response(
                {
                    "portfolios": portfolios_data,
                    "total": len(portfolios)
                },
                success=True
            )
            return jsonify(response), 200
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_list_portfolios")
            return jsonify(error_response), 500
    
    def handle_create_portfolio(self, request) -> Tuple[Any, int]:
        """
        Handle request to create a new portfolio.
        
        Args:
            request: Flask request object
            
        Returns:
            Tuple of (response_data, status_code)
        """
        try:
            data = request.get_json()
            if not data:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="No data provided"
                )
                return jsonify(error_response), 400
            
            user_id = data.get("user_id")
            portfolio_data = data.get("portfolio_data", {})
            
            if not user_id:
                error_response = self.format_response(
                    None,
                    success=False,
                    error="user_id is required"
                )
                return jsonify(error_response), 400
            
            portfolio = self.service.create_portfolio(user_id, portfolio_data)
            
            response = self.format_response(
                {
                    "portfolio": {
                        "id": portfolio.id,
                        "user_id": portfolio.user_id,
                        "name": portfolio.name
                    }
                },
                success=True
            )
            return jsonify(response), 201
            
        except Exception as e:
            error_response = self.handle_error(e, "handle_create_portfolio")
            return jsonify(error_response), 500

