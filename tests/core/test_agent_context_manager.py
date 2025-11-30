#!/usr/bin/env python3
"""
Unit tests for agent_context_manager.py - Infrastructure Test Coverage

Tests AgentContextManager class and context management operations.
Target: ≥85% coverage, comprehensive test methods.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Date: 2025-01-27
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.agent_context_manager import AgentContextManager


class TestAgentContextManager:
    """Test suite for AgentContextManager class."""

    @pytest.fixture
    def manager(self):
        """Create AgentContextManager instance."""
        return AgentContextManager()

    def test_initialization(self, manager):
        """Test manager initialization."""
        assert manager is not None
        assert manager._contexts == {}
        assert "created_at" in manager._metadata
        assert manager._metadata["version"] == "1.0.0"

    def test_set_agent_context_success(self, manager):
        """Test setting context for an agent successfully."""
        context = {"mission": "test mission", "status": "active"}
        result = manager.set_agent_context("Agent-1", context)
        
        assert result is True
        assert "Agent-1" in manager._contexts
        assert manager._contexts["Agent-1"]["mission"] == "test mission"
        assert manager._contexts["Agent-1"]["status"] == "active"
        assert "updated_at" in manager._contexts["Agent-1"]
        assert manager._contexts["Agent-1"]["agent_id"] == "Agent-1"

    def test_set_agent_context_multiple_agents(self, manager):
        """Test setting context for multiple agents."""
        manager.set_agent_context("Agent-1", {"mission": "mission1"})
        manager.set_agent_context("Agent-2", {"mission": "mission2"})
        
        assert len(manager._contexts) == 2
        assert manager._contexts["Agent-1"]["mission"] == "mission1"
        assert manager._contexts["Agent-2"]["mission"] == "mission2"

    def test_get_agent_context_existing(self, manager):
        """Test getting context for existing agent."""
        context = {"mission": "test", "priority": "high"}
        manager.set_agent_context("Agent-1", context)
        
        retrieved = manager.get_agent_context("Agent-1")
        assert retrieved is not None
        assert retrieved["mission"] == "test"
        assert retrieved["priority"] == "high"
        assert "updated_at" in retrieved

    def test_get_agent_context_nonexistent(self, manager):
        """Test getting context for non-existent agent."""
        result = manager.get_agent_context("Agent-999")
        assert result is None

    def test_update_agent_context_success(self, manager):
        """Test updating existing agent context."""
        manager.set_agent_context("Agent-1", {"mission": "old mission"})
        original_updated = manager._contexts["Agent-1"]["updated_at"]
        
        # Wait a tiny bit to ensure timestamp changes
        import time
        time.sleep(0.01)
        
        result = manager.update_agent_context("Agent-1", {"mission": "new mission", "priority": "high"})
        
        assert result is True
        assert manager._contexts["Agent-1"]["mission"] == "new mission"
        assert manager._contexts["Agent-1"]["priority"] == "high"
        assert manager._contexts["Agent-1"]["updated_at"] != original_updated

    def test_update_agent_context_nonexistent(self, manager):
        """Test updating context for non-existent agent."""
        result = manager.update_agent_context("Agent-999", {"mission": "new"})
        assert result is False

    def test_remove_agent_context_success(self, manager):
        """Test removing agent context successfully."""
        manager.set_agent_context("Agent-1", {"mission": "test"})
        assert "Agent-1" in manager._contexts
        
        result = manager.remove_agent_context("Agent-1")
        assert result is True
        assert "Agent-1" not in manager._contexts

    def test_remove_agent_context_nonexistent(self, manager):
        """Test removing context for non-existent agent."""
        result = manager.remove_agent_context("Agent-999")
        assert result is False

    def test_list_agents_empty(self, manager):
        """Test listing agents when no contexts exist."""
        agents = manager.list_agents()
        assert agents == []

    def test_list_agents_multiple(self, manager):
        """Test listing multiple agents."""
        manager.set_agent_context("Agent-1", {})
        manager.set_agent_context("Agent-2", {})
        manager.set_agent_context("Agent-3", {})
        
        agents = manager.list_agents()
        assert len(agents) == 3
        assert "Agent-1" in agents
        assert "Agent-2" in agents
        assert "Agent-3" in agents

    def test_agent_contexts_property(self, manager):
        """Test agent_contexts property."""
        manager.set_agent_context("Agent-1", {"mission": "test"})
        manager.set_agent_context("Agent-2", {"status": "active"})
        
        contexts = manager.agent_contexts
        assert isinstance(contexts, dict)
        assert "Agent-1" in contexts
        assert "Agent-2" in contexts
        assert contexts["Agent-1"]["mission"] == "test"
        assert contexts["Agent-2"]["status"] == "active"

    def test_get_context_summary_empty(self, manager):
        """Test getting context summary with no agents."""
        summary = manager.get_context_summary()
        
        assert summary["total_agents"] == 0
        assert summary["agent_ids"] == []
        assert "metadata" in summary
        assert summary["metadata"]["version"] == "1.0.0"

    def test_get_context_summary_with_agents(self, manager):
        """Test getting context summary with agents."""
        manager.set_agent_context("Agent-1", {"mission": "test1"})
        manager.set_agent_context("Agent-2", {"mission": "test2"})
        
        summary = manager.get_context_summary()
        
        assert summary["total_agents"] == 2
        assert len(summary["agent_ids"]) == 2
        assert "Agent-1" in summary["agent_ids"]
        assert "Agent-2" in summary["agent_ids"]
        assert "metadata" in summary

    def test_set_context_overwrites_existing(self, manager):
        """Test that setting context overwrites existing context."""
        manager.set_agent_context("Agent-1", {"mission": "old"})
        first_updated = manager._contexts["Agent-1"]["updated_at"]
        
        import time
        time.sleep(0.01)
        
        manager.set_agent_context("Agent-1", {"mission": "new", "priority": "high"})
        
        assert manager._contexts["Agent-1"]["mission"] == "new"
        assert manager._contexts["Agent-1"]["priority"] == "high"
        assert manager._contexts["Agent-1"]["updated_at"] != first_updated

    def test_context_includes_timestamps(self, manager):
        """Test that contexts include proper timestamps."""
        manager.set_agent_context("Agent-1", {"mission": "test"})
        context = manager.get_agent_context("Agent-1")
        
        assert "updated_at" in context
        assert isinstance(context["updated_at"], str)
        # Verify it's a valid ISO format timestamp
        datetime.fromisoformat(context["updated_at"])

    def test_metadata_initialization(self, manager):
        """Test metadata is properly initialized."""
        assert "created_at" in manager._metadata
        assert "version" in manager._metadata
        assert isinstance(manager._metadata["created_at"], str)
        # Verify it's a valid ISO format timestamp
        datetime.fromisoformat(manager._metadata["created_at"])

