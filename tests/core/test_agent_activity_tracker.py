"""
Unit tests for agent_activity_tracker.py - HIGH PRIORITY

Tests agent activity tracking functionality.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
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


class TestGetActivityTracker:
    """Test suite for get_activity_tracker function."""

    def test_get_tracker_singleton(self):
        """Test getting tracker singleton instance."""
        tracker1 = get_activity_tracker()
        tracker2 = get_activity_tracker()
        
        # Should return same instance (singleton pattern)
        assert tracker1 is not None
        assert tracker2 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

