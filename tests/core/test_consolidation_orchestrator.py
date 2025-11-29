"""
Unit tests for consolidation/consolidation_orchestrator.py - HIGH PRIORITY

Tests ConsolidationOrchestrator class functionality.
Note: Maps to utility_consolidation_orchestrator.py until consolidation_orchestrator.py is created.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import sys
from pathlib import Path
import tempfile
import os

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the actual orchestrator (utility_consolidation_orchestrator)
from src.core.consolidation.utility_consolidation.utility_consolidation_orchestrator import (
    UtilityConsolidationOrchestrator
)
from src.core.consolidation.utility_consolidation.utility_consolidation_models import (
    ConsolidationConfig,
    ConsolidationResult,
    ConsolidationType,
    ConsolidationOpportunity,
    UtilityFunction
)

# Alias for test purposes
ConsolidationOrchestrator = UtilityConsolidationOrchestrator


class TestConsolidationOrchestrator:
    """Test suite for ConsolidationOrchestrator class."""

    @pytest.fixture
    def config(self):
        """Create a ConsolidationConfig instance."""
        return ConsolidationConfig(target_directory=tempfile.mkdtemp())

    @pytest.fixture
    def orchestrator(self, config):
        """Create a ConsolidationOrchestrator instance."""
        return ConsolidationOrchestrator(config)

    @pytest.fixture
    def mock_engine(self):
        """Create a mock engine for testing."""
        engine = MagicMock()
        engine.consolidation_opportunities = []
        engine.analyze_codebase = Mock(return_value={})
        return engine

    def test_initialization(self, config):
        """Test ConsolidationOrchestrator initialization."""
        orchestrator = ConsolidationOrchestrator(config)
        
        assert orchestrator.config == config
        assert orchestrator.engine is not None

    def test_initialization_default_config(self):
        """Test initialization with default config."""
        orchestrator = ConsolidationOrchestrator()
        
        assert orchestrator.config is not None
        assert isinstance(orchestrator.config, ConsolidationConfig)

    def test_run_consolidation_analysis(self, orchestrator, tmp_path):
        """Test run_consolidation_analysis method."""
        source_dir = str(tmp_path)
        
        # Mock engine methods
        orchestrator.engine.analyze_codebase = Mock(return_value={"results": "data"})
        orchestrator.engine.consolidation_opportunities = []
        
        result = orchestrator.run_consolidation_analysis(source_dir)
        
        assert "analysis_results" in result
        assert "report" in result
        assert result["status"] == "completed"
        orchestrator.engine.analyze_codebase.assert_called_once_with(source_dir)

    def test_generate_consolidation_report_empty(self, orchestrator):
        """Test generate_consolidation_report with no opportunities."""
        orchestrator.engine.consolidation_opportunities = []
        
        report = orchestrator.generate_consolidation_report()
        
        assert "timestamp" in report
        assert report["consolidation_summary"]["total_opportunities"] == 0
        assert report["consolidation_summary"]["estimated_lines_reduced"] == 0

    def test_generate_consolidation_report_with_opportunities(self, orchestrator):
        """Test generate_consolidation_report with opportunities."""
        # Create mock opportunities
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
        orchestrator.engine.consolidation_opportunities = [opp]
        
        report = orchestrator.generate_consolidation_report()
        
        assert report["consolidation_summary"]["total_opportunities"] == 1
        assert report["consolidation_summary"]["estimated_lines_reduced"] == 5
        assert report["consolidation_summary"]["high_priority_count"] == 1
        assert len(report["detailed_opportunities"]) == 1

    def test_execute_consolidation_invalid_index(self, orchestrator):
        """Test execute_consolidation with invalid index."""
        orchestrator.engine.consolidation_opportunities = []
        
        result = orchestrator.execute_consolidation(0)
        
        assert result.success is False
        assert "Invalid opportunity index" in result.error_message

    def test_execute_consolidation_success(self, orchestrator, tmp_path):
        """Test execute_consolidation with valid index."""
        orchestrator.config.target_directory = str(tmp_path)
        
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
        )
        orchestrator.engine.consolidation_opportunities = [opp]
        
        result = orchestrator.execute_consolidation(0)
        
        assert result.success is True
        assert result.functions_consolidated == 1
        assert result.lines_reduced == 5
        assert result.new_file_path is not None

    def test_execute_consolidation_exception(self, orchestrator):
        """Test execute_consolidation with exception."""
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
        )
        orchestrator.engine.consolidation_opportunities = [opp]
        
        # Mock file write to raise exception
        with patch('builtins.open', side_effect=IOError("Permission denied")):
            result = orchestrator.execute_consolidation(0)
            
            assert result.success is False
            assert result.error_message is not None

    def test_create_consolidated_function(self, orchestrator):
        """Test _create_consolidated_function method."""
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
        )
        
        content = orchestrator._create_consolidated_function(opp)
        
        assert "Consolidated utility function: test_func" in content
        assert primary_func.content in content
        assert "test2.py" in content

    def test_write_consolidated_file(self, orchestrator, tmp_path):
        """Test _write_consolidated_file method."""
        orchestrator.config.target_directory = str(tmp_path)
        
        file_path = orchestrator._write_consolidated_file("test_func", "def test_func(): pass")
        
        assert os.path.exists(file_path)
        assert "consolidated_test_func.py" in file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            assert f.read() == "def test_func(): pass"

    def test_update_references(self, orchestrator):
        """Test _update_references method."""
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
        )
        
        # Should not raise exception
        orchestrator._update_references(opp)

    def test_save_report(self, orchestrator, tmp_path):
        """Test save_report method."""
        report = {"test": "data", "timestamp": datetime.now().isoformat()}
        file_path = os.path.join(tmp_path, "report.json")
        
        orchestrator.save_report(report, file_path)
        
        assert os.path.exists(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            import json
            loaded = json.load(f)
            assert loaded["test"] == "data"

    def test_get_opportunities_summary_empty(self, orchestrator):
        """Test get_opportunities_summary with no opportunities."""
        orchestrator.engine.consolidation_opportunities = []
        
        summary = orchestrator.get_opportunities_summary()
        
        assert summary == []

    def test_get_opportunities_summary_with_opportunities(self, orchestrator):
        """Test get_opportunities_summary with opportunities."""
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
        orchestrator.engine.consolidation_opportunities = [opp]
        
        summary = orchestrator.get_opportunities_summary()
        
        assert len(summary) == 1
        assert summary[0]["function_name"] == "test_func"
        assert summary[0]["index"] == 0
        assert summary[0]["priority"] == "HIGH"

