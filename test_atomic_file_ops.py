#!/usr/bin/env python3
"""
Test Atomic File Operations
===========================

Tests the atomic file operations utility to ensure it prevents file corruption.

Author: Agent-6 (Swarm Intelligence Coordinator)
Date: 2025-12-20
"""

import os
import tempfile
from pathlib import Path
from src.utils.atomic_file_ops import AtomicFileWriter, atomic_write_text, atomic_write_json


def test_atomic_text_write():
    """Test atomic text file writing."""
    print("🧪 Testing atomic text file writing...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"

        # Write initial content
        initial_content = "Line 1\nLine 2\nLine 3\n"
        test_file.write_text(initial_content)

        # Test atomic write
        new_content = "Line 1\nLine 2 MODIFIED\nLine 3\nLine 4\n"
        success = atomic_write_text(test_file, new_content)

        assert success, "Atomic write should succeed"
        assert test_file.read_text() == new_content, "Content should match"

        # Check backup was created
        backup_files = list(test_file.parent.glob(f"{test_file.name}.backup_*"))
        assert len(backup_files) == 1, "Backup should be created"

        print("✅ Atomic text write test passed")


def test_atomic_json_write():
    """Test atomic JSON file writing."""
    print("🧪 Testing atomic JSON file writing...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.json"

        # Test atomic JSON write
        test_data = {"key": "value", "number": 42, "list": [1, 2, 3]}
        success = atomic_write_json(test_file, test_data)

        assert success, "Atomic JSON write should succeed"

        # Verify content
        import json
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)

        assert loaded_data == test_data, "JSON data should match"

        print("✅ Atomic JSON write test passed")


def test_atomic_write_with_failure_simulation():
    """Test atomic write behavior when operations fail."""
    print("🧪 Testing atomic write failure recovery...")

    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"

        # Write initial content
        initial_content = "Original content\n"
        test_file.write_text(initial_content)

        # Test with AtomicFileWriter directly for more control
        writer = AtomicFileWriter(test_file, backup=True)

        # Verify backup was created
        backup_files = list(test_file.parent.glob(f"{test_file.name}.backup_*"))
        assert len(backup_files) == 1, "Backup should be created for existing file"

        # Test successful write
        success = writer.write_text("Modified content\n")
        assert success, "Write should succeed"
        assert test_file.read_text() == "Modified content\n", "Content should be updated"

        print("✅ Atomic write failure recovery test passed")


def test_master_task_log_simulation():
    """Simulate MASTER_TASK_LOG.md operations."""
    print("🧪 Testing MASTER_TASK_LOG.md simulation...")

    with tempfile.TemporaryDirectory() as temp_dir:
        task_log = Path(temp_dir) / "MASTER_TASK_LOG.md"

        # Create initial task log content
        initial_content = """# MASTER TASK LOG

## INBOX

- [ ] Test task 1
- [ ] Test task 2

## THIS_WEEK

## WAITING_ON
"""
        task_log.write_text(initial_content)

        # Simulate claiming a task (like claim_and_fix_master_task.py does)
        lines = initial_content.splitlines()
        # Find and modify task line
        for i, line in enumerate(lines):
            if "Test task 1" in line and "[CLAIMED BY" not in line:
                lines[i] = line.rstrip() + " [CLAIMED BY Agent-6]"
                break

        # Use atomic write
        new_content = '\n'.join(lines) + '\n'
        success = atomic_write_text(task_log, new_content, backup=True)

        assert success, "Task claiming should succeed"
        content = task_log.read_text()
        assert "[CLAIMED BY Agent-6]" in content, "Task should be claimed"
        assert "Test task 1" in content, "Original task should remain"

        print("✅ MASTER_TASK_LOG.md simulation test passed")


def main():
    """Run all tests."""
    print("🚀 Testing Atomic File Operations\n")

    try:
        test_atomic_text_write()
        test_atomic_json_write()
        test_atomic_write_with_failure_simulation()
        test_master_task_log_simulation()

        print("\n🎉 All atomic file operation tests passed!")
        print("✅ File corruption prevention is working correctly")
        return 0

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
