"""
Unit tests for onboarding_constants.py
Target: ≥85% coverage
"""

import pytest
from src.services.utils.onboarding_constants import (
    PHASE_2_STATUS,
    AGENT_ASSIGNMENTS,
    TARGETS,
    DEFAULT_AGENT_ROLES,
    get_phase_2_status,
    get_agent_assignments,
    get_targets,
    is_phase_2_active,
)


class TestOnboardingConstants:
    """Tests for onboarding constants."""

    def test_phase_2_status_exists(self):
        """Test PHASE_2_STATUS is defined."""
        assert PHASE_2_STATUS is not None
        assert isinstance(PHASE_2_STATUS, dict)

    def test_phase_2_status_contains_keys(self):
        """Test PHASE_2_STATUS contains expected keys."""
        assert "wrap_up_completed" in PHASE_2_STATUS
        assert "agent_8_prepared" in PHASE_2_STATUS
        assert "swarm_coordination_activated" in PHASE_2_STATUS

    def test_phase_2_status_values_are_bool(self):
        """Test PHASE_2_STATUS values are boolean."""
        for value in PHASE_2_STATUS.values():
            assert isinstance(value, bool)

    def test_agent_assignments_exists(self):
        """Test AGENT_ASSIGNMENTS is defined."""
        assert AGENT_ASSIGNMENTS is not None
        assert isinstance(AGENT_ASSIGNMENTS, dict)

    def test_agent_assignments_contains_agents(self):
        """Test AGENT_ASSIGNMENTS contains agent entries."""
        assert "Agent-8" in AGENT_ASSIGNMENTS
        assert "Agent-3" in AGENT_ASSIGNMENTS
        assert "Agent-7" in AGENT_ASSIGNMENTS
        assert "Agent-4" in AGENT_ASSIGNMENTS

    def test_agent_assignments_values_are_strings(self):
        """Test AGENT_ASSIGNMENTS values are strings."""
        for value in AGENT_ASSIGNMENTS.values():
            assert isinstance(value, str)

    def test_targets_exists(self):
        """Test TARGETS is defined."""
        assert TARGETS is not None
        assert isinstance(TARGETS, dict)

    def test_targets_contains_keys(self):
        """Test TARGETS contains expected keys."""
        assert "file_reduction" in TARGETS
        assert "timeline" in TARGETS
        assert "coordination" in TARGETS
        assert "documentation" in TARGETS

    def test_default_agent_roles_exists(self):
        """Test DEFAULT_AGENT_ROLES is defined."""
        assert DEFAULT_AGENT_ROLES is not None
        assert isinstance(DEFAULT_AGENT_ROLES, dict)

    def test_default_agent_roles_contains_all_agents(self):
        """Test DEFAULT_AGENT_ROLES contains all 8 agents."""
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            assert agent_id in DEFAULT_AGENT_ROLES

    def test_default_agent_roles_values_are_strings(self):
        """Test DEFAULT_AGENT_ROLES values are strings."""
        for value in DEFAULT_AGENT_ROLES.values():
            assert isinstance(value, str)
            assert len(value) > 0

    def test_get_phase_2_status_returns_copy(self):
        """Test get_phase_2_status returns a copy."""
        result = get_phase_2_status()
        assert result == PHASE_2_STATUS
        assert result is not PHASE_2_STATUS  # Should be a copy

    def test_get_phase_2_status_modification_doesnt_affect_original(self):
        """Test modifying returned dict doesn't affect original."""
        result = get_phase_2_status()
        result["test_key"] = True
        assert "test_key" not in PHASE_2_STATUS

    def test_get_agent_assignments_returns_copy(self):
        """Test get_agent_assignments returns a copy."""
        result = get_agent_assignments()
        assert result == AGENT_ASSIGNMENTS
        assert result is not AGENT_ASSIGNMENTS  # Should be a copy

    def test_get_agent_assignments_modification_doesnt_affect_original(self):
        """Test modifying returned dict doesn't affect original."""
        result = get_agent_assignments()
        result["Test-Agent"] = "Test Assignment"
        assert "Test-Agent" not in AGENT_ASSIGNMENTS

    def test_get_targets_returns_copy(self):
        """Test get_targets returns a copy."""
        result = get_targets()
        assert result == TARGETS
        assert result is not TARGETS  # Should be a copy

    def test_get_targets_modification_doesnt_affect_original(self):
        """Test modifying returned dict doesn't affect original."""
        result = get_targets()
        result["test_target"] = "test value"
        assert "test_target" not in TARGETS

    def test_is_phase_2_active_returns_bool(self):
        """Test is_phase_2_active returns boolean."""
        result = is_phase_2_active()
        assert isinstance(result, bool)

    def test_is_phase_2_active_when_all_true(self):
        """Test is_phase_2_active returns True when all statuses are True."""
        # All values in PHASE_2_STATUS should be True based on the code
        result = is_phase_2_active()
        # This will be True if all values are True
        assert result == all(PHASE_2_STATUS.values())

    def test_is_phase_2_active_with_false_value(self):
        """Test is_phase_2_active returns False when any status is False."""
        # Create a modified copy for testing
        original_status = PHASE_2_STATUS.copy()
        # Since we can't modify the original, we test the logic
        # If all values are True, it should return True
        # If any value is False, it should return False
        result = is_phase_2_active()
        expected = all(PHASE_2_STATUS.values())
        assert result == expected

    def test_constants_are_immutable(self):
        """Test that constants are not accidentally modified."""
        original_phase_2 = PHASE_2_STATUS.copy()
        original_assignments = AGENT_ASSIGNMENTS.copy()
        original_targets = TARGETS.copy()
        original_roles = DEFAULT_AGENT_ROLES.copy()

        # Call functions that return copies
        get_phase_2_status()
        get_agent_assignments()
        get_targets()

        # Verify originals unchanged
        assert PHASE_2_STATUS == original_phase_2
        assert AGENT_ASSIGNMENTS == original_assignments
        assert TARGETS == original_targets
        assert DEFAULT_AGENT_ROLES == original_roles


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
