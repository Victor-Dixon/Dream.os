#!/usr/bin/env python3
"""
Unit Tests for Business Intelligence Engine
===========================================

Tests for business intelligence engine core and operations.

Author: Agent-5 (Business Intelligence Specialist)
Date: 2025-01-28
"""

import pytest
from datetime import datetime
from src.core.analytics.intelligence.business_intelligence_engine import (
    BusinessIntelligenceEngine
)
from src.core.analytics.intelligence.business_intelligence_engine_core import (
    BusinessIntelligenceEngineCore
)
from src.core.analytics.intelligence.business_intelligence_engine_operations import (
    BusinessIntelligenceEngineOperations
)


class TestBusinessIntelligenceEngineCore:
    """Tests for BusinessIntelligenceEngineCore."""

    def test_initialization(self):
        """Test engine core initialization."""
        engine = BusinessIntelligenceEngineCore()
        assert engine.config == {}
        assert engine.insights == []
        assert engine.metrics == {}

    def test_initialization_with_config(self):
        """Test engine core initialization with config."""
        config = {"setting": "value"}
        engine = BusinessIntelligenceEngineCore(config)
        assert engine.config == config

    def test_generate_insights_empty_data(self):
        """Test insight generation with empty data."""
        engine = BusinessIntelligenceEngineCore()
        result = engine.generate_insights([])
        assert "error" in result
        assert result["error"] == "No data provided"

    def test_generate_insights_with_data(self):
        """Test insight generation with valid data."""
        engine = BusinessIntelligenceEngineCore()
        data = [
            {"value": 10, "count": 5},
            {"value": 20, "count": 8},
            {"value": 30, "count": 12},
        ]
        result = engine.generate_insights(data)
        assert "insights" in result
        assert "recommendations" in result
        assert "kpis" in result
        assert result["data_points"] == 3
        assert "timestamp" in result

    def test_generate_insights_stores_results(self):
        """Test that insights are stored."""
        engine = BusinessIntelligenceEngineCore()
        data = [{"value": 10}]
        engine.generate_insights(data)
        assert len(engine.insights) == 1

    def test_insights_limit(self):
        """Test that insights are limited to 50."""
        engine = BusinessIntelligenceEngineCore()
        for i in range(55):
            engine.generate_insights([{"value": i}])
        assert len(engine.insights) == 50


class TestBusinessIntelligenceEngineOperations:
    """Tests for BusinessIntelligenceEngineOperations."""

    def test_initialization(self):
        """Test operations initialization."""
        engine = BusinessIntelligenceEngineOperations()
        assert engine.config == {}
        assert engine.insights == []
        assert engine.metrics == {}

    def test_generate_dashboard_data_empty(self):
        """Test dashboard generation with empty data."""
        engine = BusinessIntelligenceEngineOperations()
        result = engine.generate_dashboard_data([])
        assert "error" in result
        assert result["error"] == "No data provided"

    def test_generate_dashboard_data_with_data(self):
        """Test dashboard generation with valid data."""
        engine = BusinessIntelligenceEngineOperations()
        data = [
            {"value": 10, "timestamp": "2025-01-01"},
            {"value": 20, "timestamp": "2025-01-02"},
        ]
        result = engine.generate_dashboard_data(data)
        assert "summary" in result
        assert "charts" in result
        assert "alerts" in result
        assert "timestamp" in result

    def test_dashboard_summary(self):
        """Test dashboard summary generation."""
        engine = BusinessIntelligenceEngineOperations()
        data = [
            {"value": 10, "timestamp": "2025-01-01"},
            {"value": 20, "timestamp": "2025-01-02"},
        ]
        result = engine.generate_dashboard_data(data)
        summary = result["summary"]
        assert "total_records" in summary
        assert summary["total_records"] == 2


class TestBusinessIntelligenceEngine:
    """Tests for unified BusinessIntelligenceEngine."""

    def test_initialization(self):
        """Test unified engine initialization."""
        engine = BusinessIntelligenceEngine()
        assert engine.config == {}
        assert engine.insights == []

    def test_initialization_with_config(self):
        """Test unified engine initialization with config."""
        config = {"setting": "value"}
        engine = BusinessIntelligenceEngine(config)
        assert engine.config == config

    def test_generate_insights(self):
        """Test insight generation on unified engine."""
        engine = BusinessIntelligenceEngine()
        data = [{"value": 10, "count": 5}]
        result = engine.generate_insights(data)
        assert "insights" in result
        assert "recommendations" in result
        assert "kpis" in result

    def test_generate_dashboard_data(self):
        """Test dashboard generation on unified engine."""
        engine = BusinessIntelligenceEngine()
        data = [{"value": 10, "timestamp": "2025-01-01"}]
        result = engine.generate_dashboard_data(data)
        assert "summary" in result
        assert "charts" in result
        assert "alerts" in result

    def test_both_functionalities(self):
        """Test that unified engine has both core and operations."""
        engine = BusinessIntelligenceEngine()
        data = [{"value": 10, "timestamp": "2025-01-01"}]
        
        # Test core functionality
        insights = engine.generate_insights(data)
        assert "insights" in insights
        
        # Test operations functionality
        dashboard = engine.generate_dashboard_data(data)
        assert "summary" in dashboard


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

