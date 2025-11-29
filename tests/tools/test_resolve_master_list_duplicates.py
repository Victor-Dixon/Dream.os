#!/usr/bin/env python3
"""
Tests for Resolve Master List Duplicates Tool

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-27
"""

import pytest
import json
import tempfile
from pathlib import Path
from collections import defaultdict
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from tools.resolve_master_list_duplicates import (
    find_duplicates,
    resolve_duplicates,
    update_stats
)


class TestFindDuplicates:
    """Test find_duplicates function"""
    
    def test_no_duplicates(self):
        """Test with no duplicates"""
        repos = [
            {"num": 1, "name": "repo1"},
            {"num": 2, "name": "repo2"},
            {"num": 3, "name": "repo3"},
        ]
        result = find_duplicates(repos)
        assert len(result) == 0
    
    def test_case_insensitive_duplicates(self):
        """Test finding case-insensitive duplicates"""
        repos = [
            {"num": 1, "name": "Repo1"},
            {"num": 2, "name": "repo1"},  # Case duplicate
            {"num": 3, "name": "repo2"},
        ]
        result = find_duplicates(repos)
        assert len(result) == 1
        assert (1, 2) in result
    
    def test_multiple_duplicates(self):
        """Test finding multiple duplicates"""
        repos = [
            {"num": 1, "name": "repo1"},
            {"num": 2, "name": "repo1"},  # Duplicate 1
            {"num": 3, "name": "repo2"},
            {"num": 4, "name": "repo2"},  # Duplicate 2
        ]
        result = find_duplicates(repos)
        assert len(result) == 2
    
    def test_three_way_duplicate(self):
        """Test finding three-way duplicate"""
        repos = [
            {"num": 1, "name": "repo1"},
            {"num": 2, "name": "repo1"},
            {"num": 3, "name": "repo1"},
        ]
        result = find_duplicates(repos)
        assert len(result) == 2  # (1,2) and (1,3)


class TestResolveDuplicates:
    """Test resolve_duplicates function"""
    
    def test_no_duplicates_to_resolve(self):
        """Test resolving with no duplicates"""
        repos = [
            {"num": 1, "name": "repo1"},
            {"num": 2, "name": "repo2"},
        ]
        kept, removed = resolve_duplicates(repos)
        assert len(kept) == 2
        assert len(removed) == 0
    
    def test_resolve_single_duplicate(self):
        """Test resolving single duplicate"""
        repos = [
            {"num": 1, "name": "repo1"},
            {"num": 2, "name": "repo1"},  # Duplicate
            {"num": 3, "name": "repo2"},
        ]
        kept, removed = resolve_duplicates(repos)
        assert len(kept) == 2
        assert len(removed) == 1
        assert removed[0]["num"] == 2  # Lower num (1) kept, higher (2) removed
    
    def test_resolve_multiple_duplicates(self):
        """Test resolving multiple duplicates"""
        repos = [
            {"num": 1, "name": "repo1"},
            {"num": 2, "name": "repo1"},  # Duplicate 1
            {"num": 3, "name": "repo2"},
            {"num": 4, "name": "repo2"},  # Duplicate 2
        ]
        kept, removed = resolve_duplicates(repos)
        assert len(kept) == 2
        assert len(removed) == 2
        assert all(r["num"] in [2, 4] for r in removed)
    
    def test_keep_lower_num(self):
        """Test that lower num is always kept"""
        repos = [
            {"num": 5, "name": "repo1"},
            {"num": 1, "name": "repo1"},  # Lower num, should be kept
        ]
        kept, removed = resolve_duplicates(repos)
        assert len(kept) == 1
        assert kept[0]["num"] == 1
        assert removed[0]["num"] == 5


class TestUpdateStats:
    """Test update_stats function"""
    
    def test_basic_stats(self):
        """Test basic stats calculation"""
        repos = [
            {"num": 1, "name": "repo1", "analyzed": True, "agent": "Agent-1"},
            {"num": 2, "name": "repo2", "analyzed": False, "agent": "Agent-2"},
            {"num": 3, "name": "repo3", "analyzed": True, "agent": "Agent-1", "goldmine": True},
        ]
        stats = update_stats(repos)
        assert stats["total_repos"] == 3
        assert stats["analyzed"] == 2
        assert stats["pending"] == 1
        assert stats["goldmines"] == 1
    
    def test_agent_counts(self):
        """Test agent count calculation"""
        repos = [
            {"num": 1, "name": "repo1", "analyzed": True, "agent": "Agent-1"},
            {"num": 2, "name": "repo2", "analyzed": True, "agent": "Agent-1"},
            {"num": 3, "name": "repo3", "analyzed": False, "agent": "Agent-2"},
        ]
        stats = update_stats(repos)
        assert stats["agents"]["Agent-1"]["assigned"] == 2
        assert stats["agents"]["Agent-1"]["completed"] == 2
        assert stats["agents"]["Agent-2"]["assigned"] == 1
        assert stats["agents"]["Agent-2"]["completed"] == 0
    
    def test_completion_percent(self):
        """Test completion percentage calculation"""
        repos = [
            {"num": 1, "name": "repo1", "analyzed": True},
            {"num": 2, "name": "repo2", "analyzed": True},
            {"num": 3, "name": "repo3", "analyzed": False},
        ]
        stats = update_stats(repos)
        assert stats["completion_percent"] == pytest.approx(66.7, rel=0.1)
    
    def test_empty_repos(self):
        """Test stats with empty repos list"""
        repos = []
        stats = update_stats(repos)
        assert stats["total_repos"] == 0
        assert stats["analyzed"] == 0
        assert stats["completion_percent"] == 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

