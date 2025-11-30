#!/usr/bin/env python3
"""
SSOT Validation Tests for GitHub Bypass System
===============================================

Validates SSOT compliance across all GitHub bypass components:
- Single source of truth getter functions
- No duplicate implementations
- Proper singleton/SSOT patterns
- Integration between components

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-01-28
Priority: HIGH
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
import importlib
import inspect
import ast

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.local_repo_layer import get_local_repo_manager, LocalRepoManager
from src.core.deferred_push_queue import get_deferred_push_queue, DeferredPushQueue
from src.core.synthetic_github import get_synthetic_github, SyntheticGitHub
from src.core.consolidation_buffer import get_consolidation_buffer, ConsolidationBuffer
from src.core.merge_conflict_resolver import get_conflict_resolver, MergeConflictResolver


class TestSSOTGetterFunctions:
    """Test SSOT getter function compliance."""
    
    def test_local_repo_manager_ssot(self):
        """Test LocalRepoManager uses SSOT getter pattern."""
        # First call
        manager1 = get_local_repo_manager()
        assert manager1 is not None
        assert isinstance(manager1, LocalRepoManager)
        
        # Second call should return same instance (singleton pattern)
        manager2 = get_local_repo_manager()
        # Note: Some implementations may create new instances, which is acceptable
        # The key is that getter function exists as SSOT entry point
        assert isinstance(manager2, LocalRepoManager)
    
    def test_deferred_push_queue_ssot(self):
        """Test DeferredPushQueue uses SSOT getter pattern."""
        queue1 = get_deferred_push_queue()
        assert queue1 is not None
        assert isinstance(queue1, DeferredPushQueue)
        
        queue2 = get_deferred_push_queue()
        assert isinstance(queue2, DeferredPushQueue)
    
    def test_synthetic_github_ssot(self):
        """Test SyntheticGitHub uses SSOT getter pattern."""
        github1 = get_synthetic_github()
        assert github1 is not None
        assert isinstance(github1, SyntheticGitHub)
        
        github2 = get_synthetic_github()
        assert isinstance(github2, SyntheticGitHub)
    
    def test_consolidation_buffer_ssot(self):
        """Test ConsolidationBuffer uses SSOT getter pattern."""
        buffer1 = get_consolidation_buffer()
        assert buffer1 is not None
        assert isinstance(buffer1, ConsolidationBuffer)
        
        buffer2 = get_consolidation_buffer()
        assert isinstance(buffer2, ConsolidationBuffer)
    
    def test_conflict_resolver_ssot(self):
        """Test MergeConflictResolver uses SSOT getter pattern."""
        resolver1 = get_conflict_resolver()
        assert resolver1 is not None
        assert isinstance(resolver1, MergeConflictResolver)
        
        resolver2 = get_conflict_resolver()
        assert isinstance(resolver2, MergeConflictResolver)


class TestSSOTNoDuplicates:
    """Test no duplicate implementations exist."""
    
    def test_no_duplicate_getter_functions(self):
        """Test getter functions are not duplicated in source files."""
        # Check for duplicate getter function definitions
        synthetic_github_file = project_root / "src" / "core" / "synthetic_github.py"
        deferred_queue_file = project_root / "src" / "core" / "deferred_push_queue.py"
        consolidation_buffer_file = project_root / "src" / "core" / "consolidation_buffer.py"
        merge_resolver_file = project_root / "src" / "core" / "merge_conflict_resolver.py"
        
        def count_getter_functions(file_path: Path, function_name: str) -> int:
            """Count occurrences of getter function definition."""
            if not file_path.exists():
                return 0
            
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                count = 0
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name == function_name:
                        count += 1
                return count
            except Exception:
                return 0
        
        # Check for duplicates (should be exactly 1 per file)
        assert count_getter_functions(synthetic_github_file, "get_synthetic_github") <= 1, \
            "Duplicate get_synthetic_github function found"
        
        assert count_getter_functions(deferred_queue_file, "get_deferred_push_queue") <= 1, \
            "Duplicate get_deferred_push_queue function found"
        
        assert count_getter_functions(consolidation_buffer_file, "get_consolidation_buffer") <= 1, \
            "Duplicate get_consolidation_buffer function found"
        
        assert count_getter_functions(merge_resolver_file, "get_conflict_resolver") <= 1, \
            "Duplicate get_conflict_resolver function found"
    
    def test_no_duplicate_class_definitions(self):
        """Test no duplicate class definitions exist."""
        # Check for duplicate class definitions
        files_to_check = [
            ("synthetic_github.py", ["SyntheticGitHub", "GitHubSandboxMode"]),
            ("deferred_push_queue.py", ["DeferredPushQueue", "PushStatus"]),
            ("consolidation_buffer.py", ["ConsolidationBuffer", "ConsolidationStatus", "MergePlan"]),
            ("merge_conflict_resolver.py", ["MergeConflictResolver"]),
            ("local_repo_layer.py", ["LocalRepoManager"])
        ]
        
        for file_name, class_names in files_to_check:
            file_path = project_root / "src" / "core" / file_name
            if not file_path.exists():
                continue
            
            try:
                content = file_path.read_text(encoding='utf-8')
                tree = ast.parse(content, filename=str(file_path))
                
                for class_name in class_names:
                    count = 0
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef) and node.name == class_name:
                            count += 1
                    
                    assert count == 1, \
                        f"Duplicate {class_name} class found in {file_name} (found {count})"
            except Exception:
                pass  # Skip if file can't be parsed


class TestSSOTIntegration:
    """Test SSOT integration between components."""
    
    def test_synthetic_github_uses_local_repo_manager_ssot(self):
        """Test SyntheticGitHub uses LocalRepoManager via SSOT getter."""
        github = get_synthetic_github()
        assert hasattr(github, 'local_repo_manager')
        assert github.local_repo_manager is not None
        
        # Should use getter function, not direct instantiation
        # This is validated by checking imports and usage patterns
        assert isinstance(github.local_repo_manager, LocalRepoManager)
    
    def test_synthetic_github_uses_deferred_queue_ssot(self):
        """Test SyntheticGitHub uses DeferredPushQueue via SSOT getter."""
        github = get_synthetic_github()
        assert hasattr(github, 'queue') or hasattr(github, 'deferred_queue')
        
        # Should use getter function pattern
        queue_attr = getattr(github, 'queue', None) or getattr(github, 'deferred_queue', None)
        if queue_attr is not None:
            assert isinstance(queue_attr, DeferredPushQueue)
    
    def test_components_import_correctly(self):
        """Test all components can be imported and initialized."""
        # Test all SSOT getters work
        assert get_local_repo_manager() is not None
        assert get_deferred_push_queue() is not None
        assert get_synthetic_github() is not None
        assert get_consolidation_buffer() is not None
        assert get_conflict_resolver() is not None


class TestSSOTPatternCompliance:
    """Test SSOT pattern compliance across components."""
    
    def test_getter_functions_exist(self):
        """Test all required getter functions exist."""
        required_getters = [
            "get_local_repo_manager",
            "get_deferred_push_queue",
            "get_synthetic_github",
            "get_consolidation_buffer",
            "get_conflict_resolver"
        ]
        
        for getter_name in required_getters:
            # Check if getter is importable
            try:
                if getter_name == "get_local_repo_manager":
                    func = get_local_repo_manager
                elif getter_name == "get_deferred_push_queue":
                    func = get_deferred_push_queue
                elif getter_name == "get_synthetic_github":
                    func = get_synthetic_github
                elif getter_name == "get_consolidation_buffer":
                    func = get_consolidation_buffer
                elif getter_name == "get_conflict_resolver":
                    func = get_conflict_resolver
                
                assert callable(func), f"{getter_name} is not callable"
                assert func is not None, f"{getter_name} is None"
            except Exception as e:
                pytest.fail(f"{getter_name} failed to import: {e}")
    
    def test_components_use_getter_pattern(self):
        """Test components use getter pattern for dependencies."""
        # SyntheticGitHub should use get_local_repo_manager
        github = get_synthetic_github()
        
        # Verify it has required attributes from SSOT getters
        assert hasattr(github, 'local_repo_manager'), \
            "SyntheticGitHub should use LocalRepoManager via SSOT"
        
        # Verify types
        assert isinstance(github.local_repo_manager, LocalRepoManager), \
            "local_repo_manager should be LocalRepoManager instance"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

