"""
Unit tests for src/core/ssot/ssot_models.py - SSOT Models

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-27
"""

import pytest
from datetime import datetime

from src.core.ssot.ssot_models import (
    SSOTComponentType,
    SSOTExecutionPhase,
    SSOTValidationLevel,
    SSOTComponent,
    SSOTIntegrationResult,
    SSOTExecutionTask,
    SSOTValidationReport,
    SSOTMetrics,
)


class TestSSOTEnums:
    """Test SSOT enum types."""

    def test_ssot_component_type_enum(self):
        """Test SSOTComponentType enum values."""
        assert SSOTComponentType.LOGGING.value == "logging"
        assert SSOTComponentType.CONFIGURATION.value == "configuration"
        assert SSOTComponentType.INTERFACE.value == "interface"
        assert SSOTComponentType.MESSAGING.value == "messaging"
        assert SSOTComponentType.FILE_LOCKING.value == "file_locking"
        assert SSOTComponentType.VALIDATION.value == "validation"
        assert SSOTComponentType.EXECUTION.value == "execution"

    def test_ssot_execution_phase_enum(self):
        """Test SSOTExecutionPhase enum values."""
        assert SSOTExecutionPhase.INITIALIZATION.value == "initialization"
        assert SSOTExecutionPhase.VALIDATION.value == "validation"
        assert SSOTExecutionPhase.EXECUTION.value == "execution"
        assert SSOTExecutionPhase.COORDINATION.value == "coordination"
        assert SSOTExecutionPhase.COMPLETION.value == "completion"

    def test_ssot_validation_level_enum(self):
        """Test SSOTValidationLevel enum values."""
        assert SSOTValidationLevel.BASIC.value == "basic"
        assert SSOTValidationLevel.COMPREHENSIVE.value == "comprehensive"
        assert SSOTValidationLevel.STRESS.value == "stress"
        assert SSOTValidationLevel.INTEGRATION.value == "integration"


class TestSSOTComponent:
    """Test SSOTComponent dataclass."""

    def test_ssot_component_creation(self):
        """Test creating SSOTComponent."""
        component = SSOTComponent(
            component_id="test-1",
            component_type=SSOTComponentType.CONFIGURATION,
            name="Test Component",
            description="Test description"
        )
        assert component.component_id == "test-1"
        assert component.component_type == SSOTComponentType.CONFIGURATION
        assert component.name == "Test Component"
        assert component.description == "Test description"

    def test_ssot_component_defaults(self):
        """Test SSOTComponent with default values."""
        component = SSOTComponent(
            component_id="test-2",
            component_type=SSOTComponentType.MESSAGING,
            name="Test Component 2"
        )
        assert component.dependencies == []
        assert component.metadata == {}
        assert isinstance(component.created_at, datetime)

    def test_ssot_component_to_dict(self):
        """Test SSOTComponent.to_dict() method."""
        component = SSOTComponent(
            component_id="test-3",
            component_type=SSOTComponentType.VALIDATION,
            name="Test Component 3",
            dependencies=["dep-1", "dep-2"],
            metadata={"key": "value"}
        )
        result = component.to_dict()
        assert isinstance(result, dict)
        assert result["component_id"] == "test-3"
        assert result["component_type"] == "validation"
        assert result["name"] == "Test Component 3"
        assert result["dependencies"] == ["dep-1", "dep-2"]
        assert result["metadata"] == {"key": "value"}


class TestSSOTIntegrationResult:
    """Test SSOTIntegrationResult dataclass."""

    def test_ssot_integration_result_creation(self):
        """Test creating SSOTIntegrationResult."""
        result = SSOTIntegrationResult(
            component_id="test-1",
            success=True,
            execution_time=1.5
        )
        assert result.component_id == "test-1"
        assert result.success is True
        assert result.execution_time == 1.5
        assert result.error_message is None

    def test_ssot_integration_result_with_error(self):
        """Test SSOTIntegrationResult with error."""
        result = SSOTIntegrationResult(
            component_id="test-2",
            success=False,
            error_message="Test error"
        )
        assert result.success is False
        assert result.error_message == "Test error"

    def test_ssot_integration_result_to_dict(self):
        """Test SSOTIntegrationResult.to_dict() method."""
        result = SSOTIntegrationResult(
            component_id="test-3",
            success=True,
            execution_time=2.5,
            validation_results={"test": "passed"},
            performance_metrics={"cpu": 50.0}
        )
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["component_id"] == "test-3"
        assert result_dict["success"] is True
        assert result_dict["execution_time"] == 2.5
        assert result_dict["validation_results"] == {"test": "passed"}
        assert result_dict["performance_metrics"] == {"cpu": 50.0}


class TestSSOTExecutionTask:
    """Test SSOTExecutionTask dataclass."""

    def test_ssot_execution_task_creation(self):
        """Test creating SSOTExecutionTask."""
        task = SSOTExecutionTask(
            task_id="task-1",
            component_id="comp-1",
            phase=SSOTExecutionPhase.EXECUTION
        )
        assert task.task_id == "task-1"
        assert task.component_id == "comp-1"
        assert task.phase == SSOTExecutionPhase.EXECUTION
        assert task.status == "pending"
        assert task.retry_count == 0
        assert task.max_retries == 3

    def test_ssot_execution_task_defaults(self):
        """Test SSOTExecutionTask with default values."""
        task = SSOTExecutionTask(
            task_id="task-2",
            component_id="comp-2",
            phase=SSOTExecutionPhase.VALIDATION
        )
        assert task.dependencies == []
        assert task.priority == 1
        assert task.timeout_seconds == 300
        assert isinstance(task.created_at, datetime)
        assert task.started_at is None
        assert task.completed_at is None

    def test_ssot_execution_task_to_dict(self):
        """Test SSOTExecutionTask.to_dict() method."""
        task = SSOTExecutionTask(
            task_id="task-3",
            component_id="comp-3",
            phase=SSOTExecutionPhase.COORDINATION,
            dependencies=["dep-1"],
            priority=2
        )
        result = task.to_dict()
        assert isinstance(result, dict)
        assert result["task_id"] == "task-3"
        assert result["component_id"] == "comp-3"
        assert result["phase"] == "coordination"
        assert result["dependencies"] == ["dep-1"]
        assert result["priority"] == 2


class TestSSOTValidationReport:
    """Test SSOTValidationReport dataclass."""

    def test_ssot_validation_report_creation(self):
        """Test creating SSOTValidationReport."""
        report = SSOTValidationReport(
            report_id="report-1",
            component_id="comp-1",
            validation_level=SSOTValidationLevel.BASIC
        )
        assert report.report_id == "report-1"
        assert report.component_id == "comp-1"
        assert report.validation_level == SSOTValidationLevel.BASIC
        assert report.results == []
        assert report.summary == {}
        assert report.recommendations == []

    def test_ssot_validation_report_to_dict(self):
        """Test SSOTValidationReport.to_dict() method."""
        result = SSOTIntegrationResult(
            component_id="comp-1",
            success=True,
            execution_time=1.0
        )
        report = SSOTValidationReport(
            report_id="report-2",
            component_id="comp-2",
            validation_level=SSOTValidationLevel.COMPREHENSIVE,
            results=[result],
            summary={"total": 1, "passed": 1},
            recommendations=["Recommendation 1"]
        )
        result_dict = report.to_dict()
        assert isinstance(result_dict, dict)
        assert result_dict["report_id"] == "report-2"
        assert result_dict["validation_level"] == "comprehensive"
        assert len(result_dict["results"]) == 1
        assert result_dict["summary"] == {"total": 1, "passed": 1}
        assert result_dict["recommendations"] == ["Recommendation 1"]


class TestSSOTMetrics:
    """Test SSOTMetrics class."""

    def test_ssot_metrics_initialization(self):
        """Test SSOTMetrics initialization."""
        metrics = SSOTMetrics()
        assert metrics.total_components == 0
        assert metrics.total_tasks == 0
        assert metrics.completed_tasks == 0
        assert metrics.failed_tasks == 0
        assert metrics.average_execution_time == 0.0
        assert metrics.validation_reports_generated == 0

    def test_ssot_metrics_record_component_registration(self):
        """Test recording component registration."""
        metrics = SSOTMetrics()
        metrics.record_component_registration()
        assert metrics.total_components == 1
        metrics.record_component_registration()
        assert metrics.total_components == 2

    def test_ssot_metrics_record_task_creation(self):
        """Test recording task creation."""
        metrics = SSOTMetrics()
        metrics.record_task_creation()
        assert metrics.total_tasks == 1
        metrics.record_task_creation()
        assert metrics.total_tasks == 2

    def test_ssot_metrics_record_task_completion_success(self):
        """Test recording successful task completion."""
        metrics = SSOTMetrics()
        metrics.record_task_creation()
        metrics.record_task_completion(success=True, execution_time=1.5)
        assert metrics.completed_tasks == 1
        assert metrics.failed_tasks == 0
        assert metrics.average_execution_time == 1.5

    def test_ssot_metrics_record_task_completion_failure(self):
        """Test recording failed task completion."""
        metrics = SSOTMetrics()
        metrics.record_task_creation()
        metrics.record_task_completion(success=False, execution_time=0.5)
        assert metrics.completed_tasks == 0
        assert metrics.failed_tasks == 1
        assert metrics.average_execution_time == 0.5

    def test_ssot_metrics_average_execution_time(self):
        """Test average execution time calculation."""
        metrics = SSOTMetrics()
        metrics.record_task_creation()
        metrics.record_task_creation()
        metrics.record_task_completion(success=True, execution_time=1.0)
        metrics.record_task_completion(success=True, execution_time=3.0)
        assert metrics.average_execution_time == 2.0

    def test_ssot_metrics_record_report_generation(self):
        """Test recording report generation."""
        metrics = SSOTMetrics()
        metrics.record_report_generation()
        assert metrics.validation_reports_generated == 1
        metrics.record_report_generation()
        assert metrics.validation_reports_generated == 2

    def test_ssot_metrics_to_dict(self):
        """Test SSOTMetrics.to_dict() method."""
        metrics = SSOTMetrics()
        metrics.record_component_registration()
        metrics.record_task_creation()
        metrics.record_task_creation()
        metrics.record_task_completion(success=True, execution_time=1.0)
        metrics.record_report_generation()
        
        result = metrics.to_dict()
        assert isinstance(result, dict)
        assert result["total_components"] == 1
        assert result["total_tasks"] == 2
        assert result["completed_tasks"] == 1
        assert result["failed_tasks"] == 0
        assert result["average_execution_time"] == 1.0
        assert result["validation_reports_generated"] == 1
        assert "success_rate" in result
        assert result["success_rate"] == 50.0

