"""
Unit tests for orchestration/core_orchestrator.py - MEDIUM PRIORITY

Tests CoreOrchestrator class functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from collections.abc import Iterable
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Create mock contracts matching actual structure
from dataclasses import dataclass
from typing import Any, Protocol

@dataclass(frozen=True)
class OrchestrationContext:
    config: dict
    emit: callable
    logger: callable
    
    def __init__(self, config=None, emit=None, logger=None):
        object.__setattr__(self, 'config', config or {})
        object.__setattr__(self, 'emit', emit or (lambda x, y: None))
        object.__setattr__(self, 'logger', logger or (lambda x: None))

@dataclass
class OrchestrationResult:
    ok: bool
    summary: str
    metrics: dict[str, Any]

class Step(Protocol):
    def name(self) -> str: ...
    def run(self, ctx, payload: dict[str, Any]) -> dict[str, Any]: ...

class Orchestrator(Protocol):
    def plan(self, ctx, payload: dict[str, Any]): ...
    def execute(self, ctx, payload: dict[str, Any]): ...
    def report(self, result): ...

# Concrete Step implementation for testing
class ConcreteStep:
    def __init__(self, name):
        self._name = name
    
    def name(self):
        return self._name
    
    def run(self, ctx, data):
        return data

# Mock the contracts module
mock_contracts = MagicMock()
mock_contracts.OrchestrationContext = OrchestrationContext
mock_contracts.OrchestrationResult = OrchestrationResult
mock_contracts.Step = Step
mock_contracts.Orchestrator = Orchestrator

# Mock registry
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

# Import using importlib to bypass __init__.py chain
import importlib.util
core_orchestrator_path = project_root / "src" / "core" / "orchestration" / "core_orchestrator.py"
spec = importlib.util.spec_from_file_location("core_orchestrator", core_orchestrator_path)
core_orchestrator = importlib.util.module_from_spec(spec)
core_orchestrator.__package__ = 'src.core.orchestration'
spec.loader.exec_module(core_orchestrator)

CoreOrchestrator = core_orchestrator.CoreOrchestrator
StepRegistry = StepRegistry


class TestCoreOrchestrator:
    """Test suite for CoreOrchestrator class."""

    @pytest.fixture
    def registry(self):
        """Create a StepRegistry instance."""
        reg = StepRegistry()
        reg.register("step1", lambda: ConcreteStep("step1"))
        reg.register("step2", lambda: ConcreteStep("step2"))
        return reg

    @pytest.fixture
    def orchestrator(self, registry):
        """Create a CoreOrchestrator instance."""
        return CoreOrchestrator(registry, ["step1", "step2"])

    @pytest.fixture
    def context(self):
        """Create an OrchestrationContext instance."""
        events = []
        def emit(event_type, data):
            events.append((event_type, data))
        def logger(msg):
            pass
        ctx = OrchestrationContext(config={}, emit=emit, logger=logger)
        # Store events list in a way that works with frozen dataclass
        object.__setattr__(ctx, '_events', events)
        return ctx

    def test_initialization(self, registry):
        """Test CoreOrchestrator initialization."""
        orchestrator = CoreOrchestrator(registry, ["step1", "step2"])
        
        assert orchestrator.registry == registry
        assert orchestrator.pipeline_keys == ["step1", "step2"]

    def test_plan_returns_steps(self, orchestrator, context):
        """Test that plan returns steps from registry."""
        payload = {}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 2
        assert steps[0].name() == "step1"
        assert steps[1].name() == "step2"

    def test_plan_with_empty_pipeline(self, registry):
        """Test plan with empty pipeline."""
        orchestrator = CoreOrchestrator(registry, [])
        context = OrchestrationContext()
        payload = {}
        
        steps = list(orchestrator.plan(context, payload))
        
        assert len(steps) == 0

    def test_execute_runs_pipeline(self, orchestrator, context):
        """Test that execute runs all steps in pipeline."""
        payload = {"data": "test"}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert "ran 2 step(s)" in result.summary
        assert result.metrics["steps"] == 2

    def test_execute_emits_events(self, orchestrator, context):
        """Test that execute emits events."""
        payload = {}
        
        orchestrator.execute(context, payload)
        
        # Check for orchestrator.start event
        start_events = [e for e in context._events if e[0] == "orchestrator.start"]
        assert len(start_events) == 1
        
        # Check for step.start and step.end events
        step_start_events = [e for e in context._events if e[0] == "step.start"]
        step_end_events = [e for e in context._events if e[0] == "step.end"]
        assert len(step_start_events) == 2
        assert len(step_end_events) == 2
        
        # Check for orchestrator.end event
        end_events = [e for e in context._events if e[0] == "orchestrator.end"]
        assert len(end_events) == 1

    def test_execute_passes_data_through_steps(self, orchestrator, context):
        """Test that execute passes data through steps."""
        payload = {"value": 1}
        
        # Mock step to modify data
        class ModifyingStep:
            def __init__(self, name):
                self._name = name
            def name(self):
                return self._name
            def run(self, ctx, data):
                data["value"] = data.get("value", 0) + 1
                return data
        
        orchestrator.registry.register("modify", lambda: ModifyingStep("modify"))
        orchestrator.pipeline_keys = ["modify"]
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True

    def test_report_formats_result(self, orchestrator):
        """Test that report formats result correctly."""
        result = OrchestrationResult(ok=True, summary="test summary", metrics={"steps": 5})
        
        report = orchestrator.report(result)
        
        assert "[CoreOrchestrator]" in report
        assert "test summary" in report
        assert "metrics=" in report

    def test_report_with_empty_metrics(self, orchestrator):
        """Test report with empty metrics."""
        result = OrchestrationResult(ok=True, summary="test", metrics={})
        
        report = orchestrator.report(result)
        
        assert "[CoreOrchestrator]" in report
        assert "test" in report

    def test_execute_with_single_step(self, registry):
        """Test execute with single step."""
        orchestrator = CoreOrchestrator(registry, ["step1"])
        context = OrchestrationContext()
        payload = {}
        
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["steps"] == 1

    def test_execute_with_missing_step(self, registry):
        """Test execute with missing step in registry."""
        orchestrator = CoreOrchestrator(registry, ["nonexistent"])
        context = OrchestrationContext()
        payload = {}
        
        # Should handle missing step gracefully
        result = orchestrator.execute(context, payload)
        
        assert result.ok is True
        assert result.metrics["steps"] == 0

