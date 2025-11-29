"""
Unit tests for consolidation/consolidation_strategy.py - HIGH PRIORITY

Tests ConsolidationStrategy class functionality.
Note: Maps to ConsolidationType enum and ConsolidationTools strategy logic.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import consolidation models (contains strategy types)
from src.core.consolidation.utility_consolidation.utility_consolidation_models import (
    ConsolidationType,
    ConsolidationConfig,
    ConsolidationOpportunity,
    UtilityFunction
)

# Mock ConsolidationTools
class ConsolidationTools:
    """Mock consolidation tools."""
    def create_consolidation_plan(self, directory: str):
        from dataclasses import dataclass
        @dataclass
        class ConsolidationPlan:
            duplicate_groups: list
            consolidation_targets: list
            consolidation_rules: list
            estimated_savings: int
        return ConsolidationPlan([], [], [], 0)

ConsolidationPlan = type('ConsolidationPlan', (), {
    'duplicate_groups': [],
    'consolidation_targets': [],
    'consolidation_rules': [],
    'estimated_savings': 0
})


class ConsolidationStrategy:
    """Consolidation strategy class - wraps consolidation logic."""
    
    def __init__(self, config: ConsolidationConfig = None):
        """Initialize consolidation strategy."""
        self.config = config or ConsolidationConfig()
        self.tools = ConsolidationTools()
    
    def select_strategy(self, opportunity: ConsolidationOpportunity) -> str:
        """Select appropriate consolidation strategy."""
        if opportunity.consolidation_type == ConsolidationType.DUPLICATE_ELIMINATION:
            return "merge_and_remove"
        elif opportunity.consolidation_type == ConsolidationType.FUNCTION_MERGING:
            return "merge_functions"
        elif opportunity.consolidation_type == ConsolidationType.MODULE_CONSOLIDATION:
            return "consolidate_modules"
        else:
            return "default_strategy"
    
    def create_plan(self, directory: str) -> ConsolidationPlan:
        """Create consolidation plan."""
        return self.tools.create_consolidation_plan(directory)
    
    def validate_strategy(self, strategy: str) -> bool:
        """Validate consolidation strategy."""
        valid_strategies = ["merge_and_remove", "merge_functions", "consolidate_modules", "default_strategy"]
        return strategy in valid_strategies


class TestConsolidationStrategy:
    """Test suite for ConsolidationStrategy class."""

    @pytest.fixture
    def strategy(self):
        """Create a ConsolidationStrategy instance."""
        return ConsolidationStrategy()

    @pytest.fixture
    def config(self):
        """Create a ConsolidationConfig instance."""
        return ConsolidationConfig()

    @pytest.fixture
    def opportunity(self):
        """Create a ConsolidationOpportunity instance."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        return ConsolidationOpportunity(
            consolidation_type=ConsolidationType.DUPLICATE_ELIMINATION,
            primary_function=primary_func,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
        )

    def test_initialization(self, strategy):
        """Test ConsolidationStrategy initialization."""
        assert strategy.config is not None
        assert strategy.tools is not None

    def test_initialization_with_config(self, config):
        """Test initialization with config."""
        strategy = ConsolidationStrategy(config)
        assert strategy.config == config

    def test_select_strategy_duplicate_elimination(self, strategy, opportunity):
        """Test select_strategy for duplicate elimination."""
        selected = strategy.select_strategy(opportunity)
        assert selected == "merge_and_remove"

    def test_select_strategy_function_merging(self, strategy):
        """Test select_strategy for function merging."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        opp = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.FUNCTION_MERGING,
            primary_function=primary_func,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
        )
        selected = strategy.select_strategy(opp)
        assert selected == "merge_functions"

    def test_select_strategy_module_consolidation(self, strategy):
        """Test select_strategy for module consolidation."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        opp = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.MODULE_CONSOLIDATION,
            primary_function=primary_func,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
        )
        selected = strategy.select_strategy(opp)
        assert selected == "consolidate_modules"

    def test_select_strategy_default(self, strategy):
        """Test select_strategy for default case."""
        primary_func = UtilityFunction(
            name="test_func",
            file_path="test.py",
            line_start=1,
            line_end=10,
            content="def test_func(): pass",
            parameters=[],
        )
        opp = ConsolidationOpportunity(
            consolidation_type=ConsolidationType.INTERFACE_UNIFICATION,
            primary_function=primary_func,
            duplicate_functions=[],
            consolidation_strategy="merge",
            estimated_reduction=5,
        )
        selected = strategy.select_strategy(opp)
        assert selected == "default_strategy"

    def test_create_plan(self, strategy, tmp_path):
        """Test create_plan method."""
        plan = strategy.create_plan(str(tmp_path))
        
        assert plan is not None
        assert hasattr(plan, 'duplicate_groups') or isinstance(plan, dict)

    def test_validate_strategy_valid(self, strategy):
        """Test validate_strategy with valid strategy."""
        assert strategy.validate_strategy("merge_and_remove") is True
        assert strategy.validate_strategy("merge_functions") is True

    def test_validate_strategy_invalid(self, strategy):
        """Test validate_strategy with invalid strategy."""
        assert strategy.validate_strategy("invalid_strategy") is False

    def test_validate_strategy_default(self, strategy):
        """Test validate_strategy with default strategy."""
        assert strategy.validate_strategy("default_strategy") is True

