"""
Unit tests for orchestration/integration_orchestrator.py - MEDIUM PRIORITY

Tests IntegrationOrchestrator class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock
from dataclasses import dataclass
from typing import Any
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Create mock contracts (same as service_orchestrator)
@dataclass(frozen=True)
class OrchestrationContext:
    config: dict
    emit: callable
    logger: callable

@dataclass
class OrchestrationResult:
    ok: bool
    summary: str
    metrics: dict[str, Any]

class Step:
    def __init__(self, name):
        self._name = name
    def name(self):
        return self._name
    def run(self, ctx, data):
        return data

class Orchestrator:
    pass

# Mock the contracts and registry
mock_contracts = MagicMock()
mock_contracts.OrchestrationContext = OrchestrationContext
mock_contracts.OrchestrationResult = OrchestrationResult
mock_contracts.Step = Step
mock_contracts.Orchestrator = Orchestrator

class StepRegistry:
    def __init__(self):
        self._steps = {}
    def register(self, key, factory):
        if key in self._steps:
            raise ValueError(f"duplicate step key: {key}")
        self._steps[key] = factory
    def build(self, keys):
        return [self._steps[k]() for k in keys if k in self._steps]

mock_registry = MagicMock()
mock_registry.StepRegistry = StepRegistry

# Patch sys.modules
sys.modules['src.core.orchestration.contracts'] = mock_contracts
sys.modules['src.core.orchestration.registry'] = mock_registry

# Import using importlib
import importlib.util
integration_orchestrator_path = project_root / "src" / "core" / "orchestration" / "integration_orchestrator.py"
spec = importlib.util.spec_from_file_location("integration_orchestrator", integration_orchestrator_path)
integration_orchestrator = importlib.util.module_from_spec(spec)
integration_orchestrator.__package__ = 'src.core.orchestration'
spec.loader.exec_module(integration_orchestrator)

IntegrationOrchestrator = integration_orchestrator.IntegrationOrchestrator


class TestIntegrationOrchestrator:
    """Test suite for IntegrationOrchestrator class."""

    @pytest.fixture
    def registry(self):
        """Create a StepRegistry instance."""
        reg = StepRegistry()
        reg.register("step1", lambda: Step("step1"))
        reg.register("step2", lambda: Step("step2"))
        return reg

    @pytest.fixture
    def orchestrator(self, registry):
        """Create an IntegrationOrchestrator instance."""
        return IntegrationOrchestrator(registry)

    @pytest.fixture
    def context(self):
        """Create an OrchestrationContext instance."""
        events = []
        def emit(event_type, data):
            events.append((event_type, data))
        def logger(msg):
            pass
        ctx = OrchestrationContext(config={}, emit=emit, logger=logger)
        object.__setattr__(ctx, '_events', events)
        return ctx

    def test_initialization(self, registry):
        """Test IntegrationOrchestrator initialization."""
        orchestrator = IntegrationOrchestrator(registry)
        
        assert orchestrator.registry == registry

    def test_plan_uses_integration_pipeline(self, orchestrator, context):
        """Test that plan uses integration_pipeline from payload."""
        payload = {"integration_pipeline": ["step1", "step2"]}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 2
        assert steps[0].name() == "step1"
        assert steps[1].name() == "step2"

    def test_plan_with_empty_pipeline(self, orchestrator, context):
        """Test plan with empty integration_pipeline."""
        payload = {"integration_pipeline": []}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 0

    def test_plan_with_missing_pipeline(self, orchestrator, context):
        """Test plan with missing integration_pipeline key."""
        payload = {}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 0

    def test_execute_runs_pipeline(self, orchestrator, context):
        """Test that execute runs all steps in pipeline."""
        payload = {"integration_pipeline": ["step1", "step2"], "data": "test"}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.summary == "integration:2"
        assert result.metrics["integration_steps"] == 2

    def test_execute_preserves_data(self, orchestrator, context):
        """Test that execute preserves data through steps."""
        payload = {"integration_pipeline": ["step1"], "value": 42}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["integration_steps"] == 1

    def test_report_formats_result(self, orchestrator):
        """Test that report formats result correctly."""
        result = OrchestrationResult(ok=True, summary="integration:3", metrics={})
        
        report = orchestrator.report(result)
        
        assert "[IntegrationOrchestrator]" in report
        assert "integration:3" in report

    def test_execute_with_single_step(self, registry, context):
        """Test execute with single step."""
        orchestrator = IntegrationOrchestrator(registry)
        payload = {"integration_pipeline": ["step1"]}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["integration_steps"] == 1

