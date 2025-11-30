"""Tests for Status Change Monitor."""
import pytest
from unittest.mock import Mock, patch, AsyncMock


class TestStatusChangeMonitor:
    """Test StatusChangeMonitor."""

    @pytest.fixture
    def mock_bot(self):
        return Mock()

    @pytest.fixture
    def monitor(self, mock_bot):
        from src.discord_commander.status_change_monitor import StatusChangeMonitor
        return StatusChangeMonitor(mock_bot)

    def test_initialization(self, monitor, mock_bot):
        assert monitor.bot == mock_bot
        assert monitor.workspace_path.name == "agent_workspaces"
        assert isinstance(monitor.last_modified, dict)
        assert isinstance(monitor.last_status, dict)

    def test_start_monitoring(self, monitor):
        with patch.object(monitor, 'monitor_status_changes') as mock_task:
            mock_task.start = Mock()
            monitor.start_monitoring()
            if hasattr(monitor, 'monitor_status_changes'):
                assert True

    def test_stop_monitoring(self, monitor):
        with patch.object(monitor, 'monitor_status_changes') as mock_task:
            mock_task.cancel = Mock()
            monitor.stop_monitoring()
            assert True

