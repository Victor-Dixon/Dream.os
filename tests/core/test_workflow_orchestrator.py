"""
Unit tests for orchestration/workflow_orchestrator.py - HIGH PRIORITY

Tests WorkflowOrchestrator class functionality.
Note: Maps to OrchestrationCoreEngine or core_orchestrator.py.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Mock the engines module before importing
sys.modules['src.core.engines'] = MagicMock()
sys.modules['src.core.engines.contracts'] = MagicMock()

# Import using importlib to bypass __init__.py chain
import importlib.util

contracts_path = project_root / "src" / "core" / "engines" / "contracts.py"
spec = importlib.util.spec_from_file_location("contracts", contracts_path)
contracts = importlib.util.module_from_spec(spec)
contracts.__package__ = 'src.core.engines'
spec.loader.exec_module(contracts)

orchestration_engine_path = project_root / "src" / "core" / "engines" / "orchestration_core_engine.py"
spec = importlib.util.spec_from_file_location("orchestration_core_engine", orchestration_engine_path)
orchestration_core_engine = importlib.util.module_from_spec(spec)
orchestration_core_engine.__package__ = 'src.core.engines'
# Patch the contracts import in the module
orchestration_core_engine.contracts = contracts
spec.loader.exec_module(orchestration_core_engine)

OrchestrationCoreEngine = orchestration_core_engine.OrchestrationCoreEngine
EngineContext = contracts.EngineContext
EngineResult = contracts.EngineResult

# Alias for test purposes
WorkflowOrchestrator = OrchestrationCoreEngine


class TestWorkflowOrchestrator:
    """Test suite for WorkflowOrchestrator class."""

    @pytest.fixture
    def orchestrator(self):
        """Create a WorkflowOrchestrator instance."""
        return WorkflowOrchestrator()

    @pytest.fixture
    def context(self):
        """Create an EngineContext instance."""
        from src.core.engines.contracts import EngineContext
        return EngineContext(
            config={},
            logger=MagicMock(),
            metrics={"timestamp": 1234567890}
        )

    def test_initialization(self, orchestrator):
        """Test WorkflowOrchestrator initialization."""
        assert orchestrator.workflows == {}
        assert orchestrator.executions == []
        assert orchestrator.is_initialized is False

    def test_initialize_success(self, orchestrator, context):
        """Test initialize method."""
        result = orchestrator.initialize(context)
        
        assert result is True
        assert orchestrator.is_initialized is True
        context.logger.info.assert_called()

    def test_initialize_failure(self, orchestrator, context):
        """Test initialize with exception."""
        context.logger.info.side_effect = Exception("Init failed")
        
        result = orchestrator.initialize(context)
        
        assert result is False
        assert orchestrator.is_initialized is False

    def test_execute_orchestrate_operation(self, orchestrator, context):
        """Test execute with orchestrate operation."""
        orchestrator.initialize(context)
        
        payload = {
            "operation": "orchestrate",
            "operations": ["op1", "op2"]
        }
        
        result = orchestrator.execute(context, payload)
        
        assert result.success is True
        assert "orchestration_id" in result.data

    def test_execute_workflow_operation(self, orchestrator, context):
        """Test execute with execute_workflow operation."""
        orchestrator.initialize(context)
        
        payload = {
            "operation": "execute_workflow",
            "workflow_id": "workflow1",
            "steps": ["step1", "step2"]
        }
        
        result = orchestrator.execute(context, payload)
        
        assert result.success is True
        assert result.data["workflow_id"] == "workflow1"
        assert result.data["steps_executed"] == 2

    def test_execute_coordinate_operation(self, orchestrator, context):
        """Test execute with coordinate operation."""
        orchestrator.initialize(context)
        
        payload = {
            "operation": "coordinate",
            "components": ["comp1", "comp2"]
        }
        
        result = orchestrator.execute(context, payload)
        
        assert result.success is True
        assert "coordination_id" in result.data
        assert len(orchestrator.executions) > 0

    def test_execute_unknown_operation(self, orchestrator, context):
        """Test execute with unknown operation."""
        orchestrator.initialize(context)
        
        payload = {"operation": "unknown"}
        
        result = orchestrator.execute(context, payload)
        
        assert result.success is False
        assert "Unknown orchestration operation" in result.error

    def test_execute_exception_handling(self, orchestrator, context):
        """Test execute handles exceptions."""
        orchestrator.initialize(context)
        
        payload = {"operation": "orchestrate"}
        context.metrics = None  # Cause exception
        
        result = orchestrator.execute(context, payload)
        
        assert result.success is False
        assert result.error is not None

    def test_cleanup(self, orchestrator, context):
        """Test cleanup method."""
        orchestrator.initialize(context)
        orchestrator.workflows["w1"] = {}
        orchestrator.executions.append({})
        
        result = orchestrator.cleanup(context)
        
        assert result is True
        assert orchestrator.is_initialized is False
        assert len(orchestrator.workflows) == 0
        assert len(orchestrator.executions) == 0

    def test_cleanup_not_initialized(self, orchestrator, context):
        """Test cleanup when not initialized."""
        result = orchestrator.cleanup(context)
        
        assert result is True

    def test_get_status(self, orchestrator):
        """Test get_status method."""
        status = orchestrator.get_status()
        
        assert "initialized" in status
        assert "workflows_count" in status
        assert "executions_count" in status
        assert status["initialized"] is False

    def test_get_status_after_initialization(self, orchestrator, context):
        """Test get_status after initialization."""
        orchestrator.initialize(context)
        
        status = orchestrator.get_status()
        
        assert status["initialized"] is True

    def test_workflow_storage(self, orchestrator, context):
        """Test workflows are stored after execution."""
        orchestrator.initialize(context)
        
        payload = {
            "operation": "execute_workflow",
            "workflow_id": "test_workflow",
            "steps": ["step1"]
        }
        
        orchestrator.execute(context, payload)
        
        assert "test_workflow" in orchestrator.workflows

    def test_executions_tracking(self, orchestrator, context):
        """Test executions are tracked."""
        orchestrator.initialize(context)
        
        payload = {
            "operation": "coordinate",
            "components": ["comp1"]
        }
        
        orchestrator.execute(context, payload)
        
        assert len(orchestrator.executions) == 1

