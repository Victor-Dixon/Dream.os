import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.unit
def test_devlog_manager_help_exits_zero():
    repo_root = Path(__file__).resolve().parents[2]
    tool = repo_root / "tools" / "devlog_manager.py"

    result = subprocess.run(
        [sys.executable, str(tool), "--help"],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "devlog" in (result.stdout + result.stderr).lower()
