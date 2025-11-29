"""
Tests for coordinator_models.py

Tests for coordinator data models, enums, and dataclasses.
"""

import pytest
from datetime import datetime
from src.core.coordinator_models import (
    CoordinationStatus,
    TargetType,
    Priority,
    CoordinationTarget,
    CoordinationResult,
    CoordinatorStatus,
    CoordinatorConfig,
)


class TestCoordinationStatus:
    """Tests for CoordinationStatus enum."""

    def test_enum_values(self):
        """Test enum has correct values."""
        assert CoordinationStatus.INITIALIZING.value == "initializing"
        assert CoordinationStatus.OPERATIONAL.value == "operational"
        assert CoordinationStatus.ERROR.value == "error"
        assert CoordinationStatus.SHUTDOWN.value == "shutdown"

    def test_enum_membership(self):
        """Test enum membership."""
        assert CoordinationStatus.INITIALIZING in CoordinationStatus
        assert CoordinationStatus.OPERATIONAL in CoordinationStatus


class TestTargetType:
    """Tests for TargetType enum."""

    def test_enum_values(self):
        """Test enum has correct values."""
        assert TargetType.TASK.value == "task"
        assert TargetType.RESOURCE.value == "resource"
        assert TargetType.SERVICE.value == "service"
        assert TargetType.AGENT.value == "agent"
        assert TargetType.SYSTEM.value == "system"


class TestPriority:
    """Tests for Priority enum."""

    def test_enum_values(self):
        """Test enum has correct numeric values."""
        assert Priority.LOW.value == 1
        assert Priority.MEDIUM.value == 2
        assert Priority.HIGH.value == 3
        assert Priority.CRITICAL.value == 4

    def test_priority_ordering(self):
        """Test priority ordering."""
        assert Priority.LOW.value < Priority.MEDIUM.value
        assert Priority.MEDIUM.value < Priority.HIGH.value
        assert Priority.HIGH.value < Priority.CRITICAL.value


class TestCoordinationTarget:
    """Tests for CoordinationTarget dataclass."""

    def test_creation_with_valid_data(self):
        """Test creating target with valid data."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.HIGH,
            status=CoordinationStatus.OPERATIONAL,
        )
        assert target.target_id == "test-123"
        assert target.target_type == TargetType.TASK
        assert target.priority == Priority.HIGH
        assert target.status == CoordinationStatus.OPERATIONAL
        assert isinstance(target.created_at, datetime)
        assert isinstance(target.updated_at, datetime)
        assert target.metadata == {}

    def test_creation_with_empty_id_raises_error(self):
        """Test creating target with empty ID raises ValueError."""
        with pytest.raises(ValueError, match="Target ID cannot be empty"):
            CoordinationTarget(
                target_id="",
                target_type=TargetType.TASK,
                priority=Priority.LOW,
                status=CoordinationStatus.INITIALIZING,
            )

    def test_post_init_converts_string_target_type(self):
        """Test post_init converts string target_type."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type="task",
            priority=Priority.LOW,
            status=CoordinationStatus.OPERATIONAL,
        )
        assert target.target_type == TargetType.TASK

    def test_post_init_converts_int_priority(self):
        """Test post_init converts int priority."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=2,
            status=CoordinationStatus.OPERATIONAL,
        )
        assert target.priority == Priority.MEDIUM

    def test_post_init_converts_string_status(self):
        """Test post_init converts string status."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.LOW,
            status="operational",
        )
        assert target.status == CoordinationStatus.OPERATIONAL

    def test_update_metadata(self):
        """Test updating metadata."""
        import time
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.LOW,
            status=CoordinationStatus.OPERATIONAL,
        )
        old_updated = target.updated_at
        time.sleep(0.01)  # Small delay to ensure timestamp difference
        target.update_metadata({"key": "value"})
        assert target.metadata == {"key": "value"}
        assert target.updated_at >= old_updated

    def test_is_active_operational(self):
        """Test is_active returns True for operational status."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.LOW,
            status=CoordinationStatus.OPERATIONAL,
        )
        assert target.is_active() is True

    def test_is_active_non_operational(self):
        """Test is_active returns False for non-operational status."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.LOW,
            status=CoordinationStatus.ERROR,
        )
        assert target.is_active() is False

    def test_to_dict(self):
        """Test converting target to dictionary."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.HIGH,
            status=CoordinationStatus.OPERATIONAL,
            metadata={"key": "value"},
        )
        result = target.to_dict()
        assert result["target_id"] == "test-123"
        assert result["target_type"] == "task"
        assert result["priority"] == 3
        assert result["status"] == "operational"
        assert result["metadata"] == {"key": "value"}
        assert "created_at" in result
        assert "updated_at" in result


class TestCoordinationResult:
    """Tests for CoordinationResult dataclass."""

    def test_creation_with_success(self):
        """Test creating result with success."""
        result = CoordinationResult(
            success=True,
            operation="test_op",
            result="test_result",
        )
        assert result.success is True
        assert result.operation == "test_op"
        assert result.result == "test_result"
        assert result.error is None
        assert isinstance(result.timestamp, datetime)
        assert result.coordinator == ""
        assert result.metadata == {}

    def test_creation_with_error(self):
        """Test creating result with error."""
        result = CoordinationResult(
            success=False,
            operation="test_op",
            error="test_error",
            coordinator="test_coordinator",
        )
        assert result.success is False
        assert result.operation == "test_op"
        assert result.error == "test_error"
        assert result.coordinator == "test_coordinator"

    def test_to_dict_success(self):
        """Test converting success result to dictionary."""
        result = CoordinationResult(
            success=True,
            operation="test_op",
            result="test_result",
            coordinator="test_coord",
        )
        data = result.to_dict()
        assert data["success"] is True
        assert data["operation"] == "test_op"
        assert data["result"] == "test_result"
        assert data["error"] is None
        assert data["coordinator"] == "test_coord"
        assert "timestamp" in data

    def test_to_dict_error(self):
        """Test converting error result to dictionary."""
        result = CoordinationResult(
            success=False,
            operation="test_op",
            error="test_error",
        )
        data = result.to_dict()
        assert data["success"] is False
        assert data["operation"] == "test_op"
        assert data["error"] == "test_error"
        assert data["result"] is None


class TestCoordinatorStatus:
    """Tests for CoordinatorStatus dataclass."""

    def test_creation(self):
        """Test creating coordinator status."""
        status = CoordinatorStatus(
            name="test_coordinator",
            initialized=True,
            coordination_status=CoordinationStatus.OPERATIONAL,
            config={"key": "value"},
            start_time=datetime.now(),
            uptime_seconds=100.5,
            operations_count=50,
            error_count=2,
            success_rate=0.96,
            targets_count=10,
            targets_by_type={"task": 5, "resource": 5},
            status="operational",
        )
        assert status.name == "test_coordinator"
        assert status.initialized is True
        assert status.coordination_status == CoordinationStatus.OPERATIONAL
        assert status.config == {"key": "value"}
        assert status.uptime_seconds == 100.5
        assert status.operations_count == 50
        assert status.error_count == 2
        assert status.success_rate == 0.96
        assert status.targets_count == 10

    def test_to_dict(self):
        """Test converting status to dictionary."""
        start_time = datetime.now()
        status = CoordinatorStatus(
            name="test_coordinator",
            initialized=True,
            coordination_status=CoordinationStatus.OPERATIONAL,
            config={"key": "value"},
            start_time=start_time,
            uptime_seconds=100.5,
            operations_count=50,
            error_count=2,
            success_rate=0.96,
            targets_count=10,
            targets_by_type={"task": 5},
            status="operational",
        )
        data = status.to_dict()
        assert data["name"] == "test_coordinator"
        assert data["initialized"] is True
        assert data["coordination_status"] == "operational"
        assert data["config"] == {"key": "value"}
        assert data["uptime_seconds"] == 100.5
        assert data["operations_count"] == 50
        assert data["error_count"] == 2
        assert data["success_rate"] == 0.96
        assert data["targets_count"] == 10
        assert data["targets_by_type"] == {"task": 5}
        assert data["status"] == "operational"


class TestCoordinatorConfig:
    """Tests for CoordinatorConfig dataclass."""

    def test_creation_with_defaults(self):
        """Test creating config with defaults."""
        config = CoordinatorConfig(name="test_coordinator")
        assert config.name == "test_coordinator"
        assert config.config == {}
        assert config.max_targets == 1000
        assert config.operation_timeout == 30.0
        assert config.retry_attempts == 3
        assert config.enable_logging is True
        assert config.enable_metrics is True

    def test_creation_with_custom_values(self):
        """Test creating config with custom values."""
        config = CoordinatorConfig(
            name="test_coordinator",
            config={"key": "value"},
            max_targets=500,
            operation_timeout=60.0,
            retry_attempts=5,
            enable_logging=False,
            enable_metrics=False,
        )
        assert config.name == "test_coordinator"
        assert config.config == {"key": "value"}
        assert config.max_targets == 500
        assert config.operation_timeout == 60.0
        assert config.retry_attempts == 5
        assert config.enable_logging is False
        assert config.enable_metrics is False

    def test_creation_with_empty_name_raises_error(self):
        """Test creating config with empty name raises ValueError."""
        with pytest.raises(ValueError, match="Coordinator name cannot be empty"):
            CoordinatorConfig(name="")

    def test_creation_with_zero_max_targets_raises_error(self):
        """Test creating config with zero max_targets raises ValueError."""
        with pytest.raises(ValueError, match="Max targets must be positive"):
            CoordinatorConfig(name="test", max_targets=0)

    def test_creation_with_negative_max_targets_raises_error(self):
        """Test creating config with negative max_targets raises ValueError."""
        with pytest.raises(ValueError, match="Max targets must be positive"):
            CoordinatorConfig(name="test", max_targets=-1)

    def test_creation_with_zero_timeout_raises_error(self):
        """Test creating config with zero timeout raises ValueError."""
        with pytest.raises(ValueError, match="Operation timeout must be positive"):
            CoordinatorConfig(name="test", operation_timeout=0.0)

    def test_creation_with_negative_timeout_raises_error(self):
        """Test creating config with negative timeout raises ValueError."""
        with pytest.raises(ValueError, match="Operation timeout must be positive"):
            CoordinatorConfig(name="test", operation_timeout=-1.0)

    def test_creation_with_negative_retry_attempts_raises_error(self):
        """Test creating config with negative retry_attempts raises ValueError."""
        with pytest.raises(ValueError, match="Retry attempts cannot be negative"):
            CoordinatorConfig(name="test", retry_attempts=-1)

    def test_get_existing_key(self):
        """Test getting existing config key."""
        config = CoordinatorConfig(name="test", config={"key": "value"})
        assert config.get("key") == "value"

    def test_get_missing_key_with_default(self):
        """Test getting missing config key with default."""
        config = CoordinatorConfig(name="test", config={})
        assert config.get("missing", "default") == "default"

    def test_get_missing_key_without_default(self):
        """Test getting missing config key without default."""
        config = CoordinatorConfig(name="test", config={})
        assert config.get("missing") is None

    def test_update_config(self):
        """Test updating configuration."""
        config = CoordinatorConfig(name="test", config={"key": "value"})
        config.update({"new_key": "new_value"})
        assert config.config == {"key": "value", "new_key": "new_value"}

    def test_validate_valid_config(self):
        """Test validating valid config."""
        config = CoordinatorConfig(name="test")
        assert config.validate() is True

    def test_validate_invalid_config(self):
        """Test validating invalid config."""
        # Create valid config first
        config = CoordinatorConfig(name="test", max_targets=100)
        # Modify to invalid value after creation
        config.max_targets = 0
        # validate() should catch the ValueError and return False
        assert config.validate() is False

    def test_coordination_target_metadata_initialization(self):
        """Test CoordinationTarget metadata initialization."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.LOW,
            status=CoordinationStatus.OPERATIONAL,
            metadata={"initial": "value"},
        )
        assert target.metadata == {"initial": "value"}

    def test_coordination_target_update_metadata_multiple_times(self):
        """Test updating metadata multiple times."""
        target = CoordinationTarget(
            target_id="test-123",
            target_type=TargetType.TASK,
            priority=Priority.LOW,
            status=CoordinationStatus.OPERATIONAL,
        )
        target.update_metadata({"key1": "value1"})
        target.update_metadata({"key2": "value2"})
        assert target.metadata == {"key1": "value1", "key2": "value2"}

    def test_coordination_result_with_metadata(self):
        """Test CoordinationResult with metadata."""
        result = CoordinationResult(
            success=True,
            operation="test_op",
            metadata={"key": "value"},
        )
        assert result.metadata == {"key": "value"}

    def test_coordination_result_timestamp_auto_generated(self):
        """Test CoordinationResult timestamp is auto-generated."""
        import time
        before = datetime.now()
        time.sleep(0.01)  # Small delay
        result = CoordinationResult(
            success=True,
            operation="test_op",
        )
        time.sleep(0.01)
        after = datetime.now()
        assert before <= result.timestamp <= after

    def test_coordinator_config_get_nested_key(self):
        """Test getting nested config key."""
        config = CoordinatorConfig(
            name="test",
            config={"nested": {"key": "value"}},
        )
        assert config.get("nested") == {"key": "value"}

    def test_coordinator_config_update_overwrites_existing(self):
        """Test updating config overwrites existing keys."""
        config = CoordinatorConfig(
            name="test",
            config={"key": "old_value"},
        )
        config.update({"key": "new_value"})
        assert config.config["key"] == "new_value"

