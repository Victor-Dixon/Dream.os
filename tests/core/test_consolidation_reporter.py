"""
Unit tests for consolidation/consolidation_reporter.py - HIGH PRIORITY

Tests ConsolidationReporter class functionality.
Note: Maps to utility_consolidation_orchestrator.py report generation methods.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path
import tempfile
import os
import json

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the orchestrator (has reporting functionality)
from src.core.consolidation.utility_consolidation.utility_consolidation_orchestrator import (
    UtilityConsolidationOrchestrator
)
from src.core.consolidation.utility_consolidation.utility_consolidation_models import (
    ConsolidationConfig,
    ConsolidationType,
    ConsolidationOpportunity,
    UtilityFunction
)

# Alias for test purposes
ConsolidationReporter = UtilityConsolidationOrchestrator


class TestConsolidationReporter:
    """Test suite for ConsolidationReporter class."""

    @pytest.fixture
    def config(self):
        """Create a ConsolidationConfig instance."""
        return ConsolidationConfig(target_directory=tempfile.mkdtemp())

    @pytest.fixture
    def reporter(self, config):
        """Create a ConsolidationReporter instance."""
        return ConsolidationReporter(config)

    def test_initialization(self, config):
        """Test ConsolidationReporter initialization."""
        reporter = ConsolidationReporter(config)
        
        assert reporter.config == config
        assert reporter.engine is not None

    def test_generate_consolidation_report_empty(self, reporter):
        """Test generate_consolidation_report with no opportunities."""
        reporter.engine.consolidation_opportunities = []
        
        report = reporter.generate_consolidation_report()
        
        assert "timestamp" in report
        assert report["consolidation_summary"]["total_opportunities"] == 0
        assert report["consolidation_summary"]["estimated_lines_reduced"] == 0

    def test_generate_consolidation_report_with_opportunities(self, reporter):
        """Test generate_consolidation_report with opportunities."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        opp = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
            primary_function=primary_func,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
            priority="HIGH"
        )
        reporter.engine.consolidation_opportunities = [opp]
        
        report = reporter.generate_consolidation_report()
        
        assert report["consolidation_summary"]["total_opportunities"] == 1
        assert report["consolidation_summary"]["estimated_lines_reduced"] == 5
        assert report["consolidation_summary"]["high_priority_count"] == 1
        assert len(report["detailed_opportunities"]) == 1

    def test_generate_consolidation_report_consolidation_types(self, reporter):
        """Test generate_consolidation_report groups by consolidation types."""
        primary_func1 = UtilityFunction(
            name="func1",
            file_path="test1.py",
            line_start=1,
            line_end=10,
            content="def func1(): pass",
            parameters=[],
        )
        opp1 = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
            primary_function=primary_func1,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
        )
        
        primary_func2 = UtilityFunction(
            name="func2",
            file_path="test2.py",
            line_start=1,
            line_end=10,
            content="def func2(): pass",
            parameters=[],
        )
        opp2 = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.FUNCTION_MERGING,
            primary_function=primary_func2,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=3,
        )
        
        reporter.engine.consolidation_opportunities = [opp1, opp2]
        
        report = reporter.generate_consolidation_report()
        
        assert len(report["consolidation_summary"]["consolidation_types"]) == 2

    def test_save_report(self, reporter, tmp_path):
        """Test save_report method."""
        report = {"test": "data", "timestamp": "2025-01-01T00:00:00"}
        file_path = os.path.join(tmp_path, "report.json")
        
        reporter.save_report(report, file_path)
        
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            assert loaded["test"] == "data"

    def test_save_report_json_format(self, reporter, tmp_path):
        """Test save_report saves valid JSON."""
        report = {"summary": {"count": 5}, "details": []}
        file_path = os.path.join(tmp_path, "report.json")
        
        reporter.save_report(report, file_path)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
            assert loaded["summary"]["count"] == 5

    def test_generate_consolidation_report_detailed_opportunities(self, reporter):
        """Test generate_consolidation_report includes detailed opportunities."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        dup_func = UtilityFunction(
            name="test_func2",
            file_path="test2.py",
            line_start=5,
            line_end=15,
            content="def test_func2(): pass",
            parameters=[],
        )
        opp = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
            primary_function=primary_func,
            duplicate_functions=[dup_func],
            consolidation_strategy="merge",
            estimated_reduction=10,
            priority="MEDIUM"
        )
        reporter.engine.consolidation_opportunities = [opp]
        
        report = reporter.generate_consolidation_report()
        
        assert len(report["detailed_opportunities"]) == 1
        detail = report["detailed_opportunities"][0]
        assert detail["function_name"] == "test_func"
        assert detail["duplicate_count"] == 1

    def test_get_opportunities_summary(self, reporter):
        """Test get_opportunities_summary method."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        opp = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
            primary_function=primary_func,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
            priority="HIGH"
        )
        reporter.engine.consolidation_opportunities = [opp]
        
        summary = reporter.get_opportunities_summary()
        
        assert len(summary) == 1
        assert summary[0]["function_name"] == "test_func"
        assert summary[0]["priority"] == "HIGH"

    def test_generate_consolidation_report_timestamp(self, reporter):
        """Test generate_consolidation_report includes timestamp."""
        reporter.engine.consolidation_opportunities = []
        
        report = reporter.generate_consolidation_report()
        
        assert "timestamp" in report
        assert report["timestamp"] is not None

    def test_save_report_creates_directory(self, reporter, tmp_path):
        """Test save_report creates directory if needed."""
        nested_dir = tmp_path / "nested" / "deep"
        file_path = nested_dir / "report.json"
        
        report = {"test": "data"}
        reporter.save_report(report, str(file_path))
        
        assert file_path.exists()

