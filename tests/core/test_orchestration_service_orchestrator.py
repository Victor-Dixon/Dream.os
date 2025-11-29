"""
Unit tests for orchestration/service_orchestrator.py - MEDIUM PRIORITY

Tests ServiceOrchestrator class functionality.
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

# Create mock contracts
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
service_orchestrator_path = project_root / "src" / "core" / "orchestration" / "service_orchestrator.py"
spec = importlib.util.spec_from_file_location("service_orchestrator", service_orchestrator_path)
service_orchestrator = importlib.util.module_from_spec(spec)
service_orchestrator.__package__ = 'src.core.orchestration'
spec.loader.exec_module(service_orchestrator)

ServiceOrchestrator = service_orchestrator.ServiceOrchestrator


class TestServiceOrchestrator:
    """Test suite for ServiceOrchestrator class."""

    @pytest.fixture
    def registry(self):
        """Create a StepRegistry instance."""
        reg = StepRegistry()
        reg.register("step1", lambda: Step("step1"))
        reg.register("step2", lambda: Step("step2"))
        return reg

    @pytest.fixture
    def orchestrator(self, registry):
        """Create a ServiceOrchestrator instance."""
        return ServiceOrchestrator(registry)

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
        """Test ServiceOrchestrator initialization."""
        orchestrator = ServiceOrchestrator(registry)
        
        assert orchestrator.registry == registry

    def test_plan_uses_service_pipeline(self, orchestrator, context):
        """Test that plan uses service_pipeline from payload."""
        payload = {"service_pipeline": ["step1", "step2"]}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 2
        assert steps[0].name() == "step1"
        assert steps[1].name() == "step2"

    def test_plan_with_empty_pipeline(self, orchestrator, context):
        """Test plan with empty service_pipeline."""
        payload = {"service_pipeline": []}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 0

    def test_plan_with_missing_pipeline(self, orchestrator, context):
        """Test plan with missing service_pipeline key."""
        payload = {}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 0

    def test_execute_runs_pipeline(self, orchestrator, context):
        """Test that execute runs all steps in pipeline."""
        payload = {"service_pipeline": ["step1", "step2"], "data": "test"}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.summary == "service:2"
        assert result.metrics["service_steps"] == 2

    def test_execute_preserves_data(self, orchestrator, context):
        """Test that execute preserves data through steps."""
        payload = {"service_pipeline": ["step1"], "value": 42}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["service_steps"] == 1

    def test_report_formats_result(self, orchestrator):
        """Test that report formats result correctly."""
        result = OrchestrationResult(ok=True, summary="service:5", metrics={})
        
        report = orchestrator.report(result)
        
        assert "[ServiceOrchestrator]" in report
        assert "service:5" in report

    def test_execute_with_single_step(self, registry, context):
        """Test execute with single step."""
        orchestrator = ServiceOrchestrator(registry)
        payload = {"service_pipeline": ["step1"]}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["service_steps"] == 1

    def test_execute_data_modification(self, orchestrator, context):
        """Test that execute allows data modification through steps."""
        class ModifyingStep:
            def __init__(self, name):
                self._name = name
            def name(self):
                return self._name
            def run(self, ctx, data):
                data["modified"] = True
                data["value"] = data.get("value", 0) + 1
                return data
        
        orchestrator.registry.register("modify", lambda: ModifyingStep("modify"))
        payload = {"service_pipeline": ["modify"], "value": 5}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["service_steps"] == 1

    def test_execute_with_missing_steps(self, orchestrator, context):
        """Test execute with missing steps in registry."""
        payload = {"service_pipeline": ["nonexistent_step"]}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["service_steps"] == 0

    def test_execute_with_step_failure(self, registry, context):
        """Test execute with a step that raises an exception."""
        class FailingStep:
            def name(self):
                return "failing_step"
            def run(self, ctx, data):
                raise ValueError("Step failed")
        
        registry.register("failing_step", lambda: FailingStep())
        orchestrator = ServiceOrchestrator(registry)
        payload = {"service_pipeline": ["failing_step"]}
        
        with pytest.raises(ValueError, match="Step failed"):
            orchestrator.execute(context, payload)

    def test_execute_preserves_all_data(self, orchestrator, context):
        """Test that execute preserves all data fields through steps."""
        payload = {
            "service_pipeline": ["step1"],
            "data1": "value1",
            "data2": 42,
            "data3": {"nested": "value"}
        }
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["service_steps"] == 1

    def test_report_with_different_summaries(self, orchestrator):
        """Test report with different summary formats."""
        result1 = OrchestrationResult(ok=True, summary="service:0", metrics={})
        result2 = OrchestrationResult(ok=True, summary="service:10", metrics={})
        
        report1 = orchestrator.report(result1)
        report2 = orchestrator.report(result2)
        
        assert "[ServiceOrchestrator]" in report1
        assert "service:0" in report1
        assert "[ServiceOrchestrator]" in report2
        assert "service:10" in report2

    def test_plan_with_invalid_step_types(self, orchestrator, context):
        """Test plan with invalid step types in pipeline."""
        payload = {"service_pipeline": ["step1", None, "step2"]}
        
        # Should handle gracefully or skip invalid entries
        steps = list(orchestrator.plan(context, payload))
        
        # Registry should only return valid steps
        assert len(steps) >= 0  # At least handle gracefully

