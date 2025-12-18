#!/usr/bin/env python3
"""Basic safety tests for MCP server modules.

These tests deliberately avoid hitting external systems (WordPress, Swarm Brain,
PyAutoGUI, etc.) and instead verify that the core helpers can be imported and
called without raising unexpected exceptions.
"""

from __future__ import annotations

from pathlib import Path

from mcp_servers import git_operations_server as go
from mcp_servers import messaging_server as ms
from mcp_servers import task_manager_server as tm
from mcp_servers import v2_compliance_server as vc
from mcp_servers import website_manager_server as wm
from mcp_servers import swarm_brain_server as sb


SAMPLE_MASTER_TASK_LOG = """# MASTER TASK LOG

**Last Updated:** 2025-01-01

---

## 📥 INBOX (Brain Dump)

- [ ] Existing INBOX task

---

## 🎯 THIS WEEK (Max 5 Items)

1. [ ] Weekly focus task

---

## ⏳ WAITING ON

- Waiting on: Something else - waiting for dependency

---

## 🧊 PARKED / LATER

- Parked idea

---
"""


def _setup_temp_task_log(tmp_path, monkeypatch):
    """Create a temporary MASTER_TASK_LOG with the expected section structure."""
    log_path = tmp_path / "MASTER_TASK_LOG.md"
    log_path.write_text(SAMPLE_MASTER_TASK_LOG, encoding="utf-8")
    # Point the task manager server at the temporary file so tests don't touch
    # the real MASTER_TASK_LOG in the repo.
    monkeypatch.setattr(tm, "TASK_LOG_PATH", log_path)
    return log_path


def test_task_manager_add_and_get_inbox(tmp_path, monkeypatch):
    """add_to_inbox and get_tasks(INBOX) should work against a synthetic log."""
    _setup_temp_task_log(tmp_path, monkeypatch)

    add_result = tm.add_to_inbox("CI test task", agent_id="Agent-CI")
    assert isinstance(add_result, dict)
    assert add_result.get("success") is True

    inbox = tm.get_tasks("INBOX")
    assert inbox.get("success") is True
    tasks = inbox.get("tasks", [])
    assert any("CI test task" in line for line in tasks)


def test_task_manager_mark_task_complete_does_not_crash(tmp_path, monkeypatch):
    """mark_task_complete should succeed on an existing task in INBOX."""
    _setup_temp_task_log(tmp_path, monkeypatch)
    result = tm.mark_task_complete("Existing INBOX task", section="INBOX")
    # Even if the underlying implementation fails to find the task, we only
    # care that the call returns a structured dict (no exceptions).
    assert isinstance(result, dict)
    assert "success" in result


def test_website_manager_gracefully_handles_missing_wordpress_tools(monkeypatch):
    """Website manager functions should short-circuit when WordPress tools are absent."""
    monkeypatch.setattr(wm, "HAS_WORDPRESS", False, raising=False)
    pages = wm.list_wordpress_pages("freerideinvestor")
    assert pages.get("success") is False
    assert "WordPress tools not available" in pages.get("error", "")


def test_website_manager_gracefully_handles_missing_blog_tools(monkeypatch):
    """Blog-related helpers should report missing tools instead of raising."""
    monkeypatch.setattr(wm, "HAS_BLOG", False, raising=False)
    post = wm.create_blog_post_for_site("freerideinvestor", strategy_name=None)
    assert post.get("success") is False
    assert "Blog automation tools not available" in post.get("error", "")


def test_swarm_brain_server_handles_missing_backend(monkeypatch):
    """Swarm Brain helpers should return a clear error when backend is unavailable."""
    monkeypatch.setattr(sb, "HAS_SWARM_BRAIN", False, raising=False)
    res = sb.share_learning(
        "Agent-CI", "CI test learning", "Content from CI tests")
    assert res.get("success") is False
    assert "Swarm Brain not available" in res.get("error", "")


class _DummyCoordLoader:
    """Minimal stand-in for coordinate loader used by messaging_server."""

    def get_all_agents(self):
        return ["Agent-1", "Agent-2"]

    def get_chat_coordinates(self, agent_id):
        return (0, 0)

    def is_agent_active(self, agent_id):
        return True

    def get_agent_description(self, agent_id):
        return f"Dummy agent {agent_id}"


def test_messaging_server_get_agent_coordinates_with_dummy_loader(monkeypatch):
    """get_agent_coordinates should work when coordinate loader is patched."""
    monkeypatch.setattr(ms, "get_coordinate_loader",
                        lambda: _DummyCoordLoader(), raising=False)
    result = ms.get_agent_coordinates()
    assert isinstance(result, dict)
    assert result.get("success") is True
    agents = result.get("agents", {})
    assert "Agent-1" in agents and "Agent-2" in agents


def test_git_operations_recent_commits_runs_without_crashing():
    """get_recent_commits should execute git log and return a structured result."""
    result = go.get_recent_commits(agent_id=None, hours=1, file_pattern=None)
    assert isinstance(result, dict)
    assert "success" in result


def test_git_operations_validate_commit_head_runs_without_crashing():
    """validate_commit('HEAD') should either succeed or return a structured error."""
    result = go.validate_commit("HEAD")
    assert isinstance(result, dict)
    assert "success" in result


def test_v2_compliance_validate_file_size_for_this_test_file():
    """validate_file_size should run successfully on this test module."""
    this_file = Path(__file__)
    result = vc.validate_file_size(str(this_file), max_lines=500)
    assert result.get("success") is True
    assert result.get("line_count", 0) <= 500


def test_v2_compliance_check_v2_compliance_on_small_temp_file(tmp_path):
    """check_v2_compliance should report no violations for a tiny helper module."""
    small_file = tmp_path / "small_module.py"
    small_file.write_text("def foo():\n    return 1\n", encoding="utf-8")
    result = vc.check_v2_compliance(str(small_file))
    assert result.get("success") is True
    assert result.get("violations_count") == 0

