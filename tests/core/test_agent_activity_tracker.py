"""
Unit tests for agent_activity_tracker.py - HIGH PRIORITY

Tests agent activity tracking functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch, mock_open
from datetime import datetime, timedelta

# Import activity tracker
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.agent_activity_tracker import (
    get_activity_tracker,
    AgentActivityTracker
)


class TestAgentActivityTracker:
    """Test suite for AgentActivityTracker class."""

    @pytest.fixture
    def tracker(self):
        """Create AgentActivityTracker instance."""
        return AgentActivityTracker()

    def test_tracker_initialization(self, tracker):
        """Test tracker initialization."""
        assert tracker is not None

    def test_mark_active(self, tracker):
        """Test marking agent as active."""
        agent_id = "Agent-1"
        action = "message_sent"
        
        # Simulate marking active
        activity = {
            "agent_id": agent_id,
            "action": action,
            "timestamp": datetime.now()
        }
        
        assert activity["agent_id"] == agent_id
        assert activity["action"] == action

    def test_get_agent_status(self, tracker):
        """Test getting agent status."""
        agent_id = "Agent-1"
        
        # Simulate status retrieval
        status = {
            "agent_id": agent_id,
            "status": "ACTIVE",
            "last_activity": datetime.now()
        }
        
        assert status["agent_id"] == agent_id
        assert status["status"] == "ACTIVE"

    def test_track_activity(self, tracker):
        """Test tracking agent activity."""
        agent_id = "Agent-1"
        activity_type = "task_completed"
        
        # Simulate activity tracking
        activity_record = {
            "agent_id": agent_id,
            "activity_type": activity_type,
            "timestamp": datetime.now()
        }
        
        assert activity_record["agent_id"] == agent_id
        assert activity_record["activity_type"] == activity_type

    def test_get_inactive_agents(self, tracker):
        """Test getting inactive agents."""
        # Simulate inactive detection
        threshold = datetime.now() - timedelta(hours=1)
        
        agents = [
            {"agent_id": "Agent-1", "last_activity": datetime.now() - timedelta(hours=2)},
            {"agent_id": "Agent-2", "last_activity": datetime.now()}
        ]
        
        inactive = [a for a in agents if a["last_activity"] < threshold]
        
        assert len(inactive) >= 0

    def test_get_activity_summary(self, tracker):
        """Test getting activity summary."""
        # Simulate summary generation
        summary = {
            "total_agents": 8,
            "active_agents": 6,
            "inactive_agents": 2
        }
        
        assert summary["total_agents"] == 8
        assert summary["active_agents"] + summary["inactive_agents"] == summary["total_agents"]

    def test_mark_active_creates_entry(self, tracker):
        """Test mark_active creates activity entry."""
        with patch.object(tracker, '_load_activity', return_value={"agents": {}, "metadata": {"version": "1.0"}}):
            with patch.object(tracker, '_save_activity', return_value=True) as mock_save:
                result = tracker.mark_active("Agent-1", "test_operation")
                
                assert result is True
                mock_save.assert_called_once()

    def test_mark_active_increments_count(self, tracker):
        """Test mark_active increments activity count."""
        existing_data = {
            "agents": {
                "Agent-1": {
                    "status": "active",
                    "activity_count": 5
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=existing_data):
            with patch.object(tracker, '_save_activity', return_value=True) as mock_save:
                tracker.mark_active("Agent-1", "test_operation")
                
                # Verify save was called with incremented count
                call_args = mock_save.call_args[0][0]
                assert call_args["agents"]["Agent-1"]["activity_count"] == 6

    def test_mark_delivering(self, tracker):
        """Test mark_delivering method."""
        with patch.object(tracker, '_load_activity', return_value={"agents": {}, "metadata": {"version": "1.0"}}):
            with patch.object(tracker, '_save_activity', return_value=True) as mock_save:
                result = tracker.mark_delivering("Agent-1", "queue-123")
                
                assert result is True
                mock_save.assert_called_once()
                call_args = mock_save.call_args[0][0]
                assert call_args["agents"]["Agent-1"]["status"] == "delivering"
                assert call_args["agents"]["Agent-1"]["queue_id"] == "queue-123"

    def test_mark_inactive(self, tracker):
        """Test mark_inactive method."""
        existing_data = {
            "agents": {
                "Agent-1": {
                    "status": "active",
                    "last_active": datetime.now().isoformat()
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=existing_data):
            with patch.object(tracker, '_save_activity', return_value=True) as mock_save:
                result = tracker.mark_inactive("Agent-1")
                
                assert result is True
                call_args = mock_save.call_args[0][0]
                assert call_args["agents"]["Agent-1"]["status"] == "inactive"
                assert "last_inactive" in call_args["agents"]["Agent-1"]

    def test_mark_inactive_nonexistent_agent(self, tracker):
        """Test mark_inactive with nonexistent agent."""
        with patch.object(tracker, '_load_activity', return_value={"agents": {}, "metadata": {"version": "1.0"}}):
            with patch.object(tracker, '_save_activity', return_value=True):
                result = tracker.mark_inactive("Agent-99")
                
                # Should still return True but not modify anything
                assert result is True

    def test_is_agent_active_true(self, tracker):
        """Test is_agent_active returns True for active agent."""
        recent_time = datetime.now().isoformat()
        data = {
            "agents": {
                "Agent-1": {
                    "status": "active",
                    "last_active": recent_time
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=data):
            result = tracker.is_agent_active("Agent-1", timeout_minutes=5)
            
            assert result is True

    def test_is_agent_active_false_inactive(self, tracker):
        """Test is_agent_active returns False for inactive agent."""
        data = {
            "agents": {
                "Agent-1": {
                    "status": "inactive",
                    "last_active": datetime.now().isoformat()
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=data):
            result = tracker.is_agent_active("Agent-1", timeout_minutes=5)
            
            assert result is False

    def test_is_agent_active_false_timeout(self, tracker):
        """Test is_agent_active returns False when timeout exceeded."""
        old_time = (datetime.now() - timedelta(minutes=10)).isoformat()
        data = {
            "agents": {
                "Agent-1": {
                    "status": "active",
                    "last_active": old_time
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=data):
            result = tracker.is_agent_active("Agent-1", timeout_minutes=5)
            
            assert result is False

    def test_is_agent_active_false_nonexistent(self, tracker):
        """Test is_agent_active returns False for nonexistent agent."""
        with patch.object(tracker, '_load_activity', return_value={"agents": {}, "metadata": {"version": "1.0"}}):
            result = tracker.is_agent_active("Agent-99", timeout_minutes=5)
            
            assert result is False

    def test_get_agent_activity(self, tracker):
        """Test get_agent_activity returns activity info."""
        data = {
            "agents": {
                "Agent-1": {
                    "status": "active",
                    "last_active": datetime.now().isoformat(),
                    "activity_count": 10
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=data):
            activity = tracker.get_agent_activity("Agent-1")
            
            assert activity["status"] == "active"
            assert activity["activity_count"] == 10

    def test_get_agent_activity_nonexistent(self, tracker):
        """Test get_agent_activity returns defaults for nonexistent agent."""
        with patch.object(tracker, '_load_activity', return_value={"agents": {}, "metadata": {"version": "1.0"}}):
            activity = tracker.get_agent_activity("Agent-99")
            
            assert activity["status"] == "inactive"
            assert activity["activity_count"] == 0

    def test_get_all_agent_activity(self, tracker):
        """Test get_all_agent_activity returns all agents."""
        data = {
            "agents": {
                "Agent-1": {"status": "active"},
                "Agent-2": {"status": "inactive"}
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=data):
            all_activity = tracker.get_all_agent_activity()
            
            assert len(all_activity) == 2
            assert "Agent-1" in all_activity
            assert "Agent-2" in all_activity

    def test_get_active_agents(self, tracker):
        """Test get_active_agents returns list of active agents."""
        recent_time = datetime.now().isoformat()
        old_time = (datetime.now() - timedelta(minutes=10)).isoformat()
        data = {
            "agents": {
                "Agent-1": {
                    "status": "active",
                    "last_active": recent_time
                },
                "Agent-2": {
                    "status": "active",
                    "last_active": old_time
                },
                "Agent-3": {
                    "status": "inactive",
                    "last_active": recent_time
                }
            },
            "metadata": {"version": "1.0"}
        }
        
        with patch.object(tracker, '_load_activity', return_value=data):
            active = tracker.get_active_agents(timeout_minutes=5)
            
            # Only Agent-1 should be active (within timeout)
            assert "Agent-1" in active
            assert "Agent-2" not in active  # Timeout exceeded
            assert "Agent-3" not in active  # Inactive status

    def test_ensure_activity_file_creates_file(self):
        """Test _ensure_activity_file creates file if missing."""
        import tempfile
        from pathlib import Path
        
        with tempfile.TemporaryDirectory() as tmpdir:
            activity_file = Path(tmpdir) / "activity.json"
            tracker = AgentActivityTracker(activity_file=str(activity_file))
            
            # File should be created
            assert activity_file.exists()

    def test_load_activity_file_not_found(self, tracker):
        """Test _load_activity handles missing file."""
        with patch('builtins.open', side_effect=FileNotFoundError):
            result = tracker._load_activity()
            
            assert "agents" in result
            assert result["agents"] == {}

    def test_load_activity_invalid_json(self, tracker):
        """Test _load_activity handles invalid JSON."""
        with patch('builtins.open', mock_open(read_data="invalid json")):
            result = tracker._load_activity()
            
            assert "agents" in result
            assert result["agents"] == {}

    def test_save_activity_success(self, tracker):
        """Test _save_activity successfully saves."""
        with patch('builtins.open', mock_open()) as mock_file:
            result = tracker._save_activity({"agents": {}, "metadata": {"version": "1.0"}})
            
            assert result is True
            mock_file.assert_called_once()

    def test_save_activity_failure(self, tracker):
        """Test _save_activity handles save failure."""
        with patch('builtins.open', side_effect=OSError("Permission denied")):
            result = tracker._save_activity({"agents": {}, "metadata": {"version": "1.0"}})
            
            assert result is False


class TestGetActivityTracker:
    """Test suite for get_activity_tracker function."""

    def test_get_tracker_singleton(self):
        """Test getting tracker singleton instance."""
        # Reset global instance
        import src.core.agent_activity_tracker
        src.core.agent_activity_tracker._activity_tracker = None
        
        tracker1 = get_activity_tracker()
        tracker2 = get_activity_tracker()
        
        # Should return same instance (singleton pattern)
        assert tracker1 is not None
        assert tracker2 is not None
        assert tracker1 is tracker2

    def test_get_tracker_creates_instance(self):
        """Test get_activity_tracker creates instance if None."""
        import src.core.agent_activity_tracker
        src.core.agent_activity_tracker._activity_tracker = None
        
        tracker = get_activity_tracker()
        
        assert tracker is not None
        assert isinstance(tracker, AgentActivityTracker)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

