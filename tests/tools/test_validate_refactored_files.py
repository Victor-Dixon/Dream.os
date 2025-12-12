#!/usr/bin/env python3
"""
Tests for validate_refactored_files.py

Author: Agent-8 (SSOT & System Integration Specialist)
Date: 2025-12-12
V2 Compliant: Yes
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.validate_refactored_files import (
    count_lines,
    count_functions,
    count_classes,
    validate_file,
)


class TestValidateRefactoredFiles:
    """Test suite for validate_refactored_files.py"""

    def test_count_lines(self):
        """Test line counting."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("line 1\nline 2\nline 3\n")
            temp_path = Path(f.name)
        
        try:
            assert count_lines(temp_path) == 3
        finally:
            temp_path.unlink()

    def test_count_functions(self):
        """Test function counting."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("def func1():\n    pass\n\ndef func2():\n    pass\n")
            temp_path = Path(f.name)
        
        try:
            # Should count def statements
            count = count_functions(temp_path)
            assert count > 0
        finally:
            temp_path.unlink()

    def test_count_classes(self):
        """Test class counting."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("class Class1:\n    pass\n\nclass Class2:\n    pass\n")
            temp_path = Path(f.name)
        
        try:
            assert count_classes(temp_path) == 2
        finally:
            temp_path.unlink()

    def test_validate_file_compliant(self):
        """Test validation of compliant file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            # Create file with <300 lines
            f.write("\n".join([f"# line {i}" for i in range(100)]))
            temp_path = Path(f.name)
        
        try:
            result = validate_file(temp_path, loc_limit=300)
            assert result["compliant"] is True
            assert len(result["violations"]) == 0
            assert result["lines"] == 100
        finally:
            temp_path.unlink()

    def test_validate_file_violation(self):
        """Test validation of non-compliant file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            # Create file with >300 lines
            f.write("\n".join([f"# line {i}" for i in range(400)]))
            temp_path = Path(f.name)
        
        try:
            result = validate_file(temp_path, loc_limit=300)
            assert result["compliant"] is False
            assert len(result["violations"]) > 0
            assert result["lines"] == 400
        finally:
            temp_path.unlink()

    def test_cli_help(self):
        """Test CLI help output."""
        result = subprocess.run(
            [sys.executable, "scripts/validate_refactored_files.py", "--help"],
            capture_output=True,
            text=True,
            cwd=project_root
        )
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()

    def test_cli_validation_compliant(self):
        """Test CLI validation of compliant file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("\n".join([f"# line {i}" for i in range(100)]))
            temp_path = Path(f.name)
        
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/validate_refactored_files.py",
                    str(temp_path),
                    "--output-format",
                    "text"
                ],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            assert result.returncode == 0
            assert "Compliant Files: 1" in result.stdout
        finally:
            temp_path.unlink()

    def test_cli_validation_json(self):
        """Test CLI validation with JSON output."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as f:
            f.write("\n".join([f"# line {i}" for i in range(100)]))
            temp_path = Path(f.name)
        
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/validate_refactored_files.py",
                    str(temp_path),
                    "--output-format",
                    "json"
                ],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            assert result.returncode == 0
            output = json.loads(result.stdout)
            assert output["total_files"] == 1
            assert output["compliant_files"] == 1
        finally:
            temp_path.unlink()

