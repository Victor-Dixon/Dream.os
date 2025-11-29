#!/usr/bin/env python3
"""
Tests for Batch 2 SSOT Verifier

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-11-27
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

from tools.batch2_ssot_verifier import Batch2SSOTVerifier


@pytest.fixture
def temp_master_list():
    """Create temporary master list for testing"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        master_list = {
            "repos": [
                {"num": 1, "name": "repo1", "analyzed": True, "agent": "Agent-1"},
                {"num": 2, "name": "repo2", "analyzed": True, "agent": "Agent-2"},
                {"num": 3, "name": "Unknown", "analyzed": False, "agent": "Agent-3"},
            ],
            "stats": {"total_repos": 3, "analyzed": 2, "pending": 1}
        }
        json.dump(master_list, f)
        temp_path = Path(f.name)
    
    yield temp_path
    
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def verifier_with_temp_list(temp_master_list):
    """Create verifier with temporary master list"""
    verifier = Batch2SSOTVerifier()
    verifier.master_list_path = temp_master_list
    return verifier


class TestBatch2SSOTVerifier:
    """Test Batch2SSOTVerifier class"""
    
    def test_load_master_list_success(self, verifier_with_temp_list):
        """Test loading master list successfully"""
        result = verifier_with_temp_list.load_master_list()
        assert result is not None
        assert "repos" in result
        assert len(result["repos"]) == 3
    
    def test_load_master_list_not_found(self):
        """Test loading non-existent master list"""
        verifier = Batch2SSOTVerifier()
        verifier.master_list_path = Path("/nonexistent/file.json")
        result = verifier.load_master_list()
        assert result is None
    
    def test_verify_master_list_no_duplicates(self, verifier_with_temp_list):
        """Test master list verification with no duplicates"""
        result = verifier_with_temp_list.verify_master_list()
        assert result is True
        assert verifier_with_temp_list.verification_results["master_list"] is True
    
    def test_verify_master_list_with_duplicates(self, temp_master_list):
        """Test master list verification with duplicates"""
        # Add duplicate
        master_list = json.loads(temp_master_list.read_text())
        master_list["repos"].append({
            "num": 4,
            "name": "repo1",  # Duplicate of repo1
            "analyzed": True,
            "agent": "Agent-4"
        })
        temp_master_list.write_text(json.dumps(master_list))
        
        verifier = Batch2SSOTVerifier()
        verifier.master_list_path = temp_master_list
        result = verifier.verify_master_list()
        assert result is False
        assert len(verifier.issues_found) > 0
    
    def test_verify_master_list_unknown_repos(self, verifier_with_temp_list):
        """Test master list verification with Unknown repos"""
        result = verifier_with_temp_list.verify_master_list()
        # Should pass but warn about Unknown repos
        assert result is True  # Unknown repos are warnings, not failures
    
    @patch('subprocess.run')
    def test_verify_imports_success(self, mock_subprocess, verifier_with_temp_list):
        """Test import verification success"""
        mock_subprocess.return_value = MagicMock(returncode=0, stdout="OK")
        result = verifier_with_temp_list.verify_imports()
        assert result is True
        assert verifier_with_temp_list.verification_results["imports"] is True
    
    @patch('subprocess.run')
    def test_verify_imports_failure(self, mock_subprocess, verifier_with_temp_list):
        """Test import verification failure"""
        mock_subprocess.return_value = MagicMock(returncode=1, stdout="Error")
        result = verifier_with_temp_list.verify_imports()
        assert result is False
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_verify_config_ssot_success(self, mock_read, mock_exists, verifier_with_temp_list):
        """Test config SSOT verification success"""
        mock_exists.return_value = True
        mock_read.return_value = "class Config:\n    pass"
        result = verifier_with_temp_list.verify_config_ssot()
        assert result is True
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_verify_config_ssot_duplicate_classes(self, mock_read, mock_exists, verifier_with_temp_list):
        """Test config SSOT verification with duplicate classes"""
        mock_exists.return_value = True
        mock_read.return_value = "class Config:\n    pass\nclass Config:\n    pass"
        result = verifier_with_temp_list.verify_config_ssot()
        assert result is False
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_verify_messaging_integration_success(self, mock_read, mock_exists, verifier_with_temp_list):
        """Test messaging integration verification success"""
        mock_exists.return_value = True
        mock_read.return_value = "repo = MessageRepository()"
        result = verifier_with_temp_list.verify_messaging_integration()
        assert result is True
    
    @patch('pathlib.Path.exists')
    @patch('pathlib.Path.read_text')
    def test_verify_messaging_integration_duplicates(self, mock_read, mock_exists, verifier_with_temp_list):
        """Test messaging integration verification with duplicates"""
        mock_exists.return_value = True
        mock_read.return_value = "repo1 = MessageRepository()\nrepo2 = MessageRepository()"
        result = verifier_with_temp_list.verify_messaging_integration()
        assert result is False
    
    def test_verify_full_all_pass(self, verifier_with_temp_list):
        """Test full verification with all checks passing"""
        with patch.object(verifier_with_temp_list, 'verify_imports', return_value=True):
            with patch.object(verifier_with_temp_list, 'verify_config_ssot', return_value=True):
                with patch.object(verifier_with_temp_list, 'verify_messaging_integration', return_value=True):
                    with patch.object(verifier_with_temp_list, 'verify_tool_registry', return_value=True):
                        result = verifier_with_temp_list.verify_full()
                        assert result is True
    
    def test_update_master_list_after_merge(self, verifier_with_temp_list):
        """Test updating master list after merge"""
        result = verifier_with_temp_list.update_master_list_after_merge("repo1", "repo2")
        assert result is True
        
        # Verify updates
        master_list = verifier_with_temp_list.load_master_list()
        repo1 = next(r for r in master_list["repos"] if r["name"] == "repo1")
        repo2 = next(r for r in master_list["repos"] if r["name"] == "repo2")
        
        assert repo1.get("merged") is True
        assert repo1.get("merged_into") == "repo2"
        assert "repo1" in repo2.get("merged_repos", [])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

