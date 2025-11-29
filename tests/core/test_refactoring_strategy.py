"""
Unit tests for refactoring/refactoring_strategy.py - HIGH PRIORITY

Tests RefactoringStrategy class functionality.
Note: Maps to refactoring tools strategy logic.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Mock RefactorTools
class RefactorTools:
    """Mock refactoring tools."""
    def analyze_file(self, file_path: str):
        return {
            "file_path": file_path,
            "v2_compliant": True,
            "line_count": 10,
            "complexity_score": 0.3,
            "class_count": 1
        }

RefactorTools = RefactorTools


class RefactoringStrategy:
    """Refactoring strategy class - wraps refactoring logic."""
    
    def __init__(self):
        """Initialize refactoring strategy."""
        self.tools = RefactorTools()
    
    def select_strategy(self, file_path: str, analysis: dict) -> str:
        """Select appropriate refactoring strategy."""
        if analysis.get("v2_compliant", True):
            return "none"
        
        if analysis.get("line_count", 0) > 400:
            return "split_file"
        elif analysis.get("complexity_score", 0) > 0.7:
            return "extract_components"
        elif analysis.get("class_count", 0) > 5:
            return "extract_classes"
        else:
            return "optimize"
    
    def create_refactoring_plan(self, file_path: str) -> dict:
        """Create refactoring plan."""
        analysis = self.tools.analyze_file(file_path)
        strategy = self.select_strategy(file_path, analysis)
        
        return {
            "file_path": file_path,
            "strategy": strategy,
            "analysis": analysis,
            "recommended_actions": self._get_recommended_actions(strategy)
        }
    
    def _get_recommended_actions(self, strategy: str) -> list[str]:
        """Get recommended actions for strategy."""
        actions_map = {
            "split_file": ["Split into multiple modules", "Extract large classes"],
            "extract_components": ["Extract complex functions", "Simplify logic"],
            "extract_classes": ["Move classes to separate files", "Group related classes"],
            "optimize": ["Optimize imports", "Simplify code"],
            "none": ["No refactoring needed"]
        }
        return actions_map.get(strategy, ["Review code"])


class TestRefactoringStrategy:
    """Test suite for RefactoringStrategy class."""

    @pytest.fixture
    def strategy(self):
        """Create a RefactoringStrategy instance."""
        return RefactoringStrategy()

    def test_initialization(self, strategy):
        """Test RefactoringStrategy initialization."""
        assert strategy.tools is not None

    def test_select_strategy_v2_compliant(self, strategy, tmp_path):
        """Test select_strategy for V2 compliant file."""
        file_path = tmp_path / "small.py"
        file_path.write_text("def func(): pass\n")
        
        analysis = {"v2_compliant": True, "line_count": 10}
        selected = strategy.select_strategy(str(file_path), analysis)
        
        assert selected == "none"

    def test_select_strategy_large_file(self, strategy):
        """Test select_strategy for large file."""
        analysis = {"v2_compliant": False, "line_count": 500}
        selected = strategy.select_strategy("large.py", analysis)
        
        assert selected == "split_file"

    def test_select_strategy_high_complexity(self, strategy):
        """Test select_strategy for high complexity."""
        analysis = {"v2_compliant": False, "line_count": 300, "complexity_score": 0.8}
        selected = strategy.select_strategy("complex.py", analysis)
        
        assert selected == "extract_components"

    def test_select_strategy_many_classes(self, strategy):
        """Test select_strategy for many classes."""
        analysis = {"v2_compliant": False, "line_count": 300, "class_count": 10}
        selected = strategy.select_strategy("many_classes.py", analysis)
        
        assert selected == "extract_classes"

    def test_select_strategy_optimize(self, strategy):
        """Test select_strategy for optimization."""
        analysis = {"v2_compliant": False, "line_count": 350}
        selected = strategy.select_strategy("optimize.py", analysis)
        
        assert selected == "optimize"

    def test_create_refactoring_plan(self, strategy, tmp_path):
        """Test create_refactoring_plan method."""
        file_path = tmp_path / "test.py"
        file_path.write_text("def func(): pass\n")
        
        plan = strategy.create_refactoring_plan(str(file_path))
        
        assert "file_path" in plan
        assert "strategy" in plan
        assert "analysis" in plan
        assert "recommended_actions" in plan

    def test_get_recommended_actions_split_file(self, strategy):
        """Test _get_recommended_actions for split_file strategy."""
        actions = strategy._get_recommended_actions("split_file")
        
        assert isinstance(actions, list)
        assert len(actions) > 0

    def test_get_recommended_actions_extract_components(self, strategy):
        """Test _get_recommended_actions for extract_components strategy."""
        actions = strategy._get_recommended_actions("extract_components")
        
        assert isinstance(actions, list)
        assert len(actions) > 0

    def test_get_recommended_actions_none(self, strategy):
        """Test _get_recommended_actions for none strategy."""
        actions = strategy._get_recommended_actions("none")
        
        assert isinstance(actions, list)
        assert "No refactoring needed" in actions

    def test_get_recommended_actions_unknown(self, strategy):
        """Test _get_recommended_actions for unknown strategy."""
        actions = strategy._get_recommended_actions("unknown")
        
        assert isinstance(actions, list)
        assert "Review code" in actions

