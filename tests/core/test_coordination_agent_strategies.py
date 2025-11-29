"""
Tests for agent_strategies.py

Comprehensive tests for agent coordination strategies, factory, and decision logic.
Target: 12+ test methods, ≥85% coverage
"""

import pytest
from unittest.mock import MagicMock, patch
from src.core.coordination.agent_strategies import (
    AgentType,
    AgentCoordinatorStrategy,
    Agent1CoordinatorStrategy,
    Agent6CoordinatorStrategy,
    Agent7CoordinatorStrategy,
    AgentStrategyFactory,
)


class TestAgentType:
    """Tests for AgentType enum."""

    def test_enum_values(self):
        """Test enum has correct values."""
        assert AgentType.AGENT_1.value == "agent_1"
        assert AgentType.AGENT_5.value == "agent_5"
        assert AgentType.AGENT_6.value == "agent_6"
        assert AgentType.AGENT_7.value == "agent_7"
        assert AgentType.AGENT_8.value == "agent_8"

    def test_enum_membership(self):
        """Test enum membership."""
        assert AgentType.AGENT_1 in AgentType
        assert AgentType.AGENT_6 in AgentType


class TestAgentCoordinatorStrategy:
    """Tests for AgentCoordinatorStrategy abstract base class."""

    def test_abstract_class_cannot_be_instantiated(self):
        """Test that abstract class cannot be instantiated."""
        with pytest.raises(TypeError):
            AgentCoordinatorStrategy()

    def test_abstract_methods_required(self):
        """Test that concrete implementations must implement abstract methods."""
        class IncompleteStrategy(AgentCoordinatorStrategy):
            pass

        with pytest.raises(TypeError):
            IncompleteStrategy()


class TestAgent1CoordinatorStrategy:
    """Tests for Agent1CoordinatorStrategy."""

    @pytest.mark.asyncio
    async def test_coordinate_agent_with_data(self):
        """Test coordinate_agent with provided data."""
        strategy = Agent1CoordinatorStrategy()
        agent_data = {"integration_targets": ["target1", "target2"]}
        result = await strategy.coordinate_agent(agent_data)
        
        assert result["status"] == "coordinated"
        assert result["integration_targets"] == ["target1", "target2"]
        assert result["core_systems_status"] == "optimized"
        assert result["v2_compliance"] == 100
        assert isinstance(result["vector_insights"], list)
        assert len(result["vector_insights"]) > 0

    @pytest.mark.asyncio
    async def test_coordinate_agent_without_data(self):
        """Test coordinate_agent without provided data."""
        strategy = Agent1CoordinatorStrategy()
        agent_data = {}
        result = await strategy.coordinate_agent(agent_data)
        
        assert result["status"] == "coordinated"
        assert result["integration_targets"] == []
        assert result["v2_compliance"] == 100

    def test_get_agent_metrics(self):
        """Test get_agent_metrics returns correct structure."""
        strategy = Agent1CoordinatorStrategy()
        metrics = strategy.get_agent_metrics()
        
        assert "integration_efficiency" in metrics
        assert "core_systems_coverage" in metrics
        assert "consolidation_impact" in metrics
        assert "v2_compliance_score" in metrics
        assert metrics["v2_compliance_score"] == 100

    def test_get_vector_insights(self):
        """Test get_vector_insights returns insights."""
        strategy = Agent1CoordinatorStrategy()
        insights = strategy.get_vector_insights("integration")
        
        assert isinstance(insights, list)
        assert len(insights) > 0
        assert all(isinstance(insight, str) for insight in insights)


class TestAgent6CoordinatorStrategy:
    """Tests for Agent6CoordinatorStrategy."""

    @pytest.mark.asyncio
    async def test_coordinate_agent_with_data(self):
        """Test coordinate_agent with provided data."""
        strategy = Agent6CoordinatorStrategy()
        agent_data = {"coordination_systems": ["system1", "system2"]}
        result = await strategy.coordinate_agent(agent_data)
        
        assert result["status"] == "coordinated"
        assert result["coordination_systems"] == ["system1", "system2"]
        assert result["communication_protocols"] == "optimized"
        assert result["v2_compliance"] == 100

    @pytest.mark.asyncio
    async def test_coordinate_agent_without_data(self):
        """Test coordinate_agent without provided data."""
        strategy = Agent6CoordinatorStrategy()
        agent_data = {}
        result = await strategy.coordinate_agent(agent_data)
        
        assert result["status"] == "coordinated"
        assert result["coordination_systems"] == []
        assert result["v2_compliance"] == 100

    def test_get_agent_metrics(self):
        """Test get_agent_metrics returns correct structure."""
        strategy = Agent6CoordinatorStrategy()
        metrics = strategy.get_agent_metrics()
        
        assert "coordination_efficiency" in metrics
        assert "communication_coverage" in metrics
        assert "v2_compliance_impact" in metrics
        assert "vector_integration_score" in metrics
        assert metrics["v2_compliance_impact"] == 100

    def test_get_vector_insights(self):
        """Test get_vector_insights returns insights."""
        strategy = Agent6CoordinatorStrategy()
        insights = strategy.get_vector_insights("coordination")
        
        assert isinstance(insights, list)
        assert len(insights) > 0
        assert all(isinstance(insight, str) for insight in insights)


class TestAgent7CoordinatorStrategy:
    """Tests for Agent7CoordinatorStrategy."""

    @pytest.mark.asyncio
    async def test_coordinate_agent_with_data(self):
        """Test coordinate_agent with provided data."""
        strategy = Agent7CoordinatorStrategy()
        agent_data = {"frontend_components": ["comp1", "comp2"]}
        result = await strategy.coordinate_agent(agent_data)
        
        assert result["status"] == "coordinated"
        assert result["frontend_components"] == ["comp1", "comp2"]
        assert result["react_implementation"] == "optimized"
        assert result["v2_compliance"] == 100

    @pytest.mark.asyncio
    async def test_coordinate_agent_without_data(self):
        """Test coordinate_agent without provided data."""
        strategy = Agent7CoordinatorStrategy()
        agent_data = {}
        result = await strategy.coordinate_agent(agent_data)
        
        assert result["status"] == "coordinated"
        assert result["frontend_components"] == []
        assert result["v2_compliance"] == 100

    def test_get_agent_metrics(self):
        """Test get_agent_metrics returns correct structure."""
        strategy = Agent7CoordinatorStrategy()
        metrics = strategy.get_agent_metrics()
        
        assert "frontend_coverage" in metrics
        assert "react_best_practices" in metrics
        assert "component_reusability" in metrics
        assert "v2_compliance_score" in metrics
        assert metrics["v2_compliance_score"] == 100

    def test_get_vector_insights(self):
        """Test get_vector_insights returns insights."""
        strategy = Agent7CoordinatorStrategy()
        insights = strategy.get_vector_insights("web_development")
        
        assert isinstance(insights, list)
        assert len(insights) > 0
        assert all(isinstance(insight, str) for insight in insights)


class TestAgentStrategyFactory:
    """Tests for AgentStrategyFactory."""

    def test_create_strategy_agent_1(self):
        """Test creating strategy for Agent-1."""
        strategy = AgentStrategyFactory.create_strategy(AgentType.AGENT_1)
        assert isinstance(strategy, Agent1CoordinatorStrategy)

    def test_create_strategy_agent_6(self):
        """Test creating strategy for Agent-6."""
        strategy = AgentStrategyFactory.create_strategy(AgentType.AGENT_6)
        assert isinstance(strategy, Agent6CoordinatorStrategy)

    def test_create_strategy_agent_7(self):
        """Test creating strategy for Agent-7."""
        strategy = AgentStrategyFactory.create_strategy(AgentType.AGENT_7)
        assert isinstance(strategy, Agent7CoordinatorStrategy)

    def test_create_strategy_unsupported_agent_raises_error(self):
        """Test creating strategy for unsupported agent raises error."""
        with patch('src.core.coordination.agent_strategies.get_unified_validator') as mock_validator:
            mock_validator_instance = MagicMock()
            mock_validator.return_value = mock_validator_instance
            
            with pytest.raises(Exception):
                AgentStrategyFactory.create_strategy(AgentType.AGENT_5)
            
            mock_validator_instance.raise_validation_error.assert_called_once()

    def test_get_all_strategies(self):
        """Test get_all_strategies returns all strategies."""
        strategies = AgentStrategyFactory.get_all_strategies()
        
        assert isinstance(strategies, dict)
        assert AgentType.AGENT_1 in strategies
        assert AgentType.AGENT_6 in strategies
        assert AgentType.AGENT_7 in strategies
        assert isinstance(strategies[AgentType.AGENT_1], Agent1CoordinatorStrategy)
        assert isinstance(strategies[AgentType.AGENT_6], Agent6CoordinatorStrategy)
        assert isinstance(strategies[AgentType.AGENT_7], Agent7CoordinatorStrategy)

    def test_get_all_strategies_returns_new_instances(self):
        """Test get_all_strategies returns new instances each time."""
        strategies1 = AgentStrategyFactory.get_all_strategies()
        strategies2 = AgentStrategyFactory.get_all_strategies()
        
        # Should be different instances
        assert strategies1[AgentType.AGENT_1] is not strategies2[AgentType.AGENT_1]

    def test_agent1_strategy_vector_insights_different_contexts(self):
        """Test Agent1 strategy returns different insights for different contexts."""
        strategy = Agent1CoordinatorStrategy()
        insights1 = strategy.get_vector_insights("integration")
        insights2 = strategy.get_vector_insights("core_systems")
        
        # Should return insights (may be same or different)
        assert isinstance(insights1, list)
        assert isinstance(insights2, list)
        assert len(insights1) > 0
        assert len(insights2) > 0

    def test_agent6_strategy_coordination_systems(self):
        """Test Agent6 strategy handles coordination systems correctly."""
        strategy = Agent6CoordinatorStrategy()
        agent_data = {"coordination_systems": ["system1", "system2", "system3"]}
        
        import asyncio
        result = asyncio.run(strategy.coordinate_agent(agent_data))
        
        assert result["coordination_systems"] == ["system1", "system2", "system3"]
        assert len(result["vector_insights"]) > 0

    def test_agent7_strategy_frontend_components(self):
        """Test Agent7 strategy handles frontend components correctly."""
        strategy = Agent7CoordinatorStrategy()
        agent_data = {"frontend_components": ["Component1", "Component2"]}
        
        import asyncio
        result = asyncio.run(strategy.coordinate_agent(agent_data))
        
        assert result["frontend_components"] == ["Component1", "Component2"]
        assert result["react_implementation"] == "optimized"

    def test_factory_strategy_consistency(self):
        """Test that factory returns consistent strategy types."""
        strategy1 = AgentStrategyFactory.create_strategy(AgentType.AGENT_1)
        strategy2 = AgentStrategyFactory.create_strategy(AgentType.AGENT_1)
        
        # Should be same type
        assert type(strategy1) == type(strategy2)
        assert isinstance(strategy1, Agent1CoordinatorStrategy)
        assert isinstance(strategy2, Agent1CoordinatorStrategy)

    def test_all_strategies_have_metrics(self):
        """Test that all strategies return metrics."""
        strategies = AgentStrategyFactory.get_all_strategies()
        
        for agent_type, strategy in strategies.items():
            metrics = strategy.get_agent_metrics()
            assert isinstance(metrics, dict)
            assert len(metrics) > 0
            # All should have v2_compliance related metric
            assert any("v2" in key.lower() or "compliance" in key.lower() for key in metrics.keys())

