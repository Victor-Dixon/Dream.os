#!/usr/bin/env python3
"""
Trading BI Analytics Orchestrator
==================================

Orchestrates trading business intelligence analytics operations.
Provides unified interface for market analysis, performance metrics,
and risk assessment.

V2 COMPLIANT: Modular orchestrator under 300 lines.
"""

from typing import Dict, List, Any, Optional
from .market_trend_engine import MarketTrendEngine
from .performance_metrics_engine import PerformanceMetricsEngine
from .risk_analysis_engine import RiskAnalysisEngine
from .trading_bi_models import TrendAnalysisConfig, PerformanceConfig, RiskAssessmentConfig


class TradingBiAnalyticsOrchestrator:
    """Orchestrator for trading business intelligence analytics operations."""

    def __init__(self):
        """Initialize the analytics orchestrator."""
        self.market_trend_engine = MarketTrendEngine()
        self.performance_engine = PerformanceMetricsEngine()
        self.risk_engine = RiskAnalysisEngine()

    def analyze_market_trends(self, market_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze market trends from trading data.

        Args:
            market_data: List of market data points

        Returns:
            Analysis results dictionary
        """
        return self.market_trend_engine.analyze_trends(market_data)

    def calculate_performance_metrics(self, trades: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate performance metrics from trading data.

        Args:
            trades: List of trade records

        Returns:
            Performance metrics dictionary
        """
        return self.performance_engine.calculate_metrics(trades)

    def assess_portfolio_risk(self, portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess portfolio risk metrics.

        Args:
            portfolio: Portfolio data dictionary

        Returns:
            Risk assessment results
        """
        return self.risk_engine.analyze_risk(portfolio)

    def generate_comprehensive_report(self,
                                    market_data: List[Dict[str, Any]],
                                    trades: List[Dict[str, Any]],
                                    portfolio: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive trading analytics report.

        Args:
            market_data: Market data for trend analysis
            trades: Trade data for performance analysis
            portfolio: Portfolio data for risk analysis

        Returns:
            Comprehensive analytics report
        """
        trends = self.analyze_market_trends(market_data)
        performance = self.calculate_performance_metrics(trades)
        risk = self.assess_portfolio_risk(portfolio)

        return {
            "market_trends": trends,
            "performance_metrics": performance,
            "risk_assessment": risk,
            "timestamp": "2026-01-08T08:44:00Z",  # Mock timestamp
            "version": "2.0.0"
        }


def create_trading_bi_analytics_orchestrator() -> TradingBiAnalyticsOrchestrator:
    """
    Factory function to create a TradingBiAnalyticsOrchestrator instance.

    Returns:
        Configured TradingBiAnalyticsOrchestrator instance
    """
    return TradingBiAnalyticsOrchestrator()