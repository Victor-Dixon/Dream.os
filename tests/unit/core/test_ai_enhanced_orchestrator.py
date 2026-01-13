"""
Tests for AI-Enhanced Orchestrator
==================================

Tests for the AI-enhanced orchestrator functionality including
intelligent coordination, decision making, and learning capabilities.

Author: Agent-5 (Infrastructure Automation Specialist)
Date: 2026-01-13
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from collections.abc import Iterable

from src.core.orchestration.ai_enhanced_orchestrator import (
    AIEnhancedOrchestrator,
    CoordinationMetrics,
    AIDecision
)
from src.core.orchestration.ai_orchestrator_factory import (
    AIOrchestratorFactory,
    OrchestratorType,
    create_smart_orchestrator
)
from src.core.orchestration.contracts import OrchestrationContext, OrchestrationResult
from src.core.orchestration.registry import StepRegistry


class MockStep:
    """Mock step for testing."""
    def __init__(self, name: str = "test_step"):
        self.step_name = name

    def name(self) -> str:
        return self.step_name

    def run(self, ctx: OrchestrationContext, data: dict) -> dict:
        data[f"{self.step_name}_executed"] = True
        return data


class TestAIEnhancedOrchestrator:
    """Test cases for AI-enhanced orchestrator."""

    @pytest.fixture
    def mock_registry(self):
        """Create a mock step registry."""
        registry = Mock(spec=StepRegistry)
        registry.build.return_value = [MockStep("step1"), MockStep("step2")]
        return registry

    @pytest.fixture
    def sample_context(self):
        """Sample coordination context for testing."""
        return {
            'agents': [
                {'id': 'agent-1', 'specialties': ['python', 'testing'], 'capacity': 5},
                {'id': 'agent-2', 'specialties': ['javascript', 'ui'], 'capacity': 3}
            ],
            'tasks': [
                {'id': 'task-1', 'priority': 4, 'assigned_to': 'agent-1', 'complexity': 3},
                {'id': 'task-2', 'priority': 2, 'assigned_to': 'agent-2', 'dependencies': ['task-1']}
            ],
            'coordination_state': {'phase': 'execution', 'progress': 0.5}
        }

    @patch('src.core.orchestration.ai_enhanced_orchestrator.AI_AVAILABLE', True)
    @patch('src.core.orchestration.ai_enhanced_orchestrator.CONTEXT_AVAILABLE', True)
    def test_orchestrator_initialization(self, mock_registry):
        """Test orchestrator initializes correctly."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        assert orchestrator.registry == mock_registry
        assert orchestrator.pipeline_keys == pipeline
        assert isinstance(orchestrator.metrics, CoordinationMetrics)
        assert orchestrator.decision_history == []

    @patch('src.core.orchestration.ai_enhanced_orchestrator.AI_AVAILABLE', False)
    def test_orchestrator_fallback_when_ai_unavailable(self, mock_registry):
        """Test orchestrator works when AI is unavailable."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        assert orchestrator.reasoning_engine is None
        assert orchestrator.context_engine is None

    def test_workload_analysis(self, mock_registry, sample_context):
        """Test workload distribution analysis."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        analysis = orchestrator._analyze_workload_distribution(
            sample_context['agents'],
            sample_context['tasks']
        )

        assert 'agent-1' in analysis
        assert 'agent-2' in analysis
        assert analysis['agent-1']['current_tasks'] == 1
        assert analysis['agent-2']['current_tasks'] == 1
        assert analysis['agent-1']['workload_score'] > 0
        assert analysis['agent-2']['workload_score'] > 0

    def test_priority_optimization(self, mock_registry, sample_context):
        """Test AI-enhanced priority optimization."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        recommendations = orchestrator._optimize_priorities(
            sample_context['tasks'],
            sample_context['coordination_state']
        )

        assert 'task-1' in recommendations
        assert 'task-2' in recommendations
        assert 'original' in recommendations['task-1']
        assert 'recommended' in recommendations['task-1']
        assert 'reasoning' in recommendations['task-1']

    def test_strategy_recommendation(self, mock_registry, sample_context):
        """Test coordination strategy recommendations."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        analysis = {'complexity': 0.7, 'agent_count': 2, 'task_count': 2}
        strategy = orchestrator._recommend_strategy(
            sample_context['agents'],
            sample_context['tasks'],
            analysis
        )

        assert isinstance(strategy, str)
        assert strategy in ['parallel_execution', 'prioritized_sequential', 'pair_programming', 'balanced_distribution']

    def test_risk_assessment(self, mock_registry, sample_context):
        """Test coordination risk assessment."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        risks = orchestrator._assess_coordination_risks(
            sample_context['agents'],
            sample_context['tasks']
        )

        assert 'high_priority_tasks' in risks
        assert 'overloaded_agents' in risks
        assert 'single_points_failure' in risks
        assert 'deadline_pressure' in risks
        assert 'overall_score' in risks
        assert 0.0 <= risks['overall_score'] <= 1.0

    def test_orchestrator_execution(self, mock_registry):
        """Test basic orchestrator execution."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        ctx = Mock(spec=OrchestrationContext)
        ctx.emit = Mock()
        payload = {'test': 'data'}

        result = orchestrator.execute(ctx, payload)

        assert isinstance(result, OrchestrationResult)
        assert result.ok is True
        assert 'steps' in result.metrics
        assert result.metrics['steps'] == 2

    def test_learning_metrics_update(self, mock_registry, sample_context):
        """Test that learning metrics are updated during execution."""
        pipeline = ["step1", "step2"]
        orchestrator = AIEnhancedOrchestrator(mock_registry, pipeline)

        ctx = Mock(spec=OrchestrationContext)
        ctx.emit = Mock()

        # Execute orchestration
        result = orchestrator.execute(ctx, sample_context)

        # Check that metrics were updated
        assert len(orchestrator.metrics.coordination_patterns) > 0
        latest_pattern = orchestrator.metrics.coordination_patterns[-1]
        assert 'timestamp' in latest_pattern
        assert 'success' in latest_pattern
        assert 'execution_time' in latest_pattern


class TestAIOrchestratorFactory:
    """Test cases for AI orchestrator factory."""

    @pytest.fixture
    def mock_registry(self):
        """Create a mock step registry."""
        registry = Mock(spec=StepRegistry)
        return registry

    def test_factory_initialization(self):
        """Test factory initializes correctly."""
        factory = AIOrchestratorFactory()
        assert hasattr(factory, 'ai_available')
        assert isinstance(factory.performance_metrics, dict)

    @patch('src.core.orchestration.ai_orchestrator_factory.AIOrchestratorFactory._check_ai_availability')
    def test_orchestrator_type_selection_ai_available(self, mock_check, mock_registry):
        """Test orchestrator type selection when AI is available."""
        mock_check.return_value = True
        factory = AIOrchestratorFactory()

        # High complexity context should select AI
        complex_context = {
            'tasks': [{'priority': 5, 'dependencies': ['task1', 'task2'], 'required_skills': ['ai', 'ml', 'python']}],
            'agents': [{'id': 'agent1', 'specialties': ['ai', 'ml']}, {'id': 'agent2', 'specialties': ['python']}],
            'requirements': {'ai_enhancement': True}
        }

        orchestrator_type = factory.select_orchestrator_type(complex_context)
        assert orchestrator_type == OrchestratorType.AI_ENHANCED

    @patch('src.core.orchestration.ai_orchestrator_factory.AIOrchestratorFactory._check_ai_availability')
    def test_orchestrator_type_selection_ai_unavailable(self, mock_check, mock_registry):
        """Test orchestrator type selection when AI is unavailable."""
        mock_check.return_value = False
        factory = AIOrchestratorFactory()

        context = {'tasks': [], 'agents': []}
        orchestrator_type = factory.select_orchestrator_type(context)
        assert orchestrator_type == OrchestratorType.STANDARD

    @patch('src.core.orchestration.ai_orchestrator_factory.AIOrchestratorFactory._check_ai_availability')
    def test_orchestrator_creation_ai_enhanced(self, mock_check, mock_registry):
        """Test AI-enhanced orchestrator creation."""
        mock_check.return_value = True
        factory = AIOrchestratorFactory()

        pipeline = ["step1", "step2"]
        context = {
            'tasks': [{'priority': 5}],
            'agents': [{'id': 'agent1'}]
        }

        with patch('src.core.orchestration.ai_enhanced_orchestrator.AI_AVAILABLE', True):
            orchestrator = factory.create_orchestrator(mock_registry, pipeline, context)
            assert isinstance(orchestrator, AIEnhancedOrchestrator)

    @patch('src.core.orchestration.ai_orchestrator_factory.AIOrchestratorFactory._check_ai_availability')
    def test_orchestrator_creation_fallback(self, mock_check, mock_registry):
        """Test fallback to standard orchestrator."""
        mock_check.return_value = False
        factory = AIOrchestratorFactory()

        pipeline = ["step1", "step2"]
        context = {}

        orchestrator = factory.create_orchestrator(mock_registry, pipeline, context)
        # Should be CoreOrchestrator when AI unavailable
        assert orchestrator.__class__.__name__ == 'CoreOrchestrator'

    def test_task_complexity_assessment(self, mock_registry):
        """Test task complexity assessment."""
        factory = AIOrchestratorFactory()

        # High complexity task
        complex_tasks = [{
            'priority': 5,
            'dependencies': ['dep1', 'dep2', 'dep3'],
            'required_skills': ['ai', 'ml', 'python', 'react', 'docker']
        }]

        complexity = factory._assess_task_complexity(complex_tasks)
        assert complexity > 0.8  # Should be high complexity

        # Low complexity task
        simple_tasks = [{
            'priority': 1,
            'dependencies': [],
            'required_skills': []
        }]

        complexity = factory._assess_task_complexity(simple_tasks)
        assert complexity < 0.3  # Should be low complexity

    def test_time_pressure_assessment(self, mock_registry):
        """Test time pressure assessment."""
        factory = AIOrchestratorFactory()

        # High pressure tasks
        pressure_tasks = [
            {'priority': 4, 'deadline': 'urgent'},
            {'priority': 5, 'blocked': True}
        ]

        pressure = factory._assess_time_pressure(pressure_tasks)
        assert pressure > 0.5  # Should detect pressure

        # Low pressure tasks
        relaxed_tasks = [
            {'priority': 1},
            {'priority': 2}
        ]

        pressure = factory._assess_time_pressure(relaxed_tasks)
        assert pressure < 0.5  # Should be relaxed


@pytest.mark.asyncio
class TestSmartOrchestratorCreation:
    """Test smart orchestrator creation function."""

    @pytest.fixture
    def mock_registry(self):
        """Create a mock step registry."""
        registry = Mock(spec=StepRegistry)
        return registry

    @patch('src.core.orchestration.ai_orchestrator_factory.AIOrchestratorFactory._check_ai_availability')
    def test_smart_orchestrator_creation(self, mock_check, mock_registry):
        """Test smart orchestrator creation function."""
        mock_check.return_value = True

        pipeline = ["step1", "step2"]
        context = {
            'tasks': [{'priority': 5}],
            'agents': [{'id': 'agent1'}]
        }

        with patch('src.core.orchestration.ai_enhanced_orchestrator.AI_AVAILABLE', True):
            orchestrator = create_smart_orchestrator(mock_registry, pipeline, context)
            assert isinstance(orchestrator, AIEnhancedOrchestrator)