"""
Tests for policy_loader.py

Comprehensive tests for messaging template policy loading.
Target: ≥85% coverage
"""

import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from src.services.messaging.policy_loader import (
    DEFAULT_POLICY,
    load_template_policy,
    _merge_policy,
    resolve_template_by_roles,
    resolve_template_by_channel,
)


class TestDefaultPolicy:
    """Tests for DEFAULT_POLICY constant."""

    def test_default_policy_structure(self):
        """Test that default policy has correct structure."""
        assert "version" in DEFAULT_POLICY
        assert "roles" in DEFAULT_POLICY
        assert "role_matrix" in DEFAULT_POLICY
        assert "channels" in DEFAULT_POLICY

    def test_default_policy_version(self):
        """Test default policy version."""
        assert DEFAULT_POLICY["version"] == 1

    def test_default_policy_roles(self):
        """Test default policy roles."""
        assert "defaults" in DEFAULT_POLICY["roles"]
        assert "CAPTAIN" in DEFAULT_POLICY["roles"]

    def test_default_policy_role_matrix(self):
        """Test default policy role matrix."""
        # Access role_matrix directly (it exists in DEFAULT_POLICY)
        assert "role_matrix" in DEFAULT_POLICY
        matrix = DEFAULT_POLICY["role_matrix"]
        assert "CAPTAIN->ANY" in matrix
        assert "ANY->CAPTAIN" in matrix
        assert "ANY->ANY" in matrix
        assert "NON_CAPTAIN->NON_CAPTAIN" in matrix

    def test_default_policy_channels(self):
        """Test default policy channels."""
        channels = DEFAULT_POLICY["channels"]
        assert "onboarding" in channels
        assert "passdown" in channels
        assert "standard" in channels


class TestLoadTemplatePolicy:
    """Tests for load_template_policy function."""

    @patch('src.services.messaging.policy_loader.yaml', None)
    def test_load_template_policy_no_yaml(self):
        """Test loading policy when yaml is not available."""
        result = load_template_policy()
        
        assert result == DEFAULT_POLICY

    @patch('src.services.messaging.policy_loader.Path')
    def test_load_template_policy_file_not_exists(self, mock_path):
        """Test loading policy when file doesn't exist."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance
        
        result = load_template_policy("nonexistent.yaml")
        
        assert result == DEFAULT_POLICY

    @patch('builtins.open', new_callable=mock_open, read_data='version: 2\nroles:\n  defaults:\n    fallback: "minimal"')
    @patch('src.services.messaging.policy_loader.Path')
    @patch('src.services.messaging.policy_loader.yaml')
    def test_load_template_policy_success(self, mock_yaml, mock_path, mock_file):
        """Test loading policy successfully."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        mock_yaml.safe_load.return_value = {"version": 2, "roles": {"defaults": {"fallback": "minimal"}}}
        
        result = load_template_policy("test.yaml")
        
        assert result["version"] == 2
        assert result["roles"]["defaults"]["fallback"] == "minimal"
        # Should merge with defaults
        assert "channels" in result

    @patch('builtins.open', side_effect=Exception("Test error"))
    @patch('src.services.messaging.policy_loader.Path')
    @patch('src.services.messaging.policy_loader.yaml')
    def test_load_template_policy_exception(self, mock_yaml, mock_path, mock_file):
        """Test loading policy with exception."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        
        result = load_template_policy("test.yaml")
        
        # Should fall back to defaults
        assert result == DEFAULT_POLICY

    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('src.services.messaging.policy_loader.Path')
    @patch('src.services.messaging.policy_loader.yaml')
    def test_load_template_policy_empty_file(self, mock_yaml, mock_path, mock_file):
        """Test loading policy from empty file."""
        mock_path_instance = MagicMock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance
        mock_yaml.safe_load.return_value = None
        
        result = load_template_policy("empty.yaml")
        
        # Should merge with defaults
        assert result == DEFAULT_POLICY


class TestMergePolicy:
    """Tests for _merge_policy function."""

    def test_merge_policy_simple_override(self):
        """Test merging policy with simple override."""
        base = {"key1": "value1", "key2": "value2"}
        override = {"key1": "new_value1"}
        
        result = _merge_policy(base, override)
        
        assert result["key1"] == "new_value1"
        assert result["key2"] == "value2"

    def test_merge_policy_nested_dict(self):
        """Test merging policy with nested dictionaries."""
        base = {"roles": {"defaults": {"fallback": "compact"}}}
        override = {"roles": {"defaults": {"fallback": "minimal"}}}
        
        result = _merge_policy(base, override)
        
        assert result["roles"]["defaults"]["fallback"] == "minimal"

    def test_merge_policy_add_new_key(self):
        """Test merging policy with new key."""
        base = {"key1": "value1"}
        override = {"key2": "value2"}
        
        result = _merge_policy(base, override)
        
        assert result["key1"] == "value1"
        assert result["key2"] == "value2"

    def test_merge_policy_deep_nesting(self):
        """Test merging policy with deep nesting."""
        base = {"level1": {"level2": {"level3": "value"}}}
        override = {"level1": {"level2": {"level3": "new_value"}}}
        
        result = _merge_policy(base, override)
        
        assert result["level1"]["level2"]["level3"] == "new_value"

    def test_merge_policy_dict_to_non_dict(self):
        """Test merging when override replaces dict with non-dict."""
        base = {"key": {"nested": "value"}}
        override = {"key": "simple_value"}
        
        result = _merge_policy(base, override)
        
        assert result["key"] == "simple_value"


class TestResolveTemplateByRoles:
    """Tests for resolve_template_by_roles function."""

    def test_resolve_template_captain_to_any(self):
        """Test resolving template for captain to any."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_roles(policy, "CAPTAIN", "Agent-1")
        
        assert result == "full"

    def test_resolve_template_any_to_captain(self):
        """Test resolving template for any to captain."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_roles(policy, "Agent-1", "CAPTAIN")
        
        assert result == "full"

    def test_resolve_template_non_captain_to_non_captain(self):
        """Test resolving template for non-captain to non-captain."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_roles(policy, "Agent-1", "Agent-2")
        
        assert result == "minimal"

    def test_resolve_template_any_to_any(self):
        """Test resolving template with any to any fallback."""
        policy = DEFAULT_POLICY.copy()
        # Remove NON_CAPTAIN->NON_CAPTAIN to test ANY->ANY
        del policy["role_matrix"]["NON_CAPTAIN->NON_CAPTAIN"]
        
        result = resolve_template_by_roles(policy, "Agent-1", "Agent-2")
        
        assert result == "compact"

    def test_resolve_template_fallback_to_defaults(self):
        """Test resolving template with fallback to defaults."""
        policy = {"roles": {"defaults": {"fallback": "minimal"}}}
        
        result = resolve_template_by_roles(policy, "Agent-1", "Agent-2")
        
        assert result == "minimal"

    def test_resolve_template_case_insensitive_captain(self):
        """Test that captain role is case insensitive."""
        policy = DEFAULT_POLICY.copy()
        result1 = resolve_template_by_roles(policy, "captain", "Agent-1")
        result2 = resolve_template_by_roles(policy, "CAPTAIN", "Agent-1")
        
        assert result1 == result2 == "full"

    def test_resolve_template_missing_role_matrix(self):
        """Test resolving template when role_matrix is missing."""
        policy = {"roles": {"defaults": {"fallback": "compact"}}}
        
        result = resolve_template_by_roles(policy, "Agent-1", "Agent-2")
        
        assert result == "compact"


class TestResolveTemplateByChannel:
    """Tests for resolve_template_by_channel function."""

    def test_resolve_template_onboarding_channel(self):
        """Test resolving template for onboarding channel."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_channel(policy, "onboarding")
        
        assert result == "full"

    def test_resolve_template_passdown_channel(self):
        """Test resolving template for passdown channel."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_channel(policy, "passdown")
        
        assert result == "minimal"

    def test_resolve_template_standard_channel(self):
        """Test resolving template for standard channel."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_channel(policy, "standard")
        
        assert result == "compact"

    def test_resolve_template_unknown_channel(self):
        """Test resolving template for unknown channel."""
        policy = DEFAULT_POLICY.copy()
        result = resolve_template_by_channel(policy, "unknown")
        
        # Should fall back to standard
        assert result == "compact"

    def test_resolve_template_missing_channels(self):
        """Test resolving template when channels are missing."""
        policy = {}
        result = resolve_template_by_channel(policy, "test")
        
        # Should handle gracefully
        assert isinstance(result, str)

    def test_resolve_template_custom_channel(self):
        """Test resolving template for custom channel."""
        policy = {
            "channels": {
                "custom": "full",
                "standard": "compact"
            }
        }
        result = resolve_template_by_channel(policy, "custom")
        
        assert result == "full"

