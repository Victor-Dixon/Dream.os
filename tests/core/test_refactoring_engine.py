"""
Unit tests for refactoring/refactor_tools.py - HIGH PRIORITY

Tests RefactorTools class functionality (treating as refactoring_engine).
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from pathlib import Path
import sys
import tempfile
import os

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import using importlib to handle dependencies
import importlib.util

refactor_tools_path = project_root / "src" / "core" / "refactoring" / "refactor_tools.py"
spec = importlib.util.spec_from_file_location("refactor_tools", refactor_tools_path)
refactor_tools = importlib.util.module_from_spec(spec)
refactor_tools.__package__ = 'src.core.refactoring'

# Mock dependencies before loading
mock_unified_imports = MagicMock()
mock_unified_imports.Path = Path

mock_extraction = MagicMock()
mock_extraction.ExtractionPlan = type('ExtractionPlan', (), {})
mock_extraction.ExtractionTools = MagicMock()

mock_consolidation = MagicMock()
mock_consolidation.ConsolidationPlan = type('ConsolidationPlan', (), {})
mock_consolidation.ConsolidationTools = MagicMock()

mock_optimization = MagicMock()
mock_optimization.OptimizationPlan = type('OptimizationPlan', (), {})
mock_optimization.OptimizationTools = MagicMock()

sys.modules['src.core.unified_import_system'] = MagicMock()
sys.modules['src.core.unified_import_system'].get_unified_import_system = lambda: mock_unified_imports
sys.modules['src.core.refactoring.extraction_tools'] = mock_extraction
sys.modules['src.core.refactoring.tools.consolidation_tools'] = mock_consolidation
sys.modules['src.core.refactoring.tools.optimization_tools'] = mock_optimization

spec.loader.exec_module(refactor_tools)

RefactorTools = refactor_tools.RefactorTools
get_refactor_tools = refactor_tools.get_refactor_tools


class TestRefactorTools:
    """Test suite for RefactorTools class."""

    @pytest.fixture
    def refactor_tools(self):
        """Create a RefactorTools instance."""
        return RefactorTools()

    @pytest.fixture
    def temp_file(self):
        """Create a temporary file for testing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def test_function():\n    pass\n")
            temp_path = f.name
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    def test_initialization(self, refactor_tools):
        """Test RefactorTools initialization."""
        assert refactor_tools.unified_imports is not None
        assert refactor_tools.extraction_tools is not None
        assert refactor_tools.consolidation_tools is not None
        assert refactor_tools.optimization_tools is not None

    def test_create_extraction_plan(self, refactor_tools):
        """Test creating extraction plan."""
        mock_plan = MagicMock()
        refactor_tools.extraction_tools.create_extraction_plan = Mock(return_value=mock_plan)
        
        plan = refactor_tools.create_extraction_plan("test.py")
        
        assert plan == mock_plan
        refactor_tools.extraction_tools.create_extraction_plan.assert_called_once_with("test.py")

    def test_execute_extraction(self, refactor_tools):
        """Test executing extraction plan."""
        mock_plan = MagicMock()
        refactor_tools.extraction_tools.execute_extraction = Mock(return_value=True)
        
        result = refactor_tools.execute_extraction(mock_plan)
        
        assert result is True
        refactor_tools.extraction_tools.execute_extraction.assert_called_once_with(mock_plan)

    def test_create_consolidation_plan(self, refactor_tools):
        """Test creating consolidation plan."""
        mock_plan = MagicMock()
        refactor_tools.consolidation_tools.create_consolidation_plan = Mock(return_value=mock_plan)
        
        plan = refactor_tools.create_consolidation_plan("test_dir")
        
        assert plan == mock_plan
        refactor_tools.consolidation_tools.create_consolidation_plan.assert_called_once_with("test_dir")

    def test_execute_consolidation(self, refactor_tools):
        """Test executing consolidation plan."""
        mock_plan = MagicMock()
        refactor_tools.consolidation_tools.execute_consolidation = Mock(return_value=True)
        
        result = refactor_tools.execute_consolidation(mock_plan)
        
        assert result is True
        refactor_tools.consolidation_tools.execute_consolidation.assert_called_once_with(mock_plan)

    def test_find_duplicate_files(self, refactor_tools):
        """Test finding duplicate files."""
        mock_duplicates = [["file1.py", "file2.py"]]
        refactor_tools.consolidation_tools._find_duplicate_files = Mock(return_value=mock_duplicates)
        
        duplicates = refactor_tools.find_duplicate_files("test_dir")
        
        assert duplicates == mock_duplicates
        refactor_tools.consolidation_tools._find_duplicate_files.assert_called_once_with("test_dir")

    def test_analyze_duplicates(self, refactor_tools):
        """Test analyzing duplicates."""
        mock_analysis = {"count": 5, "groups": 2}
        refactor_tools.consolidation_tools.analyze_duplicates = Mock(return_value=mock_analysis)
        
        analysis = refactor_tools.analyze_duplicates("test_dir")
        
        assert analysis == mock_analysis
        refactor_tools.consolidation_tools.analyze_duplicates.assert_called_once_with("test_dir")

    def test_create_optimization_plan(self, refactor_tools):
        """Test creating optimization plan."""
        mock_plan = MagicMock()
        refactor_tools.optimization_tools.create_optimization_plan = Mock(return_value=mock_plan)
        
        plan = refactor_tools.create_optimization_plan("test.py")
        
        assert plan == mock_plan
        refactor_tools.optimization_tools.create_optimization_plan.assert_called_once_with("test.py")

    def test_execute_optimization(self, refactor_tools):
        """Test executing optimization plan."""
        mock_plan = MagicMock()
        refactor_tools.optimization_tools.execute_optimization = Mock(return_value=True)
        
        result = refactor_tools.execute_optimization(mock_plan, "test.py")
        
        assert result is True
        refactor_tools.optimization_tools.execute_optimization.assert_called_once_with(mock_plan, "test.py")

    def test_get_tool_status(self, refactor_tools):
        """Test getting tool status."""
        status = refactor_tools.get_tool_status()
        
        assert status["extraction_tools"] == "active"
        assert status["consolidation_tools"] == "active"
        assert status["optimization_tools"] == "active"
        assert status["unified_imports"] == "active"

    def test_analyze_file_success(self, refactor_tools, temp_file):
        """Test analyzing file successfully."""
        mock_extraction_plan = MagicMock()
        mock_optimization_plan = MagicMock()
        refactor_tools.create_extraction_plan = Mock(return_value=mock_extraction_plan)
        refactor_tools.create_optimization_plan = Mock(return_value=mock_optimization_plan)
        
        analysis = refactor_tools.analyze_file(temp_file)
        
        assert analysis["file_path"] == temp_file
        assert "line_count" in analysis
        assert "character_count" in analysis
        assert "v2_compliant" in analysis
        assert analysis["extraction_plan"] == mock_extraction_plan
        assert analysis["optimization_plan"] == mock_optimization_plan

    def test_analyze_file_not_found(self, refactor_tools):
        """Test analyzing non-existent file."""
        analysis = refactor_tools.analyze_file("nonexistent.py")
        
        assert "error" in analysis
        assert "not found" in analysis["error"].lower()

    def test_refactor_file_success(self, refactor_tools):
        """Test refactoring file successfully."""
        mock_extraction_plan = MagicMock()
        mock_optimization_plan = MagicMock()
        refactor_tools.create_extraction_plan = Mock(return_value=mock_extraction_plan)
        refactor_tools.create_optimization_plan = Mock(return_value=mock_optimization_plan)
        refactor_tools.execute_extraction = Mock(return_value=True)
        refactor_tools.execute_optimization = Mock(return_value=True)
        
        result = refactor_tools.refactor_file("test.py")
        
        assert result is True
        refactor_tools.execute_extraction.assert_called_once()
        refactor_tools.execute_optimization.assert_called_once()

    def test_refactor_file_extraction_failure(self, refactor_tools):
        """Test refactoring file with extraction failure."""
        mock_extraction_plan = MagicMock()
        mock_optimization_plan = MagicMock()
        refactor_tools.create_extraction_plan = Mock(return_value=mock_extraction_plan)
        refactor_tools.create_optimization_plan = Mock(return_value=mock_optimization_plan)
        refactor_tools.execute_extraction = Mock(return_value=False)
        refactor_tools.execute_optimization = Mock(return_value=True)
        
        result = refactor_tools.refactor_file("test.py")
        
        assert result is False

    def test_refactor_file_exception(self, refactor_tools):
        """Test refactoring file with exception."""
        refactor_tools.create_extraction_plan = Mock(side_effect=Exception("Error"))
        
        result = refactor_tools.refactor_file("test.py")
        
        assert result is False

    def test_get_refactor_tools_singleton(self):
        """Test get_refactor_tools returns singleton."""
        tools1 = get_refactor_tools()
        tools2 = get_refactor_tools()
        
        assert tools1 is tools2
        assert isinstance(tools1, RefactorTools)

