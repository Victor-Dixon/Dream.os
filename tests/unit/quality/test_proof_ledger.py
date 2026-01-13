#!/usr/bin/env python3
"""
Tests for Proof Ledger - QA Domain SSOT
========================================

Tests for proof_ledger.py SSOT functionality.

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-07
"""

import json
import os
import pytest
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from src.quality.proof_ledger import run_tdd_proof, _git_head


class TestProofLedger:
    """Tests for Proof Ledger SSOT."""

    def test_git_head_success(self):
        """Test _git_head returns commit hash when git is available."""
        result = _git_head()
        assert result is not None
        assert result != "unknown"
        assert len(result) == 40  # SHA-1 hash length

    @patch('subprocess.check_output')
    def test_git_head_failure(self, mock_check_output):
        """Test _git_head returns 'unknown' when git fails."""
        mock_check_output.side_effect = Exception("Git not available")
        result = _git_head()
        assert result == "unknown"

    @patch('subprocess.run')
    @patch('src.quality.proof_ledger.os.makedirs')
    @patch('src.quality.proof_ledger._git_head')
    def test_run_tdd_proof_pytest_available(self, mock_git_head, mock_makedirs, mock_run):
        """Test run_tdd_proof with pytest available."""
        # Mock git head
        mock_git_head.return_value = 'abc123'
        
        # Mock pytest run
        mock_proc = Mock()
        mock_proc.returncode = 0
        mock_proc.stdout = "10 passed, 0 failed in 2.5s"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        # Use actual temp directory and ensure makedirs creates it
        with tempfile.TemporaryDirectory() as tmpdir:
            original_join = os.path.join
            original_makedirs = os.makedirs
            original_dirname = os.path.dirname
            
            def mock_join(*args):
                # Convert runtime paths to tmpdir paths
                if len(args) > 0 and args[0] == "runtime":
                    return original_join(tmpdir, *args[1:])
                # If any arg contains runtime, convert it
                str_args = [str(a) for a in args]
                if any("runtime" in str(a) for a in args):
                    # Find runtime in args and replace with tmpdir
                    new_args = []
                    for a in args:
                        if "runtime" in str(a):
                            # Replace runtime with tmpdir
                            new_args.append(str(a).replace("runtime", tmpdir))
                        else:
                            new_args.append(a)
                    return original_join(*new_args)
                return original_join(*args)
            
            def mock_dirname(path):
                # If path contains tmpdir, return dirname of transformed path
                if tmpdir in path:
                    return original_dirname(path)
                # If path contains runtime, transform it
                if "runtime" in path:
                    transformed = path.replace("runtime", tmpdir)
                    return original_dirname(transformed)
                return original_dirname(path)
            
            def mock_makedirs_wrapper(path, *args, **kwargs):
                # Convert runtime paths to tmpdir paths
                if "runtime" in path:
                    path = path.replace("runtime", tmpdir)
                if path.startswith(tmpdir):
                    return original_makedirs(path, *args, **kwargs)
                return None
            
            with patch('src.quality.proof_ledger.os.path.join', side_effect=mock_join), \
                 patch('src.quality.proof_ledger.os.path.dirname', side_effect=mock_dirname), \
                 patch('src.quality.proof_ledger.os.makedirs', side_effect=mock_makedirs_wrapper), \
                 patch('builtins.open', create=True) as mock_open:
                # Mock file writing
                mock_file = Mock()
                mock_open.return_value.__enter__.return_value = mock_file
                proof_path = run_tdd_proof("test_mode", {"Agent-1": "role1"})
                
                assert proof_path is not None
                assert "proof-" in proof_path
                assert tmpdir in proof_path or "runtime" not in proof_path
                # Verify file was opened for writing
                mock_open.assert_called_once()

    @patch('subprocess.run')
    @patch('src.quality.proof_ledger.os.makedirs')
    @patch('src.quality.proof_ledger._git_head')
    def test_run_tdd_proof_pytest_not_available(self, mock_git_head, mock_makedirs, mock_run):
        """Test run_tdd_proof when pytest is not available."""
        # Mock git head
        mock_git_head.return_value = 'abc123'
        
        # Mock pytest not found
        mock_run.side_effect = FileNotFoundError("pytest not found")

        with tempfile.TemporaryDirectory() as tmpdir:
            original_join = os.path.join
            original_makedirs = os.makedirs
            original_dirname = os.path.dirname
            
            def mock_join(*args):
                if len(args) > 0 and args[0] == "runtime":
                    return original_join(tmpdir, *args[1:])
                return original_join(*args)
            
            def mock_dirname(path):
                # If path contains tmpdir, return dirname of transformed path
                if tmpdir in path:
                    return original_dirname(path)
                # If path contains runtime, transform it
                if "runtime" in path:
                    transformed = path.replace("runtime", tmpdir)
                    return original_dirname(transformed)
                return original_dirname(path)
            
            def mock_makedirs_wrapper(path, *args, **kwargs):
                # Always create directories in temp dir
                if "runtime" in path or path.startswith(tmpdir):
                    # Extract the relative path and create in tmpdir
                    if path.startswith(tmpdir):
                        target_path = path
                    else:
                        # Convert runtime path to tmpdir path
                        parts = path.replace("\\", "/").split("/")
                        if "runtime" in parts:
                            idx = parts.index("runtime")
                            target_path = os.path.join(tmpdir, *parts[idx+1:])
                        else:
                            target_path = os.path.join(tmpdir, *parts)
                    return original_makedirs(target_path, *args, **kwargs)
                return None
            
            with patch('src.quality.proof_ledger.os.path.join', side_effect=mock_join), \
                 patch('src.quality.proof_ledger.os.path.dirname', side_effect=mock_dirname), \
                 patch('src.quality.proof_ledger.os.makedirs', side_effect=mock_makedirs_wrapper), \
                 patch('builtins.open', create=True) as mock_open:
                # Mock file writing
                mock_file = Mock()
                mock_open.return_value.__enter__.return_value = mock_file
                proof_path = run_tdd_proof("test_mode", {"Agent-1": "role1"})
                
                assert proof_path is not None
                assert "proof-" in proof_path
                # Verify file was opened for writing
                mock_open.assert_called_once()

    @patch('subprocess.run')
    @patch('src.quality.proof_ledger.os.makedirs')
    @patch('src.quality.proof_ledger._git_head')
    def test_run_tdd_proof_pytest_error(self, mock_git_head, mock_makedirs, mock_run):
        """Test run_tdd_proof when pytest raises an error."""
        # Mock git head
        mock_git_head.return_value = 'abc123'
        
        # Mock pytest error
        mock_run.side_effect = Exception("pytest error")

        with tempfile.TemporaryDirectory() as tmpdir:
            original_join = os.path.join
            original_makedirs = os.makedirs
            original_dirname = os.path.dirname
            
            def mock_join(*args):
                if len(args) > 0 and args[0] == "runtime":
                    return original_join(tmpdir, *args[1:])
                return original_join(*args)
            
            def mock_dirname(path):
                # If path contains tmpdir, return dirname of transformed path
                if tmpdir in path:
                    return original_dirname(path)
                # If path contains runtime, transform it
                if "runtime" in path:
                    transformed = path.replace("runtime", tmpdir)
                    return original_dirname(transformed)
                return original_dirname(path)
            
            def mock_makedirs_wrapper(path, *args, **kwargs):
                # Always create directories in temp dir
                if "runtime" in path or path.startswith(tmpdir):
                    # Extract the relative path and create in tmpdir
                    if path.startswith(tmpdir):
                        target_path = path
                    else:
                        # Convert runtime path to tmpdir path
                        parts = path.replace("\\", "/").split("/")
                        if "runtime" in parts:
                            idx = parts.index("runtime")
                            target_path = os.path.join(tmpdir, *parts[idx+1:])
                        else:
                            target_path = os.path.join(tmpdir, *parts)
                    return original_makedirs(target_path, *args, **kwargs)
                return None
            
            with patch('src.quality.proof_ledger.os.path.join', side_effect=mock_join), \
                 patch('src.quality.proof_ledger.os.path.dirname', side_effect=mock_dirname), \
                 patch('src.quality.proof_ledger.os.makedirs', side_effect=mock_makedirs_wrapper), \
                 patch('builtins.open', create=True) as mock_open:
                # Mock file writing
                mock_file = Mock()
                mock_open.return_value.__enter__.return_value = mock_file
                proof_path = run_tdd_proof("test_mode", {"Agent-1": "role1"})
                
                assert proof_path is not None
                assert "proof-" in proof_path
                # Verify file was opened for writing
                mock_open.assert_called_once()

    @patch('subprocess.run')
    @patch('src.quality.proof_ledger.os.makedirs')
    @patch('src.quality.proof_ledger._git_head')
    def test_run_tdd_proof_creates_directory(self, mock_git_head, mock_makedirs, mock_run):
        """Test run_tdd_proof creates output directory."""
        mock_git_head.return_value = 'abc123'
        
        mock_proc = Mock()
        mock_proc.returncode = 0
        mock_proc.stdout = "5 passed"
        mock_proc.stderr = ""
        mock_run.return_value = mock_proc

        with tempfile.TemporaryDirectory() as tmpdir:
            original_join = os.path.join
            original_makedirs = os.makedirs
            original_dirname = os.path.dirname
            makedirs_called = []
            
            def mock_join(*args):
                if len(args) > 0 and args[0] == "runtime":
                    return original_join(tmpdir, *args[1:])
                return original_join(*args)
            
            def mock_dirname(path):
                # If path contains tmpdir, return dirname of transformed path
                if tmpdir in path:
                    return original_dirname(path)
                # If path contains runtime, transform it
                if "runtime" in path:
                    transformed = path.replace("runtime", tmpdir)
                    return original_dirname(transformed)
                return original_dirname(path)
            
            def mock_makedirs_wrapper(path, *args, **kwargs):
                makedirs_called.append(path)
                # Convert runtime paths to tmpdir paths
                if "runtime" in path:
                    path = path.replace("runtime", tmpdir)
                if path.startswith(tmpdir):
                    return original_makedirs(path, *args, **kwargs)
                return None
            
            with patch('src.quality.proof_ledger.os.path.join', side_effect=mock_join), \
                 patch('src.quality.proof_ledger.os.path.dirname', side_effect=mock_dirname), \
                 patch('src.quality.proof_ledger.os.makedirs', side_effect=mock_makedirs_wrapper), \
                 patch('builtins.open', create=True) as mock_open:
                # Mock file writing
                mock_file = Mock()
                mock_open.return_value.__enter__.return_value = mock_file
                run_tdd_proof("test_mode", {})
                # Verify makedirs was called
                assert len(makedirs_called) > 0
                # Verify file was opened for writing
                mock_open.assert_called_once()
